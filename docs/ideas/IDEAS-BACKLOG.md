# Ideas Backlog

**Last triage:** 2026-03-28
**Next triage:** At v2.0 release planning (before PHASE-A)

## How to Use

- Add new ideas immediately when they arise — never inject them directly into canonical docs.
- Create a corresponding `IDEA-NNN.md` file with full details.
- Status is updated at triage sessions (before each release starts and after each release is tagged).

## Status Legend

| Status | Meaning |
|---|---|
| `[IDEA]` | Captured, not yet evaluated |
| `[ACCEPTED]` | Approved for a specific release |
| `[IMPLEMENTED]` | Built, tested, in a released version |
| `[DEFERRED]` | Good idea, but not this release |
| `[REJECTED]` | Will never be implemented (reason documented) |
| `[SUPERSEDED]` | Replaced by a better idea |

---

## Backlog

| ID | Title | Source | Captured | Status | Target Release | Disposition |
|---|---|---|---|---|---|---|
| [IDEA-001](IDEA-001-hot-cold-memory.md) | Hot/Cold memory architecture | Batch reviews 1+2 | 2026-03-28 | [ACCEPTED] | v2.0 | Planned for PHASE-A |
| [IDEA-002](IDEA-002-calypso-orchestration.md) | Calypso orchestration scripts (Phase 2-4 pipeline) | Batch reviews 1+2 | 2026-03-28 | [ACCEPTED] | v2.0 | Planned for PHASE-C |
| [IDEA-003](IDEA-003-release-governance.md) | Release governance model | Human 2026-03-28 | 2026-03-28 | [IMPLEMENTED] | v2.0 | Implemented in PHASE-0, commit 1bde967 |
| IDEA-004 | Gherkin linter integration | Batch review 1 | 2026-03-28 | [DEFERRED] | v3.0 | Too complex for v2.0 scope |
| IDEA-005 | Multi-developer collaboration | Batch review 2 | 2026-03-28 | [DEFERRED] | v3.0 | Single-developer workbench by design for v2.0 |
| IDEA-006 | Template enrichment (memory-bank/ subdirs, mcp.json, .clinerules Hot/Cold) | Batch review 2 | 2026-03-28 | [ACCEPTED] | v2.0 | Planned for PHASE-B |
| IDEA-007 | Global Brain / Librarian Agent (Chroma/Mem0, cross-project memory) | Batch review 2 | 2026-03-28 | [IMPLEMENTED] | v2.0 | Implemented in PHASE-D, commit ba61920 |
| IDEA-008 | OpenRouter MinMax M2.7 as default LLM with Claude fallback on consecutive errors | Human | 2026-03-28 | [IDEA] | v2.1 | OpenRouter API key + fallback mechanism |
