# Active Context

**Last updated:** 2026-04-09

**Active mode:** scrum-master

**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)

LLM Backend: minmax (default via OpenRouter)

Consecutive Errors: 0

Fallback State: Not triggered

## Current task

RELEASE.md v2.15 scope maintenance fix — completed.
- Populated "Commits Since v2.14.0" table with all 14 commits
- Populated "Features in Scope" table: IDEA-027, TECH-006, TECH-004 ext, TECH-007
- Added ADR-023 to decisionLog.md documenting the maintenance failure root cause

## Last result

RELEASE.md v2.15 scope retroactively populated (2026-04-09):
1. `memory-bank/hot-context/RELEASE.md` — 14 commits + 4 features in scope, status set to Draft
2. `memory-bank/hot-context/decisionLog.md` — ADR-023 added (maintenance failure root cause)
3. `memory-bank/hot-context/activeContext.md` — updated (this file)

## Next step(s)

- [ ] Git commit: `chore(release): populate v2.15 scope from develop — 14 commits, IDEA-027, TECH-004/006/007`
- [ ] (Carry-forward) Switch to Developer mode to update `.clinerules` RULE 10 (all `develop-vX.Y` → `stabilization/vX.Y`, remove `release/vX.Y.Z` row, update 10.5/10.6)
- [ ] Developer: update `plans/governance/ADR-006-develop-main-branching.md` (renames throughout)
- [ ] Developer: run `python scripts/rebuild_sp002.py`

## Blockers / Open questions

None

## Last Git commit

0c366ec (docs(memory): ADR-022 human directive override for TECH-007)

## Release Summary

**v2.14.0** — Latest released version (2026-04-09)
- TECH-004/005: Enhanced GitFlow branch types and timebox-first naming
- IDEA-026: Session lifecycle automation (heartbeat + conversation logging)

**v2.15** — Draft (in progress)
- IDEA-027: Orchestrator as Default Entry Point
- TECH-006: Dummy Task Mode Switch (switch_mode autonomous)
- TECH-004 (extension): ADR-006-AMEND-001 stabilization/vX.Y + main rename
- TECH-007: --no-ff Merge Enforcement via GitHub Actions

