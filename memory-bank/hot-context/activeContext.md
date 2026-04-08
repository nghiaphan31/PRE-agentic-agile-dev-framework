---
# Active Context

**Last updated:** 2026-04-08T17:06:00Z
**Active mode:** developer
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Session ID:** s2026-04-08-developer-002
**Branch:** develop
**Plan:** v2.11 released; TECH-002 merged to develop
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `develop`
- Last commit: e2b7439 — Merge branch 'feature/TECH-002-auto-detect-merged-features' into develop

## v2.11 Release Complete ✅

**Released:** 2026-04-08
**Version:** v2.11.0
**Tag:** v2.11.0 (on master)
**Release Branch:** develop-v2.11 (kept for traceability)

### Release Summary
- 8 governance features implemented
- All tests pass (47 pytest)
- Documentation coherence: PASS
- Prompts sync: 6 PASS | 1 WARN (SP-007 manual deploy)

### Day 0 Actions Completed
1. ✅ Merged develop-v2.11 to master (fast-forward)
2. ✅ Tagged v2.11.0 on master
3. ✅ Pushed master and tag to origin
4. ✅ Fast-forwarded develop to master
5. ✅ Deleted RC1 tag v2.11.0-rc1
6. ✅ Pushed develop to origin

## Current task

TECH-002 merged to develop. Fast-forward merge completed successfully.

## TECH-002 Implementation ✅ (merged)

**Feature:** Auto-detect merged features for release scope
**Branch:** feature/TECH-002-auto-detect-merged-features (merged to develop)
**Merge commit:** e2b7439 (fast-forward)

### Deliverables
- `scripts/detect-merged-features.py` - Core detection script
- `.githooks/pre-receive-detect` - Pre-receive hook
- `src/calypso/branch_tracker.py` - Enhanced IDEA/TECH ID extraction

### Key Features
- Detects ALL branches merged to develop since last release tag
- Extracts IDEA-NNN, TECH-NNN, or branch name as feature identifier
- Auto-adds detected features to next release DOC-3
- Supports --dry-run mode

## v2.12 Planning

Next release scope: docs/releases/v2.12/DOC-3-v2.12-Implementation-Plan.md (to be created)

## Last Git commits
- 254d0e1 docs(memory): add IDEA-019 to v2.11 scope in activeContext
- 0c140be docs(ideas): refine TECH-002 with human requirements for release automation
- 4450e40 docs(releases): add IDEA-019 to v2.11 review summary and release notes

---
