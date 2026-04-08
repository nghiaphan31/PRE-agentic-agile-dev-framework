# Active Context

**Last updated:** 2026-04-08

**Active mode:** developer

**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)

LLM Backend: minmax (default via OpenRouter)

Consecutive Errors: 0

Fallback State: Not triggered

## Current task

Fix 2 critical QA blockers for v2.13 release

## Last result

Fixed both QA blockers:
1. Renamed .githooks/pre-receive-detect → .githooks/pre-receive-merged-features (matches docs)
2. Removed `if len(parents) < 2: continue` filter in detect-merged-features.py line 164-166 (R-006 compliance)
Committed as 1d18282

## Next step(s)

- [ ] QA re-validation
- [ ] Tag v2.13.0 release

## Blockers / Open questions

None

## Last Git commit

1d18282 (fix(blocker): resolve v2.13 QA blockers for release tag)

## Release Summary

**v2.12.0** — Latest released version (2026-04-08)
- Governance Enhancement Release

**v2.13** — Draft (blocked by QA validation)

