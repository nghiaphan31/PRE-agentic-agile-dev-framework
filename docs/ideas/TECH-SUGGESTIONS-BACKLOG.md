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
| TECH-002 | Auto-Detect Merged Features for Release Scope | 2026-04-08 | [ACCEPTED] | 7/10 | All options implemented: Option A (Git Hook), Option B (PR merge trigger), Option C (push/nightly), R-005 (tag-creation trigger). R-006 added: ALL commits on develop since previous release tag MUST be in scope. |
| TECH-003 | Single Source of Truth for Release Tracking | 2026-04-08 | [ACCEPTED] | 3/10 | Implemented: release-consistency-check.yml created, .clinerules RULE 2 updated, DOC-5/DOC-3-CURRENT.md fixed. |
| TECH-004 | Master Traceability Tree — Enhanced Git Flow | 2026-04-08 | [DEFERRED] | 8/10 | Extends ADR-006 with lab/, bugfix/, release/ branches; Refining workflow (lab→feature); Hot vs Cold fix separation; Release parallelism. **RE-REFINED 2026-04-08:** `--no-ff` extracted as standalone — accepted for v2.14. Naming convention (feature/YYYY/QN/) is BREAKING CHANGE vs ADR-006 — deferred. Hybrid naming pattern proposed: feature/{IDEA-NNN}/{YYYY}Q{N}-{slug}. Full analysis in REFINE-2026-04-08-TECH-004.md Section 10. |
| TECH-005 | Timebox-First Branch Naming Convention | 2026-04-08 | [REFINED] | 3/10 | Corrected per Gemini: feature/{Timebox}/{IDEA-NNN}-{slug} — timebox grouping (2026-Q2, Sprint-42) instead of IDEA folder. Forward-compatible (existing branches don't need rename). Awaiting ACCEPTED/REJECTED. |

---

*Generated 2026-04-08*
