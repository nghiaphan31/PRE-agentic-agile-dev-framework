---
# Active Context
**Last updated:** 2026-03-28
**Active mode:** Code
**Active LLM backend:** Claude Sonnet API (claude-sonnet-4-6)

## Current task
PHASE-C: Calypso orchestration scripts — complete. 28/28 unit tests PASS. Ready to commit and proceed to PHASE-D.

## Last result
### PHASE-B: Template Folder Enrichment (Session 2026-03-28)

Completed on `release/v2.0` branch (commit 137e977):

- `template/memory-bank/hot-context/` — 5 blank stubs
- `template/memory-bank/archive-cold/` — sprint-logs/, completed-tickets/, productContext_Master.md
- `template/mcp.json` — Calypso FastMCP server config template
- `deploy-workbench-to-project.ps1` — updated with mcp.json + docs + memory-bank in copy lists

### PHASE-C: Calypso Orchestration Scripts (Session 2026-03-28)

All deliverables created (pending commit):

- **`src/calypso/__init__.py`** — package init
- **`src/calypso/orchestrator_phase2.py`** — submits PRD to Anthropic Batch API (4 expert agents)
- **`src/calypso/check_batch_status.py`** — polls batch status, retrieves expert reports
- **`src/calypso/orchestrator_phase3.py`** — Synthesizer Agent (SP-008), produces draft_backlog.json
- **`src/calypso/orchestrator_phase4.py`** — Devil's Advocate (SP-009), GREEN/ORANGE classification
- **`src/calypso/triage_dashboard.py`** — generates human triage dashboard with checkboxes
- **`src/calypso/apply_triage.py`** — applies human decisions to systemPatterns.md + productContext.md
- **`src/calypso/fastmcp_server.py`** — FastMCP server (5 tools: launch_factory, check_batch_status, retrieve_backlog, memory_query, memory_archive)
- **`src/calypso/librarian_agent.py`** — PHASE-D stub
- **`src/calypso/schemas/expert_report.json`** — JSON schema for expert reports
- **`src/calypso/schemas/backlog_item.json`** — JSON schema for backlog items
- **`src/calypso/tests/test_orchestrator.py`** — 15 unit tests (all PASS)
- **`src/calypso/tests/test_triage.py`** — 13 unit tests (all PASS)
- **`src/calypso/tests/fixtures/`** — sample_prd.md, sample_expert_report.json, sample_backlog.json
- **`prompts/SP-008-synthesizer-agent.md`** — Synthesizer Agent system prompt v1.0.0
- **`prompts/SP-009-devils-advocate-agent.md`** — Devil's Advocate system prompt v1.0.0
- **`prompts/README.md`** — updated with SP-008 and SP-009 entries
- **`requirements.txt`** — added fastmcp>=2.0.0 and jsonschema>=4.23.0

**Test results:** 28/28 PASS (0 failures, 0 errors)

## Next step(s)
- [ ] PHASE-C commit and push
- [ ] PHASE-D: Global Brain / Librarian Agent
  - D.1: Install Chroma on Calypso (manual step)
  - D.2: Implement librarian_agent.py (index cold archive)
  - D.3: Wire memory_query() in fastmcp_server.py to Chroma
  - D.4: Write SP-010 (Librarian Agent)
  - D.5: End-to-end test: memory:query returns relevant results
  - D.6: Commit and push
- [ ] PHASE-E: v2.0 release finalization (DOC-4, DOC-5, tag v2.0.0)

## Blockers / Open questions
- SP-002 check script regex issue (nested code blocks) — low priority, non-blocking
- Chroma vector DB installation on Calypso required for PHASE-D (manual step — human must install)
- fastmcp package version: using >=2.0.0 (verify compatibility with Roo Code MCP client)
- PHASE-C.10 (end-to-end test with real API) deferred — requires Anthropic API call + batch wait

## Last Git commit
137e977 feat(template): PHASE-B complete -- template folder enrichment
---
