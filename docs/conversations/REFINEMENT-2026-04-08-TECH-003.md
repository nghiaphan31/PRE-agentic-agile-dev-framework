# Refinement Session: TECH-003

**Date:** 2026-04-08  
**Session ID:** s2026-04-08-architect-TECH-003  
**Mode:** Architect  
**Status:** COMPLETE

---

## Participants

- Architect mode (AI)
- Human (via task input)

---

## Input Context

The human requested refinement of TECH-003 (Single Source of Truth for Release Tracking), referencing:
- `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md`
- `docs/ideas/TECH-002-auto-detect-merged-features-for-release-scope.md`

The existing TECH-003 proposal (status: PROPOSED) was captured on 2026-04-08 with complexity 3/10, but lacked precise schema definitions.

---

## Discussion Summary

### Background

TECH-003 was proposed to address inconsistencies in release tracking:
- CHANGELOG.md is stale (only v1.0, v2.0)
- DOC-5-CURRENT.md shows wrong version (v2.11 vs actual v2.12)
- Git tags are partial
- Agents cannot reliably determine current release state

### Refinement Actions

1. **Schema Precision**: Defined exact table structures and field requirements for RELEASE.md
2. **Update Protocol**: Established when and how to update RELEASE.md (on release events, commits, scope changes)
3. **Consistency Enforcement**: Defined GitHub Actions workflow requirements
4. **Artifact Relationships**: Clarified how RELEASE.md interacts with EXECUTION-TRACKER, DOC-5-CURRENT, Git tags

### Key Decisions

| Decision | Rationale |
|----------|-----------|
| Location: `memory-bank/hot-context/RELEASE.md` | Already exists, hot-context is mandatory read per RULE 1 |
| No root-level RELEASE.md | Redundant, memory-bank location is sufficient for agents |
| Deprecate CHANGELOG.md | Legacy, points to DOC-5 instead |
| GitHub Actions consistency check | Enforces SSOT validity |

---

## Requirements Defined

### R-001: RELEASE.md Location
File MUST be at `memory-bank/hot-context/RELEASE.md`

### R-002: Required Sections
1. Top-level fields (Current Released Version, Current Draft Version)
2. Released Versions table (Version, Tag, Release Date, Branch, Status, DOC-5 Path)
3. Draft Version table (Version, Branch, Status, Target Release Date)
4. Scope section per draft version (Commits Since, Features in Scope)

### R-003: Update Triggers
- New release tag created
- New commit to develop
- Feature added to scope
- Version number decided

### R-004: Update Rules
- No direct commits to main
- Draft section created on release
- Atomic updates (commits + features tables together)
- Timestamp required on every update

### R-005: Consistency Enforcement
- Git tag must match RELEASE.md
- DOC-5-CURRENT.md must point to correct version
- EXECUTION-TRACKER must exist for current draft

---

## Parked Technical Suggestions

None. All technical suggestions have been addressed in the refinement.

---

## Status Transitions

| Item | From | To | Reason |
|------|------|-----|--------|
| TECH-003 | [PROPOSED] | [REFINED] | Precise schema and update protocol defined |

---

## Files Modified

| File | Change |
|------|--------|
| `docs/ideas/TECH-003-release-tracking-single-source-of-truth.md` | Updated status to REFINED, added precise schema |
| `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md` | Updated TECH-003 status to [REFINED] |

---

## Next Steps

1. **Implementation (Developer mode):**
   - Create `.github/workflows/release-consistency-check.yml`
   - Update `.clinerules` RULE 2 to include RELEASE.md update protocol

2. **Documentation (Product Owner mode):**
   - Deprecate CHANGELOG.md or mark as legacy
   - Add RELEASE.md reference to DOC-4 Operations Guide

---

**Session completed:** 2026-04-08T18:15:00Z
