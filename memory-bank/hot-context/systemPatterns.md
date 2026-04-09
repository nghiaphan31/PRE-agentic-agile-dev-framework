# System Patterns

## Directory Architecture
[Paste your project directory tree here]

## Naming Conventions
- Files: [convention, e.g.: kebab-case]
- Variables: [convention, e.g.: camelCase]
- Classes: [convention, e.g.: PascalCase]
- Constants: [convention, e.g.: UPPER_SNAKE_CASE]

## Adopted Technical Patterns
- [Pattern 1: e.g.: Repository Pattern for data access]
- [Pattern 2: e.g.: Service Layer for business logic]

## Anti-Patterns to Avoid
- [Anti-pattern 1]

## Refining Workflow (Strategy B)

The **Refining Workflow** (Strategy B from TECH-004) enables experimental lab work to be refined into production features through a Z-pattern workflow: `lab → feature → develop`.

```mermaid
gitGraph
    %% 1. INITIALIZATION & PRODUCTION
    commit id: "v1.0.0-Live" tag: "v1.0.0"
    
    branch develop
    checkout develop
    commit id: "Sprint-Start-Q2"

    %% 2. FEATURE LOOP (Timeboxed for Q2)
    branch "feature/2026-Q2/T-101-Auth"
    checkout "feature/2026-Q2/T-101-Auth"
    commit id: "T101: Init-Auth"
    commit id: "T101: JWT-Impl"
    checkout develop
    merge "feature/2026-Q2/T-101-Auth" id: "Merge-T101-Auth"

    %% 3. AD-HOC STRATEGY A (Timeboxed Lab directly promoted)
    branch "lab/2026-Q2/Spike-AI"
    checkout "lab/2026-Q2/Spike-AI"
    commit id: "Lab: Neural-POC"
    checkout develop
    merge "lab/2026-Q2/Spike-AI" id: "PROMOTE: Lab-to-Dev"

    %% 4. AD-HOC STRATEGY B (Timeboxed Lab refined into Timeboxed Feature)
    branch "lab/2026-Q2/Spike-GQL"
    checkout "lab/2026-Q2/Spike-GQL"
    commit id: "Lab: GQL-Schema"
    
    checkout develop
    branch "feature/2026-Q2/T-102-Refined"
    checkout "feature/2026-Q2/T-102-Refined"
    merge "lab/2026-Q2/Spike-GQL" id: "REFINE: Consume-Lab"
    commit id: "T102: Final-Cleanup"
    
    checkout develop
    merge "feature/2026-Q2/T-102-Refined" id: "Merge-T102"

    %% 5. COLD FIX (Timeboxed Bugfix)
    branch "bugfix/2026-Q2/T-305-UI"
    checkout "bugfix/2026-Q2/T-305-UI"
    commit id: "T305: Fix-CSS"
    checkout develop
    merge "bugfix/2026-Q2/T-305-UI" id: "Merge-T305"

    %% 6. THE STABILIZATION ZONE (NOT Timeboxed - Permanent Artifact)
    branch "stabilization/v2.3"
    checkout "stabilization/v2.3"
    commit id: "Stabilize: QA Pass 1"
    commit id: "Stabilize: Fix-Regression"
    
    %% 7. PARALLELISM: develop continues next sprint (New Timebox!)
    checkout develop
    branch "feature/2026-Q3/T-200"
    checkout "feature/2026-Q3/T-200"
    commit id: "START-Q3"

    %% 8. DEPLOY FINAL RELEASE
    checkout main
    merge "stabilization/v2.3" id: "PUBLISH-v2.3.0" tag: "v2.3.0"
    
    %% 9. BACK-PORT POLISH TO DEVELOP
    checkout develop
    merge "stabilization/v2.3" id: "Sync-Polish-to-Dev"

    %% 10. HOTFIX (NOT Timeboxed - High Visibility Diamond Pattern)
    checkout main
    branch "hotfix/T-202-CVE"
    checkout "hotfix/T-202-CVE"
    commit id: "T202: CVE-Patch"
    
    checkout main
    merge "hotfix/T-202-CVE" id: "PROD-v2.3.1" tag: "v2.3.1"
    
    checkout develop
    merge "hotfix/T-202-CVE" id: "Sync-to-Dev"
```

### Z-Pattern: lab → feature → develop

The Z-pattern describes the git merge path for Strategy B:

1. **lab/{Timebox}/{slug}** — Experimental spike, branched from `develop`
2. **feature/{Timebox}/{IDEA-NNN}-{slug}** — Refined feature, branched from `develop`, consumes lab via merge
3. **develop** — Receives refined feature via PR merge

This pattern preserves traceability from experiment to product while keeping experimental work isolated until production-ready.

### Branch Naming Conventions

| Branch Type | Pattern | Example |
|-------------|---------|---------|
| Feature | `feature/{Timebox}/{IDEA-NNN}-{slug}` | `feature/2026-Q2/IDEA-101-authentication` |
| Lab (Spike) | `lab/{Timebox}/{slug}` | `lab/2026-Q2/Spike-GraphQL` |
| Bugfix | `bugfix/{Timebox}/{Ticket}-{slug}` | `bugfix/2026-Q2/T-305-UI-Align` |
| Hotfix | `hotfix/{Ticket}` | `hotfix/T-202-DB-Leak` |
| Stabilization | `stabilization/vX.Y` | `stabilization/v2.3` |

> **Note:** `stabilization/vX.Y` replaces the previous `release/vX.Y.Z` concept. Stabilization is NOT timeboxed — it is a permanent artifact that exists until the release is published to `main`.
