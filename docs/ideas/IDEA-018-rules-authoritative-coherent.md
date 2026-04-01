---
id: IDEA-018
title: Make Rules Authoritative and Ensure Rule Coherence
status: [IDEA]
target_release: [v2.7] — **CRITICAL**
source: Human (2026-04-01)
source_files: .clinerules, prompts/SP-002-clinerules-global.md, prompts/README.md
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

**CRITICAL:** Two related issues:

1. **Rules Must Be More Authoritative:** The `.clinerules` (SP-002) must be made truly authoritative to ALL agents. IDEA-017 (cumulative docs violation) happened because agents didn't follow rules strictly enough. Rules need stronger enforcement mechanisms.

2. **Rule Coherence Audit Required:** We have multiple rule systems (`.clinerules`, SP-002, SP-003-006, prompts/README.md) that may contain contradictions:
   - RULE 6.2 vs RULE 7.2 (PowerShell contradiction - already identified)
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

## Required Actions

### 1. Make Rules Authoritative
- Add enforcement mechanism (Git pre-receive hook exists but may not be sufficient)
- Add CI/CD checks that verify rule compliance
- Make violating rules a blocking issue (like P0)
- Add "RULE VIOLATION" as a critical category

### 2. Rule Coherence Audit
- Systematic review of ALL rules across all documents
- Identify contradictions (RULE 6.2 vs 7.2 is one example)
- Identify redundant rules
- Identify gaps (rules that should exist but don't)
- Document all rules in a single authoritative list

### 3. Rule Classification
- Which rules apply to workbench-only?
- Which rules apply to application projects?
- Which rules are universal?

## Complexity Score

**Score: 8/10** — MAJOR effort, requires systematic audit

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | CRITICAL issue - captured immediately |

---
