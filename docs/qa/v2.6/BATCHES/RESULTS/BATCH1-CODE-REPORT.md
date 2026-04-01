# BATCH 1: Code vs Documentation Coherence Report

**Batch ID:** msgbatch_01UciRkApJME9VRggGhUy7Xa
**Completed at:** 2026-04-02 17:56:44.736992+00:00

---

## Calypso Phase 2-4 Scripts vs DOC-2 Architecture

## 1. Executive Summary

- **Scope mismatch is fundamental**: The code (`orchestrator_phase2.py`) implements a specific Calypso batch-dispatch workflow, while DOC-2 is a system-wide Technical Architecture document covering Memory Bank, Session Checkpoints, and Artifact ID schemas — these documents address largely non-overlapping concerns.
- **Artifact ID non-compliance**: The code saves batch artifacts using hardcoded filenames (`batch_id_phase2.txt`, implied metadata files) with no reference to the `BATCH-{YYYY-MM-DD}-{NNNN}` or `RPT-{YYYY-MM-DD}-{NNNN}` schema mandated in DOC-2 §5.1.
- **Model identifier undocumented**: The code uses `claude-haiku-4-5` (line 33), which appears nowhere in DOC-2's architecture documentation, leaving the model selection rationale untracked.
- **No session checkpoint integration**: The code performs a multi-step batch submission with no heartbeat, no `session-checkpoint.md` update, and no crash-recovery instrumentation as required by DOC-2 §4.3 (RULE MB-2).
- **Truncated code prevents full audit**: The submitted code is cut off mid-metadata-dict (line ~175), making it impossible to audit the complete output artifact naming, error handling, and any downstream phase logic.

---

## 2. Findings

### Finding 1 — Artifact Naming Violates DOC-2 §5.1 Schema
**File:** `orchestrator_phase2.py`, lines ~140–145 (output file construction)

```python
batch_id_file = output_path / "batch_id_phase2.txt"
```

DOC-2 §5.1 defines:
- Batch Jobs → `BATCH-{YYYY-MM-DD}-{NNNN}` (e.g., `BATCH-2026-04-01-0001`)
- Expert Reports → `RPT-{YYYY-MM-DD}-{NNNN}` (e.g., `RPT-2026-04-01-0001`)

The code uses a static, non-conformant filename `batch_id_phase2.txt`. There is no date-stamped, sequenced ID generation anywhere in the visible code. The metadata file (truncated) also appears to use a flat structure rather than the schema-compliant naming.

**Impact:** Artifacts produced by this script cannot be cross-referenced, searched, or archived using the system-wide artifact ID schema. Downstream scripts or humans looking for `BATCH-*` files will not find them.

---

### Finding 2 — No Session Checkpoint / Heartbeat Integration
**File:** `orchestrator_phase2.py` (entire file)
**DOC-2 Reference:** §4.2, §4.3, RULE MB-2

DOC-2 §4.3 mandates:
> Every 5 minutes during active work: Update `session-checkpoint.md.last_heartbeat`

A batch submission is a long-running operation (Anthropic Batch API jobs can take minutes to hours). The code:
- Does not read or write `memory-bank/hot-context/session-checkpoint.md`
- Does not update `last_heartbeat`
- Does not update `current_task` or `git_state`
- Does not check for crash state at startup

If this script is invoked from within a Roo Code session, the session checkpoint will go stale, triggering false crash detection on the next session start.

---

### Finding 3 — Model Selection Not Documented in Architecture
**File:** `orchestrator_phase2.py`, line 33
```python
MODEL = "claude-haiku-4-5"          # Cost-efficient for batch expert reviews
```
**DOC-2 Reference:** §1.1 (Core Components table)

DOC-2 §1.1 lists `Ollama` as the local LLM inference component and `proxy.py` as the Gemini Chrome proxy. There is no mention of direct Anthropic API usage, the `claude-haiku-4-5` model, or the Batch API as an architectural component. The inline comment provides a rationale ("cost-efficient") but this is not captured as an ADR in `decisionLog.md` as required by DOC-2 §3.2 (RULE MB-3).

---

### Finding 4 — No ADR for Batch API Architecture Decision
**File:** `orchestrator_phase2.py` (entire file)
**DOC-2 Reference:** §3.2 (RULE MB-3), §5.1 (`ADR-{YYYY-MM-DD}-{NNN}` format)

The choice to use the Anthropic Batch API for multi-agent PRD review is a significant architectural decision. DOC-2 §3.2 requires all Architecture Decision Records to be appended to `decisionLog.md`. No evidence exists in the code that this decision was recorded. The code does not reference, create, or update any ADR artifact.

---

### Finding 5 — Expert Agent Count Matches Documentation Implicitly, But Is Not Formally Specified
**File:** `orchestrator_phase2.py`, lines 38–170 (`EXPERT_AGENTS` list)
**DOC-2 Reference:** §1.1 (Calypso description: "Orchestration scripts")

DOC-2 §1.1 describes Calypso only as "Orchestration scripts" with no further detail. The 4-agent design (architecture, security, UX, QA), their JSON output schemas, severity levels (`HIGH|MEDIUM|LOW|INFO`), and the `findings[]` structure are entirely undocumented in DOC-2. This is not a code defect per se, but represents significant documentation debt — the architecture document does not describe what Calypso actually does.

---

### Finding 6 — Output Directory Convention Not Specified in DOC-2
**File:** `orchestrator_phase2.py`, line 35
```python
DEFAULT_OUTPUT_DIR = "batch_artifacts"
```
**DOC-2 Reference:** §3.1 (Memory Bank directory tree)

DOC-2 §3.1 defines the canonical directory structure under `memory-bank/`. The `batch_artifacts/` directory does not appear in this tree. It is unclear whether batch artifacts are intended to live inside or outside the Memory Bank, whether they are "hot" or "cold" context, and whether they should be under `archive-cold/` (MCP-only access per §3.1).

---

### Finding 7 — Truncated Code Prevents Complete Audit
**File:** `orchestrator_phase2.py`, line ~175 (truncated mid-statement)

```python
    metadata = {
        "batch_id": batch_id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "prd_ref": prd_path,
        "model": MODEL,
        "age   # <-- TRUNCATED
```

