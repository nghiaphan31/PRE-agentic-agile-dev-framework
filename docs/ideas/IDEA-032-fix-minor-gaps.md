# IDEA-032: Fix Minor Gaps (P2)

**Status:** [IDEA]
**Created:** 2026-04-09
**Source:** v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md)
**Priority:** P2
**Effort:** M

## Problem Statement

Documentation inconsistencies across 17 files that affect project coherence. These include incorrect references, missing updates after refactoring, and inconsistent formatting/terminology across governance documents.

## Proposed Solution

Review and fix all documented inconsistencies in the affected files. Each file requires specific corrections identified in the consistency review.

## Affected Files (17 items)

### Configuration Files (3 files)
- .roomodes
- prompts/README.md
- scripts/rebuild_sp002.py

### Ideas Documentation (2 files)
- docs/ideas/IDEA-022-ideation-to-release-journey.md
- plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md

### Memory Bank (1 file)
- memory-bank/progress.md

### Release Documentation (2 files)
- docs/releases/v2.15/DOC-3-v2.15-Implementation-Plan.md
- docs/releases/v2.15/DOC-5-v2.15-Release-Notes.md

### Template Files (4 files)
- template/docs/DOC-1-CURRENT.md
- template/docs/DOC-2-CURRENT.md
- template/docs/DOC-4-CURRENT.md

## Acceptance Criteria

- [ ] All 17 inconsistencies resolved
- [ ] .roomodes consistent with current branch naming conventions
- [ ] prompts/README.md lists all current SP-* files accurately
- [ ] scripts/rebuild_sp002.py works correctly
- [ ] IDEA-022 and PLAN-IDEA-022 are internally consistent
- [ ] memory-bank/progress.md reflects current project state
- [ ] DOC-3-v2.15 and DOC-5-v2.15 are internally consistent
- [ ] Template DOC-*-CURRENT.md files are correct

## Status History

- 2026-04-09: Created from v2.15 consistency review findings (17 minor issues)
