# PLAN: IDEA-022 — Ideation-to-Release Journey — Operational Reference

**Author:** Architect (mode: architect)  
**Created:** 2026-04-08  
**IDEA:** IDEA-022  
**Target Release:** v2.10  
**Status:** Draft — Awaiting Human Approval

---

## 1. Context

**Problem:** The workbench has implemented a full ideation-to-release governance pipeline (IDEA-012A/B/C), but there is no comprehensive human-readable runbook describing the complete journey from raw vague idea to released feature.

**Solution:** Create a new chapter in DOC-4 (Operations Guide, v2.10) called **"Ideation-to-Release Journey — Operational Reference"** that documents the complete journey with:
- **WHO** does what (roles)
- **WHAT** is the expected deliverable
- **WITH WHOM** (collaboration)
- **WHERE** (Git branch context)
- **HOW** (tools, inputs/dependencies, rules applied)
- **Mermaid diagrams** for each phase's workflow (synergy with IDEA-016)
- **Decision trees** for branching paths at each phase

---

## 2. Scope of Changes

### 2.1 Files Modified

| File | Change |
|------|--------|
| `docs/releases/v2.10/DOC-4-v2.10-Operations-Guide.md` | Add new chapter "Ideation-to-Release Journey" |

### 2.2 Files NOT Changed

| File | Reason |
|------|--------|
| `docs/releases/v2.10/DOC-1-v2.10-PRD.md` | Not in scope |
| `docs/releases/v2.10/DOC-2-v2.10-Architecture.md` | Not in scope |
| `docs/releases/v2.10/DOC-3-v2.10-Implementation-Plan.md` | Already release-specific |
| `docs/releases/v2.10/DOC-5-v2.10-Release-Notes.md` | Already release-specific |

---

## 3. Chapter Structure

### 3.1 Proposed TOC Entry

```
## X. Ideation-to-Release Journey — Operational Reference

X.1 [Introduction](#x1-introduction)
X.2 [Phase 0: Idea Intake](#x2-phase-0-idea-intake)
X.3 [Phase 1: Idea Refinement](#x3-phase-1-idea-refinement)
X.4 [Phase 2: Triage and Release Assignment](#x4-phase-2-triage-and-release-assignment)
X.5 [Phase 3: Implementation Planning](#x5-phase-3-implementation-planning)
X.6 [Phase 4: Development](#x6-phase-4-development)
X.7 [Phase 5: Documentation](#x7-phase-5-documentation)
X.8 [Phase 6: QA and Validation](#x8-phase-6-qa-and-validation)
X.9 [Phase 7: Release](#x9-phase-7-release)
X.10 [Decision Trees Summary](#x10-decision-trees-summary)
```

---

## 4. Detailed Phase Documentation

### X.1 Introduction

- **Purpose:** This chapter provides a complete operational reference for the ideation-to-release journey
- **Target audience:** Humans and agents working on the workbench
- **How to use:** Follow sequentially or jump to specific phase
- **Mermaid diagram:** High-level journey overview

### X.2 Phase 0: Idea Intake

| Field | Value |
|-------|-------|
| **WHO** | Human (initiator), Orchestrator (intake agent) |
| **WHAT** | Raw idea captured in IDEAS-BACKLOG.md or TECH-SUGGESTIONS-BACKLOG.md |
| **WITH WHOM** | Orchestrator routes to appropriate backlog |
| **WHERE** | No Git branch (pre-ideation) |
| **HOW** | Verbal or structured input; RULE 13 (Ideation Intake) |
| **Tools** | Orchestrator intake form |
| **Inputs** | Human raw idea |
| **Outputs** | New IDEA entry with status `[IDEA]` |
| **Rules** | RULE 13 (Ideation Intake) |

**Files Modified:**
- `docs/ideas/IDEAS-BACKLOG.md` OR `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md` (new entry added)
- `docs/conversations/YYYY-MM-DD-orchestrator-intake-IDEA-NNN.md` (conversation log)