The metadata dict, the `main()` function, argument parsing, and any phase 3/4 scripts referenced in the audit title ("Phase 2-4 Scripts") are not present. This audit is therefore **partial**. Phase 3 (batch polling/retrieval) and Phase 4 (report synthesis) scripts — which would be most critical for artifact ID compliance and Memory Bank integration — could not be reviewed.

---

## 3. Inconsistencies Found

| Severity | Location | Description | Expected (per DOC-2) | Actual (in Code) |
|---|---|---|---|---|
| **P0** | `orchestrator_phase2.py:141` | Batch artifact filename does not conform to artifact ID schema | `BATCH-{YYYY-MM-DD}-{NNNN}.txt` or similar per §5.1 | Hardcoded `batch_id_phase2.txt` |
| **P0** | `orchestrator_phase2.py` (entire) | No session checkpoint integration for long-running batch job | Read/write `session-checkpoint.md`, update `last_heartbeat` per §4.3 RULE MB-2 | No checkpoint interaction whatsoever |
| **P1** | `orchestrator_phase2.py:33` | Model `claude-haiku-4-5` and Anthropic Batch API not documented as architectural components | Listed in §1.1 Core Components table or covered by an ADR | Absent from DOC-2 entirely |
| **P1** | `decisionLog.md` (implied) | Batch API architectural decision not recorded as ADR | `ADR-{YYYY-MM-DD}-{NNN}` entry in `decisionLog.md` per §3.2 RULE MB-3 | No ADR created or referenced |
| **P1** | `orchestrator_phase2.py:35` | `batch_artifacts/` output directory not in Memory Bank directory tree | Directory placement defined in §3.1 tree | Undefined placement, defaults to repo root |
| **P1** | DOC-2 §1.1 | Calypso's 4-agent design, JSON schemas, severity model entirely absent from architecture doc | Calypso internals documented in §1.1 or a dedicated section | Only "Orchestration scripts" — no detail |
| **P2** | `orchestrator_phase2.py` (entire) | Expert Report artifacts (`RPT-*`) not generated with schema-compliant IDs | `RPT-{YYYY-MM-DD}-{NNNN}` per §5.1 | Not visible in truncated code; likely absent |
| **P2** | DOC-2 §6 (v2.6 Changes) | No changelog entry for Calypso Phase 2 batch orchestration feature | New Calypso capabilities listed under §6.x | Absent from v2.6 changes section |

---

## 4. Prioritized Remediation

### P0 (Critical)

1. **Fix artifact naming to comply with DOC-2 §5.1:**
   - Replace `batch_id_phase2.txt` with a date-sequenced filename generator:
     ```python
     # Example: BATCH-2026-04-01-0001.json
     batch_artifact_id = f"BATCH-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{seq:04d}"
     batch_id_file = output_path / f"{batch_artifact_id}.txt"
     ```
   - Ensure Phase 3/4 scripts generate `RPT-{YYYY-MM-DD}-{NNNN}` IDs for expert reports.
   - Add a sequence counter mechanism (file-based or registry-based) to guarantee uniqueness.

2. **Integrate session checkpoint updates:**
   - At script start: read `memory-bank/hot-context/session-checkpoint.md`, check `last_heartbeat` staleness.
   - Before and after batch submission: update `last_heartbeat`, `current_task` (e.g., `"Submitting Phase 2 batch: {batch_id}"`).
   - On error/exception: update checkpoint status to `CRASHED` with error context.

### P1 (Important)

3. **Add Anthropic Batch API as a Core Component in DOC-2 §1.1:**
   ```markdown
   | **Anthropic Batch API** | Async multi-agent PRD review via claude-haiku-4-5 |
   ```
   Include model selection rationale and cost/latency tradeoffs.

4. **Create ADR for Batch API architectural decision:**
   - Append to `memory-bank/hot-context/decisionLog.md` per RULE MB-3.
   - Format: `ADR-{date}-{NNN}` covering: decision to use Anthropic Batch API, model choice, 4-agent design, JSON schema contract.

5. **Define `batch_artifacts/` placement in DOC-2 §3.1 Memory Bank tree:**
   - Decide: is this hot context (active batch jobs), cold archive (completed reports), or outside Memory Bank entirely?
   - Update the directory tree diagram accordingly.

6. **Expand DOC-2 §1.1 Calypso description** or add a new §7 (Calypso Architecture) covering:
   - Phase 2 (batch submission), Phase 3 (polling), Phase 4 (synthesis) pipeline
   - 4-agent roles and JSON output schema
   - Severity taxonomy (`HIGH|MEDIUM|LOW|INFO`)
   - PRD-to-backlog workflow

### P2 (Nice to Have)

7. **Add v2.6 changelog entry** in DOC-2 §6 for Calypso Phase 2-4 batch orchestration feature.

8. **Complete the audit** once Phase 3 and Phase 4 scripts are available — artifact ID compliance and Memory Bank write patterns in those scripts are likely the highest-risk areas.

9. **Document the `MAX_TOKENS = 2048` limit** as an architectural constraint — expert reports for large PRDs may be truncated, which is a quality risk worth noting in the architecture doc.

---

## 5. Verdict

**[MAJOR_INCONSISTENCIES]**

The code and documentation are misaligned at a structural level. The two most critical failures are: (1) artifact output naming completely ignores the system-wide ID schema defined in DOC-2 §5.1, which will break cross-referencing and archival workflows; and (2) the long-running batch orchestration script has zero integration with the session checkpoint system mandated by DOC-2 §4.3, creating crash-detection false positives. Additionally, the Anthropic Batch API — a core runtime dependency — is entirely absent from the architecture document, representing a significant documentation gap for a system that claims cumulative architecture coverage from v1.0 through v2.6.

---

## Session Heartbeat vs MB-4 Rule

## 1. Executive Summary

