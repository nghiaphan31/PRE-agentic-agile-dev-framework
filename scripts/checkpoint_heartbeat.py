#!/usr/bin/env python3
"""
checkpoint_heartbeat.py — Session Checkpoint Heartbeat

Writes a heartbeat to memory-bank/hot-context/session-checkpoint.md every 5 minutes.
This enables crash recovery if the session is interrupted.

Usage:
    python checkpoint_heartbeat.py --start        # Start the heartbeat loop
    python checkpoint_heartbeat.py --stop         # Stop the heartbeat loop
    python checkpoint_heartbeat.py --once         # Write single heartbeat and exit
    python checkpoint_heartbeat.py --status       # Show current checkpoint status

RULE MB-2: Session Checkpoint (Crash Recovery)
Every 5 minutes during active work:
1. Update session-checkpoint.md.last_heartbeat
2. Update session-checkpoint.md.git_state
3. Update session-checkpoint.md.current_task
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import re

# Configuration
CHECKPOINT_PATH = Path("memory-bank/hot-context/session-checkpoint.md")
ACTIVECONTEXT_PATH = Path("memory-bank/hot-context/activeContext.md")
HEARTBEAT_INTERVAL = 300  # 5 minutes in seconds
PID_FILE = Path(".checkpoint_heartbeat.pid")
CONVERSATIONS_DIR = Path("docs/conversations")
CONVERSATIONS_README = Path("docs/conversations/README.md")


def get_git_state():
    """Get current Git state for checkpoint."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        
        last_commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        
        commit_msg = subprocess.check_output(
            ["git", "-C", ".", "log", "-1", "--format=%s"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        
        # Get staged files (single subprocess call)
        staged_output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        staged_result = staged_output.split('\n') if staged_output else []
        
        # Get unstaged files (single subprocess call)
        unstaged_output = subprocess.check_output(
            ["git", "diff", "--name-only"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        unstaged_result = unstaged_output.split('\n') if unstaged_output else []
        
        # Get untracked files (single subprocess call)
        untracked_output = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        untracked_result = untracked_output.split('\n') if untracked_output else []
        
        return {
            "branch": branch,
            "last_commit": last_commit,
            "last_commit_message": commit_msg,
            "staged_files": staged_result,
            "modified_files": unstaged_result,
            "untracked_files": untracked_result
        }
    except subprocess.CalledProcessError:
        return {"error": "Not a git repository or git error"}


def get_session_info():
    """Get session info from checkpoint or environment."""
    # Try to read from checkpoint
    if CHECKPOINT_PATH.exists():
        content = CHECKPOINT_PATH.read_text()
        # Extract session_id if present
        for line in content.split('\n'):
            if line.startswith('session_id:'):
                return line.split(':', 1)[1].strip()
    
    # Fallback: generate from environment or use default
    mode = os.environ.get('SESSION_MODE', 'unknown')
    return f"s{datetime.now().strftime('%Y-%m-%d')}-{mode}-001"


def read_checkpoint_metadata():
    """Read existing checkpoint metadata."""
    if not CHECKPOINT_PATH.exists():
        return {}
    
    metadata = {}
    content = CHECKPOINT_PATH.read_text()
    
    # Parse frontmatter-like metadata
    in_frontmatter = False
    for line in content.split('\n'):
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    return metadata


def write_heartbeat(git_state, task_description="Active work"):
    """Write a heartbeat entry to the checkpoint file."""
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()
    
    metadata = read_checkpoint_metadata()
    session_id = metadata.get('session_id', get_session_info())
    
    # Read existing content
    if CHECKPOINT_PATH.exists():
        content = CHECKPOINT_PATH.read_text()
    else:
        content = ""
    
    # Find the heartbeat log section and add entry
    heartbeat_entry = f"| {timestamp} | Heartbeat |\n"
    
    if "## Heartbeat Log" in content:
        # Append to existing heartbeat log
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.strip() == '| Timestamp | Event |':
                # Found header, skip to next and add entries after
                while new_lines and not new_lines[-1].startswith('| '):
                    new_lines.append(lines.pop(0) if lines else '')
                break
        content = '\n'.join(lines) + heartbeat_entry
    else:
        # Append heartbeat section
        content += f"\n## Heartbeat Log\n\n| Timestamp | Event |\n|----------|-------|\n{heartbeat_entry}"
    
    # Update the frontmatter heartbeat time
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('last_heartbeat:'):
            new_lines.append(f"last_heartbeat: {timestamp}")
        elif line.startswith('modified:'):
            new_lines.append(f"modified: {timestamp}")
        else:
            new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Also update git_state in checkpoint
    if "## Git State at Last Checkpoint" in content:
        # Update existing git state section
        pass  # For now, just update heartbeat
    
    CHECKPOINT_PATH.write_text(content)
    print(f"Heartbeat written: {timestamp}")
    return True


def write_checkpoint_with_git_state(git_state, task_description="Active work"):
    """Write complete checkpoint including git state."""
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()
    
    metadata = read_checkpoint_metadata()
    session_id = metadata.get('session_id', get_session_info())
    
    checkpoint_content = f"""---
artifact_id: CHECKPOINT-{datetime.now().strftime('%Y-%m-%d')}-001
session_id: {session_id}
status: ACTIVE
created: {metadata.get('created', timestamp)}
modified: {timestamp}
author: checkpoint heartbeat script
---

# Session Checkpoint — Crash Recovery

> **Purpose**: This file is written every 5 minutes during active work. If the session crashes, the next session reads this to recover context.

## Session Metadata

| Field | Value |
|-------|-------|
| `session_id` | {session_id} |
| `mode` | {os.environ.get('SESSION_MODE', 'unknown')} |
| `status` | ACTIVE |
| `created` | {metadata.get('created', timestamp)} |
| `last_heartbeat` | {timestamp} |
| `plan` | {metadata.get('plan', 'PLAN-2026-04-01-001')} |

## Git State at Last Checkpoint

```yaml
branch: {git_state.get('branch', 'unknown')}
last_commit: {git_state.get('last_commit', 'unknown')}
last_commit_message: "{git_state.get('last_commit_message', '')}"
staged_files: {json.dumps(git_state.get('staged_files', []))}
modified_files: {json.dumps(git_state.get('modified_files', []))}
untracked_files: {json.dumps(git_state.get('untracked_files', []))}
```

## Current Task

{task_description}

## Heartbeat Log

| Timestamp | Event |
|-----------|-------|
| {timestamp} | Heartbeat |
"""
    
    CHECKPOINT_PATH.write_text(checkpoint_content)
    print(f"Checkpoint written: {timestamp}")
    return True


def run_heartbeat_loop():
    """Run the heartbeat loop every 5 minutes."""
    print(f"Starting heartbeat loop (every {HEARTBEAT_INTERVAL} seconds)")
    print(f"PID file: {PID_FILE}")
    
    # Write PID file
    PID_FILE.write_text(str(os.getpid()))
    
    try:
        while True:
            git_state = get_git_state()
            write_checkpoint_with_git_state(git_state)
            time.sleep(HEARTBEAT_INTERVAL)
    except KeyboardInterrupt:
        print("\nHeartbeat loop stopped")
    finally:
        if PID_FILE.exists():
            PID_FILE.unlink()


def stop_heartbeat():
    """Stop the running heartbeat loop."""
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text())
        try:
            os.kill(pid, 9)
            print(f"Stopped heartbeat process (PID: {pid})")
            PID_FILE.unlink()
        except ProcessLookupError:
            print(f"Process {pid} not found")
            PID_FILE.unlink()
    else:
        print("No heartbeat process running")


def read_active_context():
    """Read session metadata from activeContext.md."""
    if not ACTIVECONTEXT_PATH.exists():
        return {}
    
    metadata = {}
    content = ACTIVECONTEXT_PATH.read_text()
    
    # Parse frontmatter-like metadata
    in_frontmatter = False
    for line in content.split('\n'):
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    # Also extract non-frontmatter fields
    for line in content.split('\n'):
        if line.startswith('**Session ID:**'):
            metadata['session_id'] = line.split('**Session ID:**')[1].strip()
        elif line.startswith('**Active mode:**'):
            metadata['mode'] = line.split('**Active mode:**')[1].strip()
        elif line.startswith('**Current task**'):
            metadata['current_task'] = line.split('**Current task**')[1].strip()
    
    return metadata


def generate_slug(session_id):
    """Generate a slug from session ID for filename."""
    # Extract meaningful parts from session_id like s2026-04-08-architect-002
    # Returns: 2026-04-08-architect-002
    if session_id.startswith('s'):
        session_id = session_id[1:]
    # Replace any colons or special chars with dashes
    slug = re.sub(r'[^a-zA-Z0-9-]', '-', session_id)
    # Remove trailing dash if present
    slug = slug.rstrip('-')
    return slug


def log_conversation(conversation_text=None):
    """Log the current conversation session to docs/conversations/.
    
    Args:
        conversation_text: The actual conversation content to log. If None,
            a placeholder template is used with instructions to add notes.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H%M%S')  # Add timestamp for uniqueness
    
    # Get source from SESSION_MODE env var or fallback to 'code'
    source = os.environ.get('SESSION_MODE', 'code')
    
    # Read session metadata
    active_context = read_active_context()
    checkpoint_metadata = read_checkpoint_metadata()
    
    # Determine conversation_id (unique per conversation, not per session)
    # Use timestamp to ensure uniqueness within the same day/mode
    conversation_id = f"s{date_str}-{source}-{time_str}"
    
    # Generate slug from conversation_id
    slug = generate_slug(conversation_id)
    
    # Generate filename: {YYYY-MM-DD}-{source}-{timestamp}.md
    filename = f"{date_str}-{source}-{slug}.md"
    
    # Ensure conversations directory exists
    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Prepare conversation content
    if conversation_text:
        # Use actual conversation content provided
        conversation_content = f"""---
conversation_id: {conversation_id}
mode: {source}
date: {date_str}
source: {source}
duration: ~{active_context.get('duration', 'N/A')}
---

# Conversation Log

**Mode:** {source}
**Conversation ID:** {conversation_id}
**Date:** {date_str}

## Session Context

{active_context.get('current_task', 'N/A')}

## Conversation Content

{conversation_text}

## Source Reference

This conversation was captured via `checkpoint_heartbeat.py --log-conversation`.
"""
    else:
        # Fallback: placeholder template (legacy behavior for backward compatibility)
        conversation_content = f"""---
conversation_id: {conversation_id}
mode: {source}
date: {date_str}
source: {source}
duration: ~{active_context.get('duration', 'N/A')}
---

# Conversation Log

**Mode:** {source}
**Conversation ID:** {conversation_id}
**Date:** {date_str}

## Session Context

{active_context.get('current_task', 'N/A')}

## Conversation Content

<!-- Conversation content was not provided. Add the conversation summary,
key decisions, and outcomes below. -->

---

## Notes

<!-- Add conversation summary, key decisions, and outcomes below -->

## Source Reference

This conversation was captured via `checkpoint_heartbeat.py --log-conversation`.
"""
    
    # Write conversation file
    conversation_file = CONVERSATIONS_DIR / filename
    conversation_file.write_text(conversation_content)
    print(f"Conversation logged: {conversation_file}")
    
    # Update README.md with new entry
    if CONVERSATIONS_README.exists():
        readme_content = CONVERSATIONS_README.read_text()
    else:
        readme_content = """# Conversation Log Index

This folder contains AI conversation logs that informed the project design.
These files are **read-only after creation** — they are historical records, not canonical docs.

## How to Use

1. When saving a new AI conversation, add an entry to this table.
2. Set triage status to `Not yet triaged`.
3. Mine the conversation for ideas and create `IDEA-NNN.md` entries in `docs/ideas/`.
4. Update triage status to `Fully triaged` when all findings are captured.

## Triage Status Values

- `Not yet triaged` — conversation saved but not yet mined for ideas
- `Partially triaged` — some findings captured, review incomplete
- `Fully triaged` — all significant findings captured as IDEA-NNN entries or explicitly dismissed

---

## Conversation Registry

| Date | Source | File | Ideas Generated | Triage Status |
|---|---|---|---|---|
"""
    
    # Find the table and add new entry before the last |
    # Check if entry already exists
    if filename in readme_content:
        print(f"Entry already exists in README: {filename}")
        return str(conversation_file)
    
    # Find the last row in the table (ends with |)
    lines = readme_content.split('\n')
    insert_index = None
    for i, line in enumerate(lines):
        if line.startswith('|') and '---' not in line and 'Date | Source' not in line:
            insert_index = i
    
    if insert_index is not None:
        new_entry = f"| {date_str} | {source.capitalize()} | [{filename}]({filename}) | {conversation_id} | Not yet triaged |"
        lines.insert(insert_index + 1, new_entry)
        readme_content = '\n'.join(lines)
        CONVERSATIONS_README.write_text(readme_content)
        print(f"Updated README: {CONVERSATIONS_README}")
    
    return str(conversation_file)


def show_status():
    """Show current checkpoint status."""
    if CHECKPOINT_PATH.exists():
        metadata = read_checkpoint_metadata()
        content = CHECKPOINT_PATH.read_text()
        
        print("=== Session Checkpoint Status ===")
        print(f"Session ID: {metadata.get('session_id', 'unknown')}")
        print(f"Status: {metadata.get('status', 'unknown')}")
        print(f"Last Heartbeat: {metadata.get('last_heartbeat', 'unknown')}")
        print(f"Modified: {metadata.get('modified', 'unknown')}")
        print(f"File exists: Yes")
        
        # Show git state if present
        if "## Git State at Last Checkpoint" in content:
            print("\n--- Git State ---")
            in_git_section = False
            for line in content.split('\n'):
                if "## Git State at Last Checkpoint" in line:
                    in_git_section = True
                    continue
                if in_git_section and line.startswith('## '):
                    break
                if in_git_section and line.strip():
                    print(line)
    else:
        print("No checkpoint file found")


def main():
    parser = argparse.ArgumentParser(description="Session Checkpoint Heartbeat")
    parser.add_argument('--start', action='store_true', help='Start heartbeat loop')
    parser.add_argument('--stop', action='store_true', help='Stop heartbeat loop')
    parser.add_argument('--once', action='store_true', help='Write single heartbeat')
    parser.add_argument('--status', action='store_true', help='Show checkpoint status')
    parser.add_argument('--log-conversation', action='store_true', help='Log current conversation session')
    parser.add_argument('--content', type=str, default=None, help='Conversation content to log (use - to read from stdin)')
    
    args = parser.parse_args()
    
    if args.stop:
        stop_heartbeat()
    elif args.status:
        show_status()
    elif args.log_conversation:
        # Get conversation content: from --content arg, stdin, or placeholder
        content = None
        if args.content == '-':
            # Read from stdin
            content = sys.stdin.read()
        elif args.content:
            content = args.content
        log_conversation(content)
    elif args.once:
        git_state = get_git_state()
        write_checkpoint_with_git_state(git_state)
    elif args.start:
        run_heartbeat_loop()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
