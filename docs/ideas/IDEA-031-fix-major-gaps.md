# IDEA-031: Fix Major Gaps (P1)

**Status:** [IDEA]
**Created:** 2026-04-09
**Source:** v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md)
**Priority:** P1
**Effort:** L

## Problem Statement

Multiple automation scripts have critical reliability issues:
1. `checkpoint_heartbeat.py` fails silently on errors and drops conversation content
2. `audit_cumulative_docs.py` has hardcoded release versions instead of dynamic detection
3. Pre-receive hook has incorrect line count thresholds
4. No test coverage for handoff, mode switching, or release workflow automation

## Proposed Solution

1. Fix `checkpoint_heartbeat.py` to handle all edge cases and properly write conversation content
2. Update `audit_cumulative_docs.py` to dynamically detect all releases
3. Fix pre-receive hook line count thresholds (DOC-3: 100 lines minimum, DOC-5: 50 lines minimum)
4. Add 3 new test suites for handoff, mode switching, and release workflow

## Affected Files

### Scripts to Fix (3 files)
- scripts/checkpoint_heartbeat.py
- scripts/audit_cumulative_docs.py
- .githooks/pre-receive

### New Test Files (3 files)
- src/calypso/tests/test_handoff.py (NEW)
- src/calypso/tests/test_mode_switching.py (NEW)
- src/calypso/tests/test_release_workflow.py (NEW)

## Acceptance Criteria

- [ ] checkpoint_heartbeat.py passes all edge cases (no silent failures, no content drops)
- [ ] log_conversation() writes actual conversation content (not placeholder text)
- [ ] audit_cumulative_docs.py detects all releases dynamically (not hardcoded)
- [ ] pre-receive hook enforces correct line counts: DOC-3 >= 100 lines, DOC-5 >= 50 lines
- [ ] test_handoff.py passes — validates handoff state creation and acknowledgment
- [ ] test_mode_switching.py passes — validates mode switching functionality
- [ ] test_release_workflow.py passes — validates release workflow automation

## Status History

- 2026-04-09: Created from v2.15 consistency review findings (8 major issues)
