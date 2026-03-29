# QA Report — v2.3 Coherence Audit
**Date:** 2026-03-29
**QA Engineer:** Roo Code (Code mode, minimax/minimax-m2.7)
**Audit Type:** Full Coherence Audit via Anthropic Message Batch API
**Branch:** develop
**Method:** 3 async batches, 14 requests, 50% cost reduction vs synchronous

---

## Executive Summary

| Dimension | Verdict | P0 | P1 | P2 |
|-----------|---------|----|----|-----|
| Governance (SP vs .clinerules vs .roomodes) | **MAJOR_INCONSISTENCIES** | 3 | 4 | 5 |
| Cross-Document (DOC-1..5, v1.0→v2.2) | **MINOR_DRIFT** | 0 | 3 | 6 |
| Template Sync (.clinerules, .roomodes, Modelfile, proxy.py) | **MAJOR_DRIFT** | 2 | 4 | 3 |
| Implementation vs Documentation (calypso, memory-bank) | **MAJOR_DRIFT** | 2 | 5 | 3 |
| **Overall** | **MAJOR_REMEDIATION REQUIRED** | **7** | **16** | **17** |

**Batch API Cost:** $0.21 for 14 requests (vs ~$0.42 synchronous)
**Batches:** msgbatch_0155bidg6RmPsSYWczTTxBkD (gov), msgbatch_01H1mhdtqCPdu5wweGL2q8L3 (xd), msgbatch_01G17QJW3DQzznMApr7J1LLz (template)

---

## 1. Governance Coherence (BATCH 1)

### 1.1 SP-002 vs .clinerules — MAJOR_INCONSISTENCIES

#### P0 Issues (Critical)

| # | Issue | Files Affected | Fix Required |
|---|-------|----------------|--------------|
| **P0-A** | UTF-8 BOM (`\ufeff`) present at file start | `.clinerules` (root), `SP-002` | Remove BOM from both files |
| **P0-B** | Em-dash mojibake: `—` → `â€"â€` throughout Rules 5-7 | `.clinerules`, `SP-002 Prompt Content` | Re-encode as proper UTF-8 |
| **P0-C** | Arrow mojibake: `→` → `Ã¢€š` in RULE 1 CHECK→CREATE→READ→ACT | `.clinerules` (root) | Re-encode as proper UTF-8 |
| **P0-D** | RULE 10 contains literal `\n` backslash-n sequences (not real newlines) | Both `.clinerules`, both `SP-002` embeddings, `template/.clinerules` | Replace `\n` with actual newlines |
| **P0-E** | SP-002 double-embedded: `.clinerules` content appears TWICE with different LLM backend values | `prompts/SP-002-clinerules-global.md` | Remove second embedding, fix first |
| **P0-F** | Second SP-002 embedding missing RULE 10 entirely | `prompts/SP-002-clinerules-global.md` | Align with first embedding |

**Root cause:** Files saved as UTF-8 but read/copied through a Latin-1/Windows-1252 pipeline, producing double-encoding mojibake. The BOM indicates original UTF-8 save.

**Evidence from batch audit:**
```
Root .clinerules title: # PROTOCOL le workbench â€"â€ MANDATORY DIRECTIVES
Should be:             # PROTOCOL le workbench — MANDATORY DIRECTIVES
```

#### P1 Issues (Important)

| # | Issue | Fix |
|---|-------|-----|
| **P1-A** | `.clinerules` root has EXTRA `\x9d` byte (worse corruption than template) | Copy template/.clinerules to root/.clinerules |
| **P1-B** | `activeContext.md` template in SP-002 first embedding shows old LLM backend `[Ollama uadf-agent \| Proxy Gemini \| Claude Sonnet API]` | Update to MinMax M2.7 via OpenRouter |
| **P1-C** | Second embedding shows different corruption variant for arrows | Normalize to single clean embedding |
| **P1-D** | `prompts/README.md` Last updated: 2026-03-24 but SP-002 updated 2026-03-28 | Update timestamp to 2026-03-28 |

#### P2 Issues (Nice to Have)

| # | Issue |
|---|-------|
| **P2-A** | SP-002 YAML front matter uses `hors_git: false` while SP-008/009/010 use `sp_id` — schema inconsistency |
| **P2-B** | SP-004/Sp-005 `depends_on SP-002` not listed in README Critical Dependencies |
| **P2-C** | Rules 8 and 9 use `--` workaround (not `—`) — inconsistency with Rules 5-7 |
| **P2-D** | No CI encoding validation for BOM/mojibake detection |
| **P2-E** | SP-002 second embedding has single blank lines vs double in first embedding |

