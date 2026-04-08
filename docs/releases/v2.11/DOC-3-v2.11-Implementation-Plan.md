---
doc_id: DOC-3
release: v2.11
status: Draft
title: Implementation Plan
version: 1.0
date_created: 2026-04-08
authors: [Developer mode, Human]
previous_release: v2.10
cumulative: false
type: release-specific
---

# DOC-3 — Implementation Plan (v2.11)

> **Status: DRAFT** -- This document is under construction for v2.11 release.
> **Release-Specific: YES** -- This document contains ONLY v2.11 implementation scope.
> **Cumulative: NO** -- This is NOT a cumulative document. Historical implementation details are preserved in `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md`.

---

## Table of Contents

1. [v2.11 Release Scope](#1-v211-release-scope)
2. [Release Gate Pre-Checklist](#2-release-gate-pre-checklist)
3. [Key Implementation Decisions](#3-key-implementation-decisions)
4. [Execution Tracking](#4-execution-tracking)
5. [Dependencies and Risks](#5-dependencies-and-risks)

---

## 1. v2.11 Release Scope

v2.11 is a **Governance Release** focused on documentation coherence, backlog maintenance, and release process improvements.

### IDEAS in Scope

| IDEA | Title | Status | Tier |
|------|-------|--------|------|
| IDEA-014 | Canonical Docs Status Governance | IMPLEMENTED | Minor |
| IDEA-015 | Mandatory Release Coherence Audit | IMPLEMENTED | Minor |
| IDEA-016 | Enrich Docs with Mermaid Diagrams | PARTIAL | Minor |
| IDEA-018 | Rules Authoritative & Coherent | PARTIAL | Major |
| IDEA-020 | Authoritative Orchestrator Default | ACCEPTED | Major |
| IDEA-021 | DOC-3/5 Release-Specific | ACCEPTED | Major |
| IDEA-024 | Mandatory Backlog Maintenance | IMPLEMENTED | Minor |

### Features

**Implemented:**
- IDEA-014: Documented canonical docs status governance findings (v2.9 docs show Draft status)
- IDEA-015: Release gate workflow (.github/workflows/release-gate.yml) + DOC-4 Chapter 12
- IDEA-024: RULE 2 updated with mandatory backlog maintenance items

**In Progress:**
- IDEA-016: Enriching DOC-2 with Mermaid diagrams
- IDEA-018: Making rules authoritative and coherent

---

## 2. Release Gate Pre-Checklist

Per IDEA-015, the following checks MUST pass before v2.11 can be tagged:

### Pre-Release Gate Checklist (5 Days Before Target)

| Day | Task | Status |
|-----|------|--------|
| Day -5 | **Scope freeze** — All ideas not [REFINED] are deferred | [ ] |
| Day -4 | **Documentation coherence** — DOC-1 through DOC-5 are aligned | [ ] |
| Day -3 | **Code coherence** — All branches merged, full QA pass | [ ] |
| Day -2 | **Dry run** — RC1 tag, full test suite | [ ] |
| Day -1 | **Final review** — Human approves, v2.11.0 tag applied | [ ] |
| Day 0 | **Announcement** — DOC-5 published, GitHub release created | [ ] |

### Release Gate P0 Blockers

| Check | Severity | Status |
|-------|----------|--------|
| SP-002 (.clinerules vs prompts/SP-002-clinerules-global.md) byte-for-byte sync | P0 BLOCKER | [ ] |
| DOC-1 line count >= 500 (cumulative) | P0 BLOCKER | [ ] |
| DOC-2 line count >= 500 (cumulative) | P0 BLOCKER | [ ] |
| DOC-4 line count >= 300 (cumulative) | P0 BLOCKER | [ ] |
| DOC-3 line count >= 100 (release-specific) | P0 BLOCKER | [ ] |
| DOC-5 line count >= 50 (release-specific) | P0 BLOCKER | [ ] |
| Cumulative pointers consistent (DOC-1, DOC-2, DOC-4) | P0 BLOCKER | [ ] |
| Cumulative flags verified (DOC-1, DOC-2, DOC-4) | P0 BLOCKER | [ ] |

### Release Gate P1 Warnings

| Check | Severity | Status |
|-------|----------|--------|
| DOC-4 contains Release Gate Procedure chapter | P1 WARNING | [ ] |
| P1 issues formally triaged or deferred | P1 WARNING | [ ] |

### How to Run Release Gate

**Automatic:** Push to `develop-v2.11` triggers `.github/workflows/release-gate.yml`

**Manual:** Via GitHub Actions UI → "Release Gate — Pre-Tag Coherence Audit" → Run workflow

---

## 3. Key Implementation Decisions

### IDEA-015: Mandatory Release Coherence Audit

**Decision:** Create `.github/workflows/release-gate.yml` that enforces P0 blockers before release tagging.

**Rationale:** v2.6 had 14 P0, 17 P1, and 14 P2 findings post-release. These should have been caught before tagging.

**Implementation:**
- Extends existing `canonical-docs-check.yml` infrastructure
- Adds SP-002 byte-for-byte sync check
- Adds P0/P1 severity classification
- Documents release gate procedure in DOC-4 Chapter 12

**Consequences:**
- Release tagging is now blocked until all P0 checks pass
- P1 issues require explicit triage or deferral

---

## 4. Execution Tracking

### IDEA-015 Implementation Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Create .github/workflows/release-gate.yml | DONE |
| 2 | Add Chapter 12 (Release Gate Procedure) to DOC-4-v2.11 | DONE |
| 3 | Update DOC-3-v2.11 with release gate pre-checklist | DONE |
| 4 | Update RULE 13 to reference mandatory release gate | PENDING |
| 5 | Update DOC-*-CURRENT.md pointers to v2.11 | PENDING |

---

## 5. Dependencies and Risks

### Dependencies

| IDEA | Dependency Type | Reason |
|------|----------------|--------|
| IDEA-011 | Dependency | SP-002 sync check script is prerequisite |
| IDEA-017 | Dependency | Canonical docs line count infrastructure is prerequisite |
| IDEA-021 | Dependency | Release-specific DOC-3/DOC-5 format is prerequisite |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Gate fails due to SP-002 desync | Low | High | Run `python scripts/rebuild_sp002.py` before tagging |
| Gate fails due to doc line counts | Low | Medium | Ensure cumulative docs meet minimums before release |
| Gate blocks release unexpectedly | Low | High | Test gate on feature branch before release |

---

**End of DOC-3 Implementation Plan (v2.11)**
