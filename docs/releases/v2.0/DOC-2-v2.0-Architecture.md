---
doc_id: DOC-2
release: v2.0
status: Frozen
title: Architecture Document
version: 0.1
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Architect mode, Human]
previous_release: docs/releases/v1.0/DOC-2-v1.0-Architecture.md
---

# DOC-2 -- Architecture Document (v2.0)

> **Status: DRAFT** -- This document is under active development on branch `release/v2.0`.
> It will be frozen when the v2.0 release is tagged.

---

## 1. Architecture Overview

### 1.1 System Tiers

The Agentic Agile Workbench v2.0 is organized into three tiers:

```
+----------------------------------------------------------+
|  TIER 1 -- Human Interface Layer                         |
|  VS Code + Roo Code (Windows 11 laptop)                  |
|  - 4 Agile personas (.roomodes)                          |
|  - Memory Bank (Hot/Cold architecture)                   |
|  - .clinerules (8 rules)                                 |
|  - MCP client (connects to Tier 2 FastMCP server)        |
+----------------------------------------------------------+
         |                          |
         | MCP tools                | Anthropic API
         v                          v
+---------------------------+  +----------------------------+
|  TIER 2 -- Calypso        |  |  TIER 3 -- Cloud APIs      |
|  Orchestration Layer      |  |                            |
|  (Python scripts, local)  |  |  - Anthropic Batch API     |
|  - fastmcp_server.py      |  |    (Committee of Experts)  |
|  - orchestrator_phase2.py |  |  - Gemini Chrome Proxy     |
|  - orchestrator_phase3.py |  |    (free, via proxy.py)    |
|  - orchestrator_phase4.py |  |  - Ollama on Calypso       |
|  - triage_dashboard.py    |  |    (local, sovereign)      |
|  - apply_triage.py        |  |                            |
|  - Global Brain (Chroma)  |  |                            |
+---------------------------+  +----------------------------+
```

### 1.2 Key Architectural Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| DA-001 | Hot/Cold memory split | Prevent context explosion; bounded activeContext.md |
| DA-002 | Anthropic Batch API for Phase 2 | Asynchronous; developer can disconnect; cost-efficient |
| DA-003 | FastMCP server on Calypso | Exposes Tier 2 tools to Roo Code via standard MCP protocol |
| DA-004 | Chroma for Global Brain (preferred) | Local-first; no cloud dependency; semantic search |
| DA-005 | GREEN/ORANGE classification in Phase 4 | Human arbitration only on ORANGE items; GREEN auto-accepted |
| DA-006 | Cold Zone Firewall in .clinerules | Agent cannot read cold archive directly; must use MCP query |

---

## 2. Hot/Cold Memory Architecture

### 2.1 Problem Statement

v1.0 loads all 7 `memory-bank/` files into every agent context window simultaneously. On large projects this causes:
- **Context explosion**: 7 files × growing content = thousands of tokens per session
- **"Lost in the Middle"**: Agent ignores content in the middle of a long context
- **No temporal separation**: Current sprint context mixed with historical data

### 2.2 Hot Zone (Read Every Session)

Location: `memory-bank/hot-context/`

| File | Purpose | Max Size |
|------|---------|---------|
| `activeContext.md` | Current task, last result, next steps, blockers | ~100 lines |
| `progress.md` | Sprint checkbox state | ~80 lines |
| `decisionLog.md` | Recent ADRs (last 5) | ~100 lines |
| `systemPatterns.md` | Current architecture patterns | ~80 lines |
| `productContext.md` | Current sprint user stories | ~60 lines |

**Total hot zone budget:** ~420 lines / ~8,000 tokens maximum.

### 2.3 Cold Zone (Read via MCP Only)

Location: `memory-bank/archive-cold/`

| Directory | Contents | Access Method |
|-----------|---------|--------------|
| `sprint-logs/` | Completed sprint summaries (one file per sprint) | `memory:query(semantic)` |
| `completed-tickets/` | Closed ticket details | `memory:query(semantic)` |
| `productContext_Master.md` | Historical BDD accumulator (all sprints) | `memory:query(semantic)` |

