---
id: IDEA-026
title: Session Lifecycle Automation — Wire Heartbeat and Conversation Logging
status: [IMPLEMENTED]
target_release: v2.14
source: Analysis gap identified during conversation logging and heartbeat review
source_files: docs/ideas/IDEA-019-conversation-logging-mechanism.md, scripts/checkpoint_heartbeat.py
captured: 2026-04-08
captured_by: Code mode agent
refined_by: Architect mode
refinement_session: REFINEMENT-2026-04-08-003
implemented: 2026-04-08
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

## Classification

Type: TECHNICAL
- TECHNICAL: Implementation approach for wiring existing mechanisms into automated workflows

## Complexity Score

**Score: 4/10** — SYNCHRONOUS refinement recommended (straightforward implementation)

---

## Refined Implementation Details

### Component 1: `.vscode/tasks.json` — "Start Heartbeat" Task

**File:** `.vscode/tasks.json` (new file)

**Purpose:** Provide a runnable task for developers to start the heartbeat monitor manually, and optionally auto-start on VS Code launch.

**Exact structure:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Heartbeat",
      "type": "shell",
      "command": "python scripts/checkpoint_heartbeat.py --start",
      "problemMatcher": [],
      "isBackground": true,
      "presentation": {
        "reveal": "never",
        "panel": "dedicated"
      },
      "runOptions": {
        "runOn": "default"
      }
    },
    {
      "label": "Stop Heartbeat",
      "type": "shell",
      "command": "python scripts/checkpoint_heartbeat.py --stop",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Heartbeat Status",
      "type": "shell",
      "command": "python scripts/checkpoint_heartbeat.py --status",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always"
      }
    }
  ]
}
```

**Trigger conditions:**
- **Manual:** Developer runs `Tasks: Run Task` → `Start Heartbeat` from VS Code command palette
- **Auto-start (optional):** Add to `.vscode/settings.json`:
  ```json
  {
    "task.allowAutomaticTasks": "on",
    "files.watcherExclude": {
      "**/.checkpoint_heartbeat.pid": true
    }
  }
  ```

**Failure mode:**
- If `checkpoint_heartbeat.py` fails, task shows error in terminal
- Heartbeat loop exits; next session detects stale checkpoint and flags it

**Dependencies:**
- `scripts/checkpoint_heartbeat.py` must exist (IDEA-019 implemented)
- Python 3.7+ must be in PATH

---

### Component 2: Wire `checkpoint_heartbeat.py --log-conversation` to `attempt_completion`

**Files to modify:**
1. `.clinerules` — Add item 7 to RULE 2
2. `prompts/SP-002-clinerules-global.md` — Mirror the change in the embedded RULE 2

**Location in RULE 2:** After existing item 6 (RELEASE.md update), add item 7:

**Exact text to add to RULE 2 (after line ~70 in .clinerules):**

```
7. **Conversation logging:**
   - Before calling attempt_completion, execute: `python scripts/checkpoint_heartbeat.py --log-conversation`
   - This saves session metadata to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`
   - If the script fails or returns non-zero, log the error but DO NOT block completion
   - RULE 8.3 Conversation Log Mandate requires all conversations be saved
```

**Trigger condition:**
- Fires on every `attempt_completion` call, before the tool executes
- Non-blocking: if script fails, agent continues with completion

**Failure mode:**
- If script fails silently, conversation is not logged
- CI workflow (Component 3) will detect missing conversation and fail
- Agent should note the failure in the completion output

**Dependencies:**
- `scripts/checkpoint_heartbeat.py` must implement `--log-conversation` flag (IDEA-019 implemented)
- `docs/conversations/` directory must exist
- `docs/conversations/README.md` must exist

**Implementation note:** This is a RULE modification, not a code change. The agent is instructed to run the command manually as part of its protocol.

---

### Component 3: `.github/workflows/conversation-check.yml`

**File:** `.github/workflows/conversation-check.yml` (new file)

**Purpose:** Validate that conversation files are being created as required by RULE 8.3.

**Exact structure:**

