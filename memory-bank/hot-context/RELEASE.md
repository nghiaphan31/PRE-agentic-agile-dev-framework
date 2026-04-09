# Release Tracking

**Current Released Version:** v2.14.0
**Current Draft Version:** v2.15 (on branch develop)

---

## Released Versions

| Version | Tag | Release Date | Branch | Status | DOC-5 Path |
|---------|-----|--------------|--------|--------|------------|
| v1.0 | v1.0.0 | 2026-03-28 | main | Frozen | docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md |
| v2.0 | v2.0.0 | 2026-03-29 | main | Frozen | docs/releases/v2.0/DOC-5-v2.0-Release-Notes.md |
| v2.1 | v2.1.0 | 2026-04-01 | main | Frozen | docs/releases/v2.1/DOC-5-v2.1-Release-Notes.md |
| v2.2 | v2.2.0 | 2026-04-02 | main | Frozen | docs/releases/v2.2/DOC-5-v2.2-Release-Notes.md |
| v2.3 | v2.3.0 | 2026-04-03 | main | Frozen | docs/releases/v2.3/DOC-5-v2.3-Release-Notes.md |
| v2.4 | v2.4.0 | 2026-04-03 | main | Frozen | docs/releases/v2.4/DOC-5-v2.4-Release-Notes.md |
| v2.5 | v2.5.0 | 2026-04-04 | main | Frozen | docs/releases/v2.5/DOC-5-v2.5-Release-Notes.md |
| v2.6 | v2.6.0 | 2026-04-05 | main | Frozen | docs/releases/v2.6/DOC-5-v2.6-Release-Notes.md |
| v2.7 | v2.7.0 | 2026-04-05 | main | Frozen | docs/releases/v2.7/DOC-5-v2.7-Release-Notes.md |
| v2.8 | v2.8.0 | 2026-04-06 | main | Frozen | docs/releases/v2.8/DOC-5-v2.8-Release-Notes.md |
| v2.9 | v2.9.0 | 2026-04-06 | main | Frozen | docs/releases/v2.9/DOC-5-v2.9-Release-Notes.md |
| v2.10 | v2.10.0 | 2026-04-07 | main | Frozen | docs/releases/v2.10/DOC-5-v2.10-Release-Notes.md |
| v2.11 | v2.11.0 | 2026-04-07 | main | Frozen | docs/releases/v2.11/DOC-5-v2.11-Release-Notes.md |
| v2.12 | v2.12.0 | 2026-04-08 | main | Frozen | docs/releases/v2.12/DOC-5-v2.12-Release-Notes.md |
| v2.13 | v2.13.0 | 2026-04-08 | main | Frozen | docs/releases/v2.13/DOC-5-v2.13-Release-Notes.md |
| v2.14 | v2.14.0 | 2026-04-08 | main | Frozen | docs/releases/v2.14/DOC-5-v2.14-Release-Notes.md |

---

## Draft Version

| Version | Branch | Status | Target Release Date |
|---------|--------|--------|---------------------|
| v2.15 | develop | In Progress | TBD |

---

## v2.15 Scope

**Current draft version:** v2.15
**Status:** Draft
**Base:** v2.14.0 (most recent tag)
**Branch:** develop

### Commits Since v2.14.0

| Commit | Description | Date | IDEA/TECH |
|--------|-------------|------|-----------|
| `2076c2e` | docs(conversations): log v2.14.0 release session | 2026-04-09 | Governance |
| `fe2fc08` | docs(memory): update handoff state after v2.14.0 release | 2026-04-09 | Governance |
| `7e8d09f` | docs(memory): handoff to orchestrator after v2.14.0 release | 2026-04-09 | Governance |
| `f16fb94` | docs(memory): acknowledge handoff - v2.14.0 release confirmed | 2026-04-09 | Governance |
| `b84fa6d` | feat(governance): IDEA-027 - document Orchestrator default mode limitation | 2026-04-09 | IDEA-027 |
| `5cb149d` | docs(memory): update activeContext after IDEA-027 implementation | 2026-04-09 | IDEA-027 |
| `1c9fc81` | feat(governance): add TECH-006 for dummy task mode switch investigation | 2026-04-09 | TECH-006 |
| `2ef9816` | feat(governance): TECH-006 accepted — switch_mode works autonomously | 2026-04-09 | TECH-006 |
| `ed1e1bf` | feat(governance): TECH-006 implemented — auto-switch to Orchestrator at session start | 2026-04-09 | TECH-006 |
| `9aac166` | docs(memory): ADR-006-AMEND-001 — stabilization/vX.Y + main naming corrections | 2026-04-09 | TECH-004 ext |
| `90ee993` | chore(config): ADR-006-AMEND-001 — stabilization/vX.Y + main naming corrections | 2026-04-09 | TECH-004 ext |
| `216d7ce` | docs(memory): sync TECH-004/ADR-006 — stabilization/vX.Y + main naming, refine workflow | 2026-04-09 | TECH-004 ext |
| `6235664` | feat(TECH-007): implement --no-ff merge enforcement workflow | 2026-04-09 | TECH-007 |
| `0c366ec` | docs(memory): ADR-022 human directive override for TECH-007 | 2026-04-09 | TECH-007 |

### Features in Scope

| IDEA/TECH | Title | Status |
|-----------|-------|--------|
| IDEA-027 | Orchestrator as Default Entry Point — document limitation, RULE 16.5 auto-switch | [IMPLEMENTED] |
| TECH-006 | Dummy Task Mode Switch — `switch_mode` works autonomously, no dummy task needed | [IMPLEMENTED] |
| TECH-004 (extension) | ADR-006-AMEND-001: `stabilization/vX.Y` rename, `main` rename, Refining Workflow (Strategy B) | [ACCEPTED-EXTENSION] |
| TECH-007 | Mechanical `--no-ff` Merge Enforcement via GitHub Actions (`require-merge-commit.yml`) | [IMPLEMENTED] |

---

**Last updated:** 2026-04-09

**Source:** This is the operational source of truth for release tracking.