### 2.4 Cold Zone Firewall

A new clause in `.clinerules` (RULE 9, to be added in PHASE-A) enforces:
> The agent MUST NOT read files in `memory-bank/archive-cold/` directly.
> All access to cold archive MUST go through the `memory:query` MCP tool.

### 2.5 Memory Rotation Protocol

At sprint end, the `memory:archive` script:
1. Appends `activeContext.md` to `archive-cold/sprint-logs/sprint-NNN.md`
2. Appends `productContext.md` to `archive-cold/productContext_Master.md`
3. Resets `activeContext.md` and `productContext.md` to blank stubs
4. Triggers Librarian Agent to index new cold archive content into vector DB

---

## 3. Calypso Orchestration Layer (Tier 2)

### 3.1 The Asynchronous Factory Concept

The core innovation of v2.0 is the ability to **disconnect after Phase 1** and let the factory run autonomously:

```
Phase 1 (Human + Roo Code):
  Human writes PRD → Roo Code refines → DOC-1 approved

Phase 2 (Calypso, async):
  orchestrator_phase2.py dispatches PRD to Anthropic Batch API
  → Committee of Experts (Architecture, Security, UX/UI, QA agents)
  → Human disconnects; factory runs overnight

Phase 3 (Calypso, auto):
  check_batch_status.py retrieves results when ready
  orchestrator_phase3.py runs Synthesizer Agent
  → draft_backlog.json produced

Phase 4 (Calypso, auto):
  orchestrator_phase4.py runs Devil's Advocate (MAX_ATTEMPTS=2)
  → final_backlog.json with GREEN/ORANGE classification

Human arbitration:
  triage_dashboard.py generates triage_dashboard.md
  Human reviews ORANGE items, checks boxes
  apply_triage.py applies decisions → systemPatterns.md + productContext.md updated
```

### 3.2 Script Architecture

#### 3.2.1 orchestrator_phase2.py

**Input:** `docs/releases/vX.Y/DOC-1-vX.Y-PRD.md`
**Output:** Anthropic Batch job ID (saved to `batch_id_phase2.txt`)
**Agents dispatched:**
- `architecture_expert`: Reviews technical feasibility, identifies risks
- `security_expert`: Reviews security implications, OWASP top 10
- `ux_expert`: Reviews user experience, accessibility
- `qa_expert`: Reviews testability, acceptance criteria completeness

#### 3.2.2 check_batch_status.py

**Input:** `batch_id_phase2.txt`
**Output:** `expert_reports/` directory with one JSON file per expert
**Behavior:** Polls every 60 seconds until batch complete; validates JSON schema

#### 3.2.3 orchestrator_phase3.py

**Input:** `expert_reports/` + `DOC-1-vX.Y-PRD.md`
**Output:** `draft_backlog.json`
**Agent:** Synthesizer Agent (SP-008) -- consolidates expert reports into structured backlog

#### 3.2.4 orchestrator_phase4.py

**Input:** `draft_backlog.json` + `DOC-1-vX.Y-PRD.md`
**Output:** `final_backlog.json`
**Agent:** Devil's Advocate (SP-009) -- challenges each backlog item
**Classification:**
- `GREEN`: Item accepted without challenge
- `ORANGE`: Item challenged; requires human arbitration

#### 3.2.5 triage_dashboard.py

**Input:** `final_backlog.json`
**Output:** `triage_dashboard.md` (human-readable, with checkboxes for ORANGE items)

#### 3.2.6 apply_triage.py

**Input:** `triage_dashboard.md` (with human checkbox decisions)
**Output:** Updated `memory-bank/hot-context/systemPatterns.md` + `productContext.md`

#### 3.2.7 fastmcp_server.py

