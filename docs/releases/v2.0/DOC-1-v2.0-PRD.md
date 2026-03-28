---
doc_id: DOC-1
release: v2.0
status: Draft
title: Product Requirements Document
version: 0.1
date_created: 2026-03-28
date_frozen: TBD
authors: [Architect mode, Human]
previous_release: docs/releases/v1.0/DOC-1-v1.0-PRD.md
---

# DOC-1 -- Product Requirements Document (v2.0)

> **Status: DRAFT** -- This document is under active development on branch `release/v2.0`.
> It will be frozen when the v2.0 release is tagged.

---

## 1. Product Vision

### 1.1 What Is the Agentic Agile Workbench

The Agentic Agile Workbench is a **sovereign, local-first agentic development factory** that enables a single developer to operate a structured multi-agent software development pipeline from a Windows 11 laptop, using a combination of:

- A headless Linux GPU server (Calypso, RTX 5060 Ti 16GB) for local LLM inference via Ollama
- VS Code + Roo Code as the agentic execution engine
- A Gemini Chrome proxy for free cloud LLM access
- The Anthropic Claude API for full automation

The workbench is both a **product** (the factory itself) and a **template** (deployable to any application project).

### 1.2 v2.0 Vision Statement

> v2.0 transforms the workbench from a **manually-operated agentic environment** (v1.0) into a **semi-autonomous asynchronous factory** capable of running multi-agent analysis pipelines while the developer is disconnected.

The key capability added in v2.0 is the **Calypso Tier 2 orchestration layer**: a set of Python scripts that dispatch work to the Anthropic Batch API, collect expert committee reviews, synthesize a product backlog, and deposit the result into the local project environment -- all without requiring the developer to be present.

---

## 2. Stakeholders

| Role | Name | Responsibilities |
|------|------|-----------------|
| Product Owner | Human developer | Defines requirements, approves releases, arbitrates triage |
| Architect | Roo Code (Architect mode) | Designs system architecture, writes DOC-2 |
| Developer | Roo Code (Developer mode) | Implements features, writes code, commits |
| QA Engineer | Roo Code (QA mode) | Validates acceptance criteria, writes QA reports |
| Scrum Master | Roo Code (Scrum Master mode) | Sprint planning, process compliance |

---

## 3. Scope of v2.0

### 3.1 In Scope

| ID | Feature | Source | Phase |
|----|---------|--------|-------|
| REQ-2.1 | Release governance model (docs/ structure, RULE 8, template/docs/) | IDEA-003 | PHASE-0 |
| REQ-2.2 | Hot/Cold memory architecture (memory-bank/ restructure) | IDEA-001 | PHASE-A |
| REQ-2.3 | Template folder enrichment (memory-bank/ subdirs, mcp.json, .clinerules update) | IDEA-006 | PHASE-B |
| REQ-2.4 | Calypso orchestration scripts (Phase 2-4 pipeline, FastMCP server) | IDEA-002 | PHASE-C |
| REQ-2.5 | Global Brain / Librarian Agent (Chroma/Mem0, cross-project memory) | IDEA-007 | PHASE-D |

### 3.2 Out of Scope for v2.0

| Feature | Reason | Target |
|---------|--------|--------|
| Gherkin linter integration | Too complex, low ROI for v2.0 | v3.0 |
| Multi-developer collaboration | Single-developer workbench by design | v3.0 |
| Web UI for triage dashboard | CLI-first approach sufficient | v3.0 |
| CI/CD pipeline integration | Out of scope for local workbench | v3.0 |

### 3.3 Carried Over from v1.0 (Not Regressions)

All v1.0 features remain operational in v2.0:
- 3-mode LLM switcher (Ollama / Gemini proxy / Claude API)
- 4 Agile personas (.roomodes)
- Memory Bank + .clinerules (now 8 rules)
- Prompts registry (SP-001..007) + pre-commit hook
- Template folder + deployment script

---

## 4. Detailed Requirements

### 4.1 REQ-2.1 -- Release Governance Model

**Status:** IMPLEMENTED (PHASE-0 complete, commit 905d418)

**Description:** A universal governance model for managing project evolution, applicable to both the workbench and all application projects built with it.

