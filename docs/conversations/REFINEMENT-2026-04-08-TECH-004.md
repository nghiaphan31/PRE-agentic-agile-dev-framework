# REFINE Session: TECH-004 Master Traceability Tree Feasibility

**Date:** 2026-04-08  
**Refined by:** Architect Mode  
**Input documents:** TECH-004, ADR-006  
**Output:** This refinement report + TECH-SUGGESTIONS-BACKLOG update

---

## 1. Concept Map: TECH-004 → ADR-006/RULE 10

### 1.1 Branch Type Mapping

| TECH-004 Branch | ADR-006 Equivalent | Mapping Status | Notes |
|-----------------|-------------------|----------------|-------|
| `lab/YYYY/Spike-name` | New (not in ADR-006) | **Addition** | For ad-hoc experimental work; merges to `develop` |
| `feature/YYYY/QN/T-xxx-name` | `feature/{IDEA-NNN}-{slug}` | **Compatible** | TECH-004 uses date-based naming; ADR-006 uses IDEA-NNN; hybrid possible |
| `bugfix/T-xxx-name` | Not explicitly named | **Addition** | Pre-release cold fixes; merges to `develop` (ADR-006 covers only `hotfix/`) |
| `release/vX.Y.Z` | Not in ADR-006 | **Addition** | ADR-006 uses `develop-vX.Y` for scoped work; TECH-004 adds release stabilization buffer |
| `hotfix/T-xxx-name` | `hotfix/vX.Y.Z` | **Compatible** | TECH-004 uses ticket-based naming; ADR-006 uses version-based; both merge to `main` + `develop` |

### 1.2 Workflow Mapping

| TECH-004 Workflow | ADR-006 Workflow | Gap Analysis |
|-------------------|-----------------|-------------|
| Lab → Develop (Strategy A: Direct Promotion) | ADR-006: commits directly to `develop` for ad-hoc work | TECH-004 formalizes `lab/` prefix for traceability |
| Lab → Feature → Develop (Strategy B: Refining) | Not in ADR-006 | **New workflow** — explicit "Z-pattern" traceability |
| Feature → Release → Main | `feature/` → `develop-vX.Y` → `main` | TECH-004 adds `release/` buffer; ADR-006 uses `develop-vX.Y` as release staging |
| Bugfix → Develop | Covered by `feature/` in ADR-006 | TECH-004 distinguishes `bugfix/` (cold) from `feature/` |
| Hotfix → Main + Develop | Covered by `hotfix/` in ADR-006 | Compatible |

---

## 2. Gap Analysis: What's Missing in ADR-006/RULE 10

### 2.1 Gaps Identified

| Gap | TECH-004 Proposal | ADR-006 Current State | Severity |
|-----|-------------------|----------------------|----------|
| **No explicit ad-hoc/experimental branch type** | `lab/` prefix | ADR-006 says `develop` is "wild mainline" but doesn't formalize experimental branches | Medium |
| **No "refining" workflow** | Lab → Feature merge pattern | ADR-006 has no concept of consuming a lab into a feature | High |
| **No release stabilization buffer branch** | `release/vX.Y.Z` | ADR-006 uses `develop-vX.Y` for both scoped development AND release staging | Medium |
| **No cold fix vs hot fix distinction** | `bugfix/` vs `hotfix/` | ADR-006 only defines `hotfix/` | Low |
| **No release parallelism** | Develop continues while release stabilizes | Not explicitly addressed in ADR-006 | Medium |

### 2.2 ADR-006 Strengths TECH-004 Doesn't Improve

- **Scoped backlog clarity:** `develop-vX.Y` explicitly tied to formal IDEA triage — this is superior to TECH-004's `release/vX.Y.Z` which doesn't indicate scope
- **Simplicity:** Fewer branch types = easier to understand and enforce
- **Version-based hotfix naming:** `hotfix/vX.Y.Z` immediately tells you which production version is being patched

---

## 3. Complexity Assessment: Minimal Extension vs. Rewrite

### 3.1 RULE 10 Change Complexity: **MINIMAL EXTENSION**

**Current RULE 10 defines:**
- `main` (frozen)
- `develop` (wild mainline)
- `develop-vX.Y` (scoped backlog)
- `feature/{IDEA-NNN}-{slug}`
- `hotfix/vX.Y.Z`

**TECH-004 proposes adding:**
- `lab/YYYY/Spike-name` — 1 new branch type
- `bugfix/T-xxx-name` — 1 new branch type (cold fix)
- `release/vX.Y.Z` — 1 new branch type (stabilization buffer)