**Entry Criteria:**
- Human expresses a new idea, request, or remark
- Input is outside current task scope (RULE 13 detection)

**Exit Criteria:**
- IDEA entry created with status `[IDEA]`
- Backlog file updated with new entry
- Conversation log created
- Human acknowledged with routing confirmation

**Decision Tree:**
- Is idea business (WHAT) → IDEAS-BACKLOG
- Is idea technical (HOW) → TECH-SUGGESTIONS-BACKLOG

**Mermaid Diagram:** Intake workflow

### X.3 Phase 1: Idea Refinement

| Field | Value |
|-------|-------|
| **WHO** | Human (Product Owner), Orchestrator (facilitator), Architect (technical feasibility) |
| **WHAT** | Structured requirements and feasibility assessment |
| **WITH WHOM** | Orchestrator, Architect (if technical) |
| **WHERE** | No Git branch (pre-refinement) |
| **HOW** | Structured refinement session |
| **Inputs** | Raw idea, IDEAS-BACKLOG.md entry |
| **Outputs** | Updated IDEA entry with status `[REFINED]` and structured requirements |
| **Rules** | RULE 13 (Refinement options) |

**Files Modified:**
- `docs/ideas/IDEA-NNN-{slug}.md` (status updated to `[REFINED]`)
- `docs/conversations/REFINEMENT-YYYY-MM-DD-NNN.md` (refinement conversation log)

**Entry Criteria:**
- IDEA has status `[IDEA]`
- Human chooses "Refine Now" option

**Exit Criteria:**
- IDEA status updated to `[REFINED]`
- Structured requirements documented in IDEA file
- Refinement conversation log created
- Human approves final requirements

**Decision Tree:**
- Refine now? → Proceed to Phase 2
- Defer? → Mark as `[DEFERRED]`
- Sync first? → Run sync detection (RULE 11)

**Mermaid Diagram:** Refinement workflow with decision points

### X.4 Phase 2: Triage and Release Assignment

| Field | Value |
|-------|-------|
| **WHO** | Human (Product Owner), Orchestrator (sync detector) |
| **WHAT** | Idea triaged and assigned to release |
| **WITH WHOM** | Orchestrator (sync detection) |
| **WHERE** | No Git branch |
| **HOW** | Triage dashboard, sync detection |
| **Inputs** | Refined IDEA, current release backlog |
| **Outputs** | IDEA assigned to release (e.g., v2.11), status `[TRIAGED]` |
| **Rules** | RULE 11 (Synchronization Awareness) |

**Files Modified:**
- `docs/ideas/IDEA-NNN-{slug}.md` (status updated to `[TRIAGED]`, release assigned)
- `memory-bank/hot-context/progress.md` (checkbox added for new IDEA)

**Entry Criteria:**
- IDEA has status `[REFINED]`
- Sync detection completed (RULE 11)

**Exit Criteria:**
- IDEA assigned to target release
- IDEA status updated to `[TRIAGED]`
- Any conflicts resolved by human
- Progress tracker updated

**Decision Tree:**
- Any conflicts? → Human arbitrates (🔴 CONFLICT)
- Redundant ideas? → Merge (🟡 REDUNDANCY)
- Dependency exists? → Reorder (🔵 DEPENDENCY)
- No overlap? → Proceed (🟢 NO_OVERLAP)

**Mermaid Diagram:** Triage workflow with sync categories

### X.5 Phase 3: Implementation Planning

| Field | Value |
|-------|-------|
| **WHO** | Developer, Architect |
| **WHAT** | Implementation plan created |
| **WITH WHOM** | Architect (for complex features) |
| **WHERE** | `develop-vX.Y` branch |
| **HOW** | Feature branch created, implementation planned |
| **Inputs** | Triaged IDEA, DOC-3 (release-specific) |
| **Outputs** | `feature/IDEA-NNN-slug` branch, updated DOC-3 |
| **Rules** | RULE 10 (GitFlow), RULE 12 (Canonical Docs) |

