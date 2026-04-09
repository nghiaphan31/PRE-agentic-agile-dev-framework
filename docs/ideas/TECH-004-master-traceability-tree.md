# TECH-004: Master Traceability Tree — Enhanced Git Flow with Full Traceability

**Status:** [RELEASED-v2.15] — Extension of ADR-006. Branch types (lab/, bugfix/), stabilization/vX.Y naming, Refining Workflow (lab→feature→develop) implemented via ADR-006-AMEND-001.
**Captured:** 2026-04-08
**Source:** User discussion with Gemini
**Classification:** TECHNICAL (How)
**Supersedes:** TECH-001, TECH-002, TECH-003 (unrelated)
**Potential Overlap:** ADR-006 (develop/main branching model)
**Released:** v2.15 (ADR-006-AMEND-001)

---

## Summary

An enhanced Git branching strategy that provides comprehensive traceability from initial lab experiments through production deployment, with explicit handling of ad-hoc work, formal features, release stabilization, and emergency fixes.

## Motivation

The current GitFlow (ADR-006) provides clean branch naming but lacks:
1. Explicit handling of ad-hoc/experimental work (lab branches)
2. Clear "refining" workflow for converting experiments into production features
3. Hot vs. Cold fix separation with distinct merge paths
4. Visual "diamond" patterns for emergency production fixes
5. Release buffer parallelism (develop continues while release is stabilized)

## Detailed Proposal

### The Master Traceability Tree

```mermaid
gitGraph
    %% 1. PRODUCTION (Target)
    commit id: "v1.0.0-Live" tag: "v1.0.0"
    
    %% 2. RELEASE BUFFER (The "Gatekeeper")
    branch "release/v1.1.0"
    
    %% 3. INTEGRATION (The Highway)
    branch develop
    checkout develop
    commit id: "Sprint-Start-Q2"

    %% 4. PLANNED DEVELOPMENT: FEATURE/
    branch "feature/2026/Q2/T-101-Auth"
    checkout "feature/2026/Q2/T-101-Auth"
    commit id: "T101: Init-Auth"
    commit id: "T101: JWT-Implementation"
    checkout develop
    merge "feature/2026/Q2/T-101-Auth" id: "Merge-T101-Auth-Loop"

    %% 5. AD-HOC STRATEGY A: DIRECT PROMOTION (Lab-to-Dev)
    branch "lab/2026/Spike-AI-Engine"
    checkout "lab/2026/Spike-AI-Engine"
    commit id: "Lab: Neural-Net-POC"
    commit id: "Lab: Weights-FineTune"
    %% Decided: This is production-ready logic.
    checkout develop
    merge "lab/2026/Spike-AI-Engine" id: "PROMOTION: Lab-AI-to-Develop"

    %% 6. AD-HOC STRATEGY B: FORMALIZED FEATURE (Refining)
    branch "lab/2026/Spike-GQL-API"
    checkout "lab/2026/Spike-GQL-API"
    commit id: "Lab: GQL-Schema-Draft"
    commit id: "Lab: Messy-Resolvers"
    
    %% Now we refine it using a Feature branch
    checkout develop
    branch "feature/2026/Q2/T-102-GQL-Refined"
    checkout "feature/2026/Q2/T-102-GQL-Refined"
    commit id: "T102: Industrial-Arch"
    %% The "Traceability Bridge": Feature consumes the Lab
    merge "lab/2026/Spike-GQL-API" id: "Refine: Consume-GQL-Lab"
    commit id: "T102: Final-Cleanup"
    
    %% Merge refined work to develop
    checkout develop
    merge "feature/2026/Q2/T-102-GQL-Refined" id: "Merge-T102-Refined"

    %% 7. COLD FIX: BUGFIX/ (Pre-Release)
    branch "bugfix/T-305-UI-Alignment"
    checkout "bugfix/T-305-UI-Alignment"
    commit id: "T305: Fix-CSS-Grid"
    checkout develop
    merge "bugfix/T-305-UI-Alignment" id: "Merge-T305-UI-Fix"

    %% 8. THE RELEASE LIFECYCLE (THE STABILIZATION BENEFIT)
    checkout "release/v1.1.0"
    merge develop id: "Pull-All-Sprint-Work-to-v1.1"
    
    %% PARALLELISM: Dev team starts next sprint while QA tests release
    checkout develop
    commit id: "START-SPRINT-Q3"
    branch "feature/2026/Q3/T-200-New-Dashboard"
    checkout "feature/2026/Q3/T-200-New-Dashboard"
    commit id: "T200: Early-Work"
    
    %% RELEASE POLISH: Work happening in isolation
    checkout "release/v1.1.0"
    commit id: "Rel: Update-Release-Notes"
    commit id: "Rel: Fix-QA-Found-Bug"
    
    %% FINAL DEPLOY
    checkout main
    merge "release/v1.1.0" id: "PUBLISH-V1.1.0" tag: "v1.1.0"
    
    %% MANDATORY BACK-PORT (Sync the polish back to active dev)
    checkout develop
    merge "release/v1.1.0" id: "Sync-Rel-v1.1-into-Dev"

    %% 9. HOTFIX: HOTFIX/ (The Emergency Lane)
    checkout main
    branch "hotfix/T-202-Security-Patch"
    checkout "hotfix/T-202-Security-Patch"
    commit id: "T202: Patch-CVE-X"
    
    %% Instant update to Prod
    checkout main
    merge "hotfix/T-202-Security-Patch" id: "PROD-V1.1.1" tag: "v1.1.1"
    
    %% Instant update to Dev (Traceability: Fix doesn't get lost)
    checkout develop
    merge "hotfix/T-202-Security-Patch" id: "Sync-T202-Security-to-Dev"
```

