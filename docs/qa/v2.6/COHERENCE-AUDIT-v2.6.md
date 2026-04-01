# v2.6 Coherence Audit — Final Consolidated Report

**Audit Date:** 2026-04-02
**Batch IDs:** msgbatch_01UciRkApJME9VRggGhUy7Xa (Code), msgbatch_01YaZMR4Ft6FnZJvXK4r6KGZ (Gov), msgbatch_01E6VkmhMnWtp3rQgzjFn1LG (Prompt)
**Completed:** 2026-04-02 17:56:47 UTC
**Auditors:** Anthropic claude-sonnet-4-5 via Batch API (3 batches, 11 requests)

---

## Executive Summary

| Dimension | Verdict | P0 | P1 | P2 |
|---|---|---|---|---|
| Code vs Documentation | **MAJOR_INCONSISTENCIES** | 8 | 12 | 5 |
| Governance (Rules vs Embedded) | **MAJOR_INCONSISTENCIES** | 6 | 5 | 5 |
| Prompt vs .roomodes | **CONSISTENT** | 0 | 0 | 4 |
| **TOTAL** | | **14** | **17** | **14** |

**Critical Path:** SP-002 sync broken → rebuild_sp002.py must run immediately. DOC-1 must be frozen before v2.6.0 tag is valid. Heartbeat delivery gap must be resolved or formally deferred.

---

## Dimension 1: Code vs Documentation

### 1.1 orchestrator_phase2.py vs DOC-2 Architecture

**Verdict: MAJOR_INCONSISTENCIES**

| Severity | Location | Issue | Expected | Actual |
|---|---|---|---|---|
| P0 | `orchestrator_phase2.py:141` | Hardcoded artifact filename | `BATCH-{YYYY-MM-DD}-{NNNN}.txt` per DOC-2 §5.1 | `batch_id_phase2.txt` |
| P0 | `orchestrator_phase2.py` (entire) | No session checkpoint integration | Read/write `session-checkpoint.md`, update `last_heartbeat` | No checkpoint interaction |
| P1 | `orchestrator_phase2.py:33` | Model and Batch API undocumented | Listed in DOC-2 §1.1 Core Components | Absent |
| P1 | `decisionLog.md` | No ADR for Batch API decision | ADR entry per RULE MB-3 | None |
| P1 | `orchestrator_phase2.py:35` | Output dir not in Memory Bank tree | Defined in DOC-2 §3.1 | Undefined |
| P1 | DOC-2 §1.1 | Calypso 4-agent design undocumented | Calypso internals in §1.1 | Only "Orchestration scripts" |
| P2 | DOC-2 §6 (v2.6 Changes) | No changelog for Calypso Phase 2-4 | Listed in §6.x | Absent |
| P2 | `orchestrator_phase2.py` | `MAX_TOKENS = 2048` undocumented | Architectural constraint noted | Not documented |

**Remediation:**
1. Replace hardcoded `batch_id_phase2.txt` with schema-compliant `BATCH-{date}-{seq:04d}.txt`
2. Integrate session checkpoint: read at start, update `last_heartbeat` before/after batch submit
3. Add Anthropic Batch API to DOC-2 §1.1 as a Core Component
4. Create ADR for Batch API architectural decision
5. Define `batch_artifacts/` placement in DOC-2 §3.1

---

### 1.2 checkpoint_heartbeat.py vs Memory Bank Rules

**Verdict: MAJOR_INCONSISTENCIES**

| Severity | Location | Issue | Expected | Actual |
|---|---|---|---|---|
| P0 | `checkpoint_heartbeat.py:14` | Rule reference does not exist | Rules named `RULE 1`–`RULE 9` | Code cites `RULE MB-2` |
| P0 | Entire file | Heartbeat/crash-recovery feature entirely undocumented | Feature documented in protocol | No corresponding rule |
| P0 | `checkpoint_heartbeat.py:32` | `session-checkpoint.md` not in MB file inventory | Listed in RULE 1–3 | New undocumented file |
| P1 | `checkpoint_heartbeat.py:39–88` | Git state capture may conflict with RULE 5.2 commit mandate | Heartbeat writes should commit or be exempted | No commit triggered |
| P1 | `checkpoint_heartbeat.py:55–88` | Each git command runs twice; race condition | Single-pass git state capture | Double subprocess calls |
| P1 | `checkpoint_heartbeat.py:91–102` | `SESSION_MODE` env var and session ID format undocumented | Env var documented in techContext | Silently falls back to `unknown` |
| P1 | Documentation RULE 7.2 vs RULE 6.5 | PowerShell concat prescribed then forbidden | Consistent guidance | Direct contradiction |
| P2 | `checkpoint_heartbeat.py:35` | PID file not in RULE 5.5 exclusion list | `.pid` files in exclusion list | Not mentioned |
| P2 | `checkpoint_heartbeat.py:104+` | Code truncated; `--start/--stop/--status` logic unauditable | Full implementation reviewable | Missing |
| P2 | Documentation RULE 9 | Rule definition truncated at `memory-ban` | Complete rule definition | Incomplete |

