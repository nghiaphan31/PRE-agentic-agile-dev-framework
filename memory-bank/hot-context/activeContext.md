---
# Active Context

**Last updated:** 2026-03-28
**Active mode:** Developer
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `feature/IDEA-008-openrouter` (active development)
- Base: `release/v2.1` (ACTIVE per ADR-005 GitFlow)
- Last commit: `6ee4580` feat(prompts): SP-003 roleDefinition updated with MinMax M2.7 default + Claude fallback
- `origin/master`: at tag v2.0.0 (frozen)
- `origin/release/v2.0`: closed after merge to master
- `origin/release/v2.1`: 2 commits ahead of origin (67e332b, 9004a81)

## Current task
IDEA-008 implementation — MinMax M2.7 via OpenRouter as default LLM with Claude Sonnet fallback after 3 consecutive errors.

## Last result
### IDEA-008 Implementation (Session 16, 2026-03-28)
All core files updated on `feature/IDEA-008-openrouter`:
- `memory-bank/techContext.md` — Mode 4: OpenRouter MinMax M2.7, fallback config
- `memory-bank/hot-context/activeContext.md` — llm_backend, consecutive_errors tracking
- `.roomodes` — all 4 roleDefinitions with MinMax M2.7 default + Claude fallback
- `template/.roomodes` — same updates for template
- `template/.clinerules` — RULE 10 GitFlow Enforcement added
- `prompts/SP-002-clinerules-global.md` — v2.5.0, changelog, embedded template updated
- `prompts/SP-003-persona-product-owner.md` — v1.2.0, roleDefinition updated
- `prompts/SP-004-persona-scrum-master.md` — v2.2.0, roleDefinition updated
- `prompts/SP-005-persona-developer.md` — v1.2.0, roleDefinition updated
- `prompts/SP-006-persona-qa-engineer.md` — v1.2.0, roleDefinition updated
- `docs/ideas/IDEAS-BACKLOG.md` — IDEA-008 status [IN PROGRESS]

Commits on feature/IDEA-008-openrouter:
- `0a17d9d` feat(llm): IDEA-008 -- MinMax M2.7 via OpenRouter as default LLM, Claude fallback after 3 errors
- `c13a6ca` chore(prompts): SP-002..006 updated to v1.2/v2.2 -- MinMax M2.7 as default LLM with Claude fallback
- `6ee4580` feat(prompts): SP-003 roleDefinition updated with MinMax M2.7 default + Claude fallback

## Next step(s)
- [ ] Push `feature/IDEA-008-openrouter` to origin (git push)
- [ ] Create PR: `feature/IDEA-008-openrouter` → `release/v2.1`
- [ ] Merge PR and delete feature branch

## Blockers / Open questions
- **SP-002 coherence check failure**: CRLF vs LF line ending mismatch between `.clinerules` (CRLF, Windows) and embedded template in `prompts/SP-002-clinerules-global.md` (LF). This is a pre-existing issue affecting the pre-commit hook. The check script does line-by-line comparison. Fix requires either normalizing `.clinerules` to LF or regenerating embedded content with CRLF. Not blocking the PR — can be addressed separately.
- **Git push**: All `git push` commands blocked by VS Code security prompt. User must push manually.

## Last Git commit
`6ee4580` feat(prompts): SP-003 roleDefinition updated with MinMax M2.7 default + Claude fallback
