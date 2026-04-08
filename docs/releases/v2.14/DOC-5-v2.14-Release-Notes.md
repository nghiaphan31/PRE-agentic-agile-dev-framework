---
doc_id: DOC-5
release: v2.14
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-04-08
authors: [Developer mode, Human]
previous_release: v2.13
cumulative: false
type: release-specific
---

# DOC-5 — Release Notes (v2.14)

> **Status: DRAFT** -- This document is under construction for v2.14 release.
> **Release-Specific: YES** -- This document contains ONLY v2.14 changes.
> **Cumulative: NO** -- This is NOT a cumulative changelog. For historical release notes, see `docs/releases/vX.Y/DOC-5-vX.Y-Release-Notes.md`.

---

## What's New in v2.14

v2.14 is an **Enhanced GitFlow Release** focused on improved branch naming conventions and traceability.

### Features

| Feature | Description | TECH |
|---------|-------------|------|
| Master Traceability Tree — Enhanced Git Flow | New branch types (lab/, bugfix/, release/) for better traceability | TECH-004 |
| Timebox-First Branch Naming Convention | `feature/{Timebox}/{IDEA-NNN}-{slug}` pattern for grouping | TECH-005 |
| Session Lifecycle Automation | Wire heartbeat and conversation logging | IDEA-026 |
| --no-ff Merge Requirement | Enforced merge commits for full traceability | TECH-004 |

---

## TECH-004: Master Traceability Tree — Enhanced Git Flow

### Summary

TECH-004 extends ADR-006 with new branch types and workflows for better traceability from experimental work through production deployment.

### Key Changes

**New Branch Types:**
- `lab/{Timebox}/{slug}` — Experimental spike or research
- `bugfix/{Timebox}/{Ticket}-{slug}` — Planned bug fix (pre-release)
- `release/vX.Y.Z` — Release stabilization buffer

**New Workflows:**
- RULE 10.4: Ad-Hoc Workflow (Lab-to-Feature Refining) with two strategies
- RULE 10.6: Release Buffer Parallelism

**Traceability:**
- `--no-ff` merge requirement ensures explicit merge commits
- Hot vs Cold fix separation (hotfix/ vs bugfix/)

---

## TECH-005: Timebox-First Branch Naming Convention

### Summary

TECH-005 introduces timebox-based branch naming for better organization of feature branches.

### Key Changes

**Pattern:**
```
feature/{Timebox}/{IDEA-NNN}-{slug}
```

**Examples:**
- `feature/2026-Q2/IDEA-101-authentication`
- `feature/Sprint-42/IDEA-101-authentication`

**Benefits:**
- Temporal grouping by quarter or sprint
- IDEA traceability preserved via prefix
- Forward-compatible (existing branches don't need rename)

---

## IDEA-026: Session Lifecycle Automation

### Summary

IDEA-026 wires the heartbeat and conversation logging automation using checkpoint_heartbeat.py.

### Key Changes

- VS Code task configuration for session-end triggers
- CI workflows for automated conversation logging
- RULE 2 trigger integration

---

## TECH-002: Auto-Detect Merged Features for Release Scope

### Summary

TECH-002 provides automated detection of features merged to `develop` since the last release tag. This ensures no feature is inadvertently excluded from release scope.

### Key Changes

**New Files:**
- `.githooks/pre-receive-merged-features`: Pre-receive hook for real-time merge detection
- `scripts/detect-merged-features.py`: Python script for programmatic detection
- `.github/workflows/detect-merged-features.yml`: GitHub Actions workflow for scheduled/on-demand detection

**R-006 Compliance:**
- The scope of the next release MUST include ALL commits on `develop` since the previous release tag
- Detection uses Git tags as authoritative boundary
- Any exclusion requires ADR documentation

### Usage

```bash
# Run detection manually
python scripts/detect-merged-features.py --since-tag v2.12.0 --branch develop

# Verify scope completeness
git log v2.12.0..develop --oneline
```

### Benefits

- **Completeness**: No merged feature is inadvertently excluded from a release
- **Traceability**: Every commit since the last release is accounted for
- **Auditability**: Release scope can be verified against `git log`

---

## TECH-003: Single Source of Truth for Release Tracking

### Summary

TECH-003 establishes `memory-bank/hot-context/RELEASE.md` as the authoritative source for release state, replacing scattered sources (CHANGELOG.md, DOC-5-CURRENT.md, Git tags).

### Key Changes

**New/Updated Files:**
- `memory-bank/hot-context/RELEASE.md`: Single source of truth for release tracking
- `.github/workflows/release-consistency-check.yml`: GitHub Actions workflow for consistency enforcement

**Schema:**
- `Current Released Version`: Latest version with tag on main
- `Current Draft Version`: Version currently in development
- `Released Versions`: Table of all released versions
- `Draft Version`: Current draft version info
- `vX.Y Scope`: Per-version scope section with commits and features

### Enforcement

The `release-consistency-check.yml` workflow enforces:
1. RELEASE.md existence and schema validation
2. Git tag consistency with RELEASE.md
3. DOC-5-CURRENT.md consistency with RELEASE.md
4. Frozen docs existence for released versions
5. DOC-3-CURRENT.md consistency

---

## Breaking Changes

*(None for v2.13 - governance tooling release)*

---

## Bug Fixes

*(None for v2.13 - governance tooling release)*

---

## Known Limitations

| Issue | Description | Workaround |
|-------|-------------|------------|
| Git hook requires manual deployment | `.githooks/pre-receive-merged-features` is not automatically deployed | Use GitHub Actions as primary enforcement |
| Detection may have false positives | Non-feature commits detected | Human review step in scope update protocol |

---

## Upgrade Notes

v2.13 is a governance-focused release with no breaking changes to existing functionality.

**Agent Behavior Changes:**
- Agents now read `memory-bank/hot-context/RELEASE.md` at session start for release state
- Release scope is auto-detected from Git history
- Consistency checks run on PR and tag push

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-08 | Initial draft for v2.13 | Developer mode |
| 2026-04-08 | Add TECH-002 details | Developer mode |
| 2026-04-08 | Add TECH-003 details | Developer mode |
| 2026-04-08 | Add R-006 enforcement details | Developer mode |
| 2026-04-08 | Add release-consistency-check.yml details | Developer mode |

---

**End of DOC-5 Release Notes (v2.13)**