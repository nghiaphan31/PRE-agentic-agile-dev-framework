---
doc_id: DOC-4
release: v2.0
status: Frozen
title: Operations Guide
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v1.0/DOC-4-v1.0-Operations-Guide.md
---

# DOC-4 -- Operations Guide (v2.0)

> **Status: FROZEN** -- This document is read-only. Do not modify.
> See DOC-8.1 (governance rules) for the Cold Zone Firewall protocol.

---

## Table of Contents

1. [Overview: What v2.0 Adds](#1-overview-what-v20-adds)
2. [Workbench Deployment to a New Project](#2-workbench-deployment-to-a-new-project)
3. [Calypso Pipeline: PRD â†’ Backlog](#3-calypso-pipeline-prd--backlog)
   - 3.1 Prerequisites
   - 3.2 Phase 2 â€” Expert Analysis (Batch API)
   - 3.3 Phase 3 â€” Synthesis (Synthesizer Agent)
   - 3.4 Phase 4 â€” Validation (Devil's Advocate)
   - 3.5 Triage Dashboard
   - 3.6 Apply Triage Decisions
4. [FastMCP Server: Calypso Tools for Roo Code](#4-fastmcp-server-calypso-tools-for-roo-code)
   - 4.1 Starting the Server
   - 4.2 Available Tools
   - 4.3 Configuring Roo Code
5. [Memory Operations: Archive and Query](#5-memory-operations-archive-and-query)
   - 5.1 memory:archive (memory-archive.ps1)
   - 5.2 memory:query (Librarian Agent)
   - 5.3 Global Brain Setup (Chroma + Ollama)
6. [Hot/Cold Memory Architecture](#6-hotcold-memory-architecture)
   - 6.1 Hot Zone (Read Directly)
   - 6.2 Cold Zone (MCP Only)
   - 6.3 Archival Workflow
7. [Troubleshooting Guide](#7-troubleshooting-guide)
8. [Reference: File Locations](#8-reference-file-locations)
9. [Appendix: Deployment Checklist](#9-appendix-deployment-checklist)

---

## 1. Overview: What v2.0 Adds

v2.0 of the Agentic Agile Workbench introduces four major operational capabilities on top of the v1.0 foundation:

| Capability | What It Does | Key Files |
|-----------|-------------|-----------|
| **Hot/Cold Memory** | Separates active context (hot) from historical archive (cold) | `memory-bank/hot-context/`, `memory-bank/archive-cold/` |
| **Calypso Pipeline** | Transforms a PRD into a validated backlog using AI agents | `src/calypso/orchestrator_phase*.py` |
| **FastMCP Server** | Exposes Calypso tools to Roo Code via MCP protocol | `src/calypso/fastmcp_server.py` |
| **Global Brain** | Semantic search over the cold archive via Chroma + Ollama | `src/calypso/librarian_agent.py` |

**v1.0 operations (deployment, Agile process, LLM modes) remain unchanged.** See DOC-4-v1.0 for those procedures. This document covers only the v2.0 additions.

---

## 2. Workbench Deployment to a New Project

### 2.1 What Changed in v2.0

The `deploy-workbench-to-project.ps1` script now copies additional files:

| Added in v2.0 | Description |
|--------------|-------------|
| `mcp.json` | FastMCP server configuration for Roo Code |
| `docs/` | Documentation structure (conversations, ideas, qa, releases) |
| `memory-bank/` | Full Hot/Cold memory structure (hot-context/ + archive-cold/) |

The Memory Bank initialization block now creates only `projectBrief.md` and `techContext.md` at the root (the rest of the structure is copied from `template/memory-bank/`).

### 2.2 Deployment Command

```powershell
# From the workbench root
$Workbench = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench"
$Project   = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-new-project"

& "$Workbench\deploy-workbench-to-project.ps1" -ProjectPath $Project
```

### 2.3 Post-Deployment: Fill in the Memory Bank

After deployment, the only mandatory manual step is filling in `memory-bank/projectBrief.md` and `memory-bank/techContext.md`. The hot-context files are pre-populated with blank templates.

Then open `memory-bank/hot-context/productContext.md` and define the first sprint backlog.

### 2.4 Post-Deployment: Configure the FastMCP Server

1. Edit `mcp.json` at the project root â€” verify the `args` path points to `src/calypso/fastmcp_server.py`
2. Set the `ANTHROPIC_API_KEY` environment variable (or add it to `.env`)
3. In Roo Code settings, add the MCP server entry (see Section 4.3)

### 2.5 Updating an Existing Project from v1.0

If you have a project deployed with workbench v1.0, run the deployment script with `-Update`:

```powershell
& "$Workbench\deploy-workbench-to-project.ps1" -ProjectPath $Project -Update
```

Then manually migrate the Memory Bank:

```powershell
# Create the Hot/Cold structure
New-Item -Path "$Project\memory-bank\hot-context" -ItemType Directory -Force
New-Item -Path "$Project\memory-bank\archive-cold\sprint-logs" -ItemType Directory -Force
New-Item -Path "$Project\memory-bank\archive-cold\completed-tickets" -ItemType Directory -Force

# Move existing files to hot-context
Move-Item "$Project\memory-bank\activeContext.md"  "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\progress.md"       "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\decisionLog.md"    "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\systemPatterns.md" "$Project\memory-bank\hot-context\"
Move-Item "$Project\memory-bank\productContext.md" "$Project\memory-bank\hot-context\"

# Keep projectBrief.md and techContext.md at root (they are not hot-context files)
```

> **Important:** After migration, update `.clinerules` RULE 1 to read from `memory-bank/hot-context/` instead of `memory-bank/`.

---

## 3. Calypso Pipeline: PRD â†’ Backlog

The Calypso pipeline transforms a Product Requirements Document (PRD) into a validated, prioritized backlog using a sequence of AI agents. It runs in 3 phases (2, 3, 4) plus a human triage step.

```
PRD (Markdown)
    â”‚
    â–¼ Phase 2: orchestrator_phase2.py
    â”‚   4 Expert Agents (Architecture, Security, UX, QA)
    â”‚   â†’ Anthropic Batch API (async, ~5 min)
    â”‚   â†’ batch_artifacts/expert_reports/*.json
    â”‚
    â–¼ Phase 3: orchestrator_phase3.py
    â”‚   Synthesizer Agent (SP-008)
    â”‚   â†’ Consolidates expert reports into structured backlog
    â”‚   â†’ batch_artifacts/draft_backlog.json
    â”‚
    â–¼ Phase 4: orchestrator_phase4.py
    â”‚   Devil's Advocate Agent (SP-009)
    â”‚   â†’ Challenges each backlog item
    â”‚   â†’ GREEN (auto-accept) or ORANGE (human review)
    â”‚   â†’ batch_artifacts/final_backlog.json
    â”‚
    â–¼ Triage: triage_dashboard.py
    â”‚   â†’ docs/triage_dashboard.md (checkboxes for ORANGE items)
    â”‚
    â–¼ Human Decision (edit triage_dashboard.md)
    â”‚
    â–¼ Apply: apply_triage.py
        â†’ Updates final_backlog.json with human decisions
        â†’ Appends accepted items to memory-bank/hot-context/systemPatterns.md
        â†’ Appends accepted items to memory-bank/hot-context/productContext.md
```

### 3.1 Prerequisites

Before running the pipeline:

1. **Python environment** with dependencies installed:
   ```powershell
   cd $Project
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Anthropic API key** set in environment:
   ```powershell
   $env:ANTHROPIC_API_KEY = "sk-ant-..."
   # Or add to .env file (never commit .env to Git)
   ```

3. **PRD file** ready at a known path (e.g., `docs/prd.md`)

4. **Output directory** created:
   ```powershell
   New-Item -Path "batch_artifacts\expert_reports" -ItemType Directory -Force
   ```

### 3.2 Phase 2 â€” Expert Analysis (Batch API)

Phase 2 submits the PRD to 4 expert agents in parallel via the Anthropic Batch API. This is asynchronous â€” the batch runs in the background and you poll for results.

**Submit the batch:**

```powershell
python src/calypso/orchestrator_phase2.py --prd docs/prd.md
```

Output:
```
[OK] PRD loaded: docs/prd.md (2847 chars)
[OK] Batch submitted: msgbatch_01XYZ...
[OK] Batch ID saved to: batch_artifacts/batch_id_phase2.txt
[OK] Metadata saved to: batch_artifacts/batch_metadata_phase2.json
Estimated completion: 5-15 minutes
```

**Check batch status:**

```powershell
# One-time check
python src/calypso/check_batch_status.py

# Auto-poll every 60 seconds until complete
python src/calypso/check_batch_status.py --poll
```

When complete:
```
[OK] Batch complete: 4/4 requests succeeded
[OK] Expert reports saved:
     batch_artifacts/expert_reports/architecture_expert.json
     batch_artifacts/expert_reports/security_expert.json
     batch_artifacts/expert_reports/ux_expert.json
     batch_artifacts/expert_reports/qa_expert.json
```

**Expert report format** (validated against `src/calypso/schemas/expert_report.json`):
```json
{
  "expert_id": "architecture_expert",
  "expert_role": "Software Architect",
  "findings": [
    {
      "severity": "HIGH",
      "category": "scalability",
      "description": "...",
      "recommendation": "..."
    }
  ]
}
```

### 3.3 Phase 3 â€” Synthesis (Synthesizer Agent)

Phase 3 loads all expert reports and the PRD, then calls the Synthesizer Agent (SP-008) synchronously to produce a structured draft backlog.

```powershell
python src/calypso/orchestrator_phase3.py --prd docs/prd.md
```

Output:
```
[OK] PRD loaded: docs/prd.md
[OK] Expert reports loaded: 4 reports
[OK] Calling Synthesizer Agent (claude-sonnet-4-5)...
[OK] Draft backlog saved: batch_artifacts/draft_backlog.json
     12 backlog items generated
```

**Draft backlog format** (validated against `src/calypso/schemas/backlog_item.json`):
```json
[
  {
    "id": "BL-001",
    "title": "User authentication system",
    "description": "...",
    "acceptance_criteria": ["...", "..."],
    "source_experts": ["architecture_expert", "security_expert"],
    "priority": "HIGH",
    "phase": "Phase 1"
  }
]
```

### 3.4 Phase 4 â€” Validation (Devil's Advocate)

Phase 4 runs the Devil's Advocate Agent (SP-009) on each backlog item. Items that survive challenge are marked GREEN; items requiring human review are marked ORANGE.

```powershell
python src/calypso/orchestrator_phase4.py
```

Output:
```
[OK] Draft backlog loaded: 12 items
Processing BL-001... GREEN (passed challenge)
Processing BL-002... ORANGE (challenge: scope too broad)
Processing BL-003... GREEN (passed challenge)
...
[OK] Final backlog saved: batch_artifacts/final_backlog.json
     GREEN: 9 items | ORANGE: 3 items
```

**Configuration** (edit at top of `orchestrator_phase4.py`):
```python
MAX_ATTEMPTS = 2      # Number of challenge rounds (default: 2)
MODEL = "claude-haiku-4-5"  # Model for Devil's Advocate
```

### 3.5 Triage Dashboard

Generate the human-readable triage dashboard:

```powershell
python src/calypso/triage_dashboard.py
```

Output: `docs/triage_dashboard.md`

The dashboard contains:
- **Summary table**: all items with GREEN/ORANGE status
- **ORANGE items section**: each item with `- [ ] ACCEPT` and `- [ ] REJECT` checkboxes
- **GREEN items section**: auto-accepted items (no action needed)

**Human action required:** Open `docs/triage_dashboard.md` and for each ORANGE item, check either `- [x] ACCEPT` or `- [x] REJECT`.

### 3.6 Apply Triage Decisions

After editing the dashboard, apply the decisions:

```powershell
# Dry run first (preview changes without writing)
python src/calypso/apply_triage.py --dry-run

# Apply for real
python src/calypso/apply_triage.py
```

Output:
```
[OK] Triage dashboard loaded
[OK] BL-002: ACCEPT (human decision)
[OK] BL-007: REJECT (human decision)
[OK] final_backlog.json updated
[OK] Accepted items appended to memory-bank/hot-context/systemPatterns.md
[OK] Accepted items appended to memory-bank/hot-context/productContext.md
```

The accepted backlog items are now in the Memory Bank, ready for sprint planning.

---

## 4. FastMCP Server: Calypso Tools for Roo Code

The FastMCP server exposes Calypso pipeline operations as MCP tools that Roo Code can call directly during a session.

### 4.1 Starting the Server

**Stdio mode** (default â€” Roo Code manages the process):
```powershell
# Roo Code starts this automatically via mcp.json
python src/calypso/fastmcp_server.py
```

**SSE mode** (for debugging or external clients):
```powershell
python src/calypso/fastmcp_server.py --transport sse --port 8001
```

**Required environment variables:**
```
ANTHROPIC_API_KEY=sk-ant-...
CHROMA_HOST=localhost        # Optional (default: localhost)
CHROMA_PORT=8002             # Optional (default: 8002)
```

### 4.2 Available Tools

| Tool | Description | Parameters |
|------|-------------|-----------|
| `launch_factory` | Runs Phase 2 (submit batch) | `prd_path: str` |
| `check_batch_status` | Checks batch status + retrieves results | `batch_id: str` |
| `retrieve_backlog` | Returns the current backlog JSON | `phase: str = "final"` |
| `memory_query` | Semantic search over cold archive | `semantic_query: str`, `top_k: int = 5` |
| `memory_archive` | Triggers memory archival script | *(no parameters)* |

**Example usage in Roo Code chat:**

```
Use the launch_factory tool with prd_path="docs/prd.md" to start the expert analysis.
```

```
Use memory_query with semantic_query="authentication decisions sprint 3" to find relevant context.
```

### 4.3 Configuring Roo Code

The `mcp.json` file at the project root configures the MCP server for Roo Code:

```json
{
  "mcpServers": {
    "calypso": {
      "command": "python",
      "args": ["src/calypso/fastmcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "CHROMA_HOST": "localhost",
        "CHROMA_PORT": "8002"
      }
    }
  }
}
```

In VS Code:
1. Open Roo Code settings (`Ctrl+Shift+P` â†’ "Roo Code: Open Settings")
2. Navigate to "MCP Servers"
3. The `mcp.json` at the project root is loaded automatically

> **Note:** `${ANTHROPIC_API_KEY}` is resolved from the environment at server startup. Never hardcode the key in `mcp.json`.


---

## 5. Memory Operations: Archive and Query

### 5.1 memory:archive (memory-archive.ps1)

The `memory:archive` operation moves completed sprint artifacts from the hot zone to the cold archive and triggers the Librarian Agent to index them.

**When to run:** At the end of each sprint, after the retrospective is complete.

**Run manually:**
```powershell
.\scripts\memory-archive.ps1
```

**Or via Roo Code MCP tool:**
```
Use the memory_archive tool to archive the current sprint artifacts.
```

**What the script does:**

1. Reads `memory-bank/hot-context/productContext.md` to identify completed sprint items
2. Copies completed sprint logs to `memory-bank/archive-cold/sprint-logs/`
3. Copies completed ticket files to `memory-bank/archive-cold/completed-tickets/`
4. Updates `memory-bank/archive-cold/productContext_Master.md` with the archived items
5. **[v2.0 NEW]** Triggers `librarian_agent.py --index --files <new_files>` to index the new archive files into Chroma

**Step 5 output (if Chroma is running):**
```
[OK] Librarian Agent: indexed 3 new files into global_brain collection
```

**Step 5 output (if Chroma is NOT running):**
```
[WARN] Chroma not available -- skipping indexing (run manually later)
       To index manually: python src/calypso/librarian_agent.py --index
```

### 5.2 memory:query (Librarian Agent)

The `memory:query` operation performs semantic search over the cold archive using Chroma vector embeddings.

**Via Roo Code MCP tool (recommended):**
```
Use memory_query with semantic_query="authentication decisions from sprint 2" and top_k=5
```

**Via CLI:**
```powershell
python src/calypso/librarian_agent.py --query "authentication decisions from sprint 2" --top-k 5
```

**Output format:**
```
Query: "authentication decisions from sprint 2"
Top 5 results:

[1] Score: 0.923 | sprint-002-retrospective.md (sprint_log)
    "...decided to use JWT tokens for stateless authentication..."

[2] Score: 0.887 | BL-003-auth-system.md (ticket)
    "...acceptance criteria: token expiry must be configurable..."

[3] Score: 0.841 | productContext_Master.md (product_context)
    "...Sprint 2 delivered: US-007 (JWT auth), US-008 (refresh tokens)..."
```

**Fallback behavior (if Chroma unavailable):**
The MCP tool falls back to keyword search over `memory-bank/archive-cold/` files. Results are less precise but still useful.

### 5.3 Global Brain Setup (Chroma + Ollama)

The Global Brain requires two services running on the Calypso machine (or locally):

#### 5.3.1 Chroma Vector Database

**Install:**
```bash
pip install chromadb
```

**Start (persistent mode):**
```bash
chroma run --host 0.0.0.0 --port 8002 --path /data/chroma
```

**Verify:**
```bash
curl http://localhost:8002/api/v1/heartbeat
# Expected: {"nanosecond heartbeat": 1234567890}
```

**Check status via CLI:**
```powershell
python src/calypso/librarian_agent.py --status
```

Output:
```
Chroma status: CONNECTED
Host: localhost:8002
Collection: global_brain
Documents indexed: 47
```

#### 5.3.2 Ollama Embedding Model

The Librarian Agent uses `nomic-embed-text` for generating embeddings.

**Install the model:**
```bash
ollama pull nomic-embed-text
```

**Verify:**
```bash
curl http://localhost:11434/api/embeddings \
  -d '{"model": "nomic-embed-text", "prompt": "test"}'
# Expected: {"embedding": [0.123, -0.456, ...]}
```

#### 5.3.3 Initial Indexing

After setting up Chroma and Ollama, index the existing cold archive:

```powershell
python src/calypso/librarian_agent.py --index
```

Output:
```
Indexing cold archive: memory-bank/archive-cold/
  sprint-logs/sprint-001-retro.md ... [OK] 3 chunks
  sprint-logs/sprint-002-retro.md ... [OK] 4 chunks
  completed-tickets/BL-001.md     ... [OK] 2 chunks
  productContext_Master.md         ... [OK] 8 chunks
[OK] Total: 17 chunks indexed into global_brain collection
```

#### 5.3.4 Librarian Agent CLI Reference

```
python src/calypso/librarian_agent.py [OPTIONS]

Options:
  --index              Index all files in archive-cold/
  --query TEXT         Semantic query string
  --status             Check Chroma connectivity
  --files FILE [...]   Index specific files only
  --top-k INT          Number of results to return (default: 5)
  --quiet              Suppress progress output

Examples:
  python src/calypso/librarian_agent.py --status
  python src/calypso/librarian_agent.py --index
  python src/calypso/librarian_agent.py --query "sprint 3 decisions" --top-k 3
  python src/calypso/librarian_agent.py --files archive-cold/sprint-logs/sprint-003.md
```

---

## 6. Hot/Cold Memory Architecture

### 6.1 Hot Zone (Read Directly)

Files in `memory-bank/hot-context/` are read directly by agents at session start (RULE 1).

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `activeContext.md` | Current task, last result, next steps | Every session |
| `progress.md` | Feature checklist, sprint status | Every sprint end |
| `decisionLog.md` | Architecture Decision Records (ADRs) | After each ADR |
| `systemPatterns.md` | Current architecture patterns | After architecture change |
| `productContext.md` | Active sprint backlog, user stories | Every sprint |

**RULE 1 sequence (mandatory at session start):**
```
CHECK â†’ CREATE â†’ READ â†’ ACT
1. Does memory-bank/hot-context/activeContext.md exist?
2. If NO â†’ create from template
3. READ activeContext.md then progress.md
4. ACT on the user's request
```

### 6.2 Cold Zone (MCP Only)

Files in `memory-bank/archive-cold/` MUST NOT be read directly by agents.

**Access protocol:** Use `memory:query` MCP tool only.

```
# CORRECT: via MCP tool
Use memory_query with semantic_query="sprint 1 authentication decisions"

# WRONG: direct file read (violates RULE 9)
read_file("memory-bank/archive-cold/sprint-logs/sprint-001.md")
```

**Why this rule exists:**
- Direct reading floods the context window with stale historical data
- Causes "Lost in the Middle" errors on large projects
- The Librarian Agent provides targeted, relevant excerpts instead

**Cold archive structure:**
```
memory-bank/archive-cold/
â”œâ”€â”€ sprint-logs/           # Retrospectives, sprint reviews
â”‚   â”œâ”€â”€ sprint-001-retro.md
â”‚   â””â”€â”€ sprint-002-retro.md
â”œâ”€â”€ completed-tickets/     # Closed backlog items
â”‚   â”œâ”€â”€ BL-001-auth.md
â”‚   â””â”€â”€ BL-002-api.md
â””â”€â”€ productContext_Master.md  # Cumulative product history
```

### 6.3 Archival Workflow

The recommended archival workflow at sprint end:

```
1. Scrum Master Mode:
   "Run the retrospective for sprint [NNN] and update memory-bank/hot-context/progress.md"

2. After retrospective is committed:
   Run: .\scripts\memory-archive.ps1
   (or: Use the memory_archive MCP tool)

3. Verify archival:
   python src/calypso/librarian_agent.py --status
   # Should show increased document count

4. Commit:
   git add memory-bank/
   git commit -m "docs(memory): sprint [NNN] archived to cold zone"
```

---

## 7. Troubleshooting Guide

### 7.1 Calypso Pipeline Issues

#### Problem: `orchestrator_phase2.py` fails with `AuthenticationError`
```
anthropic.AuthenticationError: Invalid API key
```
**Solution:** Set the `ANTHROPIC_API_KEY` environment variable:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

#### Problem: `check_batch_status.py` shows batch in `errored` state
```
Batch status: errored
Failed requests: 2/4
```
**Solution:**
1. Check `batch_artifacts/batch_metadata_phase2.json` for error details
2. Re-run `orchestrator_phase2.py` â€” it creates a new batch
3. If errors persist, check the PRD format (must be valid Markdown, < 100KB)

#### Problem: `orchestrator_phase3.py` fails with `JSONDecodeError`
```
json.JSONDecodeError: Expecting value: line 1 column 1
```
**Solution:** The Synthesizer Agent returned non-JSON output. This can happen if the model adds markdown fences. The script strips common fences automatically, but if the issue persists:
1. Check `batch_artifacts/expert_reports/` â€” ensure all 4 reports are valid JSON
2. Re-run Phase 3 (it's synchronous and fast)

#### Problem: `apply_triage.py` shows `No decisions found`
```
[WARN] No checkbox decisions found in triage_dashboard.md
```
**Solution:** Ensure you checked the boxes correctly:
- Correct: `- [x] ACCEPT` (lowercase x, space after bracket)
- Wrong: `- [X] ACCEPT` (uppercase X â€” not recognized)
- Wrong: `- [ x] ACCEPT` (space before x)

### 7.2 FastMCP Server Issues

#### Problem: Roo Code shows "MCP server not connected"
**Solutions:**
1. Verify `mcp.json` exists at the project root
2. Check that `python` is in PATH: `python --version`
3. Check that `fastmcp` is installed: `pip show fastmcp`
4. Check the Roo Code MCP logs: `Ctrl+Shift+P` â†’ "Roo Code: Show MCP Logs"

#### Problem: `launch_factory` tool returns error about missing PRD
```
Error: PRD file not found: docs/prd.md
```
**Solution:** Pass the correct path:
```
Use launch_factory with prd_path="path/to/your/prd.md"
```

#### Problem: `memory_query` returns only keyword results (no semantic search)
```
[WARN] Chroma unavailable, falling back to keyword search
```
**Solution:** Start Chroma (see Section 5.3.1) and re-run the query.

### 7.3 Global Brain / Librarian Agent Issues

#### Problem: `librarian_agent.py --status` shows `DISCONNECTED`
```
Chroma status: DISCONNECTED
Error: Connection refused (localhost:8002)
```
**Solutions:**
1. Start Chroma: `chroma run --host 0.0.0.0 --port 8002 --path /data/chroma`
2. If using Tailscale (Calypso machine): verify Tailscale is connected
3. Check `CHROMA_HOST` and `CHROMA_PORT` environment variables

#### Problem: `librarian_agent.py --index` fails with `OllamaConnectionError`
```
Error: Cannot connect to Ollama at localhost:11434
```
**Solutions:**
1. Start Ollama: `ollama serve`
2. Verify `nomic-embed-text` is installed: `ollama list`
3. If model is missing: `ollama pull nomic-embed-text`

#### Problem: Embedding quality is poor (irrelevant results)
**Solutions:**
1. Ensure `nomic-embed-text` is used (not a smaller model)
2. Re-index after adding more content: `python src/calypso/librarian_agent.py --index`
3. Try more specific queries (include sprint numbers, dates, or specific terms)

### 7.4 Memory Bank Issues

#### Problem: Agent reads cold archive directly (RULE 9 violation)
**Symptom:** Agent uses `read_file` on `memory-bank/archive-cold/` files.
**Solution:** Remind the agent of RULE 9 in `.clinerules`:
```
RULE 9 applies: Do not read archive-cold/ directly.
Use memory_query MCP tool instead.
```

#### Problem: `activeContext.md` is stale (shows old task)
**Solution:** Update it manually or ask the Scrum Master mode:
```
Update memory-bank/hot-context/activeContext.md with the current state.
```

#### Problem: Hot-context files missing after deployment
**Solution:** The template files should have been copied by `deploy-workbench-to-project.ps1`. If missing:
```powershell
$Workbench = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench"
Copy-Item "$Workbench\template\memory-bank\hot-context\*" `
          "$Project\memory-bank\hot-context\" -Recurse
```

---

## 8. Reference: File Locations

### 8.1 Calypso Pipeline Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `orchestrator_phase2.py` | `src/calypso/` | Submit PRD to Batch API |
| `check_batch_status.py` | `src/calypso/` | Poll batch + retrieve expert reports |
| `orchestrator_phase3.py` | `src/calypso/` | Synthesizer Agent â†’ draft backlog |
| `orchestrator_phase4.py` | `src/calypso/` | Devil's Advocate â†’ final backlog |
| `triage_dashboard.py` | `src/calypso/` | Generate triage dashboard |
| `apply_triage.py` | `src/calypso/` | Apply human decisions |
| `fastmcp_server.py` | `src/calypso/` | MCP server for Roo Code |
| `librarian_agent.py` | `src/calypso/` | Global Brain indexing + query |

### 8.2 Calypso Artifacts

| Artifact | Location | Created By |
|----------|----------|-----------|
| `batch_id_phase2.txt` | `batch_artifacts/` | `orchestrator_phase2.py` |
| `batch_metadata_phase2.json` | `batch_artifacts/` | `orchestrator_phase2.py` |
| `expert_reports/*.json` | `batch_artifacts/expert_reports/` | `check_batch_status.py` |
| `draft_backlog.json` | `batch_artifacts/` | `orchestrator_phase3.py` |
| `final_backlog.json` | `batch_artifacts/` | `orchestrator_phase4.py` |
| `triage_dashboard.md` | `docs/` | `triage_dashboard.py` |

### 8.3 System Prompts

| ID | File | Agent |
|----|------|-------|
| SP-008 | `prompts/SP-008-synthesizer-agent.md` | Synthesizer Agent (Phase 3) |
| SP-009 | `prompts/SP-009-devils-advocate-agent.md` | Devil's Advocate (Phase 4) |
| SP-010 | `prompts/SP-010-librarian-agent.md` | Librarian Agent (Global Brain) |

### 8.4 Configuration Files

| File | Purpose |
|------|---------|
| `mcp.json` | FastMCP server config for Roo Code |
| `requirements.txt` | Python dependencies (includes `fastmcp`, `chromadb`, `jsonschema`) |
| `.env` | API keys (never commit to Git) |

### 8.5 Memory Bank Structure (v2.0)

```
memory-bank/
â”œâ”€â”€ projectBrief.md          # Project vision (root level, rarely changes)
â”œâ”€â”€ techContext.md           # Stack, commands, env vars (root level)
â”œâ”€â”€ hot-context/             # READ DIRECTLY by agents
â”‚   â”œâ”€â”€ activeContext.md     # Current task + next steps
â”‚   â”œâ”€â”€ progress.md          # Feature checklist
â”‚   â”œâ”€â”€ decisionLog.md       # Architecture Decision Records
â”‚   â”œâ”€â”€ systemPatterns.md    # Current architecture patterns
â”‚   â””â”€â”€ productContext.md    # Active sprint backlog
â””â”€â”€ archive-cold/            # ACCESS VIA MCP ONLY (RULE 9)
    â”œâ”€â”€ sprint-logs/         # Completed sprint retrospectives
    â”œâ”€â”€ completed-tickets/   # Closed backlog items
    â””â”€â”€ productContext_Master.md  # Cumulative product history
```

---

## 9. Appendix: Deployment Checklist

### 9.1 New Project with v2.0 Workbench

- [ ] Git repository created outside the workbench folder
- [ ] `deploy-workbench-to-project.ps1` run successfully
- [ ] `memory-bank/projectBrief.md` filled with project vision
- [ ] `memory-bank/techContext.md` filled with stack and commands
- [ ] `mcp.json` verified (path to `fastmcp_server.py` correct)
- [ ] `ANTHROPIC_API_KEY` set in environment
- [ ] Python venv created and `requirements.txt` installed
- [ ] Roo Code MCP server configured
- [ ] First commit done: `chore(init): project initialization with workbench v2.0`

### 9.2 Calypso Pipeline Run Checklist

- [ ] PRD file ready at known path
- [ ] `batch_artifacts/expert_reports/` directory created
- [ ] `ANTHROPIC_API_KEY` set
- [ ] Phase 2: batch submitted (`orchestrator_phase2.py`)
- [ ] Phase 2: batch complete, 4 expert reports retrieved (`check_batch_status.py --poll`)
- [ ] Phase 3: draft backlog generated (`orchestrator_phase3.py`)
- [ ] Phase 4: final backlog with GREEN/ORANGE classification (`orchestrator_phase4.py`)
- [ ] Triage dashboard generated (`triage_dashboard.py`)
- [ ] Human decisions entered in `docs/triage_dashboard.md`
- [ ] Triage applied (`apply_triage.py`)
- [ ] Backlog items visible in `memory-bank/hot-context/productContext.md`

### 9.3 Global Brain Setup Checklist

- [ ] Chroma installed: `pip install chromadb`
- [ ] Chroma running: `chroma run --host 0.0.0.0 --port 8002 --path /data/chroma`
- [ ] Ollama running with `nomic-embed-text` model
- [ ] Status check passes: `python src/calypso/librarian_agent.py --status`
- [ ] Initial indexing done: `python src/calypso/librarian_agent.py --index`
- [ ] Test query returns relevant results: `python src/calypso/librarian_agent.py --query "test"`
- [ ] `memory_query` MCP tool returns semantic results (not keyword fallback)

### 9.4 Sprint End Archival Checklist

- [ ] Sprint retrospective committed to Git
- [ ] `memory-bank/hot-context/progress.md` updated (sprint items checked off)
- [ ] `.\scripts\memory-archive.ps1` run successfully
- [ ] Librarian Agent indexed new files (check `--status` for increased count)
- [ ] `git commit -m "docs(memory): sprint [NNN] archived to cold zone"`

---

*End of DOC-4-v2.0-Operations-Guide.md*
