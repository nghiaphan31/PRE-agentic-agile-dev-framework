---
doc_id: DOC-4
release: v2.3
status: Draft
title: Operations Guide
version: 1.0
date_created: 2026-03-29
authors: [Developer mode, Human]
previous_release: docs/releases/v2.2/DOC-4-v2.2-Operations-Guide.md
---

# DOC-4 -- Operations Guide (v2.3)

> **Status: DRAFT** -- This document is under active development.

---

## Overview

v2.3 Operations Guide covers:
- **IDEA-009** — Generic Anthropic Batch API Toolkit usage
- **IDEA-011** — SP-002 Coherence Fix (pre-commit hook enhancement)

---

## 1. Anthropic Batch API Toolkit Operations

### 1.1 Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m scripts.batch.cli --help
```

### 1.2 Creating a batch.yaml

```yaml
name: my-batch
model: claude-sonnet-4-6
max_tokens: 8192
temperature: 0.7
output_dir: ./batch_results
batch_id_file: .batch_id

requests:
  - custom_id: request-001
    method: POST
    url: https://api.anthropic.com/v1/messages
    headers:
      x-api-key: ${ANTHROPIC_API_KEY}
      anthropic-version: 2023-06-01
      content-type: application/json
    body:
      model: claude-sonnet-4-6
      max_tokens: 8192
      temperature: 0.7
      messages:
        - role: user
          content: "Your prompt here"
```

### 1.3 Submitting a Batch

```bash
# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Submit
python -m scripts.batch.cli submit batch.yaml

# Output: Batch submitted. batch_id: abc123 saved to .batch_id
```

### 1.4 Polling for Completion

```bash
# Poll every 60 seconds
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60

# Or check status without polling
python -m scripts.batch.cli status batch.yaml
```

### 1.5 Retrieving Results

```bash
# Retrieve results
python -m scripts.batch.cli retrieve batch.yaml

# Results saved to:
#   ./batch_results/results.md      (summary)
#   ./batch_results/{custom_id}_raw.txt  (raw responses)
```

### 1.6 Generating Scripts

```bash
# Generate standalone scripts
python -m scripts.batch.generate batch.yaml --output ./generated/

# Run generated scripts
python generated/submit_batch.py
python generated/retrieve_batch.py
```

### 1.7 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ANTHROPIC_API_KEY` not set | Export key or pass `--api-key` flag |
| Batch not found | Check `batch_id_file` exists and contains valid ID |
| JSON parse error | Check response has ```json fences; retrieve.py handles this |
| Rate limit | Wait and retry; reduce polling frequency |

---

## 2. SP-002 Pre-Commit Hook Operations

### 2.1 Enhanced Validation (IDEA-011 pending)

The pre-commit hook (`scripts/check-prompts-sync.ps1`) will validate:

- **BOM detection** — UTF-8 BOM (EF BB BF) at file start → FAIL
- **Mojibake detection** — Ã©, â†', â€œ, â€" patterns → FAIL
- **Literal \n detection** — \n inside string content → FAIL

### 2.2 Manual Check

```powershell
# Run coherence check manually
./scripts/check-prompts-sync.ps1

# Expected output after IDEA-011 fix:
# [SP-002] .clinerules (entire file)... PASS
```

### 2.3 If SP-002 Fails

1. Do not bypass the pre-commit hook
2. Investigate encoding: open in binary mode, check for BOM
3. Fix encoding issues in canonical SP-002
4. Re-run check-prompts-sync.ps1
5. Commit only when all SPs pass

---

## 3. Unchanged Operations

All v2.0, v2.1, v2.2 operational procedures remain unchanged:

- Calypso pipeline operations (Phase 2, 3, 4)
- Global Brain / Librarian Agent
- Memory Bank hot/cold management
- GitFlow branching operations
- pre-commit hook (except SP-002 enhancement)

---

## 4. Rollback Procedures

### 4.1 Rollback IDEA-009

```bash
# If issues found after merge:
git revert <merge-commit>
git push origin develop
# Re-tag v2.3.0 after fix
```

### 4.2 Rollback IDEA-011

```bash
# Revert SP-002 to previous version
git checkout HEAD~1 -- prompts/SP-002-clinerules-global.md
git checkout HEAD~1 -- template/prompts/SP-002-clinerules-global.md
git commit -m "revert: IDEA-011 SP-002 changes"
```

---

*End of DOC-4 v2.3 (Draft)*
