# Ideas Backlog

**Last triage:** 2026-03-30
**Next triage:** At v2.4 release planning

## How to Use

- Add new ideas immediately when they arise — never inject them directly into canonical docs.
- Create a corresponding `IDEA-NNN.md` file with full details.
- Status is updated at triage sessions (before each release starts and after each release is tagged).
- Per RULE 11: The Orchestrator Agent handles intake, classification, and sync detection.

## Status Legend

| Status | Meaning |
|--------|---------|
| `[IDEA]` | Captured, not yet evaluated |
| `[REFINING]` | Business requirements being formalized |
| `[REFINED]` | Requirements complete, awaiting triage |
| `[ACCEPTED]` | Approved for a specific release |
| `[IMPLEMENTING]` | Feature branch active development |
| `[IMPLEMENTED]` | Built, tested, in a released version |
| `[DEFERRED]` | Good idea, but not this release |
| `[REJECTED]` | Will never be implemented (reason documented) |
| `[SUPERSEDED]` | Replaced by a better idea |

## Type Legend

| Type | Meaning |
|------|---------|
| `feature` | New product feature |
| `fix` | Bug fix |
| `dev-tooling` | Developer tooling improvement |
| `governance` | Process/workflow improvement |
| `refactor` | Code restructuring |

## Tier Legend (per ADR-010)

| Tier | Description |
|------|-------------|
| `Minor` | Bug fixes, small improvements, low-risk changes |
| `Medium` | New features, product improvements |
| `Major` | Significant architectural changes |

---

## Backlog

| ID | Title | Source | Captured | Status | Type | Tier | Target Release | Disposition |
|----|-------|--------|----------|--------|------|------|----------------|-------------|
| [IDEA-001](IDEA-001-hot-cold-memory.md) | Hot/Cold memory architecture | Batch reviews 1+2 | 2026-03-28 | [IMPLEMENTED] | feature | Minor | v2.0 | PHASE-A |
| [IDEA-002](IDEA-002-calypso-orchestration.md) | Calypso orchestration scripts (Phase 2-4 pipeline) | Batch reviews 1+2 | 2026-03-28 | [IMPLEMENTED] | feature | Medium | v2.0 | PHASE-C |
| [IDEA-003](IDEA-003-release-governance.md) | Release governance model | Human 2026-03-28 | 2026-03-28 | [IMPLEMENTED] | governance | Minor | v2.0 | PHASE-0 |
| IDEA-004 | Gherkin linter integration | Batch review 1 | 2026-03-28 | [DEFERRED] | dev-tooling | Medium | v3.0 | Too complex for v2.0 scope |
| IDEA-005 | Multi-developer collaboration | Batch review 2 | 2026-03-28 | [DEFERRED] | feature | Major | v3.0 | Single-developer workbench by design |
| IDEA-006 | Template enrichment | Batch review 2 | 2026-03-28 | [IMPLEMENTED] | governance | Minor | v2.0 | PHASE-B |
| IDEA-007 | Global Brain / Librarian Agent | Batch review 2 | 2026-03-28 | [IMPLEMENTED] | feature | Medium | v2.0 | PHASE-D |
| [IDEA-008](IDEA-008-openrouter-minimax-default.md) | OpenRouter MinMax M2.7 as default LLM | Human | 2026-03-28 | [IMPLEMENTED] | dev-tooling | Minor | v2.1 | Merged |
| [IDEA-009](IDEA-009-batch-api-toolkit.md) | Generic Anthropic Batch API Toolkit | Batch audit lessons | 2026-03-29 | [IMPLEMENTED] | dev-tooling | Minor | v2.3 | scripts/batch/ toolkit |
| [IDEA-011](IDEA-011-fix-sp002-coherence.md) | Fix SP-002/.clinerules Coherence | Human (SP-002 recurring FAIL) | 2026-03-29 | [IMPLEMENTED] | fix | Minor | v2.3 | Persistent encoding corruption fixed |
| [IDEA-012A](IDEA-012A-phases-implementation-idea-to-release.md) | Ideation-to-Release PHASE-A Foundation | Architect mode | 2026-03-30 | [IMPLEMENTED] | governance | Minor | v2.4 | TECH-SUGGESTIONS-BACKLOG, RULE 11-14 |
| [IDEA-012B](IDEA-012B-phases-implementation-idea-to-release.md) | Ideation-to-Release PHASE-B Core Logic | Architect mode | 2026-03-30 | [IMPLEMENTED] | governance | Medium | v2.4 | SyncDetector, RefinementWorkflow |
| [IDEA-012C](IDEA-012C-phases-implementation-idea-to-release.md) | Ideation-to-Release PHASE-C Full Features | Architect mode | 2026-03-30 | [ACCEPTED] | governance | Medium | v2.5 | Full pipeline, BranchTracker, DOC-3 auto-gen |

---

## Archive (Historical)

### v2.3 Scope (Frozen)

| ID | Title | Final Status |
|----|-------|--------------|
| IDEA-009 | Generic Anthropic Batch API Toolkit | [IMPLEMENTED] |
| IDEA-011 | SP-002 Coherence Fix | [IMPLEMENTED] |

### v2.2 Scope (Frozen)

| ID | Title | Final Status |
|----|-------|--------------|
| IDEA-008 | OpenRouter MinMax default | [IMPLEMENTED] |

### v2.0 Scope (Frozen)

| ID | Title | Final Status |
|----|-------|--------------|
| IDEA-001 | Hot/Cold memory architecture | [IMPLEMENTED] |
| IDEA-002 | Calypso orchestration | [IMPLEMENTED] |
| IDEA-003 | Release governance model | [IMPLEMENTED] |
| IDEA-006 | Template enrichment | [IMPLEMENTED] |
| IDEA-007 | Global Brain / Librarian Agent | [IMPLEMENTED] |
