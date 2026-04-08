---
title: "TECH-002: Auto-Detect Merged Features for Release Scope"
description: "Automatically detect features merged to develop since last release and add them to next release scope"
status: "[REFINED]"
complexity: 7
captured: 2026-04-08
source: Developer mode (routing from IDEA-019 context)
owner: Architect

## Problem Statement

Currently, release scoping is a **manual process** that relies on human tracking of which features have been merged to `develop` since the last release. This leads to features being missed from the release scope.

**Example:** IDEA-019 (conversation-logging-mechanism) was implemented and merged into `develop` but was not automatically added to the next release scope (v2.11).

## Human Requirements

The following requirements were explicitly stated by the human during refinement:

1. **Immediate scope placeholder**: Upon a release being done, immediately create/define a placeholder for the scope of the next release

2. **Auto-add merged features**: Features or changes already merged into `develop` branch should be automatically added to the scope of the next release

3. **Systematic merge suggestion**: A mechanism to systematically suggest merging feature branches when the feature is complete

## Root Cause

The ideation-to-release pipeline lacks automated detection of:
1. Which features have been merged to `develop` since the last tagged release
2. Which release scope (develop-vX.Y) they should be added to
3. Automatic promotion from backlog status to the appropriate release scope

## Refined Requirements

### R-001: Git Query Requirements
The system MUST be able to:
- Query Git for all commits added to `develop` since a given tag (e.g., `git log v2.10.0..develop --oneline`)
- Extract branch names from commit messages or merge commits
- Identify merge commits specifically (commits with two parents)
- Parse IDEA-NNN identifiers from branch names using pattern `feature/(IDEA-\d+)-`

### R-002: Branch Name Extraction
The system MUST parse:
- Branch names: `feature/IDEA-019-conversation-logging` → IDEA-019
- Merge commit messages: `"Merge branch 'feature/IDEA-019-conversation-logging'"` → IDEA-019
- Squash merge commit messages: `"IDEA-019: Implement conversation logging"` → IDEA-019

### R-003: Backlog Cross-Reference
The system MUST:
- Verify detected IDEA IDs exist in `docs/ideas/IDEAS-BACKLOG.md`
- Check their status is `IMPLEMENTED`, `REVIEW`, or similar merged state
- Flag any IDEA IDs that don't exist in the backlog (for human review)

### R-004: Release Scope Update
The system MUST:
- Update the current "next release" scope (develop-vX.Y) documentation
- Add detected features to the release scope section
- Create a human-review step before finalizing scope changes

### R-005: Scope Placeholder Creation
The system MUST:
- Detect when a new release is tagged (vX.Y.0)
- Automatically create a placeholder `develop-v{X+1}.0` branch or documentation
- Initialize the new scope with an empty or "TBD" feature list

## Feasibility Analysis

### Option A: Git Hook + Script (Pre-merge)
**Approach:** Pre-receive hook on `develop` that triggers when a feature branch is merged.

**Feasibility: HIGH**

| Aspect | Assessment |
|--------|------------|
| Implementation | Simple shell/python script triggered by hook |
| Git Integration | Direct - hook runs in Git context |
| Extraction | Can parse branch name from hook parameters |
| Timing | Real-time: triggers on every merge |
| Dependencies | Only Git and local scripts |

**Git Hook Implementation:**
```bash
# In .git/hooks/pre-receive or a custom hooks directory
while read old_sha new_sha ref; do
  if [ "$ref" = "refs/heads/develop" ]; then
    # Detect merge commits
    git log --merges "$old_sha..$new_sha" --format="%s"
  fi
done
```

**Pros:**
- Real-time detection
- No external dependencies
- Simple to implement
- Immediate notification

**Cons:**
- Only detects merges to `develop` (not `develop-vX.Y`)
- No scheduled aggregation
- Hook maintenance across clones
- No human approval step built-in

**Required Files to Modify:**
- `.githooks/pre-receive` (or create `pre-receive-merged-features`)
- `scripts/detect-merged-features.py` (new)
- `memory-bank/hot-context/release-scope-tracker.md` (new - to track next release)

---

### Option B: Scheduled Scan (CI/CD)
**Approach:** GitHub Actions workflow that runs on schedule, queries Git log since last release tag, compares against IDEAS-BACKLOG.

**Feasibility: MEDIUM-HIGH**

