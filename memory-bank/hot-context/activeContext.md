---
# Active Context
**Last updated:** 2026-03-28
**Active mode:** Code
**Active LLM backend:** Claude Sonnet API (claude-sonnet-4-6)

## Current task
PHASE-D: Global Brain / Librarian Agent — code complete. Pending commit. PHASE-D.1 (Chroma install on Calypso) and live end-to-end test are manual steps requiring the physical machine.

## Last result
### PHASE-C: Calypso Orchestration Scripts (Session 2026-03-28)

Completed on `release/v2.0` branch (commit 2220121):
- 7 scripts + schemas + tests (28/28 PASS)
- SP-008 Synthesizer Agent + SP-009 Devil's Advocate
- FastMCP server with 5 tools

### PHASE-D: Global Brain / Librarian Agent (Session 2026-03-28)

All code-side deliverables complete (pending commit):

- **`src/calypso/librarian_agent.py`** — full implementation:
  - `index_cold_archive()`: chunks files, generates Ollama embeddings, upserts to Chroma
  - `query_memory()`: embeds query, queries Chroma, returns top-K chunks with scores
  - `get_status()`: checks Chroma connectivity
  - CLI: `--index`, `--query`, `--status`, `--files`, `--top-k`
- **`src/calypso/fastmcp_server.py`** — `memory_query()` tool updated:
  - Tries Chroma-backed semantic search via `librarian_agent.query_memory()`
  - Falls back to keyword search if Chroma unavailable
- **`scripts/memory-archive.ps1`** — updated:
  - Step 5: triggers `librarian_agent.py --index --files <new_files>` after archival
  - Graceful fallback if Chroma not running
  - Added "Next steps" instructions
- **`prompts/SP-010-librarian-agent.md`** — Librarian Agent documentation v1.0.0
- **`prompts/README.md`** — updated with SP-010 entry
- **`requirements.txt`** — added `chromadb>=0.6.0`

**Manual steps remaining (require Calypso machine):**
- PHASE-D.1: `pip install chromadb && chroma run --host 0.0.0.0 --port 8002 --path /data/chroma`
- PHASE-D.5: Live end-to-end test: `memory-archive.ps1` → Librarian indexes → `memory:query` returns results

## Next step(s)
- [ ] PHASE-D commit and push
- [ ] PHASE-E: v2.0 release finalization
  - E.1: Freeze v2.0 canonical docs (Draft → Frozen)
  - E.2: Write DOC-4-v2.0-Operations-Guide.md
  - E.3: Write DOC-5-v2.0-Release-Notes.md
  - E.4: Update docs/DOC-N-CURRENT.md pointers
  - E.5: Run full QA pass
  - E.6: Tag v2.0.0 + push

## Blockers / Open questions
- SP-002 check script regex issue (nested code blocks) — low priority, non-blocking
- PHASE-D.1: Chroma installation on Calypso — manual step, requires SSH access
- PHASE-D.5: Live end-to-end test deferred until Chroma is running on Calypso
- fastmcp package: verify version compatibility with Roo Code MCP client before PHASE-E

## Last Git commit
2220121 feat(calypso): PHASE-C complete -- Calypso orchestration scripts
---