**Estimated RULE 10 delta:** 3 new branch rows in the table + 1 new section on "Refining workflow"

### 3.2 Conflict Analysis

| TECH-004 Element | Conflict with ADR-006? | Resolution |
|-----------------|----------------------|------------|
| `release/vX.Y.Z` vs `develop-vX.Y` | **Partial** | Both can coexist: `develop-vX.Y` = scoped backlog, `release/vX.Y.Z` = stabilization buffer. ADR-006's `develop-vX.Y` already serves this purpose. |
| `lab/` vs `develop` | None | Additive — `lab/` is just `develop` with a prefix for traceability |
| `bugfix/` vs `feature/` | None | Additive — `bugfix/` is a semantic distinction for pre-release bug fixes |

### 3.3 Implementation Effort

| Component | Effort | Notes |
|-----------|--------|-------|
| RULE 10 extension | **Low** | Add 3 branch types, ~20 lines |
| `.clinerules` update | **Low** | Mirror RULE 10 changes in embedded prompt |
| Git pre-receive hook update | **Low** | Add 3 new patterns to validation regex |
| GitHub Actions update | **Low** | Add branch name checks to canonical-docs-check.yml |
| Template update | **Low** | Sync `.clinerules` in template/ |

**Total: Minimal extension, no rewrite required.**

---

## 4. Release Fit Assessment: v2.14 Scope Viability

### 4.1 Is TECH-004 Viable for v2.14?

**Decision: DEFER to v2.15**

**Rationale:**

| Factor | Assessment | v2.14 Fit |
|--------|------------|-----------|
| **Scope creep risk** | TECH-004 introduces 3 new branch types + new workflows | Medium-High |
| **RULE 10 stability** | v2.14 is likely a stabilization release | Low — changes to core GitFlow during stabilization are risky |
| **ADR-006 just implemented** | ADR-006 was created 2026-03-28, may still be in adoption phase | Changing it again so soon could cause confusion |
| **Parallel work** | Multiple IDEA/TECH refinements happening simultaneously | MEDIUM — need sync detection |
| **User need** | TECH-004 addresses traceability gaps, not critical blockers | Low — nice to have |

### 4.2 TECH-004 Fit by Component

| Component | v2.14 | v2.15 | Notes |
|-----------|-------|-------|-------|
| `lab/` branch type | ❌ | ✅ | Low risk, can wait |
| `bugfix/` branch type | ❌ | ✅ | Low risk, can wait |
| `release/vX.Y.Z` | ❌ | ✅ | Medium risk — introduces parallelism complexity |
| Refining workflow (lab→feature) | ❌ | ✅ | Medium risk — changes developer workflow |
| Hot vs Cold fix separation | ❌ | ✅ | Low risk, nice-to-have |

### 4.3 Recommendation

**DEFER TECH-004 to v2.15** with the following conditions:
1. Implement `lab/` and `bugfix/` as low-risk extensions in v2.15
2. Re-evaluate `release/vX.Y.Z` vs `develop-vX.Y` dual-buffer approach in v2.15
3. Do NOT implement release parallelism until RULE 10 is stable for 2+ releases

---

## 5. Refinement Decision

### 5.1 Decision: **DEFER**

**Rationale:**

1. **ADR-006 is too recent** (2026-03-28) — changing core GitFlow again within 2 weeks risks confusion
2. **v2.14 scope should be stabilization** — TECH-004 adds complexity without addressing critical blockers
3. **Partial acceptance possible:** The concepts are sound, but timing is wrong
4. **Minimal implementation debt:** TECH-004 doesn't require architectural changes, just RULE 10 extension

### 5.2 What Gets Accepted Now (Conceptual)

| Accepted Concept | Status | Implementation |
|-----------------|--------|----------------|
| `lab/` branch type for ad-hoc work | **ACCEPTED (concept)** | Implement in v2.15 |
| `bugfix/` branch type for cold fixes | **ACCEPTED (concept)** | Implement in v2.15 |
| Refining workflow (lab→feature) | **ACCEPTED (concept)** | Implement in v2.15 |
| `release/vX.Y.Z` buffer branch | **DEFERRED** | Re-evaluate in v2.15 |
| Release parallelism | **DEFERRED** | Re-evaluate in v2.16+ |
| Hot vs Cold fix separation | **ACCEPTED (concept)** | Implement in v2.15 |

### 5.3 Required for v2.15 Implementation

Before implementing TECH-004 in v2.15, the following must be true:
- [ ] ADR-006 has been stable for at least 1 release (no RULE 10 changes)
- [ ] v2.14 release completed successfully
- [ ] RULE 10 extension drafted and reviewed
- [ ] GitHub Actions updated to validate new branch patterns
- [ ] Template `.clinerules` updated