**Acceptance Criteria:**
- [x] `docs/releases/vX.Y/` structure exists with 5 canonical docs per release
- [x] `docs/ideas/` with IDEAS-BACKLOG.md and IDEA-NNN.md files
- [x] `docs/conversations/` with README.md triage index
- [x] `docs/qa/vX.Y/` for QA reports per release
- [x] RULE 8 (Documentation Discipline) in `.clinerules`
- [x] SP-002 bumped to v2.3.0 with RULE 8 content
- [x] `template/docs/` structure for new projects
- [x] Git tags `v1.0.0-baseline` and `v1.0.0` created

---

### 4.2 REQ-2.2 -- Hot/Cold Memory Architecture

**Status:** Pending (PHASE-A)

**Description:** Restructure the flat `memory-bank/` (7 monolithic files) into a Hot/Cold architecture to prevent context explosion on large projects.

**Hot Zone** (read every session):
- `memory-bank/hot-context/activeContext.md`
- `memory-bank/hot-context/progress.md`
- `memory-bank/hot-context/decisionLog.md`
- `memory-bank/hot-context/systemPatterns.md`
- `memory-bank/hot-context/productContext.md`

**Cold Zone** (read via MCP semantic query only):
- `memory-bank/archive-cold/sprint-logs/` -- completed sprint logs
- `memory-bank/archive-cold/completed-tickets/` -- completed ticket history
- `memory-bank/archive-cold/productContext_Master.md` -- historical BDD accumulator

**Acceptance Criteria:**
- [ ] `memory-bank/hot-context/` directory created with 5 files migrated
- [ ] `memory-bank/archive-cold/` directory created with subdirectories
- [ ] `memory:archive` script rotates hot-context to cold archive at sprint end
- [ ] `.clinerules` updated with Cold Zone Firewall clause (agent reads cold archive via MCP only)
- [ ] `template/` updated with new memory-bank/ subdirectory structure
- [ ] All existing agents continue to function correctly with new structure

---

### 4.3 REQ-2.3 -- Template Folder Enrichment

**Status:** Pending (PHASE-B)

**Description:** Enrich the `template/` folder to include the Hot/Cold memory structure, an MCP configuration template, and updated `.clinerules` with Cold Zone Firewall.

**Acceptance Criteria:**
- [ ] `template/memory-bank/hot-context/` with 5 blank stub files
- [ ] `template/memory-bank/archive-cold/` with subdirectory structure
- [ ] `template/mcp.json` with Calypso FastMCP server entry (placeholder URL)
- [ ] `template/.clinerules` updated with Cold Zone Firewall clause
- [ ] `deploy-workbench-to-project.ps1` updated to copy new structure

---

### 4.4 REQ-2.4 -- Calypso Orchestration Scripts

**Status:** Pending (PHASE-C)

**Description:** Build the Calypso (Tier 2) orchestration layer for the multi-agent pipeline.

**Scripts to deliver:**

| Script | Purpose |
|--------|---------|
| `orchestrator_phase2.py` | Packages PRD into JSONL, dispatches to Anthropic Batch API (Committee of Experts) |
| `check_batch_status.py` | Polls Batch API, validates JSON schemas, saves consolidated expert reports |
| `orchestrator_phase3.py` | Runs Synthesizer Agent against expert reports + PRD, produces `draft_backlog.json` |
| `orchestrator_phase4.py` | Runs Devil's Advocate micro-loop (MAX_ATTEMPTS=2), produces `final_backlog.json` |
| `triage_dashboard.py` | Parses `final_backlog.json`, generates `triage_dashboard.md` for human arbitration |
| `apply_triage.py` | Reads human checkbox decisions, updates `systemPatterns.md`, populates `productContext.md` |
| `fastmcp_server.py` | FastMCP server exposing `launch_factory()`, `check_batch_status()`, `retrieve_backlog()` |

**Acceptance Criteria:**
- [ ] All 7 scripts implemented and tested end-to-end
- [ ] `orchestrator_phase2.py` successfully dispatches a batch job to Anthropic API
- [ ] `check_batch_status.py` correctly polls and retrieves batch results
- [ ] `orchestrator_phase3.py` produces a valid `draft_backlog.json`
- [ ] `orchestrator_phase4.py` produces a valid `final_backlog.json` with GREEN/ORANGE classification
- [ ] `triage_dashboard.py` produces a readable `triage_dashboard.md`
- [ ] `apply_triage.py` correctly updates `systemPatterns.md` and `productContext.md`
- [ ] `fastmcp_server.py` starts and responds to MCP tool calls from Roo Code
- [ ] `template/mcp.json` includes Calypso FastMCP server entry
- [ ] End-to-end test: PRD in → `final_backlog.json` out, no human intervention required

