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

