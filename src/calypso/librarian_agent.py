"""
librarian_agent.py — Calypso Librarian Agent (PHASE-D)

Indexes cold archive files into the Chroma vector database and
provides semantic search over the Global Brain.

Prerequisites (PHASE-D.1 — manual):
    On Calypso:
        pip install chromadb
        chroma run --host 0.0.0.0 --port 8002 --path /data/chroma

    On Windows laptop:
        pip install chromadb

Usage:
    # Index all cold archive files
    python src/calypso/librarian_agent.py --index

    # Index specific new files (called by memory-archive.ps1)
    python src/calypso/librarian_agent.py --index --files memory-bank/archive-cold/sprint-logs/sprint-001.md

    # Query the Global Brain
    python src/calypso/librarian_agent.py --query "authentication decisions"

    # Check status
    python src/calypso/librarian_agent.py --status
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8002"))
COLLECTION_NAME = "global_brain"
CHUNK_SIZE = 500          # tokens (approximate: ~4 chars per token → ~2000 chars)
CHUNK_OVERLAP = 50        # token overlap between chunks
EMBED_MODEL = "nomic-embed-text"   # Ollama embedding model
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

COLD_ARCHIVE_DIR = os.environ.get("CALYPSO_MEMORY_DIR", "memory-bank") + "/archive-cold"

# File type classification
FILE_TYPE_MAP = {
    "sprint-logs": "sprint_log",
    "completed-tickets": "ticket",
    "productContext_Master.md": "product_context",
}


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_text(text: str, chunk_size_chars: int = 2000, overlap_chars: int = 200) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Input text to chunk
        chunk_size_chars: Target chunk size in characters
        overlap_chars: Overlap between consecutive chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size_chars
        # Try to break at a paragraph boundary
        if end < len(text):
            # Look for paragraph break within last 200 chars of chunk
            break_pos = text.rfind("\n\n", start, end)
            if break_pos > start + chunk_size_chars // 2:
                end = break_pos + 2
            else:
                # Fall back to sentence break
                break_pos = text.rfind(". ", start, end)
                if break_pos > start + chunk_size_chars // 2:
                    end = break_pos + 2

        chunks.append(text[start:end].strip())
        start = end - overlap_chars

    return [c for c in chunks if c.strip()]


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

def get_embedding(text: str) -> list[float]:
    """
    Generate embedding for text using Ollama nomic-embed-text model.

    Args:
        text: Text to embed

    Returns:
        Embedding vector as list of floats
    """
    try:
        import urllib.request
        import json as _json

        payload = _json.dumps({
            "model": EMBED_MODEL,
            "prompt": text,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/embeddings",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = _json.loads(response.read().decode("utf-8"))
            return result["embedding"]

    except Exception as e:
        raise RuntimeError(f"Failed to get embedding from Ollama: {e}") from e


# ---------------------------------------------------------------------------
# Chroma client
# ---------------------------------------------------------------------------

def get_chroma_client():
    """Get or create Chroma HTTP client."""
    try:
        import chromadb
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        # Test connection
        client.heartbeat()
        return client
    except ImportError:
        print("ERROR: chromadb not installed. Run: pip install chromadb", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to Chroma at {CHROMA_HOST}:{CHROMA_PORT}: {e}", file=sys.stderr)
        print("Ensure Chroma is running: chroma run --host 0.0.0.0 --port 8002 --path /data/chroma", file=sys.stderr)
        sys.exit(1)


def get_or_create_collection(client):
    """Get or create the global_brain collection."""
    try:
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Agentic Agile Workbench Global Brain — cold archive index"},
        )
        return collection
    except Exception as e:
        print(f"ERROR: Cannot get/create collection '{COLLECTION_NAME}': {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# File classification
# ---------------------------------------------------------------------------

def classify_file(file_path: Path) -> str:
    """Classify a cold archive file by type."""
    for dir_name, file_type in FILE_TYPE_MAP.items():
        if dir_name in str(file_path):
            return file_type
    return "document"


def extract_sprint_number(file_path: Path) -> str | None:
    """Extract sprint number from sprint log filename (e.g., sprint-001.md → '001')."""
    name = file_path.stem
    if name.startswith("sprint-"):
        return name[7:]
    return None


# ---------------------------------------------------------------------------
# Indexing
# ---------------------------------------------------------------------------

def index_file(collection, file_path: Path, verbose: bool = True) -> int:
    """
    Index a single file into Chroma.

    Args:
        collection: Chroma collection
        file_path: Path to file to index
        verbose: Print progress

    Returns:
        Number of chunks indexed
    """
    if not file_path.exists():
        print(f"  WARNING: File not found: {file_path}", file=sys.stderr)
        return 0

    if file_path.suffix not in (".md", ".txt", ".json"):
        if verbose:
            print(f"  SKIP: {file_path.name} (unsupported type)")
        return 0

    content = file_path.read_text(encoding="utf-8").strip()
    if not content or content == "":
        if verbose:
            print(f"  SKIP: {file_path.name} (empty)")
        return 0

    file_type = classify_file(file_path)
    sprint_num = extract_sprint_number(file_path)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    chunks = chunk_text(content)
    if verbose:
        print(f"  Indexing: {file_path.name} ({len(chunks)} chunks, type={file_type})")

    indexed = 0
    for i, chunk in enumerate(chunks):
        chunk_id = f"{file_path.stem}__chunk_{i:04d}"

        # Build metadata
        metadata = {
            "source_file": str(file_path),
            "file_name": file_path.name,
            "file_type": file_type,
            "date": date_str,
            "chunk_index": i,
            "total_chunks": len(chunks),
        }
        if sprint_num:
            metadata["sprint"] = sprint_num

        try:
            embedding = get_embedding(chunk)
            collection.upsert(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[metadata],
            )
            indexed += 1
        except Exception as e:
            print(f"  WARNING: Failed to index chunk {i} of {file_path.name}: {e}", file=sys.stderr)

    return indexed


def index_cold_archive(
    cold_archive_dir: str = COLD_ARCHIVE_DIR,
    specific_files: list[str] | None = None,
    verbose: bool = True,
) -> dict:
    """
    Index all files in the cold archive into the vector database.

    Args:
        cold_archive_dir: Path to memory-bank/archive-cold/
        specific_files: If provided, only index these files
        verbose: Print progress

    Returns:
        Dict with indexing statistics
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    archive_path = Path(cold_archive_dir)
    if not archive_path.exists():
        print(f"ERROR: Cold archive directory not found: {cold_archive_dir}", file=sys.stderr)
        sys.exit(1)

    if specific_files:
        files_to_index = [Path(f) for f in specific_files]
    else:
        files_to_index = [
            f for f in archive_path.rglob("*")
            if f.is_file() and f.name != ".gitkeep"
        ]

    if verbose:
        print(f"\nIndexing {len(files_to_index)} file(s) into Global Brain...")
        print(f"  Chroma: {CHROMA_HOST}:{CHROMA_PORT}")
        print(f"  Collection: {COLLECTION_NAME}")
        print(f"  Embedding model: {EMBED_MODEL} (via Ollama at {OLLAMA_HOST})")

    total_chunks = 0
    indexed_files = 0
    skipped_files = 0

    for file_path in sorted(files_to_index):
        chunks = index_file(collection, file_path, verbose=verbose)
        if chunks > 0:
            total_chunks += chunks
            indexed_files += 1
        else:
            skipped_files += 1

    stats = {
        "indexed_files": indexed_files,
        "skipped_files": skipped_files,
        "total_chunks": total_chunks,
        "collection": COLLECTION_NAME,
        "chroma_host": f"{CHROMA_HOST}:{CHROMA_PORT}",
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }

    if verbose:
        print(f"\n[DONE] Indexing complete!")
        print(f"  Files indexed: {indexed_files}")
        print(f"  Files skipped: {skipped_files}")
        print(f"  Total chunks: {total_chunks}")

    return stats


