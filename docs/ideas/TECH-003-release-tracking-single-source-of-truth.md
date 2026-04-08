# TECH-003: Single Source of Truth for Release Tracking

**Status:** REFINED

**Captured:** 2026-04-08

**Refined:** 2026-04-08

**Complexity:** 3/10

**Owner:** Architect

---

## Problem Statement

No authoritative location stores the latest release version. The following inconsistencies exist:

- **CHANGELOG.md** is stale (only v1.0, v2.0)
- **DOC-5-CURRENT.md** shows v2.11 but v2.12 exists
- **Git tags** are partial
- **Agents cannot reliably determine current release state**

This creates confusion during handoff, release planning, and cross-release coordination.

---

## Refined Definition: Single Source of Truth for Release Tracking

### What "Single Source of Truth" Means (Precisely)

The **Single Source of Truth (SSOT) for Release Tracking** is a specific file (`RELEASE.md`) that is:

1. **Authoritative**: All release state queries MUST read from this file
2. **Complete**: It contains all necessary fields to determine current state
3. **Consistent**: It is kept in sync with Git tags, DOC-5-CURRENT.md, and frozen docs
4. **Discoverable**: Agents know exactly where to look for release state

### What It Is NOT

- It is NOT a replacement for Git tags (tags are still required for GitFlow)
- It is NOT a replacement for DOC-5 release notes (which are the human-readable record)
- It is NOT a replacement for EXECUTION-TRACKER (which is per-release and detailed)
- It is NOT a general-purpose changelog

---

## Canonical Location and File Structure

### Location

```
memory-bank/hot-context/RELEASE.md
```

**Rationale:** `memory-bank/hot-context/` is already in the agent's mandatory read path (per RULE 1: CHECK→CREATE→READ→ACT). Placing RELEASE.md here ensures agents automatically read it at session start without additional discovery logic.

### Required Sections

```markdown
# Release Tracking

**Current Released Version:** vX.Y.Z  
**Current Draft Version:** vX.Y (on branch develop-vX.Y)

---

## Released Versions

| Version | Tag | Release Date | Branch | Status | DOC-5 Path |
|---------|-----|--------------|--------|--------|------------|
| v1.0 | v1.0.0 | 2026-03-28 | main | Frozen | docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md |
| ... | ... | ... | ... | ... | ... |

---

## Draft Version

| Version | Branch | Status | Target Release Date |
|---------|--------|--------|---------------------|
| v2.13 | develop-v2.12 | In Progress | TBD |

---

## v2.13 Scope

**Current draft version:** v2.13
**Status:** IN PROGRESS
**Base:** v2.12.0 (most recent tag)
**Branch:** develop-v2.12

### Commits Since v2.12.0

| Commit | Description | Feature/Idea |
|--------|-------------|--------------|
| abc1234 | feat(tech): ... | TECH-002: ... |

### Features in Scope

| Feature | Type | Status | Notes |
|---------|------|--------|-------|
| TECH-002: ... | Technical | ACCEPTED | ... |

---

**Last updated:** YYYY-MM-DD

**Source:** This is the operational source of truth for release tracking.
```

---

## Schema Specification

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Current Released Version` | SemVer | Yes | Latest version with tag on main |
| `Current Draft Version` | SemVer | Yes | Version currently in development |

### Released Versions Table

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `Version` | SemVer (minor) | Yes | e.g., v2.13 |
| `Tag` | SemVer (patch) | Yes | e.g., v2.13.0 (the actual git tag) |
| `Release Date` | ISO 8601 | Yes | Date tag was created |
| `Branch` | Git branch name | Yes | Usually "main" |
| `Status` | Enum | Yes | "Frozen" for all released versions |
| `DOC-5 Path` | File path | Yes | Relative path to release notes |

### Draft Version Table

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `Version` | SemVer (minor) | Yes | Next version number |
| `Branch` | Git branch name | Yes | develop-vX.Y branch |
| `Status` | Enum | Yes | "In Progress" or "Planning" |
| `Target Release Date` | String | No | "TBD" or ISO 8601 date |

### Scope Section (Per-Draft-Version)

The scope section is dynamically named after the draft version (e.g., `## v2.13 Scope`).

| Sub-section | Required | Description |
|-------------|----------|-------------|
| `Current draft version` | Yes | Matches draft version table |
| `Status` | Yes | IN PROGRESS, PLANNING, etc. |
| `Base` | Yes | Previous release tag |
| `Branch` | Yes | Current development branch |
| `Commits Since vX.Y.Z` | Yes | Table of commits since last release |
| `Features in Scope` | Yes | Table of features being released |

---

## Update Protocol

### When RELEASE.md Must Be Updated

| Event | Update Required | Updated By |
|-------|-----------------|------------|
| New release tag created | Add row to Released Versions, create new scope section | Release automation or agent |
| New commit to develop | Update Commits Since table | Agent (on commit) |
| Feature added to scope | Update Features in Scope table | Agent (on scope decision) |
| Version number decided | Update Draft Version table | Scrum Master / Agent |

### Update Rules

1. **No direct commits to main**: RELEASE.md is NEVER modified on main (only via merge from develop)
2. **Draft section created on release**: When vX.Y.0 is tagged, the previous draft section becomes the "Released Versions" entry
3. **Atomic updates**: Both the commits table AND the features table must be updated together
4. **Timestamp required**: Every update MUST update the `Last updated` field

### Update Sequence for New Release

```
1. Tag vX.Y.0 on main
2. Merge develop to main (fast-forward)
3. On develop, create new draft section for v{X+1}.Y
4. Move current draft to Released Versions with tag vX.Y.0
5. Update "Current Released Version" and "Current Draft Version" fields
6. Update Last updated timestamp
```

---

