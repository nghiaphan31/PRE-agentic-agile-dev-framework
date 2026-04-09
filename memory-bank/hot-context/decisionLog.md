# Decision Log

## ADR-010: Dev Tooling Process Bypass
- **Date:** 2026-04-08
- **Context:** DEVELOPER mode bypasses architectural review for tooling scripts
- **Decision:** Accept bypass as intentional design — tooling scripts are governance, not product code
- **Consequences:** Developer mode can modify scripts/proxy.py without Architect review

## ADR-011: GitFlow Violation Remediation
- **Date:** 2026-04-08
- **Context:** Commits 7cebc6f, 115cc80, f0f2418 made directly to develop instead of feature branch
- **Decision:** ADR to document violation and remediation protocol
- **Consequences:** All future work on develop must use feature branches

## ADR-012: Canonical Docs Cumulative GitFlow Enforcement
- **Date:** 2026-04-08
- **Context:** Need to enforce GitFlow on DOC-1, DOC-2, DOC-4 (cumulative docs)
- **Decision:** Implement R-CANON-1 through R-CANON-7, enforce via pre-receive hook + GitHub Actions
- **Consequences:** Canonical docs on develop only via feature branch

## ADR-013: Co-Accept IDEA-014, IDEA-015
- **Date:** 2026-04-08
- **Context:** IDEA-014 (canonical docs status governance) and IDEA-015 (mandatory release coherence audit) both ready
- **Decision:** Co-accept both, implement together
- **Consequences:** New governance ADRs, release gate workflow

## ADR-014: IDEA-030 Refinement — GitHub Actions Branch Patterns + Test Coverage

**Date:** 2026-04-09

**Context:** v2.15 consistency review identified 6 critical gaps in GitHub Actions branch triggers and test coverage.

**Decision:** IDEA-030 refined with two parts:
- Part A: Fix 3 GitHub Actions workflows to use `stabilization/v*` instead of `develop-v*`
- Part B: Create 3 new test files for branch naming, DOC-CURRENT pointers, and SP-002 sync

**Consequences:** All v2.16 release validation will use correct stabilization branch pattern.

## ADR-014: Git Hook Filename Fix for v2.13
- **Date:** 2026-04-08
- **Context:** QA blocker - docs reference `.githooks/pre-receive-merged-features` but actual file was `.githooks/pre-receive-detect`
- **Decision:** Rename file to match docs (more self-documenting name)
- **Consequences:** File renamed, docs already reference correct name

## ADR-015: R-006 Compliance Fix for v2.13
- **Date:** 2026-04-08
- **Context:** QA blocker - detect-merged-features.py line 164-166 filtered to merge commits only, violating R-006
- **Decision:** Remove `if len(parents) < 2: continue` to detect ALL commits per R-006 requirement
- **Consequences:** Script now detects all commits on develop since previous release tag

## ADR-016: v2.13 Release Decisions
- **Date:** 2026-04-08
- **Context:** v2.13.0 release completed - TECH-002 and TECH-003 fully implemented and merged
- **Decision:**
  - TECH-002 (Auto-Detect Merged Features): All options implemented - Option A (Git Hook), Option B (PR merge trigger), Option C (push/nightly), R-005 (tag-creation trigger), R-006 (all commits detection)
  - TECH-003 (Single Source of Truth): RELEASE.md established as sole authoritative source, release-consistency-check.yml workflow deployed, .clinerules RULE 2 updated
  - Fast-forward merge from feature branches to develop completed successfully
- **Consequences:** v2.14 planning can begin; all release tracking now governed by RELEASE.md

## ADR-017: TECH-005 Timebox-First Naming Correction
- **Date:** 2026-04-08
- **Context:** Original TECH-005 used wrong pattern `feature/{IDEA-NNN}/{YYYY}Q{N}-{slug}` — creates hundreds of single-branch folders. User correction: `feature/{Timebox}/{IDEA-NNN}-{slug}` groups by timebox instead.

