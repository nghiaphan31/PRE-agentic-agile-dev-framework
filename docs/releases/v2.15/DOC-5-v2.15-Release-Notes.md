---
doc_id: DOC-5
release: v2.15
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-04-09
authors: [Architect mode, Developer mode, Human]
previous_release: v2.14
cumulative: false
type: release-specific
---

# DOC-5 — Release Notes (v2.15)

> **Status: DRAFT** -- This document is under construction for v2.15 release.
> **Release-Specific: YES** -- This document contains ONLY v2.15 changes.
> **Cumulative: NO** -- This is NOT a cumulative changelog. For historical release notes, see `docs/releases/vX.Y/DOC-5-vX.Y-Release-Notes.md`.

---

## What's New in v2.15

v2.15 is a **Governance Enforcement Release** focused on mechanical enforcement of GitFlow rules, orchestrator as default entry point, and workflow automation.

### Features

| Feature | Description | IDEA/TECH |
|---------|-------------|-----------|
| Orchestrator Default Mode | Auto-switch to Orchestrator at session start via RULE 16.5 | IDEA-027 |
| `--no-ff` Merge Enforcement | GitHub Actions workflow validates merge commits have 2 parents | TECH-007 |
| GitFlow Naming Corrections | `stabilization/vX.Y`, `main`, excised `release/vX.Y.Z` | TECH-004 ext |
| Refining Workflow | Strategy B: `lab/` → `feature/` → `develop` Z-pattern | TECH-004 ext |

---

## IDEA-027: Orchestrator as Default Entry Point

### Summary

IDEA-027 establishes the Orchestrator as the authoritative default mode, with an auto-switch directive at session start.

### Key Changes

- RULE 16.5: Auto-switch to Orchestrator at session start via `switch_mode("orchestrator")`
- `switch_mode` confirmed to work autonomously — no dummy task required (TECH-006)

### Files Modified

- `.clinerules`: Added RULE 16.5 auto-switch directive

---

## TECH-007: `--no-ff` Merge Enforcement

### Summary

TECH-007 provides mechanical enforcement of RULE 10.3's `--no-ff` merge strategy mandate.

### Key Changes

**New Files:**
- `.github/workflows/require-merge-commit.yml`: GitHub Actions workflow

**Mechanism:**
- Triggers on PR close event
- Verifies merge commit has exactly 2 parents
- Fails PR merge check if squash/ff merge attempted

**Compliance:**
- RULE 10.3 now has GitHub-level enforcement
- All merge commits to `develop`, `stabilization/vX.Y`, and `main` must use `--no-ff`

---

## TECH-004 Extension: ADR-006-AMEND-001

### Summary

ADR-006-AMEND-001 corrects GitFlow naming inconsistencies and excises the deprecated `release/vX.Y.Z` concept.

### Key Changes

**Naming Corrections:**
- `develop-vX.Y` → `stabilization/vX.Y` (scoped release branch)
- `master` → `main` (production branch)
- `release/vX.Y.Z` → EXCISED (dual-buffer concept removed)

**New Pattern:**
- Refining Workflow Strategy B: `lab/{Timebox}/{slug}` → `feature/{Timebox}/{IDEA-NNN}-{slug}` → `develop`

**Files Modified:**
- `.clinerules` RULE 10 (branch table, workflow sections)
- `plans/governance/ADR-006-develop-main-branching.md`
- `memory-bank/hot-context/systemPatterns.md`

---

## Known Issues

| Issue | Status | Resolution |
|-------|--------|------------|
| v2.11 cumulative docs gap | KNOWN | DOC-1 and DOC-2 for v2.11 were never created — historical gap documented in ADR-024 |
| template/.clinerules sync | PENDING | Developer mode to sync RULE 10/12 naming |

---

**Previous Release:** [DOC-5-v2.14-Release-Notes.md](../v2.14/DOC-5-v2.14-Release-Notes.md)
