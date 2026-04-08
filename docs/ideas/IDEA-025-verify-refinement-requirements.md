# IDEA-025 — Verify Refinement Requirements Before Implementation Close

---
**ID:** IDEA-025
**Title:** Verify Refinement Requirements Before Implementation Close
**Type:** `governance`
**Tier:** `Medium`
**Status:** `[ACCEPTED]`
**Target Release:** `v2.12`
**Captured:** `2026-04-08`
**Source:** TECH-002 implementation gap (R-005)
**Disposition:** Process improvement to enforce requirement coverage verification
**Complexity:** `2/10` (governance-only, no new tooling)
**Architect:** `REFINED` on 2026-04-08
---

## 0. Refinement Summary

| Open Question | Decision | Rationale |
|---------------|----------|-----------|
| OQ1: Auto-generate `requirements_list` from refinement artifacts? | **YES** | Low complexity, high value — reduces manual entry |
| OQ2: Auto-update DOC-3 with verification status? | **YES** | Reduces manual overhead, keeps DOC-3 current |
| OQ3: Escalate to human if verification fails? | **YES** | Human should decide on rework scope |
| OQ4: Support partial acceptance? | **YES** | With explicit deferral notation (`[DEFERRED-R-NNN]`) |

**Feasibility Assessment:** ✅ **Feasible** — This is governance-only (process/workflow changes). No new tooling required. Implementation involves updating:
- RULE 16 (Handoff Protocol) — minimal schema change
- DOC-3 (Implementation Plan) — add verification section
- DOC-4 (Operations Guide) — document verification step
- Memory Bank handoff-state.md schema

---

## 1. Context

### 1.1 Problem Statement
During the implementation of **TECH-002 (Auto-Detect Merged Features for Release Scope)**, a critical gap was identified:
- **Requirement R-005** ("Auto-create next release scope when tag is created") was **defined during refinement** but **not implemented**.
- The gap was **manually identified** by the human after the implementation task was marked complete.
- The root cause is that **refinement requirements (R-001 through R-00N) are not verified against actual implementation** before marking a task complete.

### 1.2 Impact
- **Undelivered requirements**: Features may be marked complete without delivering all agreed-upon requirements.
- **Manual gap detection**: Humans must manually verify requirement coverage, which is error-prone and time-consuming.
- **Technical debt**: Undetected gaps accumulate, leading to incomplete releases and rework.

### 1.3 Root Cause Analysis
- **Non-Orchestrator agents** (e.g., Developer, QA Engineer) implement features without explicitly verifying that all refinement requirements (R-001 through R-00N) are delivered.
- The **Orchestrator does not verify requirement coverage** before accepting handoff from implementation agents.
- There is **no enforced verification step** in the implementation workflow to ensure alignment between refinement requirements and delivered code.

### 1.4 Relationship to Existing Ideas
- **TECH-002**: This idea was born from a gap identified during TECH-002 implementation. TECH-002 is now complete, but the process gap remains.
- **IDEA-012A/B/C (Ideation-to-Release Pipeline)**: This idea **complements** IDEA-012A/B/C by adding a **requirement verification gate** to the implementation phase.
- **IDEA-020 (Orchestrator as Default Mode)**: This idea **leverages the Orchestrator** as a verification gate (Option 2).

### 1.5 Sync Analysis
- **🟢 NO_OVERLAP**: No conflicts with active branches or ideas.
- **🟢 NO_DEPENDENCY**: This is a **process improvement** and does not block or depend on any implementation.
- **🟢 SHARED_LAYER**: This idea touches the **implementation phase** (Phase 4 of IDEA-012A/B/C) and **handoff protocol** (RULE 16). Coordination with the Orchestrator is required.

---

## 2. Proposal

### 2.1 Solution Options
Three options were proposed to address the problem. **Option 2 (Orchestrator Verification Gate)** is recommended as the **most robust and scalable** solution.

| Option | Description | Pros | Cons | Recommendation |
|--------|-------------|------|------|----------------|
| **1. Strict Enforcement** | Require all implementation tasks to include a requirements verification step where each R-00N is checked against delivered code before `attempt_completion`. | - Simple to implement<br>- Developer-owned | - Relies on developer discipline<br>- No centralized verification | ❌ Not scalable |
| **2. Orchestrator Verification Gate** | Orchestrator must verify R-00N coverage before accepting handoff from implementation agent. | - Centralized verification<br>- Scalable<br>- Aligns with IDEA-020 (Orchestrator as Default Mode) | - Requires Orchestrator tooling updates | ✅ **Recommended** |
| **3. Template Requirement** | Implementation task instructions must include an explicit R-00N checklist that the developer fills in. | - Lightweight<br>- Developer-owned | - No enforcement<br>- Prone to human error | ❌ Not robust |

### 2.2 Selected Solution: Orchestrator Verification Gate
The Orchestrator will act as a **verification gate** before accepting handoff from implementation agents. This ensures:
- **Centralized verification**: The Orchestrator is the single source of truth for requirement coverage.
- **Scalability**: Works for all implementation tasks, regardless of complexity.
- **Alignment with IDEA-020**: Leverages the Orchestrator's role as the authoritative default mode.

#### 2.2.1 Implementation Steps
1. **Update Orchestrator Handoff Protocol** (RULE 16):
   - Add a **requirement verification step** to the handoff state schema.
   - The Orchestrator must verify that all R-00N requirements are delivered before accepting handoff.
