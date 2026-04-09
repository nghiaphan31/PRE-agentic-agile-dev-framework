---
doc_id: DOC-3
release: v2.15
status: Draft
title: Implementation Plan
version: 1.0
date_created: 2026-04-09
authors: [Architect mode, Developer mode, Human]
previous_release: v2.14
cumulative: false
type: release-specific
---

# DOC-3 — Implementation Plan (v2.15)

> **Status: DRAFT** -- This document is under construction for v2.15 release.
> **Release-Specific: YES** -- This document contains ONLY v2.15 implementation scope.
> **Cumulative: NO** -- This is NOT a cumulative document. Historical implementation details are preserved in `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md`.

---

## Table of Contents

1. [v2.15 Release Scope](#1-v215-release-scope)
2. [Key Implementation Decisions](#2-key-implementation-decisions)
3. [Execution Tracking](#3-execution-tracking)
4. [Dependencies and Risks](#4-dependencies-and-risks)

---

## 1. v2.15 Release Scope

v2.15 is a **Governance Enforcement Release** focused on mechanical enforcement of GitFlow rules, orchestrator as default entry point, and workflow automation.

### Features in Scope

| IDEA/TECH | Title | Status |
|-----------|-------|--------|
| IDEA-027 | Orchestrator as Default Entry Point | [IMPLEMENTED] |
| TECH-006 | Dummy Task Mode Switch — `switch_mode` autonomous | [IMPLEMENTED] |
| TECH-004 (extension) | ADR-006-AMEND-001: `stabilization/vX.Y` rename, `main` rename, Refining Workflow | [ACCEPTED-EXTENSION] |
| TECH-007 | `--no-ff` Merge Enforcement via GitHub Actions | [IMPLEMENTED] |

### Commits Since v2.14.0

| Commit | Description | Date |
|--------|-------------|------|
| `2076c2e` | docs(conversations): log v2.14.0 release session | 2026-04-09 |
| `fe2fc08` | docs(memory): update handoff state after v2.14.0 release | 2026-04-09 |
| `7e8d09f` | docs(memory): handoff to orchestrator after v2.14.0 release | 2026-04-09 |
| `f16fb94` | docs(memory): acknowledge handoff - v2.14.0 release confirmed | 2026-04-09 |
| `b84fa6d` | feat(governance): IDEA-027 - document Orchestrator default mode limitation | 2026-04-09 |
| `5cb149d` | docs(memory): update activeContext after IDEA-027 implementation | 2026-04-09 |
| `1c9fc81` | feat(governance): add TECH-006 for dummy task mode switch investigation | 2026-04-09 |
| `2ef9816` | feat(governance): TECH-006 accepted — switch_mode works autonomously | 2026-04-09 |
| `ed1e1bf` | feat(governance): TECH-006 implemented — auto-switch to Orchestrator at session start | 2026-04-09 |
| `9aac166` | docs(memory): ADR-006-AMEND-001 — stabilization/vX.Y + main naming corrections | 2026-04-09 |
| `90ee993` | chore(config): ADR-006-AMEND-001 — stabilization/vX.Y + main naming corrections | 2026-04-09 |
| `216d7ce` | docs(memory): sync TECH-004/ADR-006 — stabilization/vX.Y + main naming, refine workflow | 2026-04-09 |
| `6235664` | feat(TECH-007): implement --no-ff merge enforcement workflow | 2026-04-09 |
| `0c366ec` | docs(memory): ADR-022 human directive override for TECH-007 | 2026-04-09 |

---

## 2. Key Implementation Decisions

### ADR-006-AMEND-001: GitFlow Naming Corrections

- **`develop-vX.Y` → `stabilization/vX.Y`** — Scoped release branch renamed for clarity
- **`master` → `main`** — Standard Git convention adopted
- **`release/vX.Y.Z` EXCISED** — Dual-buffer concept removed; `stabilization/vX.Y` subsumes this role
- **Refining Workflow (Strategy B)** — `lab/` → `feature/` → `develop` Z-pattern documented

### TECH-007: `--no-ff` Enforcement

- GitHub Actions workflow `.github/workflows/require-merge-commit.yml`
- Triggers on PR close, verifies merge commit has exactly 2 parents
- RULE 10.3 now has mechanical enforcement

### IDEA-027: Orchestrator as Default Entry Point

- RULE 16.5 added: auto-switch to Orchestrator at session start
- `switch_mode("orchestrator")` works autonomously — no dummy task needed

---

## 3. Execution Tracking

### IDEA-027: Orchestrator as Default Entry Point

| Step | Description | Status |
|------|-------------|--------|
| 1 | Document limitation in IDEA-027 | DONE |
| 2 | Add RULE 16.5 auto-switch directive | DONE |
| 3 | Verify switch_mode autonomy (TECH-006) | DONE |

### TECH-006: Dummy Task Mode Switch

| Step | Description | Status |
|------|-------------|--------|
| 1 | Investigate switch_mode autonomy | DONE |
| 2 | Confirm switch_mode works without dummy task | DONE |
| 3 | Document in TECH-006 refinement | DONE |

### TECH-004 Extension: ADR-006-AMEND-001

| Step | Description | Status |
|------|-------------|--------|
| 1 | Sync TECH-004 with ADR-006 via sync session | DONE |
| 2 | Apply `develop-vX.Y` → `stabilization/vX.Y` rename in .clinerules | DONE |
| 3 | Apply `master` → `main` rename throughout | DONE |
| 4 | Excise `release/vX.Y.Z` row from RULE 10.1 | DONE |
| 5 | Update template/.clinerules (PENDING — Developer mode) | PENDING |

### TECH-007: `--no-ff` Merge Enforcement

| Step | Description | Status |
|------|-------------|--------|
| 1 | Create `.github/workflows/require-merge-commit.yml` | DONE |
| 2 | Implement PR close trigger with 2-parent verification | DONE |
| 3 | Update RULE 10.3 enforcement section | DONE |

---

## 4. Dependencies and Risks

### Dependencies

- TECH-004 extension (ADR-006-AMEND-001) requires template/.clinerules sync — delegated to Developer mode
- TECH-007 requires GitHub Actions to be enabled on the repository

### Risks

- **Risk:** `template/.clinerules` not synced with `.clinerules` — template deployed to new projects would have stale GitFlow rules
- **Mitigation:** Developer mode to update template/.clinerules RULE 10 and RULE 12