**Files Modified:**
- `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md` (IDEA added to scope)
- `plans/IDEA-NNN/PLAN-IDEA-NNN-{slug}.md` (implementation plan created)

**Files Created:**
- `feature/IDEA-NNN-{slug}` branch (from `develop-vX.Y`)

**Entry Criteria:**
- IDEA has status `[TRIAGED]`
- Release branch `develop-vX.Y` exists or will be created

**Exit Criteria:**
- Feature branch `feature/IDEA-NNN-{slug}` created
- DOC-3 updated with IDEA in scope
- Implementation plan written and approved

**Mermaid Diagram:** Branch creation workflow

### X.6 Phase 4: Development

| Field | Value |
|-------|-------|
| **WHO** | Developer |
| **WHAT** | Feature implemented and committed |
| **WITH WHOM** | QA Engineer (for testing) |
| **WHERE** | `feature/IDEA-NNN-slug` branch |
| **HOW** | Code implementation, unit tests, commit on feature branch |
| **Inputs** | Feature branch, implementation plan |
| **Outputs** | Committed changes on feature branch |
| **Rules** | RULE 10 (GitFlow), Git commit conventions |

**Files Modified:**
- Source code files (`.py`, `.md`, `.ps1`, etc.)
- Test files (`src/calypso/tests/*.py`)

**Files Created:**
- New source files as needed by implementation

**Entry Criteria:**
- Feature branch exists
- Implementation plan approved

**Exit Criteria:**
- All code implemented
- Unit tests written and passing
- Commits made with Conventional Commits format
- GitHub Actions CI passing

**Mermaid Diagram:** Development workflow on feature branch

### X.7 Phase 5: Documentation

| Field | Value |
|-------|-------|
| **WHO** | Developer, Architect |
| **WHAT** | Canonical docs updated (DOC-1, DOC-2, DOC-4) |
| **WITH WHOM** | Product Owner (for requirements clarification) |
| **WHERE** | `feature/IDEA-NNN-slug` branch |
| **HOW** | Update cumulative docs per release scope |
| **Inputs** | Feature implementation, DOC-1/DOC-2/DOC-4 |
| **Outputs** | Updated canonical docs on feature branch |
| **Rules** | RULE 12 (Canonical Docs) |

**Files Modified:**
- `docs/releases/vX.Y/DOC-1-vX.Y-PRD.md` (if PRD changes needed)
- `docs/releases/vX.Y/DOC-2-vX.Y-Architecture.md` (if architecture changes needed)
- `docs/releases/vX.Y/DOC-4-vX.Y-Operations-Guide.md` (if operations changes needed)

**Entry Criteria:**
- Feature implementation complete
- Feature branch has passing CI

**Exit Criteria:**
- All affected cumulative docs updated
- DOCs have correct front matter (`cumulative: true`)
- GitHub Actions CI passes

**Mermaid Diagram:** Documentation update workflow

### X.8 Phase 6: QA and Validation

| Field | Value |
|-------|-------|
| **WHO** | QA Engineer |
| **WHAT** | Feature validated and tested |
| **WITH WHOM** | Developer (for bug fixes) |
| **WHERE** | `feature/IDEA-NNN-slug` branch |
| **HOW** | Test execution, coherence audit, QA report |
| **Inputs** | Feature branch, test suite |
| **Outputs** | QA report, test results |
| **Rules** | RULE 8 (QA Validation) |

**Files Modified:**
- `docs/qa/vX.Y/QA-REPORT-vX.Y.md` (QA report updated)

**Files Created:**
- `docs/qa/vX.Y/submit_batch*.py` (batch test scripts if needed)

**Entry Criteria:**
- Feature branch merged to `develop-vX.Y`
- All code commits on feature branch