---

## 6. Answers to Key Questions

### Q1: Does `release/` branch add value over current `develop-vX.Y` approach?

**A:** Partially. `develop-vX.Y` already serves as a scoped backlog and release staging area. TECH-004's `release/vX.Y.Z` adds a **separate stabilization buffer** that allows:
- `develop` continues with next sprint work
- `release/vX.Y.Z` isolates release-finalization work

**However:** This creates **two** versioned branches (`develop-vX.Y` + `release/vX.Y.Z`) which increases complexity. The benefit may not outweigh the confusion. **Recommendation: DEFER, evaluate hybrid model in v2.15.**

### Q2: Is `bugfix/` (cold) vs `hotfix/` (emergency) separation useful?

**A:** Yes, semantically useful but operationally low impact.

| | Cold Fix (`bugfix/`) | Hot Fix (`hotfix/`) |
|--|---------------------|---------------------|
| **Trigger** | Pre-release QA found bug | Production emergency |
| **Merge path** | `bugfix/` → `develop` → `develop-vX.Y` → `release` | Branch from `main` tag → merge to `main` + `develop` |
| **Traceability** | Linear pipeline | Diamond pattern |

**Verdict:** Low-risk addition, good for traceability. Accept concept, implement in v2.15.

### Q3: Does `lab/` for ad-hoc work fit the workbench's experimental nature?

**A:** **Yes, strongly.** The workbench is explicitly experimental (SP-010: "Librarian Agent for AI-Centric Development"). `lab/` formalizes what is already happening — ad-hoc exploration on `develop`.

**The refining workflow (lab→feature) is the key innovation:**
```
lab/2026/Spike-AI-Engine (messy POC)
        ↓ merge into
feature/2026/Q2/T-102-GQL-Refined (industrialized)
        ↓ merge into
develop
```

This creates a **"Z-pattern"** that preserves the messy lab history while keeping `develop` clean.

**Verdict:** High-value addition. Accept concept, implement in v2.15.

### Q4: How does "refining" workflow change the development process?

**A:** Currently, developers either:
1. Work directly on `develop` (messy history)
2. Create a `feature/` branch (clean but loses informal work)

The refining workflow adds a **third option:**
3. Work on `lab/`, then "promote" to `feature/` by merging lab into feature

**Process change:**
```
Before: lab work → develop (messy)
After:  lab work → feature (merge lab) → develop (clean + traceable)
```

**Impact:**
- More commits on `develop` from feature merges (traceability gain)
- Lab history preserved (archival gain)
- Slightly longer feature cycle (workflow cost)

**Verdict:** Accept concept with caution. Requires developer training.

---

## 7. Next Steps

| Step | Owner | Target |
|------|-------|--------|
| Mark TECH-004 as [DEFERRED] in TECH-SUGGESTIONS-BACKLOG | Architect | Immediate |
| Log decision to decisionLog.md | Architect | Immediate |
| Add TECH-004 to v2.15 backlog consideration | Product Owner | Next triage |
| Schedule TECH-004 re-review at v2.15 planning | Scrum Master | v2.14 release + 1 |
| Draft RULE 10 extension (for reference) | Architect | v2.14 scope planning |

---

## 8. Sync Opportunities

### 8.1 Overlap with TECH-002/TECH-003

TECH-003 (Single Source of Truth for Release Tracking) was **ACCEPTED** and implemented. TECH-004 should be checked for overlap with any changes made by TECH-003.

**Overlap:** None identified — TECH-003 is about release tracking, TECH-004 is about branch lifecycle.

### 8.2 Dependency with IDEA-020 (Authoritative Orchestrator)

IDEA-020 established the Orchestrator as the default mode. TECH-004's `lab/` branch type aligns well with the Orchestrator's ideation intake process.

**Potential integration:** `lab/` branches could be created from Orchestrator intake, then promoted to `feature/` upon refinement decision.

---

## 9. Summary

| Dimension | Assessment |
|-----------|------------|
| **Conceptual soundness** | ✅ Strong — addresses real traceability gaps |
| **ADR-006 compatibility** | ✅ Additive, no conflicts |
| **RULE 10 change magnitude** | ✅ Minimal extension (3 new branch types) |
| **v2.14 fit** | ❌ Too soon after ADR-006 |
| **v2.15 fit** | ✅ Good — after stabilization |
| **Implementation risk** | 🟡 Medium — new workflows require training |
| **Developer impact** | 🟡 Medium — refining workflow adds steps |
| **Traceability gain** | ✅ High — Z-pattern preserves lab history |

