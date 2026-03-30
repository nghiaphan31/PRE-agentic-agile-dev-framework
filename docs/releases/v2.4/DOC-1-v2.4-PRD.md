---
doc_id: DOC-1
release: v2.4
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-03-30
authors: [Product Owner, Human]
previous_release: docs/releases/v2.3/DOC-1-v2.3-PRD.md
---

# DOC-1 -- Product Requirements Document (v2.4)

> **Status: DRAFT** -- This document is in draft for v2.4.0 release. It will be frozen upon QA approval.

---

## Overview

v2.4 is a **minor release** capturing **IDEA-012**: **Ideation-to-Release Governance Pipeline** (Calypso Orchestration v1).

This release formalizes the full ideation-to-release pipeline with:
- **SyncDetector** (parallel work detection)
- **BranchTracker** (GitFlow compliance)
- **ExecutionTracker** (live progress tracking)
- **IntakeAgent** (structured idea intake)
- **IdeasDashboard** (centralized backlog management)

This release follows the **structured process** per [ADR-010](docs/ideas/ADR-010-dev-tooling-process-bypass.md).

---

## Scope of v2.4

| IDEA | Title | Type | Tier | Status |
|------|-------|------|------|--------|
| IDEA-012 | Ideation-to-Release Governance Pipeline | feature | Minor | [IMPLEMENTED] |

---

## IDEA-012: Ideation-to-Release Governance Pipeline

### Problem Statement

The current ideation process lacks:
- **Structured intake**: Ideas are captured ad-hoc without classification or routing.
- **Sync detection**: Parallel work is not detected, leading to merge conflicts and redundant effort.
- **Branch governance**: GitFlow compliance is manual and error-prone.
- **Execution tracking**: Progress is not tracked in real-time, leading to blind spots.
- **Backlog management**: Ideas are scattered across documents, making prioritization difficult.

### Solution

**Calypso Orchestration v1** — A full ideation-to-release pipeline with:

| Component | Purpose | Location |
|-----------|---------|----------|
| **IntakeAgent** | Structured idea intake with classification (BUSINESS/TECHNICAL) and routing to the correct backlog. | `src/calypso/intake_agent.py` |
| **SyncDetector** | Detects parallel work and sync opportunities (CONFLICT, REDUNDANCY, DEPENDENCY, SHARED_LAYER, NO_OVERLAP). | `src/calypso/sync_detector.py` |
| **BranchTracker** | Enforces GitFlow compliance (ADR-006) and tracks release progress. | `src/calypso/branch_tracker.py` |
| **ExecutionTracker** | Tracks live progress across all active ideas and releases. | `src/calypso/execution_tracker.py` |
| **IdeasDashboard** | Centralized backlog management with triage status and refinement tracking. | `src/calypso/ideas_dashboard.py` |

### Key Features

1. **Structured Intake**
   - Ideas are classified as **BUSINESS** (WHAT) or **TECHNICAL** (HOW).
   - Business ideas route to `IDEAS-BACKLOG.md`.
   - Technical ideas route to `TECH-SUGGESTIONS-BACKLOG.md`.
   - Sync detection runs automatically at intake.

2. **Sync Detection**
   - Detects 5 sync categories: CONFLICT, REDUNDANCY, DEPENDENCY, SHARED_LAYER, NO_OVERLAP.
   - Prevents merge conflicts and redundant work.
   - Coordinates timing for shared components.

3. **Branch Governance**
   - Enforces GitFlow (ADR-006) with 3-branch model: `main`, `develop`, `develop-vX.Y`.
   - Tracks release progress and prevents forbidden actions (e.g., committing directly to `main`).
   - Coordinates feature branch merges to avoid conflicts.

4. **Execution Tracking**
   - Tracks live progress across all active ideas and releases.
   - Updates `DOC-3` execution chapter, `memory-bank/progress.md`, and `EXECUTION-TRACKER-vX.Y.md` in real-time.
   - Ensures consistency across all tracking documents.

5. **Backlog Management**
   - Centralized dashboard for all ideas with triage status (IDEA, REFINED, DEFERRED, IN_PROGRESS, COMPLETE).
   - Tracks refinement sessions and parked technical suggestions.

### Requirements

- Python 3.11+
- `GitPython>=3.1.40` (for BranchTracker)
- `jsonschema>=4.23.0` (for intake validation)

### Out of Scope

- Multi-developer collaboration (planned for v2.5).
- Brownfield workflow (planned for v2.6).
- DOC6 revision (pending).

---

## v2.3 Workflow Preserved

All v2.0, v2.1, v2.2, and v2.3 features and workflows remain unchanged:

- Hot/Cold memory architecture
- Template folder enrichment
- Calypso orchestration scripts (Phase 2, 3, 4)
- Global Brain / Librarian Agent
- 4 Agile personas (.roomodes)
- Memory Bank (7 files in hot-context/)
- ADR-010 governance (structured vs ad-hoc paths)
- GitFlow branching model (ADR-006)
- Generic Anthropic Batch API Toolkit (IDEA-009)

---

## Out of Scope for v2.4

- New Calypso phases beyond v1.
- Multi-developer collaboration features.
- Brownfield workflow.
- DOC6 revision.

---

## DOC-1 / DOC-2 Coherency (ADR-010)

Per ADR-010, this DOC-1 and the corresponding DOC-2 must be coherent:
- All requirements in DOC-1 have a corresponding architecture element in DOC-2.
- All architecture elements in DOC-2 support a requirement in DOC-1.
- No blind spots: anything not in DOC-1 is not required; anything not in DOC-2 is not architecture.

---

*End of DOC-1 v2.4 (Draft)*