| Aspect | Assessment |
|--------|------------|
| Implementation | GitHub Actions YAML + Python script |
| Git Integration | Via `actions/checkout` + local Git |
| Extraction | Python script parses git log output |
| Timing | Scheduled (e.g., nightly) or on-demand |
| Dependencies | GitHub Actions, workflow_dispatch trigger |

**GitHub Actions Implementation:**
```yaml
# .github/workflows/detect-merged-features.yml
name: Detect Merged Features
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:  # Manual trigger
  push:
    branches: [main, develop, 'develop-v*']
```

**Pros:**
- Centralized (runs in GitHub, not local hooks)
- Full Git history available
- Can create PR for scope updates
- Multiple triggers supported
- Human review via PR

**Cons:**
- Requires GitHub Actions knowledge
- Scheduled, not real-time
- API rate limits possible
- Secrets/permissions management

**Required Files to Modify:**
- `.github/workflows/detect-merged-features.yml` (new)
- `scripts/detect-merged-features.py` (new - reusable across options)
- `scripts/update-release-scope.py` (new)
- `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md` (updated by workflow)

---

### Option C: On-Demand Orchestrator Command
**Approach:** Developer/Scrum Master requests "sync release scope" via Orchestrator, which queries Git and backlog, presents list of detected but un-scoped features.

**Feasibility: HIGH**

| Aspect | Assessment |
|--------|------------|
| Implementation | Orchestrator command + Python script |
| Git Integration | Via Python subprocess or MCP tool |
| Extraction | Python script with BranchTracker integration |
| Timing | On-demand (when human requests) |
| Dependencies | Orchestrator, BranchTracker, Git access |

**Implementation in `src/calypso/orchestrator_phase4.py`:**
```python
async def sync_release_scope(self, release: str) -> dict:
    """Sync release scope with merged features."""
    # 1. Get last release tag
    last_tag = self._get_last_release_tag(release)
    
    # 2. Query commits since last tag
    merged_features = self._get_merged_features_since_tag(last_tag)
    
    # 3. Cross-reference with backlog
    unscoped = self._filter_unscoped_features(merged_features)
    
    # 4. Present to human for approval
    return {
        "detected": merged_features,
        "unscoped": unscoped,
        "recommendations": self._generate_scope_additions(unscoped)
    }
```

**Pros:**
- Human-in-the-loop (more control)
- Integrates with existing Orchestrator
- Leverages BranchTracker (already exists)
- Can combine with other release planning

**Cons:**
- Requires human to remember to run
- Not automated - depends on human action
- Multiple steps for full automation

**Required Files to Modify:**
- `src/calypso/orchestrator_phase4.py` (new method or new phase)
- `scripts/detect-merged-features.py` (new - shared)
- `src/calypso/release_scope_manager.py` (new)
- `prompts/SP-010-librarian-agent.md` (optional integration)

---

## Shared Technical Components

### Core Script: `scripts/detect-merged-features.py`

All three options can share a common Python script for the core detection logic:

```python
"""
detect-merged-features.py - Core logic for detecting merged features

Usage:
    python detect-merged-features.py [--since-tag v2.10.0] [--output json|markdown]
"""

import subprocess
import re
import json
import argparse
from dataclasses import dataclass
from typing import Optional

@dataclass
class MergedFeature:
    idea_id: str
    branch_name: str
    merge_commit_hash: str
    merge_date: str
    commit_message: str

def get_merged_features_since_tag(tag: str, target_branch: str = "develop") -> list[MergedFeature]:
    """Get all features merged into target branch since the given tag."""
    # Get merge commits since tag
    cmd = [
        "git", "log", "--merges", "--format=%H|%s|%ci",
        f"{tag}..{target_branch}"
    ]
    # Parse output, extract IDEA-NNN from merge messages
    # Return list of MergedFeature objects
    pass

def extract_idea_id(text: str) -> Optional[str]:
    """Extract IDEA-NNN from branch name or commit message."""
    match = re.search(r'(IDEA-\d+)', text)
    return match.group(1) if match else None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since-tag", default="v2.10.0")
    parser.add_argument("--output", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    
    features = get_merged_features_since_tag(args.since_tag)
    # Output in requested format
```

### BranchTracker Enhancement

The existing `BranchTracker` class (in `src/calypso/branch_tracker.py`) already has:
- `BranchType.FEATURE` classification
- `idea_id` extraction from branch names
- `BranchStatus.MERGED` detection

