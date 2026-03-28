---
doc_id: DOC-5
release: v2.0
status: Frozen
title: Release Notes
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md
---

# DOC-5 -- Release Notes (v2.0)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Release date** | 2026-03-28 |
| **Git tag** | `v2.0.0` |
| **Branch** | `release/v2.0` |
| **Previous release** | v1.0.0 (2026-03-24) |
| **Type** | MINOR — new features, no breaking changes to v1.0 workflow |

---

## What v2.0 Delivers

v2.0 introduces four major capabilities that transform the Agentic Agile Workbench from a structured development environment into an **AI-powered backlog factory with persistent semantic memory**.

### PHASE-0: Release Governance Model

**Delivered:** Universal release governance framework applicable to both the workbench itself and application projects.

- `plans/governance/PLAN-release-governance.md` — 931-line governance plan
- `docs/releases/` directory structure with versioned canonical docs (DOC-1 through DOC-5)
- `docs/DOC-N-CURRENT.md` pointer files for always-current references
- `docs/ideas/` backlog for capturing out-of-scope improvements
- `docs/conversations/` log for AI conversation outputs
- Execution tracker per release (`EXECUTION-TRACKER-vX.Y.md`)

### PHASE-A: Hot/Cold Memory Architecture

**Delivered:** Separation of active context (hot zone) from historical archive (cold zone) to prevent context window flooding on long projects.

- `memory-bank/hot-context/` — 5 files read directly by agents at session start
- `memory-bank/archive-cold/` — historical data accessed only via MCP (RULE 9)
- `scripts/memory-archive.ps1` — archival script with Librarian Agent trigger
- RULE 9 (Cold Zone Firewall) added to `.clinerules`
- Template updated: `template/memory-bank/` has full Hot/Cold structure

**Key files:**
- `memory-bank/hot-context/activeContext.md`
- `memory-bank/hot-context/progress.md`
- `memory-bank/hot-context/decisionLog.md`
- `memory-bank/hot-context/systemPatterns.md`
- `memory-bank/hot-context/productContext.md`
- `memory-bank/archive-cold/sprint-logs/`
- `memory-bank/archive-cold/completed-tickets/`
- `memory-bank/archive-cold/productContext_Master.md`

### PHASE-B: Template Folder Enrichment

**Delivered:** The `template/` folder now contains everything needed to deploy a fully operational v2.0 workbench to a new project in one command.

- `template/mcp.json` — FastMCP server configuration
- `template/memory-bank/` — full Hot/Cold memory structure
- `template/docs/` — documentation structure (conversations, ideas, qa, releases)
- `deploy-workbench-to-project.ps1` updated to copy `mcp.json`, `docs/`, `memory-bank/`

### PHASE-C: Calypso Orchestration Scripts

**Delivered:** A complete AI-powered pipeline that transforms a PRD into a validated, prioritized backlog using Anthropic's Batch API and multi-agent orchestration.

**Pipeline scripts:**
- `src/calypso/orchestrator_phase2.py` — submits PRD to 4 expert agents via Batch API
- `src/calypso/check_batch_status.py` — polls batch status, retrieves expert reports
- `src/calypso/orchestrator_phase3.py` — Synthesizer Agent consolidates reports into draft backlog
- `src/calypso/orchestrator_phase4.py` — Devil's Advocate classifies items GREEN/ORANGE
- `src/calypso/triage_dashboard.py` — generates human-readable triage dashboard
- `src/calypso/apply_triage.py` — applies human decisions, updates Memory Bank

**FastMCP server:**
- `src/calypso/fastmcp_server.py` — 5 MCP tools for Roo Code integration

**JSON schemas:**
- `src/calypso/schemas/expert_report.json`
- `src/calypso/schemas/backlog_item.json`

**System prompts:**
- `prompts/SP-008-synthesizer-agent.md` — v1.0.0
- `prompts/SP-009-devils-advocate-agent.md` — v1.0.0

**Tests:** 28/28 unit tests PASS (`src/calypso/tests/`)

