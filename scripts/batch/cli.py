"""
cli.py — Command-line interface for the batch toolkit

Usage:
    # Submit a batch
    python -m scripts.batch.cli submit batch.yaml

    # Retrieve results (wait if not complete)
    python -m scripts.batch.cli retrieve batch.yaml

    # Poll until complete
    python -m scripts.batch.cli retrieve batch.yaml --poll

    # Quick status check
    python -m scripts.batch.cli status batch.yaml

    # Override batch ID
    python -m scripts.batch.cli retrieve batch.yaml --batch-id msgbatch_xxxxx
"""

from __future__ import annotations

import argparse
import os
import sys
import pathlib

import anthropic

from scripts.batch.config import BatchConfig
from scripts.batch.submit import submit_batch, submit_batch_from_yaml
from scripts.batch.retrieve import retrieve_and_save
from scripts.batch.poll import poll_until_complete


def _get_api_key() -> str | None:
    """Get API key from environment or return None."""
    return os.environ.get("ANTHROPIC_API_KEY")


def cmd_submit(args: argparse.Namespace) -> int:
    """Handle `cli.py submit`."""
    config = BatchConfig.from_yaml(args.config)

    errors = config.validate()
    if errors:
        print("[cli/submit] Config validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    try:
        batch = submit_batch(config, api_key=args.api_key)
        print(f"\n[cli/submit] Done. Batch ID: {batch.id}")
        print(f"[cli/submit] Run: python -m scripts.batch.cli retrieve {args.config}")
        return 0
    except Exception as e:
        print(f"[cli/submit] ERROR: {e}", file=sys.stderr)
        return 1


def cmd_retrieve(args: argparse.Namespace) -> int:
    """Handle `cli.py retrieve`."""
    config = BatchConfig.from_yaml(args.config)

    # Allow overriding batch ID
    if args.batch_id:
        config.save_batch_id(args.batch_id)
        print(f"[cli/retrieve] Using overridden batch ID: {args.batch_id}")

    try:
        if args.poll:
            print(f"[cli/retrieve] Polling until batch complete...")
            results = poll_until_complete(
                config,
                api_key=args.api_key,
                interval_seconds=args.interval,
            )
            if results:
                print(f"[cli/retrieve] Retrieved {len(results)} results.")
        else:
            results = retrieve_and_save(config, api_key=args.api_key)
            if not results:
                print(f"[cli/retrieve] No results yet (batch may still be processing).")
                print(f"[cli/retrieve] Use --poll to wait, or run retrieve again later.")
            else:
                print(f"[cli/retrieve] Retrieved {len(results)} results.")
        return 0
    except Exception as e:
        print(f"[cli/retrieve] ERROR: {e}", file=sys.stderr)
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """Handle `cli.py status`."""
    config = BatchConfig.from_yaml(args.config)

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(f"[cli/status] ANTHROPIC_API_KEY not set. Cannot check status.", file=sys.stderr)
        return 1

    batch_id = config.load_batch_id()
    if not batch_id:
        print(f"[cli/status] No batch ID found at: {config.batch_id_path}")
        print(f"[cli/status] Run `python -m scripts.batch.cli submit {args.config}` first.")
        return 1

    try:
        client = anthropic.Anthropic(api_key=api_key)
        batch = client.messages.batches.retrieve(message_batch_id=batch_id)

        print(f"[cli/status] Batch ID : {batch.id}")
        print(f"[cli/status] Status   : {batch.processing_status}")
        print(f"[cli/status] Created  : {batch.created_at}")
        print(f"[cli/status] Expires  : {batch.expires_at}")

        if batch.request_counts:
            print(
                f"[cli/status] Counts   : "
                f"{batch.request_counts.succeeded} succeeded, "
                f"{batch.request_counts.errored} errored, "
                f"{batch.request_counts.expired} expired"
            )

        return 0
    except Exception as e:
        print(f"[cli/status] ERROR: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generic Anthropic Batch API CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Submit a batch:
    python -m scripts.batch.cli submit plans/batch-full-audit/batch.yaml

  Retrieve results:
    python -m scripts.batch.cli retrieve plans/batch-full-audit/batch.yaml

  Poll until complete:
    python -m scripts.batch.cli retrieve plans/batch-full-audit/batch.yaml --poll

  Quick status check:
    python -m scripts.batch.cli status plans/batch-full-audit/batch.yaml

  Override batch ID:
    python -m scripts.batch.cli retrieve plans/batch-full-audit/batch.yaml --batch-id msgbatch_xxxxx
        """,
    )

    parser.add_argument(
        "--api-key",
        default=None,
        help="Anthropic API key. Defaults to $env:ANTHROPIC_API_KEY",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # submit
    p_submit = sub.add_parser("submit", help="Submit a batch from YAML config")
    p_submit.add_argument("config", help="Path to batch.yaml")
    p_submit.set_defaults(func=cmd_submit)

    # retrieve
    p_retrieve = sub.add_parser("retrieve", help="Retrieve batch results")
    p_retrieve.add_argument("config", help="Path to batch.yaml")
    p_retrieve.add_argument(
        "--poll",
        action="store_true",
        help="Poll until batch is complete (every --interval seconds)",
    )
    p_retrieve.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Polling interval in seconds (default: 60)",
    )
    p_retrieve.add_argument(
        "--batch-id",
        default=None,
        help="Override the batch ID (for re-checking old batches)",
    )
    p_retrieve.set_defaults(func=cmd_retrieve)

    # status
    p_status = sub.add_parser("status", help="Check batch status")
    p_status.add_argument("config", help="Path to batch.yaml")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
