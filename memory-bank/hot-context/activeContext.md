# Active Context

**Last updated:** 2026-04-09

**Active mode:** developer

**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)

LLM Backend: minmax (default via OpenRouter)

Consecutive Errors: 0

Fallback State: Not triggered

## Current task

Fix P0 blockers for v2.15 release — completed all 4 QA blockers.

## Last result

All P0 blockers fixed (2026-04-09):
1. P0-1: DOC-4-CURRENT.md updated to point to v2.13
2. P0-2: ADR-024 documented in decisionLog.md (v2.11 cumulative docs gap = historical issue)
3. P0-3: template/.clinerules RULE 10/12 synced with ADR-006-AMEND-001
4. P0-4: Created docs/releases/v2.15/ with DOC-3, DOC-5, EXECUTION-TRACKER
5. DOC-3-CURRENT.md and DOC-5-CURRENT.md updated to v2.15
6. SP-002 rebuilt via rebuild_sp002.py — verified match
7. Git commit: `fix(qa): P0 blockers for v2.15 release` (ef97659)

## Next step(s)

- [ ] QA re-validation of v2.15 release

## Blockers / Open questions

None

## Last Git commit

ef97659 (fix(qa): P0 blockers for v2.15 release)

## Release Summary

**v2.14.0** — Latest released version (2026-04-09)
- TECH-004/005: Enhanced GitFlow branch types and timebox-first naming
- IDEA-026: Session lifecycle automation (heartbeat + conversation logging)

**v2.15** — Draft (in progress)
- IDEA-027: Orchestrator as Default Entry Point
- TECH-006: Dummy Task Mode Switch (switch_mode autonomous)
- TECH-004 (extension): ADR-006-AMEND-001 stabilization/vX.Y + main rename
- TECH-007: --no-ff Merge Enforcement via GitHub Actions

