---
id: IDEA-018
title: Make Rules Authoritative and Ensure Rule Coherence
status: [PARTIAL] — Contradiction resolved; systemic audit pending
target_release: [v2.7] — **CRITICAL**
source: Human (2026-04-01)
source_files: .clinerules, prompts/SP-002-clinerules-global.md, prompts/README.md
captured: 2026-04-01
captured_by: Developer mode
refined_by: Architect (2026-04-08)
refinement_session: REF-2026-04-08-002
---

## Description

**CRITICAL:** Two related issues:

1. **Rules Must Be More Authoritative:** The `.clinerules` (SP-002) must be made truly authoritative to ALL agents. IDEA-017 (cumulative docs violation) happened because agents didn't follow rules strictly enough. Rules need stronger enforcement mechanisms.

2. **Rule Coherence Audit Required:** We have multiple rule systems (`.clinerules`, SP-002, SP-003-006, prompts/README.md) that may contain contradictions:
   - ~~RULE 6.2 vs RULE 7.2 (PowerShell contradiction)~~ **RESOLVED - see below**
   - Other unknown contradictions may exist
   - Rules that cancel each other out defeat their purpose

## Motivation

The fundamental problem is that rules exist but are:
1. Not authoritative enough (can be ignored or bypassed)
2. Not fully coherent (contradictions cause confusion)
3. Not enforced (no mechanism to catch violations)

This is why IDEA-017 happened - the cumulative doc requirement existed in RULE 12 but wasn't enforced.

## Classification

Type: GOVERNANCE

## Severity

**P0 / CRITICAL** — Undermines the entire governance system

---

## Refinement Session 2026-04-08

### Issue 1: RULE 6.2 vs RULE 7.2 PowerShell Contradiction

#### Original Text

**RULE 6.2** (lines 270-272):
```
**File concatenation:** Never use PowerShell for file concatenation. The pattern `(Get-Content a) + (Get-Content b) | Set-Content out` silently produces a 1-line file with exit code 0 — no error is raised. Use Python instead (see `scripts/rebuild_sp002.py` for the canonical implementation).
```

**RULE 7.2** (lines 321-327):
```
4. Assemble the final file using PowerShell:

   ```powershell
   Get-Content _temp_chunk_01.md, _temp_chunk_02.md, _temp_chunk_03.md | Set-Content target-file.md -Encoding UTF8
   ```
```

#### Root Cause Analysis

The contradiction is **apparent, not actual**. The issue:

- **RULE 6.2** prohibits the **broken inline addition pattern**: `(Get-Content a) + (Get-Content b) | Set-Content out`
  - This produces a 1-line file because PowerShell evaluates `(Get-Content a) + (Get-Content b)` as **array addition**, then passes the resulting array to `Set-Content` which serializes it incorrectly

- **RULE 7.2** uses the **correct pipeline pattern**: `Get-Content a, b, c | Set-Content`
  - This correctly pipelines file content through to Set-Content

The problem is RULE 6.2's wording is too absolute ("never use PowerShell for file concatenation") when it should only prohibit the specific broken pattern.

#### Resolution

**Proposed fix to RULE 6.2** (clarify, not change intent):

```
**File concatenation:** Never use PowerShell **inline addition** for file concatenation. 
The pattern `(Get-Content a) + (Get-Content b) | Set-Content out` silently produces a 
1-line file with exit code 0 — no error is raised. 

**Correct PowerShell pattern:** `Get-Content a, b | Set-Content target.md -Encoding UTF8` 
This pipeline pattern is acceptable for multi-file assembly.

**Preferred:** Use Python for all file concatenation (see `scripts/rebuild_sp002.py` 
for the canonical implementation).
```

**Proposed clarification to RULE 7.2**:

```
4. Assemble the final file using PowerShell **pipeline pattern**:

   ```powershell
   Get-Content _temp_chunk_01.md, _temp_chunk_02.md, _temp_chunk_03.md | Set-Content target-file.md -Encoding UTF8
   ```

   **Note:** This is the ONLY acceptable PowerShell concatenation pattern. The inline
   addition pattern `(Get-Content a) + (Get-Content b)` is FORBIDDEN.
```

#### Roo Code Constraint

**Critical limitation identified:** Roo Code agents can only make **single atomic tool calls**. The chunking protocol in RULE 7.2 requires:
1. write_to_file for chunk 1
2. write_to_file for chunk 2
3. execute_command (PowerShell assembly)
4. execute_command (deletion)

This is NOT achievable in a single Roo Code turn. **Python scripts remain the canonical implementation for chunking.** The PowerShell chunking protocol applies to environments where agents can execute multi-step sequences.

### Issue 2: Systemic Rule Coherence Audit

**Status:** NOT YET DONE — requires systematic audit across all rules

**Known contradictions to audit:**
- [ ] RULE 6.2 vs 7.2 — **RESOLVED** above
- [ ] Need full audit to find OTHER contradictions

**Audit scope:**
- `.clinerules` (858 lines, 15 rules)
- `prompts/SP-002-clinerules-global.md`
- `prompts/SP-003-006` (persona prompts)
- `prompts/README.md`

---

## Required Actions

### DONE ✓
- [x] Resolve RULE 6.2 vs 7.2 contradiction

### TODO

#### Phase 1: Immediate Fixes
- [ ] Apply clarification to RULE 6.2 in `.clinerules`
- [ ] Apply clarification to RULE 7.2 in `.clinerules`
- [ ] Sync changes to `prompts/SP-002-clinerules-global.md`
- [ ] Run `python scripts/rebuild_sp002.py` to verify byte-for-byte match
- [ ] Commit with `chore(prompts): resolve RULE 6.2 vs 7.2 PowerShell contradiction`

#### Phase 2: Systemic Audit
- [ ] Systematic review of ALL rules across all documents
- [ ] Identify any additional contradictions
- [ ] Identify redundant rules
- [ ] Identify gaps (rules that should exist but don't)
- [ ] Document all rules in a single authoritative list

#### Phase 3: Authoritative Enforcement
- [ ] Add enforcement mechanism beyond Git pre-receive hook
- [ ] Add CI/CD checks that verify rule compliance
- [ ] Make violating rules a blocking issue (like P0)
- [ ] Add "RULE VIOLATION" as a critical category

#### Phase 4: Rule Classification
- [ ] Which rules apply to workbench-only?
- [ ] Which rules apply to application projects?
- [ ] Which rules are universal?

---

## Complexity Score

**Score: 8/10** — MAJOR effort, requires systematic audit

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | CRITICAL issue - captured immediately |
| 2026-04-08 | [PARTIAL] | RULE 6.2 vs 7.2 contradiction resolved; systemic audit pending |

---

## Disposition Decision

**Status: [PARTIAL]**

**Rationale:**
- ✓ RULE 6.2 vs 7.2 contradiction: RESOLVED
- ✓ Root cause identified and resolution proposed
- ✓ Roo Code constraint documented
- ✗ Systemic rule coherence audit: NOT YET DONE
- ✗ Clarification not yet applied to .clinerules
- ✗ SP-002 not yet synced

**Next Steps:**
1. Developer mode applies clarification to `.clinerules`
2. Developer mode syncs to `prompts/SP-002-clinerules-global.md`
3. Commit
4. Future refinement session for systemic audit