---

## Key Traceability Concepts

### 1. The "Refining" Logic (Strategy B)

In the diagram, look at `feature/...-GQL-Refined`:
- It explicitly merges the `lab/` branch **first** to consume the logic
- It then merges into `develop`
- **Result:** When you look at the visual graph, you see a "Z" shaped flow where the experiment flows into the feature, and the feature flows into the product. You never lose the "messy" research code, but the product history remains clean.

### 2. The Release Buffer Parallelism

Note that between the `Pull-All-Sprint-Work` and `PUBLISH-V1.1.0` commits, the **Develop** branch has already branched off into `feature/2026/Q3/T-200`.

- **Benefit:** Your "Real Time" representation shows two independent paths of travel. One path is calm and focused on fixing release bugs; the other is the high-energy start of the next quarter.

### 3. Hot vs. Cold Fix Separation

| Fix Type | Branch Pattern | Merge Path | Visual Pattern |
|----------|---------------|------------|----------------|
| **Cold** (`bugfix/T-305`) | Pre-release bug | `develop` → `release` → `main` | Linear pipeline |
| **Hot** (`hotfix/T-202`) | Emergency from prod tag | Branches from `main` tag, merges to both `main` AND `develop` | Diamond shape |

---

## Traceability Naming Convention Summary

| Category | Branch Path Pattern | Permanent Trace Method |
|:---------|:-------------------|:----------------------|
| **Planned Dev** | `feature/YYYY/QN/T-xxx-name` | `--no-ff` Merge Loop |
| **Ad-Hoc (Direct)** | `lab/YYYY/Spike-name` | Direct `--no-ff` Merge into Develop |
| **Ad-Hoc (Refined)** | `lab/` → `feature/` | Lab merged into Feature, Feature merged into Dev |
| **Release** | `release/vX.X.X` | Staged merge (Dev → Release → Main) |
| **Cold Fix** | `bugfix/T-xxx-name` | `--no-ff` Merge into Develop |
| **Hot Fix** | `hotfix/T-xxx-name` | Dual Merge (Main & Develop) + Tagging |

---

## Relationship to ADR-006

ADR-006 defines the high-level branch model:
- `main` (frozen production)
- `develop` (wild mainline)
- `develop-vX.Y` (scoped backlog)
- `feature/{IDEA-NNN}-{slug}`
- `hotfix/vX.Y.Z`

**TECH-004 extends ADR-006** by adding:
1. `lab/` branch type for ad-hoc exploration
2. `bugfix/` branch type for pre-release cold fixes
3. `release/vX.Y.Z` branch for release stabilization buffer
4. Explicit "refining" workflow (lab → feature)
5. Release parallelism (develop continues while release stabilizes)

---

## Integration Points

- **RULE 10 (GitFlow):** May need extension to include `lab/`, `bugfix/`, and `release/` branch lifecycle
- **ADR-006:** TECH-004 is additive to ADR-006, not a replacement
- **memory-bank/systemPatterns.md:** New pattern for lab-to-feature workflow

---

## Next Steps

- [x] Architect review: Evaluate feasibility and complexity
- [x] Sync with ADR-006 author to ensure compatibility
- [x] Decision: ACCEPTED / REJECTED / NEEDS_MORE_INFO
- [x] Implemented: Update RULE 10 and systemPatterns.md via ADR-006-AMEND-001

## Release History

| Version | Date | Components |
|---------|------|------------|
| v2.14 | 2026-04-08 | Branch types (lab/, bugfix/) and --no-ff merge strategy accepted |
| v2.15 | 2026-04-09 | ADR-006-AMEND-001: stabilization/vX.Y rename, main rename, Refining Workflow (lab→feature→develop) |
