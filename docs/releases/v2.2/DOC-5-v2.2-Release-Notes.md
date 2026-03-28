---
doc_id: DOC-5
release: v2.2
status: Frozen
title: Release Notes
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v2.1/DOC-5-v2.1-Release-Notes.md
---

# DOC-5 -- Release Notes (v2.2)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.2.0 |
| **Release date** | 2026-03-28 |
| **Git tag** | `v2.2.0` |
| **Branch** | `release/v2.2` (merged to `master`) |
| **Previous release** | v2.1.0 (2026-03-28) |
| **Type** | MINOR — memory-bank hygiene and governance compliance |

---

## What v2.2 Delivers

v2.2 is a **memory-bank hygiene release** — cleanup and governance compliance for the v2.1 release.

### Memory-Bank Corrections

**v2.1 backlog accuracy:** Corrected stale progress.md entries that misstated the status of orchestrator_phase3 MAX_TOKENS fix, SP-002 KI-001 false positive, and batch_artifacts/.gitignore. All were already fixed in prior commits.

**DOC6 revision closed:** Determined that `docs/conversations/2026-03-27-gemini-doc6-architecture.md` is a conversation log. Per RULE 8.3, conversation files must never be edited after creation. The DOC6 P0 issues were addressed to the source conversation, not a canonical spec — no action needed.

**activeContext hygiene:** Updated to reflect current state after v2.1 release.

### v2.1 Canonical Docs (Retroactive)

Created `docs/releases/v2.1/` folder with DOC-1..5 and EXECUTION-TRACKER, retroactively documenting the v2.1 hotfix release that bypassed formal governance process.

---

## Commits in v2.2

```
edd8b3c docs(memory): update activeContext -- v2.1 backlog fully resolved, no pending items
ba0f2a5 docs(memory): close DOC6 revision backlog item -- conversation log, RULE 8.3 prohibits editing
007d215 docs(memory): correct v2.1 backlog -- SP-002/KI-001 and batch_artifacts already fixed, orchestrator_phase3 MAX_TOKENS done on Calypso
ce3092e docs(memory): v2.1.0 release complete -- activeContext and progress updated for release v2.1
```

Plus merge commit `d9fc936` (Merge branch 'release/v2.2') and activeContext update `0dcc5ff`.

---

## v2.1 Canonical Docs (Retroactive)

Created during v2.2 cycle:

| File | Description |
|------|-------------|
| `docs/releases/v2.1/DOC-1-v2.1-PRD.md` | v2.1 scope: IDEA-008, SP-002 coherence, GitFlow |
| `docs/releases/v2.1/DOC-2-v2.1-Architecture.md` | Delta from v2.0 |
| `docs/releases/v2.1/DOC-3-v2.1-Implementation-Plan.md` | Step log with commit hashes |
| `docs/releases/v2.1/DOC-4-v2.1-Operations-Guide.md` | Delta from v2.0 |
| `docs/releases/v2.1/DOC-5-v2.1-Release-Notes.md` | Full v2.1 release notes |
| `docs/releases/v2.1/EXECUTION-TRACKER-v2.1.md` | v2.1 execution log |

All `docs/DOC-N-CURRENT.md` pointers updated to v2.1.

---

*End of Release Notes v2.2*
