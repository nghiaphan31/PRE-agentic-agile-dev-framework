# IDEA-032: Fix Minor Gaps — Documentation Consistency (P2)

**Status:** [REFINED]
**Created:** 2026-04-09
**Refined:** 2026-04-09
**Source:** v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md)
**Priority:** P2
**Effort:** M (Medium)
**Target:** v2.17

## Problem Statement

17 minor documentation inconsistencies across 11 files that affect project coherence. These include incorrect references, stale pointers, missing updates after refactoring, and inconsistent formatting/terminology.

## Identified Issues

Based on the v2.15 consistency synthesis, the following minor gaps were identified:

### 1. F-005: .roomodes Missing Orchestrator Mode Reference

| Property | Value |
|----------|-------|
| File | `.roomodes` |
| Rule Reference | RULE 16.5 |
| Issue | Orchestrator is referenced as built-in mode but `.roomodes` defines only 4 Scrum roles |
| Fix | Add Orchestrator to `.roomodes` with reference to RULE 16 |

### 2. F-006: prompts/README.md SP-002 Version Mismatch

| Property | Value |
|----------|-------|
| File | `prompts/README.md` |
| Issue | SP-002 listed as v2.8.0, actual file is v2.9.0 |
| Fix | Update README to reflect v2.9.0 |

### 3. F-007: Template DOC-CURRENT Pointers Stale

| Property | Value |
|----------|-------|
| Files | `template/docs/DOC-1-CURRENT.md`, `template/docs/DOC-2-CURRENT.md`, `template/docs/DOC-4-CURRENT.md` |
| Issue | Point to v2.4, should point to latest (v2.15 or v2.16) |
| Fix | Update template DOC-CURRENT pointers |

### 4. F-008: HJ-004 — IDEA-022 Status Inconsistency

| Property | Value |
|----------|-------|
| File | `docs/ideas/IDEA-022-ideation-to-release-journey.md` |
| Issue | Status shows `[IDEA]` despite `[IMPLEMENTED]` in progress.md |
| Fix | Update IDEA-022 status to [IMPLEMENTED] |

### 5. F-009: HJ-005 — IDEA-022 Acceptance Criteria Unchecked

| Property | Value |
|----------|-------|
| File | `docs/ideas/IDEA-022-ideation-to-release-journey.md` |
| Issue | Acceptance criteria unchecked; DOC-4 chapter referenced but incomplete |
| Fix | Verify and mark criteria complete |

### 6. F-010: HJ-006 — Hotfix Path Missing from PLAN-IDEA-022

| Property | Value |
|----------|-------|
| File | `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` |
| Issue | Hotfix branch pattern not documented in TOC |
| Fix | Add hotfix pattern to documentation |

### 7. F-011: HJ-007 — PLAN-IDEA-022 §X.8 QA Entry Criteria Wrong

| Property | Value |
|----------|-------|
| File | `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` |
| Issue | QA entry criteria says "merge before QA" but should be "QA before merge" |
| Fix | Correct the QA entry criteria |

### 8. F-012: GF-005 — Cumulative Docs (v2.9) Use Deprecated Branch Names

| Property | Value |
|----------|-------|
| Files | `docs/releases/v2.9/*` |
| Issue | Uses `develop-v*` instead of `stabilization/v*` |
| Fix | Note as historical, no change needed (frozen release) |

### 9. F-013: GF-006 — Hotfix Pattern Mismatch

| Property | Value |
|----------|-------|
| Files | Multiple docs |
| Issue | Hotfix pattern shows `hotfix/vX.Y.Z` vs `hotfix/{Ticket}` |
| Fix | Standardize to `hotfix/{Ticket}` per RULE 10.1 |

### 10. F-014: GF-007 — release-gate.yml Summary Missing fast-forward Step

| Property | Value |
|----------|-------|
| File | `.github/workflows/release-gate.yml` |
| Issue | Summary output missing fast-forward develop step |
| Fix | Add fast-forward step to workflow summary |

### 11. F-015: DP-003 — Calypso Orchestrator Phases Not Referenced

| Property | Value |
|----------|-------|
| File | `docs/ideas/IDEA-022-ideation-to-release-journey.md` |
| Issue | Calypso orchestrator phases (Phase 2-4) not mentioned in journey |
| Fix | Reference Calypso phases in appropriate steps |

