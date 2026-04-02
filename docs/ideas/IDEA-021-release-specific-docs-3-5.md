# IDEA-021: Make DOC-3 and DOC-5 Release-Specific

**ID:** IDEA-021  
**Title:** Make DOC-3 and DOC-5 Release-Specific Snapshots  
**Source:** Human (direct remark)  
**Captured:** 2026-04-02  
**Status:** [IDEA]  
**Type:** governance  
**Tier:** Major  
**Target Release:** v2.10  

---

## Problem Statement

Currently, all 5 canonical docs (DOC-1 through DOC-5) are treated as cumulative documents that contain the complete history from v1.0 to the current release.

However, this approach is inappropriate for:

1. **DOC-3 (Implementation Plan)** — Should document THIS release's scope, not repeat historical plans
2. **DOC-5 (Release Notes)** — By definition, should document what changed in THIS release only

## Current vs. Recommended Classification

| Document | Current (v2.8+) | Recommended | Rationale |
|----------|-----------------|-------------|-----------|
| **DOC-1** (PRD) | Cumulative ✅ | **Cumulative** | Complete product vision and requirements across all releases |
| **DOC-2** (Architecture) | Cumulative ✅ | **Cumulative** | Complete technical design across all versions |
| **DOC-3** (Implementation Plan) | Cumulative ❌ | **Release-Specific** | Only this release's scope and execution |
| **DOC-4** (Operations Guide) | Cumulative ✅ | **Cumulative** | Complete user manual across all versions |
| **DOC-5** (Release Notes) | Cumulative ❌ | **Release-Specific** | Only this release's changes |

## Rationale

### DOC-3: Implementation Plan (Release-Specific)
- Each release's implementation plan should focus on THAT release's scope
- Historical implementation details belong in execution trackers, not in cumulative docs
- Reduces doc bloat and focuses each release on forward-looking content

### DOC-5: Release Notes (Release-Specific)
- Release notes are by definition a record of changes in a specific release
- A cumulative release notes doc becomes an endless changelog
- Each release's DOC-5 should contain only what changed in that release
- Previous release notes preserved in `docs/releases/vX.Y/DOC-5-vX.Y-Release-Notes.md`

## Proposed Changes

### RULE 12 Modification
Update RULE 12 (Canonical Docs Cumulative Requirement) to specify:

```
R-CANON-0: Cumulative requirement applies ONLY to DOC-1, DOC-2, and DOC-4
R-CANON-1: DOC-3 is release-specific — only this release's implementation scope
R-CANON-2: DOC-5 is release-specific — only this release's changes
R-CANON-3: Historical DOC-3 and DOC-5 preserved in docs/releases/vX.Y/
```

### Enforcement Updates
- `.githooks/pre-receive` — Update to enforce release-specific format for DOC-3 and DOC-5
- `.github/workflows/canonical-docs-check.yml` — Update validation logic

### Migration Plan
- v2.10: Implement release-specific DOC-3 and DOC-5
- Backward compatibility: v2.9 and earlier remain as-is (cumulative)
- Future releases only add new content to current DOC-3/5

## Affected Documents

- `.clinerules` — RULE 12 modification
- `template/.clinerules` — RULE 12 modification
- `prompts/SP-002-clinerules-global.md` — RULE 12 modification
- `.githooks/pre-receive` — Enforcement update
- `.github/workflows/canonical-docs-check.yml` — CI update
- `docs/releases/v2.10/DOC-3-v2.10-Implementation-Plan.md` — New release-specific format
- `docs/releases/v2.10/DOC-5-v2.10-Release-Notes.md` — New release-specific format

## Questions for Refinement

1. Should DOC-3 include a brief reference to previous releases' key decisions?
2. Should DOC-5 link to detailed PRs/changesets for full history?
3. Should we create a separate "Changelog" doc for cumulative change history?

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-02 | [IDEA] | Captured from human remark |

---