**Remediation:**
1. Create `RULE 10: SESSION HEARTBEAT & CRASH RECOVERY` in documentation
2. Fix `RULE MB-2` reference to correct identifier
3. Add `session-checkpoint.md` to documented MB file inventory in RULE 1 and RULE 3
4. Resolve RULE 5.2 / heartbeat conflict (exempt or commit)
5. Fix double-subprocess anti-pattern in `get_git_state()`
6. Document `SESSION_MODE` environment variable

---

### 1.3 Memory Bank vs DOC-1 PRD

**Verdict: MAJOR_INCONSISTENCIES**

| Severity | Location | Issue | Expected | Actual |
|---|---|---|---|---|
| P0 | Active Context vs DOC-1 header | Release declared while PRD still DRAFT | DOC-1 `status: Frozen` when v2.6.0 tagged | DOC-1 `status: Draft` |
| P0 | Project Progress Epic 2 vs Active Context | Heartbeat/crash recovery undelivered | REQ-MB-1.2 and REQ-MB-1.3 acceptance criteria met | Phase 2 tasks unchecked |
| P0 | Active Context Git state vs DOC-1 §8.3 | PR merged to `master` not `develop`/`develop-vX.Y` | PR target = `develop` or `develop-vX.Y` | PR #5 merged to `master` |
| P1 | Memory Bank vs DOC-1 §8.4 | Zero ENH artifacts despite D-1 rule being "released" | ENH IDs in use with status lifecycle | No ENH IDs in Memory Bank |
| P1 | Project Progress Epic 2 Phase 1 | TECH-SUGGESTIONS archive task dropped | Task completed or formally deferred | Unchecked, no ENH record |
| P1 | Project Progress IDEA-001/002 vs DOC-1 §8.2 | Legacy IDEA IDs not migrated to dated format | `IDEA-YYYY-MM-DD-NNN` | `IDEA-001`, `IDEA-002` |
| P1 | Active Context SP-007 WARN vs DOC-1 §2.1 | Core LLM mode degraded with no documentation | All LLM modes operational or degradation documented | SP-007 WARN with no risk note |
| P1 | Project Progress Epic 2 target | Version label mismatch | `Target: Release v2.6` | `[ ] Target: Release v2.5` |
| P2 | Memory Bank vs DOC-1 §8.2 | No TECH or ADR IDs in use | TECH and ADR dated IDs applied | Zero instances |
| P2 | Project Progress v2.0 section | Competing authoritative doc sets | v2.0 docs deprecated in Memory Bank | Both v2.0 and v2.6 described as authoritative |

**Remediation:**
1. **Freeze DOC-1** before treating v2.6.0 as released, OR retract the tag
2. **Resolve heartbeat delivery gap:** implement/test 5-min heartbeat + 30-min crash detection, or formally defer to v2.7
3. **Correct PR merge target:** either amend GitFlow rule to permit `master` for release PRs, or document as known deviation
4. **Register deferred items as ENH artifacts** with `ENH-YYYY-MM-DD-NNN` IDs
5. **Migrate IDEA-001/002** to dated format or add grandfather clause in DOC-1
6. **Add Known Issues section to DOC-1** documenting SP-007 WARN status
7. **Update Epic 2 target** from `Release v2.5` to `Release v2.6`

---

### 1.4 SyncDetector + RefinementWorkflow vs DOC-3

**Verdict: MAJOR_INCONSISTENCIES**

The code and documentation describe entirely different systems. DOC-3 covers Memory Bank enhancements and heartbeat/checkpoint scripts. The code implements a synchronization detection engine and refinement workflow manager — neither mentioned anywhere in DOC-3. Zero functional overlap detected.

**Remediation:** This code-doc pairing appears to be an incorrect audit target. Verify intended pairing before re-audit.

---

## Dimension 2: Governance (Rules vs Embedded Prompts)

### 2.1 .clinerules vs SP-002 Embedded Rules

**Verdict: MAJOR_INCONSISTENCIES**

