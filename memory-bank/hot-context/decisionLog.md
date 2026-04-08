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

