---
id: IDEA-012B
title: Ideation-to-Release — PHASE-B Core Logic
status: ACCEPTED
target_release: v2.4
source: Architect mode 2026-03-30
source_files: [plans/governance/PLAN-ideation-to-release-full-process.md]
captured: 2026-03-30
captured_by: Architect mode
planned_start: After IDEA-012A merged
---

## Description

PHASE-B of the Ideation-to-Release governance process implementation. Core logic layer: implements the synchronization detection engine and enhanced backlog management.

## Motivation

After PHASE-A establishes the foundation (files + rules), PHASE-B implements the intelligent components:
1. SyncDetector class — real-time overlap/conflict detection
2. Enhanced IDEA-NNN.md structure with refinement logs
3. Refinement session templates
4. Basic branch tracking for sync detection

## Affected Documents

- `src/calypso/sync_detector.py`: New file — synchronization detection engine
- `src/calypso/refinement_workflow.py`: New file — refinement session management
- `docs/ideas/IDEA-NNN.md`: Enhanced structure with refinement log template
- `docs/conversations/`: New folder with refinement session log template

## Implementation Details

### PHASE-B Deliverables

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | `src/calypso/sync_detector.py` — basic overlap detection | ⏳ |
| 2 | `src/calypso/refinement_workflow.py` — refinement session logic | ⏳ |
| 3 | Enhanced IDEA-NNN.md template with refinement log section | ⏳ |
| 4 | `docs/conversations/REFINEMENT-YYYY-MM-DD-{id}.md` template | ⏳ |
| 5 | Sync detection basic implementation (file overlap analysis) | ⏳ |

### Complexity Score

**Score: 7/10** (Medium-High)
- Requires understanding of existing Calypso orchestrator
- Git diff analysis for branch overlap
- Semantic similarity for requirement overlap

### Branch

`feature/IDEA-012B-phases-implementation` from `develop`

### Refinement Approach

**Hybrid** — Orchestrator decides based on complexity score:
- Score 1-3: Asynchronous (document exchange)
- Score 4-6: Hybrid (quick sync, then async)
- Score 7-10: Synchronous (live conversation)

## Dependencies

- IDEA-012A must be IMPLEMENTED first

## Pre-requisites

- PHASE-A complete and merged to develop
- TECH-SUGGESTIONS-BACKLOG.md created
- RULE 11, 12, 13 in .clinerules

## Disposition

**Decision:** ACCEPTED — Part of Option B (live-test process)
**Planned:** v2.4 release, after IDEA-012A merged

## Verification

- [ ] All new Python files pass syntax check
- [ ] Unit tests for SyncDetector pass
- [ ] Refinement workflow handles both sync and async modes
- [ ] Sync detection correctly identifies file overlaps

## History

- 2026-03-30: Created by Architect mode — Part of three-phase implementation
- 2026-03-30: Approved by Human — Option B (live-test process)
- 2026-03-30: Planned for implementation after IDEA-012A