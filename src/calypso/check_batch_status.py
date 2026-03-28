"""
check_batch_status.py — Calypso Phase 2 Batch Status Checker

Polls the Anthropic Batch API for the Phase 2 batch job status.
When complete, retrieves and saves expert reports to the output directory.

Usage:
    python src/calypso/check_batch_status.py
    python src/calypso/check_batch_status.py --batch-id-file batch_artifacts/batch_id_phase2.txt
    python src/calypso/check_batch_status.py --poll   # polls every 60s until complete

Output:
    batch_artifacts/expert_reports/<expert_id>.json  — one file per expert
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import jsonschema

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_BATCH_ID_FILE = "batch_artifacts/batch_id_phase2.txt"
DEFAULT_OUTPUT_DIR = "batch_artifacts/expert_reports"
POLL_INTERVAL_SECONDS = 60
SCHEMA_PATH = Path(__file__).parent / "schemas" / "expert_report.json"


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def load_schema() -> dict:
    """Load the expert report JSON schema."""
    if not SCHEMA_PATH.exists():
        print(f"WARNING: Schema not found at {SCHEMA_PATH}. Skipping validation.", file=sys.stderr)
        return None
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def validate_report(report: dict, schema: dict, expert_id: str) -> bool:
    """Validate an expert report against the JSON schema."""
    if schema is None:
        return True
    try:
        jsonschema.validate(instance=report, schema=schema)
        return True
    except jsonschema.ValidationError as e:
        print(f"  WARNING: Schema validation failed for {expert_id}: {e.message}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def read_batch_id(batch_id_file: str) -> str:
    """Read batch ID from file."""
    path = Path(batch_id_file)
    if not path.exists():
        print(f"ERROR: Batch ID file not found: {batch_id_file}", file=sys.stderr)
        print("Run orchestrator_phase2.py first to submit the batch.", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8").strip()


def check_status(client: anthropic.Anthropic, batch_id: str) -> tuple[str, object]:
    """Check batch status. Returns (status_string, batch_object)."""
    batch = client.messages.batches.retrieve(batch_id)
    return batch.processing_status, batch


def retrieve_results(client: anthropic.Anthropic, batch_id: str, output_dir: str, schema: dict) -> list[str]:
    """Retrieve batch results and save expert reports. Returns list of saved file paths."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = []
    errors = []

    print(f"\nRetrieving results for batch {batch_id}...")

    for result in client.messages.batches.results(batch_id):
        expert_id = result.custom_id

        if result.result.type == "error":
            error_msg = f"  ERROR: {expert_id} failed: {result.result.error}"
            print(error_msg, file=sys.stderr)
            errors.append(error_msg)
            continue

        # Extract text content from the message
        message = result.result.message
        raw_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                raw_text += block.text

        # Parse JSON response
        try:
            # Strip markdown code fences if present
            text = raw_text.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

            report = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"  ERROR: {expert_id} returned invalid JSON: {e}", file=sys.stderr)
            # Save raw response for debugging
            raw_file = output_path / f"{expert_id}_raw.txt"
            raw_file.write_text(raw_text, encoding="utf-8")
            print(f"  Raw response saved to: {raw_file}", file=sys.stderr)
            errors.append(f"{expert_id}: invalid JSON")
            continue

        # Ensure required fields are present (fill defaults if missing)
        if "generated_at" not in report:
            report["generated_at"] = datetime.now(timezone.utc).isoformat()
        if "expert_id" not in report:
            report["expert_id"] = expert_id
        if "expert_role" not in report:
            report["expert_role"] = expert_id

        # Validate against schema
        validate_report(report, schema, expert_id)

        # Save report
        report_file = output_path / f"{expert_id}.json"
        report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        saved_files.append(str(report_file))
        print(f"  ✓ {expert_id} → {report_file}")

    if errors:
        print(f"\nWARNING: {len(errors)} expert(s) had errors. Check logs above.", file=sys.stderr)

    return saved_files


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso Phase 2: Check Anthropic Batch status and retrieve expert reports"
    )
    parser.add_argument(
        "--batch-id-file",
        default=DEFAULT_BATCH_ID_FILE,
        help=f"Path to batch ID file (default: {DEFAULT_BATCH_ID_FILE})",
    )
    parser.add_argument(
        "--batch-id",
        help="Batch ID directly (overrides --batch-id-file)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for expert reports (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        help=f"Poll every {POLL_INTERVAL_SECONDS}s until batch is complete",
    )
    args = parser.parse_args()

    # Validate API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # Get batch ID
    if args.batch_id:
        batch_id = args.batch_id
    else:
        batch_id = read_batch_id(args.batch_id_file)

    client = anthropic.Anthropic()
    schema = load_schema()

    print(f"\nChecking batch: {batch_id}")

    while True:
        status, batch = check_status(client, batch_id)
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

        print(f"[{now}] Status: {status}")

        if status == "ended":
            # Check request counts
            counts = batch.request_counts
            print(f"  Succeeded: {counts.succeeded}")
            print(f"  Errored:   {counts.errored}")
            print(f"  Expired:   {counts.expired}")
            print(f"  Canceled:  {counts.canceled}")

            saved = retrieve_results(client, batch_id, args.output_dir, schema)

            print(f"\n✓ Batch complete! {len(saved)} expert report(s) saved to: {args.output_dir}")
            print(f"\nNext step:")
            print(f"  python src/calypso/orchestrator_phase3.py --expert-reports-dir {args.output_dir}")
            break

        elif status in ("canceling", "canceled", "expired"):
            print(f"ERROR: Batch ended with status '{status}'. Cannot retrieve results.", file=sys.stderr)
            sys.exit(1)

        else:
            # Still processing
            if not args.poll:
                print(f"\nBatch still processing. Run again later, or use --poll to wait automatically.")
                print(f"  python src/calypso/check_batch_status.py --batch-id {batch_id} --poll")
                break
            else:
                print(f"  Waiting {POLL_INTERVAL_SECONDS}s before next check...")
                time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
