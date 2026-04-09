---

# Refinement Session: IDEA-030

**Date:** 2026-04-09  
**Session ID:** orchestrator-2026-04-09-1603  
**Mode:** orchestrator  
**Idea:** IDEA-030 — Fix Critical Gaps — GitHub Actions + Test Coverage  

---

## Attendees

- Orchestrator Agent (refinement lead)

## Agenda

1. Review IDEA-030 current state
2. Verify GitHub Actions branch trigger issues
3. Specify test coverage requirements
4. Document acceptance criteria
5. Update status to [REFINED]

---

## Discussion Summary

### 1. Current State Review

IDEA-030 was created from v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md) with 6 critical issues:

**GitHub Actions (3 issues):**
- `.github/workflows/release-gate.yml` triggers on `develop-v*` instead of `stabilization/v*`
- `.github/workflows/canonical-docs-check.yml` triggers on `develop-v*` instead of `stabilization/v*`
- `.github/workflows/release-consistency-check.yml` triggers on `develop-v*` instead of `stabilization/v*`

**Test Coverage (3 missing tests):**
- No test for branch naming conventions (RULE-10)
- No test for DOC-CURRENT.md pointer consistency
- No test for SP-002 (.clinerules) synchronization

### 2. GitHub Actions Verification

Confirmed all three workflow files have incorrect branch trigger patterns:

| Workflow | Current Pattern | Required Pattern |
|----------|---------------|------------------|
| release-gate.yml | `'develop-v*'` | `'stabilization/v*'` |
| canonical-docs-check.yml | `'develop-v*'` | `'stabilization/v*'` |
| release-consistency-check.yml | `'develop-v*'` | `'stabilization/v*'` |

**Root cause:** ADR-006-AMEND-001 (2026-04-09) renamed `develop-vX.Y` to `stabilization/vX.Y` but workflows were not updated.

### 3. Test Coverage Requirements

Defined 3 new test files in `src/calypso/tests/`:

1. **test_branch_naming.py** — Validates RULE-10 branch naming conventions:
   - `main` is frozen
   - `develop` is wild mainline
   - `stabilization/vX.Y` follows semver
   - Feature branches: `feature/{Timebox}/{IDEA-NNN}-{slug}`
   - Lab branches: `lab/{Timebox}/{slug}`
   - Bugfix branches: `bugfix/{Timebox}/{Ticket}-{slug}`
   - Hotfix branches: `hotfix/{Ticket}`

2. **test_doc_current.py** — Validates DOC-CURRENT.md pointers:
   - All 5 DOC-*-CURRENT.md files exist
   - Pointers point to existing files in `docs/releases/vX.Y/`
   - All DOC-*-CURRENT.md point to same release version
   - Cumulative docs meet minimum line counts (DOC-1 ≥500, DOC-2 ≥500, DOC-4 ≥300)
   - Release-specific docs meet minimums (DOC-3 ≥100, DOC-5 ≥50)

3. **test_sp002_sync.py** — Validates SP-002 synchronization:
   - `.clinerules` matches `prompts/SP-002-clinerules-global.md` byte-for-byte
   - Uses `scripts/rebuild_sp002.py` verification or direct file comparison

### 4. Dependencies

- RULE-10 (GitFlow Enforcement) — source of truth for branch naming
- TECH-007 (No-FF Enforcement) — may provide branch validation utilities
- IDEA-026 (Session Lifecycle Automation) — related governance

### 5. Risks Identified

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Workflows fail after branch rename | Medium | High | Test locally with `act` or manual verification |
| Existing tests break | Low | Medium | Run full test suite before/after |
| Backward compatibility with v2.15 | Low | High | v2.15 uses deprecated `develop-vX.Y` |

---

## Decisions Made

1. **Change scope:** IDEA-030 now has two distinct parts (A: GitHub Actions, B: Test Coverage)
2. **Branch patterns:** Keep `main` and `develop` in non-release workflows; only change `develop-v*` to `stabilization/v*`
3. **Test location:** All 3 new tests in `src/calypso/tests/`
4. **Minimum line counts:** Added to DOC-CURRENT validation per R-CANON-0
5. **Status:** IDEA-030 updated to [REFINED]

---

## Requirements Captured

### Part A: GitHub Actions Fixes

1. `release-gate.yml` must trigger ONLY on `stabilization/v*` branches
2. `canonical-docs-check.yml` must trigger on `main`, `develop`, AND `stabilization/v*`
3. `release-consistency-check.yml` must validate PRs targeting `main`, `develop`, AND `stabilization/v*`

### Part B: Test Coverage

4. `test_branch_naming.py` must pass — all RULE-10 branch naming conventions validated
5. `test_doc_current.py` must pass — all DOC-CURRENT.md pointers valid and consistent
6. `test_sp002_sync.py` must pass — .clinerules matches prompts/SP-002 byte-for-byte
7. All 3 new tests integrated into CI/CD pipeline
8. Full test suite passes on `stabilization/v2.16`

### Effort Estimate

- **Total:** 4-6 hours
- **GitHub Actions changes:** 1-2 hours
- **Test creation (3 files):** 2-3 hours
- **CI integration:** 1 hour

---

## Status Transition

| Field | Before | After |
|-------|--------|-------|
| Status | [IDEA] | [REFINED] |
| Refined | — | 2026-04-09 |
| Target Release | v2.16 | v2.16 |
| Priority | P0 | P0 |
| Effort | XL | XL |

---

## Next Steps

1. Human approves/refines the requirements
2. Create implementation branch: `feature/v2.16/IDEA-030-critical-gaps`
3. Implement Part A (GitHub Actions fixes)
4. Implement Part B (3 new test files)
5. Run full test suite
6. Merge via PR with `--no-ff`
7. QA validation

---
