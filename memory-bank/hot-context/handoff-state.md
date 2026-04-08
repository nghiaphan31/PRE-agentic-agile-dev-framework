---
# Handoff State

**Schema Version:** 2.0
**Last updated:** 2026-04-08T18:22:00Z

---

## Handoff State Schema (v2.0)

The handoff state is used by non-Orchestrator agents to communicate task completion to the Orchestrator.
See RULE 16 (Mandatory Handoff Protocol).

### Schema Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `handoff_id` | string | Yes | Unique identifier (format: `H-{timestamp}-{sequence}`) |
| `from_agent.mode` | string | Yes | The mode completing the task (e.g., `developer`, `qa-engineer`) |
| `from_agent.session_id` | string | Yes | Session identifier (format: `s{YYYY-MM-DD}-{mode}-{NNN}`) |
| `from_agent.task_id` | string | Yes | Task being completed (e.g., `IDEA-NNN`, `TECH-NNN`) |
| `task_completion.status` | enum | Yes | `"completed"` \| `"blocked"` \| `"needs_decision"` |
| `task_completion.output_summary` | string | Yes | Brief description of what was done |
| `task_completion.artifacts_created` | array[string] | No | List of created file paths |
| `task_completion.artifacts_modified` | array[string] | No | List of modified file paths |
| `requirement_verification` | object | Yes | **NEW in v2.0** — Requirement coverage verification |
| `next_action.recommendation` | enum | Yes | `"continue"` \| `"handoff"` \| `"escalate"` \| `"complete"` |
| `next_action.suggested_mode` | string | No | Which mode should handle next |
| `next_action.urgency` | enum | No | `"low"` \| `"normal"` \| `"high"` \| `"critical"` |
| `orchestrator_receipt.received_at` | string | No | ISO8601 timestamp (filled by Orchestrator) |
| `orchestrator_receipt.acknowledged` | boolean | No | `true` if Orchestrator has acknowledged |
| `orchestrator_receipt.acknowledged_by` | string | No | Orchestrator session_id |
| `orchestrator_receipt.notes` | string | No | Orchestrator's assessment |

---

## requirement_verification Fields (v2.0)

**Purpose:** Ensure all refinement requirements (R-001 through R-00N) are verified before implementation is considered complete.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `requirements_list` | object | Yes | Map of R-00N IDs to descriptions, auto-generated from `IDEA-NNN.md` |
| `delivered_requirements` | object | Yes | Map of R-00N IDs to delivery status (`true`=delivered, `false`=not delivered, `"deferred"`=explicitly deferred) |
| `verification_status` | enum | Yes | `"passed"` \| `"failed"` \| `"partial"` |
| `missing_requirements` | object | No | Map of R-00N IDs to reasons (only if `verification_status` is `"failed"` or `"partial"`) |
| `escalation_required` | boolean | Yes | `true` if `verification_status` != `"passed"` |
| `escalation_notes` | string | Conditional | Required if `escalation_required` is `true` |

### requirements_list Format

```yaml
requirements_list:
  R-001: "Description of requirement R-001"
  R-002: "Description of requirement R-002"
  R-003: "Description of requirement R-003"
```

### delivered_requirements Format

```yaml
delivered_requirements:
  R-001: true                    # Delivered
  R-002: false                   # Not delivered
  R-003: "deferred: lacking test coverage"  # Explicitly deferred with reason
```

### verification_status Values

| Value | Description |
|-------|-------------|
| `"passed"` | All requirements delivered. Orchestrator accepts handoff. |
| `"failed"` | No requirements delivered, or critical requirements missing. Orchestrator **rejects** handoff. |
| `"partial"` | Some requirements delivered, some missing or deferred. Orchestrator **rejects** handoff unless human approves partial acceptance. |

### missing_requirements Format

```yaml
missing_requirements:
  R-002: "Not implemented due to time constraint"
  R-004: "Deferred to v2.13 per human decision"
```

---

## Orchestrator Verification Gate (v2.0)

The Orchestrator **MUST** verify requirement coverage before accepting handoff:

1. **Read handoff-state.md** from `memory-bank/hot-context/handoff-state.md`
2. **Check `requirement_verification` section**:
   - If `verification_status = "passed"` → Accept handoff, proceed to next step
   - If `verification_status = "failed"` → **Reject** handoff, escalate to human
   - If `verification_status = "partial"` → **Reject** handoff unless human explicitly approves partial acceptance
3. **Auto-generate `requirements_list`** from the corresponding `IDEA-NNN.md` file if not provided
4. **Auto-update DOC-3 execution chapter** with verification status
5. **Escalate to human** if `escalation_required = true`

### Orchestrator Decision Matrix

| verification_status | escalation_required | Action |
|---------------------|---------------------|--------|
| `"passed"` | `false` | ✅ Accept handoff |
| `"failed"` | `true` | ❌ Reject handoff, escalate to human |
| `"partial"` | `true` | ❌ Reject handoff unless human approves partial |

### Partial Acceptance Protocol

If human approves partial delivery:
- Undelivered requirements are marked as `[DEFERRED-R-NNN]` in the implementation plan
- The implementation is considered complete for the delivered portion
- Deferred requirements are tracked for future release scope

---

## Example Handoff State (v2.0)

```yaml
---
handoff_id: H-2026-04-08-001
from_agent:
  mode: developer
  session_id: s2026-04-08-developer-002
  task_id: IDEA-025
task_completion:
  status: completed
  output_summary: "Implemented requirement verification gate in handoff protocol"
  artifacts_created:
    - memory-bank/hot-context/handoff-state.md
    - docs/releases/v2.12/DOC-3-v2.12-Implementation-Plan.md
  artifacts_modified:
    - docs/releases/v2.12/DOC-4-v2.12-Operations-Guide.md
requirement_verification:
  requirements_list:
    R-001: "Orchestrator Verification Gate"
    R-002: "Handoff State Schema Update"
    R-003: "Implementation Task Instructions"
    R-004: "DOC-3 Update"
    R-005: "DOC-4 Update"
  delivered_requirements:
    R-001: true
    R-002: true
    R-003: true
    R-004: true
    R-005: true
  verification_status: "passed"
  missing_requirements: {}
  escalation_required: false
  escalation_notes: ""
next_action:
  recommendation: handoff
  suggested_mode: orchestrator
  urgency: normal
orchestrator_receipt:
  received_at: ""
  acknowledged: false
  acknowledged_by: ""
  notes: ""
---
```

---

## Previous Handoff Log

| handoff_id | from_agent | task_id | status | verification_status | timestamp |
|------------|------------|---------|--------|---------------------|-----------|
| H-2026-04-08-001 | developer | IDEA-025 | completed | passed | 2026-04-08T18:22:00Z |

---

**Cleared:** 2026-04-08T17:38:00Z

No pending handoffs. TECH-002 implementation complete.

---
