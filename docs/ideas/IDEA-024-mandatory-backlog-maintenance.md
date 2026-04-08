# IDEA-024: Mandatory Backlog Maintenance in RULE 2

**Status:** [ACCEPTED]

**Captured:** 2026-04-08

**Source:** Code mode analysis (root cause of inconsistent backlog updates)

---

## Problem Statement

RULE 2 in `.clinerules` mandates Memory Bank updates at the close of each task:
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/decisionLog.md`

However, RULE 2 does **not** include the backlog files:
- `docs/ideas/IDEAS-BACKLOG.md`
- `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md`

This creates a gap where backlog status updates happen by convention, not mandate, leading to inconsistent enforcement.

---

## Impact

1. **Inconsistent state:** Backlog may not reflect actual implementation status
2. **Traceability loss:** Hard to track which ideas are truly in progress vs. completed
3. **Governance gap:** RULE 8.5 mandates execution tracking consistency, but without RULE 2 enforcement, the three-way sync (DOC-3, progress.md, Execution Tracker) breaks down
4. **Technical debt:** Confirmed by IDEA-022 and IDEA-023 status not being updated in backlog after implementation

---

## Proposed Solution

Add `docs/ideas/IDEAS-BACKLOG.md` and `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md` to the list of mandatory updates in RULE 2 of `.clinerules`.

### Updated RULE 2 Text

**Before:**
> Before closing any task (before attempt_completion), you MUST update:
> 1. memory-bank/activeContext.md  (new state, next action)
> 2. memory-bank/progress.md       (check off completed features)
> 3. memory-bank/decisionLog.md    (ADR with date, context, decision, consequences)

**After:**
> Before closing any task (before attempt_completion), you MUST update:
> 1. memory-bank/activeContext.md  (new state, next action)
> 2. memory-bank/progress.md       (check off completed features)
> 3. memory-bank/decisionLog.md    (ADR with date, context, decision, consequences)
> 4. docs/ideas/IDEAS-BACKLOG.md  (update status for any IDEA whose status was modified or decisions made during this session)
> 5. docs/ideas/TECH-SUGGESTIONS-BACKLOG.md  (update status for any TECH suggestion whose status was modified or decisions made during this session)

> **Note:** If SP-002 (.clinerules) was modified, increment its version per RULE 6.2 protocol.

> **Clarification:** If an agent completes work on an IDEA (whether accepting, refining, implementing, etc.), it MUST update that IDEA's status in the backlog before closing the task.

---

## Implementation

### Affected Files

| File | Change Type |
|------|-------------|
| `.clinerules` | Modify RULE 2 |
| `template/.clinerules` | Modify RULE 2 |

### Steps

1. Update `.clinerules` RULE 2 section
2. Update `template/.clinerules` RULE 2 section
3. Verify SP-002 (`.clinerules` system prompt) is still in sync after changes
4. Commit with proper conventional commit message

---

## Rationale

This is a **governance fix** that closes a loophole in RULE 2. The backlog files are already recognized as authoritative tracking documents (per IDEA-012A implementation), but they lack the same "mandatory" status as the Memory Bank files.

---

## Notes

- Related to IDEA-012A (Ideation-to-Release PHASE-A Foundation) which established RULE 11-14
- Complements RULE 8.5 (Execution Tracking consistency)
- Root cause identified during code session analyzing why IDEA-022/023 status updates were missed
