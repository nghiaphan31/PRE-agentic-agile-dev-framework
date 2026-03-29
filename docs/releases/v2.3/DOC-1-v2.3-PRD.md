---
doc_id: DOC-1
release: v2.3
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-03-29
authors: [Developer mode, Human]
previous_release: docs/releases/v2.2/DOC-1-v2.2-PRD.md
---

# DOC-1 -- Product Requirements Document (v2.3)

> **Status: DRAFT** -- This document is under active development.

---

## Overview

v2.3 is a **minor release** capturing:
1. **IDEA-009** — Generic Anthropic Batch API Toolkit (developer tooling, ad-hoc)
2. **IDEA-011** — SP-002 Coherence Fix (bug fix, ad-hoc)

Both ideas emerged ad-hoc during the v2.3 coherence audit (IDEA-009) and ongoing operations (IDEA-011).

This release follows the [AD-HOC] lightweight process per [ADR-010](docs/ideas/ADR-010-dev-tooling-process-bypass.md).

---

## Scope of v2.3

| IDEA | Title | Type | Tier | Status |
|------|-------|------|------|--------|
| IDEA-009 | Generic Anthropic Batch API Toolkit | dev-tooling | Minor | [IMPLEMENTED] |
| IDEA-011 | SP-002 Coherence Fix | fix | Minor | [PENDING] |

---

## IDEA-009: Generic Anthropic Batch API Toolkit

### Problem Statement

During the v2.3 coherence audit, we submitted 3 batches to the Anthropic Batch API (BATCH1-GOVERNANCE, BATCH2-CROSSDOCS, BATCH3-TEMPLATE). The submission and retrieval process required multiple fixing cycles due to:
- API key friction (no validation before submission)
- No polling mechanism (manual status checks)
- JSON fence parsing issues (markdown fences around JSON responses)
- Inconsistent result types ("error" vs "errored")
- No structured batch_id persistence

These issues were solved ad-hoc during the audit. IDEA-009 extracts these lessons into a reusable toolkit.

### Solution

A generic, reusable Python package for submitting and retrieving batches from the Anthropic Batch API:

**Package:** `scripts/batch/`

| Module | Purpose |
|--------|---------|
| `config.py` | BatchConfig dataclass + YAML loader with validation |
| `submit.py` | Batch submission with ANTHROPIC_API_KEY validation |
| `retrieve.py` | Result retrieval with markdown fence stripping + raw fallback |
| `poll.py` | Polling utility with interval support and request_counts display |
| `cli.py` | CLI: submit / retrieve / status / poll commands |
| `generate.py` | Jinja2-based script generator from batch.yaml |

**CLI Usage:**
```bash
python -m scripts.batch.cli submit batch.yaml
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60
python -m scripts.batch.cli status batch.yaml
```

**Template Bundle:** `template/scripts/batch/` — self-contained copy for new project deployment.

### Requirements

- Python 3.11+
- `anthropic>=0.49.0`
- `jsonschema>=4.23.0`
- `jinja2>=3.1.0`
- `pyyaml>=6.0`

### Out of Scope

- Calypso pipeline integration (this is developer tooling, not a product feature)
- Batch processing for production workloads (this is a utility, not a service)

---

## IDEA-011: SP-002 Coherence Fix

### Problem Statement

SP-002 (.clinerules) consistently fails the pre-commit coherence check:
- **UTF-8 BOM** at start of file
- **Latin-1 mojibake** (em-dash → Ã©, arrow → â†’, etc.)
- **Literal `\n`** in RULE 10 instead of real newlines
- **Double embedding** of SP-002 in itself

Root cause: files saved as UTF-8 but read through a Latin-1/Windows-1252 pipeline.

### Solution (Pending Implementation)

1. Investigate source vs deployment corruption
2. Fix SP-002 and template/SP-002: remove BOM, correct mojibake, fix literal \n
3. Add BOM/mojibake detection to pre-commit hook
4. Consolidate SP-002 double-embedding

See [IDEA-011](docs/ideas/IDEA-011-fix-sp002-coherence.md) for full details.

---

## v2.2 Workflow Preserved

All v2.0, v2.1, and v2.2 features and workflows remain unchanged:

- Hot/Cold memory architecture
- Template folder enrichment
- Calypso orchestration scripts (Phase 2, 3, 4)
- Global Brain / Librarian Agent
- 4 Agile personas (.roomodes)
- Memory Bank (7 files in hot-context/)
- ADR-010 governance (two paths: structured vs ad-hoc)
- GitFlow branching model (ADR-006)

---

## Out of Scope for v2.3

- New Calypso phases
- Multi-developer collaboration features
- Brownfield workflow
- DOC6 revision (still pending)

---

## DOC-1 / DOC-2 Coherency (ADR-010)

Per ADR-010, this DOC-1 and the corresponding DOC-2 must be coherent:
- All requirements in DOC-1 have a corresponding architecture element in DOC-2
- All architecture elements in DOC-2 support a requirement in DOC-1
- No blind spots: anything not in DOC-1 is not required; anything not in DOC-2 is not architecture

---

*End of DOC-1 v2.3 (Draft)*
