# QA Report — v2.15 Human Journey & GitFlow Consistency Review

**Date:** 2026-04-09  
**Reviewer:** Scrum Master  
**Scope:** Human Journey (IDEA-022), GitFlow Enforcement (ADR-006-AMEND-001), Development Process, Mode Switching (RULE 16)  
**Sources reviewed:**
- [`docs/ideas/IDEA-022-ideation-to-release-journey.md`](../ideas/IDEA-022-ideation-to-release-journey.md)
- [`plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md`](../../plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md)
- [`docs/releases/v2.15/DOC-3-v2.15-Implementation-Plan.md`](../releases/v2.15/DOC-3-v2.15-Implementation-Plan.md)
- [`docs/releases/v2.15/DOC-5-v2.15-Release-Notes.md`](../releases/v2.15/DOC-5-v2.15-Release-Notes.md)
- [`.clinerules`](../../.clinerules) (RULE 10, RULE 16)
- [`.roomodes`](../../.roomodes)
- [`.github/workflows/release-gate.yml`](../../.github/workflows/release-gate.yml)
- [`.github/workflows/canonical-docs-check.yml`](../../.github/workflows/canonical-docs-check.yml)
- [`.github/workflows/require-merge-commit.yml`](../../.github/workflows/require-merge-commit.yml)
- [`.github/workflows/release-consistency-check.yml`](../../.github/workflows/release-consistency-check.yml)
- [`src/calypso/orchestrator_phase2.py`](../../src/calypso/orchestrator_phase2.py)
- [`src/calypso/orchestrator_phase3.py`](../../src/calypso/orchestrator_phase3.py)
- [`src/calypso/orchestrator_phase4.py`](../../src/calypso/orchestrator_phase4.py)
- [`memory-bank/hot-context/decisionLog.md`](../../memory-bank/hot-context/decisionLog.md) (ADR-006-AMEND-001)
- [`memory-bank/hot-context/systemPatterns.md`](../../memory-bank/hot-context/systemPatterns.md)
- Prior QA reports: [`QA-REPORT-v2.15-RULES-CONSISTENCY.md`](QA-REPORT-v2.15-RULES-CONSISTENCY.md), [`QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md`](QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md)

---

## Executive Summary

| Domain | Status | Critical | Major | Minor |
|--------|--------|----------|-------|-------|
| Human Journey (IDEA-022) | ⚠️ GAPS | 0 | 3 | 4 |
| GitFlow Naming Consistency | ❌ FAIL | 3 | 2 | 3 |
| Development Process | ⚠️ GAPS | 0 | 2 | 2 |
| Mode Switching (RULE 16) | ⚠️ PARTIAL | 0 | 1 | 2 |
| **TOTAL** | | **3** | **8** | **11** |

---

## Part 1: Human Journey Consistency (IDEA-022)

### 1.1 Journey Overview

IDEA-022 defines an 8-phase ideation-to-release journey. The PLAN-IDEA-022 document defines a slightly different 7-phase structure (X.2–X.9). These two documents are **not fully aligned**.

### Finding HJ-001 — Phase Count Mismatch Between IDEA-022 and PLAN-IDEA-022

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` §3.1, `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` §3 |

**Description:**

IDEA-022 §3.1 defines **8 phases** (Phase 0 through Phase 7, plus Phase 8 Hotfix):
- Phase 0: Idea Intake
- Phase 1: Idea Refinement
- Phase 2: Triage and Release Assignment
- Phase 3: Implementation Planning
- Phase 4: Development
- Phase 5: Code Review and Merge
- Phase 6: Release Preparation
- Phase 7: Release
- Phase 8: Hotfix (Exceptional Path)

PLAN-IDEA-022 §3 defines **8 sections** (X.2–X.9) but with **different phase names**:
- X.2: Phase 0 Idea Intake
- X.3: Phase 1 Idea Refinement
- X.4: Phase 2 Triage and Release Assignment
- X.5: Phase 3 Implementation Planning
- X.6: Phase 4 Development
- X.7: **Phase 5: Documentation** ← NOT in IDEA-022 §3.1
- X.8: **Phase 6: QA and Validation** ← Merged with "Code Review" in IDEA-022
- X.9: Phase 7 Release

**Gap:** IDEA-022 has "Phase 5: Code Review and Merge" and "Phase 6: Release Preparation" but PLAN-IDEA-022 replaces these with "Phase 5: Documentation" and "Phase 6: QA and Validation". The Hotfix phase (Phase 8) is in IDEA-022 but absent from PLAN-IDEA-022's TOC.

**Consequence:** An agent implementing IDEA-022 from the PLAN would produce a different chapter structure than what IDEA-022 specifies. The DOC-4 chapter would be inconsistent with the IDEA's acceptance criteria.

**Suggested Fix:** Reconcile the two documents. The PLAN should be the authoritative implementation spec and should match IDEA-022's phase definitions exactly, or IDEA-022 should be updated to reflect the PLAN's refined structure.

---

### Finding HJ-002 — IDEA-022 Uses Stale Branch Name `develop-vX.Y`

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` §3.1.5, §3.1.6, §3.1.7, §3.1.8, §3.1.9 |
| **Rule Reference** | ADR-006-AMEND-001: `develop-vX.Y` → `stabilization/vX.Y` |