**Enhancements needed for TECH-002:**
1. Add method `get_merged_since_tag(tag: str)` to query merge history
2. Add method `get_features_merged_since_release(release_tag: str)` 
3. Enhance `_mark_merged_branches()` to accept a custom base branch
4. Add CLI arguments for tag-based queries

---

## Dependencies Analysis

### Direct Dependencies

| Dependency | Status | Impact |
|------------|--------|--------|
| `src/calypso/branch_tracker.py` | EXISTS | Must be enhanced with tag-based queries |
| `docs/ideas/IDEAS-BACKLOG.md` | EXISTS | Must be parsed for cross-reference |
| `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md` | EXISTS | Must be updated with detected features |

### Related Ideas (Not Blockers)

| Related Idea | Relationship | Notes |
|-------------|--------------|-------|
| IDEA-003: Release Governance | Synergy | Would benefit from auto-detection |
| IDEA-019: Conversation Logging | Catalyst | The original catalyst for this suggestion |
| IDEA-020: Orchestrator as Default | Implementation Path | Option C uses Orchestrator |
| IDEA-022: Ideation-to-Release Journey | Documentation | Operational reference, not implementation |
| IDEA-024: Mandatory Backlog Maintenance | Synergy | Handoff protocol could trigger detection |

### No Blocking Dependencies

- TECH-002 does NOT require IDEA-022 to be implemented first
- TECH-002 can leverage existing `BranchTracker` without waiting for other ideas
- TECH-002 can be implemented incrementally (start with Option C, evolve to Option B)

---

## Implementation Phases (for reference - not blocking)

### Phase 1: Core Detection (All Options)
- Create `scripts/detect-merged-features.py` with shared logic
- Enhance `BranchTracker` with tag-based queries
- Test with existing CLI

### Phase 2: Option-Specific Implementation
- Option A: Add git hooks
- Option B: Add GitHub Actions workflow  
- Option C: Add Orchestrator command

### Phase 3: Integration
- Connect to release scope documentation
- Add human review workflow
- Add notifications

---

## Deliverables Summary

| File | Action | Option Impact |
|------|--------|---------------|
| `scripts/detect-merged-features.py` | NEW | Shared by all |
| `scripts/update-release-scope.py` | NEW | Shared by all |
| `src/calypso/branch_tracker.py` | MODIFY | All options |
| `.githooks/pre-receive-detect` | NEW | Option A only |
| `.github/workflows/detect-merged-features.yml` | NEW | Option B only |
| `src/calypso/orchestrator_phase4.py` | MODIFY | Option C only |
| `src/calypso/release_scope_manager.py` | NEW | Options B & C |
| `memory-bank/hot-context/release-scope-tracker.md` | NEW | All options |

---

## Deferred Decision

**The implementation approach (Option A/B/C) is NOT decided here.** Per human instruction, this refinement focuses on:

1. ✅ Refined requirements (R-001 through R-005)
2. ✅ Feasibility assessment for all 3 options
3. ✅ Shared technical components identified
4. ✅ Dependencies mapped
5. ✅ Deliverables listed

**Decision required from human:** Which option to implement:
- **Option A (Git Hook):** Real-time, simple, local-only
- **Option B (CI/CD):** Centralized, scheduled, PR-based review
- **Option C (Orchestrator):** Human-in-the-loop, on-demand, integrates with planning

---

## Status History

- 2026-04-08: [IDEA] - Initial capture by Orchestrator
- 2026-04-08: [REFINED] - Feasibility analysis, requirements clarified, implementation approaches detailed

---

## Refinement Session Log

**Session:** s2026-04-08-architect-002  
**Date:** 2026-04-08  
**Participants:** Architect mode + Human via TASK input

**Key Findings:**
1. `BranchTracker` class already exists with `idea_id` extraction from branch names
2. `BranchTracker._mark_merged_branches()` can detect merged branches but doesn't query by tag
3. TECH-SUGGESTIONS-BACKLOG showed `[REFINED]` but TECH-002.md showed `[IDEA]` - inconsistency noted and fixed
4. TECH-002 does NOT depend on IDEA-022 - can be implemented independently

**Requirements Refined:**
- Clarified git query requirements (R-001)
- Defined branch name extraction patterns (R-002)
- Specified backlog cross-reference behavior (R-003)
- Detailed release scope update mechanism (R-004)
- Added scope placeholder creation requirement (R-005)

**Next Step:** Human to decide which implementation approach (A/B/C) to pursue.
