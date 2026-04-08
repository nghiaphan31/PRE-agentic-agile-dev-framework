# Refinement Session: TECH-002 Auto-Detect Merged Features

**Date:** 2026-04-08  
**Session ID:** s2026-04-08-architect-002  
**Mode:** Architect  
**Document:** docs/ideas/TECH-002-auto-detect-merged-features-for-release-scope.md

---

## 1. Context

### 1.1 Original State
- TECH-002 captured with status `[IDEA]`
- 3 implementation approaches proposed but not analyzed
- No feasibility assessment completed
- Dependencies not identified

### 1.2 Inconsistency Found
- TECH-SUGGESTIONS-BACKLOG.md showed `[REFINED]`
- TECH-002.md showed `[IDEA]`
- This inconsistency was resolved during refinement

---

## 2. Research Conducted

### 2.1 Existing Infrastructure
- **BranchTracker** (`src/calypso/branch_tracker.py`):
  - Already extracts `idea_id` from branch names
  - Has `BranchStatus.MERGED` detection
  - Has `_mark_merged_branches()` but no tag-based queries
  
- **Release State:**
  - Current release: v2.11
  - Previous release: v2.10
  - v2.11 DOC-3 and DOC-5 exist in `docs/releases/v2.11/`

### 2.2 Dependencies Identified
- **Direct:** BranchTracker enhancement, IDEAS-BACKLOG parsing, DOC-3 updates
- **NOT blockers:** IDEA-022 (documentation only), TECH-001 (unrelated)
- **Synergies:** IDEA-003, IDEA-020, IDEA-024

---

## 3. Requirements Refined

### R-001: Git Query Requirements
System MUST query commits since last release tag using:
```bash
git log v2.10.0..develop --oneline
```

### R-002: Branch Name Extraction
Must parse IDEA-NNN from:
- Branch names: `feature/IDEA-019-conversation-logging` → IDEA-019
- Merge messages: `"Merge branch 'feature/IDEA-019-conversation-logging'"` → IDEA-019
- Squash merges: `"IDEA-019: Implement..."` → IDEA-019

### R-003: Backlog Cross-Reference
Must verify:
- IDEA exists in IDEAS-BACKLOG.md
- Status is IMPLEMENTED/REVIEW (merged state)
- Flag unknown IDEA IDs for human review

### R-004: Release Scope Update
Must:
- Update develop-vX.Y documentation
- Add human-review step before finalizing

### R-005: Scope Placeholder Creation
Must:
- Detect new release tag (vX.Y.0)
- Create placeholder for next release (develop-v{X+1}.0)

---

## 4. Feasibility Analysis

### Option A: Git Hook + Script
| Aspect | Rating |
|--------|--------|
| Feasibility | HIGH |
| Complexity | 5/10 |
| Timing | Real-time |
| Pros | Simple, immediate detection |
| Cons | Local-only, no PR review |

### Option B: Scheduled CI/CD Scan
| Aspect | Rating |
|--------|--------|
| Feasibility | MEDIUM-HIGH |
| Complexity | 6/10 |
| Timing | Scheduled/on-demand |
| Pros | Centralized, PR-based review |
| Cons | Not real-time, GitHub-dependent |

### Option C: On-Demand Orchestrator
| Aspect | Rating |
|--------|--------|
| Feasibility | HIGH |
| Complexity | 5/10 |
| Timing | Human-initiated |
| Pros | Human-in-loop, integrates with planning |
| Cons | Requires human action |

---

## 5. Shared Components Identified

### scripts/detect-merged-features.py
Core detection logic shareable across all options:
- `get_merged_features_since_tag(tag, target_branch)`
- `extract_idea_id(text)`
- `MergedFeature` dataclass

### BranchTracker Enhancements Needed
- `get_merged_since_tag(tag)`
- `get_features_merged_since_release(release_tag)`
- CLI args for tag-based queries

---

## 6. Deliverables

| File | Action | Option |
|------|--------|--------|
| scripts/detect-merged-features.py | NEW | All |
| scripts/update-release-scope.py | NEW | All |
| src/calypso/branch_tracker.py | MODIFY | All |
| .githooks/pre-receive-detect | NEW | A |
| .github/workflows/detect-merged-features.yml | NEW | B |
| src/calypso/orchestrator_phase4.py | MODIFY | C |
| src/calypso/release_scope_manager.py | NEW | B, C |

---

## 7. Decision Deferred

**Implementation approach NOT decided.** Human will choose:
- **A (Git Hook):** Real-time, simple, local-only
- **B (CI/CD):** Centralized, scheduled, PR-based review  
- **C (Orchestrator):** Human-in-the-loop, on-demand

---

## 8. Status Updates Applied

- [x] TECH-002.md status changed to `[REFINED]`
- [x] TECH-SUGGESTIONS-BACKLOG.md shows `[REFINED]` (already correct)
- [x] Refinement details added to TECH-002 document
- [ ] Next: Human selects implementation approach

---

## 9. Key Insights

1. **TECH-002 does NOT depend on IDEA-022** - can be implemented independently
2. **BranchTracker already exists** - only needs enhancement, not new implementation
3. **All 3 options share core logic** - scripts/detect-merged-features.py can be shared
4. **Option C leverages existing infrastructure** - Orchestrator already exists (IDEA-020)
5. **Option B requires GitHub Actions knowledge** - slightly higher learning curve

---

*Refinement session completed. Awaiting human decision on implementation approach.*
