---
doc_id: DOC-2
release: v2.3
status: Draft
title: Architecture Document
version: 1.0
date_created: 2026-03-29
authors: [Developer mode, Human]
previous_release: docs/releases/v2.2/DOC-2-v2.2-Architecture.md
---

# DOC-2 -- Architecture Document (v2.3)

> **Status: DRAFT** -- This document is under active development.

---

## Delta from v2.2

v2.2 introduced no architectural changes. v2.3 adds:

1. **IDEA-009 Architecture** — Generic Anthropic Batch API Toolkit (`scripts/batch/`)
2. **Template Bundle** — Self-contained `template/scripts/batch/` for new project deployment

---

## 1. Architecture Overview (Unchanged from v2.0)

The three-tier architecture from [DOC-2 v2.0](docs/releases/v2.0/DOC-2-v2.0-Architecture.md) applies in full:

```
+----------------------------------------------------------+
|  TIER 1 -- Human Interface Layer                         |
|  VS Code + Roo Code (Windows 11 laptop)                  |
|  - 4 Agile personas (.roomodes)                          |
|  - Memory Bank (Hot/Cold architecture)                   |
|  - .clinerules (9 rules)                                 |
|  - MCP client (connects to Tier 2 FastMCP server)       |
+----------------------------------------------------------+
         |                          |
         | MCP tools                | Anthropic API
         v                          v
+---------------------------+  +----------------------------+
|  TIER 2 -- Calypso        |  |  TIER 3 -- Cloud APIs      |
|  Orchestration Layer      |  |                            |
|  (Python scripts, local)  |  |  - Anthropic Batch API     |
|  - fastmcp_server.py      |  |    (Committee of Experts)  |
|  - orchestrator_phase2.py |  |  - Gemini Chrome Proxy     |
|  - orchestrator_phase3.py |  |    (free, via proxy.py)    |
|  - orchestrator_phase4.py |  |  - Ollama on Calypso       |
|  - triage_dashboard.py    |  |    (local, sovereign)      |
|  - apply_triage.py       |  |                            |
|  - Global Brain (Chroma)  |  |                            |
+---------------------------+  +----------------------------+
```

---

## 2. IDEA-009 Architecture: Anthropic Batch API Toolkit

### 2.1 Package Structure

**Location:** `scripts/batch/` (canonical), `template/scripts/batch/` (deployment bundle)

```
scripts/batch/
├── __init__.py           # Public re-exports
├── config.py             # BatchConfig dataclass + YAML loader
├── submit.py             # Batch submission
├── retrieve.py           # Result retrieval + markdown report
├── poll.py               # Polling utility
├── cli.py                # CLI entry point
├── generate.py           # Jinja2 script generator
└── templates/
    ├── batch_submit_script.py.j2
    └── batch_retrieve_script.py.j2
```

### 2.2 Core Dataclass: BatchConfig

```python
@dataclass
class BatchConfig:
    name: str                      # Human-readable batch name
    model: str                     # Anthropic model (e.g., claude-sonnet-4-6)
    max_tokens: int                # Max tokens per response
    temperature: float              # Sampling temperature
    output_dir: pathlib.Path       # Where to save results
    requests: list[RequestSpec]    # List of individual requests
    batch_id_file: pathlib.Path | None = None  # Persistent batch_id
    workspace_root: pathlib.Path                  # For path resolution
```

**RequestSpec:**
```python
@dataclass
class RequestSpec:
    custom_id: str        # Unique identifier for this request
    method: str           # HTTP method (POST)
    url: str              # API endpoint
    headers: dict         # Request headers
    body: dict            # Request body
```

### 2.3 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| YAML-based configuration | Human-readable, version-controllable batch definitions |
| File-based batch_id persistence | Batch ID survives terminal restarts; no in-memory state |
| Markdown fence stripping | API wraps JSON in ```json fences; must strip before parsing |
| Normalize "error" / "errored" | API inconsistency: both appear depending on failure mode |
| Raw response fallback | When text differs after parsing, save raw for debugging |
| CLI-first design | Works standalone without Python import; composable with shell |
| Jinja2 script generation | batch.yaml → submit.py + retrieve.py for repeatable runs |
| Self-contained template bundle | template/scripts/batch/ works independently, no parent delegation |

### 2.4 CLI Commands

```bash
# Submit a batch
python -m scripts.batch.cli submit batch.yaml

# Retrieve results (with optional polling)
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60

# Check batch status
python -m scripts.batch.cli status batch.yaml

