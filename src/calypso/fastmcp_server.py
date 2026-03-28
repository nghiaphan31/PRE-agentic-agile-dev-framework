"""
fastmcp_server.py — Calypso FastMCP Server

Exposes Calypso orchestration tools to Roo Code via the MCP protocol.
Runs as a local server on port 8001 (configurable via CALYPSO_PORT env var).

Tools exposed:
  - launch_factory(prd_path)         Start Phase 2 pipeline for a PRD
  - check_batch_status(batch_id)     Check Anthropic Batch job status
  - retrieve_backlog(phase)          Get draft or final backlog
  - memory_query(query, top_k)       Query Global Brain vector DB (stub until PHASE-D)
  - memory_archive()                 Rotate hot-context to cold archive

Usage:
    python src/calypso/fastmcp_server.py
    python src/calypso/fastmcp_server.py --port 8001

Dependencies:
    pip install fastmcp
"""

import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from fastmcp import FastMCP
except ImportError:
    print("ERROR: fastmcp not installed. Run: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PORT = int(os.environ.get("CALYPSO_PORT", "8001"))
BATCH_ARTIFACTS_DIR = os.environ.get("CALYPSO_BATCH_DIR", "batch_artifacts")
MEMORY_BANK_DIR = os.environ.get("CALYPSO_MEMORY_DIR", "memory-bank")

# ---------------------------------------------------------------------------
# FastMCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="calypso",
    version="0.1.0",
    description=(
        "Calypso — Tier 2 Orchestration Layer for the Agentic Agile Workbench. "
        "Provides tools to run the asynchronous factory pipeline and query the Global Brain."
    ),
)


# ---------------------------------------------------------------------------
# Tool: launch_factory
# ---------------------------------------------------------------------------

@mcp.tool()
def launch_factory(prd_path: str) -> str:
    """
    Start the Phase 2 pipeline for the given PRD document.

    Dispatches the PRD to the Anthropic Batch API with 4 expert agents
    (architecture, security, UX, QA). Returns the batch ID.

    Args:
        prd_path: Path to the PRD document (e.g., docs/releases/v2.0/DOC-1-v2.0-PRD.md)

    Returns:
        JSON string with batch_id and status message.
    """
    if not Path(prd_path).exists():
        return json.dumps({"error": f"PRD not found: {prd_path}"})

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return json.dumps({"error": "ANTHROPIC_API_KEY not set"})

    try:
        # Import and call orchestrator_phase2 directly
        script_dir = Path(__file__).parent
        result = subprocess.run(
            [sys.executable, str(script_dir / "orchestrator_phase2.py"),
             "--prd", prd_path,
             "--output-dir", BATCH_ARTIFACTS_DIR],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,  # workspace root
        )

        if result.returncode != 0:
            return json.dumps({
                "error": "orchestrator_phase2.py failed",
                "stderr": result.stderr[-500:],
            })

        # Read the batch ID that was saved
        batch_id_file = Path(BATCH_ARTIFACTS_DIR) / "batch_id_phase2.txt"
        if batch_id_file.exists():
            batch_id = batch_id_file.read_text(encoding="utf-8").strip()
            return json.dumps({
                "status": "submitted",
                "batch_id": batch_id,
                "prd_path": prd_path,
                "message": (
                    f"Batch submitted successfully. "
                    f"Use check_batch_status('{batch_id}') to monitor progress."
                ),
            })
        else:
            return json.dumps({
                "status": "submitted",
                "message": result.stdout[-500:],
            })

    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Tool: check_batch_status
# ---------------------------------------------------------------------------

