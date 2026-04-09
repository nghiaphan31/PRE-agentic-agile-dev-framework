# Refinement Session: IDEA-032

**Date:** 2026-04-09
**Mode:** Architect
**Idea:** IDEA-032 — Fix Minor Gaps — Documentation Consistency
**Refiner:** Architect Agent

---

## Session Overview

Refined IDEA-032 from [IDEA] to [REFINED] status. The original IDEA-032 listed 17 generic documentation inconsistencies; this refinement identified specific issues with targeted fixes.

## Input Sources

- `docs/ideas/IDEA-032-fix-minor-gaps.md` (original capture)
- `docs/qa/QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md` (detailed findings)
- `prompts/SP-002-clinerules-global.md` (RULE 10, 16)
- `.roomodes` (mode definitions)

## Identified Issues (17 total)

| # | Finding | File(s) | Fix |
|---|---------|---------|-----|
| F-005 | .roomodes missing Orchestrator | `.roomodes` | Add Orchestrator reference |
| F-006 | SP-002 version mismatch | `prompts/README.md` | Update v2.8.0 → v2.9.0 |
| F-007 | Template DOC-CURRENT stale | `template/docs/DOC-*-CURRENT.md` | Update to current version |
| F-008 | IDEA-022 status [IDEA] vs [IMPLEMENTED] | `docs/ideas/IDEA-022-*.md` | Update status |
| F-009 | IDEA-022 acceptance criteria unchecked | `docs/ideas/IDEA-022-*.md` | Verify and check |
| F-010 | Hotfix path missing from PLAN | `plans/IDEA-022/PLAN-*.md` | Add hotfix pattern |
| F-011 | QA entry criteria wrong | `plans/IDEA-022/PLAN-*.md` | Fix merge before QA |
| F-012 | Deprecated branch names (historical) | `docs/releases/v2.9/*` | No change (frozen) |
| F-013 | Hotfix pattern mismatch | Multiple docs | Standardize to `hotfix/{Ticket}` |
| F-014 | release-gate.yml missing ff step | `.github/workflows/*` | Add fast-forward step |
| F-015 | Calypso phases not referenced | `docs/ideas/IDEA-022-*.md` | Reference Phase 2-4 |
| F-016 | DOC-3 v2.15 PENDING status wrong | `docs/releases/v2.15/DOC-3-*.md` | Update to actual status |
| F-017 | .roomodes no Orchestrator entry | `.roomodes` | Add built-in mode |
| F-018 | Handoff schema not validated | `memory-bank/hot-context/handoff-state.md` | Consider validation |
| F-019 | rebuild_sp002.py no --dry-run | `scripts/rebuild_sp002.py` | Add --dry-run flag |
| F-020 | check-prompts-sync.ps1 no --verbose | `scripts/check-prompts-sync.ps1` | Implement verbose |
| F-021 | release-gate.yml BOM handling | `.github/workflows/release-gate.yml` | Add BOM handling |

## Complexity Assessment

| Metric | Value |
|--------|-------|
| **Effort** | M (Medium) |
| **Risk** | Low |
| **Files Affected** | 12 |
| **Issues Fixed** | 17 |

## Decision: Split into Categories

The 17 issues were categorized:

### Documentation Fixes (12 issues)
- F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-013, F-015, F-016, F-017, F-018

### Script Enhancements (2 issues)
- F-019: `--dry-run` for rebuild_sp002.py
- F-020: `--verbose` for check-prompts-sync.ps1

### GitHub Actions Updates (2 issues)
- F-014: Fast-forward step
- F-021: BOM handling

### Historical (1 issue)
- F-012: No action (frozen release)

## Output Artifacts

| Artifact | Action |
|----------|--------|
| `docs/ideas/IDEA-032-documentation-consistency.md` | Created with full refinement |
| `docs/ideas/IDEAS-BACKLOG.md` | Updated status [IDEA] → [REFINED] |

## Next Steps

1. Product Owner reviews and accepts/refines for v2.17 scope
2. Developer mode implements the fixes
3. QA validates fixes

## Notes

- This refinement supersedes the original `IDEA-032-fix-minor-gaps.md` capture
- The new `IDEA-032-documentation-consistency.md` provides detailed, actionable fixes
- Target v2.17 per effort estimation (P2 items)