- The code file (`checkpoint_heartbeat.py`) references **"RULE MB-2"** in its docstring, but no such rule exists in the documentation; the closest analog is **RULE 1** (session read) and **RULE 2** (mandatory write at task close), neither of which describes a 5-minute heartbeat loop.
- The documentation contains **no mention whatsoever** of `checkpoint_heartbeat.py`, `session-checkpoint.md`, heartbeat intervals, PID files, or crash-recovery mechanisms — the entire feature is undocumented.
- The code's module-level docstring cites rule numbering (`MB-2`) that is inconsistent with the documentation's numbering scheme (`RULE 1` through `RULE 9+`), suggesting the code was written against a different or draft version of the spec.
- RULE 7 (large-file chunking) explicitly warns against PowerShell concatenation yet the documentation itself (RULE 7.4) still prescribes `Get-Content … | Set-Content` — an internal documentation contradiction that is unrelated to the code but worth flagging.
- The code is **truncated** (ends mid-function at `read_checkpoint_metadata`), making a complete audit impossible; several documented behaviors cannot be verified.

---

## 2. Findings

### F-1 — Rule Reference Mismatch (`checkpoint_heartbeat.py:14`)
The docstring states:
```
RULE MB-2: Session Checkpoint (Crash Recovery)
```
The documentation defines rules as `RULE 1` through `RULE 9` (and a partial `RULE 9`). There is no `RULE MB-2` anywhere in the provided documentation. The prefix `MB-` does not appear in the rule naming convention used by the docs.

### F-2 — Entire Feature Absent from Documentation
The following implementation concepts have **zero coverage** in the documentation:
- `session-checkpoint.md` file (path: `memory-bank/hot-context/session-checkpoint.md`)
- Heartbeat loop / 5-minute interval (`HEARTBEAT_INTERVAL = 300`, line 34)
- PID file mechanism (`.checkpoint_heartbeat.pid`, line 35)
- CLI flags `--start`, `--stop`, `--once`, `--status` (docstring lines 9–12)
- Crash recovery protocol
- `get_git_state()` function behavior (lines 39–88)
- `get_session_info()` function behavior (lines 91–102)

### F-3 — `session-checkpoint.md` Path vs. Documented Memory Bank Paths
The code writes to `memory-bank/hot-context/session-checkpoint.md`. The documentation (RULE 1, RULE 2, RULE 3) references:
- `memory-bank/activeContext.md`
- `memory-bank/hot-context/activeContext.md`
- `memory-bank/hot-context/progress.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/techContext.md`
- `memory-bank/productContext.md`
- `memory-bank/decisionLog.md`

`session-checkpoint.md` is not listed in any documented memory-bank file inventory.

### F-4 — Git State Fields Not Aligned with RULE 5
`get_git_state()` (lines 39–88) returns:
```python
{"branch", "last_commit", "last_commit_message", "staged_files", "modified_files", "untracked_files"}
```
RULE 5.5 states that `*.log` files must NOT be versioned. The code does not filter log files from `untracked_files`. More critically, RULE 5.2 defines *when* to commit, but the heartbeat writes git state without triggering any commit — this may conflict with the spirit of RULE 5.2 ("After updating the Memory Bank → commit").

### F-5 — Double Subprocess Execution Anti-Pattern (lines 55–88)
Each git command is executed **twice** (once for the conditional check, once for the actual value). This is a code-quality issue not addressed by any documentation guideline, but it also means the git state captured could be inconsistent between the two calls if the repo changes mid-execution.

### F-6 — RULE 7 Internal Contradiction (Documentation-only)
RULE 7.2 step 4 prescribes:
```powershell
Get-Content _temp_chunk_01.md, _temp_chunk_02.md | Set-Content target-file.md -Encoding UTF8
```
But RULE 6.5 (same document) explicitly states:
> "Never use PowerShell for file concatenation. The pattern `(Get-Content a) + (Get-Content b) | Set-Content out` silently produces a 1-line file…"

This is a direct internal contradiction within the documentation itself.

### F-7 — Truncated Code Prevents Full Audit
`read_checkpoint_metadata()` (line ~104) is cut off mid-comment (`# Parse frontmatter-like metad`). Functions for `--start`, `--stop`, `--status`, and the main heartbeat loop are entirely missing. Compliance with RULE 2 (write at task close), RULE 5.2 (commit after memory bank update), and RULE 9 (cold zone firewall) cannot be assessed.

### F-8 — `session_id` Generation Logic Undocumented
`get_session_info()` (lines 91–102) generates session IDs in the format `s{YYYY-MM-DD}-{SESSION_MODE}-001`. No documentation defines this format, the `SESSION_MODE` environment variable, or the session ID concept at all.

### F-9 — RULE 9 Reference Truncated in Documentation
The documentation itself is cut off at `memory-ban` (RULE 9.1). The "Hot Zone" definition is incomplete. This means any code that implements cold/hot zone access logic cannot be audited for compliance.

---

## 3. Inconsistencies Found

| Severity | Location | Description | Expected (Docs) | Actual (Code) |
|---|---|---|---|---|
| **P0** | `checkpoint_heartbeat.py:14` | Rule reference does not exist | Rule named `RULE 1`–`RULE 9` scheme | Code cites `RULE MB-2` |
| **P0** | Entire file | Heartbeat/crash-recovery feature has no documentation | Feature must be documented in the protocol | No corresponding rule or section exists |
| **P0** | `checkpoint_heartbeat.py:32` | `session-checkpoint.md` not in documented file inventory | Only known MB files listed in RULE 1–3 | New undocumented file written to `memory-bank/hot-context/` |
| **P1** | `checkpoint_heartbeat.py:39–88` | Git state capture may conflict with RULE 5.2 commit mandate | Writing to memory bank should trigger a git commit | Heartbeat writes MB file; no commit is triggered |
| **P1** | `checkpoint_heartbeat.py:55–88` | Each git command run twice; state may be inconsistent | Atomic, single-pass git state capture | Two `subprocess.check_output` calls per field |
| **P1** | `checkpoint_heartbeat.py:91–102` | `SESSION_MODE` env var and session ID format undocumented | All env vars and ID formats should be specified | Silently falls back to `unknown` mode |
| **P1** | Documentation RULE 7.2 vs RULE 6.5 | PowerShell concat prescribed then forbidden in same doc | Consistent guidance | Direct contradiction |
| **P2** | `checkpoint_heartbeat.py:35` | PID file `.checkpoint_heartbeat.pid` not in RULE 5.5 exclusion list | `.pid` files arguably should be in `.gitignore` / exclusion list | Not mentioned anywhere |
| **P2** | `checkpoint_heartbeat.py:104+` | Code truncated; `--start/--stop/--status` logic unauditable | Full implementation reviewable | Missing from provided code |
| **P2** | Documentation RULE 9 | Rule 9 definition is truncated | Complete rule definition | Cut off at `memory-ban` |

