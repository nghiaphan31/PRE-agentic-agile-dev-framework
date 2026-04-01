---
id: IDEA-014
title: Fix Canonical Docs Status Governance
status: [IDEA]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: docs/releases/v2.6/, docs/DOC-*-CURRENT.md
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

There are inconsistencies in how the draft/frozen status of canonical docs is managed. For example, v2.6 is fully released but some canonical docs still show "Draft" status instead of "Frozen". The P0 audit already identified that DOC-1 was still DRAFT when v2.6.0 was tagged.

## Motivation

Canonical docs should accurately reflect the release state:
- **Draft** = Under development, being actively modified
- **Frozen** = Released, no changes allowed (per RULE 8)

The current issue is that:
1. Some v2.6 docs may still show "Draft" status
2. The DOC-*-CURRENT.md pointer files may not point to the correct frozen version
3. There's no automated check to ensure all docs for a released version are Frozen

## Classification

Type: GOVERNANCE

## Complexity Score

**Score: 3/10** — SYNCHRONOUS refinement recommended

## Affected Documents

- `docs/releases/v2.6/DOC-1-v2.6-PRD.md` — Status needs verification
- `docs/DOC-*-CURRENT.md` — Pointer files need verification
- RULE 8 (Documentation Discipline) — May need enhancement

## Next Steps

1. Audit all v2.6 canonical docs for correct status
2. Verify DOC-*-CURRENT.md pointers are correct
3. Propose RULE enhancement to prevent this in future

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human remark |

---