**Protocol:** FastMCP (MCP-compatible)
**Port:** 8001 (configurable)
**Tools exposed:**
- `launch_factory(prd_path)` -- starts Phase 2 pipeline
- `check_batch_status(batch_id)` -- polls Anthropic Batch API
- `retrieve_backlog(phase)` -- returns draft or final backlog
- `memory:query(semantic_query)` -- queries Global Brain vector DB
- `memory:archive()` -- rotates hot-context to cold archive

---

## 4. Global Brain / Librarian Agent

### 4.1 Architecture

```
+------------------+     index     +------------------+
|  Cold Archive    | ------------> |  Vector DB       |
|  (markdown files)|               |  (Chroma, local) |
+------------------+               +------------------+
                                          |
                                   semantic query
                                          |
                                   +------v-------+
                                   |  Librarian   |
                                   |  Agent       |
                                   |  (SP-010)    |
                                   +------+-------+
                                          |
                                   MCP tool: memory:query
                                          |
                                   +------v-------+
                                   |  Roo Code    |
                                   |  (Tier 1)    |
                                   +--------------+
```

### 4.2 Vector Database Choice

**Preferred: Chroma (local)**
- Runs on Calypso (same machine as Ollama)
- No cloud dependency
- Python client library (`chromadb`)
- Persistent storage on Calypso disk

**Alternative: Mem0 (cloud)**
- Managed service; no local setup
- Requires internet connection
- Better semantic search quality
- Decision deferred to PHASE-D implementation

### 4.3 Librarian Agent (SP-010)

**Trigger:** Runs at sprint end after `memory:archive`
**Input:** New files in `archive-cold/`
**Action:** Chunks and indexes new content into Chroma
**System prompt:** SP-010 (to be written in PHASE-D)

### 4.4 memory:query Tool

**Input:** Natural language semantic query
**Output:** Top-K relevant chunks from cold archive with source file references
**Example:** `memory:query("What decisions were made about the proxy architecture?")`

---

## 5. LLM Backend Architecture (Unchanged from v1.0)

### 5.1 3-Mode Switcher

| Mode | Provider | Model | Use Case |
|------|---------|-------|---------|
| 1 | Ollama (Calypso) | `uadf-agent` (14b) | Sovereign, free, offline |
| 2 | Gemini Chrome Proxy | `gemini-manual` | Free cloud, copy-paste |
| 3 | Anthropic Claude API | `claude-sonnet-4-6` | Full automation, paid |

### 5.2 Batch API (New in v2.0)

The Anthropic Batch API is used exclusively by Tier 2 orchestration scripts (not by Roo Code directly). It enables:
- Asynchronous multi-agent dispatch (no blocking)
- Cost reduction (~50% vs. synchronous API)
- Parallel expert committee execution

---

## 6. Security and Sovereignty

### 6.1 Data Residency

| Data Type | Location | Leaves Local Network? |
|-----------|---------|----------------------|
| Source code | Local disk | Only on explicit git push |
| Memory bank | Local disk | Only on explicit git push |
| PRD / backlog | Local disk | Sent to Anthropic Batch API (Phase 2 only) |
| Expert reports | Local disk | Never |
| Vector DB | Calypso disk | Never |

### 6.2 API Key Management

- Anthropic API key: stored in VS Code SecretStorage (never in files)
- No other API keys required for core functionality
- Gemini proxy uses a fake key (`sk-fake-key-uadf`) -- no real credentials

### 6.3 Cold Zone Firewall

The Cold Zone Firewall (RULE 9 in `.clinerules`) prevents agents from accidentally reading stale historical context. This is both a performance optimization and a correctness guarantee.

---

## 7. Directory Structure (v2.0 Target)