**Description:**

IDEA-022 was written before ADR-006-AMEND-001 (2026-04-09) and still uses the deprecated `develop-vX.Y` branch name throughout:

- §3.1.5 Phase 3: `feature/IDEA-NNN-slug` (branched from `develop` or **`develop-vX.Y`**)
- §3.1.7 Phase 5: Feature branch merged into `develop` or **`develop-vX.Y`**
- §3.1.8 Phase 6: **`develop-vX.Y`** (WHERE field)
- §3.1.9 Phase 7: **`develop-vX.Y`** → `main`

Similarly, PLAN-IDEA-022 §X.5 uses `develop-vX.Y` in the WHERE field and §X.9 uses `develop-vX.Y` → `develop` → `main`.

**Consequence:** Any agent following IDEA-022 or PLAN-IDEA-022 to implement the journey chapter in DOC-4 would document the wrong branch names, perpetuating the deprecated naming.

**Suggested Fix:** Update all `develop-vX.Y` references to `stabilization/vX.Y` in both IDEA-022 and PLAN-IDEA-022.

---

### Finding HJ-003 — IDEA-022 Uses Stale Feature Branch Pattern

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` §3.1.5, §3.1.6 |
| **Rule Reference** | RULE 10.1 (ADR-006-AMEND-001): `feature/{Timebox}/{IDEA-NNN}-{slug}` |

**Description:**

IDEA-022 §3.1.5 and §3.1.6 reference the feature branch pattern as `feature/IDEA-NNN-slug` (no timebox). Per RULE 10.1 (updated by ADR-006-AMEND-001 and TECH-005), the correct pattern is `feature/{Timebox}/{IDEA-NNN}-{slug}` (e.g., `feature/2026-Q2/IDEA-022-ideation-journey`).

PLAN-IDEA-022 §5 PHASE A also uses the old pattern: `feature/IDEA-022-ideation-to-release-journey`.

**Consequence:** The journey documentation would teach the wrong branch naming convention.

**Suggested Fix:** Update all feature branch references to use the timebox-first pattern: `feature/{Timebox}/{IDEA-NNN}-{slug}`.

---

### Finding HJ-004 — IDEA-022 Status Is `[IDEA]` Despite Being Marked `[IMPLEMENTED]` in progress.md

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` line 8, `memory-bank/hot-context/progress.md` line 129 |

**Description:**

`progress.md` line 129 shows:
```
- [x] IDEA-022: Ideation-to-Release Journey [IMPLEMENTED]
```

But `IDEA-022-ideation-to-release-journey.md` line 8 still shows:
```
**Status:** `[IDEA]`
```

**Consequence:** The IDEA file is out of sync with the progress tracker. Per RULE 2, agents must update IDEA status in the backlog before closing a task.

**Suggested Fix:** Update IDEA-022 status to `[IMPLEMENTED]` and update `IDEAS-BACKLOG.md` accordingly.

---

### Finding HJ-005 — IDEA-022 Acceptance Criteria Not Verified

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` §5 |

**Description:**

IDEA-022 §5 lists 5 acceptance criteria, all marked `[ ]` (unchecked):
1. New chapter added to DOC-4 (v2.10) with all sections
2. Chapter is exhaustive and detailed
3. Chapter includes decision trees
4. Chapter is consistent with existing rules and tooling
5. IDEA-022 entry added to IDEAS-BACKLOG.md with status `[REFINING]`

Despite `progress.md` marking IDEA-022 as `[IMPLEMENTED]`, none of the acceptance criteria are checked off. Furthermore, the target release is `v2.10` but the current release is `v2.15` — the chapter was never added to DOC-4.

**Consequence:** IDEA-022 was marked implemented without verifying its acceptance criteria. The primary deliverable (DOC-4 chapter) does not exist.

**Suggested Fix:** Either verify the DOC-4 chapter exists (and check off criteria), or revert IDEA-022 status to `[IN-PROGRESS]` and create the chapter.

---

### Finding HJ-006 — No Entry/Exit Criteria for Hotfix Path in PLAN-IDEA-022

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` |

