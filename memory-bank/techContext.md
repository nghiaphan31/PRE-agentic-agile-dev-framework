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

### Mode 3: Direct Cloud Claude Sonnet (Paid and Fully Automatic)
- **API Provider**: Anthropic
- **Model**: `claude-sonnet-4-6`
- **Roo Code profile name**: `claude_api`
- **Status**: `[~] Deferred to Phase 10`
- **API Key**: [stored in VS Code SecretStorage — never write here]
- **Prerequisites**: Internet connection + Anthropic credit available