---

## 4. Prioritized Remediation

### P0 (Critical)

1. **Create a new rule in the documentation** (suggest `RULE 10: SESSION HEARTBEAT & CRASH RECOVERY`) that formally defines:
   - The 5-minute heartbeat interval and rationale
   - The `session-checkpoint.md` file path, schema, and lifecycle
   - The `--start / --stop / --once / --status` CLI contract
   - How this rule interacts with RULE 1 (session start) and RULE 2 (task close)

2. **Fix the rule reference in `checkpoint_heartbeat.py:14`**: Change `RULE MB-2` to the correct rule identifier once the documentation rule is created. Until then, the reference is dangerously misleading to any agent or developer reading the file.

3. **Add `session-checkpoint.md` to the documented memory-bank file inventory** in RULE 1 and RULE 3 so agents know to read it during session initialization.

### P1 (Important)

4. **Resolve the RULE 5.2 / heartbeat conflict**: Either (a) explicitly exempt heartbeat writes from the "commit after MB update" mandate in RULE 5.2, or (b) have the heartbeat script execute `git add` + `git commit` after each write. Document the chosen approach.

5. **Fix the double-subprocess anti-pattern** in `get_git_state()` (lines 55–88): Capture each command output once, assign to a variable, then test and split from that variable. This eliminates the race condition and halves subprocess overhead.

6. **Document `SESSION_MODE` environment variable**: Add to `memory-bank/techContext.md` or a new `ENV-VARS.md` the valid values, default behavior, and how it affects session ID generation.

7. **Resolve the PowerShell contradiction** between RULE 6.5 and RULE 7.2: RULE 7.2 step 4 must be updated to use the Python-based approach (`scripts/rebuild_sp002.py` pattern) consistent with RULE 6.5's explicit prohibition.

### P2 (Nice to have)

8. **Add `.checkpoint_heartbeat.pid` to RULE 5.5** (what must NOT be versioned) or to `.gitignore`, whichever is the canonical exclusion mechanism.

9. **Complete the truncated RULE 9** in the documentation so cold/hot zone access protocol is fully auditable.

10. **Provide the full `checkpoint_heartbeat.py` source** for a complete audit; the truncated `read_checkpoint_metadata()` and all CLI handler functions are currently unauditable.

---

## 5. Verdict

**[MAJOR_INCONSISTENCIES]**

The code implements a complete subsystem (session heartbeat, crash recovery, PID management, git state capture) that is entirely absent from the documentation. The rule reference in the code (`RULE MB-2`) points to a non-existent rule, meaning any agent or developer relying on the documentation to understand the system's behavior will have a fundamentally incomplete and misleading picture. The documentation also contains an internal self-contradiction (RULE 6.5 vs. RULE 7.2) that must be resolved independently of the code audit.

---

## Memory Bank vs DOC-1 PRD

# Code-vs-Documentation Coherence Audit Report
## Memory Bank (Active Context + Project Progress) vs DOC-1 PRD (v2.6)

---

## 1. Executive Summary

- **Release state mismatch**: The Memory Bank declares v2.6.0 as **RELEASED** with a frozen tag, but DOC-1 is still marked **DRAFT** — these two states are mutually exclusive and represent a critical governance inconsistency.
- **Incomplete feature delivery**: Several v2.6 requirements tracked in DOC-1 (REQ-MB-1.2 crash detection, REQ-DE-1 ENH tracking, REQ-PB-1.2/1.3 branch rules) have no corresponding completion evidence in the Memory Bank.
- **Artifact ID schema partially implemented**: The Memory Bank uses `sYYYY-MM-DD-{mode}-{NNN}` session IDs correctly (REQ-AI-1.4), but there is no evidence of `IDEA-`, `TECH-`, `ADR-`, or `ENH-` IDs being applied anywhere in the tracked work.
- **Open items carried into a "released" version**: The Project Progress file shows multiple unchecked items (`[ ]`) that belong to v2.6 scope, contradicting the release-complete status declared in Active Context.
- **DOC-1 cumulative claim is unverifiable**: DOC-1 asserts it is the single source of truth for v1.0–v2.6 requirements, but the Memory Bank references a parallel v2.0 release doc set (DOC-1..5-v2.0) that is described as frozen and canonical — creating a competing authority problem.

---

## 2. Findings

### Finding 1 — Release Status vs. Document Status Contradiction
**Active Context, line ~22:** `**v2.6.0 RELEASED** ✅` and `Tag: v2.6.0 on master`
**DOC-1, header block:** `status: Draft` and `> **Status: DRAFT** -- This document is in draft for v2.6.0 release. It will be frozen upon QA approval.`

A released version must have all its governing documents frozen. The PRD is the primary requirements contract. Shipping v2.6.0 with a DRAFT PRD means there is no frozen acceptance baseline — any post-release audit cannot definitively determine what was agreed upon.

---

### Finding 2 — Heartbeat / Crash Detection Partially Delivered
**DOC-1, §8.1, REQ-MB-1.2:** `checkpoint_heartbeat.py writes to session-checkpoint.md every 5 minutes`
**DOC-1, §8.1, REQ-MB-1.3:** `If last_heartbeat > 30 minutes, detect as potential crash`

**Active Context, v2.6 Release Summary:** Lists `scripts/checkpoint_heartbeat.py (NEW)` — file exists ✅
**Project Progress, Epic 2:**
```
- [ ] Phase 2: Implement heartbeat every 5 minutes
- [ ] Phase 2: Test crash recovery
```
Both Phase 2 items are **unchecked**. The script file may exist as a skeleton, but the acceptance criteria (5-minute write interval, 30-minute crash detection) are not confirmed as implemented or tested. This is a direct contradiction between "RELEASED" and open delivery tasks.

---

