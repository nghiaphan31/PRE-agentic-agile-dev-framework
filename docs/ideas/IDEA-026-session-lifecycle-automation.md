---
id: IDEA-026
title: Session Lifecycle Automation — Wire Heartbeat and Conversation Logging
status: [IDEA]
target_release: TBD
source: Analysis gap identified during conversation logging and heartbeat review
source_files: docs/ideas/IDEA-019-conversation-logging-mechanism.md, scripts/checkpoint_heartbeat.py
captured: 2026-04-08
captured_by: Code mode agent
refined_by: 
refinement_session: 
---

## Description

IDEA-019 specified conversation logging and heartbeat mechanisms, and the scripts (`checkpoint_heartbeat.py`) exist in the codebase. However, these mechanisms lack automation — there is no auto-start trigger for heartbeat, no session-end trigger for conversation logging, no VS Code task, and no CI workflow to validate the automation is working.

## Problem

The `checkpoint_heartbeat.py` script exists at `scripts/checkpoint_heartbeat.py` and implements both heartbeat and conversation logging functionality, but it is never invoked automatically:

1. **No auto-start trigger**: Heartbeat does not start automatically when a session begins
2. **No session-end trigger**: Conversation logging does not fire when `attempt_completion` is called
3. **No VS Code task**: No `.vscode/tasks.json` entry for developers to manually trigger heartbeat
4. **No CI workflow**: No GitHub Actions to validate that `session-checkpoint.md` remains fresh

This means the governance requirements in RULE 8.3 (conversation logging) and the heartbeat requirements are effectively unenforceable — the code exists but never runs.

## Proposed Solution

Implement the automation layer to wire the existing mechanisms:

1. **Create `.vscode/tasks.json`** with a "Start Heartbeat" task that runs `python scripts/checkpoint_heartbeat.py --start`
2. **Wire conversation logging to session end** by modifying the system prompt's `attempt_completion` behavior to invoke `checkpoint_heartbeat.py --log-conversation` before completing
3. **Create `.github/workflows/conversation-check.yml`** CI workflow to validate conversation files are being created and contain valid content
4. **Create `.github/workflows/heartbeat-check.yml`** to verify `memory-bank/hot-context/session-checkpoint.md` is fresh (updated within last 15 minutes)

## Classification

Type: TECHNICAL
- TECHNICAL: Implementation approach for wiring existing mechanisms into automated workflows

## Complexity Score

**Score: 4/10** — SYNCHRONOUS refinement recommended (straightforward implementation)

## Affected Documents

| Document | Impact | Description |
|----------|--------|-------------|
| .clinerules | Minor update | May need to clarify automation triggers in RULE 8.3 |
| .vscode/tasks.json | New file | Add heartbeat start task |
| prompts/SP-002 | Minor update | Wire attempt_completion to invoke conversation logging |
| memory-bank/hot-context/session-checkpoint.md | Minor update | Heartbeat target file |
| DOC-4 | Minor update | Document the automation in Operations Guide |
| .github/workflows/conversation-check.yml | New file | CI validation for conversation logging |
| .github/workflows/heartbeat-check.yml | New file | CI validation for heartbeat freshness |

## Sync Detection

[Filled by Orchestrator at intake — any overlaps with existing ideas?]

| Candidate | Overlap Type | Recommendation |
|-----------|--------------|----------------|
| IDEA-019 | Dependency | IDEA-026 depends on IDEA-019 (conversation logging script exists) |
| IDEA-020 | Related | Handoff state wiring may benefit from same automation layer |

---

## Requirements (after refinement)

### REQ-026-001: VS Code Heartbeat Task

**As a** developer  
**I want** a VS Code task to start the heartbeat monitor  
**So that** I can easily begin tracking my session time

**Acceptance criteria:**
- [ ] `.vscode/tasks.json` contains "Start Heartbeat" task
- [ ] Task runs `python scripts/checkpoint_heartbeat.py --start` in background
- [ ] Task is documented in DOC-4 Operations Guide

### REQ-026-002: Session-End Conversation Logging

**As a** agent  
**I want** conversation logging to trigger automatically at session end  
**So that** all conversations are captured without manual intervention

**Acceptance criteria:**
- [ ] System prompt's `attempt_completion` invokes `checkpoint_heartbeat.py --log-conversation`
- [ ] Conversation is saved to `docs/conversations/` with proper naming
- [ ] Logging failure does not block completion

### REQ-026-003: CI Validation for Conversation Logging

**As a** QA engineer  
**I want** CI to validate conversation files are being created  
**So that** I can verify the automation is working

**Acceptance criteria:**
- [ ] `.github/workflows/conversation-check.yml` exists
- [ ] Workflow checks for conversation files in last 24 hours
- [ ] Workflow fails if no recent conversations found

### REQ-026-004: CI Validation for Heartbeat Freshness

**As a** QA engineer  
**I want** CI to verify session checkpoint is fresh  
**So that** I can detect broken heartbeat automation

**Acceptance criteria:**
- [ ] `.github/workflows/heartbeat-check.yml` exists
- [ ] Workflow checks `session-checkpoint.md` was updated within 15 minutes
- [ ] Workflow fails if checkpoint is stale

---

## Refinement Log

[Link to: docs/conversations/REFINEMENT-YYYY-MM-DD-IDEA-026.md]

### Session Summary

| Date | Mode | Participants | Status |
|------|------|--------------|--------|
| — | — | — | Pending |

### Discussion Highlights

[Key discussion points that led to requirements]

### Parked Technical Suggestions

[Any "How" suggestions that were parked to TECH-SUGGESTIONS-BACKLOG]

| Suggestion | Parked to | Decision |
|-----------|-----------|----------|
| — | — | — |

---

## Implementation Details

### Branch

`feature/IDEA-026-session-lifecycle-automation` from `develop`

### Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| IDEA-019 | blocks | [IMPLEMENTED] — checkpoint_heartbeat.py exists |
| RULE 8.3 | related | [EXISTS] — conversation logging requirement |

### Files to Create

- `.vscode/tasks.json` (or update existing)
- `.github/workflows/conversation-check.yml`
- `.github/workflows/heartbeat-check.yml`

### Files to Modify

- `prompts/SP-002-clinerules-global.md` — add automation trigger to attempt_completion
- `memory-bank/hot-context/session-checkpoint.md` — heartbeat target (no content change, just understanding)
- `DOC-4-vX.Y-Operations-Guide.md` — document automation