### 12. F-016: DP-004 — DOC-3 v2.15 Shows PENDING for Completed Step

| Property | Value |
|----------|-------|
| File | `docs/releases/v2.15/DOC-3-v2.15-Implementation-Plan.md` |
| Issue | Step marked PENDING is actually done |
| Fix | Update step status |

### 13. F-017: MS-002 — .roomodes Has No Orchestrator Entry

| Property | Value |
|----------|-------|
| File | `.roomodes` |
| Issue | Orchestrator mode not listed despite being built-in per RULE 16.5 |
| Fix | Add Orchestrator to `.roomodes` |

### 14. F-018: MS-003 — Handoff Schema Not Enforced by Automation

| Property | Value |
|----------|-------|
| File | `memory-bank/hot-context/handoff-state.md` |
| Issue | Handoff schema documented but no validation automation |
| Fix | Consider adding schema validation |

### 15. F-019: RB-003 — rebuild_sp002.py Missing --dry-run Mode

| Property | Value |
|----------|-------|
| File | `scripts/rebuild_sp002.py` |
| Issue | No dry-run mode to preview changes |
| Fix | Add `--dry-run` flag |

### 16. F-020: CPS-002 — check-prompts-sync.ps1 Missing --verbose Flag

| Property | Value |
|----------|-------|
| File | `scripts/check-prompts-sync.ps1` |
| Issue | Verbose flag not implemented |
| Fix | Implement verbose flag |

### 17. F-021: RG-003 — release-gate.yml BOM Handling Incomplete

| Property | Value |
|----------|-------|
| File | `.github/workflows/release-gate.yml` |
| Issue | BOM handling for SP-002 sync incomplete |
| Fix | Add proper BOM detection/handling |

## Files to Update

| # | File | Issues |
|---|------|--------|
| 1 | `.roomodes` | F-005, F-017 |
| 2 | `prompts/README.md` | F-006 |
| 3 | `template/docs/DOC-1-CURRENT.md` | F-007 |
| 4 | `template/docs/DOC-2-CURRENT.md` | F-007 |
| 5 | `template/docs/DOC-4-CURRENT.md` | F-007 |
| 6 | `docs/ideas/IDEA-022-ideation-to-release-journey.md` | F-008, F-009, F-011, F-015 |
| 7 | `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` | F-010, F-011 |
| 8 | `docs/releases/v2.15/DOC-3-v2.15-Implementation-Plan.md` | F-016 |
| 9 | `memory-bank/progress.md` | F-008 |
| 10 | `scripts/rebuild_sp002.py` | F-019 |
| 11 | `scripts/check-prompts-sync.ps1` | F-020 |
| 12 | `.github/workflows/release-gate.yml` | F-014, F-021 |

## Implementation Approach

### Phase 1: Documentation Fixes (P2 items)
1. Update `.roomodes` with Orchestrator reference
2. Fix `prompts/README.md` SP-002 version
3. Update template DOC-CURRENT pointers
4. Fix IDEA-022 status and criteria
5. Update PLAN-IDEA-022 hotfix path and QA criteria
6. Fix DOC-3 v2.15 step status
7. Reference Calypso phases in IDEA-022 journey

### Phase 2: Script Enhancements (P2 items)
1. Add `--dry-run` to rebuild_sp002.py
2. Implement `--verbose` in check-prompts-sync.ps1

### Phase 3: GitHub Actions Updates (P2 items)
1. Add fast-forward develop step to release-gate.yml summary
2. Add BOM handling to release-gate.yml

## Complexity Assessment

- **Effort:** M (Medium) — 17 small fixes across 12 files
- **Risk:** Low — All are documentation/script improvements with clear solutions
- **Dependencies:** None — all independent fixes

## Acceptance Criteria

- [ ] All 17 inconsistencies resolved
- [ ] `.roomodes` includes Orchestrator mode reference
- [ ] `prompts/README.md` accurate SP-002 version
- [ ] Template DOC-CURRENT pointers current
- [ ] IDEA-022 shows [IMPLEMENTED] status
- [ ] PLAN-IDEA-022 includes hotfix path
- [ ] rebuild_sp002.py has `--dry-run` mode
- [ ] check-prompts-sync.ps1 has `--verbose` flag
- [ ] release-gate.yml has complete summary

## Status History

- 2026-04-09: Created from v2.15 consistency review findings
- 2026-04-09: Refined — identified 17 specific issues with fixes
