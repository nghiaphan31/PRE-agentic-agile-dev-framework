---

## IDEA-030: Fix Critical Gaps — GitHub Actions + Test Coverage (P0)

**Status:** [REFINED]  
**Created:** 2026-04-09  
**Source:** v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md)  
**Refined:** 2026-04-09  
**Priority:** P0  
**Effort:** XL  
**Target Release:** v2.16  

---

### Problem Statement

GitHub Actions workflows trigger on wrong branch patterns (`develop-v*` instead of `stabilization/v*`), which breaks the release gate mechanism per ADR-006-AMEND-001. Additionally, there is no test coverage for critical paths including branch naming validation, DOC-CURRENT pointer consistency, and SP-002 synchronization. These gaps can cause releases to proceed with invalid configurations.

### Background

ADR-006-AMEND-001 (2026-04-09) renamed `develop-vX.Y` branches to `stabilization/vX.Y`. The GitHub Actions workflows were not updated to reflect this change, creating a critical gap in the release enforcement mechanism.

### Proposed Solution

#### Part A: Fix GitHub Actions Branch Triggers (3 workflows)

| Workflow File | Current Pattern | Required Pattern | Change |
|---------------|-----------------|------------------|--------|
| `.github/workflows/release-gate.yml` | `'develop-v*'` | `'stabilization/v*'` | Replace branch pattern |
| `.github/workflows/canonical-docs-check.yml` | `'develop-v*'` | `'stabilization/v*'` | Replace branch pattern |
| `.github/workflows/release-consistency-check.yml` | `'develop-v*'` | `'stabilization/v*'` | Replace branch pattern |

**Details:**
- `release-gate.yml`: Only triggers on `stabilization/v*` (removes `develop-v*`)
- `canonical-docs-check.yml`: Keep `'develop'` and `'main'`, replace `'develop-v*'` with `'stabilization/v*'`
- `release-consistency-check.yml`: Keep `main` and `develop`, replace `'develop-v*'` with `'stabilization/v*'`

#### Part B: Add Critical Test Coverage (3 test files)

Create new test files in `src/calypso/tests/`:

1. **`test_branch_naming.py`** — Validates branch naming conventions per RULE-10:
   - `main` is frozen (no direct commits)
   - `develop` is wild mainline
   - `stabilization/vX.Y` follows semver pattern
   - Feature branches follow `feature/{Timebox}/{IDEA-NNN}-{slug}`
   - Lab branches follow `lab/{Timebox}/{slug}`
   - Bugfix branches follow `bugfix/{Timebox}/{Ticket}-{slug}`
   - Hotfix branches follow `hotfix/{Ticket}`

2. **`test_doc_current.py`** — Validates DOC-CURRENT.md pointer consistency:
   - All 5 DOC-*-CURRENT.md files exist
   - Pointers point to existing files in `docs/releases/vX.Y/`
   - All DOC-*-CURRENT.md point to the same release version
   - Cumulative docs (DOC-1, DOC-2, DOC-4) have minimum line counts (500+, 500+, 300+)
   - Release-specific docs (DOC-3, DOC-5) have minimum line counts (100+, 50+)

3. **`test_sp002_sync.py`** — Validates SP-002 synchronization:
   - `.clinerules` matches `prompts/SP-002-clinerules-global.md` byte-for-byte
   - Uses the `scripts/rebuild_sp002.py` verification or direct file comparison

### Affected Files

**Modified (3 files):**
- `.github/workflows/release-gate.yml`
- `.github/workflows/canonical-docs-check.yml`
- `.github/workflows/release-consistency-check.yml`

**New (3 files):**
- `src/calypso/tests/test_branch_naming.py`
- `src/calypso/tests/test_doc_current.py`
- `src/calypso/tests/test_sp002_sync.py`

### Dependencies

- IDEA-026 (Session Lifecycle Automation) — not a hard dependency but related governance
- TECH-007 (No-FF Enforcement) — may provide additional branch validation utilities
- RULE-10 (GitFlow Enforcement) — the source of truth for branch naming

### Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Workflows fail after branch rename | Medium | High | Test changes locally with `act` or manual verification |
| Existing tests break due to new assertions | Low | Medium | Run full test suite before and after |
| Backward compatibility with v2.15 releases | Low | High | v2.15 uses `develop-vX.Y` which is now deprecated |

### Acceptance Criteria

- [ ] `release-gate.yml` triggers only on `stabilization/v*` branches
- [ ] `canonical-docs-check.yml` triggers on `main`, `develop`, and `stabilization/v*`
- [ ] `release-consistency-check.yml` validates PRs targeting `main`, `develop`, and `stabilization/v*`
- [ ] `test_branch_naming.py` passes — all branch naming conventions validated
- [ ] `test_doc_current.py` passes — all DOC-CURRENT.md pointers valid and consistent
- [ ] `test_sp002_sync.py` passes — .clinerules matches prompts/SP-002 byte-for-byte
- [ ] All 3 new tests integrated into CI/CD pipeline
- [ ] Full test suite passes on `stabilization/v2.16`

### Implementation Notes

1. **GitHub Actions changes**: Use `--no-ff` merge strategy for the PR to keep branch history
2. **Test files**: Follow existing test patterns in `src/calypso/tests/`
3. **CI integration**: Add new tests to `.github/workflows/canonical-docs-check.yml` or create dedicated workflow
4. **Minimum effort estimate**: 4-6 hours for all 6 changes

### Status History

- 2026-04-09: Created from v2.15 consistency review findings (6 critical issues)
- 2026-04-09: Refined — added detailed branch trigger patterns, test specifications, and acceptance criteria

---
