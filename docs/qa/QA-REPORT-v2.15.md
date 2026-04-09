# QA REPORT — v2.15 Release Validation (RE-VALIDATION)

**QA Engineer:** QA Engineer (minimax/minimax-m2.7)  
**Date:** 2026-04-09  
**Release:** v2.15 (Draft)  
**Base:** v2.14.0  
**Branch:** `develop`  
**Commits since v2.14.0:** 14  
**Re-validation after:** P0 fixes applied by Architect

---

## Executive Summary

| Aspect | Original Status | Re-validation Status |
|--------|-----------------|---------------------|
| Coherence Audit | ❌ FAIL | ⚠️ PARTIAL |
| Feature Validation | ✅ PASS | ✅ PASS |
| Governance Check | ⚠️ PARTIAL | ⚠️ PARTIAL |
| **Overall Recommendation** | **REJECT** | **CONDITIONAL** |

**Reason:** 3 of 4 P0s are FIXED. P0-3 (template sync) is PARTIAL — `template/.clinerules` is fixed but `template/prompts/SP-002-clinerules-global.md` still uses `develop-vX.Y` naming.

---

## 1. COHERENCE AUDIT — RE-VALIDATION

### 1.1 Pointer Consistency (RULE 12.4.7)

| Pointer File | Original | Re-validation | Status |
|-------------|----------|--------------|--------|
| DOC-1-CURRENT.md | v2.13 | v2.13 | ✅ FIXED |
| DOC-2-CURRENT.md | v2.13 | v2.13 | ✅ FIXED |
| DOC-3-CURRENT.md | v2.13 | v2.15 | ✅ CORRECT (release-specific) |
| DOC-4-CURRENT.md | v2.12 | v2.13 | ✅ FIXED (P0-1) |
| DOC-5-CURRENT.md | v2.14 | v2.15 | ✅ CORRECT (release-specific) |

**RULE 12.4.7 Check:** Cumulative docs (DOC-1, DOC-2, DOC-4) now all point to v2.13. Release-specific docs (DOC-3, DOC-5) correctly point to v2.15. ✅ **PASS**

### 1.2 Cumulative Doc Line Count Audit (Unchanged)

| Release | DOC-1 | DOC-2 | DOC-3 | DOC-4 | DOC-5 |
|---------|-------|-------|-------|-------|-------|
| v2.10 | 538 ✅ | 999 ✅ | 215 ✅ | 871 ✅ | 67 ✅ |
| v2.11 | ❌ MISSING | ❌ MISSING | 159 ✅ | 871 ✅ | 72 ✅ |

**P0-2 Decision:** ADR-024 documents this as a historical gap. Per RULE 8.1 (Frozen docs are READ-ONLY), this cannot be retroactively fixed. ✅ **ACCEPTED AS DOCUMENTED KNOWN ISSUE**

### 1.3 v2.15 Release Docs

| Item | Original | Re-validation | Status |
|------|----------|----------------|--------|
| `docs/releases/v2.15/` directory | ❌ DOES NOT EXIST | ✅ EXISTS | ✅ FIXED (P0-4) |
| DOC-3-v2.15-Implementation-Plan.md | ❌ DOES NOT EXIST | ✅ EXISTS | ✅ FIXED (P0-4) |
| DOC-5-v2.15-Release-Notes.md | ❌ DOES NOT EXIST | ✅ EXISTS | ✅ FIXED (P0-4) |
| EXECUTION-TRACKER-v2.15.md | ❌ DOES NOT EXIST | ✅ EXISTS | ✅ FIXED (P0-4) |

**Per RULE 12:** All required v2.15 release docs now exist. ✅ **PASS**

---

## 2. FEATURE VALIDATION (Unchanged from Original)

### 2.1 IDEA-027 — Orchestrator Default Mode Limitation

| Check | Status | Notes |
|-------|--------|-------|
| Implementation matches spec | ✅ PASS | Documentation-only approach |
| No conflicts with other features | ✅ PASS | Isolated governance change |
| Commit on `develop` | ✅ PASS | `b84fa6d` |

### 2.2 TECH-006 — switch_mode Autonomously Works

| Check | Status | Notes |
|-------|--------|-------|
| Implementation matches spec | ✅ PASS | Auto-switch instruction added to RULE 16.5 |
| Commits on `develop` | ✅ PASS | `1c9fc81`, `2ef9816`, `ed1e1bf` |

### 2.3 TECH-004 Extension (ADR-006-AMEND-001)

| Check | Status | Notes |
|-------|--------|-------|
| `.clinerules` updated | ✅ PASS | `stabilization/vX.Y` naming |
| RULE 10.1/10.2/10.5 updated | ✅ PASS | New branch table |
| ADR-006-AMEND-001 in decisionLog | ✅ PASS | Lines 118-155 |
| Commit on `develop` | ✅ PASS | `9aac166`, `90ee993`, `216d7ce` |

### 2.4 TECH-007 — --no-ff Merge Enforcement

