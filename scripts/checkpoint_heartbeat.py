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

# Configuration
CHECKPOINT_PATH = Path("memory-bank/hot-context/session-checkpoint.md")
HEARTBEAT_INTERVAL = 300  # 5 minutes in seconds
PID_FILE = Path(".checkpoint_heartbeat.pid")


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
        
        # Get staged and unstaged files
        staged_result = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            text=True, stderr=subprocess.DEVNULL
        ).strip().split('\n') if subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            text=True, stderr=subprocess.DEVNULL
        ).strip() else []
        
        unstaged_result = subprocess.check_output(
            ["git", "diff", "--name-only"],
            text=True, stderr=subprocess.DEVNULL
        ).strip().split('\n') if subprocess.check_output(
            ["git", "diff", "--name-only"],
            text=True, stderr=subprocess.DEVNULL
        ).strip() else []
        
        untracked_result = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            text=True, stderr=subprocess.DEVNULL
        ).strip().split('\n') if subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            text=True, stderr=subprocess.DEVNULL
        ).strip() else []
        
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
    
    args = parser.parse_args()
    
    if args.stop:
        stop_heartbeat()
    elif args.status:
        show_status()
    elif args.once:
        git_state = get_git_state()
        write_checkpoint_with_git_state(git_state)
    elif args.start:
        run_heartbeat_loop()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
