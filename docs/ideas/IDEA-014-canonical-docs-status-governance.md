---
id: IDEA-014
title: Canonical Docs Status Governance
status: [ACCEPTED]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: docs/releases/v2.6/, docs/DOC-*-CURRENT.md, .clinerules
captured: 2026-04-01
captured_by: Developer mode
refined_by: Architect mode
refinement_session: REFINEMENT-2026-04-08-003
---

## Problem Statement

The workbench lacks an **explicit, enforceable status lifecycle** for canonical documents. While RULE 8 defines "Frozen" as read-only and "Draft" as modifiable, it does not specify:

1. **When** a document transitions from Draft → Frozen
2. **Who** is responsible for changing the status
3. **How** the transition should be verified (automated check)
4. **What** happens if a released document is still marked Draft

The v2.6 release was tagged while DOC-1 still showed "Draft" status — a violation that went undetected until the P0 audit. This is a governance gap, not a one-time error.

## Motivation

Canonical documents must accurately reflect the release state at all times:

| Status | Meaning | Who Can Modify |
|--------|---------|----------------|
| **Draft** | Under development, being actively modified | Architect, Product Owner |
| **In Review** | Under review, pending approval | Architect, Product Owner |
| **Frozen** | Released, READ-ONLY per RULE 8.1 | **Nobody** — enforced by GitHub Actions |

**Current gaps:**
1. RULE 8 defines the Two Spaces but not the transition rules
2. No automated check ensures all docs for a tagged release are Frozen
3. DOC-*-CURRENT.md pointer files may drift from actual release state
4. No explicit "In Review" intermediate state defined

## Classification

- **Type:** GOVERNANCE
- **Tier:** Minor (process clarification, not new features)
- **Release Path:** AD-HOC per ADR-010

---

## Refined Requirements

### 1. Status Lifecycle Definition

Canonical documents MUST follow this lifecycle:

```
Draft → In Review → Frozen → (archived)
```

| Status | Transition Trigger | Enforced By |
|--------|-------------------|-------------|
| Draft | Default state during development | N/A |
| In Review | When PR is opened for canonical doc changes | Human review |
| Frozen | When release is tagged (vX.Y.0) | GitHub Actions release gate |

### 2. Scope: What's IN

- **RULE 8 Enhancement**: Add explicit status lifecycle definition
- **RULE 8.1 Update**: Clarify that Frozen means "immutable after release tag"
- **Status Header Requirement**: Every canonical doc MUST have a `status:` field in its frontmatter
- **DOC-*-CURRENT.md**: Must reference the Frozen version immediately after release tag
- **GitHub Actions Gate** (from IDEA-015): Check that all docs for a release are Frozen before tagging

### 3. Scope: What's OUT

- Retroactively fixing v2.6 and earlier (already released)
- Modifying already-Frozen documents in docs/releases/vX.Y/ (forbidden by RULE 8.1)
- Real-time status tracking during development (too complex for v2.7)

### 4. Dependencies

| IDEA | Dependency Type | Reason |
|------|----------------|--------|
| [IDEA-015](IDEA-015-mandatory-release-coherence-audit.md) | **Prerequisite** | Release gate workflow enforces the Frozen status transition; IDEA-014 provides the SPEC, IDEA-015 provides the ENFORCEMENT |
| [IDEA-017](IDEA-017-docs-must-be-cumulative-self-contained.md) | Informational | Already implemented; establishes the line count infrastructure |

**Sync Analysis:**
- 🟢 NO_OVERLAP: IDEA-014 is the policy spec, IDEA-015 is the enforcement mechanism
- 🟡 DEPENDENCY: IDEA-014's acceptance criteria depend on IDEA-015's release gate

### 5. Implementation Complexity

- **Score:** 2/10
- **Reasoning:** This is primarily a RULE clarification and documentation update. The enforcement mechanism (automated status check) is already covered by IDEA-015's release gate. No new scripts or workflows needed beyond what IDEA-015 implements.

---

## Acceptance Criteria

### AC-1: RULE 8 Enhanced

- [ ] RULE 8.1 updated to explicitly define the Draft → In Review → Frozen lifecycle
- [ ] RULE 8.1 specifies that Frozen documents are immutable after release tag
- [ ] Status header (`status:` in frontmatter) is mandated for all canonical docs
- [ ] template/ updated with status header requirement

### AC-2: Status Transition Rules Defined

- [ ] Draft → In Review: When canonical doc PR is opened
- [ ] In Review → Frozen: When release is tagged (vX.Y.0)
- [ ] No other transitions allowed (Frozen documents are immutable)

### AC-3: Pointer Consistency (Documentation)

- [ ] DOC-1-CURRENT.md, DOC-2-CURRENT.md, DOC-4-CURRENT.md updated together
- [ ] DOC-3-CURRENT.md and DOC-5-CURRENT.md point to latest release-specific versions
- [ ] All DOC-*-CURRENT.md files show correct status (Draft/Frozen)

### AC-4: Release Gate Integration (via IDEA-015)

- [ ] Release gate workflow (IDEA-015) checks that all canonical docs for a release are Frozen
- [ ] If any canonical doc for release vX.Y is not Frozen when tagging → **BLOCK**
- [ ] This criterion is satisfied by IDEA-015's implementation

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human remark |
| 2026-04-08 | [REFINED] | Refined by Architect mode — split SPEC (IDEA-014) from ENFORCEMENT (IDEA-015) |
| 2026-04-08 | [ACCEPTED] | Co-accepted with IDEA-015 |

---

## Technical Notes

### Relationship to IDEA-015

IDEA-014 and IDEA-015 are **complementary**:

| Aspect | IDEA-014 | IDEA-015 |
|--------|----------|----------|
| **Role** | Policy/Specification | Enforcement/Implementation |
| **Delivers** | RULE 8 enhancement, status lifecycle definition | GitHub Actions release gate |
| **Validates** | Status transition rules documented | Status transition rules followed |

**Acceptance Criteria dependencies:**
- AC-4 cannot be verified until IDEA-015 is implemented
- IDEA-014 should be marked [ACCEPTED] alongside IDEA-015

### Historical Context

The v2.6 issue (DOC-1 showing Draft when it should be Frozen) was a symptom of missing enforcement, not missing policy. RULE 8.1 already states Frozen docs are read-only — it just wasn't being enforced. IDEA-015's release gate fixes this by automating the check.

---

## Next Steps

1. **Implementation**: Update RULE 8 with status lifecycle (Architect or Developer mode)
2. **Enforcement**: Implement GitHub Actions release gate (Developer mode) — **prerequisite for AC-4**
3. **Documentation**: Update DOC-4 with release gate procedure and status lifecycle