**Final Decision: DEFER to v2.15**

---

## 10. Re-Refinement: Critical Elements Analysis (2026-04-08)

*Per user feedback, the following two elements were missing from the original refinement and are now analyzed explicitly.*

### 10.1 `--no-ff` Merge Strategy Analysis

#### Current State: NOT MANDATED

| Document | Mentions `--no-ff`? |
|----------|---------------------|
| ADR-006 | ❌ No — only describes branch types and merge paths, not merge strategy |
| RULE 10 (`.clinerules`) | ❌ No — same, only branch lifecycle |
| TECH-004 | ✅ **YES** — explicitly required for all Planned Dev, Ad-Hoc, and Cold Fix branches |

**TECH-004's `--no-ff` Requirement (from Naming Convention table):**
```
| Planned Dev     | feature/YYYY/QN/T-xxx-name | --no-ff Merge Loop |
| Ad-Hoc (Direct) | lab/YYYY/Spike-name        | Direct --no-ff Merge into Develop |
| Cold Fix        | bugfix/T-xxx-name          | --no-ff Merge into Develop |
```

#### Gap: ADR-006/RULE 10 Does NOT Mandate `--no-ff`

**What this means:**
- Currently, the workbench uses Git's **default merge behavior** (fast-forward when possible, else `--no-ff`)
- TECH-004 would **require** `--no-ff` for ALL merges to preserve merge topology
- This creates visible "loop" patterns in `git graph` visualizations

#### Change Magnitude Assessment: **MINIMAL**

| Aspect | Assessment |
|--------|------------|
| RULE 10 delta | Add 1 sentence: "All merges MUST use `--no-ff` to preserve traceability topology" |
| `.clinerules` delta | Mirror the above in embedded prompt |
| GitHub Actions | May need to validate merge commits exist (low effort) |
| Developer workflow | Moderate — every PR creates merge commit, not fast-forward |

**Why MINIMAL?**
- It's a single directive in RULE 10
- No new branch types required
- No workflow changes beyond "every merge creates a merge commit"

#### Should `--no-ff` Be Accepted Separately from TECH-004?

**Answer: YES — but with caveats**

| Criterion | Assessment |
|-----------|------------|
| Is it separable? | Technically YES — `--no-ff` is orthogonal to branch types |
| Is it valuable alone? | Partial — traceability improves, but without TECH-004's naming convention the visual trace is harder to read |
| Risk of accepting alone | Low — no breaking changes to existing branches |
| Coupling | HIGH — TECH-004's traceability claims depend on `--no-ff` |

**Recommendation:** Accept `--no-ff` as a standalone RULE 10 amendment in **v2.14** (stabilization). It's low-risk, improves traceability, and TECH-004's full value is realized when both are implemented together.

---

### 10.2 Naming Convention Analysis: `feature/YYYY/QN/T-xxx-name` vs `feature/{IDEA-NNN}-{slug}`

#### Conflict: YES — Partial

| Convention | Pattern | Example |
|------------|---------|---------|
| **TECH-004** | `feature/YYYY/QN/T-xxx-name` | `feature/2026/Q2/T-101-Auth` |
| **ADR-006** | `feature/{IDEA-NNN}-{slug}` | `feature/IDEA-101-authentication` |

#### Key Differences

| Dimension | TECH-004 | ADR-006 | Conflict? |
|-----------|----------|---------|----------|
| Date-based | ✅ Yes (YYYY/QN) | ❌ No | **YES** |
| Ticket reference | `T-xxx` (external?) | `{IDEA-NNN}` (internal) | **YES** |
| Human-readable | Partial | ✅ Yes (slug) | TECH-004 is less readable |
| Traceability | ✅ High (date + quarter) | Medium (IDEA number only) | TECH-004 wins |
| ADR-006 alignment | ❌ Breaks pattern | N/A | Breaking change |

#### TECH-004's Rationale for Date-Based Naming

From TECH-004 section "Traceability Naming Convention":
- `YYYY/QN` (Year/Quarter) provides **temporal traceability** — you can see when work started
- `T-xxx` provides **ticket traceability** — links to external issue tracker
- The combination allows: "When was this feature worked on?" + "What ticket does it track?"

#### ADR-006's Rationale for IDEA-NNN Naming

- `{IDEA-NNN}` is **process-traceable** — links to the internal refinement workflow
- The slug provides **human context** without date clutter
- Simpler, established pattern

#### Compatibility Analysis: **BREAKING CHANGE**