```yaml
name: Conversation Logging Check

on:
  # Run on every push to detect missing conversation logs
  push:
    branches:
      - 'develop'
      - 'develop-v*'
      - 'main'
  # Also run on pull request
  pull_request:
    branches:
      - 'develop'
      - 'develop-v*'
      - 'main'

jobs:
  conversation-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Check for recent conversation files
        id: check
        run: |
          echo "=== Conversation Logging Check ==="
          
          # Check docs/conversations/ exists
          if [ ! -d "docs/conversations" ]; then
            echo "::warning::docs/conversations/ directory does not exist"
            echo "has_conversations=false" >> $GITHUB_OUTPUT
            exit 0
          fi
          
          # Find conversation files from last 48 hours
          SINCE=$(date -d '48 hours ago' +%Y-%m-%d)
          RECENT_FILES=$(find docs/conversations -name "*.md" -type f -newermt "$SINCE" 2>/dev/null | wc -l)
          
          echo "Conversation files in last 48 hours: $RECENT_FILES"
          echo "has_conversations=$([ "$RECENT_FILES" -gt 0 ] && echo 'true' || echo 'false')" >> $GITHUB_OUTPUT
          
          # List recent files for debugging
          if [ "$RECENT_FILES" -gt 0 ]; then
            echo "Recent conversation files:"
            find docs/conversations -name "*.md" -type f -newermt "$SINCE" -exec basename {} \;
          fi

      - name: Validate conversation file format
        if: steps.check.outputs.has_conversations == 'true'
        run: |
          echo "=== Validating Conversation File Format ==="
          
          SINCE=$(date -d '48 hours ago' +%Y-%m-%d)
          
          # Check each recent conversation file for required frontmatter
          for file in $(find docs/conversations -name "*.md" -type f -newermt "$SINCE"); do
            echo "Checking: $file"
            
            # Must have session_id in frontmatter
            if ! grep -q "^session_id:" "$file"; then
              echo "::error::Missing session_id in $file"
              exit 1
            fi
            
            # Must have mode in frontmatter
            if ! grep -q "^mode:" "$file"; then
              echo "::error::Missing mode in $file"
              exit 1
            fi
            
            # Must have date in frontmatter
            if ! grep -q "^date:" "$file"; then
              echo "::error::Missing date in $file"
              exit 1
            fi
            
            echo "  ✓ Valid format"
          done

      - name: Update conversations README if needed
        run: |
          echo "=== Checking conversations README ==="
          
          if [ ! -f "docs/conversations/README.md" ]; then
            echo "::warning::docs/conversations/README.md missing — will be created by heartbeat script"
          fi

      - name: Fail if no recent conversations on develop/main
        if: steps.check.outputs.has_conversations == 'false'
        run: |
          echo "::error::No conversation files found in last 48 hours!"
          echo "::error::RULE 8.3 requires all conversations be logged."
          echo "::error::Ensure checkpoint_heartbeat.py --log-conversation runs at session end."
          exit 1
```

**Trigger conditions:**
- Every push to `develop`, `develop-v*`, `main`
- Every pull request to protected branches
- Can also be triggered manually via `workflow_dispatch`

**Failure conditions:**
- No conversation files found in `docs/conversations/` in last 48 hours → FAIL
- Conversation file missing required frontmatter fields (session_id, mode, date) → FAIL

**Failure mode:**
- PR cannot be merged if workflow fails
- Developers are notified via GitHub Actions UI
- Must create conversation file or fix heartbeat trigger

**Dependencies:**
- `docs/conversations/` directory must exist (created by `checkpoint_heartbeat.py --log-conversation`)
- `checkpoint_heartbeat.py --log-conversation` must produce valid files with frontmatter

---

### Component 4: `.github/workflows/heartbeat-check.yml`

**File:** `.github/workflows/heartbeat-check.yml` (new file)

**Purpose:** Verify that `memory-bank/hot-context/session-checkpoint.md` is fresh (updated within last 15 minutes) to detect broken heartbeat automation.

**Exact structure:**

