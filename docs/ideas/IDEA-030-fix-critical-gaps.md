# IDEA-030: Fix Critical Gaps (P0)

**Status:** [IDEA]
**Created:** 2026-04-09
**Source:** v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md)
**Priority:** P0
**Effort:** XL

## Problem Statement

GitHub Actions workflows trigger on wrong branch patterns (develop-v* instead of stabilization/v*), which breaks the release gate mechanism. Additionally, there is no test coverage for critical paths including branch naming validation, DOC-CURRENT pointer consistency, and SP-002 synchronization. These gaps can cause releases to proceed with invalid configurations.

## Proposed Solution

1. Fix 3 GitHub Actions workflows to trigger on `stabilization/v*` branches instead of `develop-v*`
2. Add 3 critical test suites to validate:
   - Branch naming conventions
   - DOC-CURRENT pointer validity
   - SP-002 (.clinerules) synchronization with prompts/SP-002

## Affected Files

### GitHub Actions (3 files)
- .github/workflows/release-gate.yml
- .github/workflows/canonical-docs-check.yml
- .github/workflows/release-consistency-check.yml

### New Test Files (3 files)
- src/calypso/tests/test_branch_naming.py (NEW)
- src/calypso/tests/test_doc_current.py (NEW)
- src/calypso/tests/test_sp002_sync.py (NEW)

## Acceptance Criteria

- [ ] release-gate.yml triggers on `stabilization/v*` branches (not `develop-v*`)
- [ ] canonical-docs-check.yml triggers on `stabilization/v*` branches
- [ ] release-consistency-check.yml validates PRs targeting `stabilization/v*`
- [ ] test_branch_naming.py passes — validates branch naming conventions per RULE-10
- [ ] test_doc_current.py passes — validates DOC-*-CURRENT.md pointers point to correct release
- [ ] test_sp002_sync.py passes — validates SP-002 matches .clinerules byte-for-byte

## Status History

- 2026-04-09: Created from v2.15 consistency review findings (6 critical issues)