---

### 4.5 REQ-2.5 -- Global Brain / Librarian Agent

**Status:** Pending (PHASE-D)

**Description:** Implement a cross-project memory layer using a vector database (Chroma or Mem0) and a Librarian Agent that indexes completed project artifacts and answers semantic queries.

**Components:**
- Vector DB: Chroma (local) or Mem0 (cloud) -- TBD in DOC-2
- Librarian Agent: SP-010 system prompt, reads `archive-cold/` and indexes into vector DB
- MCP tool: `memory:query(semantic_query)` exposed via FastMCP server
- Retrospective trigger: Librarian Agent runs at sprint end after `memory:archive`

**Acceptance Criteria:**
- [ ] Vector DB installed and running on Calypso
- [ ] Librarian Agent (SP-010) implemented and tested
- [ ] `memory:query` MCP tool returns relevant results from cold archive
- [ ] Retrospective workflow: sprint end → archive → index → query available
- [ ] `template/` updated with Global Brain configuration stubs

---

## 5. Non-Functional Requirements

### 5.1 Sovereignty
- All LLM inference for development work must be possible locally (Ollama on Calypso)
- Cloud APIs (Anthropic, Gemini) are optional accelerators, not hard dependencies
- No data leaves the local network without explicit human action

### 5.2 Single-Developer Optimization
- All tooling optimized for a single developer workflow
- No multi-user authentication, no team collaboration features
- Context window management is critical -- Hot/Cold memory directly addresses this

### 5.3 Reproducibility
- Every release is fully reproducible from its Git tag
- No external state dependencies (no cloud databases required for core functionality)
- `deploy-workbench-to-project.ps1` must work on a fresh Windows 11 machine

### 5.4 Backward Compatibility
- v2.0 must not break any v1.0 workflow
- Existing `.roomodes`, `Modelfile`, `proxy.py` remain functional
- Memory bank migration (PHASE-A) must be non-destructive (old files preserved)

---

## 6. Glossary

| Term | Definition |
|------|-----------|
| Calypso | The headless Linux GPU server (RTX 5060 Ti 16GB) running Ollama |
| Hot Zone | Memory bank files read by the agent every session |
| Cold Zone | Memory bank archive files read only via MCP semantic query |
| Tier 2 | The Calypso orchestration layer (Python scripts running on the local machine) |
| Committee of Experts | The set of specialized agents dispatched via Anthropic Batch API in Phase 2 |
| Synthesizer Agent | The agent that consolidates expert reports into a draft backlog (Phase 3) |
| Devil's Advocate | The agent that challenges the draft backlog to produce a final backlog (Phase 4) |
| Librarian Agent | The agent that indexes cold archive into the vector DB and answers semantic queries |
| Global Brain | The cross-project memory layer (vector DB + Librarian Agent) |
| FastMCP | The MCP server framework used to expose Calypso tools to Roo Code |
| triage_dashboard.md | The human-readable output of Phase 4, used for arbitration |
| final_backlog.json | The machine-readable output of Phase 4, with GREEN/ORANGE classification |

---

## 7. References

| Document | Location |
|----------|---------|
| DOC-1-v1.0-PRD.md | docs/releases/v1.0/DOC-1-v1.0-PRD.md |
| DOC-2-v2.0-Architecture.md | docs/releases/v2.0/DOC-2-v2.0-Architecture.md |
| DOC-3-v2.0-Implementation-Plan.md | docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md |
| IDEA-001 Hot/Cold Memory | docs/ideas/IDEA-001-hot-cold-memory.md |
| IDEA-002 Calypso Orchestration | docs/ideas/IDEA-002-calypso-orchestration.md |
| IDEA-006 Template Enrichment | docs/ideas/IDEAS-BACKLOG.md |
| IDEA-007 Global Brain | docs/ideas/IDEAS-BACKLOG.md |
| PLAN-release-governance.md | plans/governance/PLAN-release-governance.md |
| DOC6 Batch Review Results | plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md |
| DOC6 Batch Review Results 2 | plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md |
