---
id: ADR-013
title: Co-Acceptance of IDEA-014 and IDEA-015
status: Accepted
decision_date: 2026-04-08
decided_by: Product Owner
scope: Governance process
---

# ADR-013: Co-Acceptance of IDEA-014 and IDEA-015

## Context

IDEA-014 (Canonical Docs Status Governance) and IDEA-015 (Mandatory Release Coherence Audit) were refined together in session REFINEMENT-2026-04-08-003. The refinement revealed that these ideas are **complementary and interdependent**:

| Aspect | IDEA-014 | IDEA-015 |
|--------|----------|----------|
| **Role** | Policy/Specification | Enforcement/Implementation |
| **Delivers** | RULE 8 enhancement, status lifecycle definition | GitHub Actions release gate |
| **Validates** | Status transition rules documented | Status transition rules followed |

**Key Insight:** IDEA-014 provides the **SPEC** (what the status lifecycle should be), while IDEA-015 provides the **ENFORCEMENT** (how to ensure the lifecycle is followed). Neither idea is complete without the other.

## Decision

**Co-accept IDEA-014 and IDEA-015 together as [ACCEPTED] for v2.7.**

This decision is based on:
1. **Atomicity**: The ideas were refined together and depend on each other for full implementation
2. **Completeness**: IDEA-014's acceptance criteria (AC-4) cannot be verified without IDEA-015's release gate
3. **Governance Integrity**: Policy without enforcement is ineffective; enforcement without policy is directionless

## Status Updates

| Idea | Previous Status | New Status | Notes |
|------|-----------------|------------|-------|
| IDEA-014 | [REFINED] | [ACCEPTED] | Co-accepted with IDEA-015 |
| IDEA-015 | [REFINED] | [ACCEPTED] | Co-accepted with IDEA-014 |

## Consequences

### Positive
- **Governance Completeness**: Both policy and enforcement are now formally accepted
- **Release Integrity**: The v2.7 release will include both the status lifecycle definition and its enforcement mechanism
- **Documentation Clarity**: Canonical docs will have explicit status transitions and automated checks

### Negative
- **Implementation Complexity**: Both ideas must be implemented together, requiring coordination
- **Testing Overhead**: The release gate (IDEA-015) must be tested with the status lifecycle (IDEA-014) to ensure they work together

### Mitigations
- **Phased Implementation**: IDEA-014 (RULE updates) can be implemented first, followed by IDEA-015 (release gate)
- **Shared Documentation**: DOC-4 will be updated to document both the status lifecycle and the release gate procedure

## Next Steps

1. **Update RULE 8**: Add explicit status lifecycle definition (Draft → In Review → Frozen)
2. **Implement Release Gate**: Create `.github/workflows/release-gate.yml` to enforce Frozen status at release tagging
3. **Update Documentation**: DOC-4 must document both the status lifecycle and the release gate procedure
4. **Coordinate Implementation**: Ensure IDEA-014 and IDEA-015 are implemented in sync

## Dependencies

| Dependency | Type | Reason |
|------------|------|--------|
| IDEA-015 | Prerequisite | IDEA-014's AC-4 requires IDEA-015's release gate |
| RULE 8 | Governance | Must be updated to include status lifecycle definition |
| DOC-4 | Documentation | Must document both the status lifecycle and release gate |

## Historical Context

The v2.6 release had a critical governance gap: DOC-1 was still marked "Draft" when it should have been "Frozen". This was a symptom of missing enforcement, not missing policy. RULE 8.1 already stated that Frozen documents are read-only — it just wasn't being enforced. This ADR closes that gap by accepting both the policy (IDEA-014) and its enforcement (IDEA-015) together.