2. **Update Implementation Task Instructions**:
   - Non-Orchestrator agents must **explicitly list delivered requirements** in the handoff state.
3. **Update DOC-3 (Implementation Plan)**:
   - Add a **requirement verification section** to the implementation phase.
4. **Update DOC-4 (Operations Guide)**:
   - Document the new verification step in the **ideation-to-release journey** (IDEA-022).

#### 2.2.2 Handoff State Schema Updates
The `handoff-state.md` schema will be updated to include:
```yaml
requirement_verification:
  requirements_list: # List of R-00N requirements from refinement (auto-generated from IDEA-NNN.md)
    - R-001: "Description of requirement"
    - R-002: "Description of requirement"
    - ...
  delivered_requirements: # List of R-00N requirements delivered in implementation
    - R-001: true  # Delivered
    - R-002: false # Not delivered
    - R-003: "deferred" # Explicitly deferred with reason
    - ...
  verification_status: "passed" | "failed" | "partial"
  missing_requirements: # List of undelivered requirements (if verification_status = "failed" or "partial")
    - R-002: "Reason for missing requirement"
  escalation_required: boolean # True if verification_status != "passed"
  escalation_notes: "Human decision notes" # Required if escalation_required = true
```

#### 2.2.3 Orchestrator Workflow
1. **Receive Handoff**: Orchestrator reads `handoff-state.md`.
2. **Auto-Generate Requirements List** (OQ1): Orchestrator auto-populates `requirements_list` from the corresponding `IDEA-NNN.md` file.
3. **Verify Requirements**: Orchestrator checks `requirement_verification.verification_status`.
   - If `passed`: Accept handoff and proceed to next step.
   - If `failed` or `partial`:
     - Set `escalation_required = true`.
     - Escalate to human for rework decision.
     - Human decides: rework now, defer to next release, or accept partial.
4. **Auto-Update DOC-3** (OQ2): Orchestrator auto-updates the **execution chapter** to reflect verification status.
5. **Support Partial Acceptance** (OQ4): If human approves partial delivery, mark undelivered requirements as `[DEFERRED-R-NNN]`.

---

## 3. Requirements

### 3.1 Functional Requirements
| ID | Requirement | Description |
|----|-------------|-------------|
| R-001 | Orchestrator Verification Gate | The Orchestrator must verify requirement coverage before accepting handoff from implementation agents. |
| R-002 | Handoff State Schema Update | The `handoff-state.md` schema must include fields for requirement verification. |
| R-003 | Implementation Task Instructions | Non-Orchestrator agents must explicitly list delivered requirements in the handoff state. |
| R-004 | DOC-3 Update | DOC-3 must include a requirement verification section in the implementation phase. |
| R-005 | DOC-4 Update | DOC-4 must document the new verification step in the ideation-to-release journey. |

### 3.2 Non-Functional Requirements
| ID | Requirement | Description |
|----|-------------|-------------|
| R-006 | Scalability | The solution must scale to handle complex implementation tasks with many requirements. |
| R-007 | Usability | The solution must not add significant overhead to the implementation workflow. |
| R-008 | Consistency | The solution must be consistent with existing rules (RULE 10, RULE 11, RULE 16). |

---

## 4. Deliverables

### 4.1 Primary Deliverables
1. **Updated Orchestrator Handoff Protocol** (`memory-bank/hot-context/handoff-state.md` schema).
2. **Updated DOC-3 (Implementation Plan)** with a requirement verification section.
3. **Updated DOC-4 (Operations Guide)** to document the new verification step.

### 4.2 Secondary Deliverables
1. **IDEA-025 Entry** in `docs/ideas/IDEAS-BACKLOG.md`.
2. **Updated Memory Bank** (`memory-bank/hot-context/progress.md`, `memory-bank/hot-context/activeContext.md`).
3. **Decision Log Entry** (`memory-bank/hot-context/decisionLog.md`).

---

## 5. Acceptance Criteria
- [ ] Orchestrator rejects handoff if `requirement_verification.verification_status = "failed"` or `"partial"`.
- [ ] Orchestrator accepts handoff only if `requirement_verification.verification_status = "passed"`.
- [ ] Handoff state schema includes `requirement_verification` fields.
- [ ] DOC-3 includes a requirement verification section in the implementation phase.
- [ ] DOC-4 documents the new verification step in the ideation-to-release journey.
- [ ] IDEA-025 entry added to `docs/ideas/IDEAS-BACKLOG.md` with status `[REFINED]`.
- [ ] Memory Bank updated to reflect progress.

---

## 6. Open Questions
1. Should the Orchestrator **auto-generate** the `requirements_list` from refinement artifacts (e.g., `IDEA-NNN.md`)?
2. Should the Orchestrator **auto-update DOC-3** with verification status, or should this be manual?
3. Should the Orchestrator **escalate to the human** if requirement verification fails, or should it auto-reject?
4. Should the Orchestrator **support partial acceptance** (e.g., accept delivered requirements and defer undelivered ones)?

---

## 7. Notes
- This idea is a **governance/process improvement** and does not require new tooling.
- The solution **aligns with IDEA-020 (Orchestrator as Default Mode)** and **RULE 16 (Handoff Protocol)**.
- The solution **complements IDEA-012A/B/C (Ideation-to-Release Pipeline)** by adding a verification gate to the implementation phase.
- The solution **does not overlap** with TECH-002 (Auto-Detect Merged Features), which is now complete.