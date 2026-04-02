---
doc_id: DOC-4
release: v2.8
status: Draft
title: Operations Guide
version: 1.0
date_created: 2026-04-02
authors: [Developer mode, Human]
previous_release: v2.7
cumulative: true
---

# DOC-4 — Operations Guide (v2.8)

> **Status: DRAFT** -- This document is in draft for v2.8.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all operations guidance from v1.0 through v2.8.
> To understand the full project operations history, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [Workbench Deployment Guide](#1-workbench-deployment-guide)
2. [Session Checkpoint Operations](#2-session-checkpoint-operations)
3. [Heartbeat Script Usage](#3-heartbeat-script-usage)
4. [ADR Management](#4-adr-management)
5. [Artifact ID Generation](#5-artifact-id-generation)
6. [Canonical Docs Operations](#6-canonical-docs-operations)
7. [Prompt Registry Operations](#7-prompt-registry-operations)
8. [Script Reference](#8-script-reference)
9. [Troubleshooting Guide](#9-troubleshooting-guide)

---

## 1. Workbench Deployment Guide

### 1.1 Understanding What This Repository Is (and Is Not)

**Source:** [PLAN-IDEA-020](plans/governance/PLAN-IDEA-020-deterministic-docs-from-sources.md)

```
agentic-agile-workbench/   ← YOU ARE HERE
│                                     This is the WORKBENCH
│
│  docs/           ← The workbench documentation (DOC1-5)
│  prompts/        ← The workbench tools (system prompts SP-001 to SP-010)
│  proxy.py        ← A workbench machine (Roo Code <-> Gemini Chrome bridge)
│  .roomodes       ← The workbench worker roles (4 Agile personas)
│  .clinerules     ← The workbench rulebook (15 mandatory rules)
│  scripts/        ← The workbench utility scripts
│
└── It produces PROJECTS (separate repositories, in other folders)
```

**This repository contains no application code.** It contains the rules, tools, processes and system prompts that enable developing any project in an agentic, agile and versioned manner.

### 1.2 Deployment Checklist

**Source:** [deploy-workbench-to-project.ps1](deploy-workbench-to-project.ps1:1)

| Step | Action | Verification | Source |
|------|--------|--------------|--------|
| 1 | Clone repository to local machine | `git clone <repo-url>` | External |
| 2 | Install Python 3.10+ dependencies | `pip install -r requirements.txt` | [requirements.txt](requirements.txt:1) |
| 3 | Copy template to new project | `.\deploy-workbench-to-project.ps1 -ProjectPath ./my-project` | [deploy-workbench-to-project.ps1](deploy-workbench-to-project.ps1:1) |
| 4 | Initialize Git in target project | `cd ./my-project && git init` | External |
| 5 | Configure Roo Code in VS Code | Install Roo Code extension, configure API provider | External |
| 6 | Verify Memory Bank structure | `ls memory-bank/hot-context/` shows 6 files | [.clinerules](.clinerules:1) |
| 7 | Test pre-commit hook | `git commit` triggers prompt sync check | [.githooks/pre-commit](.githooks/pre-commit:1) |

### 1.3 Deployment Parameters

**Source:** [deploy-workbench-to-project.ps1](deploy-workbench-to-project.ps1:1)

```powershell
# Initial deployment
.\deploy-workbench-to-project.ps1 -ProjectPath "C:\path\to\my-project"

# Update existing deployment
.\deploy-workbench-to-project.ps1 -ProjectPath "C:\path\to\my-project" -Update

# Dry run (simulation)
.\deploy-workbench-to-project.ps1 -ProjectPath "C:\path\to\my-project" -DryRun
```

### 1.4 Files Deployed to Target Project

**Source:** [deploy-workbench-to-project.ps1](deploy-workbench-to-project.ps1:1)

**7 Configuration Files:**
- `.roomodes` — 4 Agile personas
- `.clinerules` — 15 mandatory rules
- `.workbench-version` — Version marker
- `Modelfile` — Ollama configuration
- `proxy.py` — Clipboard proxy v2.8.0
- `requirements.txt` — Python dependencies
- `mcp.json` — Calypso MCP server config

**6 Folders:**
- `prompts/` — System prompt registry
- `scripts/` — Utility scripts
- `docs/` — Canonical documentation stubs
- `memory-bank/` — Hot-cold memory structure
- `.githooks/` — Git hooks for validation
- `.github/` — CI/CD workflows

---

## 2. Session Checkpoint Operations

### 2.1 Starting a Session

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

At session start, the agent MUST:
1. Read `memory-bank/hot-context/session-checkpoint.md`
2. Check `last_heartbeat` timestamp
3. If `last_heartbeat > 30 minutes`, report crash detection
4. Offer recovery options: continue from checkpoint or start fresh

### 2.2 Crash Detection Logic

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

```
IF session-checkpoint.last_heartbeat > NOW - 30 minutes:
    → Session is ACTIVE
ELSE:
    → Session was INTERRUPTED
    → Report: "Crash detected. Last heartbeat X minutes ago."
    → Offer: [Continue] [Start Fresh]
```

### 2.3 Session ID Format

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

Sessions use the format: `s{YYYY-MM-DD}-{mode}-{NNN}`

Examples:
- `s2026-04-02-developer-001`
- `s2026-04-02-scrum-master-002`
- `s2026-04-02-qa-engineer-001`

### 2.4 Session Checkpoint Content

**Source:** [memory-bank/hot-context/session-checkpoint.md](memory-bank/hot-context/session-checkpoint.md)

```markdown
---
session_id: s2026-04-02-developer-001
last_heartbeat: 2026-04-02T10:30:00Z
mode: developer
branch: feature/my-feature
task: Implementing feature X
status: ACTIVE | INTERRUPTED
---
```

---

## 3. Heartbeat Script Usage

### 3.1 Heartbeat Mechanism

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

The heartbeat script runs every 5 minutes to validate the session is alive:

```
┌─────────────────────────────────────────────────────┐
│                   Agent Session                       │
│                                                       │
│  Session Start ──► [Do Work] ──► Heartbeat (5min)  │
│                         │                    │        │
│                         │                    ▼        │
│                         │            Update checkpoint│
│                         │                    │        │
│                         ▼                    ▼        │
│                    [Continue] ◄───── Session Valid?  │
└─────────────────────────────────────────────────────┘
```

### 3.2 Running the Heartbeat

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

```bash
# Run heartbeat once
python scripts/checkpoint_heartbeat.py

# Run heartbeat continuously (every 5 minutes)
python scripts/checkpoint_heartbeat.py --continuous

# Custom interval (in seconds)
python scripts/checkpoint_heartbeat.py --interval 300
```

### 3.3 Heartbeat Exit Codes

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

| Code | Meaning |
|------|---------|
| 0 | Heartbeat recorded successfully |
| 1 | Error: Session checkpoint not found |
| 2 | Error: Failed to update checkpoint |

---

## 4. ADR Management

### 4.1 Creating an ADR

**Source:** [.clinerules](.clinerules:1) RULE 2

Architecture decisions are logged to `memory-bank/hot-context/decisionLog.md`:

```markdown
## ADR-{ID}: {Title}

**Date:** {YYYY-MM-DD}
**Status:** Proposed | Accepted | Deprecated | Superseded
**Context:** {Situation requiring decision}
**Decision:** {Chosen approach}
**Consequences:** {Positive and negative outcomes}
```

### 4.2 ADR ID Schema

**Source:** [.clinerules](.clinerules:1) RULE 2

ADRs are numbered sequentially: ADR-001, ADR-002, ADR-003...

### 4.3 ADR Lifecycle

**Source:** [.clinerules](.clinerules:1) RULE 2

| Status | Meaning |
|--------|---------|
| Proposed | Under review |
| Accepted | Approved for implementation |
| Deprecated | No longer recommended |
| Superseded | Replaced by another ADR |

---

## 5. Artifact ID Generation

### 5.1 Artifact ID Schema

**Source:** [memory-bank/hot-context/decisionLog.md](memory-bank/hot-context/decisionLog.md)

Artifacts use the format: `{TYPE}-{YYYY-MM-DD}-{NNN}`

| Type | Example |
|------|---------|
| DOC | DOC-2026-04-02-001 |
| IDEA | IDEA-2026-04-02-001 |
| TECH | TECH-2026-04-02-001 |
| ADR | ADR-2026-04-02-001 |
| CONV | CONV-2026-04-02-001 |

### 5.2 Conversation Logging

**Source:** [.clinerules](.clinerules:1) RULE 8.3

When saving an AI conversation output:
1. Save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`
2. Add entry to `docs/conversations/README.md` with triage status "Not yet triaged"
3. Never edit a conversation file after creation

---

## 6. Canonical Docs Operations

### 6.1 DOC-*-CURRENT.md Pointers

**Source:** [.github/workflows/canonical-docs-check.yml](.github/workflows/canonical-docs-check.yml:1)

Each release has pointer files that must be consistent:

```
docs/
├── DOC-1-CURRENT.md → docs/releases/v2.8/DOC-1-v2.8-PRD.md
├── DOC-2-CURRENT.md → docs/releases/v2.8/DOC-2-v2.8-Architecture.md
├── DOC-3-CURRENT.md → docs/releases/v2.8/DOC-3-v2.8-Implementation-Plan.md
├── DOC-4-CURRENT.md → docs/releases/v2.8/DOC-4-v2.8-Operations-Guide.md
└── DOC-5-CURRENT.md → docs/releases/v2.8/DOC-5-v2.8-Release-Notes.md
```

### 6.2 Cumulative Line Count Requirements

**Source:** [.githooks/pre-receive](.githooks/pre-receive:1)

| Document | Minimum Lines | Cumulative |
|----------|--------------|------------|
| DOC-1 (PRD) | 500 | Yes |
| DOC-2 (Architecture) | 500 | Yes |
| DOC-3 (Implementation) | 300 | Yes |
| DOC-4 (Operations) | 300 | Yes |
| DOC-5 (Release Notes) | 200 | Yes |

### 6.3 Feature Branch Requirement

**Source:** [.clinerules](.clinerules:1) RULE 10, RULE 12

Canonical docs MUST be modified on feature branches:
- `feature/canon-doc-*` — For documentation changes
- Direct commits to `develop` or release branches are **FORBIDDEN**
- Exception: Governance-only commits (ADRs, RULE additions) MAY commit directly

---

## 7. Prompt Registry Operations

### 7.1 Prompt Modification Procedure

**Source:** [prompts/README.md](prompts/README.md:1)

```
1. Open the corresponding SP-XXX-*.md file in prompts/
2. Modify the prompt content
3. Increment the version (e.g.: 1.0.0 -> 1.1.0)
4. Add an entry in the file's changelog
5. Check dependencies (depends_on field) and update linked prompts
6. Propagate to the target:
   - File in the repository: copy the content into the target file
   - Gemini Gem (SP-007): copy manually into the Gemini web interface
7. Commit ALL modified files:
   git add prompts/ .clinerules .roomodes Modelfile  (depending on what changed)
   git commit -m "chore(prompts): update SP-XXX - [description]"
```

### 7.2 SP-002 Sync (Byte-for-Byte)

**Source:** [scripts/rebuild_sp002.py](scripts/rebuild_sp002.py:1)

SP-002 (.clinerules) must be byte-for-byte identical to the SP-002 file:

```bash
# Sync SP-002
python scripts/rebuild_sp002.py

# Verify sync
git diff prompts/SP-002-clinerules-global.md
```

### 7.3 SP Coherence Check

**Source:** [scripts/check-prompts-sync.ps1](scripts/check-prompts-sync.ps1:1)

Run pre-commit to verify SP coherence:

```powershell
# Check sync status
.\scripts\check-prompts-sync.ps1

# Exit codes:
# 0 = All prompts in sync
# 1 = Desync detected (check output for details)
```

### 7.4 Prompt Deployment Status

**Source:** [prompts/README.md](prompts/README.md:1)

| SP | Target | Deployment | Last Verified |
|----|--------|------------|---------------|
| SP-001 | Modelfile SYSTEM | ✅ Git-synced | 2026-03-28 |
| SP-002 | .clinerules | ✅ rebuild_sp002.py | 2026-03-28 |
| SP-003 | .roomodes[0] | ✅ Git-synced | 2026-03-28 |
| SP-004 | .roomodes[1] | ✅ Git-synced | 2026-03-28 |
| SP-005 | .roomodes[2] | ✅ Git-synced | 2026-03-28 |
| SP-006 | .roomodes[3] | ✅ Git-synced | 2026-03-28 |
| SP-007 | Gemini Gems | ⚠️ **Manual required** | 2026-03-24 |
| SP-008 | orchestrator_phase3.py | ✅ Inline | 2026-03-24 |
| SP-009 | orchestrator_phase4.py | ✅ Inline | 2026-03-24 |
| SP-010 | librarian_agent.py | ✅ Inline | 2026-03-24 |

---

## 8. Script Reference

### 8.1 Proxy Startup

**Source:** [scripts/start-proxy.ps1](scripts/start-proxy.ps1:1)

```powershell
# Start the Gemini Chrome proxy
.\scripts\start-proxy.ps1

# With custom port
$env:PROXY_PORT = 8001
.\scripts\start-proxy.ps1

# With custom timeout
$env:TIMEOUT_SECONDS = 600
.\scripts\start-proxy.ps1
```

### 8.2 Batch API CLI

**Source:** [scripts/batch/cli.py](scripts/batch/cli.py:1)

```bash
# Submit a batch job
python scripts/batch/cli.py submit --prd docs/releases/v2.8/DOC-1-v2.8-PRD.md

# Poll batch status
python scripts/batch/cli.py poll --batch-id batch_xxxxx

# Retrieve results
python scripts/batch/cli.py retrieve --batch-id batch_xxxxx
```

### 8.3 Calypso MCP Server

**Source:** [src/calypso/fastmcp_server.py](src/calypso/fastmcp_server.py:1)

```bash
# Start Calypso MCP server (default port 8001)
python src/calypso/fastmcp_server.py

# Custom port
python src/calypso/fastmcp_server.py --port 9000

# Environment variables:
# CALYPSO_PORT=8001
# CALYPSO_BATCH_DIR=batch_artifacts
# CALYPSO_MEMORY_DIR=memory-bank
```

### 8.4 Check Batch Status

**Source:** [src/calypso/check_batch_status.py](src/calypso/check_batch_status.py:1)

```bash
# Check specific batch
python src/calypso/check_batch_status.py --batch-id batch_xxxxx

# Continuous monitoring
python src/calypso/check_batch_status.py --batch-id batch_xxxxx --watch
```

---

## 9. Troubleshooting Guide

### 9.1 proxy.py Error Codes

**Source:** [proxy.py](proxy.py:1) Changelog v2.0-v2.8

| Version | FIX | Error | Solution |
|---------|-----|-------|----------|
| v2.0.1 | FIX-001 | Multi-line console confusion | Added "NEW CONVERSATION" warning |
| v2.0.2 | FIX-004 | Clipboard crash on lock | Added try/except around pyperclip.paste() |
| v2.0.5 | FIX-008 | History explosion | MAX_HISTORY_CHARS truncation |
| v2.0.6 | FIX-014 | Empty content injection | 100 char blocking threshold |
| v2.1.0 | FIX-018 | History confusion | Always new conversation |
| v2.2.0 | FIX-020 | XML tag blocking | Validate before Gemini |
| v2.3.0 | FIX-022 | Context contamination | GEM MODE single message |
| v2.5.0 | FIX-024 | User message extraction | Extract before injected tags |
| v2.7.0 | FIX-027 | Escaped XML tags | Auto-unescape markdown |
| v2.8.0 | FIX-028 | Incomplete SSE stream | Separate role/content chunks |

### 9.2 Common Issues

**Source:** [scripts/check-prompts-sync.ps1](scripts/check-prompts-sync.ps1:1)

**Issue: "SP desync detected"**
```
1. Run: python scripts/rebuild_sp002.py
2. Verify: git diff prompts/SP-002-clinerules-global.md
3. Commit if needed
4. For other SPs: manually sync from prompts/ to target
```

**Issue: "pre-commit hook failed"**
```
1. Run: .\scripts\check-prompts-sync.ps1
2. Check output for specific desync
3. Follow SP sync procedure above
4. Re-commit
```

**Issue: "canonical-docs-check CI failed"**
```
1. Check DOC-*-CURRENT.md pointers point to same release
2. Verify cumulative: true in all docs
3. Check line counts: DOC-1/2 ≥500, DOC-3/4 ≥300, DOC-5 ≥200
4. Ensure feature branch for doc changes
```

### 9.3 Memory Bank Hot/Cold Issues

**Source:** [.clinerules](.clinerules:1) RULE 9

**Issue: "Cannot read cold archive files"**
```
Root cause: Direct reading of cold archive is FORBIDDEN
Solution: Use memory:query MCP tool to access cold data
         Or use Librarian Agent (SP-010) for vector search
```

### 9.4 Session Crash Recovery

**Source:** [scripts/checkpoint_heartbeat.py](scripts/checkpoint_heartbeat.py:1)

**Scenario: Agent crashes mid-session**
```
1. On restart, read session-checkpoint.md
2. If last_heartbeat > 30 minutes ago:
   - Report crash detection
   - Offer: [Continue from checkpoint] [Start fresh]
3. If continuing:
   - Read all hot-context files
   - Resume task from checkpoint
```

---

**End of DOC-4 Operations Guide (v2.8)**