```yaml
name: Heartbeat Freshness Check

on:
  # Run frequently to catch stale sessions
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  # Also run on push to detect broken heartbeat starts
  push:
    branches:
      - 'develop'
      - 'develop-v*'
  # Manual trigger for debugging
  workflow_dispatch:

jobs:
  heartbeat-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Check session checkpoint freshness
        id: freshness
        run: |
          echo "=== Heartbeat Freshness Check ==="
          
          CHECKPOINT="memory-bank/hot-context/session-checkpoint.md"
          
          if [ ! -f "$CHECKPOINT" ]; then
            echo "::warning::No session-checkpoint.md found — heartbeat may not be running"
            echo "fresh=false" >> $GITHUB_OUTPUT
            echo "age_minutes=999" >> $GITHUB_OUTPUT
            exit 0
          fi
          
          # Get last modified time
          LAST_MOD=$(stat -c %Y "$CHECKPOINT" 2>/dev/null || stat -f %m "$CHECKPOINT" 2>/dev/null)
          NOW=$(date +%s)
          AGE_SECONDS=$((NOW - LAST_MOD))
          AGE_MINUTES=$((AGE_SECONDS / 60))
          
          echo "Checkpoint age: $AGE_MINUTES minutes"
          echo "age_minutes=$AGE_MINUTES" >> $GITHUB_OUTPUT
          
          # Check if fresh (within 15 minutes)
          if [ $AGE_MINUTES -lt 15 ]; then
            echo "fresh=true" >> $GITHUB_OUTPUT
            echo "✓ Checkpoint is fresh (last updated $AGE_MINUTES minutes ago)"
          else
            echo "fresh=false" >> $GITHUB_OUTPUT
            echo "✗ Checkpoint is stale (last updated $AGE_MINUTES minutes ago)"
          fi

      - name: Extract checkpoint metadata
        if: steps.freshness.outputs.fresh == 'true'
        run: |
          echo "=== Checkpoint Metadata ==="
          
          CHECKPOINT="memory-bank/hot-context/session-checkpoint.md"
          
          # Extract session_id
          SESSION_ID=$(grep "^session_id:" "$CHECKPOINT" | cut -d: -f2- | tr -d ' ')
          echo "Session ID: ${SESSION_ID:-unknown}"
          
          # Extract status
          STATUS=$(grep "^status:" "$CHECKPOINT" | cut -d: -f2- | tr -d ' ')
          echo "Status: ${STATUS:-unknown}"
          
          # Extract last heartbeat
          LAST_HB=$(grep "^last_heartbeat:" "$CHECKPOINT" | cut -d: -f2- | tr -d ' ')
          echo "Last Heartbeat: ${LAST_HB:-unknown}"

      - name: Fail if heartbeat is stale on develop
        if: steps.freshness.outputs.fresh == 'false'
        run: |
          echo "::error::Heartbeat is stale!"
          echo "::error::session-checkpoint.md was last updated ${AGE_MINUTES} minutes ago"
          echo "::error::Expected: < 15 minutes"
          echo "::error::"
          echo "::error::To fix:"
          echo "::error::  1. Run 'Tasks: Start Heartbeat' in VS Code"
          echo "::error::  2. Or run: python scripts/checkpoint_heartbeat.py --start"
          echo "::error::"
          echo "::error::This failure indicates the heartbeat automation is broken."
          exit 1

      - name: Warning only on main (heartbeat not expected)
        if: github.ref == 'refs/heads/main' && steps.freshness.outputs.fresh == 'false'
        run: |
          echo "::warning::Heartbeat stale on main branch"
          echo "::warning::This is expected — main is a frozen release branch"
          echo "::warning::No action required."
```

**Trigger conditions:**
- **Scheduled:** Every 15 minutes (`*/15 * * * *`) to detect stale sessions
- **Push:** On push to `develop` or `develop-v*` to catch failed heartbeat starts
- **Manual:** Via `workflow_dispatch` for debugging

**Freshness threshold:**
- **Pass:** `session-checkpoint.md` modified within last 15 minutes
- **Fail:** `session-checkpoint.md` modified more than 15 minutes ago

**Failure mode:**
- On `develop`/`develop-v*`: Workflow fails → blocks CI → developers notified
- On `main`: Warning only (expected — main is frozen)
- Stale heartbeat means either:
  1. Heartbeat was never started
  2. Heartbeat crashed
  3. Session ended but checkpoint wasn't cleaned up

**Dependencies:**
- `memory-bank/hot-context/session-checkpoint.md` must exist
- File must have frontmatter with `last_heartbeat` timestamp

---

## Affected Documents