# ---------------------------------------------------------------------------
# Querying
# ---------------------------------------------------------------------------

def query_memory(semantic_query: str, top_k: int = 5) -> list[dict]:
    """
    Query the Global Brain vector database.

    Args:
        semantic_query: Natural language query
        top_k: Number of results to return

    Returns:
        List of relevant chunks with metadata and similarity scores
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    # Check if collection has any documents
    count = collection.count()
    if count == 0:
        return [{
            "type": "empty",
            "message": (
                "Global Brain is empty. Run the Librarian Agent to index the cold archive: "
                "python src/calypso/librarian_agent.py --index"
            ),
            "query": semantic_query,
        }]

    try:
        query_embedding = get_embedding(semantic_query)
    except RuntimeError as e:
        return [{
            "type": "error",
            "message": f"Failed to generate query embedding: {e}",
            "query": semantic_query,
        }]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )

    output = []
    if results and results["documents"]:
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )):
            output.append({
                "rank": i + 1,
                "score": round(1.0 - dist, 4),  # Convert distance to similarity
                "source": meta.get("source_file", "unknown"),
                "file_type": meta.get("file_type", "unknown"),
                "sprint": meta.get("sprint"),
                "date": meta.get("date"),
                "excerpt": doc[:500],
            })

    return output


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def get_status() -> dict:
    """Return the current status of the Global Brain."""
    try:
        client = get_chroma_client()
        collection = get_or_create_collection(client)
        count = collection.count()
        return {
            "status": "operational",
            "chroma_host": f"{CHROMA_HOST}:{CHROMA_PORT}",
            "collection": COLLECTION_NAME,
            "total_chunks": count,
            "embed_model": EMBED_MODEL,
            "ollama_host": OLLAMA_HOST,
        }
    except SystemExit:
        return {
            "status": "unavailable",
            "chroma_host": f"{CHROMA_HOST}:{CHROMA_PORT}",
            "message": "Cannot connect to Chroma. See PHASE-D.1 for setup instructions.",
        }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso Librarian Agent — index cold archive into Global Brain"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--index",
        action="store_true",
        help="Index cold archive files into Chroma",
    )
    group.add_argument(
        "--query",
        type=str,
        metavar="QUERY",
        help="Query the Global Brain with a semantic query",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Check Global Brain status",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Specific files to index (used with --index). If omitted, indexes all cold archive files.",
    )
    parser.add_argument(
        "--cold-archive-dir",
        default=COLD_ARCHIVE_DIR,
        help=f"Path to cold archive directory (default: {COLD_ARCHIVE_DIR})",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return for --query (default: 5)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output",
    )
    args = parser.parse_args()

    if args.status:
        status = get_status()
        print(json.dumps(status, indent=2))

    elif args.index:
        stats = index_cold_archive(
            cold_archive_dir=args.cold_archive_dir,
            specific_files=args.files,
            verbose=not args.quiet,
        )
        if args.quiet:
            print(json.dumps(stats))

    elif args.query:
        if not args.quiet:
            print(f"\nQuerying Global Brain: '{args.query}'")
            print(f"  Top-K: {args.top_k}")
            print()

        results = query_memory(args.query, args.top_k)

        if args.quiet:
            print(json.dumps(results))
        else:
            for result in results:
                if "rank" in result:
                    print(f"[{result['rank']}] Score: {result['score']:.4f} | {result['source']}")
                    print(f"    Type: {result['file_type']} | Date: {result.get('date', 'N/A')}")
                    print(f"    Excerpt: {result['excerpt'][:200]}...")
                    print()
                else:
                    print(f"[INFO] {result.get('message', result)}")


if __name__ == "__main__":
    main()
