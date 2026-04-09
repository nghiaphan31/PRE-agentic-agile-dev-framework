# ADR-006: Adopt `develop` / `stabilization/vX.Y` / `main` Branching Model

**Status:** Draft  
**Date:** 2026-03-28  
**Authors:** Architect + Human  
**Supersedes:** ADR-005 (RULE 10 branch lifecycle — partially)  
**Location:** This file → `memory-bank/hot-context/decisionLog.md` (permanent ADR)

---

## Context

The current GitFlow (ADR-005) has a fundamental naming problem:

- `release/v2.3` was created as the **active development branch** but its name implies it is a branch *preparing a release*
- Development work was committed directly to `release/v2.3`, making it indistinguishable from a `develop` branch
- `release/v2.1` and `release/v2.2` had the same problem — they were used for active development, not release preparation
- Canonical docs were committed directly to `main` after the v2.1/v2.2 tags, violating RULE 10

This creates confusion: when someone sees `release/v2.3`, they cannot tell if it's:
- A branch preparing v2.3 for release (minimal commits, finalization work), or
- The active development branch for the next release

Additionally, a single `develop` branch conflates two different modes:
- **Ad-hoc exploration**: experimental features, quick fixes, no formal scope
- **Disciplined release preparation**: a curated backlog of IDEAs scoped for a specific version

---

## Decision

Adopt a **3-branch model** with distinct roles:

```
main             ← Frozen production state. Tags mark releases.
develop          ← Wild mainline. Any feature lands here, any time.
stabilization/vX.Y ← Scoped backlog + release stabilization. Created when IDEAS are formally triaged for vX.Y.
```

### Branch Roles

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state. **Frozen.** Only receives merge commits from `stabilization/vX.Y` branches at release time. Tags mark releases. | Never deleted. Never committed to directly. |
| `develop` | **Wild mainline.** Ad-hoc features, experiments, quick fixes — any feature, any time. No formal scope. | Long-lived. Never deleted. Always the base for `stabilization/vX.Y` branches. |
| `stabilization/vX.Y` | **Scoped backlog + release stabilization.** Created when a set of IDEAs is formally triaged for vX.Y. All release-scope work and release polish lands here. **Permanent artifact** — NOT timeboxed. | Long-lived during development. Merged to `main` at release. Never deleted after merge — kept for traceability. |
| `feature/{Timebox}/{IDEA-NNN}-{slug}` | Single feature or fix. Timebox: `YYYY-QN` (Quarter) or `Sprint-NN`. **Active Dev.** | Branch from `develop` (ad-hoc) or `stabilization/vX.Y` (scoped), merge back via PR, then delete. Examples: `feature/2026-Q2/IDEA-101-authentication`, `feature/Sprint-42/IDEA-101-authentication` |
| `lab/{Timebox}/{slug}` | Experimental spike or research. **Active Dev.** Timebox: `YYYY-QN` (Quarter) or `Sprint-NN`. | Branch from `develop`, merge back or archive when sprint ends. Examples: `lab/2026-Q2/Spike-GraphQL`, `lab/Sprint-42/Spike-Auth` |
| `bugfix/{Timebox}/{Ticket}-{slug}` | Planned bug fix (not emergency). **Active Dev.** Timebox: `YYYY-QN` (Quarter) or `Sprint-NN`. | Branch from `stabilization/vX.Y` or `develop`, merge back via PR. Examples: `bugfix/2026-Q2/T-305-UI-Align`, `bugfix/Sprint-42/T-310-API-Timeout` |
| `hotfix/{Ticket}` | Emergency production fix. **Production.** No timebox — tied to semantic version. | Branched from the production tag on `main`. Merged to `main` and `develop`, then deleted. Example: `hotfix/T-202-DB-Leak` |

### The `vX.Y` Version — Two and Only Two Long-Lived Contexts

The version number `vX.Y` appears in exactly **two long-lived places** and **one short-lived place**:

1. **Git tag** — `v2.3.0` is a lightweight tag marking a commit on `main`. No development happens on a tag.

2. **Frozen docs folder** — `docs/releases/v2.3/` is created **after** the tag is applied, as a permanent historical record. It is **never edited** after creation (RULE 8).

3. **Scoped backlog branch** — `stabilization/v2.3` exists for the duration of the v2.3 development cycle (weeks to months), and is **never deleted** after merge to `main` (kept for traceability). It is the **only** long-lived branch that carries a version number.

### When `stabilization/vX.Y` Exists

```
develop ─────────────────────────────────────────────────────── (wild mainline, always alive)
   │
   ├── feature/2026-Q2/IDEA-009 ── PR ── merge ──► develop  (ad-hoc, anytime)
   │
   └── stabilization/v2.3 ──────────────────────────────────────────── (scoped backlog + release polish, weeks/months)
           │
           ├── feature/2026-Q2/IDEA-010 ── PR ── merge ──► stabilization/v2.3  (scoped)
           ├── feature/2026-Q2/IDEA-011 ── PR ── merge ──► stabilization/v2.3  (scoped)
           ├── bugfix/2026-Q2/T-305-UI ── PR ── merge ──► stabilization/v2.3  (scoped)
           ├── lab/2026-Q2/Spike-GraphQL ── PR ── merge ──► stabilization/v2.3  (scoped)
           │
           └── merge ──────────────────────────────────────► main  (v2.3.0 tag)
                   │
                   └── [stabilization/v2.3 KEPT — never deleted]
                            │
develop ─────────────────────────────────────────────────────── (continues)
    │
    └── stabilization/v2.4 ── branch from develop  (next cycle)
```

