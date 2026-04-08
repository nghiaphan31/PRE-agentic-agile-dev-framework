---
title: "TECH-002: Auto-Detect Merged Features for Release Scope"
description: "Automatically detect features merged to develop since last release and add them to next release scope"
status: "[IDEA]"
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

## Proposed Solution

Create an **automated pipeline** that:

1. **Detects merged features**: On demand or on a schedule, query Git to find all branches merged to `develop` since the last release tag (e.g., v2.10.0)
2. **Extracts IDEA metadata**: Parse merged branch names or commit messages to identify the IDEA ID
3. **Cross-references IDEAS-BACKLOG**: Verify the IDEA exists and is in IMPLEMENTED or REVIEW state
4. **Auto-adds to release scope**: Updates the relevant develop-vX.Y branch documentation to include the newly detected feature
5. **Notifies stakeholders**: Creates a notification/review item for human confirmation

## Implementation Approach

### Option A: Git Hook + Script (Pre-merge)
- Pre-receive hook on `develop` that triggers when a feature branch is merged
- Hook calls a script that extracts the IDEA ID from branch name or commit
- Script updates the current "next release" scope documentation

### Option B: Scheduled Scan (CI/CD)
- GitHub Actions workflow that runs on schedule (e.g., nightly)
- Queries Git log since last release tag
- Compares against IDEAS-BACKLOG to find un-scoped implemented features
- Creates a PR to update the release scope documentation

### Option C: On-Demand Orchestrator Command
- Developer/Scrum Master requests "sync release scope"
- Orchestrator queries Git and backlog
- Presents a list of detected but un-scoped features
- Human approves which to add to scope

## Affected Documents

- `memory-bank/hot-context/progress.md` - progress tracking
- `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md` - release scope
- `docs/ideas/IDEAS-BACKLOG.md` - backlog items
- `plans/governance/PLAN-release-governance.md` - governance plans
- `.github/workflows/` - potential CI/CD integration

## Related Ideas

- IDEA-003: Release Governance
- IDEA-019: Conversation Logging Mechanism (the catalyst for this suggestion)
- IDEA-022: Ideation-to-Release Journey

## Notes

This suggestion arose from observing that IDEA-019 was implemented and merged but not automatically added to v2.11 scope. The human explicitly noted: "features which are merged into the develop branch since the previous release" should be "automatically" added to the next release scope.

## Status History

- 2026-04-08: [IDEA] - Initial capture by Orchestrator
