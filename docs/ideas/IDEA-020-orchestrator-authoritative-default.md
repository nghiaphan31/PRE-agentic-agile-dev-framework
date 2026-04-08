# IDEA-020: Authoritative Orchestrator as Default Mode

**ID:** IDEA-020  
**Title:** Authoritative Orchestrator as Default Mode  
**Source:** Human (direct remark)  
**Captured:** 2026-04-02  
**Status:** [ACCEPTED]  
**Type:** governance  
**Tier:** Major  
**Target Release:** v2.10  
**Disposition:** Proceed with implementation — Orchestrator is built-in, focus on default config + handoff protocol

---

## Key Correction (2026-04-08)

**The `orchestrator` mode is a BUILT-IN Roo Code mode — NOT defined in `.roomodes`.**

The `.roomodes` file only defines **custom persona modes** (product-owner, scrum-master, developer, qa-engineer). The Orchestrator is a native Roo Code mode that already exists.

**Hard blocker #1 is RESOLVED:** Orchestrator mode already exists in Roo Code.

**Remaining hard blockers to address:**
- **#2:** No autonomous mode-switching mechanism (Roo Code limitation — mode switches require human or VS Code action)
- **#3:** No handoff state schema defined

---

## Problem Statement (Corrected)

The current orchestration model has gaps:

1. **Orchestrator is not the default entry point** — human must manually invoke orchestrator mode
2. **No automatic handoff protocol** — when one agent completes a task, there is no enforced mechanism to return control to the orchestrator
3. **Mode switches require human intervention** — Roo Code cannot autonomously switch modes

---

## Proposed Solution (Refined)

### 1. Make Orchestrator the Default Entry Point
- **Investigate:** Roo Code configuration for default mode on startup
- **Action:** If `.roomodes` or VS Code settings can set default mode, configure `orchestrator` as default
- **Fallback:** Document the procedure for users to set Orchestrator as default manually

### 2. Mandatory Handoff Protocol via .clinerules
- Add rules to `.clinerules` that mandate returning control to Orchestrator after task completion
- Define clear handoff trigger patterns (e.g., before `attempt_completion`)
- The Orchestrator receives completion status and determines next steps

### 3. Handoff State Schema
- Define a minimal state schema for handoff communication
- Store in `memory-bank/hot-context/session-checkpoint.md` or create `memory-bank/hot-context/handoff-state.md`
- Schema fields: task_id, originating_mode, completion_status, output_summary, next_action_recommendation

---

## Architecture: Handoff State Schema

```yaml
handoff_state:
  version: "1.0"
  handoff_id: "H-{timestamp}-{sequence}"
  timestamp: ISO8601
  
  from_agent:
    mode: "developer" | "qa-engineer" | "product-owner" | "scrum-master"
    session_id: string
    task_id: string
    
  task_completion:
    status: "completed" | "blocked" | "needs_decision"
    output_summary: string  # Brief description of what was done
    artifacts_created: [string]  # File paths
    artifacts_modified: [string]
    
  next_action:
    recommendation: "continue" | "handoff" | "escalate" | "complete"
    suggested_mode: string  # Which mode should handle next
    urgency: "low" | "normal" | "high" | "critical"
    
  orchestrator_receipt:
    received_at: ISO8601
    acknowledged: boolean
```

---

## Affected Documents

| Document | Action |
|----------|--------|
| `.clinerules` | Add mandatory handoff protocol rules |
| `memory-bank/hot-context/handoff-state.md` | Create new — handoff state schema |
| `memory-bank/hot-context/session-checkpoint.md` | Update to incorporate handoff state |
| `docs/ideas/IDEAS-BACKLOG.md` | Update IDEA-020 status to [ACCEPTED] |

---

## Implementation Steps

1. **Investigate default mode configuration**
   - Research if Roo Code supports setting default mode via settings or .roomodes
   - Document findings

2. **Define handoff state schema**
   - Create `memory-bank/hot-context/handoff-state.md` with YAML schema
   - Update session-checkpoint.md to reference handoff state

3. **Add handoff rules to .clinerules**
   - Rule: Before `attempt_completion`, agent MUST write handoff state
   - Rule: Orchestrator mode reads handoff state on activation
   - Rule: Non-Orchestrator modes must NOT assume they are the entry point

4. **Test the handoff protocol**
   - Verify handoff state is written on task completion
   - Verify Orchestrator can read and act on handoff state

---

## Motivation

The human user expects a self-managing workflow where:
1. They state a goal
2. The Orchestrator drives the entire process
3. Specialized agents are invoked as needed
4. The Orchestrator maintains state and determines next steps

This refinement removes the incorrect assumption that Orchestrator mode needs to be created. It focuses on:
- Making the existing Orchestrator the default entry point
- Implementing a handoff protocol so control returns to Orchestrator
- Defining state schema for handoff communication

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-02 | [IDEA] | Captured from human remark |
| 2026-04-08 | [ACCEPTED] | Corrected understanding — Orchestrator is built-in; focus on default config + handoff protocol |

---