```
agentic-agile-workbench/
+-- .clinerules                    # 9 rules (RULE 9 = Cold Zone Firewall)
+-- .roomodes                      # 4 Agile personas
+-- .gitignore
+-- Modelfile                      # uadf-agent Ollama model
+-- proxy.py                       # Gemini Chrome proxy v2.8.0
+-- requirements.txt
+-- deploy-workbench-to-project.ps1
+-- VERSION
+-- docs/
|   +-- DOC-1-CURRENT.md           # Pointer to current release DOC-1
|   +-- DOC-2-CURRENT.md
|   +-- DOC-3-CURRENT.md
|   +-- DOC-4-CURRENT.md
|   +-- DOC-5-CURRENT.md
|   +-- releases/
|   |   +-- v1.0/                  # FROZEN
|   |   +-- v2.0/                  # ACTIVE (this release)
|   +-- ideas/
|   +-- conversations/
|   +-- qa/
+-- memory-bank/
|   +-- hot-context/               # NEW in v2.0
|   |   +-- activeContext.md
|   |   +-- progress.md
|   |   +-- decisionLog.md
|   |   +-- systemPatterns.md
|   |   +-- productContext.md
|   +-- archive-cold/              # NEW in v2.0
|   |   +-- sprint-logs/
|   |   +-- completed-tickets/
|   |   +-- productContext_Master.md
+-- prompts/                       # SP-001..010
+-- scripts/
|   +-- check-prompts-sync.ps1
|   +-- start-proxy.ps1
|   +-- memory-archive.ps1         # NEW in v2.0
+-- src/
|   +-- calypso/                   # NEW in v2.0
|   |   +-- orchestrator_phase2.py
|   |   +-- check_batch_status.py
|   |   +-- orchestrator_phase3.py
|   |   +-- orchestrator_phase4.py
|   |   +-- triage_dashboard.py
|   |   +-- apply_triage.py
|   |   +-- fastmcp_server.py
|   |   +-- librarian_agent.py
+-- template/                      # Updated in v2.0
|   +-- .clinerules                # With RULE 9
|   +-- .roomodes
|   +-- Modelfile
|   +-- proxy.py
|   +-- requirements.txt
|   +-- mcp.json                   # NEW in v2.0
|   +-- docs/                      # NEW in v2.0 (PHASE-0)
|   +-- memory-bank/               # NEW in v2.0 (PHASE-B)
|   |   +-- hot-context/
|   |   +-- archive-cold/
|   +-- prompts/
|   +-- scripts/
```

---

## 8. System Prompts Registry (v2.0 Additions)

| ID | Name | Status | Purpose |
|----|------|--------|---------|
| SP-001 | Ollama Modelfile system block | Existing | Local LLM system prompt |
| SP-002 | .clinerules global rules | v2.3.0 | Agent governance rules |
| SP-003 | Product Owner persona | Existing | Requirements, user stories |
| SP-004 | Scrum Master persona | Existing | Sprint planning, process |
| SP-005 | Developer persona | Existing | Code, commits |
| SP-006 | QA Engineer persona | Existing | Tests, QA reports |
| SP-007 | Gem Gemini Roo Code Agent | Existing | Gemini proxy agent |
| SP-008 | Synthesizer Agent | NEW v2.0 | Phase 3 backlog synthesis |
| SP-009 | Devil's Advocate Agent | NEW v2.0 | Phase 4 backlog challenge |
| SP-010 | Librarian Agent | NEW v2.0 | Cold archive indexing |

---

## 9. References

| Document | Location |
|----------|---------|
| DOC-1-v2.0-PRD.md | docs/releases/v2.0/DOC-1-v2.0-PRD.md |
| DOC-3-v2.0-Implementation-Plan.md | docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md |
| DOC-2-v1.0-Architecture.md | docs/releases/v1.0/DOC-2-v1.0-Architecture.md |
| IDEA-001 Hot/Cold Memory | docs/ideas/IDEA-001-hot-cold-memory.md |
| IDEA-002 Calypso Orchestration | docs/ideas/IDEA-002-calypso-orchestration.md |
| IDEA-007 Global Brain | docs/ideas/IDEAS-BACKLOG.md |
| DOC6 Batch Review Results 2 | plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md |
