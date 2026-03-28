# IDEA-008: OpenRouter MinMax M2.7 as Default LLM with Claude Fallback

**Captured:** 2026-03-28  
**Source:** Human  
**Status:** [IDEA]  
**Target Release:** v2.1  

---

## Description

Replace Anthropic Claude Sonnet 4.6 as the default LLM backend with MinMax M2.7 via OpenRouter. Add an intelligent fallback mechanism that switches to Claude after **N consecutive errors** with MinMax, subject to **human approval**.

### Core Requirements

1. **OpenRouter + MinMax M2.7 as default**
   - Add `OPENROUTER_API_KEY` to `.env`
   - Update `.roomodes` and all relevant system prompts (SP-001..010) to reference MinMax M2.7 as the default model
   - Update `Modelfile` to target MinMax M2.7 via OpenRouter
   - Remove or deprioritize `claude-sonnet-4-6` as default

2. **Fallback to Claude on consecutive errors**
   - Track consecutive API errors (rate limit, 5xx, timeout, etc.) per session
   - After **3 consecutive failures** with MinMax, prompt human for approval before switching
   - If human approves → switch to `claude-sonnet-4-6` for remainder of session
   - If human denies → continue with MinMax (with warning logged)
   - Error count resets on successful API call

3. **Human approval gate**
   - Modal/terminal prompt: `"MinMax M2.7 failed 3 times. Switch to Claude Sonnet? [Y/N]"`
   - Human decision logged in activeContext.md

---

## Motivation

- Reduce LLM API costs (MinMax M2.7 via OpenRouter is significantly cheaper than Claude Sonnet)
- You already have MinMax M2.7 running as your current session model — aligning the default makes sense
- Fallback preserves reliability for mission-critical operations

---

## Affected Documents

| Document | Change Required |
|---|---|
| `Modelfile` | Base model → MinMax M2.7 via OpenRouter |
| `.roomodes` | Default LLM backend in all persona roleDefinitions |
| `SP-001..010` | Update model references to MinMax M2.7 |
| `memory-bank/techContext.md` | Document OpenRouter + fallback config |
| `memory-bank/hot-context/activeContext.md` | Track current backend + error count |
| `template/Modelfile` | Update template to match |
| `template/.roomodes` | Update template to match |

---

## Technical Approach

- **proxy.py** — extend to support OpenRouter as a provider alongside Gemini Chrome; add error-counting + fallback logic
- **Environment** — add `OPENROUTER_API_KEY`, `FALLBACK_ERROR_THRESHOLD=3`
- **Fallback state** — stored in `memory-bank/hot-context/activeContext.md` as `llm_backend: minmax | claude` and `consecutive_errors: N`

---

## Open Questions

- Should the fallback switch be per-session or per-operation?
- Should we log fallback events to cold archive for billing analysis?
- Do we keep Claude as fallback or also consider Ollama local models?