**Description:**

IDEA-022 §3.1.10 defines a "Phase 8: Hotfix (Exceptional Path)" with entry/exit criteria. However, PLAN-IDEA-022 has no corresponding section for the hotfix path. The TOC (§3.1) ends at X.9 (Phase 7: Release) with no hotfix section.

**Consequence:** The DOC-4 chapter, if implemented from the PLAN, would omit the hotfix path entirely — a significant operational gap for emergency production fixes.

**Suggested Fix:** Add X.10 (Hotfix Path) to PLAN-IDEA-022 matching IDEA-022 §3.1.10.

---

### Finding HJ-007 — PLAN-IDEA-022 Phase 6 (QA) Has Wrong Entry Criteria

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` §X.8 |

**Description:**

PLAN-IDEA-022 §X.8 (Phase 6: QA and Validation) states:

> **Entry Criteria:** Feature branch merged to `develop-vX.Y`

This is wrong on two counts:
1. Uses deprecated `develop-vX.Y` instead of `stabilization/vX.Y`
2. QA should happen **before** merge to the stabilization branch, not after — otherwise bugs found in QA require a second merge cycle

**Consequence:** The documented QA workflow would create unnecessary merge cycles and contradicts standard QA practice (validate before merge).

**Suggested Fix:** Change entry criteria to: "Feature branch has passing CI and is ready for merge review" — QA validates on the feature branch before merge.

---

## Part 2: GitFlow Naming Consistency

### 2.1 Summary of Branch Naming Across All Documents

| Document | `develop-vX.Y` | `stabilization/vX.Y` | `master` | `main` | Status |
|---|---|---|---|---|---|
| `.clinerules` RULE 10 | ❌ Removed | ✅ Used | ❌ Removed | ✅ Used | ✅ CORRECT |
| `prompts/SP-002` | ❌ Removed | ✅ Used | ❌ Removed | ✅ Used | ✅ CORRECT |
| `template/.clinerules` | ❌ Removed | ✅ Used | ❌ Removed | ✅ Used | ✅ CORRECT |
| `memory-bank/hot-context/systemPatterns.md` | ❌ Removed | ✅ Used | ❌ Removed | ✅ Used | ✅ CORRECT |
| `docs/releases/v2.15/DOC-3` | ❌ Removed | ✅ Used | ❌ Removed | ✅ Used | ✅ CORRECT |
| `docs/releases/v2.15/DOC-5` | ❌ Removed | ✅ Used | ❌ Removed | ✅ Used | ✅ CORRECT |
| `.github/workflows/release-gate.yml` | ✅ **STILL USED** | ❌ Missing | — | — | ❌ **WRONG** |
| `.github/workflows/canonical-docs-check.yml` | ✅ **STILL USED** | ❌ Missing | — | — | ❌ **WRONG** |
| `.github/workflows/release-consistency-check.yml` | ✅ **STILL USED** | ❌ Missing | — | — | ❌ **WRONG** |
| `docs/ideas/IDEA-022` | ✅ **STILL USED** | ❌ Missing | — | — | ❌ **WRONG** |
| `plans/IDEA-022/PLAN-IDEA-022` | ✅ **STILL USED** | ❌ Missing | — | — | ❌ **WRONG** |
| `docs/releases/v2.9/DOC-1/2/4` (cumulative) | ✅ **STILL USED** | ❌ Missing | ✅ **STILL USED** | ❌ Missing | ❌ **WRONG** |

---

### Finding GF-001 — `release-gate.yml` Triggers on `develop-v*` (CRITICAL — Already in F-001)

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **File** | `.github/workflows/release-gate.yml` lines 6, 41 |
| **Rule Reference** | ADR-006-AMEND-001 |

**Already documented in QA-REPORT-v2.15-RULES-CONSISTENCY.md as F-001.** Confirmed: the workflow will not trigger on `stabilization/v*` branches, bypassing all P0 release gate checks.

---

### Finding GF-002 — `canonical-docs-check.yml` Triggers on `develop-v*` (CRITICAL — Already in F-002)

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **File** | `.github/workflows/canonical-docs-check.yml` lines 10–11 |
| **Rule Reference** | ADR-006-AMEND-001, RULE 12.4 |

**Already documented in QA-REPORT-v2.15-RULES-CONSISTENCY.md as F-002.** Confirmed: canonical docs coherence check will not run on `stabilization/v*` branches.

---

### Finding GF-003 — `release-consistency-check.yml` Triggers on `develop-v*` (NEW — CRITICAL)

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **File** | `.github/workflows/release-consistency-check.yml` line 5 |
| **Rule Reference** | ADR-006-AMEND-001, TECH-003 |

**Description:**

`release-consistency-check.yml` line 5 shows:
```yaml
on:
  pull_request:
    branches: [main, develop, 'develop-v*']   # ← WRONG: should include 'stabilization/v*'
