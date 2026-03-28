---
# Active Context

**Last updated:** 2026-03-28T22:00:00Z
**Active mode:** Code
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `develop` (renamed from `release/v2.3` per ADR-006)
- Base: `master` at v2.2.0 (`f0826b0`)
- `master`: at v2.2.0, frozen
- `origin/master`: at v2.1.0 — needs push (v2.2.0 pending)
- `origin/develop`: does not exist yet — needs push

## Current task
ADR-006 Phase 1 implementation — branch renamed, RULE 10 updated in 3 files

## Last result
- `release/v2.3` renamed to `develop` (ADR-006)
- RULE 10 updated in `.clinerules`, `template/.clinerules`, `prompts/SP-002-clinerules-global.md`
- ADR-006 appended to `memory-bank/hot-context/decisionLog.md`

## Next step(s)
- [ ] Git commit all ADR-006 changes
- [ ] `git push origin develop`
- [ ] `git push origin master` + `git push origin v2.2.0`
- [ ] Next: triage IDEAS-BACKLOG for v2.3 scope

## Blockers / Open questions
- `origin/master` not yet pushed with v2.2.0 tag
- `origin/develop` not yet created

## Last Git commit
`f0826b0` docs(release): add v2.2 canonical docs
