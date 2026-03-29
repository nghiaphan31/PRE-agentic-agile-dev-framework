---
doc_id: DOC-3
release: v2.3
status: Frozen
title: Implementation Plan
version: 1.0
date_created: 2026-03-29
date_frozen: 2026-03-29
authors: [Developer mode, Human]
previous_release: docs/releases/v2.2/DOC-3-v2.2-Implementation-Plan.md
---

# DOC-3 -- Implementation Plan (v2.3)

> **Status: FROZEN** -- This document is frozen for v2.3.0 release.

---

## Overview

v2.3 is a **minor release** implementing two ad-hoc ideas:
- **IDEA-009** — Generic Anthropic Batch API Toolkit
- **IDEA-011** — SP-002 Coherence Fix

This plan follows the [AD-HOC] lightweight process per [ADR-010](docs/ideas/ADR-010-dev-tooling-process-bypass.md).

---

## IDEA-009: Generic Anthropic Batch API Toolkit

### Implementation Status: COMPLETE ✅

All implementation was done on branch `feature/IDEA-009-batch-toolkit` from `develop`.

#### Phase 1: Package Implementation (scripts/batch/)

| Step | Module | Status |
|------|--------|--------|
| 1 | config.py — BatchConfig + YAML loader | ✅ |
| 2 | submit.py — batch submission | ✅ |
| 3 | retrieve.py — result retrieval | ✅ |
| 4 | poll.py — polling utility | ✅ |
| 5 | cli.py — CLI commands | ✅ |
| 6 | generate.py — Jinja2 script generator | ✅ |
| 7 | templates/ — Jinja2 templates | ✅ |

#### Phase 2: Template Bundle (template/scripts/batch/)

| Step | File | Status |
|------|------|--------|
| 1 | __init__.py | ✅ |
| 2 | config.py | ✅ |
| 3 | submit.py | ✅ |
| 4 | retrieve.py | ✅ |
| 5 | poll.py | ✅ |
| 6 | batch_submit_script.py.j2 | ✅ |
| 7 | batch_retrieve_script.py.j2 | ✅ |

#### Phase 3: Dependencies

| Package | Added to requirements.txt | Status |
|---------|---------------------------|--------|
| jinja2>=3.1.0 | ✅ | ✅ |
| pyyaml>=6.0 | ✅ | ✅ |

#### Phase 4: Syntax Validation

```bash
python -m py_compile scripts/batch/*.py
# All 12 Python files: PASS
```

#### Phase 5: CLI Testing

```bash
python -m scripts.batch.cli --help  # PASS
python -m scripts.batch.cli submit --help  # PASS
python -m scripts.batch.cli retrieve --help  # PASS
python -m scripts.batch.cli status --help  # PASS
python -m scripts.batch.generate --help  # PASS
```

---

## IDEA-011: SP-002 Coherence Fix

### Implementation Status: PENDING

**Branch to create:** `fix/IDEA-011-sp002-coherence` from `develop`

#### Investigation Phase

1. Read current SP-002 in binary mode to confirm encoding issues
2. Read template/SP-002 in binary mode
3. Identify all corruption patterns:
   - UTF-8 BOM (bytes EF BB BF at start)
   - Latin-1 mojibake (Ã©, â†', â€œ, â€")
   - Literal \n in RULE 10
   - Double embedding of SP-002

#### Fix Phase

1. Rewrite SP-002 with correct UTF-8 encoding (no BOM)
2. Fix mojibake characters (restore em-dash, arrows, quotes)
3. Fix RULE 10 literal \n → real newlines
4. Remove double embedding, keep single embedding
5. Apply same fixes to template/SP-002

#### Prevention Phase

1. Enhance `scripts/check-prompts-sync.ps1`:
   - Add BOM detection (byte scan for EF BB BF)
   - Add mojibake pattern detection
   - Add literal \n detection in rule content
2. Test enhanced pre-commit hook

#### Verification Phase

```bash
# Should PASS after fixes
./scripts/check-prompts-sync.ps1
git commit -m "fix(sp002): resolve encoding issues"
```

---

## Merge to develop

### IDEA-009 Merge

```bash
git checkout develop
git merge --squash feature/IDEA-009-batch-toolkit
git commit -m "feat(batch): generic Anthropic batch API toolkit (IDEA-009, v2.3.0)"
git branch -d feature/IDEA-009-batch-toolkit
```

### IDEA-011 Merge (after implementation)

```bash
git checkout develop
git merge --squash fix/IDEA-011-sp002-coherence
git commit -m "fix(sp002): resolve encoding issues (BOM, mojibake, literal \\n)"
git branch -d fix/IDEA-011-sp002-coherence
```

---

## Release Tag

After all v2.3 work is merged to `develop`:

```bash
git tag -a v2.3.0 -m "v2.3.0: Generic batch API toolkit + SP-002 coherence fix"
git push origin v2.3.0
```

---

*End of DOC-3 v2.3 (Draft)*
