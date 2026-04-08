---
id: IDEA-015
title: Mandatory Release Coherence Audit
status: [ACCEPTED]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: docs/qa/, .github/workflows/
captured: 2026-04-01
captured_by: Developer mode
refined_by: Architect mode
refinement_session: REFINEMENT-2026-04-08-003
---

## Problem Statement

The coherence audit is currently a **reactive process** performed after releases are tagged. The v2.6 release had 14 P0, 17 P1, and 14 P2 findings — issues that should have been caught **before** the release was tagged.

**Root Cause:** No mandatory coherence gate exists in the release workflow. Audits are performed ad-hoc via batch scripts (`plans/batch-full-audit/`), but they are not enforced as a prerequisite for release tagging.

## Motivation

Given the workbench's complexity (5 canonical docs, 10 system prompts, 3 config files, 15+ rules, multiple scripts), systematic coherence violations can accumulate undetected. The ADR-011 established the batch API audit infrastructure, but it remains opt-in rather than mandatory.

## Classification

- **Type:** GOVERNANCE
- **Tier:** Minor (process improvement, tooling already exists)
- **Release Path:** AD-HOC per ADR-010

---

## Refined Requirements

### 1. Release Gate Requirements

The following checks **MUST PASS** before a release can be tagged:

| Check | Severity Gate | Description |
|-------|---------------|-------------|
| `.clinerules` vs `prompts/SP-002-clinerules-global.md` byte-for-byte sync | **P0 BLOCKER** | Per RULE 6.2, these must match. Any deviation blocks release. |
| All 5 canonical docs meet minimum line counts | **P0 BLOCKER** | DOC-1/2/4 ≥ 500/500/300 lines (cumulative); DOC-3/5 ≥ 100/50 lines (release-specific) |
| Cumulative doc pointers consistent | **P0 BLOCKER** | DOC-1, DOC-2, DOC-4 must all reference the same version |
| No P0 findings from batch coherence audit | **P0 BLOCKER** | Zero P0 severity issues allowed |
| P1 findings formally triaged or deferred | **P1 WARNING** | P1 issues must have ENH entries or explicit deferral |

### 2. Scope: What's IN

- **GitHub Actions release gate workflow** triggered on `develop-v*` branch push
- **Automated SP-002 sync check** using `scripts/check-prompts-sync.ps1`
- **Line count validation** (already exists in `canonical-docs-check.yml`, extend to gate)
- **P0/P1/P1 findings tracking** in QA report
- **DOC-4 update** documenting the new release gate procedure

### 3. Scope: What's OUT

- Full batch coherence audit as part of the CI gate (too expensive/time-consuming per CI run)
- Modifying the Anthropic Batch API audit scripts (they work fine, just not enforced)
- Retroactive re-auditing of already-released versions
- Real-time coherence monitoring during development (post-release enhancement)

### 4. Dependencies

| IDEA | Dependency Type | Reason |
|------|----------------|--------|
| [IDEA-017](IDEA-017-docs-must-be-cumulative-self-contained.md) | Dependency | Canonical docs line count infrastructure is prerequisite |
| [IDEA-011](IDEA-011-fix-sp002-coherence.md) | Dependency | SP-002 sync check script is prerequisite |
| [ADR-011](docs/ideas/ADR-010-dev-tooling-process-bypass.md) | Dependency | Batch API audit infrastructure established |

### 5. Implementation Complexity

- **Score:** 3/10
- **Reasoning:** Infrastructure already exists (`canonical-docs-check.yml`, `check-prompts-sync.ps1`, batch audit scripts). This IDEA adds enforcement gates and automates the existing manual audit process.

---

## Acceptance Criteria

### AC-1: Release Gate Workflow Exists
- [ ] `.github/workflows/release-gate.yml` created
- [ ] Workflow triggers on push to `develop-v*` branches
- [ ] Workflow runs `scripts/check-prompts-sync.ps1` and validates SP-002 sync
- [ ] Workflow checks line counts for all 5 canonical docs
- [ ] Workflow verifies cumulative doc pointer consistency

### AC-2: Zero P0 Blocker Policy Enforced
- [ ] If SP-002 sync check fails → workflow fails (hard error)
- [ ] If line counts below minimums → workflow fails (hard error)
- [ ] If cumulative pointers inconsistent → workflow fails (hard error)
- [ ] P1 issues must be documented in release QA report (soft warning)

### AC-3: Documentation Updated
- [ ] DOC-4 (Operations Guide) updated with release gate procedure
- [ ] Release gate procedure documented in DOC-3 (Implementation Plan)
- [ ] RULE 13 updated to reference mandatory release gate

### AC-4: QA Report Integration
- [ ] QA report format includes "Pre-release Gate Checklist" section
- [ ] P0/P1/P2 findings must be explicitly marked as "pre-gate" or "post-gate"
- [ ] Gate pass/fail status recorded in release QA report

---

## Affected Documents

| Document | Change Required |
|----------|-----------------|
| `.github/workflows/release-gate.yml` | **NEW** — Release gate workflow |
| `scripts/check-prompts-sync.ps1` | Already exists — ensure it exits with code 1 on failure |
| `DOC-4-v2.7-Operations-Guide.md` | Add "Release Gate Procedure" chapter |
| `DOC-3-v2.7-Implementation-Plan.md` | Document release gate in pre-release phase |
| `.clinerules` (RULE 13) | Add reference to mandatory release gate |

---

## Next Steps

1. **Implementation**: Create `.github/workflows/release-gate.yml` (extend existing `canonical-docs-check.yml`)
2. **Documentation**: Update DOC-4 with release gate procedure
3. **Documentation**: Update DOC-3 with release gate in pre-release checklist
4. **Rules Update**: Update RULE 13 to reference the mandatory release gate

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human remark |
| 2026-04-08 | [REFINED] | Refined with acceptance criteria, scope, dependencies, and implementation plan |

---