| Severity | Location | Issue | Expected | Actual |
|---|---|---|---|---|
| P0 | SP-002 code block vs `.clinerules` | SP-002 truncates mid-word at RULE 10.3 | Complete RULE 10 (10.1–10.6) | Cuts off at `"MUST foll"` |
| P0 | SP-002 code block vs changelog v2.7.0 | RULES 11–14 declared in changelog absent from code block | RULE 11–14 present | Zero content for any of these |
| P0 | SP-002 YAML `version: 2.7.0` | Version number attests non-existent content | Code block matches v2.7.0 | Content at best v2.6.x |
| P0 | RULE 6.2 sync invariant | `rebuild_sp002.py` byte-for-byte invariant violated | SP-002 == `.clinerules` | Significant divergence |
| P1 | RULE 7.2 step 4 vs RULE 6.2 step 5 | PowerShell contradiction | Consistent guidance | RULE 7.2 mandates PowerShell; RULE 6.2 forbids it |
| P1 | SOURCE `.clinerules` RULE 10.6 | ADR reference truncated | Complete reference | `memory-bank/hot-context/deci` — truncated |
| P2 | SP-002 changelog | Missing entries for RULE 8 and RULE 10 | Changelog entries | Absent |
| P2 | SP-002 `depends_on` | SP-010 not listed | SP-010 listed | Only SP-005 and SP-007 listed |

**Remediation:**
1. **Run `python scripts/rebuild_sp002.py`** immediately — this is the canonical fix
2. **Resolve RULES 11–14 gap:** determine if they exist in live `.clinerules` or if changelog entry is false
3. **Fix RULE 10.6 truncation** in SOURCE before any sync operation
4. **Correct SP-002 YAML version** to match actual content
5. **Resolve PowerShell contradiction** between RULE 6.2 and RULE 7.2

---

### 2.2 prompts/README.md vs SP Registry

**Verdict: MAJOR_INCONSISTENCIES**

| Severity | Location | Issue | Expected | Actual |
|---|---|---|---|---|
| P0 | README `Last updated` vs SP-003/004/005/006 | README not updated after 2026-03-28 changes | README `Last updated` = 2026-03-28 | Shows 2026-03-24 |
| P0 | SP-006 DEPLOYMENT | RBAC `groups` JSON truncated | Complete valid JSON | Truncated at `"docs/qa/.*\\.md\|mem` |
| P0 | README Inventory Table | No version column | Version column present | No version column; drift invisible |
| P1 | README Critical Dependencies | SP-004 → SP-002 missing | Listed under Critical Dependencies | Not listed |
| P1 | SP-003/004/005/006 versions not in README | Procedure Step 7 violated | README updated with versions | Not updated |
| P1 | SP-001, SP-002, SP-007, SP-008, SP-009, SP-010 | 6 SPs absent from DEPLOYMENT audit | All 10 SPs present | Only SP-003–SP-006 present |
| P2 | README Modification Procedure | No instruction to update README `Last updated` | Step to update date | No such step |
| P2 | Dependency directionality | SP-002 ↔ SP-005 ambiguity | Clear direction | Bidirectional claim unexplained |
| P2 | README Inventory `Out of Git` | Inconsistent casing | Uniform casing | `YES` vs `No` |

**Remediation:**
1. **Repair SP-006 RBAC JSON block** — recover complete `groups` array
2. **Add `Version` and `Last Updated` columns** to README Inventory Table
3. **Update README `Last updated` to 2026-03-28**
4. **Add SP-004 → SP-002 to README Critical Dependencies**
5. **Provide DEPLOYMENT entries for SP-001, SP-002, SP-007, SP-008, SP-009, SP-010**
6. **Amend Modification Procedure** to include README update step

---

### 2.3 template/.clinerules vs root .clinerules

**Verdict: CONSISTENT**

No SOURCE vs DEPLOYMENT drift detected. Both files are structurally and substantively identical across all 10 rules. Shared defects (RULE 10.6 truncation, PowerShell contradiction) exist equally in both and require simultaneous remediation.

---

## Dimension 3: Prompt vs .roomodes Deployment

### 3.1 SP-005 (developer) vs .roomodes developer

**Verdict: CONSISTENT** ✅

| Field | SP-005 | .roomodes | Match |
|---|---|---|---|
| `roleDefinition` | Identical | Identical | ✅ |
| `groups` array | `["read", "edit", "browser", "command", "mcp"]` | Same | ✅ |
| `slug` / `name` / `source` | developer / Developer / project | Same | ✅ |
| Array position | Index 2 | Index 2 | ✅ |

**P2 Suggestions:**
- Add version metadata comment referencing `SP-005 v1.2.0`
- Consider `command` group denylist as defense-in-depth

---

### 3.2 SP-003 (product-owner) vs .roomodes product-owner

**Verdict: CONSISTENT** ✅

