---
id: IDEA-019
title: Implement Conversation Logging Mechanism
status: [REFINED]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: RULE 8.3, docs/conversations/
captured: 2026-04-01
captured_by: Developer mode
refined_by: Architect mode
refinement_session: REFINEMENT-2026-04-08-002
---

## Description

Per RULE 8.3, conversations should be logged to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`. However, the conversation logging is NOT happening in practice - this very conversation is not being logged. We need an automated or semi-automated mechanism to trigger conversation logging.

## Motivation

RULE 8.3 Conversation Log Mandate states:
- When saving an AI conversation output, save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`
- Add entry to `docs/conversations/README.md` with triage status "Not yet triaged"
- Never edit a conversation file after creation

But there is NO trigger mechanism in place:
- Agents don't automatically log conversations
- No pre-commit hook for conversation files
- No CI check to ensure conversations are logged
- The rule exists but isn't enforced

## Classification

Type: GOVERNANCE

## Required Actions

1. **Define trigger conditions:** When should a conversation be logged?
   - Every session? Only sessions with significant decisions?
   - Sessions that produce IDEAS or ADRs?
   - All sessions or selective?

2. **Implement logging mechanism:**
   - Automated logging at session end
   - Semi-automated (agent asks human for permission)
   - Manual with reminders

3. **Add CI check** to verify conversation logging

## Complexity Score

**Score: 4/10** — SYNCHRONOUS refinement recommended

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human question |
| 2026-04-08 | [REFINED] | Refinement session REFINEMENT-2026-04-08-002 |

## Session Mechanism Issues (Findings)

From examining `memory-bank/hot-context/session-checkpoint.md`:

| Issue | Finding |
|-------|---------|
| Session ID | Shows `s2026-04-01-architect-001` (yesterday's session) — no fresh session ID generated |
| Mode | `unknown` — `SESSION_MODE` env var NOT set by the tool |
| Heartbeat | Last heartbeat `2026-04-01T16:53:47` — from yesterday, not today |
| Conversation logging | Not auto-triggered at session end |
| Crash recovery | Session checkpoint mechanism exists but not started for today's session |

## Refined Solution

### Technical Approach: Extend checkpoint_heartbeat.py

Rather than creating a new script, extend the existing `checkpoint_heartbeat.py` with a `--log-conversation` flag that:
1. Captures session metadata from `activeContext.md` and `session-checkpoint.md`
2. Generates the conversation filename: `{YYYY-MM-DD}-{source}-{slug}.md`
3. Creates the conversation file with structured content
4. Updates `docs/conversations/README.md` with new entry

### Trigger Conditions

| Trigger | Action |
|---------|--------|
| Mode starts | Auto-start heartbeat (via VS Code task or shell profile) |
| Every 5 minutes | Heartbeat updates session-checkpoint.md |
| Session ends (`attempt_completion`) | Agent manually calls `checkpoint_heartbeat.py --log-conversation` |

### Acceptance Criteria

| AC | Description |
|----|-------------|
| AC-1 | `session-checkpoint.md` shows current date when heartbeat is running |
| AC-2 | `SESSION_MODE` env var is set correctly by the tool |
| AC-3 | `checkpoint_heartbeat.py --log-conversation` creates conversation file |
| AC-4 | Entry added to `docs/conversations/README.md` |
| AC-5 | CI workflow checks conversation file creation |

### File Modifications

| File | Change |
|------|--------|
| `scripts/checkpoint_heartbeat.py` | Add `--log-conversation` command |
| `memory-bank/hot-context/session-checkpoint.md` | Update template to include `conversation_logged` field |
| `.vscode/tasks.json` | Add "Start Heartbeat" task |
| `.vscode/settings.json` | Add `sessionScript` configuration |
| `.github/workflows/conversation-check.yml` | New CI workflow for conversation logging |
