---
id: IDEA-017
title: Fix Canonical Docs Cumulative Self-Contained Requirement
status: [IDEA]
target_release: [v2.7] — **CRITICAL**
source: Human (2026-04-01)
source_files: docs/releases/v2.*/
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

**CRITICAL ISSUE:** Canonical docs (DOC-1 through DOC-5) are NOT self-contained and NOT properly cumulative. Per RULE 12 and the doc headers, each DOC-X-vX.Y.md MUST contain ALL content from previous versions PLUS the new content for that version. Content from vX.Y-1 that is not impacted by changes in vX.Y must remain strictly identical word-for-word.

**Current Problem:**
- Docs are delta-based or incomplete
- Content from previous versions is missing or restructured
- DOC-X-v2.Y is NOT a superset of DOC-X-v2.(Y-1)
- This breaks the "cumulative" requirement

## Motivation

The canonical docs MUST be:
1. **Self-contained** — Can be understood without reading previous versions
2. **Cumulative** — Contains all previous content plus new changes
3. **Word-for-word identical** for unchanged sections across versions

This is critical for:
- Onboarding new team members
- Auditing compliance at any point in time
- Understanding the full scope at any release

## Root Cause

The current release process creates new DOC-X-vX.Y files by copying DOC-X-v(X.Y-1) and applying changes, but:
1. Not all previous content is preserved
2. Sections are reorganized or removed
3. No verification that unchanged content is identical word-for-word

## Classification

Type: BUSINESS (governance/process)

## Severity

**P0 / CRITICAL** — This undermines the entire documentation system

## Required Actions

1. **Audit all DOC-X files** (v1.0 through v2.6) for missing content
2. **Verify cumulative requirement** — each version should contain all previous content
3. **Retroactive fix if needed** — may require rebuilding canonical docs
4. **Add automated verification** — Git pre-receive hook or CI check

## Complexity Score

**Score: 9/10** — MAJOR effort, potentially retroactive rebuild required

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | CRITICAL issue - captured immediately |

---
