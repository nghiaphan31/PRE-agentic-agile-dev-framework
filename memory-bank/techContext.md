# Tech Context

## Tech Stack
- Main language: [e.g.: Python 3.11]
- Framework: [e.g.: FastAPI 0.110]
- Database: [e.g.: SQLite / PostgreSQL]
- Tests: [e.g.: pytest]

## Essential Commands
```bash
pip install -r requirements.txt
python main.py
pytest tests/
```

## Required Environment Variables
- `[VAR_NAME]`: [Description and default value]

## Critical Dependencies and Versions
| Package | Version | Reason |
| :--- | :--- | :--- |
| [package] | [version] | [reason] |

## LLM Backend Configuration (le workbench Switcher)

### Mode 1: Local Ollama (Sovereign and Free — via Tailscale)
- **API Provider**: Ollama
- **Base URL**: `http://calypso:11434`
- **Model**: `uadf-agent`
- **Roo Code profile name**: `ollama_local`
- **Status**: `[x] Configured and tested`
- **Prerequisites**: Tailscale active on `pc` and `calypso`, Ollama running on `calypso`

### Mode 2: Gemini Chrome Proxy (Free Cloud + Copy-Paste)
- **API Provider**: OpenAI Compatible
- **Base URL**: `http://localhost:8000/v1`
- **API Key**: `sk-fake-key-uadf`
- **Model**: `gemini-manual`
- **Roo Code profile name**: `gemini_proxy`
- **Status**: `[x] Configured and tested`
- **Prerequisites**: proxy.py v2.8.0 started + Chrome open on Gem "Roo Code Agent"

### Mode 3: Direct Cloud Claude Sonnet (Paid, Fully Automatic — Fallback Only)
- **API Provider**: Anthropic
- **Model**: `claude-sonnet-4-6`
- **Roo Code profile name**: `claude_api`
- **Status**: `[~] Activated automatically after 3 consecutive MinMax errors (human approval required)`
- **API Key**: [stored in VS Code SecretStorage — never write here]
- **Prerequisites**: Internet connection + Anthropic credit available

### Mode 4: OpenRouter MinMax M2.7 (Default — Cost Efficient)
- **API Provider**: OpenRouter
- **Base URL**: `https://openrouter.ai/api/v1`
- **Model**: `minimax/minimax-m2.7`
- **Roo Code profile name**: `minimax_openrouter`
- **Status**: `[x] Default LLM backend — primary choice`
- **API Key**: `OPENROUTER_API_KEY` (in `.env`)
- **Prerequisites**: Internet connection + OpenRouter account with credits

## Fallback Configuration

| Setting | Value | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | (user-supplied) | OpenRouter API key |
| `FALLBACK_ERROR_THRESHOLD` | `3` | Consecutive errors before Claude fallback |
| `FALLBACK_BACKEND` | `claude-sonnet-4-6` | Fallback model |

**Fallback logic:**
1. MinMax M2.7 is the default (Mode 4)
2. Track consecutive API errors (rate limit, 5xx, timeout, network failures)
3. After 3 consecutive errors, prompt human: `"MinMax M2.7 failed 3 times. Switch to Claude Sonnet? [Y/N]"`
4. If human approves → switch to Claude Sonnet for remainder of session
5. If human denies → continue MinMax with warning logged
6. Error count resets to 0 on any successful API call
