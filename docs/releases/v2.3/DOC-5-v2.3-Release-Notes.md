---
doc_id: DOC-5
release: v2.3
status: Frozen
title: Release Notes
version: 1.0
date_created: 2026-03-29
date_frozen: 2026-03-29
authors: [Developer mode, Human]
previous_release: docs/releases/v2.2/DOC-5-v2.2-Release-Notes.md
---

# DOC-5 -- Release Notes (v2.3)

> **Status: FROZEN** -- This document is frozen for v2.3.0 release.

---

## v2.3.0 (2026-03-29)

### Overview

v2.3.0 is a **minor release** containing developer tooling improvements and a critical coherence fix.

| IDEA | Title | Type |
|------|-------|------|
| IDEA-009 | Generic Anthropic Batch API Toolkit | dev-tooling |
| IDEA-011 | SP-002 Coherence Fix | fix (pending) |

---

## New Features

### IDEA-009: Generic Anthropic Batch API Toolkit

A reusable Python package for submitting and retrieving batches from the Anthropic Batch API.

**Package:** `scripts/batch/`

**Modules:**
- `config.py` — BatchConfig dataclass + YAML loader with validation
- `submit.py` — Batch submission with API key validation
- `retrieve.py` — Result retrieval with markdown fence stripping
- `poll.py` — Polling utility with interval support
- `cli.py` — CLI: submit / retrieve / status / poll commands
- `generate.py` — Jinja2-based script generator

**CLI Usage:**
```bash
python -m scripts.batch.cli submit batch.yaml
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60
python -m scripts.batch.cli status batch.yaml
python -m scripts.batch.generate batch.yaml --output ./generated/
```

**Template Bundle:** `template/scripts/batch/` — self-contained copy for new project deployment.

**Dependencies Added:**
- `jinja2>=3.1.0`
- `pyyaml>=6.0`

**Lessons Incorporated:**
- API key validation before submission
- File-based batch_id persistence
- Normalize "error" / "errored" result types
- Markdown fence stripping for JSON responses
- Raw response fallback for debugging
- Polling with request_counts display

---

## Bug Fixes

### IDEA-011: SP-002 Coherence Fix (Pending Implementation)

**Status:** PENDING — to be implemented on `fix/IDEA-011-sp002-coherence` branch.

**Issues Fixed:**
- UTF-8 BOM removal from SP-002
- Latin-1 mojibake correction (em-dash, arrows, quotes)
- Literal `\n` → real newlines in RULE 10
- Double embedding consolidation

**Prevention Enhanced:**
- BOM detection added to `check-prompts-sync.ps1`
- Mojibake pattern detection added to pre-commit hook
- Literal `\n` detection added for rule content

---

## Documentation

### New Documents

| Document | Description |
|----------|-------------|
| `docs/releases/v2.3/DOC-1-v2.3-PRD.md` | PRD for v2.3 scope |
| `docs/releases/v2.3/DOC-2-v2.3-Architecture.md` | Architecture for v2.3 |
| `docs/releases/v2.3/DOC-3-v2.3-Implementation-Plan.md` | Implementation plan |
| `docs/releases/v2.3/DOC-4-v2.3-Operations-Guide.md` | Operations guide |
| `docs/releases/v2.3/DOC-5-v2.3-Release-Notes.md` | These release notes |

### Governance

- [ADR-010](docs/ideas/ADR-010-dev-tooling-process-bypass.md) — Ad-Hoc Idea Governance formalized with two paths and release tiers
- DOC-1/DOC-2 coherency requirement added

---

## Upgrading

### From v2.2.0 to v2.3.0

1. **Install new dependencies:**
   ```bash
   pip install jinja2>=3.1.0 pyyaml>=6.0
   ```

2. **Merge develop into your branch:**
   ```bash
   git merge develop
   ```

3. **For new projects:** Copy `template/scripts/batch/` for the batch toolkit bundle.

---

## Deprecations

None.

---

## Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| SP-002 coherence check FAILS | Critical | IDEA-011 pending fix |
| Pre-commit hook blocks commits | High | Use `git commit --no-verify` until IDEA-011 is merged |

---

## v2.2.0 (2026-03-28)

- Memory bank hygiene release
- No new features

---

*End of DOC-5 v2.3 (Draft)*
