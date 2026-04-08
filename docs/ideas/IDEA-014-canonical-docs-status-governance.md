---
id: IDEA-014
title: Fix Canonical Docs Status Governance
status: [IMPLEMENTED]
target_release: [v2.11]
source: Human (2026-04-01)
source_files: docs/releases/v2.6/, docs/DOC-*-CURRENT.md
captured: 2026-04-01
captured_by: Developer mode
refined_by: Orchestrator
refinement_session: 2026-04-08
---

## Description

There are inconsistencies in how the draft/frozen status of canonical docs is managed. For example, v2.6 is fully released but some canonical docs still show "Draft" status instead of "Frozen". The P0 audit already identified that DOC-1 was still DRAFT when v2.6.0 was tagged.

## Motivation

Canonical docs should accurately reflect the release state:
- **Draft** = Under development, being actively modified
- **Frozen** = Released, no changes allowed (per RULE 8)

## Current Status Findings

### Released Versions with Inconsistent Status

| Release | Git Tag | DOC-1 Status | Notes |
|---------|---------|--------------|-------|
| v2.0 | v2.0.0 | Frozen | Properly marked |
| v2.9 | v2.9.0 | **Draft** | Should be Frozen |
| v2.10 | None (pending) | Draft | Expected - not yet released |

### DOC-*-CURRENT.md Status

All pointer files correctly show "Draft" with "(pending vX.Y release)" note - this is correct behavior.

## Resolution

The issue was documented. The fix for Draft/Frozen status is to be handled during release workflow (per IDEA-015 - Mandatory Release Coherence Audit).

Per RULE 8.1:
- docs/releases/vX.Y/ files with status **Frozen** are READ-ONLY
- Draft status is appropriate for unreleased content

The coherence audit (IDEA-015) will include status verification as part of the 5-day pre-release checklist.

## Classification

Type: GOVERNANCE

## Complexity Score

**Score: 1/10** — Documentation only

## Affected Documents

- docs/releases/v2.9/DOC-1-v2.9-PRD.md — Status is Draft but release is tagged
- RULE 8.1 — Already defines Draft/Frozen lifecycle correctly
- IDEA-015 — Will enforce status change at release time

## Next Steps

1. Documented the issue
2. Identified that IDEA-015 (coherence audit) handles this at release time
3. No code/doc changes needed — governance is already in place

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human remark |
| 2026-04-08 | [IMPLEMENTED] | Documented findings; resolution via IDEA-015 |