**Models used:**
- Phase 2 (Expert Agents): `claude-haiku-4-5` via Batch API
- Phase 3 (Synthesizer): `claude-sonnet-4-5`
- Phase 4 (Devil's Advocate): `claude-haiku-4-5`

### PHASE-D: Global Brain / Librarian Agent

**Delivered:** Semantic search over the cold archive using Chroma vector database and Ollama embeddings, accessible via MCP tool.

- `src/calypso/librarian_agent.py` — full implementation:
  - `chunk_text()`: ~2000-char overlapping chunks with boundary detection
  - `get_embedding()`: Ollama `nomic-embed-text` embeddings
  - `index_cold_archive()`: indexes all cold archive files into Chroma
  - `query_memory()`: semantic similarity search, returns top-K with scores
  - CLI: `--index`, `--query`, `--status`, `--files`, `--top-k`
- `fastmcp_server.py` updated: `memory_query` tool uses Chroma with keyword fallback
- `scripts/memory-archive.ps1` updated: triggers Librarian Agent after archival
- `prompts/SP-010-librarian-agent.md` — v1.0.0

**Infrastructure required (manual setup):**
- Chroma vector DB: `chroma run --host 0.0.0.0 --port 8002 --path /data/chroma`
- Ollama with `nomic-embed-text`: `ollama pull nomic-embed-text`

---

## New Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastmcp` | >=2.0.0 | FastMCP server framework |
| `jsonschema` | >=4.23.0 | JSON schema validation for pipeline outputs |
| `chromadb` | >=0.6.0 | Vector database client for Global Brain |

Install: `pip install -r requirements.txt`

---

## New System Prompts

| ID | File | Version | Purpose |
|----|------|---------|---------|
| SP-008 | `prompts/SP-008-synthesizer-agent.md` | 1.0.0 | Consolidates expert reports into structured backlog |
| SP-009 | `prompts/SP-009-devils-advocate-agent.md` | 1.0.0 | Challenges backlog items, GREEN/ORANGE classification |
| SP-010 | `prompts/SP-010-librarian-agent.md` | 1.0.0 | Indexes cold archive, answers semantic queries |

---

## New `.clinerules` Rules

| Rule | Description |
|------|-------------|
| RULE 7 | Large File Generation — Mandatory Chunking Protocol (>500 lines) |
| RULE 8 | Documentation Discipline — Governance Protocol |
| RULE 9 | Cold Zone Firewall — Memory Access Protocol |

---

## Known Gaps and Limitations

### PHASE-D: Chroma Not Yet Live

The Global Brain code is complete and tested, but the Chroma vector database has not yet been installed on the Calypso machine. Until Chroma is running:

- `memory_query` MCP tool falls back to keyword search (functional but less precise)
- `librarian_agent.py --index` will fail with `DISCONNECTED` error
- `memory-archive.ps1` Step 5 will log a warning and skip indexing

**Resolution:** Run `pip install chromadb && chroma run --host 0.0.0.0 --port 8002 --path /data/chroma` on the Calypso machine.

### Calypso Pipeline: No End-to-End Test

The pipeline scripts have 28/28 unit tests passing, but no live end-to-end test has been run (requires Anthropic API credits and a real PRD). The pipeline is ready for first use.

### SP-002 Check Script: Nested Code Block Warning

`scripts/check-prompts-sync.ps1` reports a warning for SP-002 due to nested ````powershell` blocks inside ````markdown` blocks. This is a false positive — the script content is correct. Non-blocking.

---

## Migration Guide from v1.0

### Step 1: Update workbench files

```powershell
$Workbench = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench"
$Project   = "path/to/your/project"
& "$Workbench\deploy-workbench-to-project.ps1" -ProjectPath $Project -Update
```

### Step 2: Migrate Memory Bank to Hot/Cold structure

```powershell
# Create Hot/Cold directories
New-Item -Path "$Project\memory-bank\hot-context" -ItemType Directory -Force
New-Item -Path "$Project\memory-bank\archive-cold\sprint-logs" -ItemType Directory -Force
New-Item -Path "$Project\memory-bank\archive-cold\completed-tickets" -ItemType Directory -Force
New-Item -Path "$Project\memory-bank\archive-cold\productContext_Master.md" -ItemType File

# Move hot-context files
Move-Item "$Project\memory-bank\activeContext.md"  "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\progress.md"       "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\decisionLog.md"    "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\systemPatterns.md" "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\productContext.md" "$Project\memory-bank\hot-context\"

# projectBrief.md and techContext.md stay at memory-bank/ root
```

### Step 3: Update `.clinerules`

The new `.clinerules` from the workbench includes RULE 7, RULE 8, and RULE 9. The deployment script copies it automatically. Verify RULE 1 now reads from `memory-bank/hot-context/`.

### Step 4: Install new Python dependencies

```powershell
cd $Project
venv\Scripts\activate
pip install -r requirements.txt
# New: fastmcp>=2.0.0, jsonschema>=4.23.0, chromadb>=0.6.0
```

### Step 5: Configure MCP server

Edit `mcp.json` at the project root to verify the path to `fastmcp_server.py` is correct for your project structure.

### Step 6: Commit the migration

```powershell
git add .
git commit -m "chore(workbench): migrate to workbench v2.0 -- Hot/Cold memory + Calypso"
```

---

## What's Next (v3.0 Preview)

The following capabilities are captured in `docs/ideas/IDEAS-BACKLOG.md` for v3.0 consideration:

| Idea | Description |
|------|-------------|
| **Live Chroma integration** | End-to-end test of Global Brain with real sprint data |
| **DOC6 revision** | Fix P0 issues identified in Batch API review (conversational framing, PRD naming, glossary) |
| **Calypso live test** | First real PRD → backlog run with Anthropic API |
| **Multi-project Global Brain** | Single Chroma instance shared across multiple projects |
| **Automated sprint archival** | Trigger `memory-archive.ps1` automatically at sprint close |
| **Roo Code MCP dashboard** | Visual dashboard for Calypso pipeline status in VS Code |

---

## Commit History (v2.0 Branch)

| Commit | Description |
|--------|-------------|
| `905d418` | PHASE-0: Release governance restructure (13 steps) |
| `fc211cb` | Draft v2.0 canonical docs (DOC-1..3) |
| `bd1bf7d` | PHASE-A: Hot/Cold memory restructure |
| `137e977` | PHASE-B: Template folder enrichment |
| `2220121` | PHASE-C: Calypso orchestration scripts (28/28 tests PASS) |
| `ba61920` | PHASE-D: Global Brain / Librarian Agent |
| *(this commit)* | PHASE-E: v2.0 release finalization |

---

*End of DOC-5-v2.0-Release-Notes.md*