---

### 1.2 SP-003..006 vs .roomodes — SYNCHRONIZED ✅

All four personas: **byte-identical** between SP files and `.roomodes` deployment.

| Persona | roleDefinition Match | RBAC Match |
|---------|---------------------|------------|
| product-owner (SP-003) | ✅ IDENTICAL | ✅ Consistent |
| scrum-master (SP-004) | ✅ IDENTICAL | ✅ Consistent |
| developer (SP-005) | ✅ IDENTICAL | ✅ Consistent |
| qa-engineer (SP-006) | ✅ IDENTICAL | ✅ Consistent |

**No remediation required.**

---

### 1.3 prompts/README.md vs SP Registry — ACCURATE (minor P2 only)

| Check | Result |
|-------|--------|
| All 10 SP files exist | ✅ 10/10 |
| Deployment targets accurate | ✅ 10/10 |
| Orphaned files | None |
| Missing from inventory | None |

**P2 only:** Stale `Last updated` timestamp (P1-D above).

---

### 1.4 .clinerules (root) vs template/.clinerules — MAJOR_DRIFT

See Section 3.1 (Template Sync) for full analysis.

---

## 2. Cross-Document Coherence (BATCH 2)

### 2.1 DOC-1 v2.2 vs DOC-2 v2.2 — CONSISTENT ✅

- v2.2 is a documentation-only hygiene release
- All 4 scope items are documentation/governance actions requiring no architectural coverage
- No contradictions found
- No scope creep detected

**P2 observations only:**
- P2-001: Implicit inheritance without explicit traceability link (recommend "Inherited Baseline" section)
- P2-002: DOC-2 v2.2 doesn't cross-reference DOC-3 v2.2 step log

---

### 2.2 DOC-2 v2.2 vs DOC-3 v2.2 — CONSISTENT ✅

- DOC-2 correctly declares no architectural changes
- DOC-3 correctly implements exactly 4 documentation-only steps
- No tool inconsistencies
- No phase misalignments

**Flagged for separate review:** `commit be601df` (Step 4) absent from DOC-5 commit list — DOC-3/DOC-5 traceability gap.

---

### 2.3 Version Continuity v2.0→v2.1→v2.2 — MINOR_DRIFT

**P1 Issues:**

| # | Issue | Fix |
|---|-------|-----|
| **P1-E** | Commit `ce3092e` (v2.1 message) appears in v2.2 release notes log unexplained | Add annotation explaining inclusion |
| **P1-F** | v2.1 governance bypass has no formal exception ADR | Create ADR-006 (or equivalent) to ratify bypass |
| **P1-G** | `batch_artifacts/.gitignore` referenced in release notes but untraced | Add commit reference or backlog item ID |

**P2 Issues:**

| # | Issue |
|---|-------|
| **P2-F** | GitFlow/ADR-005 not explicitly named in v2.2 preservation statement |
| **P2-G** | IDEA-008 (MinMax M2.7) not explicitly named in v2.2 |
| **P2-H** | Delta-only docs (DOC-2/3/4 v2.2) are fragile audit chains |
| **P2-I** | "DOC6 P0 issues" reference opaque without v2.1 context |

---

### 2.4 DOC-N-CURRENT.md Pointers — CORRECT ✅

All 5 pointer files (DOC-1 through DOC-5) correctly point to `docs/releases/v2.2/DOC-N-v2.2-*.md` with matching metadata.

**P2 only:** Filesystem verification not performed from live disk (recommend post-freeze gate).

---

## 3. Template Sync (BATCH 3)

### 3.1 .clinerules — MAJOR_DRIFT

**Both root and template have:**
- UTF-8 BOM (P0-A)
- Em-dash mojibake `â€"â€` (P0-B)
- Arrow mojibake (P0-C variant differs)
- Literal `\n` in RULE 10 (P0-D)

**Root-specific additional issues:**
- Extra `\x9d` byte after each em-dash (worse corruption than template)

**Fix:** Copy `template/.clinerules` → `.clinerules` (root), then fix encoding in both.

---

### 3.2 .roomodes — SYNCHRONIZED ✅

Root and template `.roomodes` are **byte-identical**. No remediation required.

---

### 3.3 Modelfile — SYNCHRONIZED ✅

Root and template `Modelfile` are **byte-identical**. No remediation required.

---

### 3.4 proxy.py — CRITICAL DRIFT (P0)

| Version | Status |
|---------|--------|
| Root | `v2.8.0` |
| Template | `v2.1.1` (7 patches behind) |

**P0 functional issues in template/proxy.py:**