## Consistency Enforcement

### Consistency Rules

| Check | Source of Truth | Target | Enforcement |
|-------|-----------------|--------|--------------|
| Git tag exists | Git | RELEASE.md | GitHub Actions pre-receive hook |
| Version matches DOC-5 | RELEASE.md | DOC-5-CURRENT.md | release-gate.yml workflow |
| DOC-5 points to frozen path | DOC-5-CURRENT.md | docs/releases/vX.Y/ | release-gate.yml workflow |
| Branch matches develop-vX.Y | RELEASE.md | Git | Agent discipline + CODEOWNERS |
| Execution tracker exists | RELEASE.md | EXECUTION-TRACKER-vX.Y.md | release-gate.yml workflow |

### GitHub Actions Enforcement

A new workflow `.github/workflows/release-consistency-check.yml` verifies:

```yaml
name: Release Consistency Check
on:
  pull_request:
    branches: [main, develop, 'develop-v*']
  push:
    tags: ['v*']
  workflow_dispatch:

jobs:
  consistency:
    runs-on: ubuntu-latest
    steps:
      - name: Check RELEASE.md consistency
        run: |
          # 1. Verify current released version matches latest tag
          # 2. Verify DOC-5-CURRENT.md points to correct version
          # 3. Verify EXECUTION-TRACKER exists for current draft
          # 4. Verify frozen docs directory exists for released version
```

---

## Relationship with Other Artifacts

### RELEASE.md vs EXECUTION-TRACKER-vX.Y.md

| Aspect | RELEASE.md | EXECUTION-TRACKER-vX.Y.md |
|--------|------------|---------------------------|
| Scope | All releases (cumulative) | Single release (vX.Y) |
| Granularity | High-level tracking | Detailed per-idea progress |
| Updates | On release events | On every session |
| Location | memory-bank/hot-context/ | docs/releases/vX.Y/ |

**Relationship:** RELEASE.md references EXECUTION-TRACKER but does not replace it.

### RELEASE.md vs DOC-5-CURRENT.md

| Aspect | RELEASE.md | DOC-5-CURRENT.md |
|--------|------------|-------------------|
| Purpose | Operational state | Canonical pointer |
| Content | Version + history | Points to latest frozen DOC-5 |
| Update | On release events | On release events |

**Relationship:** `DOC-5-CURRENT.md` points to `docs/releases/vX.Y/DOC-5-vX.Y-Release-Notes.md` which is listed in RELEASE.md's "DOC-5 Path" column.

### RELEASE.md vs Git Tags

| Aspect | RELEASE.md | Git Tags |
|--------|------------|----------|
| Purpose | Human-readable state | Git-level versioning |
| Format | Markdown table | Git object |
| Update | Manual/automated | git tag command |

**Relationship:** RELEASE.md's "Tag" column MUST match actual Git tags. Git tags are the authoritative source; RELEASE.md reflects them.

---

## Implementation Requirements

### Required Files

| File | Action | Purpose |
|------|--------|---------|
| `memory-bank/hot-context/RELEASE.md` | CREATE | Already exists - validate schema |
| `.github/workflows/release-consistency-check.yml` | CREATE | Enforce consistency |
| `.clinerules` RULE 2 update | MODIFY | Add RELEASE.md update requirement |

### .clinerules Update (RULE 2)

Add to RULE 2's "Before closing any task" section:

```
2.5. RELEASE.md update (if release state changed):
    - If new release tag was created: update Released Versions table
    - If new draft was started: update Draft Version table
    - If new commits/features: update scope section
    - Update Last updated timestamp
```

### GitHub Actions Workflow

See `.github/workflows/release-consistency-check.yml` specification above.

---

## Verification Checklist

Before marking TECH-003 implementation complete, verify:

- [ ] RELEASE.md exists at `memory-bank/hot-context/RELEASE.md`
- [ ] RELEASE.md schema matches specification above
- [ ] Current Released Version matches latest Git tag
- [ ] Current Draft Version matches active develop-vX.Y branch
- [ ] All released versions have corresponding Git tags
- [ ] All released versions have corresponding DOC-5 files
- [ ] `release-consistency-check.yml` workflow exists and passes
- [ ] RULE 2 update includes RELEASE.md update protocol
- [ ] Existing inconsistencies (CHANGELOG.md, DOC-5-CURRENT.md) are noted and addressed

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| TECH-002 | REFINE | TECH-002's scope detection populates RELEASE.md's scope section |
| IDEA-003 | RELATED | Release governance framework |
| GitHub Actions | EXISTS | Need to add new workflow |

**No blocking dependencies.** TECH-003 can be implemented independently.

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-08 | [PROPOSED] | Initial capture |
| 2026-04-08 | [REFINED] | Precise schema, update protocol, consistency enforcement defined |

---

## Refinement Session Log

**Session:** s2026-04-08-architect-TECH-003  
**Date:** 2026-04-08  
**Participants:** Architect mode

**Key Decisions:**

1. **Location confirmed:** `memory-bank/hot-context/RELEASE.md` (already created, existing file is valid)
2. **Schema precision:** Defined exact table structures and field requirements
3. **Update protocol:** Defined when and how to update RELEASE.md
4. **Consistency enforcement:** Defined GitHub Actions workflow requirements
5. **Artifact relationships:** Clarified how RELEASE.md interacts with EXECUTION-TRACKER, DOC-5-CURRENT, Git tags

**Open Points:**
- Whether to also have a root-level RELEASE.md for human discoverability (recommendation: no, memory-bank/hot-context is sufficient)
- Whether CHANGELOG.md should be deprecated or kept as legacy reference (recommendation: deprecate, point to DOC-5)

**Next Step:** Implementation of release-consistency-check.yml and .clinerules update.
