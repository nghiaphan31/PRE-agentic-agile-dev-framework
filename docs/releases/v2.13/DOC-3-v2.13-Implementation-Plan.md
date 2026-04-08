---
doc_id: DOC-3
release: v2.13
status: Draft
title: Implementation Plan
version: 1.0
date_created: 2026-04-08
authors: [Developer mode, Human]
previous_release: v2.12
cumulative: false
type: release-specific
---

# DOC-3 — Implementation Plan (v2.13)

> **Status: DRAFT** -- This document is under construction for v2.13 release.
> **Release-Specific: YES** -- This document contains ONLY v2.13 implementation scope.
> **Cumulative: NO** -- This is NOT a cumulative document. Historical implementation details are preserved in `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md`.

---

## Table of Contents

1. [v2.13 Release Scope](#1-v213-release-scope)
2. [TECH-002: Auto-Detect Merged Features for Release Scope](#2-tech-002-auto-detect-merged-features-for-release-scope)
3. [TECH-003: Single Source of Truth for Release Tracking](#3-tech-003-single-source-of-truth-for-release-tracking)
4. [Key Implementation Decisions](#4-key-implementation-decisions)
5. [Execution Tracking](#5-execution-tracking)
6. [Dependencies and Risks](#6-dependencies-and-risks)

---

## 1. v2.13 Release Scope

v2.13 is a **Governance Tooling Release** focused on automated release scope detection and single source of truth for release tracking.

### TECHNICAL Suggestions in Scope

| TECH | Title | Status | Complexity |
|------|-------|--------|------------|
| TECH-002 | Auto-Detect Merged Features for Release Scope | ACCEPTED | 7/10 |
| TECH-003 | Single Source of Truth for Release Tracking | REFINED | 3/10 |

### Features

**Implemented:**
- TECH-002: Auto-detect merged features script and workflow
- TECH-003: RELEASE.md as single source of truth

**Enforcement:**
- R-006: All commits on `develop` since previous release tag are in scope
- `release-consistency-check.yml` GitHub Actions workflow

---

## 2. TECH-002: Auto-Detect Merged Features for Release Scope

> **TECH-002** provides automated detection of features merged to `develop` since the last release tag.

### 2.1 Purpose

The current release scoping process is manual, leading to features being inadvertently excluded from release scope. TECH-002 automates detection of merged features and ensures R-006 compliance: **ALL commits on `develop` since the previous release tag are included in scope**.

### 2.2 Implementation Components

#### 2.2.1 Git Hook: `.githooks/pre-receive-merged-features`

This pre-receive hook runs when commits are pushed to `develop` and detects merge commits.

**Location:** `.githooks/pre-receive-merged-features`

**Purpose:** Real-time detection of merge commits to `develop`

```bash
#!/bin/bash
# pre-receive-merged-features
# Triggered on push to develop, detects merge commits

while read old_sha new_sha ref; do
  if [ "$ref" = "refs/heads/develop" ]; then
    # Detect merge commits (commits with two parents)
    git log --merges "$old_sha..$new_sha" --format="%s" | while read msg; do
      echo "[DETECTED MERGE] $msg"
    done
  fi
done
```

#### 2.2.2 Python Script: `scripts/detect-merged-features.py`

This script provides programmatic detection of merged features and can be called by GitHub Actions or directly.

**Location:** `scripts/detect-merged-features.py`

**Key Functions:**
- `get_commits_since_tag(tag, branch='develop')`: Get all commits since last release tag
- `extract_idea_ids_from_commits(commits)`: Parse IDEA-NNN from branch names and commit messages
- `filter_merge_commits(commits)`: Extract only merge commits
- `generate_scope_report(tag)`: Generate a scope report for human review

**Usage:**
```bash
python scripts/detect-merged-features.py --since-tag v2.12.0 --branch develop
```

**Output:**
- List of commits since last tag
- Detected IDEA IDs
- Merge commit count
- Compliance report for R-006

#### 2.2.3 GitHub Actions Workflow: `.github/workflows/detect-merged-features.yml`

This workflow runs on schedule and on-demand to detect merged features.

**Location:** `.github/workflows/detect-merged-features.yml`

**Triggers:**
- `workflow_dispatch`: Manual trigger
- `schedule`: Daily at 6 AM UTC
- `push`: On push to `develop` or `develop-v*`

**Jobs:**
1. **Detect Features**: Run `detect-merged-features.py` to get commits since last tag
2. **Verify Scope**: Check against `RELEASE.md` scope section
3. **Report**: Create PR or post comment with detected features

### 2.3 R-006 Compliance

**R-006 Requirement:** The scope of the next release MUST include **ALL commits on `develop` since the previous release tag**.

**Implementation:**
- `detect-merged-features.py` uses Git tags as authoritative boundary
- All commits (not just feature branches) are detected
- Non-feature commits (docs-only, governance) are flagged but included
- Any exclusion requires ADR documentation

**Verification:**
```bash
# Verify scope completeness
git log v2.12.0..develop --oneline
# All commits should be accounted for in v2.13 scope
```

### 2.4 Scope Update Protocol

1. **Detection**: On push to `develop`, hook triggers and `detect-merged-features.py` runs
2. **Reporting**: GitHub Actions creates PR updating `RELEASE.md` scope section
3. **Review**: Human reviews and approves scope changes
4. **Merge**: Approved scope changes are merged to `develop`

---

## 3. TECH-003: Single Source of Truth for Release Tracking

> **TECH-003** establishes `memory-bank/hot-context/RELEASE.md` as the authoritative source for release state.

### 3.1 Purpose

Multiple locations stored release information (CHANGELOG.md, DOC-5-CURRENT.md, Git tags) with inconsistencies. TECH-003 establishes a single source of truth that agents read at session start.

### 3.2 Implementation Components

#### 3.2.1 RELEASE.md Schema

**Location:** `memory-bank/hot-context/RELEASE.md`

**Required Sections:**
- `Current Released Version`: Latest version with tag on main
- `Current Draft Version`: Version currently in development
- `Released Versions`: Table of all released versions
- `Draft Version`: Current draft version info
- `vX.Y Scope`: Per-version scope section with commits and features

#### 3.2.2 Update Protocol

| Event | Update Required | Updated By |
|-------|-----------------|------------|
| New release tag created | Add row to Released Versions, create new scope section | Release automation or agent |
| New commit to develop | Update Commits Since table | Agent (on commit) |
| Feature added to scope | Update Features in Scope table | Agent (on scope decision) |
| Version number decided | Update Draft Version table | Scrum Master / Agent |

#### 3.2.3 GitHub Actions: `release-consistency-check.yml`

**Location:** `.github/workflows/release-consistency-check.yml`

**Checks:**
1. RELEASE.md existence and schema validation
2. Git tag consistency with RELEASE.md
3. DOC-5-CURRENT.md consistency with RELEASE.md
4. Frozen docs existence for released versions
5. DOC-3-CURRENT.md consistency

**Enforcement:**
- Runs on PR to `main`, `develop`, or `develop-v*`
- Runs on tag push
- Can be triggered manually

### 3.3 Consistency Rules

| Check | Source of Truth | Target | Enforcement |
|-------|-----------------|--------|--------------|
| Git tag exists | Git | RELEASE.md | GitHub Actions pre-receive hook |
| Version matches DOC-5 | RELEASE.md | DOC-5-CURRENT.md | release-consistency-check.yml |
| DOC-5 points to frozen path | DOC-5-CURRENT.md | docs/releases/vX.Y/ | release-consistency-check.yml |
| Branch matches develop-vX.Y | RELEASE.md | Git | Agent discipline + CODEOWNERS |
| Execution tracker exists | RELEASE.md | EXECUTION-TRACKER-vX.Y.md | release-consistency-check.yml |

---

## 4. Key Implementation Decisions

### TECH-002: Auto-Detect Merged Features for Release Scope

**Decision:** Implement both git hook (real-time) and GitHub Actions (scheduled/on-demand) for comprehensive detection.

**Rationale:** Git hooks provide immediate notification on merge, while GitHub Actions provides scheduled scanning and human review via PR.

**Implementation:**
- `.githooks/pre-receive-merged-features`: Real-time merge detection
- `scripts/detect-merged-features.py`: Reusable detection script
- `.github/workflows/detect-merged-features.yml`: Scheduled and on-demand detection

**Consequences:**
- R-006 compliance is automated
- Release scope is always complete
- Human review step ensures scope accuracy

### TECH-003: Single Source of Truth for Release Tracking

**Decision:** Make `RELEASE.md` the authoritative source, enforced by GitHub Actions.

**Rationale:** Agents read `memory-bank/hot-context/` at session start (per RULE 1). Placing release state here ensures automatic discovery.

**Implementation:**
- `memory-bank/hot-context/RELEASE.md`: Single source of truth
- `.github/workflows/release-consistency-check.yml`: Enforcement workflow

**Consequences:**
- Consistent release state across all agents
- Automated enforcement of release tracking consistency
- Clear update protocol for release state changes

---

## 5. Execution Tracking

### TECH-002 Implementation Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Create `.githooks/pre-receive-merged-features` | DONE |
| 2 | Create `scripts/detect-merged-features.py` | DONE |
| 3 | Create `.github/workflows/detect-merged-features.yml` | DONE |
| 4 | Enforce R-006 (all commits on develop in scope) | DONE |
| 5 | Update DOC-3 with TECH-002 implementation | DONE |
| 6 | Update progress.md and activeContext.md | DONE |

**Verification Status:** ✅ PASSED (2026-04-08)

**Requirements Verified:**
- R-001: Git query requirements ✅
- R-002: Branch name extraction ✅
- R-003: Backlog cross-reference ✅
- R-004: Release scope update ✅
- R-005: Scope placeholder creation ✅
- R-006: All commits on develop since previous release ✅

### TECH-003 Implementation Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Create/validate RELEASE.md schema | DONE |
| 2 | Implement release-consistency-check.yml workflow | DONE |
| 3 | Add update protocol to RELEASE.md | DONE |
| 4 | Update DOC-3 with TECH-003 implementation | DONE |
| 5 | Update DOC-5 with TECH-003 release notes | DONE |

**Verification Status:** ✅ PASSED (2026-04-08)

**Requirements Verified:**
- R-001: RELEASE.md location in memory-bank/hot-context ✅
- R-002: Required sections implemented ✅
- R-003: Update protocol documented ✅
- R-004: Consistency enforcement implemented ✅

---

## 6. Dependencies and Risks

### Dependencies

| TECH | Dependency Type | Reason |
|------|----------------|--------|
| TECH-002 | Dependency | Auto-detect requires TECH-003 (RELEASE.md) for scope storage |
| TECH-003 | Dependency | Single source of truth is prerequisite for TECH-002 scope reporting |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook deployment across clones | Medium | Low | GitHub Actions provides centralized enforcement |
| False positives in merge detection | Low | Low | Human review step before scope finalization |

---

**End of DOC-3 Implementation Plan (v2.13)**