**Exit Criteria:**
- QA report generated and approved
- All tests passing
- Coherence audit passed (if required)
- Human approves QA results

**Mermaid Diagram:** QA workflow

### X.9 Phase 7: Release

| Field | Value |
|-------|-------|
| **WHO** | Scrum Master (merge coordination) |
| **WHAT** | Feature merged and released |
| **WITH WHOM** | Developer, Product Owner (approval) |
| **WHERE** | `develop-vX.Y` → `develop` → `main` |
| **HOW** | PR merge, tag creation, release |
| **Inputs** | Feature branch, QA approval |
| **Outputs** | Merged to develop, tagged release |
| **Rules** | RULE 10 (GitFlow), RULE 12 (Canonical Docs) |

**Files Modified:**
- `docs/DOC-*-CURRENT.md` (pointers updated after release)
- `memory-bank/hot-context/progress.md` (IDEA checkbox marked complete)
- `memory-bank/hot-context/activeContext.md` (updated for next task)

**Files Created:**
- Release tag `vX.Y.0` on `main`
- `docs/releases/vX.Y/DOC-*-vX.Y-*.md` (frozen docs after release)

**Entry Criteria:**
- QA approved
- All checks passing
- Human approves release

**Exit Criteria:**
- Fast-forward merge to `develop` completed
- Tag `vX.Y.0` pushed to origin
- DOC-*-CURRENT.md pointers updated
- Memory Bank updated

**Decision Tree:**
- All checks pass? → Merge to develop-vX.Y
- develop-vX.Y complete? → Merge to develop
- develop stable? → Tag vX.Y.0 on main

**Mermaid Diagram:** Release workflow (GitFlow visualization)

### X.10 Decision Trees Summary

Consolidated decision trees for all phases with visual flowcharts.

---

## 5. Implementation Steps

### PHASE A: Feature Branch Setup
- [ ] Create `feature/IDEA-022-ideation-to-release-journey` from `develop`

### PHASE B: Update DOC-4-v2.10
- [ ] Read existing DOC-4-v2.9-Operations-Guide.md for style consistency
- [ ] Add new chapter "Ideation-to-Release Journey — Operational Reference"
- [ ] Include all 10 sections (X.1 through X.10)
- [ ] Include Mermaid diagrams for each phase
- [ ] Include decision trees for each phase

### PHASE C: Validation
- [ ] Verify Mermaid diagrams render correctly
- [ ] Verify line count meets cumulative requirements (DOC-4 >= 300 lines)
- [ ] Check front matter has `cumulative: true`

### PHASE D: Git Operations
- [ ] Commit to feature branch
- [ ] Fast-forward merge to `develop`
- [ ] Update Memory Bank

---

## 6. Mermaid Diagrams to Include

| Phase | Diagram Type | Purpose |
|-------|--------------|---------|
| X.1 | Flowchart | High-level journey overview |
| X.2 | Flowchart | Intake workflow with routing |
| X.3 | Flowchart | Refinement with decision points |
| X.4 | Flowchart | Triage with sync categories |
| X.5 | Flowchart | Branch creation workflow |
| X.6 | Git graph | Development on feature branch |
| X.7 | Flowchart | Documentation update flow |
| X.8 | Flowchart | QA validation workflow |
| X.9 | Git graph | Release GitFlow (develop→main) |
| X.10 | Flowchart | Consolidated decision trees |

---

## 7. Human Approvals Needed

- [ ] Approve feature branch creation
- [ ] Approve chapter structure (10 sections)
- [ ] Approve Mermaid diagrams
- [ ] Approve final merge to develop

---

## 8. Notes

- This chapter is additive to DOC-4 (cumulative)
- Does not modify existing sections
- Synergy with IDEA-016 (diagrams) - includes diagrams in this chapter
- IDEA-012A/B/C implemented the machinery; this documents how to use it