| # | Issue | Impact |
|---|-------|--------|
| **P0-G** | SSE 2-chunk format instead of 3-chunk | `"Model Response Incomplete"` in Roo Code |
| **P0-H** | GEM MODE sends full history with injection tags | Context contamination in Gemini |
| **P0-I** | XML validation non-blocking (returns invalid responses) | Infinite request loops |
| **P0-J** | No injection tag stripping (`_extract_user_text` absent) | GAP R2-004/R2-005 hits immediately |

**P1 issues:**
- Missing `re` import (would crash if fixes backported)
- Missing `_unescape_markdown` (FIX-027)
- Missing `_has_escaped_xml` (FIX-021)

**Fix:** Copy `proxy.py` → `template/proxy.py` (strip DIAG logs if desired).

---

### 3.5 impl-calypso vs DOC-2 — MAJOR_DRIFT (documentation gap)

**Critical caveat:** DOC-2 v2.2 is a tombstone (zero architectural content), DOC-2 v2.1 was not provided.

**Implementation assessment (against inferred architecture):**

| Component | Status |
|-----------|--------|
| orchestrator_phase2.py | ✅ Implemented |
| check_batch_status.py | ✅ Implemented |
| orchestrator_phase3.py | ✅ Implemented |
| orchestrator_phase4.py | ✅ Implemented |
| triage_dashboard.py | ✅ Implemented |
| apply_triage.py | ✅ Implemented |
| fastmcp_server.py | ✅ Implemented |
| librarian_agent.py | ✅ Implemented |
| SP-008/SP-009 inline duplication | ⚠️ **P1**: Should load from prompts/ registry |
| final_backlog.json schema | ⚠️ **P1**: Missing, no validation |
| memory-archive.ps1 PowerShell-only | ⚠️ **P1**: Breaks on Linux/macOS |

**P2 issues:**
- Markdown fence stripping uses fragile heuristic
- `claude-haiku-4-5` model name format non-standard
- Version hardcoded vs sourced from `__init__.py`

---

### 3.6 memory-bank vs DOC-2 Section 4 — MAJOR_DRIFT

**P0 structural violation:**

| # | Issue | Fix |
|---|-------|-----|
| **P0-K** | `memory-bank/techContext.md` at ROOT level (outside hot-context/) | Move to `memory-bank/hot-context/techContext.md` |
| **P0-L** | DOC-2 v2.2 has no Section 4 content | Obtain DOC-2 v2.1 for actual spec |

**P1 issues:**

| # | Issue |
|---|-------|
| **P1-J** | `memory-bank/projectBrief.md` at root level — undefined boundary placement |
| **P1-K** | `archive-cold/sprint-logs/` existence unconfirmed |
| **P1-L** | `archive-cold/completed-tickets/` existence unconfirmed |
| **P1-M** | `hot-context/systemPatterns.md` is entirely template-stub |

**P2 issues:**
- `hot-context/productContext.md` has unpopulated template stubs (US-001, US-002)
- `decisionLog.md` has mixed CRLF/LF

---

## 4. Consolidated Remediation Tracker

### P0 — Must Fix Before Next Release

| ID | Category | Issue | Action |
|----|----------|-------|--------|
| P0-A | Encoding | UTF-8 BOM in .clinerules and SP-002 | Remove BOM from both files |
| P0-B | Encoding | Em-dash mojibake `â€"â€` | Re-encode as UTF-8 `—` |
| P0-C | Encoding | Arrow mojibake `Ã¢€š` | Re-encode as UTF-8 `→` |
| P0-D | Encoding | RULE 10 literal `\n` | Replace with actual newlines |
| P0-E | Governance | SP-002 double-embedded | Consolidate to single clean embedding |
| P0-F | Governance | Second SP-002 embedding missing RULE 10 | Align with first embedding |
| P0-G | Template | proxy.py SSE broken 2-chunk format | Sync template to v2.8.0 |
| P0-H | Template | GEM MODE sends full injection history | Sync template to v2.8.0 |
| P0-I | Template | XML validation non-blocking | Sync template to v2.8.0 |
| P0-J | Template | No injection tag stripping | Sync template to v2.8.0 |
| P0-K | Memory | techContext.md outside hot-context/ | Move to hot-context/ |
| P0-L | Docs | DOC-2 v2.2 has no Section 4 | Obtain DOC-2 v2.1 |

### P1 — Fix Before or During Next Sprint

