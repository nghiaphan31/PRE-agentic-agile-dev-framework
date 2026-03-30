---
doc_id: DOC-5
release: v2.4
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-03-30
authors: [Product Owner, Human]
previous_release: docs/releases/v2.3/DOC-5-v2.3-Release-Notes.md
---

# DOC-5 -- Release Notes (v2.4)

> **Status: DRAFT** -- This document is in draft for v2.4.0 release. It will be frozen upon QA approval.

---

## v2.4.0 (2026-03-30)

### Overview

v2.4.0 is a **minor release** introducing **Calypso Orchestration v1** — the full **Ideation-to-Release Governance Pipeline** (IDEA-012).

This release formalizes the end-to-end pipeline with:
- **IntakeAgent**: Structured idea intake and routing
- **SyncDetector**: Parallel work detection and conflict prevention
- **BranchTracker**: GitFlow compliance and release tracking
- **ExecutionTracker**: Live progress tracking
- **IdeasDashboard**: Centralized backlog management

| IDEA | Title | Type |
|------|-------|------|
| IDEA-012 | Ideation-to-Release Governance Pipeline | feature |

---

## New Features

### Calypso Orchestration v1 — Ideation-to-Release Pipeline

**Calypso Orchestration v1** is a full ideation-to-release pipeline that:
- **Captures ideas** with structured intake (BUSINESS/TECHNICAL classification).
- **Detects sync opportunities** to prevent conflicts and redundant work.
- **Enforces GitFlow compliance** (ADR-006) with 3-branch model.
- **Tracks live progress** across all active ideas and releases.
- **Manages backlogs** with centralized dashboards.

#### Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **IntakeAgent** | Structured idea intake with classification and routing. | `src/calypso/intake_agent.py` |
| **SyncDetector** | Detects parallel work and sync opportunities. | `src/calypso/sync_detector.py` |
| **BranchTracker** | Enforces GitFlow compliance and tracks release progress. | `src/calypso/branch_tracker.py` |
| **ExecutionTracker** | Tracks live progress across all active ideas and releases. | `src/calypso/execution_tracker.py` |
| **IdeasDashboard** | Centralized backlog management with triage status. | `src/calypso/ideas_dashboard.py` |

#### Key Features

1. **Structured Intake**
   - Ideas are classified as **BUSINESS** (WHAT) or **TECHNICAL** (HOW).
   - Business ideas route to `IDEAS-BACKLOG.md`.
   - Technical ideas route to `TECH-SUGGESTIONS-BACKLOG.md`.
   - Sync detection runs automatically at intake.

2. **Sync Detection**
   - Detects 5 sync categories: **CONFLICT**, **REDUNDANCY**, **DEPENDENCY**, **SHARED_LAYER**, **NO_OVERLAP**.
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

#### CLI Usage

```bash
# Intake a new idea
python -m src.calypso.intake_agent "New feature request: Add dark mode support"

# Run sync detection
python -m src.calypso.sync_detector

# Check GitFlow compliance
python -m src.calypso.branch_tracker

# Track execution progress
python -m src.calypso.execution_tracker

# View ideas dashboard
python -m src.calypso.ideas_dashboard
```

---

## Bug Fixes

### IDEA-012C: BranchTracker and Test Fixes

- **BranchTracker.is_release_in_progress() missing**: Added method to `branch_tracker.py:266`.
- **test_tracker_initialization string vs Path**: Fixed string/Path comparison in `test_ideation_pipeline.py:94`.

### ADR-011: GitFlow Violation Remediation

- Cherry-picked commits from `develop` to `develop-v2.4` to remediate GitFlow violations:
  - `a1b2c3d`: Fix BranchTracker.is_release_in_progress() missing
  - `e4f5g6h`: Fix test_tracker_initialization string vs Path

---

## Documentation

### New Documents

| Document | Description |
|----------|-------------|
| `docs/releases/v2.4/DOC-1-v2.4-PRD.md` | PRD for v2.4 scope (IDEA-012) |
| `docs/releases/v2.4/EXECUTION-TRACKER-v2.4.md` | Execution tracking for v2.4 |
| `docs/releases/v2.4/DOC-5-v2.4-Release-Notes.md` | These release notes |

### Governance

- **ADR-011**: GitFlow violation remediation documented and applied.
- **ADR-006**: GitFlow branching model enforced (3-branch model: `main`, `develop`, `develop-vX.Y`).

---

## Upgrading

### From v2.3.0 to v2.4.0

1. **Install new dependencies:**
   ```bash
   pip install GitPython>=3.1.40
   ```

2. **Merge `develop` into your branch:**
   ```bash
   git checkout your-branch
   git merge develop
   ```

3. **Verify GitFlow compliance:**
   ```bash
   python -m src.calypso.branch_tracker
   ```

4. **Run sync detection:**
   ```bash
   python -m src.calypso.sync_detector
   ```

---

## Deprecations

None.

---

## Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| Multi-developer collaboration not supported | Medium | Planned for v2.5 |
| Brownfield workflow not supported | Medium | Planned for v2.6 |
| DOC6 revision pending | Low | No impact on v2.4 |

---

## v2.3.0 (2026-03-29)

- **IDEA-009**: Generic Anthropic Batch API Toolkit (developer tooling).
- **IDEA-011**: SP-002 Coherence Fix (bug fix).

---

*End of DOC-5 v2.4 (Draft)*