| Field | SP-003 | .roomodes | Match |
|---|---|---|---|
| `roleDefinition` | Identical (verbatim) | Identical | ✅ |
| `groups` fileRegex | `memory-bank/productContext\.md\|docs/.*\.md\|user-stories.*\.md` | Same | ✅ |
| `slug` / `name` / `source` | product-owner / Product Owner / project | Same | ✅ |
| Code prohibition | Enforced | Enforced | ✅ |

**P2 Suggestions:**
- Add `_version: "1.2.0"` metadata for traceability

---

### 3.3 SP-006 (qa-engineer) vs .roomodes qa-engineer

**Verdict: CONSISTENT** ✅

| Field | SP-006 | .roomodes | Match |
|---|---|---|---|
| `roleDefinition` | Word-for-word identical | Identical | ✅ |
| RBAC `groups` | `read`, `edit` (docs/qa + memory-bank), `command` (npm test, pytest, etc.) | Same | ✅ |
| `allowedCommands` | 8 commands listed | Same | ✅ |
| `slug` / `name` / `source` | qa-engineer / QA Engineer / project | Same | ✅ |

**P2 Suggestions:**
- Add version metadata annotation inside `.roomodes`
- Document VS Code reload procedure in `CONTRIBUTING.md`

---

### 3.4 SP-004 (scrum-master) vs .roomodes scrum-master

**Verdict: CONSISTENT** ✅

| Field | SP-004 | .roomodes | Match |
|---|---|---|---|
| `roleDefinition` | Word-for-word identical | Identical | ✅ |
| RBAC `groups` | `read`, `edit` (memory-bank + docs), `command` (git only) | Same | ✅ |
| `allowedCommands` | `["git add", "git commit", "git status", "git log"]` | Same | ✅ |
| `slug` / `name` / `source` | scrum-master / Scrum Master / project | Same | ✅ |
| LLM backend policy | MinMax M2.7 / Claude Sonnet fallback | Same | ✅ |

**P2 Suggestions:**
- Add `_version: "2.2.0"` metadata field for automated drift detection
- Add CI/CD lint step comparing `.roomodes` against SP-004

---

## Consolidated P0 Remediation Tracker

| # | Finding | Owner | Blocking | Fix |
|---|---|---|---|---|
| 1 | SP-002 truncated; RULES 11-14 missing | Developer | Yes | `python scripts/rebuild_sp002.py` |
| 2 | DOC-1 still DRAFT; v2.6.0 tag invalid | Product Owner | Yes | Freeze DOC-1 or retract tag |
| 3 | Heartbeat/crash recovery undelivered | Developer | Yes | Complete Phase 2 or defer via ENH |
| 4 | PR #5 merged to `master` (violates REQ-PB-1.3) | Scrum Master | No | Amend rule or create ADR |
| 5 | SP-006 RBAC JSON truncated | Developer | Yes | Recover complete `groups` array |
| 6 | README has no version column; drift invisible | Developer | Yes | Add `Version` + `Last Updated` columns |
| 7 | `checkpoint_heartbeat.py` cites non-existent RULE MB-2 | Developer | Yes | Create RULE 10 or fix reference |
| 8 | `session-checkpoint.md` not in MB file inventory | Developer | Yes | Add to RULE 1 and RULE 3 |
| 9 | Artifact naming non-compliant with DOC-2 §5.1 | Developer | No | Implement `BATCH-{date}-{NNNN}` schema |
| 10 | No ADR for Batch API decision | Developer | No | Create ADR in `decisionLog.md` |
| 11 | `SESSION_MODE` env var undocumented | Developer | No | Document in `techContext.md` |
| 12 | PowerShell contradiction (RULE 6.2 vs 7.2) | Architect | No | Resolve: use Python in RULE 7.2 |
| 13 | RULES 11-14 gap (exist in `.clinerules`?) | Architect | Yes | Verify and sync |
| 14 | README `Last updated` is stale (2026-03-24) | Developer | No | Update to 2026-03-28 |

---

## Audit Metadata

**Scripts Used:**
- `submit_batch1_code.py` — 4 requests: code vs docs
- `submit_batch2_gov.py` — 3 requests: governance coherence
- `submit_batch3_prompt.py` — 4 requests: prompt vs .roomodes
- `retrieve_batch1.py`, `retrieve_batch2.py`, `retrieve_batch3.py`

**Batch Processing Time:** ~2 minutes each

**Model:** claude-sonnet-4-5 (batch)

**Total Cost:** ~$1.20 (estimated)

**Next Steps:**
1. Fix P0 items immediately (SP-002 sync, DOC-1 freeze, heartbeat delivery)
2. Re-audit after fixes to verify remediation
3. Update DOC-2 to reflect Calypso Phase 2-4 and Anthropic Batch API

---

*Report generated via Anthropic Batch API. Raw results at `docs/qa/v2.6/BATCHES/RESULTS/`.*