| Document | Impact | Description |
|----------|--------|-------------|
| `.clinerules` | Minor update | Add item 7 to RULE 2 (conversation logging trigger) |
| `prompts/SP-002-clinerules-global.md` | Minor update | Mirror RULE 2 change in embedded content |
| `.vscode/tasks.json` | New file | Add heartbeat start/stop/status tasks |
| `memory-bank/hot-context/session-checkpoint.md` | No change | Understanding dependency only |
| `.github/workflows/conversation-check.yml` | New file | CI validation for conversation logging |
| `.github/workflows/heartbeat-check.yml` | New file | CI validation for heartbeat freshness |
| `docs/DOC-4-CURRENT.md` | Minor update | Document automation in Operations Guide |

---

## Sync Detection

| Candidate | Overlap Type | Recommendation |
|-----------|--------------|----------------|
| IDEA-019 | Dependency | IDEA-026 depends on IDEA-019 (checkpoint_heartbeat.py exists with --log-conversation) |
| IDEA-020 | Related | Handoff state wiring may benefit from same automation layer |

---

## Requirements (after refinement)

### REQ-026-001: VS Code Heartbeat Task

**As a** developer  
**I want** a VS Code task to start the heartbeat monitor  
**So that** I can easily begin tracking my session time

**Acceptance criteria:**
- [ ] `.vscode/tasks.json` contains "Start Heartbeat", "Stop Heartbeat", "Heartbeat Status" tasks
- [ ] "Start Heartbeat" task runs `python scripts/checkpoint_heartbeat.py --start` in background
- [ ] Tasks are documented in DOC-4 Operations Guide

### REQ-026-002: Session-End Conversation Logging

**As a** agent  
**I want** conversation logging to trigger automatically at session end  
**So that** all conversations are captured without manual intervention

**Acceptance criteria:**
- [ ] RULE 2 in `.clinerules` instructs agent to run `checkpoint_heartbeat.py --log-conversation` before `attempt_completion`
- [ ] `prompts/SP-002-clinerules-global.md` mirrors the same instruction
- [ ] Logging failure does not block completion (non-blocking)
- [ ] Conversation is saved to `docs/conversations/` with proper naming

### REQ-026-003: CI Validation for Conversation Logging

**As a** QA engineer  
**I want** CI to validate conversation files are being created  
**So that** I can verify the automation is working

**Acceptance criteria:**
- [ ] `.github/workflows/conversation-check.yml` exists
- [ ] Workflow runs on every push to develop/develop-v*/main and on PRs
- [ ] Workflow checks for conversation files in last 48 hours
- [ ] Workflow validates required frontmatter (session_id, mode, date)
- [ ] Workflow fails if no recent conversations found

### REQ-026-004: CI Validation for Heartbeat Freshness

**As a** QA engineer  
**I want** CI to verify session checkpoint is fresh  
**So that** I can detect broken heartbeat automation

**Acceptance criteria:**
- [ ] `.github/workflows/heartbeat-check.yml` exists
- [ ] Workflow runs every 15 minutes via cron schedule
- [ ] Workflow checks `session-checkpoint.md` was updated within 15 minutes
- [ ] Workflow fails on develop branches if checkpoint is stale
- [ ] Workflow warns (no fail) on main branch

---

## Implementation Branch

`feature/IDEA-026-session-lifecycle-automation` from `develop`

---

## Refinement Log

| Date | Mode | Participants | Status |
|------|------|--------------|--------|
| 2026-04-08 | Architect | Code→Architect handoff | [REFINED] |

### Session Summary

Refined all 4 automation components with exact implementation details:

1. **`.vscode/tasks.json`** — Complete JSON structure with Start/Stop/Status tasks
2. **RULE 2 conversation logging** — Exact text to add, location in file
3. **`.github/workflows/conversation-check.yml`** — Full YAML with trigger conditions, validation logic, failure modes
4. **`.github/workflows/heartbeat-check.yml`** — Full YAML with 15-minute freshness threshold, scheduled + push triggers

### Parked Technical Suggestions

| Suggestion | Parked to | Decision |
|------------|-----------|----------|
| Auto-start heartbeat via VS Code extension | TECH-SUGGESTIONS | Deferred — requires extension development |
| Hook conversation logging to pre-commit hook | TECH-SUGGESTIONS | Deferred — RULE 2 instruction is sufficient |
