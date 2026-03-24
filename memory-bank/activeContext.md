# Active Context

**Last updated:** 2026-03-24
**Active mode:** code (Claude Sonnet)
**Active LLM backend:** Claude Sonnet API

## Current task
**i18n Batch 2 completed** — Translation of `.roomodes` and `prompts/SP-003` through `prompts/SP-006` from French to English.

## Last result
### Batch 2 — .roomodes + SP-003..006 translated to English ✅
- `.roomodes`: all 4 `roleDefinition` values translated to English; JSON structure, slugs, fileRegex patterns, allowedCommands unchanged; `description` fields in groups translated
- `prompts/SP-003-persona-product-owner.md`: YAML front matter, section headings, deployment notes, impact section translated; version bumped 1.0.0 → 1.1.0; content block identical to `.roomodes` product-owner roleDefinition
- `prompts/SP-004-persona-scrum-master.md`: same treatment; version bumped 2.0.0 → 2.1.0; content block identical to `.roomodes` scrum-master roleDefinition
- `prompts/SP-005-persona-developer.md`: same treatment; version bumped 1.0.0 → 1.1.0; content block identical to `.roomodes` developer roleDefinition
- `prompts/SP-006-persona-qa-engineer.md`: same treatment; version bumped 1.0.0 → 1.1.0; content block identical to `.roomodes` qa-engineer roleDefinition
- Pre-commit hook ran `check-prompts-sync.ps1`: **6 PASS | 0 FAIL | 1 WARN** (SP-007 manual warning as expected)

## Next step(s)
- [ ] i18n Batch 3: translate memory-bank/*.md files
- [ ] i18n Batch 4: translate workbench/*.md and other documentation
- [ ] i18n Batch 5: translate remaining prompts (SP-001, SP-007, prompts/README.md)
- [ ] Manual verification SP-007: sync the Gem Gemini with `prompts/SP-007-gem-gemini-roo-agent.md`

## Blockers / Open questions
- **SP-007**: Manual deployment required on https://gemini.google.com > Gems > "Roo Code Agent"
- **LLM backends**: Ollama, Gemini Proxy and Claude API are paused except Claude Sonnet API (active mode)

## Last Git commit
[to be updated after commit]