| Check | Status | Notes |
|-------|--------|-------|
| GitHub Actions workflow created | ✅ PASS | `.github/workflows/require-merge-commit.yml` |
| Workflow checks for 2-parent merge | ✅ PASS | Lines 31-38 verify merge commit |
| Commit on `develop` | ✅ PASS | `6235664`, `0c366ec` |

---

## 3. GOVERNANCE CHECK — RE-VALIDATION

### 3.1 SP-002 / .clinerules Synchronization

| Location | Original | Re-validation | Status |
|----------|----------|--------------|--------|
| `.clinerules` vs `prompts/SP-002-clinerules-global.md` | ✅ PASS | ✅ PASS | ✅ SYNCED |
| `template/.clinerules` | ❌ FAIL | ✅ FIXED | ✅ SYNCED (P0-3) |
| `template/prompts/SP-002-clinerules-global.md` | ❌ FAIL | ⚠️ PARTIAL | ❌ NOT SYNCED |

### 3.2 P0-3: Template Sync Status

**✅ FIXED:**
- `template/.clinerules` now correctly uses `stabilization/vX.Y` naming
- Verified at lines 493, 530, 543 — matches ADR-006-AMEND-001

**❌ STILL BROKEN:**
- `template/prompts/SP-002-clinerules-global.md` (lines 519-549) still contains:
  - `develop-vX.Y` instead of `stabilization/vX.Y`
  - Old branch table without `lab/` and `bugfix/` types
  - Missing `feature/{Timebox}/{IDEA-NNN}-{slug}` timebox format

---

## 4. BLOCKERS AND ISSUES — RE-VALIDATION

### P0 — Status After Fixes

| # | Category | Original Issue | Fix Status | Re-validation |
|---|----------|---------------|------------|---------------|
| 1 | Coherence | DOC-4 points to v2.12 | ✅ FIXED | ✅ VERIFIED — DOC-4 now points to v2.13 |
| 2 | Coherence | v2.11 cumulative docs missing | ✅ DOCUMENTED | ✅ ADR-024 in decisionLog — accepted as historical known issue |
| 3 | Governance | template/.clinerules not synced | ⚠️ PARTIAL | ⚠️ template/.clinerules FIXED, but template/prompts/SP-002 NOT synced |
| 4 | Release Docs | v2.15 docs missing | ✅ FIXED | ✅ VERIFIED — all 3 docs exist |

### Remaining Issue: P0-3 Template Prompts Not Synced

**Issue:** `template/prompts/SP-002-clinerules-global.md` (lines 519-549) still uses `develop-vX.Y` naming from the old ADR-006, not the new `stabilization/vX.Y` from ADR-006-AMEND-001.

**Evidence:**
```
Line 519: | main | Production state. **Frozen.** Only receives merge commits from develop-vX.Y at release time.
Line 520: | develop | **Wild mainline.** ... Always the base for develop-vX.Y.
Line 521: | develop-vX.Y | **Scoped backlog.** ...
Line 530: - **ALL** new development (features, refactors, fixes) MUST target develop, develop-vX.Y, or a feature branch
Line 536: 1. Branch from develop (ad-hoc) or develop-vX.Y (scoped)
Line 546: 1. Create develop-vX.Y from develop when IDEAs are formally triaged for vX.Y
```

**Required Fix:** Rebuild `template/prompts/SP-002-clinerules-global.md` using `python scripts/rebuild_sp002.py` with `--template` flag or equivalent, then commit.

---

## 5. RECOMMENDATIONS

### Condition for APPROVE

Before v2.15 can be approved, the following must be completed:

1. **[P0-3-FOLLOW-UP]** Rebuild `template/prompts/SP-002-clinerules-global.md` to match `template/.clinerules` (update `develop-vX.Y` → `stabilization/vX.Y` throughout)
2. **[P0-3-FOLLOW-UP]** Commit the fix with message: `chore(template): sync SP-002 with ADR-006-AMEND-001 stabilization/vX.Y naming`
3. **[P0-3-FOLLOW-UP]** Re-verify sync between `template/.clinerules` and `template/prompts/SP-002-clinerules-global.md`

---

## 6. VERDICT

| Gate | Original Result | Re-validation Result |
|------|-----------------|----------------------|
| Coherence Audit | ❌ FAIL | ✅ PASS (P0-1, P0-2, P0-4 all fixed) |
| Feature Validation | ✅ PASS | ✅ PASS |
| Governance Check | ⚠️ PARTIAL | ⚠️ PARTIAL (P0-3 partial) |
| **Overall** | **❌ REJECT** | **⚠️ CONDITIONAL** |

### CONDITIONAL APPROVAL

v2.15 is **CONDITIONALLY APPROVED** pending resolution of the remaining P0-3 template/prompts sync issue.

**Once P0-3-FOLLOW-UP is completed:**
1. Re-verify template sync
2. Update this report with final APPROVE status
3. Proceed to release tag v2.15.0

**Next Steps:**
1. **[P0-3-FOLLOW-UP]** Fix `template/prompts/SP-002-clinerules-global.md`
2. **[QA]** Re-verify template sync after fix
3. **[QA]** Update this report to APPROVE status
4. **[RELEASE]** Tag v2.15.0 on `stabilization/v2.15` (or `develop` if no stabilization branch)
