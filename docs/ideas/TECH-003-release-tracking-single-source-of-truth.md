# TECH-003: Single Source of Truth for Release Tracking

**Status:** PROPOSED

**Captured:** 2026-04-08

**Complexity:** 3/10

---

## Problem Statement

No authoritative location stores the latest release version. The following inconsistencies exist:

- **CHANGELOG.md** is stale (only v1.0, v2.0)
- **DOC-5-CURRENT.md** shows v2.11 but v2.12 exists
- **Git tags** are partial
- **Agents cannot reliably determine current release state**

This creates confusion during handoff, release planning, and cross-release coordination.

---

## Proposed Solution

Create `RELEASE.md` at repository root as the **SOLE authoritative source** for:

- Current released version
- Current draft version
- Full release history catalog

### Schema

```markdown
# Release Tracking

**Current Released Version:** vX.Y.Z  
**Current Draft Version:** vX.Y (on branch develop-vX.Y)

---

## Released Versions

| Version | Tag | Release Date | Branch | Status | DOC-5 Path |
|---------|-----|--------------|--------|--------|------------|
| v1.0 | v1.0.0 | 2026-03-28 | main | Frozen | docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md |
| v2.0 | v2.0.0 | 2026-03-29 | main | Frozen | docs/releases/v2.0/DOC-5-v2.0-Release-Notes.md |
| v2.1 | v2.1.0 | 2026-04-01 | main | Frozen | docs/releases/v2.1/DOC-5-v2.1-Release-Notes.md |
| v2.2 | v2.2.0 | 2026-04-02 | main | Frozen | docs/releases/v2.2/DOC-5-v2.2-Release-Notes.md |
| v2.3 | v2.3.0 | 2026-04-03 | main | Frozen | docs/releases/v2.3/DOC-5-v2.3-Release-Notes.md |
| v2.4 | v2.4.0 | 2026-04-03 | main | Frozen | docs/releases/v2.4/DOC-5-v2.4-Release-Notes.md |
| v2.5 | v2.5.0 | 2026-04-04 | main | Frozen | docs/releases/v2.5/DOC-5-v2.5-Release-Notes.md |
| v2.6 | v2.6.0 | 2026-04-05 | main | Frozen | docs/releases/v2.6/DOC-5-v2.6-Release-Notes.md |
| v2.7 | v2.7.0 | 2026-04-05 | main | Frozen | docs/releases/v2.7/DOC-5-v2.7-Release-Notes.md |
| v2.8 | v2.8.0 | 2026-04-06 | main | Frozen | docs/releases/v2.8/DOC-5-v2.8-Release-Notes.md |
| v2.9 | v2.9.0 | 2026-04-06 | main | Frozen | docs/releases/v2.9/DOC-5-v2.9-Release-Notes.md |
| v2.10 | v2.10.0 | 2026-04-07 | main | Frozen | docs/releases/v2.10/DOC-5-v2.10-Release-Notes.md |
| v2.11 | v2.11.0 | 2026-04-07 | main | Frozen | docs/releases/v2.11/DOC-5-v2.11-Release-Notes.md |
| v2.12 | v2.12.0 | 2026-04-08 | main | Frozen | docs/releases/v2.12/DOC-5-v2.12-Release-Notes.md |

---

## Draft Version

| Version | Branch | Status | Target Release Date |
|---------|--------|--------|---------------------|
| v2.13 | develop-v2.12 | In Progress | TBD |

---

## Implementation Plan

### Step 1: Create RELEASE.md (immediate)
- Create `RELEASE.md` at repository root
- Populate with v2.12.0 as last released version
- Set v2.13 as current draft on develop-v2.12

### Step 2: Update RULE 2
- Modify `.clinerules` RULE 2 to require RELEASE.md update at release close
- Add validation that RELEASE.md is updated before any release tag is created

### Step 3: GitHub Actions Consistency Check
- Add workflow to verify RELEASE.md matches:
  - Latest Git tag
  - DOC-5-CURRENT.md pointed version
  - Latest frozen docs/releases/vX.Y/ directory

---

## Affected Documents

- `.clinerules` (RULE 2 modification)
- `RELEASE.md` (new file)
- `.github/workflows/release-consistency-check.yml` (new file)

---

## Notes

- This addresses the inconsistency problem identified during v2.12 release tracking
- Ensures all agents can query the single source of truth for release state
