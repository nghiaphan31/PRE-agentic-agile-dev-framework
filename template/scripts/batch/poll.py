"""
poll.py — Polling utility for batch status

Polls an Anthropic batch until completion, then retrieves results.

Usage:
    from scripts.batch import BatchConfig, poll_until_complete
    config = BatchConfig.from_yaml("batch.yaml")
    results = poll_until_complete(config, interval_seconds=60)

This is the TEMPLATE VERSION. Canonical source: scripts/batch/poll.py
"""

from __future__ import annotations

import os
import sys
import time
from datetime import datetime, timezone
from typing import Callable

import anthropic

from scripts.batch.config import BatchConfig


POLL_INTERVAL_SECONDS = 60


def poll_until_complete(
    config: BatchConfig,
    api_key: str | None = None,
    interval_seconds: int = POLL_INTERVAL_SECONDS,
    on_status: Callable[[str], None] | None = None,
) -> list:
    """
    Poll batch status every `interval_seconds` until the batch is 'ended',
    then retrieve and return results.

    Args:
        config:          BatchConfig for the batch
        api_key:         Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.
        interval_seconds: Seconds between status checks (default: 60)
        on_status:       Optional callback called with status string on each poll

    Returns:
        List of RequestResult objects when the batch completes.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set.\n"
            "Set it with: $env:ANTHROPIC_API_KEY = 'sk-ant-...'\n"
            "Or pass api_key='sk-ant-...' directly."
        )

    batch_id = config.load_batch_id()
    if not batch_id:
        raise FileNotFoundError(
            f"Batch ID file not found: {config.batch_id_path}\n"
            "Run the submit script first to create the batch."
        )

    client = anthropic.Anthropic(api_key=key)

    print(f"[batch/poll] Polling batch: {batch_id}")
    print(f"[batch/poll] Interval: {interval_seconds}s  (Ctrl+C to abort)")

    # Import here to avoid circular dependency
    from scripts.batch.retrieve import retrieve_results

    while True:
        batch = client.messages.batches.retrieve(message_batch_id=batch_id)
        status = batch.processing_status
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        print(f"[batch/poll][{now}] Status: {status}")

        if on_status:
            on_status(status)

        if status == "ended":
            if batch.request_counts:
                print(
                    f"[batch/poll]   Succeeded: {batch.request_counts.succeeded}  "
                    f"Errored: {batch.request_counts.errored}  "
                    f"Expired: {batch.request_counts.expired}"
                )

            print(f"[batch/poll] Batch complete! Retrieving results...")
            results = retrieve_results(config, api_key=key)
            print(f"[batch/poll] Retrieved {len(results)} results.")
            return results

        elif status in ("canceling", "canceled", "expired"):
            print(f"[batch/poll] ERROR: Batch ended with terminal status '{status}'.", file=sys.stderr)
            return []

        else:
            print(f"[batch/poll] Still processing. Next check in {interval_seconds}s...")
            time.sleep(interval_seconds)