# Generate scripts from YAML
python -m scripts.batch.generate batch.yaml --output ./generated/
```

### 2.5 Data Flow

```
batch.yaml
    └─> config.py (BatchConfig)
            ├─> submit.py --> Anthropic Batch API --> batch_id
            │                                    |
            |                                    v
            |                              batch_id_file
            |                                    |
            |                                    v
            └─> poll.py (loop) --> retrieve.py --> output_dir/
                                                       ├─ {custom_id}_raw.txt
                                                       └─ results.md
```

### 2.6 Integration with Tier 3 (Anthropic Batch API)

The toolkit uses the Anthropic SDK for batch operations:

```python
client = anthropic.Anthropic()
client.messages.batches.create(...)  # submit
client.messages.batches.retrieve(batch_id)  # status
client.messages.batches.results_raw(batch_id)  # retrieve
```

No changes to Tier 1 or Tier 2. The toolkit is a standalone utility.

---

## 3. IDEA-011 Architecture: SP-002 Coherence Fix

### 3.1 Problem

SP-002 (.clinerules) has encoding issues:
- UTF-8 BOM at start of file
- Latin-1 mojibake (em-dash → Ã©, arrow → â†')
- Literal `\n` instead of real newlines in RULE 10
- Double embedding of SP-002 in itself

### 3.2 Proposed Fix

**Prevention:** Add BOM/mojibake detection to `check-prompts-sync.ps1`

**Detection criteria:**
- Byte order mark (BOM: EF BB BF) at file start → FAIL
- Mojibake patterns (Ã©, â†', â€œ, â€") → FAIL
- Literal `\n` inside string literals → FAIL (should be real newlines)

**Remediation:** Rewrite SP-002 and template/SP-002 with correct UTF-8 encoding.

### 3.3 No Architecture Changes

This is a bug fix with no architectural impact. The existing pre-commit hook architecture is unchanged; only the validation logic is enhanced.

---

## 4. ADR-010 Ad-Hoc Governance Architecture

### 4.1 Two Paths

| Aspect | [STRUCTURED] | [AD-HOC] |
|--------|-------------|-----------|
| Origin | Formal PRD | Reactive discovery |
| Process | Full DOC-1→DOC-2→DOC-3→Calypso→QA | Lightweight with release tier |
| Branch | `develop-vX.Y` | `develop` or `feature/IDEA-NNN-slug` |
| Calypso | Yes | Optional (Minor skip) |
| Release tier | N/A | Minor / Medium / Major |

### 4.2 Release Tier Criteria

| Tier | Trigger | Process |
|------|---------|---------|
| Minor | Bug fixes, dev-tooling, low-risk | Skip Calypso; lightweight docs; unit+integration tests |
| Medium | New features, moderate scope | Partial/full Calypso; full DOC-1/2/3; QA review |
| Major | Architectural, epic-level | Full process; stakeholder sign-off |

### 4.3 DOC-1 / DOC-2 Coherency

Per ADR-010 core principle:
- **DOC-1** must capture all applicable requirements — nothing undocumented
- **DOC-2** must describe the complete architecture — no implicit assumptions
- When DOC-1 changes, DOC-2 must be reviewed for coherency
- When DOC-2 changes, DOC-1 must be verified for completeness

---

## 5. Dependencies

### New in v2.3

| Package | Version | Purpose |
|---------|---------|---------|
| `jinja2` | >=3.1.0 | Template generation for batch scripts |
| `pyyaml` | >=6.0 | YAML configuration parsing |

**Existing dependencies (unchanged):**
- `anthropic>=0.49.0` — Anthropic SDK
- `jsonschema>=4.23.0` — JSON schema validation

---

## 6. Unchanged Architecture from v2.0

All v2.0 architectural decisions apply in full:

| ID | Decision | Preserved |
|----|----------|-----------|
| DA-001 | Hot/Cold memory split | ✅ |
| DA-002 | Anthropic Batch API for Phase 2 | ✅ |
| DA-003 | FastMCP server on Calypso | ✅ |
| DA-004 | Chroma for Global Brain | ✅ |
| DA-005 | GREEN/ORANGE classification | ✅ |
| DA-006 | Cold Zone Firewall | ✅ |

---

## 7. DOC-1 / DOC-2 Cross-Reference

| DOC-1 Requirement | DOC-2 Architecture Element |
|------------------|---------------------------|
| Generic Batch API Toolkit | scripts/batch/ package (Section 2) |
| YAML-based configuration | BatchConfig dataclass (Section 2.2) |
| CLI commands | cli.py module (Section 2.4) |
| Template bundle | template/scripts/batch/ (Section 2.1) |
| SP-002 coherence | check-prompts-sync.ps1 enhancement (Section 3.2) |
| Ad-hoc governance | ADR-010 process (Section 4) |

---

*End of DOC-2 v2.3 (Draft)*