**If TECH-004 naming is adopted:**
- All existing `feature/IDEA-xxx-slug` branches would need renaming
- GitHub Actions branch name validation would need updating
- Developer muscle memory would need retraining
- **This is NOT a minimal extension — it's a replacement of an established pattern**

**Hybrid Approach (Not in TECH-004):**
```
feature/{IDEA-NNN}/{YYYY}Q{N}-{slug}
```
Example: `feature/IDEA-101/2026Q2-authentication`

This preserves:
- ADR-006's IDEA-NNN traceability
- TECH-004's temporal context
- Slug readability

**But this was NOT proposed in TECH-004 — it's a new idea that should be routed back**

---

### 10.3 Revised Assessment: Should DEFER Decision Stand?

#### Original DEFER Rationale (from Section 5.1):
1. ADR-006 is too recent (2026-03-28) — changing core GitFlow again within 2 weeks risks confusion
2. v2.14 scope should be stabilization — TECH-004 adds complexity without addressing critical blockers
3. Partial acceptance possible — concepts are sound, but timing is wrong
4. Minimal implementation debt — TECH-004 doesn't require architectural changes, just RULE 10 extension

#### Revised Assessment with New Elements:

| Element | Original Analysis | Revised Analysis | Impact on DEFER |
|---------|------------------|-----------------|----------------|
| `--no-ff` | Not analyzed | **MINIMAL change** — single directive | **ARGUES FOR ACCEPTING `--no-ff` in v2.14** |
| Naming Convention | Not analyzed | **BREAKING CHANGE** — conflicts with ADR-006 | **ARGUES FOR KEEPING DEFER** |
| Combined | Not analyzed | `--no-ff` alone separable; naming requires broader change | **SPLIT DECISION POSSIBLE** |

#### Revised Recommendation:

| Component | Original Decision | Revised Decision | Rationale |
|-----------|-------------------|------------------|-----------|
| **`--no-ff` merge strategy** | Not in scope | **ACCEPTED (standalone)** for v2.14 | Minimal RULE 10 change; traceability benefit; separable from naming convention |
| **Branch types (`lab/`, `bugfix/`, `release/`)** | DEFER to v2.15 | **DEFER to v2.15** | Unchanged — timing risk |
| **Naming convention** | Not analyzed | **DEFER to v2.15** with note | Breaking change needs more design; propose hybrid pattern |
| **Refining workflow** | DEFER to v2.15 | **DEFER to v2.15** | Unchanged |
| **Hot vs Cold fix separation** | Accept concept | **Accept concept** | Unchanged |

#### Revised DEFER Scope: **PARTIAL — `--no-ff` extracted**

The DEFER decision for TECH-004 **as a whole** still stands, but **`--no-ff` should be extracted and accepted as a standalone RULE 10 amendment in v2.14**.

**Implementation path:**
1. v2.14: Accept `--no-ff` only (1-sentence RULE 10 change)
2. v2.15: Implement TECH-004 branch types + refining workflow (ADR-006 stable)
3. v2.15+: Naming convention re-evaluation with hybrid proposal

---

### 10.4 New Technical Suggestion: Hybrid Naming Pattern

*Per RULE 15 (Technical Suggestions Backlog), the hybrid naming pattern discovered during re-refinement should be captured:*

**Proposal:** `feature/{IDEA-NNN}/{YYYY}Q{N}-{slug}`

**Example:** `feature/IDEA-101/2026Q2-authentication`

**Preserves:**
- ADR-006's IDEA-NNN traceability ✅
- TECH-004's temporal context (YYYY/QN) ✅
- Human-readable slug ✅

**Status:** [TECH-005] — Capture as new technical suggestion for v2.15 evaluation

---

### 10.5 Updated Decision Summary

| TECH-004 Component | v2.14 | v2.15 | Notes |
|--------------------|-------|-------|-------|
| `--no-ff` merge strategy | ✅ **ACCEPTED** | — | Extracted as standalone |
| `lab/` branch type | ❌ | ✅ | Deferred |
| `bugfix/` branch type | ❌ | ✅ | Deferred |
| `release/vX.Y.Z` branch | ❌ | ✅ | Deferred |
| Naming convention | ❌ | ✅ | Hybrid pattern proposed |
| Refining workflow | ❌ | ✅ | Deferred |
| Hot vs Cold fix separation | ❌ | ✅ | Accept concept now |

**Final: TECH-004 DEFERRED to v2.15, BUT `--no-ff` ACCEPTED for v2.14 as standalone RULE 10 amendment.**

---

*Re-refinement complete. Key finding: `--no-ff` is separable and low-risk; naming convention is a breaking change requiring more design. Decision logged.*
