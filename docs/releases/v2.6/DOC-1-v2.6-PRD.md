---
doc_id: DOC-1
release: v2.6
status: Frozen
title: Product Requirements Document
version: 1.0
date_created: 2026-04-01
authors: [Architect mode, Human]
previous_release: v2.5
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.6)

> **Status: FROZEN** -- This document was frozen after QA approval and v2.6.0 release audit.
> **Cumulative: YES** -- This document contains all requirements from v1.0 through v2.6.
> To understand the full project requirements, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [Context and Strategic Vision](#1-context-and-strategic-vision)
2. [v1.0 Requirements](#2-v10-requirements)
3. [v2.1 Requirements](#3-v21-requirements)
4. [v2.2 Requirements](#4-v22-requirements)
5. [v2.3 Requirements](#5-v23-requirements)
6. [v2.4 Requirements](#6-v24-requirements)
7. [v2.5 Requirements](#7-v25-requirements)
8. [v2.6 Requirements](#8-v26-requirements)
9. [All Previous Workflows Preserved](#9-all-previous-workflows-preserved)

---

## 1. Context and Strategic Vision

This PRD synthesizes two complementary sources of inspiration:

1. **The LAAW Blueprint (mychen76)**: A local, sovereign agentic development environment, orchestrated by specialized AI agents with persistent memory and Agile rituals.
2. **The Gemini Chrome Proxy**: A network-clipboard bridge mechanism allowing Roo Code to leverage the power of Gemini Web for free via minimal human intervention (copy-paste).

The objective is to define a **unified and enriched** system that combines the local sovereignty of LAAW with the flexibility of a hybrid LLM backend (local Ollama OR Gemini Chrome via proxy OR Claude Sonnet via direct API), while maintaining Agile rigor and contextual memory persistence.

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

---

## 8. v2.6 Requirements

### 8.1 Memory Bank Enhancement (REQ-MB-1)

#### REQ-MB-1.1 -- Session Checkpoint (RULE MB-2)

The system must provide a crash recovery mechanism through a session checkpoint file.

| ID | Requirement | Acceptance Criterion |
|----|-------------|----------------------|
| REQ-MB-1.1 | Session checkpoint file in hot-context | `memory-bank/hot-context/session-checkpoint.md` exists and contains session metadata |
| REQ-MB-1.2 | Heartbeat every 5 minutes | `checkpoint_heartbeat.py` writes to session-checkpoint.md every 5 minutes |
| REQ-MB-1.3 | Crash detection | If last_heartbeat > 30 minutes, detect as potential crash |

#### REQ-MB-1.2 -- APPEND ONLY for ADRs (RULE MB-3)

The system must enforce APPEND ONLY discipline for the decision log.

| ID | Requirement | Acceptance Criterion |
|----|-------------|----------------------|
| REQ-MB-1.4 | decisionLog.md is APPEND ONLY | New ADRs are appended, existing ADRs are never edited or deleted |

### 8.2 Artifact Identification Schema

#### REQ-AI-1 -- Dated Artifact IDs

All artifacts must carry date-based sequential IDs.

| ID | Requirement | Format | Example |
|----|-------------|--------|---------|
| REQ-AI-1.1 | Business ideas | `IDEA-YYYY-MM-DD-NNN` | `IDEA-2026-04-01-001` |
| REQ-AI-1.2 | Technical suggestions | `TECH-YYYY-MM-DD-NNN` | `TECH-2026-04-01-001` |
| REQ-AI-1.3 | Architecture decisions | `ADR-YYYY-MM-DD-NNN` | `ADR-2026-04-01-001` |
| REQ-AI-1.4 | Sessions | `sYYYY-MM-DD-{mode}-{NNN}` | `s2026-04-01-developer-001` |
| REQ-AI-1.5 | Enhancements | `ENH-YYYY-MM-DD-NNN` | `ENH-2026-04-01-001` |

### 8.3 Plan-Branch Parity (RULE G-0)

#### REQ-PB-1 -- Every Plan Creates a Branch

The system must enforce that every plan execution creates a dedicated branch.

| ID | Requirement | Acceptance Criterion |
|----|-------------|----------------------|
| REQ-PB-1.1 | Branch naming | `governance/PLAN-{ID}-{slug}` |
| REQ-PB-1.2 | Branch preserved | Branches are never deleted after merge |
| REQ-PB-1.3 | PR to target | PRs merge to `develop` or `develop-vX.Y` |

### 8.4 Deferred Enhancement Tracking (RULE D-1)

#### REQ-DE-1 -- Future Items Are Tracked

The system must formally track future enhancements so they are never forgotten.

| ID | Requirement | Acceptance Criterion |
|----|-------------|----------------------|
| REQ-DE-1.1 | ENH IDs | Future items get `ENH-YYYY-MM-DD-NNN` IDs |
| REQ-DE-1.2 | Status tracking | DEFERRED → IN_PROGRESS → COMPLETED |
| REQ-DE-1.3 | Target version | Every enhancement has a target_version |