| ID | Category | Issue |
|----|----------|-------|
| P1-A | Encoding | Root .clinerules worse corruption than template |
| P1-B | Governance | SP-002 first embedding old LLM backend |
| P1-C | Governance | SP-002 embeddings have different corruption variants |
| P1-D | Docs | README Last updated timestamp stale |
| P1-E | Release | ce3092e commit unexplained in v2.2 notes |
| P1-F | Release | v2.1 governance bypass unratified |
| P1-G | Release | batch_artifacts/.gitignore untraced |
| P1-J | Memory | projectBrief.md boundary placement undefined |
| P1-K | Memory | archive-cold/sprint-logs/ unconfirmed |
| P1-L | Memory | archive-cold/completed-tickets/ unconfirmed |
| P1-M | Memory | systemPatterns.md entirely template-stub |
| P1-N | Calypso | SP-008/SP-009 inline duplication |
| P1-O | Calypso | final_backlog.json schema missing |
| P1-P | Calypso | memory-archive.ps1 PowerShell-only |

### P2 — Schedule for Next Backlog Grooming

| ID | Category | Issue |
|----|----------|-------|
| P2-A | Schema | SP YAML front matter inconsistency |
| P2-B | Governance | README Critical Dependencies incomplete |
| P2-C | Encoding | Rules 8/9 `--` vs Rules 5-7 `—` |
| P2-D | CI | No encoding validation in CI |
| P2-E | SP-002 | Blank line inconsistency between embeddings |
| P2-F | Release | GitFlow/ADR-005 not explicit in v2.2 |
| P2-G | Release | IDEA-008 not explicit in v2.2 |
| P2-H | Release | Delta-only docs fragile audit chain |
| P2-I | Release | DOC6 P0 issues reference opaque |
| P2-J | Memory | productContext.md unpopulated stubs |
| P2-K | Memory | decisionLog.md mixed line endings |
| P2-L | Calypso | Fragile markdown fence stripping |
| P2-M | Calypso | claude-haiku-4-5 model name non-standard |
| P2-N | Calypso | Version hardcoded vs __init__.py |
| P2-O | Template | MODELINE no digest SHA pinning |
| P2-P | Template | DIAG logs in template proxy.py |

---

## 5. Batch API Execution Summary

| Batch | ID | Requests | Cost | Status |
|-------|-----|----------|------|--------|
| BATCH1: Governance | msgbatch_0155bidg6RmPsSYWczTTxBkD | 4 | ~$0.06 | ✅ Completed 22:25:08 |
| BATCH2: Cross-Docs | msgbatch_01H1mhdtqCPdu5wweGL2q8L3 | 4 | ~$0.06 | ✅ Completed 22:25:18 |
| BATCH3: Template | msgbatch_01G17QJW3DQzznMApr7J1LLz | 6 | ~$0.09 | ✅ Completed 22:25:27 |
| **Total** | | **14** | **$0.21** | **All successful** |

**Savings vs synchronous:** ~$0.21 vs ~$0.42 (50% reduction)
**Model:** claude-sonnet-4-6 (temperature=0.3, max_tokens=4096)
**SDK:** anthropic v0.86.0, `message_batch_id` parameter

---

## 6. Verdict

**Overall: MAJOR_REMEDIATION REQUIRED**

The project has **7 P0 critical issues** requiring immediate remediation before any new feature work or release:
1. Encoding corruption in `.clinerules` and `SP-002` (BOM, mojibake, literal `\n`)
2. SP-002 double-embedding with missing RULE 10
3. `template/proxy.py` 7 versions behind, causing functional breakage in new projects
4. `techContext.md` misplaced outside HOT/COLD boundary

**Estimated fix effort:** 3-4 hours (encoding fixes + template sync + file moves)

**Recommended order:**
1. Fix `.clinerules` encoding (copy from template, fix both)
2. Fix SP-002 double-embedding
3. Sync `template/proxy.py` to v2.8.0
4. Move `techContext.md` to hot-context/
5. Update prompts/README.md timestamp
6. Create ADR for v2.1 governance bypass ratification
7. Update DOC-2 v2.2 with Section 4 from v2.1

---

## 7. Evidence

Full batch results available at:
- [`plans/batch-full-audit/RESULTS/BATCH1-GOVERNANCE-REPORT.md`](plans/batch-full-audit/RESULTS/BATCH1-GOVERNANCE-REPORT.md)
- [`plans/batch-full-audit/RESULTS/BATCH2-CROSSDOCS-REPORT.md`](plans/batch-full-audit/RESULTS/BATCH2-CROSSDOCS-REPORT.md)
- [`plans/batch-full-audit/RESULTS/BATCH3-TEMPLATE-REPORT.md`](plans/batch-full-audit/RESULTS/BATCH3-TEMPLATE-REPORT.md)
