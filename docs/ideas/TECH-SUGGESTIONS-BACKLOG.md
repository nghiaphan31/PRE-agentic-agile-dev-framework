# Technical Suggestions Backlog

**Last updated:** 2026-04-08

## How to Use

Technical suggestions ("How" proposals) are tracked separately from business requirements ("What" proposals). They do NOT go directly into PRD or architecture — they are parked, evaluated, and integrated appropriately.

- Add new technical suggestions immediately when they arise
- Create a corresponding `TECH-NNN.md` file with full details
- Status is evaluated by the Architect

## Status Legend

| Status | Meaning |
|--------|---------|
| `[IDEA]` | Captured, not yet evaluated |
| `[REFINED]` | Requirements and feasibility analyzed; awaiting implementation decision |
| `[INVESTIGATING]` | Under technical investigation |
| `[ACCEPTED]` | Approved for implementation |
| `[REJECTED]` | Not feasible or not worth the effort |
| `[DEFERRED]` | Good idea, but not this release |

## Backlog

| ID | Title | Captured | Status | Complexity | Notes |
|----|-------|----------|--------|------------|-------|
| TECH-001 | Investigate MinMax M2.7 Batch API Support | 2026-04-01 | [IDEA] | 6/10 | Lower costs vs Anthropic batch |
| TECH-002 | Auto-Detect Merged Features for Release Scope | 2026-04-08 | [IMPLEMENTED] | 7/10 | All options implemented: Option A (Git Hook), Option B (PR merge trigger), Option C (push/nightly), R-005 (tag-creation trigger). R-006 added: ALL commits on develop since previous release tag MUST be in scope. |
| TECH-003 | Single Source of Truth for Release Tracking | 2026-04-08 | [IMPLEMENTED] | 3/10 | Implemented: release-consistency-check.yml created, .clinerules RULE 2 updated, DOC-5/DOC-3-CURRENT.md fixed. |
| TECH-004 | Master Traceability Tree | 2026-04-08 | [ACCEPTED-EXTENSION] | 5/10 | Extension of ADR-006. stabilization/vX.Y replaces release/vX.Y.Z. Refining workflow documented. |
| TECH-005 | Hybrid Naming Convention | 2026-04-08 | [IDEA] | 3/10 | proposal to blend IDEA/TECH prefixes with feature/bugfix/lab/hotfix. |
| TECH-006 | Dummy Task Mode Switch | 2026-04-08 | [IMPLEMENTED] | 2/10 | Implemented: Added auto-switch instruction to RULE 16.5 — invoke switch_mode("orchestrator") at session start |
| TECH-004 | Master Traceability Tree — Enhanced Git Flow | 2026-04-08 | [ACCEPTED-EXTENSION] | 8/10 | Extension of ADR-006. stabilization/vX.Y replaces release/vX.Y.Z. Refining workflow (lab→feature→develop) documented. |
| TECH-005 | Timebox-First Branch Naming Convention | 2026-04-08 | [IMPLEMENTED] | 3/10 | RULE 10 updated: feature/{Timebox}/{IDEA-NNN}-{slug} pattern. Implemented in v2.14 scope. |

---

*Generated 2026-04-08*