## ADR-018: TECH-007 `--no-ff` Enforcement Capture
- **Date:** 2026-04-09
- **Context:** RULE 10.3 mandates `--no-ff` but has zero mechanical enforcement. Human asked "How do we enforce --no-ff?"
- **Decision:** Capture as TECH-007 [IDEA] with 3 options: GitHub Actions workflow (A), pre-receive hook (B), or both (C)
- **Consequences:** TECH-007 created, backlog updated, awaiting human refinement choice
- **Decision:** Correct TECH-005 pattern; status updated to [REFINED]
- **Consequences:** TECH-005 awaiting ACCEPTED/REJECTED decision. If accepted, RULE 10.1 feature branch naming will change.

## ADR-018: IDEA-026 Session Lifecycle Automation
- **Decision:** Implement 4 components:
  1. .vscode/tasks.json with Start/Stop/Status heartbeat tasks
  2. RULE 2 item 7: conversation logging before attempt_completion
  3. .github/workflows/conversation-check.yml CI validation
  4. .github/workflows/heartbeat-check.yml CI validation
- **Consequences:** Heartbeat and conversation logging now automated with CI enforcement

## ADR-018: TECH-004 Master Traceability Tree — Deferred to v2.15
- **Date:** 2026-04-08
- **Context:** TECH-004 proposes extending ADR-006 with lab/, bugfix/, release/ branches and refining workflow
- **Decision:** DEFER to v2.15
- **Rationale:**
  - ADR-006 implemented 2026-03-28 — too soon for another GitFlow change
  - v2.14 should be stabilization, not feature expansion
  - TECH-004 concepts are sound but timing is wrong
- **Concepts Accepted (for v2.15):**
  - `lab/` branch type for ad-hoc experimental work
  - `bugfix/` branch type for pre-release cold fixes
  - Refining workflow (lab→feature→develop Z-pattern)
- **Concepts Deferred:**
  - `release/vX.Y.Z` buffer branch (vs develop-vX.Y dual-buffer complexity)
  - Release parallelism (develop continues while release stabilizes)
- **Implementation:** See docs/conversations/REFINEMENT-2026-04-08-TECH-004.md
- **Consequences:** RULE 10 extension planned for v2.15; no immediate changes required

## ADR-019: TECH-004 Re-Refinement — `--no-ff` Extracted for v2.14

- **Date:** 2026-04-08
- **Context:** User feedback identified two critical elements missing from original TECH-004 refinement: (1) `--no-ff` merge strategy, (2) naming convention analysis
- **Decision:** PARTIAL AMENDMENT to ADR-018
- **Key Findings:**
  1. `--no-ff`: NOT currently mandated in ADR-006/RULE 10. TECH-004 requires it for all Planned Dev, Ad-Hoc, and Cold Fix branches. **CHANGE MAGNITUDE: MINIMAL** — single directive addition to RULE 10
  2. Naming convention `feature/YYYY/QN/T-xxx-name`: BREAKING CHANGE vs ADR-006's `feature/{IDEA-NNN}-{slug}`. Requires broader design evaluation
- **Revised Decision:**
  - TECH-004 DEFERRED to v2.15 (unchanged)
  - **`--no-ff` ACCEPTED as standalone RULE 10 amendment for v2.14** — traceability benefit, separable from naming convention, low implementation risk
  - Naming convention DEFERRED — hybrid pattern discovered: `feature/{IDEA-NNN}/{YYYY}Q{N}-{slug}` — captured as TECH-005
- **Implementation Path:**
  - v2.14: Accept `--no-ff` only (1-sentence RULE 10 change)
  - v2.15: Implement TECH-004 branch types + refining workflow + TECH-005 hybrid naming

## ADR-020: v2.15 Consistency Review Findings
- **Date:** 2026-04-09
- **Context:** Comprehensive review of v2.15 governance system consistency across rules, scripts, docs, and processes.
- **Decision:** Identified 42 findings across 5 review phases:
  - 13 CRITICAL issues including GitHub Actions triggers using wrong branch naming (`develop-v*` vs `stabilization/v*`), stale DOC-CURRENT pointers, missing test coverage
  - 12 MAJOR issues including pre-receive hook bugs, IDEA-022 journey inconsistencies, checkpoint_heartbeat.py bugs
  - 17 MINOR issues