### Finding 3 — ENH Artifact ID Tracking (REQ-DE-1) Has No Evidence
**DOC-1, §8.4, REQ-DE-1.1–1.3:** Requires `ENH-YYYY-MM-DD-NNN` IDs, status lifecycle (DEFERRED → IN_PROGRESS → COMPLETED), and target_version on every enhancement.

**Memory Bank (both files):** Zero instances of any `ENH-` prefixed identifier. The v2.6 Release Summary mentions "New Rules: MB-1 through MB-4, G-0, D-1" — D-1 is the rule that mandates ENH tracking — but no ENH artifacts are registered anywhere in the Memory Bank. The rule exists; the practice does not.

---

### Finding 4 — TECH-SUGGESTIONS Archive Task Still Open
**Project Progress, Epic 2:**
```
- [ ] Phase 1: Archive TECH-SUGGESTIONS into IDEAS-BACKLOG
```
This is a Phase 1 item (same phase as session-checkpoint and APPEND ONLY, both marked complete). Phase 1 is partially delivered. The v2.6 Release Summary does not mention this task, suggesting it was silently dropped rather than formally deferred with a `REQ-DE-1`-compliant ENH record.

---

### Finding 5 — Plan-Branch Parity Evidence is Incomplete
**DOC-1, §8.3, REQ-PB-1.1:** Branch naming must follow `governance/PLAN-{ID}-{slug}`
**DOC-1, §8.3, REQ-PB-1.2:** Branches are never deleted after merge
**DOC-1, §8.3, REQ-PB-1.3:** PRs merge to `develop` or `develop-vX.Y`

**Active Context, Git state:** Shows `develop-v2.6` branch and PR #5 merged to `master` (not `develop` or `develop-vX.Y`). REQ-PB-1.3 specifies PRs target `develop` or `develop-vX.Y`, but the actual merge target was `master`. This is a direct violation of the documented acceptance criterion.

**Project Progress, Epic 2:** `Branch created: governance/PLAN-2026-04-01-001-ideation-release-v2` — naming pattern uses `governance/PLAN-{ID}-{slug}` ✅ for REQ-PB-1.1. However, no evidence that REQ-PB-1.2 (preservation policy) was verified post-merge.

---

### Finding 6 — Artifact ID Schema Partially Applied
**DOC-1, §8.2, REQ-AI-1.1–1.5:** Five artifact types require dated sequential IDs.

**Memory Bank evidence:**
| Artifact Type | Required Format | Found in Memory Bank |
|---|---|---|
| Session IDs | `sYYYY-MM-DD-{mode}-{NNN}` | ✅ Used consistently (s2026-04-01-developer-001, etc.) |
| Plan IDs | `PLAN-YYYY-MM-DD-NNN` | ✅ PLAN-2026-04-01-001 |
| IDEA IDs | `IDEA-YYYY-MM-DD-NNN` | ⚠️ Referenced as IDEA-001, IDEA-002 (old format, not date-based) |
| TECH IDs | `TECH-YYYY-MM-DD-NNN` | ❌ No instances found |
| ADR IDs | `ADR-YYYY-MM-DD-NNN` | ❌ No instances found |
| ENH IDs | `ENH-YYYY-MM-DD-NNN` | ❌ No instances found |

IDEA-001 and IDEA-002 in Project Progress use the legacy sequential format, not the `IDEA-YYYY-MM-DD-NNN` format required by REQ-AI-1.1. Migration of existing IDs is not addressed.

---

### Finding 7 — DOC-1 Cumulative Claim vs. Parallel v2.0 Doc Set
**DOC-1, header:** `cumulative: true` and `Do not rely on previous release documents -- they are delta-based and incomplete.`

**Project Progress, v2.0 Release Status section:** Lists DOC-1-v2.0 through DOC-5-v2.0 as `Frozen (2026-03-28)` with a QA report showing `28/28 PASS`. These are described as canonical frozen documents.

If DOC-1 v2.6 is cumulative and supersedes all prior docs, the v2.0 frozen set should be explicitly deprecated in the Memory Bank. Currently both are described as authoritative, creating ambiguity about which document governs requirements for features delivered in v2.0–v2.5.

---

### Finding 8 — SP-007 WARN Status Not Reflected in DOC-1
**Active Context, Coherence Status:** `SP-007 (Gem Gemini): WARN (manual deployment required)`

**DOC-1, §2.1, REQ-000:** Explicitly requires Gemini Chrome via proxy as one of the three LLM operating modes. A WARN status on this component means a core REQ-000 capability is degraded. DOC-1 contains no known-issues section, no risk register, and no acknowledgment of this degraded state at release time.

---

### Finding 9 — v2.5 Target in Progress.md vs. v2.6 Release
**Project Progress, Epic 2, last line:** `- [ ] Target: Release v2.5`

The Memory Bank declares v2.6.0 released, but the Epic 2 plan still shows `Target: Release v2.5` as an open checkbox. This suggests Epic 2 was originally scoped for v2.5, was carried into v2.6, and the plan was never updated to reflect the version change. This is a traceability gap.

---

### Finding 10 — DOC-1 Has No Section for v2.1–v2.4 Content
**DOC-1, Table of Contents:** Lists sections 3–6 for v2.1, v2.2, v2.3, v2.4 requirements respectively.

The provided DOC-1 excerpt jumps from §2 (v1.0) directly to §8 (v2.6). Sections 3–7 are referenced in the ToC but not present in the audited text. While this may be a truncation artifact of the audit submission, if these sections are genuinely absent from the document, the "cumulative" claim (Finding 7) is false — the document would not actually contain all requirements from v1.0 through v2.6.

---

## 3. Inconsistencies Found