`stabilization/vX.Y` is created only when:
1. A set of IDEAs has been formally triaged and approved for vX.Y scope
2. The human authorises the scoped backlog branch
3. It is **never deleted** after merge to `main` — kept permanently for traceability

### Why `develop` AND `stabilization/vX.Y`?

The separation enforces discipline:

| | `develop` | `stabilization/vX.Y` |
|--|--|--|
| **Scope** | Any feature, any time | Only IDEAs approved for vX.Y |
| **When created** | Once, at project start | When vX.Y backlog is triaged |
| **When deleted** | Never | Never (permanent artifact) |
| **Features** | Wild, exploratory | Disciplined, scoped |
| **Canonical docs** | N/A | Required before merge |

---

## Consequences

### Positive
- **Unambiguous naming:** `develop` = wildcard, `stabilization/vX.Y` = scoped release work
- **Never commit to `main`:** RULE 10 enforced naturally — `main` only touched at release merges
- **Clean history:** `develop` shows the full ad-hoc story; `main` only shows release merges
- **Canonical docs on `stabilization/vX.Y`:** Release docs created on the scoped branch before merge to `main`
- **Disciplined scoping:** A version branch only exists when IDEAS have been formally triaged for it
- **Permanent traceability:** `stabilization/vX.Y` is kept after merge — never deleted

### Negative
- **Branch rename required:** `release/v2.3` (current) → `develop` (wild mainline)
- **ADR-005 lifecycle table changes:** RULE 10 must be replaced entirely
- **Existing branches** `release/v1.0`, `release/v2.0`, `release/v2.1`, `release/v2.2` remain as historical records

### Risks
- Confusion between `develop` and `stabilization/vX.Y` until the team adapts. Mitigation: clear naming and RULE 10 documentation.
- If `stabilization/vX.Y` is abandoned without merging, its work is not lost — it can be cherry-picked or merged to `develop`.

---

## Implementation

### Phase 1: Immediate (this session)
1. Rename `release/v2.3` → `develop` (current branch becomes the wild mainline)
2. Update RULE 10 in `.clinerules` to reflect the 3-branch model
3. Update `.roomodes` if any agent references branch names
4. Update `prompts/SP-002-clinerules-global.md` embedded template
5. Update `template/.clinerules`
6. Commit as `chore(governance): ADR-006 — adopt develop/main model with scoped stabilization/vX.Y branches`
7. Push `develop` to origin

### Phase 2: First scoped branch
- When IDEAS-BACKLOG is formally triaged for v2.3, create `stabilization/v2.3` from `develop`
- All v2.3-scope work lands on `stabilization/v2.3`

### Phase 3: Documentation
1. Update `PLAN-release-governance.md` to supersede ADR-005's branch table
2. At v2.3 release: create `docs/releases/v2.3/` folder on `stabilization/v2.3`, merge to `main`

---

## Diff: RULE 10 Replacement

**Current RULE 10.1 (ADR-005):**

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `master` | Production state — frozen after each release tag | NEVER commit directly after tag |
| `release/vX.Y` | Release branch — all planned work for vX.Y | CLOSED after merge to master |
| `release/vX.Y+1` | Next release branch | ACTIVE — all new work lands here |
| `hotfix/vX.Y.Z` | Emergency fixes from production tag | Merged to master + active release |

**Proposed RULE 10.1:**

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state. **Frozen.** Only receives merge commits from `stabilization/vX.Y`. Tags mark releases. | Never deleted. Never committed to directly. |
| `develop` | **Wild mainline.** Ad-hoc features, experiments, quick fixes. No formal scope. | Long-lived. Never deleted. Always the base for `stabilization/vX.Y`. |
| `stabilization/vX.Y` | **Scoped backlog + release stabilization.** Created when IDEAs are formally triaged for vX.Y. All release-scope work and release polish lands here. **Permanent artifact** — NOT timeboxed. | Created at release planning. Never deleted after merge — kept for traceability. |
| `feature/{Timebox}/{IDEA-NNN}-{slug}` | Single feature or fix. Timebox: `YYYY-QN` (Quarter) or `Sprint-NN`. **Active Dev.** | Branch from `develop` or `stabilization/vX.Y`, merge back via PR, then delete. Examples: `feature/2026-Q2/IDEA-101-authentication`, `feature/Sprint-42/IDEA-101-authentication` |
| `lab/{Timebox}/{slug}` | Experimental spike or research. **Active Dev.** Timebox: `YYYY-QN` (Quarter) or `Sprint-NN`. | Branch from `develop`, merge back or archive when sprint ends. Examples: `lab/2026-Q2/Spike-GraphQL`, `lab/Sprint-42/Spike-Auth` |
| `bugfix/{Timebox}/{Ticket}-{slug}` | Planned bug fix (not emergency). **Active Dev.** Timebox: `YYYY-QN` (Quarter) or `Sprint-NN`. | Branch from `stabilization/vX.Y` or `develop`, merge back via PR. Examples: `bugfix/2026-Q2/T-305-UI-Align`, `bugfix/Sprint-42/T-310-API-Timeout` |
| `hotfix/{Ticket}` | Emergency production fix. **Production.** No timebox — tied to semantic version. | Branched from production tag on `main`. Merged to `main` and `develop`, then deleted. Example: `hotfix/T-202-DB-Leak` |

---

## Supersession

ADR-006 **supersedes ADR-005** regarding branch naming and lifecycle. The vX.Y versioning concept and the tag/frozen-docs folder structure remain unchanged from ADR-005.

Recorded in: `memory-bank/hot-context/decisionLog.md`  
Review date: At v3.0 release planning