- **Consequences:**
  - 9 P0 action items must be addressed before next release
  - 10 P1 action items for v2.16
  - 8 P2 action items when convenient
  - Same `develop-v*` vs `stabilization/v*` issue persists from v2.13 without fix
- **Status:** OPEN — P0 items pending
- **Consequences:** RULE 10 will be updated in v2.14 with `--no-ff` mandate; TECH-005 created for naming pattern evaluation

## ADR-020: TECH-004/005 User Override — Full Acceptance
- **Date:** 2026-04-08
- **Context:** User decided to accept full implementation including TECH-004's lab/ and bugfix/ branch types (contrary to original deferral to v2.15)
- **Decision:** ACCEPT TECH-004 branch types (lab/, bugfix/) and TECH-005 despite original deferral decision
- **Scope Accepted:**
  - TECH-004: lab/, bugfix/ branch types and --no-ff merge strategy for v2.14
  - TECH-004: release/ buffer branch and parallelism remain DEFERRED to v2.15
  - TECH-005: Timebox-first naming convention feature/{Timebox}/{IDEA-NNN}-{slug}
- **Consequences:** RULE 10.1 branch type table will be updated; TECH-004/TECH-005 status updated to [ACCEPTED] in backlogs

## ADR-006-AMEND-001: Naming Corrections — stabilization/vX.Y + main
- **Date:** 2026-04-09
- **Context:** TECH-004 (Master Traceability Tree) and ADR-006 (GitFlow/RULE 10) sync resolved as **MERGE with EXCISION**. Two naming corrections approved by human during sync session (see `docs/conversations/SYNC-TECH-004-ADR-006-2026-04-09.md`).
- **Decision:**
  1. **`develop-vX.Y` → `stabilization/vX.Y`** — The scoped release branch is renamed to `stabilization/vX.Y`. It is a **permanent artifact** (NOT timeboxed), kept after merge for traceability. The `stabilization/` prefix unambiguously signals release preparation, not active development.
  2. **`master` → `main`** — Standard Git convention. `main` is the canonical production branch (renamed 2026-04-09).
  3. **`release/vX.Y.Z` EXCISED** — The separate release stabilization buffer concept is removed. `stabilization/vX.Y` subsumes this role. No dual-buffer complexity.
  4. **Refining Workflow (Strategy B) added** — `lab/{Timebox}/{slug}` → `feature/{Timebox}/{IDEA-NNN}-{slug}` → `develop` Z-pattern documented in `memory-bank/hot-context/systemPatterns.md`.
- **Supersedes:** ADR-006 (2026-03-28) branch table and RULE 10.1 branch definitions
- **Files Updated:**
  - `.clinerules` RULE 10 (all `develop-vX.Y` → `stabilization/vX.Y`, `release/vX.Y.Z` row excised)
  - `plans/governance/ADR-006-develop-main-branching.md` (renames applied throughout)
  - `memory-bank/hot-context/systemPatterns.md` (Refining Workflow added — done by Architect)
  - `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md` (TECH-004 → [ACCEPTED-EXTENSION] — done by Architect)
- **Consequences:**
  - All agents MUST use `stabilization/vX.Y` (not `develop-vX.Y`) for scoped release branches
  - `main` is the sole production branch name going forward
  - `release/vX.Y.Z` pattern is deprecated and must not be created
  - Refining Workflow (Strategy B) is now a documented pattern in systemPatterns.md
  
  ## ADR-019: TECH-007 Refinement — Option A Selected
  - **Date:** 2026-04-09
  - **Context:** TECH-007 refined — human selected Option A (GitHub Actions workflow only)
  - **Decision:** Implement `.github/workflows/require-merge-commit.yml` — triggers on PR close, verifies merge commit has 2 parents
  - **Rationale:** Simpler than pre-receive hook, works on GitHub.com, visible in PR checks
  - **Consequences:** TECH-007 status updated to [REFINED], implementation specification added
  
  ## ADR-020: TECH-007 Implementation Complete
  - **Date:** 2026-04-09
  - **Context:** Developer mode implemented `.github/workflows/require-merge-commit.yml`
  - **Decision:** Workflow created — triggers on PR close, verifies merge commit has exactly 2 parents
  - **Consequences:** TECH-007 status updated to [IMPLEMENTED], RULE 10.3 now has mechanical enforcement