```

This workflow (implemented for TECH-003) checks RELEASE.md consistency on PRs targeting `develop-v*` branches. Since the branch is now `stabilization/v*`, this check will never trigger on release preparation PRs.

**Consequence:** RELEASE.md consistency is not validated during release preparation, defeating the purpose of TECH-003.

**Suggested Fix:**
```yaml
on:
  pull_request:
    branches: [main, develop, 'stabilization/v*']
```

---

### Finding GF-004 — `release-gate.yml` Version Extraction Hardcodes `develop-v` Prefix (MAJOR)

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **File** | `.github/workflows/release-gate.yml` line 41 |
| **Rule Reference** | ADR-006-AMEND-001 |

**Description:**

Even if the trigger is fixed (GF-001), the version extraction logic will still fail:
```bash
VERSION="${GITHUB_REF#refs/heads/develop-v}"
# For stabilization/v2.16, this produces: "stabilization/v2.16" (no stripping)
# Expected: "2.16"
```

**Suggested Fix:**
```bash
VERSION="${GITHUB_REF#refs/heads/stabilization/v}"
```

---

### Finding GF-005 — Cumulative Docs (v2.9) Use Deprecated Branch Names (MINOR)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `docs/releases/v2.9/DOC-1-v2.9-PRD.md`, `docs/releases/v2.9/DOC-2-v2.9-Architecture.md`, `docs/releases/v2.9/DOC-4-v2.9-Operations-Guide.md` |
| **Rule Reference** | ADR-006-AMEND-001, RULE 8.1 (Frozen docs are READ-ONLY) |

**Description:**

The latest available cumulative docs (v2.9) use `master`, `develop-vX.Y`, and `release/vX.Y.Z` throughout. These are the docs that DOC-*-CURRENT.md pointers reference (via v2.13 which has no cumulative docs).

Per RULE 8.1, frozen docs are READ-ONLY — they cannot be modified. However, since no cumulative docs exist for v2.10–v2.15, agents reading the "current" docs will encounter stale GitFlow naming.

**Consequence:** Agents reading DOC-1/2/4 for architectural guidance will see `develop-vX.Y` as the correct branch name, contradicting `.clinerules` RULE 10.

**Suggested Fix:** Create v2.15 cumulative docs (DOC-1, DOC-2, DOC-4) with updated GitFlow naming. This is already tracked as P0 in QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md.

---

### Finding GF-006 — `hotfix/vX.Y.Z` Pattern in IDEA-022 vs `hotfix/{Ticket}` in RULE 10.1 (MINOR)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` §3.1.10, `.clinerules` RULE 10.1 |

**Description:**

IDEA-022 §3.1.10 (Phase 8: Hotfix) specifies the hotfix branch as:
```
hotfix/vX.Y.Z (branched from main)
```

But RULE 10.1 defines the hotfix branch pattern as:
```
hotfix/{Ticket}   (e.g., hotfix/T-202-DB-Leak)
```

These are inconsistent. RULE 10.1 uses a ticket-based naming; IDEA-022 uses a version-based naming.

**Consequence:** Agents following IDEA-022 would create `hotfix/v2.15.1` while RULE 10.1 expects `hotfix/T-NNN-slug`.

**Suggested Fix:** Update IDEA-022 §3.1.10 to use `hotfix/{Ticket}` pattern per RULE 10.1.

---

### Finding GF-007 — `release-gate.yml` Summary Step References Wrong Merge Target (MINOR)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `.github/workflows/release-gate.yml` lines 244–248 |

**Description:**

The release gate summary step instructs:
```
4. Merge to main (fast-forward)
```

But RULE 10.5 specifies the release workflow as:
1. Tag `vX.Y.0` on `stabilization/vX.Y`
2. Merge to `main`
3. **Fast-forward `develop` to `main`** (step 5 of RULE 10.5)

The summary omits the mandatory fast-forward of `develop` to `main` after release merge (RULE 10.5 step 5).

**Suggested Fix:** Add step 5 to the summary:
```
5. Fast-forward develop to main: git checkout develop && git merge --ff main
```

---

## Part 3: Development Process Review

### 3.1 Process Consistency Across Documents

