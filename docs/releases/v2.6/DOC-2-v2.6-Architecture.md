---
doc_id: DOC-2
release: v2.6
status: Draft
title: Technical Architecture
version: 1.0
date_created: 2026-04-01
authors: [Architect mode, Human]
previous_release: v2.5
cumulative: true
---

# DOC-2 — Technical Architecture (v2.6)

> **Status: DRAFT** -- This document is in draft for v2.6.0 release.
> **Cumulative: YES** -- This document contains all architecture from v1.0 through v2.6.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Principles](#2-architecture-principles)
3. [Memory Bank Architecture](#3-memory-bank-architecture)
4. [Session Checkpoint Architecture](#4-session-checkpoint-architecture)
5. [Artifact Identification Schema](#5-artifact-identification-schema)
6. [v2.6 Changes](#6-v26-changes)

---

## 1. System Overview

### 1.1 Core Components

| Component | Description |
|-----------|-------------|
| **Roo Code** | Central agentic execution engine |
| **Ollama** | Local LLM inference |
| **proxy.py** | Gemini Chrome proxy |
| **Memory Bank** | Persistent context storage |
| **Calypso** | Orchestration scripts (4-agent pipeline: intake → triage → refinement → execution) |
| **Anthropic Batch API** | Async batch processing for long-running audit tasks |

---

## 3. Memory Bank Architecture

### 3.1 Hot/Cold Separation

```
memory-bank/
├── hot-context/           # Read directly at session start
│   ├── activeContext.md   # Current task, session state
│   ├── progress.md       # Checkbox tracking
│   ├── decisionLog.md     # ADRs (APPEND ONLY!)
│   ├── systemPatterns.md  # Architecture conventions
│   ├── productContext.md  # Backlog, user stories
│   └── session-checkpoint.md  # CRASH RECOVERY
├── projectBrief.md        # Vision (root, rarely changes)
├── techContext.md         # Stack, commands (root)
├── archive-cold/          # MCP ONLY access
└── batch_artifacts/       # Anthropic Batch API outputs (BATCH-YYYY-MM-DD-NNNN.txt)
```

### 3.2 RULE MB-3: APPEND ONLY for ADRs

`decisionLog.md` is **APPEND ONLY**:
- Never overwrite existing ADRs
- Never delete entries
- Archive old entries to cold only when file > 500 lines

---

## 4. Session Checkpoint Architecture

### 4.1 Session Checkpoint File

Location: `memory-bank/hot-context/session-checkpoint.md`

### 4.2 Required Metadata

```yaml
---
artifact_id: CHECKPOINT-YYYY-MM-DD-NNN
session_id: sYYYY-MM-DD-{mode}-{NNN}
status: ACTIVE | CLOSED | CRASHED
created: YYYY-MM-DDTHH:MM:SSZ
modified: YYYY-MM-DDTHH:MM:SSZ
last_heartbeat: YYYY-MM-DDTHH:MM:SSZ
---
```

### 4.3 RULE MB-2: Session Checkpoint

Every 5 minutes during active work:
1. Update `session-checkpoint.md.last_heartbeat`
2. Update `session-checkpoint.md.git_state`
3. Update `session-checkpoint.md.current_task`

At session start:
- IF `session-checkpoint.last_heartbeat > 30 minutes`
- → Report crash detection
- → Offer recovery options

---

## 5. Artifact Identification Schema

### 5.1 Artifact ID Format Reference

| Artifact Type | ID Format | Example |
|--------------|-----------|---------|
| **Business Idea** | `IDEA-{YYYY-MM-DD}-{NNN}` | `IDEA-2026-04-01-001` |
| **Technical Suggestion** | `TECH-{YYYY-MM-DD}-{NNN}` | `TECH-2026-04-01-001` |
| **Architecture Decision** | `ADR-{YYYY-MM-DD}-{NNN}` | `ADR-2026-04-01-001` |
| **Session** | `s{YYYY-MM-DD}-{mode}-{NNN}` | `s2026-04-01-developer-001` |
| **Refinement Session** | `REF-{YYYY-MM-DD}-{NNN}` | `REF-2026-04-01-001` |
| **Conversation** | `{YYYY-MM-DD}-{source}-{slug}` | `2026-04-01-gemini-workbench` |
| **Batch Job** | `BATCH-{YYYY-MM-DD}-{NNNN}` | `BATCH-2026-04-01-0001` |
| **Expert Report** | `RPT-{YYYY-MM-DD}-{NNNN}` | `RPT-2026-04-01-0001` |
| **Enhancement** | `ENH-{YYYY-MM-DD}-{NNN}` | `ENH-2026-04-01-001` |

---

## 6. v2.6 Changes

### 6.1 New: Session Checkpoint

- New file: `memory-bank/hot-context/session-checkpoint.md`
- New script: `scripts/checkpoint_heartbeat.py`
- RULE MB-2: 5-minute heartbeat

### 6.2 New: APPEND ONLY for ADRs

- RULE MB-3: decisionLog.md is APPEND ONLY
- Existing ADRs never modified or deleted

### 6.3 New: Artifact ID Schema

- All artifacts use `TYPE-YYYY-MM-DD-NNN` format
- Session IDs: `sYYYY-MM-DD-{mode}-{NNN}`
- Enhancement IDs: `ENH-YYYY-MM-DD-NNN`

### 6.4 New: Plan-Branch Parity

- RULE G-0: Every plan creates a branch
- Branch preserved after merge
