---
sp_id: SP-010
title: Librarian Agent
version: 1.0.0
date_created: 2026-03-28
status: Active
used_by: src/calypso/librarian_agent.py
---

# SP-010 — Librarian Agent

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-03-28 | Initial creation — Global Brain indexing and semantic query for Calypso |

---

## Role Description

The Librarian Agent is a **non-interactive, automated agent** that:
1. Indexes cold archive files into the Chroma vector database after each sprint archival
2. Answers semantic queries from the `memory:query` MCP tool

Unlike other agents, the Librarian Agent does **not** use a conversational system prompt.
It is implemented as a Python script (`librarian_agent.py`) that calls Ollama for embeddings
and Chroma for vector storage/retrieval.

---

## Architecture

```
Sprint end
    |
    v
memory-archive.ps1
    |
    +-- Archives hot-context/ to archive-cold/
    |
    +-- Triggers: python src/calypso/librarian_agent.py --index --files <new_files>
                        |
                        v
                  Ollama nomic-embed-text
                  (generates embeddings)
                        |
                        v
                  Chroma vector DB (port 8002)
                  (stores chunks + metadata)

Roo Code query
    |
    v
memory:query MCP tool (fastmcp_server.py)
    |
    v
librarian_agent.query_memory(semantic_query, top_k)
    |
    +-- Ollama: embed query
    |
    +-- Chroma: similarity search
    |
    v
Top-K relevant chunks returned to Roo Code
```

---

## Configuration

| Parameter | Default | Environment Variable |
|-----------|---------|---------------------|
| Chroma host | `localhost` | `CHROMA_HOST` |
| Chroma port | `8002` | `CHROMA_PORT` |
| Ollama host | `http://localhost:11434` | `OLLAMA_HOST` |
| Embedding model | `nomic-embed-text` | — |
| Collection name | `global_brain` | — |
| Chunk size | ~2000 chars (~500 tokens) | — |
| Chunk overlap | ~200 chars (~50 tokens) | — |

---

## Setup (PHASE-D.1 — Manual)

### On Calypso (remote machine via SSH/Tailscale):

```bash
pip install chromadb
# Start Chroma as a persistent server
chroma run --host 0.0.0.0 --port 8002 --path /data/chroma
```

### On Windows laptop:

```bash
pip install chromadb
# Ensure nomic-embed-text model is available in Ollama
ollama pull nomic-embed-text
```

### Verify connectivity:

```bash
# Test Chroma connection
python src/calypso/librarian_agent.py --status

# Expected output:
# {
#   "status": "operational",
#   "chroma_host": "localhost:8002",
#   "collection": "global_brain",
#   "total_chunks": 0,
#   ...
# }
```

---

## Usage

### Index all cold archive files:

```bash
python src/calypso/librarian_agent.py --index
```

### Index specific new files (called by memory-archive.ps1):

```bash
python src/calypso/librarian_agent.py --index \
  --files memory-bank/archive-cold/sprint-logs/sprint-001.md \
          memory-bank/archive-cold/productContext_Master.md
```

### Query the Global Brain:

```bash
python src/calypso/librarian_agent.py --query "authentication decisions"
```

### Check status:

```bash
python src/calypso/librarian_agent.py --status
```

---

## File Type Classification

| Directory | Type Tag | Description |
|-----------|----------|-------------|
| `archive-cold/sprint-logs/` | `sprint_log` | Sprint end summaries |
| `archive-cold/completed-tickets/` | `ticket` | Closed ticket details |
| `archive-cold/productContext_Master.md` | `product_context` | Historical BDD accumulator |

---

## Output Format (memory:query)

```json
[
  {
    "rank": 1,
    "score": 0.9234,
    "source": "archive-cold/sprint-logs/sprint-001.md",
    "file_type": "sprint_log",
    "sprint": "001",
    "date": "2026-03-28",
    "excerpt": "First 500 chars of the most relevant chunk..."
  }
]
```

---

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Chroma not running | `fastmcp_server.py` falls back to keyword search |
| Ollama not running | `librarian_agent.py` raises `RuntimeError` with instructions |
| Empty cold archive | Returns `{"type": "empty", "message": "..."}` |
| No results found | Returns `{"type": "no_results", "message": "..."}` |

---

## Cold Zone Firewall Compliance

The Librarian Agent is the **only** agent authorized to read `archive-cold/` files directly
(RULE 9, exception clause). All other agents MUST use `memory:query` MCP tool.
