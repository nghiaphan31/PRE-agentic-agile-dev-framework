---
# Active Context

**Last updated:** 2026-03-29T08:10:00Z
**Active mode:** Developer
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `feature/IDEA-009-batch-toolkit` (from `develop`)
- Canonical source: `scripts/batch/` (8 modules + 2 templates)
- Template bundle: `template/scripts/batch/` (7 modules + 2 templates)
- `develop`: commit e6a0d6b (IDEA-009 + IDEA-011 committed)
- `feature/IDEA-009-batch-toolkit`: same as develop after final commit

## Current task
IDEA-009: Generic Anthropic Batch API Toolkit — IMPLEMENTED (pending merge)
IDEA-011: SP-002 Coherence Fix — CAPTURED (pending branch)

## Last result
- IDEA-009: All 12 Python files implemented, syntax checked, CLI tested
- IDEA-011: IDEA document created, added to IDEAS-BACKLOG.md
- ADR-010: Finalized with two governance paths and three release tiers

## Next step(s)
- [x] DOC-1..DOC-5 created for v2.3 (Draft)
- [x] DOC-1..DOC-5 pointers updated to v2.3
- [ ] Merge feature/IDEA-009-batch-toolkit to develop via PR
- [ ] Create `fix/IDEA-011-sp002-coherence` branch to debug SP-002 encoding issues
- [ ] Freeze DOC-1..DOC-5 when ready for v2.3.0 tag

## Blockers / Open questions
- SP-002 coherence check FAILS on every commit (BOM, mojibake, literal \n)
- ADR-010 requires all 5 canonical docs updated for every idea (structured or ad-hoc)
- Minor release formalization: tag v2.3.1 after DOC-1..5 updates

## Governance Notes (ADR-010)
- Path 1 [STRUCTURED]: Full DOC-1→DOC-2→DOC-3→Calypso→QA→release
- Path 2 [AD-HOC]: Lightweight with mandatory release tier
  - Minor: dev-tooling, skip Calypso, lightweight docs, unit+integration tests
  - Medium: new features, partial Calypso
  - Major: architectural changes, full process
- All 5 canonical docs (DOC-1..DOC-5) non-negotiable regardless of tier
- GitFlow always enforced
- ADR mandatory for every ad-hoc idea
- **DOC-1 and DOC-2 coherency non-negotiable**: no blind spots in requirements or architecture

## Last Git commit
`6854381` docs(memory): sync decisionLog with ADR-010 DOC-1 DOC-2 coherency requirement
