---
doc_id: DOC-1
release: v2.10
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-04-08
authors: [Architect mode, Human]
previous_release: v2.9
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.10)

> **Status: DRAFT** -- This document is under construction for v2.9 release.
> **Cumulative: YES** -- This document contains ALL requirements from v1.0 through v2.9.
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
11. [v2.8 Requirements](#11-v28-requirements)
12. [v2.9 Requirements](#12-v29-requirements-new)
13. [v2.10 Requirements](#13-v210-requirements-no-changes)

---

## 1. Context and Strategic Vision

This PRD synthesizes the complete requirements history of the Agentic Agile Workbench project, from initial vision through v2.9.

### 1.1 Project Overview

**Project Name:** Agentic Agile Workbench  
**Version:** v2.9 (Cumulative)  
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

### 1.6 Memory Bank Architecture

**Source:** [.clinerules](.clinerules:1) RULE 9, [v2.7 DOC-1 §1.6]

The Memory Bank uses a **Hot/Cold Architecture** with enforced firewall:

```
memory-bank/
├── hot-context/              ← Read directly at session start
│   ├── activeContext.md      (Current task state)
│   ├── progress.md           (Feature checklist)
│   ├── decisionLog.md         (ADRs - APPEND ONLY)
│   ├── systemPatterns.md      (Architecture conventions)
│   ├── productContext.md      (Business context)
│   └── session-checkpoint.md  (Crash recovery, 5-min heartbeat)
├── archive-cold/              ← MCP tool access ONLY
│   ├── completed-tickets/
│   └── sprint-logs/
└── batch_artifacts/           (Anthropic Batch API outputs)
```

**Critical:** Files in `archive-cold/` MUST NOT be read directly by the agent. Access via `memory:query` MCP tool or Librarian Agent (SP-010).

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
| REQ-3.3.1 | Heartbeat mechanism | 5-minute interval checkpoint updates |
| REQ-3.3.2 | Crash detection | Alert if last heartbeat > 30 minutes ago |
| REQ-3.3.3 | Session recovery | Continue from checkpoint or start fresh |

---

## 10. v2.7 Requirements

### 10.1 Hot/Cold Memory Architecture (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 9

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-3.4.1 | Hot/Cold separation | Active vs archived memory zones |
| REQ-3.4.2 | Cold archive MCP-only | Direct read of cold files forbidden |
| REQ-3.4.3 | Librarian Agent | SP-010 for vector DB indexing of cold archive |

### 10.2 Prompt Registry (v2.7)

**Source:** [prompts/README.md](prompts/README.md:1)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-4.1.1 | SP-001 to SP-006 | Git-synced prompts (.clinerules, .roomodes) |
| REQ-4.1.2 | SP-007 Gemini Gems | Manual deployment required |
| REQ-4.1.3 | SP-008 to SP-010 | Inline prompts in Calypso orchestration |

---

## 11. v2.8 Requirements

### 11.1 Source Attribution (v2.8)

**Source:** [PLAN-IDEA-020](plans/governance/PLAN-IDEA-020-deterministic-docs-from-sources.md)

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-5.1.1 | Deterministic docs | All canonical docs generated from source files |
| REQ-5.1.2 | Source citations | All sections cite source files with line references |
| REQ-5.1.3 | Mermaid diagrams | Architecture documents include visual diagrams |

### 11.2 Cumulative Documentation (v2.8)

**Source:** [.clinerules](.clinerules:1) RULE 12

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-5.2.1 | Self-contained docs | Each release doc contains complete history |
| REQ-5.2.2 | Line count minimums | DOC-1 ≥500, DOC-2 ≥500, DOC-3 ≥300, DOC-4 ≥300, DOC-5 ≥200 |
| REQ-5.2.3 | GitFlow enforcement | Feature branch required for doc modifications |

### 11.3 Governance Documentation (v2.8)

**Source:** [.clinerules](.clinerules:1) RULE 8

| ID | Requirement | Description |
|----|-------------|-------------|
| REQ-5.3.1 | The Two Spaces | Frozen (read-only) vs Draft/In Review (PO/Architect only) |
| REQ-5.3.2 | Idea Capture Mandate | New ideas → docs/ideas/IDEAS-BACKLOG.md |
| REQ-5.3.3 | Conversation Log | Save to docs/conversations/ with README entry |

---

## 12. v2.9 Requirements (NEW)

### 12.1 Documentation Maintenance (v2.9)

**Source:** [v2.7 DOC-1](docs/releases/v2.7/DOC-1-v2.7-PRD.md:1) (gap-fill)

This release focuses on documentation enrichment and clarification. The v2.8 content remains authoritative; v2.7 content is used only to fill gaps where v2.8 is silent.

**Enriched sections:**
- Section 1.6 (Memory Bank Architecture): Added complete directory structure with explicit file listing, derived from v2.7's more detailed representation.
- Source attribution consistency: All v2.8 sections maintain their source file citations; new gap-filled content also cites sources.

### 12.2 v2.9 Scope

| Area | Status | Source |
|------|--------|--------|
| Core architecture | Unchanged from v2.8 | v2.8 is authoritative |
| Proxy functionality | Unchanged from v2.8 | v2.8 is authoritative |
| Memory Bank structure | Clarified via v2.7 gap-fill | v2.7 §1.6 used |
| Prompt Registry | Clarified via v2.7 gap-fill | v2.7 §10.2 used |
| GitFlow rules | Unchanged from v2.8 | v2.8 is authoritative |

---

## 13. Calypso Orchestration Phases

### 13.1 Phase Overview

**Source:** [src/calypso/orchestrator_phase2.py](src/calypso/orchestrator_phase2.py:1)

| Phase | Input | Output | Agents |
|-------|-------|--------|--------|
| Phase 1 | Raw Idea | Structured IDEA | Human |
| Phase 2 | PRD | Expert Reports | 4 Batch Experts |
| Phase 3 | Expert Reports | Synthesized View | Synthesizer (SP-008) |
| Phase 4 | Synthesized | Challenges | Devil's Advocate (SP-009) |
| Phase 5 | Challenges | Refined Idea | Human |

### 13.2 Phase 2: Expert Batch Review

**Source:** [src/calypso/orchestrator_phase2.py](src/calypso/orchestrator_phase2.py:1)

---

## 14. Sync Detection System

### 14.1 Five Sync Categories

**Source:** [src/calypso/sync_detector.py](src/calypso/sync_detector.py:1)

| Category | Meaning | Action |
|----------|---------|--------|
| CONFLICT | Mutually exclusive changes | Human arbitration |
| REDUNDANCY | Same problem solved twice | Merge ideas |
| DEPENDENCY | B needs A first | Reorder, communicate |
| SHARED_LAYER | Same component touched | Coordinate timing |
| NO_OVERLAP | No conflicts | Proceed normally |

### 14.2 Sync Detection Flow

**Source:** [.clinerules](.clinerules:1) RULE 11

---

## 15. Release Governance

### 15.1 Pre-Release Freeze (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 14

| Day | Action |
|-----|--------|
| Day -5 | Scope freeze (all unrefined ideas deferred) |
| Day -4 | Documentation coherence (DOC-1..5 aligned) |
| Day -3 | Code coherence (all branches merged, full QA) |
| Day -2 | Dry run (RC1 tag, full test suite) |
| Day -1 | Final review (human approval, vX.Y.0 tag) |
| Day 0 | Announcement (DOC-5 published, GitHub release) |

### 15.2 Hotfix Priority (v2.7)

**Source:** [.clinerules](.clinerules:1) RULE 14

> A hotfix ALWAYS interrupts a planned release.

---

## 16. User Story Templates

### 16.1 Product Owner Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-001 | Product Owner | To capture ideas in IDEAs-BACKLOG | I can track all feature requests |
| US-002 | Product Owner | To refine ideas into requirements | The team has clear implementation targets |
| US-003 | Product Owner | To prioritize the backlog | The team works on highest value items first |

### 16.2 Scrum Master Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-004 | Scrum Master | To facilitate Agile ceremonies | The team follows Scrum practices |
| US-005 | Scrum Master | To update progress.md | Stakeholders see sprint status |
| US-006 | Scrum Master | To version the Memory Bank | All changes are traceable |

### 16.3 Developer Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-007 | Developer | To read the Memory Bank before coding | I have full context |
| US-008 | Developer | To switch between LLM backends | I can choose cost/privacy options |
| US-009 | Developer | To commit all changes to Git | No work is lost |

### 16.4 QA Engineer Stories

**Source:** [.roomodes](.roomodes:1)

| Story | As a... | I want... | So that... |
|-------|---------|-----------|------------|
| US-010 | QA Engineer | To design test plans | Quality is ensured |
| US-011 | QA Engineer | To write bug reports | Developers can reproduce issues |
| US-012 | QA Engineer | To run batch API tests | I can validate at scale |

---



---

## 13. v2.10 Requirements (No Changes)

> **Status:** No functional changes in v2.10

The v2.10 release focused on documentation governance improvements:
- **IDEA-021:** DOC-3 and DOC-5 became release-specific (not cumulative)
- **IDEA-022:** Added Chapter 11 (Ideation-to-Release Journey) to DOC-4

No new requirements in v2.10.

---

**End of DOC-1 Product Requirements Document (v2.10)**
