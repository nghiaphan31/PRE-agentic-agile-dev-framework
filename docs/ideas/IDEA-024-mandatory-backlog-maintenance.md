# IDEA-024: Mandatory Backlog Maintenance in RULE 2

**Status:** [IMPLEMENTED]
**Captured:** 2026-04-08
**Source:** Code mode analysis
**Type:** governance
**Tier:** Minor
**Target Release:** v2.11

## Summary

RULE 2 was missing items 3-5 for mandatory backlog maintenance at task close. This idea adds the missing items to ensure consistency between memory-bank/progress.md and EXECUTION-TRACKER-vX.Y.md.

## Motivation

When closing a task, agents must update multiple memory bank files. The original RULE 2 only specified items 1-2, but per RULE 8.5 (Execution Tracking Mandate), the EXECUTION-TRACKER-vX.Y.md must also be updated and kept in sync with progress.md.

## Changes Made

### .clinerules (RULE 2)

Updated RULE 2 to include items 3-5:

```
Before closing any task (before attempt_completion), you MUST update:

1. memory-bank/activeContext.md  (new state, next action)
2. memory-bank/progress.md       (check off completed features)
3. docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md  (session log entry)
4. memory-bank/decisionLog.md    (ADR with date, context, decision, consequences) — ONLY if an architecture decision was made
5. Ensure memory-bank/progress.md and EXECUTION-TRACKER-vX.Y.md are consistent — both files MUST reflect the same status for all items
```

### template/.clinerules

Synced the same RULE 2 update to template/.clinerules.

### prompts/SP-002-clinerules-global.md

Rebuilt via scripts/rebuild_sp002.py to reflect the .clinerules changes. Verified byte-for-byte match.

## Disposition

[IMPLEMENTED] - RULE 2 updated with items 3-5; SP-002 rebuilt

## Files Modified

- `.clinerules` (RULE 2)
- `template/.clinerules` (RULE 2)
- `prompts/SP-002-clinerules-global.md` (rebuilt)
- `docs/ideas/IDEAS-BACKLOG.md` (status update)
