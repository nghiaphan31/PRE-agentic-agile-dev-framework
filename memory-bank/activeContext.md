---
# Active Context
**Last updated:** 2026-03-24
**Active mode:** code (Claude Sonnet)
**Active LLM backend:** Claude Sonnet API

## Current task
**i18n workbench/ Sub-batch C (DOC3) completed** — Translated `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` to English (2212 lines).

## Last result
### workbench/ Sub-batch C translation ✅
- `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md`: 2212 lines — all French text translated to English
- All phase names, step headings, validation criteria, notes, table headers, and prose translated
- All `.gitignore` comments translated (French `#` comments → English)
- All PowerShell script comments translated (startup script, check-prompts-sync.ps1)
- All proxy.py docstrings and inline comments translated
- All Memory Bank template content translated (activeContext, progress templates)
- All Appendix A/B/C content translated (references table, abbreviations, glossary)
- Technical identifiers kept unchanged: file paths, model names (`uadf-agent`, `qwen3`, `claude-sonnet-4-6`), hostnames (`calypso`, `pc`), port numbers, URLs, requirement IDs (REQ-xxx), decision IDs (DA-xxx), command examples, JSON keys, regex patterns
- `.roomodes` JSON `roleDefinition` values kept unchanged (already in French — canonical source)
- Gem Gemini instructions block kept unchanged (canonical source)
- BOM character removed (correct — was on line 1 of original)
- Pre-commit hook: **6 PASS | 0 FAIL | 1 WARN** (SP-007 manual — expected)
- Assembly method: 6 temp chunk files assembled via PowerShell `Get-Content | Set-Content`

## Next step(s)
- [ ] Manual verification SP-007: sync the Gem Gemini with `prompts/SP-007-gem-gemini-roo-agent.md`
- [ ] i18n remaining workbench/ documents (Sub-batch C remaining: DOC4, DOC5)

## Blockers / Open questions
- **SP-007**: Manual deployment required on https://gemini.google.com > Gems > "Roo Code Agent"
- **LLM backends**: Ollama, Gemini Proxy and Claude API are paused except Claude Sonnet API (active mode)

## Last Git commit
e98ecc8 — chore(i18n): translate workbench/DOC3 to English
---
