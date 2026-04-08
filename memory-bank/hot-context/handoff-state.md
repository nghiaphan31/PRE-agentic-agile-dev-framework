---
# Handoff State Schema

**File:** `memory-bank/hot-context/handoff-state.md`  
**Purpose:** Defines the state schema for mandatory handoff protocol between agents  
**Version:** 1.0  
**Last Updated:** 2026-04-08

---

## Overview

When any non-Orchestrator agent completes a task (before `attempt_completion`), it MUST write a handoff state to this file. The Orchestrator agent reads this file on activation to determine next steps.

---

## Handoff State Schema (YAML)

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
    artifacts_created: [string]  # File paths created
    artifacts_modified: [string]  # File paths modified
    
  next_action:
    recommendation: "continue" | "handoff" | "escalate" | "complete"
    suggested_mode: string  # Which mode should handle next
    urgency: "low" | "normal" | "high" | "critical"
    blocking_issues: [string]  # If blocked, list issues
    
  orchestrator_receipt:
    received_at: ISO8601
    acknowledged: boolean
    acknowledged_by: string  # Orchestrator session_id
    notes: string  # Orchestrator's assessment
```

---

## Example Handoff State

```yaml
handoff_state:
  version: "1.0"
  handoff_id: "H-2026-04-08T10-30-00-001"
  timestamp: "2026-04-08T10:30:00Z"
  
  from_agent:
    mode: "developer"
    session_id: "s2026-04-08-code-005"
    task_id: "IDEA-020-implementation"
    
  task_completion:
    status: "completed"
    output_summary: "Updated IDEA-020 with corrected problem statement; changed status to ACCEPTED"
    artifacts_created:
      - "memory-bank/hot-context/handoff-state.md"
    artifacts_modified:
      - "docs/ideas/IDEA-020-orchestrator-authoritative-default.md"
      - "docs/ideas/IDEAS-BACKLOG.md"
    
  next_action:
    recommendation: "handoff"
    suggested_mode: "orchestrator"
    urgency: "normal"
    blocking_issues: []
    
  orchestrator_receipt:
    received_at: ""
    acknowledged: false
    acknowledged_by: ""
    notes: ""
```

---

## Handoff Protocol Rules (from .clinerules)

1. **Before `attempt_completion`**: Non-Orchestrator agents MUST write handoff state
2. **Orchestrator on activation**: MUST read this file to check for pending handoffs
3. **Acknowledgment**: Orchestrator sets `acknowledged: true` and adds notes
4. **State reset**: After Orchestrator acknowledges, file is cleared for next handoff

---

## File Location

This file is stored at: `memory-bank/hot-context/handoff-state.md`

---

## Integration with session-checkpoint.md

The `session-checkpoint.md` should reference this file for handoff state:

```
## Pending Handoff
[Reference to handoff-state.md if exists]
```

---

**Next Review:** Before v2.10 release planning
