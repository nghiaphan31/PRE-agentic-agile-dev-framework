---
doc_id: DOC-3
release: v2.0
status: Draft
title: Implementation Plan
version: 0.1
date_created: 2026-03-28
date_frozen: TBD
authors: [Architect mode, Human]
previous_release: docs/releases/v1.0/DOC-3-v1.0-Implementation-Plan.md
---

# DOC-3 -- Implementation Plan (v2.0)

> **Status: DRAFT** -- This document is under active development on branch `release/v2.0`.
> It will be frozen when the v2.0 release is tagged.

---

## Table of Contents

1. [Overview and Sequencing](#1-overview-and-sequencing)
2. [PHASE-0: Release Governance Restructure](#2-phase-0-release-governance-restructure)
3. [PHASE-A: Hot/Cold Memory Architecture](#3-phase-a-hotcold-memory-architecture)
4. [PHASE-B: Template Folder Enrichment](#4-phase-b-template-folder-enrichment)
5. [PHASE-C: Calypso Orchestration Scripts](#5-phase-c-calypso-orchestration-scripts)
6. [PHASE-D: Global Brain / Librarian Agent](#6-phase-d-global-brain--librarian-agent)
7. [PHASE-E: v2.0 Release Finalization](#7-phase-e-v20-release-finalization)
8. [Dependencies and Sequencing Constraints](#8-dependencies-and-sequencing-constraints)
9. [Validation Criteria](#9-validation-criteria)

---

## 1. Overview and Sequencing

### 1.1 Phase Summary

| Phase | Name | Status | Prerequisite | Estimated Effort |
|-------|------|--------|-------------|-----------------|
| PHASE-0 | Release Governance Restructure | COMPLETE | None | Done |
| PHASE-A | Hot/Cold Memory Architecture | Pending | PHASE-0 | 1 session |
| PHASE-B | Template Folder Enrichment | Pending | PHASE-A | 1 session |
| PHASE-C | Calypso Orchestration Scripts | Pending | PHASE-B | 3-4 sessions |
| PHASE-D | Global Brain / Librarian Agent | Pending | PHASE-C | 2-3 sessions |
| PHASE-E | v2.0 Release Finalization | Pending | PHASE-D | 1 session |

### 1.2 Sequencing Rationale

```
PHASE-0 (governance) --> PHASE-A (memory) --> PHASE-B (template)
                                                      |
                                                      v
                                              PHASE-C (calypso)
                                                      |
                                                      v
                                              PHASE-D (global brain)
                                                      |
                                                      v
                                              PHASE-E (release)
```

**Why this order:**
1. PHASE-0 first: governance structure must exist before any v2.0 work is tracked
2. PHASE-A before PHASE-B: template must reflect the new memory structure
3. PHASE-B before PHASE-C: Calypso scripts deposit output into the local environment; that environment must be stable first
4. PHASE-C before PHASE-D: Librarian Agent indexes cold archive; cold archive is populated by the factory pipeline
5. PHASE-E last: all features must be complete before release finalization

---

## 2. PHASE-0: Release Governance Restructure

**Status: COMPLETE** (commit 905d418, 2026-03-28)

### 2.1 Summary of Completed Steps

| Step | Description | Commit |
|------|-------------|--------|
| PHASE-0.1 | Tagged v1.0.0-baseline on master | Prior session |
| PHASE-0.2 | Created release/v2.0 branch | Prior session |
| PHASE-0.3 | Created docs/ folder structure | 905d418 |
| PHASE-0.4 | Moved + renamed workbench/ docs to docs/releases/v1.0/ | 905d418 |
| PHASE-0.5 | Created DOC-5-v1.0-Release-Notes.md | 905d418 |
| PHASE-0.6 | Moved QA reports to docs/qa/v1.0/ | 905d418 |
| PHASE-0.7 | Moved Gemini conversations to docs/conversations/ | 905d418 |
| PHASE-0.8 | Created docs/ideas/ with IDEAS-BACKLOG.md + IDEA-001..003 | 905d418 |
| PHASE-0.9 | Created docs/DOC-1..5-CURRENT.md pointer stubs | 905d418 |
| PHASE-0.10 | Deleted workbench/ folder | 905d418 |
| PHASE-0.11 | Added RULE 8 to .clinerules + SP-002 v2.3.0 sync | 905d418 |
| PHASE-0.12 | Tagged v1.0.0 + pushed to origin | 905d418 |
| PHASE-0.13 | Created template/docs/ structure | 905d418 |

### 2.2 Deliverables

- [x] `docs/releases/v1.0/` with 5 canonical docs (DOC-1..5) + EXECUTION-TRACKER + RESUME-GUIDE
- [x] `docs/releases/v2.0/` (active, this release)
- [x] `docs/ideas/` with IDEAS-BACKLOG.md + IDEA-001..003
- [x] `docs/conversations/` with README.md
- [x] `docs/qa/v1.0/` with QA reports
- [x] `docs/DOC-1..5-CURRENT.md` pointer stubs
- [x] `.clinerules` RULE 8 (Documentation Discipline)
- [x] SP-002 v2.3.0 (synced to all 4 copies)
- [x] `template/docs/` structure
- [x] Git tags: `v1.0.0-baseline` (on master), `v1.0.0` (on release/v2.0)

---

## 3. PHASE-A: Hot/Cold Memory Architecture

**Status: Pending**
**Prerequisite:** PHASE-0 complete
**Estimated effort:** 1 session

### 3.1 Objectives

Transform the flat `memory-bank/` (7 monolithic files) into a Hot/Cold architecture:
- Hot Zone: `memory-bank/hot-context/` (5 files, read every session)
- Cold Zone: `memory-bank/archive-cold/` (historical data, MCP-only access)
- Add RULE 9 (Cold Zone Firewall) to `.clinerules`
- Add `memory:archive` script

### 3.2 Steps

#### PHASE-A.1 -- Create Hot/Cold Directory Structure

```
memory-bank/
+-- hot-context/
|   +-- activeContext.md      (migrated from memory-bank/activeContext.md)
|   +-- progress.md           (migrated from memory-bank/progress.md)
|   +-- decisionLog.md        (migrated from memory-bank/decisionLog.md)
|   +-- systemPatterns.md     (migrated from memory-bank/systemPatterns.md)
|   +-- productContext.md     (migrated from memory-bank/productContext.md)
+-- archive-cold/
|   +-- sprint-logs/
|   |   +-- .gitkeep
|   +-- completed-tickets/
|   |   +-- .gitkeep
|   +-- productContext_Master.md  (blank stub)
```

**Validation:** Directory structure exists; all 5 hot-context files contain current content.

#### PHASE-A.2 -- Migrate Existing Files

Use `git mv` to preserve history:
```
git mv memory-bank/activeContext.md memory-bank/hot-context/activeContext.md
git mv memory-bank/progress.md memory-bank/hot-context/progress.md
git mv memory-bank/decisionLog.md memory-bank/hot-context/decisionLog.md
git mv memory-bank/systemPatterns.md memory-bank/hot-context/systemPatterns.md
git mv memory-bank/productContext.md memory-bank/hot-context/productContext.md
```

**Note:** `projectBrief.md` and `techContext.md` remain at `memory-bank/` root (they are reference docs, not session context).

**Validation:** `git status` shows renames; content unchanged.

#### PHASE-A.3 -- Add RULE 9 (Cold Zone Firewall) to .clinerules

Insert after RULE 8, before MEMORY BANK FILE TEMPLATES:

```
## RULE 9: COLD ZONE FIREWALL -- MANDATORY MEMORY ACCESS PROTOCOL

### 9.1 -- Hot Zone (Read Directly)
Files in `memory-bank/hot-context/` are read directly by the agent at session start (RULE 1).

### 9.2 -- Cold Zone (MCP Only)
Files in `memory-bank/archive-cold/` MUST NOT be read directly by the agent.
All access to cold archive MUST go through the `memory:query` MCP tool:
  memory:query("your semantic query here")

### 9.3 -- Why This Rule Exists
Direct reading of cold archive files would:
1. Flood the context window with stale historical data
2. Cause "Lost in the Middle" errors on large projects
3. Defeat the purpose of the Hot/Cold architecture

### 9.4 -- Exception
The Librarian Agent (SP-010) is the ONLY agent authorized to read cold archive files
directly, for the purpose of indexing them into the vector database.
```

**Validation:** `.clinerules` contains RULE 9; `template/.clinerules` synced; SP-002 bumped to v2.4.0.

#### PHASE-A.4 -- Update RULE 1 in .clinerules

Update the READ step in RULE 1 to reference the new hot-context path:

```
3. READ : Read memory-bank/hot-context/activeContext.md then memory-bank/hot-context/progress.md
```

**Validation:** RULE 1 references `hot-context/` paths.

#### PHASE-A.5 -- Create memory-archive Script

Create `scripts/memory-archive.ps1`:
- Appends `hot-context/activeContext.md` to `archive-cold/sprint-logs/sprint-NNN.md`
- Appends `hot-context/productContext.md` to `archive-cold/productContext_Master.md`
- Resets `hot-context/activeContext.md` and `hot-context/productContext.md` to blank stubs
- Prints confirmation message

**Validation:** Script runs without error; sprint log file created in `archive-cold/sprint-logs/`.

#### PHASE-A.6 -- Update Memory Bank Templates in .clinerules

Update the MEMORY BANK FILE TEMPLATES section to reference `hot-context/` paths.

**Validation:** Templates reference correct paths.

#### PHASE-A.7 -- Commit and Push

```
git add .
git commit -m "feat(memory): PHASE-A complete -- Hot/Cold memory architecture

- memory-bank/hot-context/ created (5 files migrated via git mv)
- memory-bank/archive-cold/ created (sprint-logs/, completed-tickets/, productContext_Master.md)
- RULE 9 (Cold Zone Firewall) added to .clinerules
- RULE 1 updated to reference hot-context/ paths
- scripts/memory-archive.ps1 created
- SP-002 bumped to v2.4.0
- template/ updated with new memory-bank/ structure"
git push origin release/v2.0
```

### 3.3 Deliverables

- [ ] `memory-bank/hot-context/` with 5 migrated files
- [ ] `memory-bank/archive-cold/` with subdirectory structure
- [ ] RULE 9 in `.clinerules` (Cold Zone Firewall)
- [ ] RULE 1 updated to reference `hot-context/` paths
- [ ] `scripts/memory-archive.ps1`
- [ ] SP-002 v2.4.0
- [ ] `template/memory-bank/` updated

---

## 4. PHASE-B: Template Folder Enrichment

**Status: Pending**
**Prerequisite:** PHASE-A complete
**Estimated effort:** 1 session

### 4.1 Objectives

Enrich the `template/` folder to include:
- Hot/Cold memory structure (from PHASE-A)
- MCP configuration template (`mcp.json`)
- Updated `.clinerules` with RULE 9
- Updated deployment script

### 4.2 Steps

#### PHASE-B.1 -- Add memory-bank/ Structure to template/

```
template/memory-bank/
+-- hot-context/
|   +-- activeContext.md      (blank stub)
|   +-- progress.md           (blank stub)
|   +-- decisionLog.md        (blank stub)
|   +-- systemPatterns.md     (blank stub)
|   +-- productContext.md     (blank stub)
+-- archive-cold/
|   +-- sprint-logs/
|   |   +-- .gitkeep
|   +-- completed-tickets/
|   |   +-- .gitkeep
|   +-- productContext_Master.md  (blank stub)
```

**Validation:** All files exist with correct blank stub content.

#### PHASE-B.2 -- Create template/mcp.json

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

**Validation:** File is valid JSON; placeholder values documented.

#### PHASE-B.3 -- Update deploy-workbench-to-project.ps1

Add copy of `template/memory-bank/` and `template/mcp.json` to the deployment script.

**Validation:** Script copies new files to target project directory.

#### PHASE-B.4 -- Commit and Push

```
git add .
git commit -m "feat(template): PHASE-B complete -- template folder enrichment

- template/memory-bank/ with Hot/Cold structure (blank stubs)
- template/mcp.json with Calypso FastMCP server entry
- deploy-workbench-to-project.ps1 updated"
git push origin release/v2.0
```

### 4.3 Deliverables

- [ ] `template/memory-bank/hot-context/` with 5 blank stubs
- [ ] `template/memory-bank/archive-cold/` with subdirectory structure
- [ ] `template/mcp.json`
- [ ] `deploy-workbench-to-project.ps1` updated

---

## 5. PHASE-C: Calypso Orchestration Scripts

**Status: Pending**
**Prerequisite:** PHASE-B complete
**Estimated effort:** 3-4 sessions

### 5.1 Objectives

Build the complete Tier 2 orchestration layer:
- 7 Python scripts implementing the Phase 2-4 pipeline
- FastMCP server exposing tools to Roo Code
- End-to-end test: PRD in → `final_backlog.json` out

### 5.2 Steps

#### PHASE-C.1 -- Create src/calypso/ Directory Structure

```
src/calypso/
+-- __init__.py
+-- orchestrator_phase2.py
+-- check_batch_status.py
+-- orchestrator_phase3.py
+-- orchestrator_phase4.py
+-- triage_dashboard.py
+-- apply_triage.py
+-- fastmcp_server.py
+-- librarian_agent.py        (stub, implemented in PHASE-D)
+-- schemas/
|   +-- expert_report.json    (JSON schema for expert report validation)
|   +-- backlog_item.json     (JSON schema for backlog item validation)
+-- tests/
|   +-- test_orchestrator.py
|   +-- test_triage.py
|   +-- fixtures/
|       +-- sample_prd.md
|       +-- sample_expert_report.json
|       +-- sample_backlog.json
```

**Validation:** Directory structure exists; `__init__.py` present.

#### PHASE-C.2 -- Implement orchestrator_phase2.py

**Inputs:**
- `prd_path`: Path to DOC-1-vX.Y-PRD.md
- `output_dir`: Directory for batch artifacts (default: `batch_artifacts/`)

**Behavior:**
1. Read PRD content
2. Build JSONL batch request with 4 expert agents:
   - `architecture_expert`: Technical feasibility, risks, scalability
   - `security_expert`: Security implications, OWASP top 10, data privacy
   - `ux_expert`: User experience, accessibility, workflow clarity
   - `qa_expert`: Testability, acceptance criteria completeness, edge cases
3. Submit to Anthropic Batch API
4. Save batch ID to `batch_artifacts/batch_id_phase2.txt`
5. Print confirmation with estimated completion time

**System prompts:** SP-008 (Synthesizer Agent) -- to be written as part of this step.

**Validation:** Batch job submitted; `batch_id_phase2.txt` created; batch visible in Anthropic console.

#### PHASE-C.3 -- Implement check_batch_status.py

**Inputs:**
- `batch_id_file`: Path to `batch_id_phase2.txt`
- `output_dir`: Directory for expert reports (default: `batch_artifacts/expert_reports/`)
- `--poll`: If set, polls every 60 seconds until complete

**Behavior:**
1. Read batch ID from file
2. Query Anthropic Batch API for status
3. If complete: retrieve results, validate against `schemas/expert_report.json`, save to `expert_reports/`
4. If pending: print status and exit (or poll if `--poll` flag set)

**Validation:** Expert reports saved to `expert_reports/`; JSON schema validation passes.

#### PHASE-C.4 -- Implement orchestrator_phase3.py

**Inputs:**
- `expert_reports_dir`: Path to `batch_artifacts/expert_reports/`
- `prd_path`: Path to DOC-1-vX.Y-PRD.md
- `output_path`: Path for `draft_backlog.json` (default: `batch_artifacts/draft_backlog.json`)

**Behavior:**
1. Read all expert reports
2. Read PRD
3. Call Synthesizer Agent (SP-008) via Anthropic API (synchronous)
4. Parse response into structured backlog items
5. Validate against `schemas/backlog_item.json`
6. Save to `draft_backlog.json`

**Output format (draft_backlog.json):**
```json
{
  "version": "1.0",
  "prd_ref": "docs/releases/v2.0/DOC-1-v2.0-PRD.md",
  "generated_at": "2026-03-28T14:00:00Z",
  "items": [
    {
      "id": "BL-001",
      "title": "...",
      "description": "...",
      "acceptance_criteria": ["..."],
      "source_experts": ["architecture_expert", "qa_expert"],
      "priority": "HIGH|MEDIUM|LOW",
      "phase": "PHASE-A|PHASE-B|PHASE-C|PHASE-D"
    }
  ]
}
```

**Validation:** `draft_backlog.json` created; JSON schema validation passes; at least 5 backlog items.

#### PHASE-C.5 -- Implement orchestrator_phase4.py

**Inputs:**
- `draft_backlog_path`: Path to `draft_backlog.json`
- `prd_path`: Path to DOC-1-vX.Y-PRD.md
- `output_path`: Path for `final_backlog.json` (default: `batch_artifacts/final_backlog.json`)
- `--max-attempts`: Devil's Advocate iterations (default: 2)

**Behavior:**
1. Read draft backlog and PRD
2. For each backlog item, run Devil's Advocate Agent (SP-009):
   - Challenge: "What could go wrong with this item?"
   - If challenge accepted: mark ORANGE, add challenge text
   - If challenge rejected: mark GREEN
3. After MAX_ATTEMPTS, finalize classification
4. Save to `final_backlog.json`

**Output format (final_backlog.json):**
```json
{
  "version": "1.0",
  "items": [
    {
      "id": "BL-001",
      "title": "...",
      "classification": "GREEN|ORANGE",
      "challenge": "...",        // only for ORANGE items
      "human_decision": null     // filled by apply_triage.py
    }
  ]
}
```

**Validation:** `final_backlog.json` created; all items have GREEN or ORANGE classification.

#### PHASE-C.6 -- Implement triage_dashboard.py

**Inputs:**
- `final_backlog_path`: Path to `final_backlog.json`
- `output_path`: Path for `triage_dashboard.md` (default: `batch_artifacts/triage_dashboard.md`)

**Behavior:**
1. Read final backlog
2. Generate markdown with:
   - Summary table (GREEN count, ORANGE count)
   - GREEN items section (auto-accepted, no action needed)
   - ORANGE items section (each with checkbox: `- [ ] ACCEPT` / `- [ ] REJECT`)
   - Instructions for human arbitration

**Validation:** `triage_dashboard.md` created; ORANGE items have checkboxes; GREEN items listed.

#### PHASE-C.7 -- Implement apply_triage.py

**Inputs:**
- `triage_dashboard_path`: Path to `triage_dashboard.md` (with human checkbox decisions)
- `final_backlog_path`: Path to `final_backlog.json`
- `systempatterns_path`: Path to `memory-bank/hot-context/systemPatterns.md`
- `productcontext_path`: Path to `memory-bank/hot-context/productContext.md`

**Behavior:**
1. Parse checkbox decisions from `triage_dashboard.md`
2. Update `final_backlog.json` with `human_decision` field
3. Append accepted items to `systemPatterns.md` (architectural decisions)
4. Append accepted items to `productContext.md` (user stories for next sprint)
5. Print summary of applied decisions

**Validation:** `systemPatterns.md` and `productContext.md` updated; `final_backlog.json` has `human_decision` values.

#### PHASE-C.8 -- Implement fastmcp_server.py

**Protocol:** FastMCP (MCP-compatible, port 8001)
**Dependencies:** `fastmcp` Python package

**Tools to expose:**
```python
@mcp.tool()
def launch_factory(prd_path: str) -> str:
    """Start Phase 2 pipeline for the given PRD."""

@mcp.tool()
def check_batch_status(batch_id: str) -> dict:
    """Check status of an Anthropic Batch job."""

@mcp.tool()
def retrieve_backlog(phase: str) -> dict:
    """Retrieve draft or final backlog. phase: 'draft' or 'final'"""

@mcp.tool()
def memory_query(semantic_query: str, top_k: int = 5) -> list:
    """Query the Global Brain vector DB. Returns top-K relevant chunks."""

@mcp.tool()
def memory_archive() -> str:
    """Rotate hot-context to cold archive. Returns archive summary."""
```

**Validation:** Server starts on port 8001; Roo Code can connect; all 5 tools respond correctly.

#### PHASE-C.9 -- Write SP-008 (Synthesizer Agent) and SP-009 (Devil's Advocate)

**SP-008 Synthesizer Agent:**
- Role: Consolidate expert reports into a structured product backlog
- Input format: Expert reports + PRD
- Output format: JSON backlog items (strict schema)
- Tone: Analytical, structured, no hallucination

**SP-009 Devil's Advocate Agent:**
- Role: Challenge each backlog item to identify risks and ambiguities
- Input format: Single backlog item + PRD context
- Output format: Challenge text + ACCEPT/REJECT recommendation
- Tone: Critical, constructive, evidence-based

**Validation:** Both SPs added to `prompts/` registry; `prompts/README.md` updated.

#### PHASE-C.10 -- End-to-End Test

Run the complete pipeline with a sample PRD:
1. `python src/calypso/orchestrator_phase2.py --prd docs/releases/v2.0/DOC-1-v2.0-PRD.md`
2. Wait for batch completion
3. `python src/calypso/check_batch_status.py`
4. `python src/calypso/orchestrator_phase3.py`
5. `python src/calypso/orchestrator_phase4.py`
6. `python src/calypso/triage_dashboard.py`
7. Human reviews `triage_dashboard.md`, checks boxes
8. `python src/calypso/apply_triage.py`

**Validation:** All steps complete without error; `final_backlog.json` produced; `systemPatterns.md` updated.

#### PHASE-C.11 -- Commit and Push

```
git add .
git commit -m "feat(calypso): PHASE-C complete -- Calypso orchestration scripts

- src/calypso/ directory with 7 scripts + schemas + tests
- orchestrator_phase2.py: PRD -> Anthropic Batch API dispatch
- check_batch_status.py: Batch API polling + expert report retrieval
- orchestrator_phase3.py: Synthesizer Agent -> draft_backlog.json
- orchestrator_phase4.py: Devil's Advocate -> final_backlog.json
- triage_dashboard.py: final_backlog.json -> triage_dashboard.md
- apply_triage.py: human decisions -> systemPatterns.md + productContext.md
- fastmcp_server.py: FastMCP server (port 8001) with 5 tools
- SP-008 Synthesizer Agent + SP-009 Devil's Advocate added to prompts/
- End-to-end test passed"
git push origin release/v2.0
```

### 5.3 Deliverables

- [ ] `src/calypso/` with 7 scripts + schemas + tests
- [ ] `batch_artifacts/` directory structure documented
- [ ] SP-008 Synthesizer Agent in `prompts/`
- [ ] SP-009 Devil's Advocate in `prompts/`
- [ ] `fastmcp_server.py` running on port 8001
- [ ] End-to-end test passed
- [ ] `template/mcp.json` updated with correct tool names

---

## 6. PHASE-D: Global Brain / Librarian Agent

**Status: Pending**
**Prerequisite:** PHASE-C complete
**Estimated effort:** 2-3 sessions

### 6.1 Objectives

Implement the cross-project memory layer:
- Chroma vector DB running on Calypso
- Librarian Agent (SP-010) indexing cold archive
- `memory:query` MCP tool returning semantic results
- Retrospective workflow: sprint end → archive → index → query

### 6.2 Steps

#### PHASE-D.1 -- Install and Configure Chroma on Calypso

```bash
# On Calypso (SSH)
pip install chromadb
# Start Chroma server
chroma run --host 0.0.0.0 --port 8002 --path /data/chroma
```

**Configuration:**
- Host: `calypso` (via Tailscale)
- Port: 8002
- Persistent storage: `/data/chroma`

**Validation:** Chroma server running; accessible from Windows laptop via `http://calypso:8002`.

#### PHASE-D.2 -- Implement librarian_agent.py

**Trigger:** Called by `memory:archive` MCP tool after rotation
**Input:** List of new files in `archive-cold/`
**Behavior:**
1. Read each new file
2. Chunk content into ~500-token segments
3. Generate embeddings using Ollama (`nomic-embed-text` model)
4. Index chunks into Chroma with metadata:
   - `source_file`: original file path
   - `sprint`: sprint number (if sprint log)
   - `date`: file creation date
   - `type`: `sprint_log | ticket | product_context`
5. Print indexing summary

**Validation:** Chroma collection populated; `memory:query` returns relevant results.

#### PHASE-D.3 -- Implement memory:query in fastmcp_server.py

Update `fastmcp_server.py` to implement the `memory_query` tool:
1. Connect to Chroma on `calypso:8002`
2. Generate query embedding using Ollama
3. Query Chroma for top-K similar chunks
4. Return chunks with source file references and similarity scores

**Validation:** `memory:query("proxy architecture decisions")` returns relevant chunks from cold archive.

#### PHASE-D.4 -- Write SP-010 (Librarian Agent)

**SP-010 Librarian Agent:**
- Role: Index cold archive content into vector DB; answer semantic queries
- Trigger: Sprint end (after `memory:archive`)
- Input: New cold archive files
- Output: Indexed chunks in Chroma
- Tone: Systematic, precise, no interpretation

**Validation:** SP-010 added to `prompts/` registry; `prompts/README.md` updated.

#### PHASE-D.5 -- Update memory-archive.ps1

Add Librarian Agent trigger to `scripts/memory-archive.ps1`:
```powershell
# After rotation, trigger Librarian Agent indexing
python src/calypso/librarian_agent.py --new-files $newFiles
```

**Validation:** `memory-archive.ps1` triggers indexing; Chroma collection updated.

#### PHASE-D.6 -- Retrospective Workflow Test

1. Run `scripts/memory-archive.ps1` (simulated sprint end)
2. Verify sprint log created in `archive-cold/sprint-logs/`
3. Verify Librarian Agent indexed new content
4. Run `memory:query("What was completed in the last sprint?")` via Roo Code
5. Verify relevant results returned

**Validation:** Full retrospective workflow completes without error.

#### PHASE-D.7 -- Update template/ with Global Brain Stubs

Add to `template/`:
- `mcp.json` updated with Chroma configuration
- `src/calypso/librarian_agent.py` stub (with TODO comments)
- Documentation in `template/docs/` about Global Brain setup

**Validation:** Template includes Global Brain configuration stubs.

#### PHASE-D.8 -- Commit and Push

```
git add .
git commit -m "feat(global-brain): PHASE-D complete -- Global Brain / Librarian Agent

- Chroma vector DB configured on Calypso (port 8002)
- src/calypso/librarian_agent.py: cold archive indexing
- fastmcp_server.py: memory:query tool implemented
- scripts/memory-archive.ps1: Librarian Agent trigger added
- SP-010 Librarian Agent added to prompts/
- Retrospective workflow test passed
- template/ updated with Global Brain stubs"
git push origin release/v2.0
```

### 6.3 Deliverables

- [ ] Chroma running on Calypso (port 8002)
- [ ] `src/calypso/librarian_agent.py` implemented
- [ ] `memory:query` MCP tool functional
- [ ] SP-010 Librarian Agent in `prompts/`
- [ ] `scripts/memory-archive.ps1` triggers indexing
- [ ] Retrospective workflow test passed
- [ ] `template/` updated with Global Brain stubs

---

## 7. PHASE-E: v2.0 Release Finalization

**Status: Pending**
**Prerequisite:** PHASE-D complete
**Estimated effort:** 1 session

### 7.1 Steps

#### PHASE-E.1 -- Freeze v2.0 Canonical Docs

Update status in all 5 v2.0 docs from `Draft` to `Frozen`:
- `docs/releases/v2.0/DOC-1-v2.0-PRD.md`
- `docs/releases/v2.0/DOC-2-v2.0-Architecture.md`
- `docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md`
- `docs/releases/v2.0/DOC-4-v2.0-Operations-Guide.md` (to be written)
- `docs/releases/v2.0/DOC-5-v2.0-Release-Notes.md` (to be written)

#### PHASE-E.2 -- Write DOC-4-v2.0-Operations-Guide.md

Document:
- How to run the Calypso pipeline (Phase 2-4)
- How to use the FastMCP server
- How to run `memory:archive` and `memory:query`
- How to deploy the workbench to a new project (updated `deploy-workbench-to-project.ps1`)
- Troubleshooting guide

#### PHASE-E.3 -- Write DOC-5-v2.0-Release-Notes.md

Document:
- What v2.0 delivered (all 4 phases)
- Known gaps and limitations
- Migration guide from v1.0
- What's next (v3.0 preview)

#### PHASE-E.4 -- Update docs/DOC-N-CURRENT.md Pointers

Update all 5 pointer files to reference v2.0:
```
docs/DOC-1-CURRENT.md -> docs/releases/v2.0/DOC-1-v2.0-PRD.md
docs/DOC-2-CURRENT.md -> docs/releases/v2.0/DOC-2-v2.0-Architecture.md
...
```

#### PHASE-E.5 -- Run Full QA Pass

- Verify all acceptance criteria in DOC-1 are met
- Run `check-prompts-sync.ps1` -- all PASS
- Run end-to-end pipeline test
- Write QA report to `docs/qa/v2.0/`

#### PHASE-E.6 -- Tag v2.0.0 and Push

```
git add .
git commit -m "docs(release): v2.0 release finalization -- freeze docs, QA pass, release notes"
git tag -a v2.0.0 -m "Release v2.0.0 -- Agentic Agile Workbench

What v2.0 delivers:
- PHASE-0: Release governance model
- PHASE-A: Hot/Cold memory architecture
- PHASE-B: Template folder enrichment
- PHASE-C: Calypso orchestration scripts (Phase 2-4 pipeline)
- PHASE-D: Global Brain / Librarian Agent"
git push origin release/v2.0
git push origin v2.0.0
```

### 7.2 Deliverables

- [ ] All 5 v2.0 docs frozen
- [ ] `docs/DOC-N-CURRENT.md` pointers updated to v2.0
- [ ] QA report in `docs/qa/v2.0/`
- [ ] Git tag `v2.0.0` pushed to origin

---

## 8. Dependencies and Sequencing Constraints

| Constraint | Description |
|-----------|-------------|
| PHASE-A before PHASE-B | Template must reflect new memory structure |
| PHASE-B before PHASE-C | Calypso scripts deposit output into local environment |
| PHASE-C before PHASE-D | Librarian Agent indexes cold archive populated by factory |
| PHASE-C.8 before PHASE-D.3 | `memory:query` tool is in `fastmcp_server.py` |
| SP-008 before PHASE-C.4 | Synthesizer Agent needed for Phase 3 |
| SP-009 before PHASE-C.5 | Devil's Advocate needed for Phase 4 |
| SP-010 before PHASE-D.2 | Librarian Agent system prompt needed |
| Chroma before PHASE-D.2 | Vector DB must be running before indexing |

---

## 9. Validation Criteria

### 9.1 PHASE-A Complete When:
- `memory-bank/hot-context/` exists with 5 files
- `memory-bank/archive-cold/` exists with subdirectory structure
- RULE 9 in `.clinerules`
- `scripts/memory-archive.ps1` runs without error
- All agents continue to function correctly

### 9.2 PHASE-B Complete When:
- `template/memory-bank/` has Hot/Cold structure
- `template/mcp.json` exists and is valid JSON
- `deploy-workbench-to-project.ps1` copies new files

### 9.3 PHASE-C Complete When:
- All 7 scripts implemented and tested
- End-to-end test: PRD in → `final_backlog.json` out
- `fastmcp_server.py` running and responding to MCP calls
- SP-008 and SP-009 in `prompts/` registry

### 9.4 PHASE-D Complete When:
- Chroma running on Calypso
- `memory:query` returns relevant results
- Retrospective workflow completes without error
- SP-010 in `prompts/` registry

### 9.5 v2.0 Release Complete When:
- All 5 canonical docs frozen
- All acceptance criteria in DOC-1 met
- `check-prompts-sync.ps1` all PASS
- Git tag `v2.0.0` pushed to origin

---

## 10. References

| Document | Location |
|----------|---------|
| DOC-1-v2.0-PRD.md | docs/releases/v2.0/DOC-1-v2.0-PRD.md |
| DOC-2-v2.0-Architecture.md | docs/releases/v2.0/DOC-2-v2.0-Architecture.md |
| IDEA-001 Hot/Cold Memory | docs/ideas/IDEA-001-hot-cold-memory.md |
| IDEA-002 Calypso Orchestration | docs/ideas/IDEA-002-calypso-orchestration.md |
| IDEA-006 Template Enrichment | docs/ideas/IDEAS-BACKLOG.md |
| IDEA-007 Global Brain | docs/ideas/IDEAS-BACKLOG.md |
| PLAN-release-governance.md | plans/governance/PLAN-release-governance.md |
| DOC6 Batch Review Results | plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md |
| DOC6 Batch Review Results 2 | plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md |
