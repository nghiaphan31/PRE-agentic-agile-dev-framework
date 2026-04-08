# TECH-006: Dummy Session-Start Task for Orchestrator Mode Switch

**ID:** TECH-006
**Title:** Dummy Session-Start Task for Orchestrator Mode Switch
**Source:** Human (direct suggestion)
**Captured:** 2026-04-08
**Status:** [ACCEPTED]
**Type:** technical
**Tier:** Minor
**Target Release:** TBD
**Disposition:** Human reports seeing automatic mode switching — need to verify

---

## Problem Statement

Human wants a workaround for the Roo Code limitation: Orchestrator cannot be set as the default mode programmatically. The human suggested: "having a dummy task at session start that, upon completion, requests a switch to Orchestrator mode."

## Proposed Solution

1. Create a lightweight "session start" dummy task
2. When the dummy task completes, it requests mode switch to Orchestrator
3. Mode switches automatically (if possible) or with human approval

## Technical Analysis

**Confirmed by Gemini:** The `switch_mode` tool works autonomously — no human approval required. As long as:
1. The target mode exists in the configuration (`.roomodes` for custom modes, or built-in like Orchestrator)
2. The current persona has permission to use the tool

**This means:** A dummy task at session start CAN autonomously switch to Orchestrator mode!

### Implementation Approach

1. **Add instruction to RULE 16.5 in .clinerules:**
   - At session start, any mode should invoke `switch_mode("orchestrator")`
   - This provides automatic mode switch to Orchestrator

2. Test the workflow:
   - Start in any mode (e.g., `ask`)
   - Verify it auto-switches to Orchestrator

## Status History

| Date       | Status | Notes                                      |
|------------|--------|--------------------------------------------|
| 2026-04-08 | [IDEA] | Captured from human suggestion             |
| 2026-04-08 | [NEEDS_MORE_INFO] | Human reports seeing auto switch — verify |