| Severity | ID | Location | Description | Expected | Actual |
|---|---|---|---|---|---|
| P0 | F1 | Active Context ~L22 vs DOC-1 header | Release declared while PRD is still DRAFT | DOC-1 status = `Frozen` when v2.6.0 is tagged | DOC-1 status = `Draft`; v2.6.0 tag exists on master |
| P0 | F2 | Project Progress, Epic 2 `[ ]` items vs Active Context "RELEASED" | Heartbeat and crash recovery undelivered | REQ-MB-1.2 and REQ-MB-1.3 acceptance criteria met | Phase 2 tasks unchecked; no test evidence |
| P0 | F5 | Active Context Git state vs DOC-1 §8.3 REQ-PB-1.3 | PR merged to `master`, not `develop`/`develop-vX.Y` | PR target = `develop` or `develop-vX.Y` | PR #5 merged to `master` |
| P1 | F3 | Memory Bank (both files) vs DOC-1 §8.4 REQ-DE-1 | Zero ENH artifacts registered despite D-1 rule being "released" | ENH IDs in use with status lifecycle | No ENH IDs anywhere in Memory Bank |
| P1 | F4 | Project Progress Epic 2 `[ ]` Phase 1 item | TECH-SUGGESTIONS archive task silently dropped | Task completed or formally deferred with ENH ID | Unchecked, no ENH record, not in Release Summary |
| P1 | F6 | Project Progress IDEA-001/002 vs DOC-1 §8.2 REQ-AI-1.1 | Legacy IDEA IDs not migrated to dated format | `IDEA-YYYY-MM-DD-NNN` | `IDEA-001`, `IDEA-002` |
| P1 | F8 | Active Context SP-007 WARN vs DOC-1 §2.1 REQ-000 | Core LLM mode degraded at release with no documentation | All three LLM modes operational or degradation documented | SP-007 WARN with no risk note in DOC-1 |
| P1 | F9 | Project Progress Epic 2 target line | Version label mismatch in plan | `Target: Release v2.6` (checked) | `[ ] Target: Release v2.5` |
| P2 | F6b | Memory Bank vs DOC-1 §8.2 REQ-AI-1.2/1.3 | No TECH or ADR IDs in use | TECH and ADR dated IDs applied to artifacts | Zero instances in Memory Bank |
| P2 | F7 | Project Progress v2.0 section vs DOC-1 header | Competing authoritative document sets | v2.0 docs explicitly deprecated in Memory Bank | Both v2.0 frozen set and v2.6 cumulative doc described as authoritative |
| P2 | F10 | DOC-1 ToC §3–7 vs provided content | Sections 3–7 absent from audited DOC-1 text | Full cumulative content v1.0–v2.5 present | Only v1.0 (§2) and v2.6 (§8) content provided |

---

## 4. Prioritized Remediation

### P0 (Critical — blocks release integrity)

1. **Freeze DOC-1 or retract the v2.6.0 tag.** The release tag and DRAFT PRD status cannot coexist. Either: (a) complete QA approval and update DOC-1 `status: Frozen` before treating v2.6.0 as released, or (b) retract the tag and treat v2.6.0 as a release candidate until the PRD is frozen.

2. **Resolve the heartbeat/crash detection delivery gap.** REQ-MB-1.2 and REQ-MB-1.3 have open tasks in Project Progress. Before freezing DOC-1: either implement and test the 5-minute heartbeat and 30-minute crash detection (and check off the tasks), or formally defer them to v2.7 with an ENH record and remove them from the v2.6 acceptance table.

3. **Correct the PR merge target or update REQ-PB-1.3.** PR #5 merged to `master`, violating the documented acceptance criterion. Either: (a) amend the GitFlow rule to permit master as a valid target for release PRs and update DOC-1 §8.3, or (b) document this as a known deviation with a rationale ADR.

### P1 (Important — governance and traceability)

4. **Register all deferred items as ENH artifacts.** The TECH-SUGGESTIONS archive task and Phase 3 MCP integration are deferred but have no `ENH-YYYY-MM-DD-NNN` IDs. Create ENH records with `target_version` per REQ-DE-1 to make D-1 rule operational, not just declared.

5. **Migrate IDEA-001/002 to dated format or document a grandfather clause.** REQ-AI-1.1 requires `IDEA-YYYY-MM-DD-NNN`. Either migrate existing IDs and update all references, or add an explicit note in DOC-1 §8.2 that pre-v2.6 IDs are grandfathered.

6. **Add a Known Issues / Degraded State section to DOC-1.** Document SP-007 WARN status against REQ-000 so the release record accurately reflects the operational state of the Gemini Chrome mode at time of release.

7. **Update Epic 2 target label** from `Release v2.5` to `Release v2.6` and check it off (or formally close the epic) to maintain Memory Bank accuracy.

### P2 (Nice to have — hygiene and completeness)

8. **Deprecate v2.0 frozen doc set in Memory Bank.** Add a note in Project Progress (v2.0 Release Status section) pointing to DOC-1 v2.6 as the superseding cumulative document, eliminating the dual-authority ambiguity.

9. **Verify DOC-1 §3–7 completeness.** Confirm that sections covering v2.1–v2.5 requirements exist in the actual file. If the audit submission was truncated, no action needed; if sections are genuinely absent, the cumulative claim must be qualified.

10. **Begin applying TECH and ADR dated IDs** to new technical decisions and architecture records going forward, and add a one-time sweep task to backfill any undocumented decisions from v2.6 development.

---

## 5. Verdict