@mcp.tool()
def check_batch_status(batch_id: str) -> dict:
    """
    Check the status of an Anthropic Batch job.

    Args:
        batch_id: The Anthropic Batch job ID (e.g., msgbatch_01abc...)

    Returns:
        Dict with status, request_counts, and next_step instructions.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {"error": "ANTHROPIC_API_KEY not set"}

    try:
        client = anthropic.Anthropic()
        batch = client.messages.batches.retrieve(batch_id)

        result = {
            "batch_id": batch_id,
            "status": batch.processing_status,
            "request_counts": {
                "succeeded": batch.request_counts.succeeded,
                "errored": batch.request_counts.errored,
                "expired": batch.request_counts.expired,
                "canceled": batch.request_counts.canceled,
                "processing": batch.request_counts.processing,
            },
        }

        if batch.processing_status == "ended":
            result["next_step"] = (
                "Batch complete! Run check_batch_status.py to retrieve results, "
                "then orchestrator_phase3.py to synthesize the backlog."
            )
            result["retrieve_command"] = (
                f"python src/calypso/check_batch_status.py --batch-id {batch_id}"
            )
        else:
            result["message"] = f"Batch still processing. Check again later."

        return result

    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Tool: retrieve_backlog
# ---------------------------------------------------------------------------

@mcp.tool()
def retrieve_backlog(phase: str = "final") -> dict:
    """
    Retrieve the draft or final backlog from batch artifacts.

    Args:
        phase: "draft" for draft_backlog.json, "final" for final_backlog.json

    Returns:
        The backlog dict, or an error dict if not found.
    """
    if phase not in ("draft", "final"):
        return {"error": f"Invalid phase '{phase}'. Use 'draft' or 'final'."}

    filename = f"{phase}_backlog.json"
    backlog_path = Path(BATCH_ARTIFACTS_DIR) / filename

    if not backlog_path.exists():
        return {
            "error": f"{filename} not found at {backlog_path}",
            "hint": (
                "Run orchestrator_phase3.py to generate draft_backlog.json, "
                "then orchestrator_phase4.py to generate final_backlog.json."
            ),
        }

    try:
        with open(backlog_path, encoding="utf-8") as f:
            backlog = json.load(f)
        return backlog
    except json.JSONDecodeError as e:
        return {"error": f"Could not parse {filename}: {e}"}


# ---------------------------------------------------------------------------
# Tool: memory_query
# ---------------------------------------------------------------------------

@mcp.tool()
def memory_query(semantic_query: str, top_k: int = 5) -> list:
    """
    Query the Global Brain vector database for relevant context.

    Searches the cold archive (sprint logs, completed tickets, product context history)
    using semantic similarity via Chroma + Ollama embeddings.
    Falls back to keyword search if Chroma is unavailable.

    Args:
        semantic_query: Natural language query (e.g., "authentication decisions")
        top_k: Number of results to return (default: 5)

    Returns:
        List of relevant text chunks with metadata and similarity scores.
    """
    # Try Chroma-backed semantic search via librarian_agent
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from calypso.librarian_agent import query_memory as _query_memory
        return _query_memory(semantic_query, top_k)
    except SystemExit:
        # Chroma unavailable -- fall through to keyword fallback
        pass
    except Exception as e:
        print(f"WARNING: Chroma query failed: {e}. Falling back to keyword search.", file=sys.stderr)

    # Fallback: keyword search across cold archive files
    cold_archive_dir = Path(MEMORY_BANK_DIR) / "archive-cold"
    results = []

    if not cold_archive_dir.exists():
        return [{
            "type": "unavailable",
            "message": (
                "Global Brain not available. Chroma may not be running. "
                "See PHASE-D.1: chroma run --host 0.0.0.0 --port 8002 --path /data/chroma"
            ),
            "query": semantic_query,
        }]

    # Basic keyword search across cold archive files
    query_terms = semantic_query.lower().split()
    for md_file in cold_archive_dir.rglob("*.md"):
        if md_file.name == ".gitkeep":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            score = sum(content.lower().count(term) for term in query_terms)
            if score > 0:
                results.append({
                    "source": str(md_file.relative_to(Path(MEMORY_BANK_DIR))),
                    "score": score,
                    "excerpt": content[:500],
                    "type": "keyword_fallback",
                })
        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:top_k]

    if not results:
        results = [{
            "type": "no_results",
            "message": f"No results found for query: '{semantic_query}'",
            "hint": (
                "Cold archive may be empty. Run memory_archive() after completing a sprint, "
                "then librarian_agent.py --index to populate the Global Brain."
            ),
        }]

    return results


# ---------------------------------------------------------------------------
# Tool: memory_archive
# ---------------------------------------------------------------------------

@mcp.tool()
def memory_archive() -> str:
    """
    Rotate hot-context to cold archive (sprint end operation).

    Appends activeContext.md to archive-cold/sprint-logs/sprint-NNN.md,
    appends productContext.md to archive-cold/productContext_Master.md,
    and resets both files to blank stubs.

    Returns:
        JSON string with archive summary.
    """
    archive_script = Path(__file__).parent.parent.parent / "scripts" / "memory-archive.ps1"

    if not archive_script.exists():
        return json.dumps({
            "error": f"memory-archive.ps1 not found at {archive_script}",
            "hint": "Run manually: scripts/memory-archive.ps1",
        })

    try:
        result = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(archive_script)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        if result.returncode != 0:
            return json.dumps({
                "error": "memory-archive.ps1 failed",
                "stderr": result.stderr[-500:],
            })

        return json.dumps({
            "status": "success",
            "message": "Hot-context archived to cold archive. Memory bank reset.",
            "output": result.stdout[-500:],
        })

    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Server entry point
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Calypso FastMCP Server — exposes orchestration tools to Roo Code"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help=f"Port to listen on (default: {PORT}, or set CALYPSO_PORT env var)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="MCP transport: stdio (for Roo Code) or sse (for HTTP clients). Default: stdio",
    )
    args = parser.parse_args()

    print(f"Starting Calypso FastMCP Server v0.1.0")
    print(f"  Transport: {args.transport}")
    if args.transport == "sse":
        print(f"  Port: {args.port}")
    print(f"  Tools: launch_factory, check_batch_status, retrieve_backlog, memory_query, memory_archive")
    print(f"  Batch artifacts dir: {BATCH_ARTIFACTS_DIR}")
    print(f"  Memory bank dir: {MEMORY_BANK_DIR}")
    print()

    if args.transport == "sse":
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
