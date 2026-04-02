---
doc_id: DOC-1
release: v2.8
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-04-02
authors: [Architect mode, Human]
previous_release: v2.7
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.8)

> **Status: DRAFT** -- This document is under construction for v2.8 release.
> **Cumulative: YES** -- This document contains ALL requirements from v1.0 through v2.8.
> To understand the complete project requirements, read this document from top to bottom.
> Each section represents a release version. Content grows cumulatively.

---

## Table of Contents

1. [Context and Strategic Vision](#1-context-and-strategic-vision)
2. [v1.0 Requirements](#2-v10-requirements)
3. [v2.0 Requirements](#3-v20-requirements)
4. [v2.1 Requirements](#4-v21-requirements)
5. [v2.2 Requirements](#5-v22-requirements)
6. [v2.3 Requirements](#6-v23-requirements)
7. [v2.4 Requirements](#7-v24-requirements)
8. [v2.5 Requirements](#8-v25-requirements)
9. [v2.6 Requirements](#9-v26-requirements)
10. [v2.7 Requirements](#10-v27-requirements)
11. [v2.8 Requirements](#11-v28-requirements-new)

---

## 1. Context and Strategic Vision

This PRD synthesizes the complete requirements history of the Agentic Agile Workbench project, from initial vision through v2.8.

### 1.1 Project Overview

**Project Name:** Agentic Agile Workbench  
**Version:** v2.8 (Cumulative)  
**Date:** 2026-04-02  
**Status:** Under Development

### 1.2 Core Inspiration Sources

1. **The LAAW Blueprint (mychen76)**: A local, sovereign agentic development environment, orchestrated by specialized AI agents with persistent memory and Agile rituals.

2. **The Gemini Chrome Proxy**: A network-clipboard bridge mechanism allowing Roo Code to leverage the power of Gemini Web for free via minimal human intervention (copy-paste).

### 1.3 Unified System Objective

The objective is to define a **unified and enriched** system that combines:
- Local sovereignty of LAAW with hybrid LLM backend flexibility
- Switchable LLM backends: local Ollama OR Gemini Chrome via proxy OR Claude Sonnet via direct API
- Agile rigor and contextual memory persistence
- Roo Code as central agentic execution engine

### 1.4 System Architecture Summary

| Component | Description |
|-----------|-------------|
| **Roo Code** | Central agentic execution engine (VS Code extension) |
| **Ollama** | Local LLM inference (calypso server via Tailscale) |
| **Gemini Chrome Proxy** | Network-clipboard bridge to Gemini Web |
| **Anthropic API** | Direct Claude Sonnet API access |
| **Memory Bank** | Persistent context across sessions (Git-versioned) |
| **Agile Personas** | RBAC-controlled role simulation |

### 1.5 Three LLM Backend Modes

| Mode | Provider | Cost | Human Intervention | Data Sovereignty |
|------|----------|------|---------------------|------------------|
| **Local Mode** | Ollama (Qwen3-14B) | Free | None | Total (100% local) |
| **Proxy Mode** | Gemini Chrome | Free | Copy-paste | Partial (Google) |
| **Cloud Mode** | Claude Sonnet | Paid | None | Partial (Anthropic) |

---

## 2. v1.0 Requirements

### 2.1 Foundational Requirement (REQ-000)

> **REQ-000 -- Root Requirement of the Unified System**
>
> The overall system must provide an operational agentic development environment on a Windows laptop (`pc`) with VS Code, relying on a dedicated headless Linux server (`calypso`) for local LLM inference, both machines connected via Tailscale. The system must be capable of:
> - Orchestrating specialized AI agents according to Agile roles (Product Owner, Scrum Master, QA Engineer, Developer)
> - Maintaining absolute context continuity between sessions via persistent memory in auditable Markdown files
> - Executing complex development tasks relying on a **switchable** LLM backend: either a local model (Ollama on `calypso` via Tailscale) for total sovereignty, or Gemini Chrome via a local API proxy for free cloud power, or Claude Sonnet via direct Anthropic API for full automation
> - Ensuring that Roo Code remains the central agentic execution engine in all three operating modes, without modification of its native behavior

### 2.2 Domain 1 — Agentic Engine & Foundation Models (REQ-1.x)

#### REQ-1.0 — Local LLM Inference Capability

The system must be capable of executing LLM inferences on the private local network (Tailscale), via Ollama installed on the Linux server `calypso` (RTX 5060 Ti 16 GB).

| ID | Requirement | Acceptance Criterion | Source |
|----|-------------|---------------------|--------|
| REQ-1.1 | Main model optimized for Tool Calling | `mychen76/qwen3_cline_roocode:14b` fine-tuned for Roo Code | [Modelfile](Modelfile:1) |
| REQ-1.2 | Minimum context window of 128K tokens | `num_ctx 131072` in Modelfile | [Modelfile](Modelfile:1) |
| REQ-1.3 | Inference determinism | `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` | [Modelfile](Modelfile:1) |

### 2.3 Domain 2 — Hybrid LLM Backend & Gemini Chrome Proxy (REQ-2.x)

#### REQ-2.0 — LLM Backend Switchability

The system must allow switching Roo Code's LLM backend between three modes by modifying only the "API Provider" parameter.

##### REQ-2.1 — Local Proxy Server (Interception)

| ID | Requirement | Acceptance Criterion | Source |
|----|-------------|---------------------|--------|
| REQ-2.1.1 | Local FastAPI server on localhost:8000 | `http://localhost:8000/health` returns HTTP 200 | [proxy.py](proxy.py:1) |
| REQ-2.1.2 | Exact emulation of OpenAI Chat Completions format | Roo Code connects without error | [proxy.py](proxy.py:1) |
| REQ-2.1.3 | Separate extraction of system/user/assistant prompts | Correct identification of message roles | [proxy.py](proxy.py:1) |
| REQ-2.1.4 | "Dedicated Gem" mode: system prompt filtering | `USE_GEM_MODE=true` omits system message | [proxy.py](proxy.py:1) |
| REQ-2.1.5 | Cleaning of base64 content (images) | Images replaced with `[IMAGE OMITTED]` | [proxy.py](proxy.py:1) |

##### REQ-2.2 — Clipboard Transfer (Uplink)

| ID | Requirement | Acceptance Criterion | Source |
|----|-------------|---------------------|--------|
| REQ-2.2.1 | Injection into Windows clipboard in <500ms | Clipboard available within 500ms | [proxy.py](proxy.py:1) |
| REQ-2.2.2 | Readable format with explicit separators | Human can identify sections in <5 seconds | [proxy.py](proxy.py:1) |
| REQ-2.2.3 | Timestamped console notification | Console shows time, size, actions, timeout | [proxy.py](proxy.py:1) |

##### REQ-2.3 — Response Wait and Capture (Downlink)

| ID | Requirement | Acceptance Criterion | Source |
|----|-------------|---------------------|--------|
| REQ-2.3.1 | Asynchronous clipboard polling every second | FastAPI still responds during polling | [proxy.py](proxy.py:1) |
| REQ-2.3.2 | Change detection by MD5 hash comparison | Detection within 2 seconds | [proxy.py](proxy.py:1) |
| REQ-2.3.3 | Configurable timeout with HTTP 408 response | HTTP 408 after TIMEOUT_SECONDS | [proxy.py](proxy.py:1) |
| REQ-2.3.4 | Validation of Roo Code XML tag presence | Warning if no XML tags found | [proxy.py](proxy.py:1) |

##### REQ-2.4 — Re-injection to Roo Code

| ID | Requirement | Acceptance Criterion | Source |
|----|-------------|---------------------|--------|
| REQ-2.4.1 | SSE streaming support in a single chunk | Streaming works without error | [proxy.py](proxy.py:1) |
| REQ-2.4.2 | Complete OpenAI JSON format for non-streamed response | JSON parseable by Roo Code | [proxy.py](proxy.py:1) |
| REQ-2.4.3 | HTTP 200 response with Content-Type application/json | Headers correct in both modes | [proxy.py](proxy.py:1) |
| REQ-2.4.4 | Complete preservation of Gemini content | Byte-for-byte identical content | [proxy.py](proxy.py:1) |

### 2.4 Domain 3 — Agility & Role Segregation (REQ-3.x)

#### REQ-3.0 — Four Agile Personas

The system must provide four distinct Agile personas, each with specific permissions and responsibilities.

| Persona | Role | Groups | Source |
|---------|------|--------|--------|
| product-owner | Define and prioritize backlog | read, edit (docs only) | [.roomodes](.roomodes:1) |
| scrum-master | Facilitate Agile ceremonies | read, edit, git commands | [.roomodes](.roomodes:1) |
| developer | Implement user stories | read, edit, browser, command, mcp | [.roomodes](.roomodes:1) |
| qa-engineer | Design and execute test plans | read, edit (qa only), test commands | [.roomodes](.roomodes:1) |

#### REQ-3.1 — Session Persistence

The system must maintain context continuity across sessions via Git-versioned Markdown files.

| File | Purpose | Source |
|------|---------|--------|
| `memory-bank/activeContext.md` | Current session state | [.clinerules](.clinerules:1) |
| `memory-bank/progress.md` | Feature checklist | [.clinerules](.clinerules:1) |
| `memory-bank/decisionLog.md` | Architecture decisions | [.clinerules](.clinerules:1) |

---

## 3. v2.0 Requirements

### 3.1 Proxy Mode Enhancements (v2.0)

**Source:** [proxy.py](proxy.py:1) v2.0.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.5.1 | Multi-line console output | FIX-001: Multi-line console with NEW CONVERSATION warning |
| REQ-2.5.2 | Clipboard exception handling | FIX-004: try/except around pyperclip.paste() |
| REQ-2.5.3 | Request counter | FIX-005: Counter to distinguish concurrent requests |
| REQ-2.5.4 | Minimum content length | FIX-006: Verify minimum content length |

### 3.2 History Management (v2.0)

**Source:** [proxy.py](proxy.py:1) v2.0.5

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.6.1 | Automatic history truncation | FIX-008: MAX_HISTORY_CHARS (40K default) |
| REQ-2.6.2 | Blocking length check | FIX-014: 100 char threshold blocks empty content |
| REQ-2.6.3 | Single message fallback | FIX-016: Truncate if single message exceeds limit |

---

## 4. v2.1 Requirements

### 4.1 Conversation Mode Fixes (v2.1)

**Source:** [proxy.py](proxy.py:1) v2.1.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.7.1 | Always new conversation | FIX-018: Remove "clear history" option, always fresh |
| REQ-2.7.2 | UTF-8 stdout on Windows | FIX-019: Force UTF-8 encoding on Windows (cp1252 issue) |

---

## 5. v2.2 Requirements

### 5.1 XML Validation (v2.2)

**Source:** [proxy.py](proxy.py:1) v2.2.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.8.1 | XML tag blocking validation | FIX-020: Gemini text blocked if contains XML-like tags |
| REQ-2.8.2 | Escaped tag detection | FIX-021: Detect escaped XML tags (markdown escaping) |

---

## 6. v2.3 Requirements

### 6.1 GEM MODE Refinements (v2.3)

**Source:** [proxy.py](proxy.py:1) v2.3.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.9.1 | Single-message GEM mode | FIX-022: GEM MODE sends only last user message |
| REQ-2.9.2 | Injection tag stripping | FIX-023: Remove `<environment_details>`, `<SYSTEM>`, `<task>`, `<feedback>` |

### 6.2 User Message Extraction (v2.3)

**Source:** [proxy.py](proxy.py:1) v2.4.0/v2.5.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.10.1 | Extract pure user text | FIX-024: Extract before first injected tag |
| REQ-2.10.2 | User message wrapper | FIX-026: `<user_message>` in role='tool' is the real message |

---

## 7. v2.4 Requirements

### 7.1 Message Format Corrections (v2.4)

**Source:** [proxy.py](proxy.py:1) v2.5.1/v2.6.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.11.1 | Correct Roo Code structure | FIX-026: user in role='tool' inside `<user_message>` |
| REQ-2.11.2 | Runtime lock preservation | FIX-015: Keep `<new_task>` runtime lock in wait |

---

## 8. v2.5 Requirements

### 8.1 Response Processing (v2.5)

**Source:** [proxy.py](proxy.py:1) v2.7.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.12.1 | Markdown unescaping | FIX-027: Auto-unescape `\<tag\>` from Gemini copy button |
| REQ-2.12.2 | Asyncio clipboard lock | FIX-017: asyncio.Lock() for clipboard serialization |

### 8.2 SSE Streaming Fix (v2.5)

**Source:** [proxy.py](proxy.py:1) v2.8.0

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-2.13.1 | Correct SSE format | FIX-028: Separate chunks for role, content, finish_reason |

---

## 9. v2.6 Requirements

### 9.1 Batch API Toolkit (v2.6)

**Source:** [scripts/batch/](scripts/batch:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-3.2.1 | Batch CLI tool | CLI for submitting Anthropic Batch jobs |
| REQ-3.2.2 | Batch polling | Poll batch status until complete |
| REQ-3.2.3 | Batch retrieval | Retrieve results from completed batches |
| REQ-3.2.4 | Jinja2 templates | Script generation via templates |

### 9.2 Session Checkpoint (v2.6)

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-3.3.1 | Session checkpoint | Write state to session-checkpoint.md |
| REQ-3.3.2 | 5-minute heartbeat | Validate session is alive |
| REQ-3.3.3 | Crash detection | 30-minute threshold triggers recovery |

---

## 10. v2.7 Requirements

### 10.1 Canonical Documentation (v2.7)

**Source:** [.githooks/pre-receive](.githooks/pre-receive:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-4.1.1 | Cumulative docs | All 5 DOCs contain full history (not delta) |
| REQ-4.1.2 | Line count minimums | DOC-1/2 ≥500, DOC-3/4 ≥300, DOC-5 ≥200 |
| REQ-4.1.3 | Feature branch required | Canonical doc changes via feature branches only |
| REQ-4.1.4 | Pointer consistency | DOC-*-CURRENT.md all point to same release |

### 10.2 Prompt Registry (v2.7)

**Source:** [prompts/README.md](prompts/README.md:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-4.2.1 | 10 system prompts | SP-001 through SP-010 |
| REQ-4.2.2 | Deployment tracking | SP-007 requires manual Gemini deployment |
| REQ-4.2.3 | Version tracking | Each SP has version field |

### 10.3 Memory Bank Enhancement (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 9

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-4.3.1 | Hot/Cold firewall | Hot zone read directly, cold zone via MCP only |
| REQ-4.3.2 | Librarian Agent | SP-010 for cold archive access |

---

## 11. v2.8 Requirements (NEW)

### 11.1 Source Attribution (IDEA-020)

**Source:** [PLAN-IDEA-020](plans/governance/PLAN-IDEA-020-deterministic-docs-from-sources.md)

All canonical docs must attribute content to specific source files.

| ID | Requirement | Description | Source |
|----|-------------|-------------|--------|
| REQ-5.1.1 | Deterministic generation | Docs built from 18 source files | PLAN-IDEA-020 |
| REQ-5.1.2 | Source reference | Every section cites source file and line | PLAN-IDEA-020 |
| REQ-5.1.3 | Mermaid diagrams | ≥3 architecture diagrams per DOC-2 | IDEA-016 |

### 11.2 Idea Intake Protocol (IDEA-020)

**Source:** [.clinerules](.clinerules:1) RULE 13

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-5.2.1 | Off-topic detection | Human remarks outside current task → Orchestrator |
| REQ-5.2.2 | Idea classification | BUSINESS (What) vs TECHNICAL (How) |
| REQ-5.2.3 | Intake routing | Orchestrator assigns IDEA/TECH ID |
| REQ-5.2.4 | Sync detection | Check for overlap with active branches |

### 11.3 Synchronization Awareness (IDEA-020)

**Source:** [.clinerules](.clinerules:1) RULE 11

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-5.3.1 | Pre-implementation check | Read DOC-3 for active branch overlap |
| REQ-5.3.2 | 5 sync categories | CONFLICT, REDUNDANCY, DEPENDENCY, SHARED_LAYER, NO_OVERLAP |
| REQ-5.3.3 | Conflict notification | Inform human if overlap detected |

### 11.4 Execution Tracking (IDEA-020)

**Source:** [.clinerules](.clinerules:1) RULE 14

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-5.4.1 | Live DOC-3 | Execution chapter updated continuously |
| REQ-5.4.2 | Three-way consistency | DOC-3, progress.md, EXECUTION-TRACKER in sync |
| REQ-5.4.3 | Session logging | EXECUTION-TRACKER entry per session |

---

## Appendix A: Idea Intake Routing

### A.1 Intake Flow

**Source:** [.clinerules](.clinerules:1) RULE 13

```
Human Input → Agent (any mode)
                ↓
         Off-topic?
                ↓ Yes
         Route to Orchestrator
                ↓
         IDEAs-BACKLOG (BUSINESS)
         or
         TECH-SUGGESTIONS-BACKLOG (TECHNICAL)
                ↓
         Human chooses: [Refine Now] [Park for Later] [Sync First]
```

### A.2 Idea Classification

| Type | Scope | Backlog |
|------|-------|---------|
| BUSINESS | What the user needs | IDEAS-BACKLOG |
| TECHNICAL | How to implement | TECH-SUGGESTIONS-BACKLOG |

---

## Appendix B: Non-Functional Requirements Summary

### B.1 Performance

**Source:** [Modelfile](Modelfile:1)

| Metric | Target | Source |
|--------|--------|--------|
| Context Window | 128K tokens | num_ctx 131072 |
| Temperature | 0.15 (deterministic) | temperature 0.15 |
| Clipboard Latency | <500ms | REQ-2.2.1 |

### B.2 Dependencies

**Source:** [requirements.txt](requirements.txt:1)

| Package | Version | Purpose |
|---------|---------|---------|
| anthropic | >=0.49.0 | Claude API client |
| fastmcp | >=2.0.0 | MCP protocol |
| chromadb | >=0.6.0 | Vector database |
| fastapi | 0.135.2 | Web framework |
| uvicorn | 0.42.0 | ASGI server |
| pyperclip | 1.11.0 | Clipboard access |

---

## 12. v2.1 Requirements

### 12.1 Memory Bank Session Protocol (v2.1)

**Source:** [.clinerules](.clinerules:1) RULE 1-3

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-6.1.1 | CHECK→CREATE→READ→ACT | Mandatory session start protocol |
| REQ-6.1.2 | Active context creation | Create activeContext.md if absent |
| REQ-6.1.3 | Progress tracking | Update progress.md with feature checklist |
| REQ-6.1.4 | Decision logging | Log architecture decisions to decisionLog.md |

### 12.2 Git Versioning Requirements (v2.1)

**Source:** [.clinerules](.clinerules:1) RULE 5

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-6.2.1 | Everything versioned | src/, proxy.py, scripts/, prompts/, memory-bank/ |
| REQ-6.2.2 | Conventional commits | feat, fix, docs, chore, refactor, test prefixes |
| REQ-6.2.3 | Commit triggers | After code/modification, Memory Bank update, prompt modification |

---

## 13. v2.2 Requirements

### 13.1 Deployment Model (v2.2)

**Source:** [deploy-workbench-to-project.ps1](deploy-workbench-to-project.ps1:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-7.1.1 | Template deployment | Copy template/ to target projects |
| REQ-7.1.2 | Update mode | Sync existing projects with -Update flag |
| REQ-7.1.3 | Version tracking | Write .workbench-version to target |

### 13.2 Files Deployed (v2.2)

**Source:** [deploy-workbench-to-project.ps1](deploy-workbench-to-project.ps1:1)

| Category | Files/Folders |
|----------|---------------|
| Config Files | .roomodes, .clinerules, .workbench-version, Modelfile, proxy.py, requirements.txt, mcp.json |
| Folders | prompts/, scripts/, docs/, memory-bank/, .githooks/, .github/ |

---

## 14. v2.3 Requirements

### 14.1 System Prompt Registry (v2.3)

**Source:** [prompts/README.md](prompts/README.md:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-8.1.1 | Single source of truth | All system prompts in prompts/ directory |
| REQ-8.1.2 | SP modification procedure | Modify canonical SP-XXX, propagate to target, commit |
| REQ-8.1.3 | Version increment | Each SP has version field, increment on change |

### 14.2 Prompt Inventory (v2.3)

**Source:** [prompts/README.md](prompts/README.md:1)

| SP | Name | Target | Deployment |
|----|------|--------|------------|
| SP-001 | Ollama Modelfile | Modelfile SYSTEM | Git-synced |
| SP-002 | Global Directives | .clinerules | rebuild_sp002.py |
| SP-003 | Product Owner | .roomodes[0] | Git-synced |
| SP-004 | Scrum Master | .roomodes[1] | Git-synced |
| SP-005 | Developer | .roomodes[2] | Git-synced |
| SP-006 | QA Engineer | .roomodes[3] | Git-synced |
| SP-007 | Gem Gemini | Gemini Gems | **Manual** |
| SP-008 | Synthesizer | orchestrator_phase3.py | Inline |
| SP-009 | Devil's Advocate | orchestrator_phase4.py | Inline |
| SP-010 | Librarian | librarian_agent.py | Inline |

---

## 15. v2.4 Requirements

### 15.1 LLM Backend Modes (v2.4)

**Source:** [Modelfile](Modelfile:1), [proxy.py](proxy.py:1)

| Mode | Provider | Format | Human Intervention | Source |
|------|----------|--------|---------------------|--------|
| LOCAL | Ollama (Qwen3-14B) | OpenAI-compatible | None | Modelfile |
| PROXY | Gemini Chrome | Clipboard bridge | Copy/paste | proxy.py |
| CLOUD | Claude Sonnet | Direct API | None | requirements.txt |

### 15.2 Ollama Configuration (v2.4)

**Source:** [Modelfile](Modelfile:1)

```
PARAMETER temperature 0.15     # Anti-hallucination
PARAMETER min_p 0.03          # Minimum probability
PARAMETER top_p 0.95          # Nucleus sampling
PARAMETER repeat_penalty 1.1  # Repetition penalty
PARAMETER num_ctx 131072      # 128K context window
PARAMETER num_gpu 99          # Max GPU usage
PARAMETER num_thread 8        # CPU threads
```

---

## 16. v2.5 Requirements

### 16.1 Batch API Toolkit (v2.5)

**Source:** [scripts/batch/](scripts/batch:1)

| Script | Purpose |
|--------|---------|
| cli.py | Main entry point for batch operations |
| submit.py | Submit batch jobs to Anthropic API |
| poll.py | Poll batch job status |
| retrieve.py | Retrieve batch results |
| generate.py | Generate batch submission scripts |
| config.py | Configuration management |

### 16.2 Batch Template Engine (v2.5)

**Source:** [scripts/batch/templates/](scripts/batch/templates:1)

| Template | Purpose |
|----------|---------|
| batch_submit_script.py.j2 | Jinja2 template for batch submission |
| batch_retrieve_script.py.j2 | Jinja2 template for result retrieval |

---

## 17. v2.6 Requirements

### 17.1 Git Infrastructure (v2.6)

**Source:** [.githooks/pre-commit](.githooks/pre-commit:1)

| Hook | Purpose | Trigger |
|------|---------|---------|
| pre-commit | Run check-prompts-sync.ps1 | git commit |

**Source:** [.githooks/pre-receive](.githooks/pre-receive:1)

| Check | Purpose |
|-------|---------|
| Feature branch required | Canonical docs must be on feature branch |
| Cumulative line count | DOC-1 ≥500, DOC-2 ≥500, DOC-3 ≥300, DOC-4 ≥300, DOC-5 ≥200 |

### 17.2 CI/CD Pipeline (v2.6)

**Source:** [.github/workflows/canonical-docs-check.yml](.github/workflows/canonical-docs-check.yml:1)

| Validation | Purpose |
|------------|---------|
| Pointer consistency | All DOC-*-CURRENT.md point to same release |
| Cumulative nature | Docs contain full history |
| Front matter flags | cumulative: true, status, version |

---

## 18. v2.7 Requirements

### 18.1 Hot/Cold Memory Architecture (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 9

### 18.2 Librarian Agent (v2.7)

**Source:** [src/calypso/librarian_agent.py](src/calypso/librarian_agent.py:1)

| Capability | Description |
|------------|-------------|
| SP-010 | Vector DB indexing of cold archive |
| Semantic search | Query across historical decisions |
| Cold archive access | MCP-only access (no direct read) |

---

## 19. Calypso Orchestration Phases

### 19.1 Phase Overview

**Source:** [src/calypso/orchestrator_phase2.py](src/calypso/orchestrator_phase2.py:1)

| Phase | Input | Output | Agents |
|-------|-------|--------|--------|
| Phase 1 | Raw Idea | Structured IDEA | Human |
| Phase 2 | PRD | Expert Reports | 4 Batch Experts |
| Phase 3 | Expert Reports | Synthesized View | Synthesizer (SP-008) |
| Phase 4 | Synthesized | Challenges | Devil's Advocate (SP-009) |
| Phase 5 | Challenges | Refined Idea | Human |

### 19.2 Phase 2: Expert Batch Review

**Source:** [src/calypso/orchestrator_phase2.py](src/calypso/orchestrator_phase2.py:1)

---

## 20. Sync Detection System

### 20.1 Five Sync Categories

**Source:** [src/calypso/sync_detector.py](src/calypso/sync_detector.py:1)

| Category | Meaning | Action |
|----------|---------|--------|
| CONFLICT | Mutually exclusive changes | Human arbitration |
| REDUNDANCY | Same problem solved twice | Merge ideas |
| DEPENDENCY | B needs A first | Reorder, communicate |
| SHARED_LAYER | Same component touched | Coordinate timing |
| NO_OVERLAP | No conflicts | Proceed normally |

### 20.2 Sync Detection Flow

**Source:** [.clinerules](.clinerules:1) RULE 11

---

## 21. Release Governance

### 21.1 Pre-Release Freeze (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 14

| Day | Action |
|-----|--------|
| Day -5 | Scope freeze (all unrefined ideas deferred) |
| Day -4 | Documentation coherence (DOC-1..5 aligned) |
| Day -3 | Code coherence (all branches merged, full QA) |
| Day -2 | Dry run (RC1 tag, full test suite) |
| Day -1 | Final review (human approval, vX.Y.0 tag) |
| Day 0 | Announcement (DOC-5 published, GitHub release) |

### 21.2 Hotfix Priority (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 14

> A hotfix ALWAYS interrupts a planned release.

---

## 22. User Story Templates

### 22.1 Product Owner Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-001 | Product Owner | To capture ideas in IDEAs-BACKLOG | I can track all feature requests |
| US-002 | Product Owner | To refine ideas into requirements | The team has clear implementation targets |
| US-003 | Product Owner | To prioritize the backlog | The team works on highest value items first |

### 22.2 Scrum Master Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-004 | Scrum Master | To facilitate Agile ceremonies | The team follows Scrum practices |
| US-005 | Scrum Master | To update progress.md | Stakeholders see sprint status |
| US-006 | Scrum Master | To version the Memory Bank | All changes are traceable |

### 22.3 Developer Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-007 | Developer | To read the Memory Bank before coding | I have full context |
| US-008 | Developer | To switch between LLM backends | I can choose cost/privacy options |
| US-009 | Developer | To commit all changes to Git | No work is lost |

### 22.4 QA Engineer Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-010 | QA Engineer | To design test plans | Quality is ensured |
| US-011 | QA Engineer | To write bug reports | Developers can reproduce issues |
| US-012 | QA Engineer | To run batch API tests | I can validate at scale |

---

**End of DOC-1 Product Requirements Document (v2.8)**