| Process Step | `.clinerules` | DOC-3 v2.15 | IDEA-022 | PLAN-IDEA-022 | Consistent? |
|---|---|---|---|---|---|
| Branch from `stabilization/vX.Y` | ✅ RULE 10.1 | ✅ | ❌ `develop-vX.Y` | ❌ `develop-vX.Y` | ❌ |
| Feature branch pattern | ✅ `feature/{Timebox}/{IDEA-NNN}-{slug}` | ✅ | ❌ `feature/IDEA-NNN-slug` | ❌ `feature/IDEA-022-...` | ❌ |
| `--no-ff` merge | ✅ RULE 10.3 | ✅ TECH-007 | ❌ Not mentioned | ❌ Not mentioned | ❌ |
| Hotfix branch pattern | ✅ `hotfix/{Ticket}` | ✅ | ❌ `hotfix/vX.Y.Z` | ❌ Not in TOC | ❌ |
| Orchestrator as default | ✅ RULE 16.5 | ✅ IDEA-027 | ❌ Not mentioned | ❌ Not mentioned | ❌ |
| Handoff protocol | ✅ RULE 16 | ✅ | ❌ Not mentioned | ❌ Not mentioned | ❌ |

---

### Finding DP-001 — IDEA-022 Journey Does Not Include Orchestrator Handoff Protocol (MAJOR)

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md`, `.clinerules` RULE 16 |

**Description:**

IDEA-022 defines the journey in terms of human roles (Product Owner, Developer, QA Engineer, Scrum Master) but makes no mention of:
- RULE 16 (Mandatory Handoff Protocol)
- The `handoff-state.md` schema
- The Orchestrator's role in routing between phases
- The `switch_mode("orchestrator")` auto-switch at session start (RULE 16.5)

RULE 16 was implemented in v2.15 (IDEA-027), but IDEA-022 was written before this and was never updated to incorporate the handoff protocol into the journey.

**Consequence:** The DOC-4 chapter produced from IDEA-022 would describe a journey without the Orchestrator coordination layer — agents following the chapter would not know to use the handoff protocol between phases.

**Suggested Fix:** Add a "Orchestrator Coordination" section to each phase in IDEA-022, describing how the Orchestrator routes between phases using `handoff-state.md`.

---

### Finding DP-002 — `--no-ff` Merge Requirement Not Documented in Journey (MAJOR)

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Files** | `docs/ideas/IDEA-022-ideation-to-release-journey.md` §3.1.5, `plans/IDEA-022/PLAN-IDEA-022-ideation-to-release-journey.md` §X.9 |
| **Rule Reference** | RULE 10.3 (TECH-007) |

**Description:**

IDEA-022 Phase 5 (Code Review and Merge) and PLAN-IDEA-022 Phase 7 (Release) describe merge operations but do not mention the `--no-ff` requirement mandated by RULE 10.3 and enforced by TECH-007.

PLAN-IDEA-022 §X.9 describes the release merge as:
> "PR merge, tag creation, release"

Without specifying `--no-ff`.

**Consequence:** Agents following the journey documentation would not know to use `--no-ff`, potentially triggering the TECH-007 GitHub Actions check failure.

**Suggested Fix:** Add explicit `--no-ff` requirement to Phase 5 (Merge) and Phase 7 (Release) in both documents.

---

### Finding DP-003 — Calypso Orchestrator Phases (2/3/4) Are Disconnected from IDEA-022 Journey (MINOR)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `src/calypso/orchestrator_phase2.py`, `src/calypso/orchestrator_phase3.py`, `src/calypso/orchestrator_phase4.py` |

**Description:**

The Calypso orchestrator phases (2/3/4) implement a PRD → Expert Review → Backlog Synthesis → Devil's Advocate pipeline. This is a **technical implementation** of the ideation pipeline, but it is not referenced anywhere in IDEA-022's journey phases.

Specifically:
- Phase 2 (`orchestrator_phase2.py`): Submits PRD to 4 expert agents (architecture, security, UX, QA) via Anthropic Batch API
- Phase 3 (`orchestrator_phase3.py`): Synthesizes expert reports into a draft backlog (SP-008 Synthesizer)
- Phase 4 (`orchestrator_phase4.py`): Devil's Advocate classification (SP-009) — GREEN/ORANGE per item

These phases correspond to IDEA-022's Phase 1 (Refinement) and Phase 2 (Triage), but the journey documentation does not reference these tools.

**Consequence:** The journey documentation is incomplete — it describes the process at a high level but does not tell users which tools to invoke at each phase.

**Suggested Fix:** Add tool references to IDEA-022 Phase 1 and Phase 2:
- Phase 1 (Refinement): "Use `orchestrator_phase2.py` for expert PRD review"
- Phase 2 (Triage): "Use `orchestrator_phase3.py` + `orchestrator_phase4.py` for backlog synthesis and classification"

---

### Finding DP-004 — DOC-3 v2.15 Has Pending Step Not Resolved Before Release (MINOR)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `docs/releases/v2.15/DOC-3-v2.15-Implementation-Plan.md` §3, Step 5 |

**Description:**

DOC-3 v2.15 §3 (TECH-004 Extension execution tracking) shows:
```
| 5 | Update template/.clinerules (PENDING — Developer mode) | PENDING |
```

v2.15.0 was tagged and released with this step still PENDING. Per RULE 14.3:
> "Never mark a step as complete if: Tests are failing / QA has not validated it / The feature branch has not been merged"

The inverse also applies: a release should not be tagged with PENDING implementation steps.

**Consequence:** `template/.clinerules` may still have stale GitFlow naming (`develop-vX.Y`, `master`) when deployed to new projects. This is confirmed by QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md §5.2 which shows template `.clinerules` IS correctly updated — so the PENDING status in DOC-3 is stale/incorrect.

**Suggested Fix:** Update DOC-3 v2.15 §3 Step 5 to DONE (template was updated per QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md §5.2).

---

## Part 4: Mode Switching Review (RULE 16)

### Finding MS-001 — RULE 16.5 Auto-Switch Instruction Is Ambiguous (MAJOR)

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **File** | `.clinerules` RULE 16.5 |

**Description:**

RULE 16.5 states:
> "**Auto-Switch Instruction:** At the start of each session, invoke `switch_mode("orchestrator")` to automatically transfer control to the Orchestrator mode. The `switch_mode` tool works autonomously — no human approval required."

This instruction is ambiguous about **which agent** should invoke `switch_mode`. The rule is in `.clinerules` which applies to ALL modes. This creates a logical paradox:

1. If the Scrum Master reads `.clinerules` at session start (RULE 1), it would immediately switch to Orchestrator before doing any work — but the Scrum Master has a legitimate task to complete
2. If the Developer reads `.clinerules`, same issue — it would switch before implementing anything
3. The Orchestrator itself cannot switch to itself

In practice, non-Orchestrator modes execute their assigned tasks without switching, which is correct behavior — but it contradicts the literal reading of RULE 16.5.

**Consequence:** Agents may interpret RULE 16.5 as requiring an immediate mode switch at every session start, even when they have been explicitly assigned a task in their current mode. This would make non-Orchestrator modes non-functional.

**Suggested Fix:** Clarify RULE 16.5 to specify it applies only when the **entry point is the human with no specific mode assignment** (i.e., the human opens a new session without specifying a mode). When a specific mode is already active with an assigned task, RULE 16.5 does not apply.

---

### Finding MS-002 — `.roomodes` Has No Orchestrator Entry or Comment (MINOR — Already in F-005)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `.roomodes` |
| **Rule Reference** | RULE 16.5 |

**Already documented in QA-REPORT-v2.15-RULES-CONSISTENCY.md as F-005.** Confirmed: `.roomodes` defines 4 Scrum roles but has no reference to the Orchestrator built-in mode, creating a documentation gap for new users.

---

### Finding MS-003 — RULE 16 Handoff Schema Not Enforced by Any Automation (MINOR)

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **Files** | `.clinerules` RULE 16.1, `memory-bank/hot-context/handoff-state.md` |

**Description:**

RULE 16.1 defines a detailed handoff state schema with fields like `handoff_id`, `from_agent.mode`, `task_completion.status`, `next_action.recommendation`, etc. However:

1. There is no GitHub Actions workflow that validates `handoff-state.md` schema
2. There is no script that validates the schema
3. The current `handoff-state.md` contains only:
   ```
   # Handoff State
   **Last updated:** 2026-04-09T08:55:32Z
   **Status:** No pending handoffs
   ```
   — which does not match the schema defined in RULE 16.1

**Consequence:** The handoff protocol is defined but not enforced. Agents may write minimal or non-conforming handoff states without detection.

**Suggested Fix:** Create a `scripts/validate-handoff-state.py` script and a GitHub Actions workflow to validate `handoff-state.md` against the RULE 16.1 schema on every push.

---

## Part 5: Consolidated Findings Summary

### 5.1 All Findings by Severity

| ID | Domain | Severity | File(s) | Issue | Status |
|---|---|---|---|---|---|
| GF-001 | GitFlow | **CRITICAL** | `release-gate.yml` | Triggers on `develop-v*` not `stabilization/v*` | Duplicate of F-001 |
| GF-002 | GitFlow | **CRITICAL** | `canonical-docs-check.yml` | Triggers on `develop-v*` not `stabilization/v*` | Duplicate of F-002 |
| GF-003 | GitFlow | **CRITICAL** | `release-consistency-check.yml` | Triggers on `develop-v*` not `stabilization/v*` | **NEW** |
| HJ-001 | Human Journey | **MAJOR** | `IDEA-022`, `PLAN-IDEA-022` | Phase count/name mismatch between documents | **NEW** |
| HJ-002 | Human Journey | **MAJOR** | `IDEA-022`, `PLAN-IDEA-022` | Uses deprecated `develop-vX.Y` branch name | **NEW** |
| HJ-003 | Human Journey | **MAJOR** | `IDEA-022`, `PLAN-IDEA-022` | Uses old feature branch pattern (no timebox) | **NEW** |
| GF-004 | GitFlow | **MAJOR** | `release-gate.yml` line 41 | Version extraction hardcodes `develop-v` prefix | **NEW** |
| DP-001 | Dev Process | **MAJOR** | `IDEA-022` | Journey missing Orchestrator handoff protocol | **NEW** |
| DP-002 | Dev Process | **MAJOR** | `IDEA-022`, `PLAN-IDEA-022` | `--no-ff` requirement not documented in journey | **NEW** |
| MS-001 | Mode Switching | **MAJOR** | `.clinerules` RULE 16.5 | Auto-switch instruction is ambiguous | **NEW** |
| HJ-004 | Human Journey | **MINOR** | `IDEA-022` | Status `[IDEA]` despite being marked `[IMPLEMENTED]` | **NEW** |
| HJ-005 | Human Journey | **MINOR** | `IDEA-022` §5 | Acceptance criteria unchecked, DOC-4 chapter missing | **NEW** |
| HJ-006 | Human Journey | **MINOR** | `PLAN-IDEA-022` | Hotfix path missing from PLAN TOC | **NEW** |
| HJ-007 | Human Journey | **MINOR** | `PLAN-IDEA-022` §X.8 | QA entry criteria wrong (merge before QA) | **NEW** |
| GF-005 | GitFlow | **MINOR** | `docs/releases/v2.9/DOC-*` | Cumulative docs use deprecated branch names | Duplicate of F-05 |
| GF-006 | GitFlow | **MINOR** | `IDEA-022` §3.1.10 | Hotfix branch pattern mismatch (`hotfix/vX.Y.Z` vs `hotfix/{Ticket}`) | **NEW** |
| GF-007 | GitFlow | **MINOR** | `release-gate.yml` summary | Missing fast-forward develop step in release instructions | **NEW** |
| DP-003 | Dev Process | **MINOR** | `orchestrator_phase2/3/4.py` | Calypso phases not referenced in IDEA-022 journey | **NEW** |
| DP-004 | Dev Process | **MINOR** | `DOC-3-v2.15` §3 | PENDING step in released DOC-3 (actually done) | **NEW** |
| MS-002 | Mode Switching | **MINOR** | `.roomodes` | Orchestrator not mentioned | Duplicate of F-005 |
| MS-003 | Mode Switching | **MINOR** | `handoff-state.md` | Handoff schema not enforced by automation | **NEW** |

### 5.2 New Findings (Not in Prior QA Reports)

| ID | Severity | Issue |
|---|---|---|
| GF-003 | CRITICAL | `release-consistency-check.yml` uses `develop-v*` instead of `stabilization/v*` |
| GF-004 | MAJOR | `release-gate.yml` version extraction hardcodes `develop-v` prefix |
| HJ-001 | MAJOR | Phase count/name mismatch between IDEA-022 and PLAN-IDEA-022 |
| HJ-002 | MAJOR | IDEA-022 and PLAN-IDEA-022 use deprecated `develop-vX.Y` branch name |
| HJ-003 | MAJOR | IDEA-022 and PLAN-IDEA-022 use old feature branch pattern (no timebox) |
| DP-001 | MAJOR | IDEA-022 journey missing Orchestrator handoff protocol (RULE 16) |
| DP-002 | MAJOR | `--no-ff` requirement not documented in IDEA-022 journey |
| MS-001 | MAJOR | RULE 16.5 auto-switch instruction is ambiguous (applies to all modes) |
| HJ-004 | MINOR | IDEA-022 status `[IDEA]` despite `progress.md` marking it `[IMPLEMENTED]` |
| HJ-005 | MINOR | IDEA-022 acceptance criteria unchecked; DOC-4 chapter never created |
| HJ-006 | MINOR | Hotfix path missing from PLAN-IDEA-022 TOC |
| HJ-007 | MINOR | PLAN-IDEA-022 §X.8 QA entry criteria wrong (merge before QA) |
| GF-006 | MINOR | Hotfix branch pattern mismatch in IDEA-022 (`hotfix/vX.Y.Z` vs `hotfix/{Ticket}`) |
| GF-007 | MINOR | `release-gate.yml` summary missing fast-forward develop step |
| DP-003 | MINOR | Calypso orchestrator phases not referenced in IDEA-022 journey |
| DP-004 | MINOR | DOC-3 v2.15 shows PENDING step that is actually done |
| MS-003 | MINOR | Handoff state schema (RULE 16.1) not enforced by any automation |

---

## Part 6: Action Items

### P0 — Critical (Must Fix Before Next Release)

| Priority | Owner | Action | Finding |
|---|---|---|---|
| P0 | Developer | Fix `release-gate.yml`: `develop-v*` → `stabilization/v*` (trigger + version extraction) | GF-001, GF-004 |
| P0 | Developer | Fix `canonical-docs-check.yml`: `develop-v*` → `stabilization/v*` | GF-002 |
| P0 | Developer | Fix `release-consistency-check.yml`: add `stabilization/v*` to PR target branches | GF-003 |

### P1 — Major (Fix in v2.16)

| Priority | Owner | Action | Finding |
|---|---|---|---|
| P1 | Developer/Architect | Update IDEA-022 and PLAN-IDEA-022: replace `develop-vX.Y` → `stabilization/vX.Y` | HJ-002 |
| P1 | Developer/Architect | Update IDEA-022 and PLAN-IDEA-022: replace feature branch pattern with timebox-first | HJ-003 |
| P1 | Architect | Reconcile phase structure between IDEA-022 and PLAN-IDEA-022 | HJ-001 |
| P1 | Architect | Add Orchestrator handoff protocol to IDEA-022 journey phases | DP-001 |
| P1 | Architect | Add `--no-ff` requirement to IDEA-022 Phase 5 and Phase 7 | DP-002 |
| P1 | Scrum Master | Clarify RULE 16.5 scope (only applies when no mode is pre-assigned) | MS-001 |

### P2 — Minor (Fix When Convenient)

| Priority | Owner | Action | Finding |
|---|---|---|---|
| P2 | Scrum Master | Update IDEA-022 status to `[IMPLEMENTED]` in IDEA file and IDEAS-BACKLOG.md | HJ-004 |
| P2 | Architect | Verify IDEA-022 acceptance criteria and check off completed items | HJ-005 |
| P2 | Architect | Add hotfix path (X.10) to PLAN-IDEA-022 | HJ-006 |
| P2 | Architect | Fix PLAN-IDEA-022 §X.8 QA entry criteria (validate on feature branch, not after merge) | HJ-007 |
| P2 | Architect | Fix hotfix branch pattern in IDEA-022 §3.1.10 (`hotfix/{Ticket}` per RULE 10.1) | GF-006 |
| P2 | Developer | Add fast-forward develop step to `release-gate.yml` summary | GF-007 |
| P2 | Architect | Add Calypso tool references to IDEA-022 Phase 1 and Phase 2 | DP-003 |
| P2 | Developer | Update DOC-3 v2.15 §3 Step 5 to DONE (template was updated) | DP-004 |
| P2 | Developer | Create handoff-state schema validation script and CI workflow | MS-003 |

---

## Part 7: Items Confirmed Correct

- ✅ `.clinerules` RULE 10 correctly uses `stabilization/vX.Y`, `main`, timebox-first feature branches
- ✅ `prompts/SP-002` is byte-for-byte identical to `.clinerules` (per prior QA)
- ✅ `template/.clinerules` correctly updated with ADR-006-AMEND-001 changes
- ✅ `memory-bank/hot-context/systemPatterns.md` correctly uses `stabilization/v2.3` in Mermaid diagram
- ✅ `docs/releases/v2.15/DOC-3` and `DOC-5` correctly use `stabilization/vX.Y` and `main`
- ✅ `.github/workflows/require-merge-commit.yml` correctly enforces `--no-ff` (TECH-007)
- ✅ `orchestrator_phase2/3/4.py` are internally consistent and do not reference branch names
- ✅ `memory-bank/hot-context/decisionLog.md` ADR-006-AMEND-001 is correctly documented
- ✅ `release-gate.yml` P0 blocker checks (SP-002 sync, line counts, cumulative flags) are correct
- ✅ `release-consistency-check.yml` RELEASE.md schema validation is correct
- ✅ RULE 16 handoff schema is well-defined (though not enforced by automation)
- ✅ IDEA-022 Phase 0 (Intake) and Phase 1 (Refinement) entry/exit criteria are well-defined
- ✅ IDEA-022 Phase 2 (Triage) sync detection decision tree is complete and correct
- ✅ PLAN-IDEA-022 Phase 0–4 entry/exit criteria are well-defined

---

**End of QA Report**