**[MAJOR

---

## SyncDetector + RefinementWorkflow vs DOC-3

# Code-vs-Documentation Coherence Audit: SyncDetector + RefinementWorkflow vs DOC-3

---

## 1. Executive Summary

- **The CODE and DOCUMENTATION describe entirely different systems.** DOC-3 is an implementation plan for Memory Bank enhancements and a heartbeat/checkpoint script; the code files implement a synchronization detection engine and a refinement workflow manager — neither of which is mentioned anywhere in DOC-3.
- **Zero functional overlap exists** between the code under audit (`sync_detector.py`, `refinement_workflow.py`) and the document under comparison (DOC-3 v2.6). There is no shared terminology, no shared file paths, no shared class names, and no shared behavioral contracts.
- **The code references concepts** (IDEAS-BACKLOG, TECH-SUGGESTIONS-BACKLOG, RULE 12.4, OverlapType, RefinementMode, IdeaState) that are entirely absent from DOC-3, which instead covers `session-checkpoint.md`, `checkpoint_heartbeat.py`, `decisionLog.md`, and governance plan execution.
- **DOC-3 does contain one tangential data point** — "Archive TECH-SUGGESTIONS into IDEAS-BACKLOG" (§3.1) — which shares vocabulary with the code, but it is a one-line checklist item with no specification, making it impossible to validate code behavior against it.
- **The audit cannot confirm consistency or inconsistency on any behavioral claim** because the document does not specify the behavior of either audited module. The pairing of this code against this document appears to be an incorrect audit target assignment.

---

## 2. Findings

### Finding 1 — Wrong Document Paired with Code

**Location:** Audit request metadata  
**Detail:** DOC-3 is titled *"Implementation Plan (v2.6)"* and covers three phases: Memory Bank Enhancements, Heartbeat Script, and MCP Integration (deferred). It contains zero specification for:
- Synchronization detection logic
- Overlap type classification (`CONFLICT`, `REDUNDANCY`, `DEPENDENCY`, `SHARED_LAYER`)
- Refinement mode determination (`ASYNC`, `HYBRID`, `SYNC`)
- Complexity scoring algorithm
- `IdeaState` lifecycle states
- `SyncReport` or `RefinementSession` data structures

Neither `sync_detector.py` nor `refinement_workflow.py` is listed in any file table in DOC-3 (§3.2, §4.3).

---

### Finding 2 — RULE 12.4 Referenced in Code, Absent from DOC-3

**Location:** `sync_detector.py:17` — `"""Sync categories as defined in RULE 12.4"""`  
**Detail:** The `OverlapType` enum docstring cites "RULE 12.4" as its normative source. DOC-3 contains no rule numbered 12.4. The Appendix (DOC-3 §Appendix) defines rules MB-1 through MB-4, G-0, and D-1 — none of which correspond to overlap/sync detection. The governing rule for this enum is unverifiable against the supplied documentation.

---

### Finding 3 — IdeaState Machine Defined in Code, Not in DOC-3

**Location:** `refinement_workflow.py:44–57`  
**Detail:** The code defines an 11-state lifecycle:
```
RAW → INTAKE_PROCESSING → REFINING → EVALUATING → REFINED →
ACCEPTED / REJECTED / DEFERRED → IMPLEMENTING → READY_FOR_QA → RELEASED
```
DOC-3 makes no mention of any idea lifecycle state machine, transition rules, terminal states, or guard conditions. This is a significant behavioral specification that exists only in code.

---

### Finding 4 — Complexity Scoring Algorithm Undocumented

**Location:** `refinement_workflow.py:72–124`  
**Detail:** `ComplexityScore.calculate()` implements a weighted keyword heuristic (e.g., "architecture" +2, "security" +2, "api" +1) with thresholds:
- Score ≤ 3 → `ASYNC`
- Score 4–6 → `HYBRID`
- Score 7–10 → `SYNC`

None of these thresholds, weights, keywords, or mode-selection rules appear in DOC-3. There is no specification to validate the algorithm against.

---

### Finding 5 — Architectural Layer Taxonomy Undocumented

**Location:** `sync_detector.py:85–93`  
**Detail:** `SyncDetector.ARCH_LAYERS` defines five layers (`data`, `api`, `auth`, `ui`, `infra`) with associated keyword lists used for `SHARED_LAYER` detection. DOC-3 contains no architectural taxonomy, no layer definitions, and no keyword-matching specification.

---

### Finding 6 — File Path Conventions in Code vs DOC-3

**Location:** `sync_detector.py:77–79` vs DOC-3 §3.2, §4.3  
**Detail:**

| Source | Paths Referenced |
|--------|-----------------|
| `sync_detector.py` | `docs/ideas/IDEAS-BACKLOG.md`, `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md`, `docs/ideas/<IDEA-ID>.md` |
| DOC-3 §3.2 | `memory-bank/hot-context/session-checkpoint.md`, `memory-bank/hot-context/decisionLog.md`, `plans/governance/...` |
| DOC-3 §4.3 | `scripts/checkpoint_heartbeat.py` |

No path overlap exists. The `docs/ideas/` directory is not referenced anywhere in DOC-3.

---

### Finding 7 — TECH-SUGGESTIONS Mention in DOC-3 §3.1

**Location:** DOC-3 §3.1, row 4: *"Archive TECH-SUGGESTIONS into IDEAS-BACKLOG — Not yet needed"*  
**Detail:** This is the only vocabulary overlap between the document and the code. However:
- It is a one-line status note, not a specification
- It describes an archival operation, not the detection/refinement logic in the code
- Status is "Not yet needed," meaning the feature is explicitly not yet in scope for v2.6
- `sync_detector.py` reads from `TECH-SUGGESTIONS-BACKLOG` at runtime (`sync_detector.py:100–111`), which may be premature relative to DOC-3's deferral of this archival step

---

### Finding 8 — Code Truncation (Incomplete Audit Surface)

**Location:** `sync_detector.py` — truncated after `load_idea_details` method signature  
**Location:** `refinement_workflow.py` — truncated mid-method in `to_markdown()`  
**Detail:** Both files are cut off before completion. This means:
- The full `detect_sync()` method (referenced in the module docstring) is not auditable
- The `RefinementWorkflow` class body is entirely absent
- `determine_mode()`, `start_sync_session()`, and `create_async_refinement_doc()` (all referenced in the module docstring) cannot be audited
- Any additional undocumented behavior in the truncated sections cannot be assessed

---

### Finding 9 — `SyncReport.to_markdown()` Severity Field Unused

**Location:** `sync_detector.py:68–70` (`SyncFinding.severity`) vs `sync_detector.py:88–100` (`SyncReport.to_markdown()`)  
**Detail:** `SyncFinding` declares a `severity` field (`HIGH`, `MEDIUM`, `LOW`) but `to_markdown()` never renders it in the output table. The table columns are `Candidate | Overlap Type | Detail | Recommendation` — severity is silently dropped. This is an internal code inconsistency (not a doc/code gap, since DOC-3 doesn't specify this), but it is a behavioral defect worth flagging.

---

### Finding 10 — Module Docstring Contracts vs Visible Code

**Location:** `sync_detector.py:1–11`, `refinement_workflow.py:1–14`  
**Detail:**

| Claimed in Docstring | Present in Visible Code |
|----------------------|------------------------|
| `detector.detect_sync("IDEA-015")` | Method not visible (truncated) |
| `workflow.determine_mode(idea_id)` | Method not visible (class body absent) |
| `workflow.start_sync_session(idea_id, conversation)` | Not visible |
| `workflow.create_async_refinement_doc(idea_id)` | Not visible |
| `result.mode == "synchronous"` | `RefinementMode.SYNC.value == "synchronous"` ✅ (consistent) |

---

## 3. Inconsistencies Found

| Severity | Location | Description | Expected (per DOC-3) | Actual (in Code) |
|----------|----------|-------------|----------------------|------------------|
| **P0** | Entire audit pairing | Code modules are not specified by DOC-3 at all | DOC-3 should describe `sync_detector.py` and `refinement_workflow.py` behavior | DOC-3 describes heartbeat script and memory bank files; zero overlap |
| **P0** | `sync_detector.py:17` | RULE 12.4 cited as normative source for `OverlapType` | Rule 12.4 should be defined in referenced documentation | DOC-3 contains no Rule 12.4; rules defined are MB-1–4, G-0, D-1 |
| **P0** | `sync_detector.py:100–111` | Code reads from `TECH-SUGGESTIONS-BACKLOG` at runtime | Per DOC-3 §3.1, archiving TECH-SUGGESTIONS is "not yet needed" (deferred) | Code actively parses the backlog as a live data source |
| **P1** | `refinement_workflow.py:44–57` | 11-state `IdeaState` machine has no specification in DOC-3 | State transitions, guards, and terminal states should be documented | Fully implemented in code with no governing spec in supplied doc |
| **P1** | `refinement_workflow.py:72–124` | Complexity scoring thresholds (≤3/≤6/>6) and keyword weights are undocumented | Thresholds and weights should appear in a specification document | Hardcoded in `ComplexityScore.calculate()` with no doc reference |
| **P1** | `sync_detector.py:85–93` | `ARCH_LAYERS` taxonomy (5 layers, keyword lists) has no specification | Layer definitions should be in a design document | Hardcoded dict in `SyncDetector` class |
| **P1** | `sync_detector.py:77–79` | `docs/ideas/` path convention not in DOC-3 | File layout should be documented | Hardcoded paths with no DOC-3 reference |
| **P2** | `sync_detector.py:68–70` + `88–100` | `SyncFinding.severity` field declared but not rendered in `to_markdown()` | Severity should appear in sync report output | Silently omitted from markdown table |
| **P2** | Both files | Both modules are truncated; `detect_sync()`, `RefinementWorkflow` class, and 4 public methods are not auditable | Full implementation should be present for audit | Incomplete code submitted for review |
| **P2** | DOC-3 Appendix | Rules MB-1–4, G-0, D-1 are defined but have no corresponding implementation in either audited file | If these rules govern the audited modules, they should be referenced in code | No cross-reference in either `.py` file |

---

## 4. Prioritized Remediation

### P0 (Critical)

1. **Identify and supply the correct governing document** for `sync_detector.py` and `refinement_workflow.py`. DOC-3 is an implementation execution log for Memory Bank/Heartbeat work — it is the wrong document for this audit. The correct document is likely a separate specification (e.g., a DOC covering RULE 12.4, the ideation workflow, or the sync detection design). This audit **cannot produce a meaningful consistency verdict** until the correct document is supplied.

2. **Resolve the TECH-SUGGESTIONS-BACKLOG tension:** DOC-3 §3.1 marks archiving TECH-SUGGESTIONS as "not yet needed." If `sync_detector.py` is already parsing `TECH-SUGGESTIONS-BACKLOG.md` as a live input, either (a) DOC-3 §3.1 must be updated to reflect that the backlog is already in use as a read source (not just an archive target), or (b) the code must be gated behind a feature flag until the archival step is formally complete.

3. **Locate or create the specification for RULE 12.4.** The `OverlapType` enum cites it as normative. If no such rule document exists, the enum docstring must be corrected and the rule must be formally written and published.

### P1 (Important)

4. **Document the `IdeaState` lifecycle.** The 11-state machine in `refinement_workflow.py:44–57` is a critical behavioral contract. A state transition diagram with guard conditions and terminal states must exist in a specification document and be cross-referenced from the code.

5. **Document the complexity scoring algorithm.** The thresholds (≤3 → ASYNC, ≤6 → HYBRID, >6 → SYNC), keyword weights, and scoring rationale in `ComplexityScore.calculate()` must be specified in a design document. Hardcoded magic numbers without a spec are a maintenance and auditability risk.

6. **Document the `ARCH_LAYERS` taxonomy.** The five-layer architecture model used for `SHARED_LAYER` detection should be defined in an architecture decision record (ADR) or design document, not only as a Python dict.

7. **Complete the code submission.** The truncated `load_idea_details()` method, the entire `RefinementWorkflow` class, and all four public methods referenced in the module docstring must be included in any future audit submission.

### P2 (Nice to Have)

8. **Fix the `severity` field rendering gap** in `SyncReport.to_markdown()`. Either add a `Severity` column to the markdown table or remove the `severity` field from `SyncFinding` to eliminate dead data.

9. **Add cross-references from code to governing rules.** Both modules should include docstring or comment references to their governing specification documents (e.g., `# See DOC-X §Y.Z` or `# Implements RULE 12.4`), making future audits tractable.

10. **Reconcile DOC-3 Appendix rules with code.** If MB-1 through MB-4, G-0, and D-1 are intended to govern behavior in these modules (e.g., G-0 Plan-Branch Parity, D-1 Deferred Enhancement Tracking), add explicit references in the code. If they do not apply, the audit scope should be clarified.

---

## 5. Verdict

**[MAJOR_INCONSISTENCIES]**

The primary finding is a **category mismatch**: the two Python modules submitted for audit implement an ideation synchronization and refinement workflow system, while DOC-3 specifies a memory bank enhancement and heartbeat script implementation plan. These are non-overlapping systems. No behavioral claim in the code can be validated against DOC-3, and no specification in DOC-3 can be traced to the code.

Secondary findings include an unresolvable normative reference (RULE 12.4), a potential premature use of a deferred data source (TECH-SUGGESTIONS-BACKLOG), a fully undocumented state machine, undocumented scoring thresholds, and incomplete code submission. Even if the correct governing document were supplied, the audit would require a full re-run against that document before any consistency verdict could be issued.

---