## ADR-022: TECH-007 Human Directive Override (2026-04-09)

**Decision:** Human chose [D] to accept TECH-007 implementation as-is.

**Rationale:** Direct response to governance question "How do we enforce --no-ff?" — valid expedited path per RULE 13.2.

**Note:** Normal sync detection with ADR-019/ADR-020 was bypassed. Human accepts this.

**Status:** TECH-007 [IMPLEMENTED]

## ADR-023: RELEASE.md Backlog Maintenance Failure — Post-v2.14.0 (2026-04-09)

- **Date:** 2026-04-09
- **Context:** Human identified that `memory-bank/hot-context/RELEASE.md` was never updated after the v2.14.0 release. The "Commits Since v2.14.0" and "Features in Scope" tables were empty despite 14 commits having landed on `develop` since the tag. This is a maintenance failure: TECH-002 (`scripts/detect-merged-features.py`) was implemented specifically to auto-detect merged features and prevent this gap, but the RELEASE.md update step was not triggered.
- **Decision:**
  1. Populate RELEASE.md v2.15 scope retroactively with all 14 commits (IDEA-027, TECH-006, TECH-004 extension, TECH-007, and 4 governance handoff commits).
  2. Document this failure as an ADR to create institutional memory.
  3. Identify root cause: TECH-002 detects commits but does NOT automatically write to RELEASE.md — the agent must do so manually per RULE 2. The agent failed to execute RULE 2 item 6 ("RELEASE.md update") after the v2.14.0 release session.
- **Root Cause:** RULE 2 item 6 was not executed at the close of the v2.14.0 release task. The Scrum Master and Developer agents both closed their sessions without populating the v2.15 draft scope.
- **Consequences:**
  - RELEASE.md v2.15 scope is now populated (retroactive fix applied this session).
  - All agents MUST execute RULE 2 item 6 at task close, especially after a release tag is created.
  - TECH-002 auto-detection is a detection tool, not a write tool — human or agent must still update RELEASE.md.
  - Future consideration: TECH-002 could be extended to auto-write RELEASE.md draft scope (new IDEA candidate).
  
  ## ADR-024: v2.11 Cumulative Docs Gap — Historical Issue (2026-04-09)
  
  - **Date:** 2026-04-09
  - **Context:** QA REJECTED v2.15 due to P0-2: v2.11 cumulative docs (DOC-1, DOC-2) are missing. Investigation revealed:
    - `docs/releases/v2.11/DOC-1-v2.11-PRD.md` — **DOES NOT EXIST**
    - `docs/releases/v2.11/DOC-2-v2.11-Architecture.md` — **DOES NOT EXIST**
    - `docs/releases/v2.11/DOC-3-v2.11-Implementation-Plan.md` — EXISTS (release-specific)
    - `docs/releases/v2.11/DOC-4-v2.11-Operations-Guide.md` — EXISTS (cumulative)
    - `docs/releases/v2.11/DOC-5-v2.11-Release-Notes.md` — EXISTS (release-specific)
  - **Decision:** This is a **historical gap** — DOC-1 and DOC-2 for v2.11 were never created. Per RULE 8.2, frozen release docs must not be retroactively modified. This gap is documented as a known issue.
  - **Consequences:**
    - R-CANON-7 pointer consistency check (`DOC-1-CURRENT` → v2.13, `DOC-2-CURRENT` → v2.13, `DOC-4-CURRENT` → v2.12 → **FIXED to v2.13 by P0-1**) is now consistent.
    - v2.11 cumulative docs gap cannot be remediated retroactively — frozen release docs are immutable.
    - This gap represents a pre-IDEA-017 violation (before canonical docs cumulative requirement was established).
    - No action required — the inconsistency is a closed historical case.
