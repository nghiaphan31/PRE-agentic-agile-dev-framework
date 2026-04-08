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

## ADR-017: IDEA-026 Session Lifecycle Automation
- **Date:** 2026-04-08
- **Context:** IDEA-019 implemented checkpoint_heartbeat.py with --log-conversation, but automation was not wired
- **Decision:** Implement 4 components:
  1. .vscode/tasks.json with Start/Stop/Status heartbeat tasks
  2. RULE 2 item 7: conversation logging before attempt_completion
  3. .github/workflows/conversation-check.yml CI validation
  4. .github/workflows/heartbeat-check.yml CI validation
- **Consequences:** Heartbeat and conversation logging now automated with CI enforcement

