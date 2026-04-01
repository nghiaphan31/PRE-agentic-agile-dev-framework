---
id: IDEA-013
title: Improve Batch Toolkit Reusability
status: [IDEA]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: scripts/batch/, plans/batch-doc6-review/, plans/batch-full-audit/
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

During the v2.6 coherence audit, we had to fix the batch scripts multiple times (submit, retrieve). We have `scripts/batch/` as a supposedly generic toolkit, but it wasn't reusable enough for different audit scenarios. We need to improve the generic batch toolkit so it can be reused without constant fixes.

## Motivation

The batch API toolkit in `scripts/batch/` was meant to be generic and reusable. However, when running coherence audits (batch-doc6-review, batch-full-audit), we had to:
1. Create project-specific submit scripts (submit_batch1.py, submit_batch2.py, etc.)
2. Create project-specific retrieve scripts
3. Fix bugs that should have been caught by the generic toolkit

This defeats the purpose of having a generic toolkit. If we use batch API frequently (which we should to reduce costs), we need the toolkit to work correctly out of the box.

## Classification

Type: TECHNICAL

## Complexity Score

**Score: 5/10** — SYNCHRONOUS refinement recommended

## Affected Documents

- `scripts/batch/` — Generic batch toolkit (needs improvement)
- `plans/batch-doc6-review/` — Project-specific scripts
- `plans/batch-full-audit/` — Project-specific scripts
- DOC-3 (Implementation Plan) — May need update

## Next Steps

1. Analyze what went wrong: why were project-specific scripts needed?
2. Identify gaps in the generic toolkit
3. Propose improvements to make it truly reusable

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human remark |

---
