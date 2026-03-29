"""
submit.py — Batch submission logic

Submits a batch job to the Anthropic Batch API from a BatchConfig.

Usage:
    from scripts.batch import BatchConfig, submit_batch
    config = BatchConfig.from_yaml("batch.yaml")
    batch = submit_batch(config)

    # Or with explicit API key:
    batch = submit_batch(config, api_key="sk-ant-...")

Key behaviors (lessons from coherence audit):
    - Validates ANTHROPIC_API_KEY before hitting the API
    - Saves batch_id to config.batch_id_path on success
    - Validates config before submission
"""

from __future__ import annotations

import os
import sys

import anthropic

from scripts.batch.config import BatchConfig


# ---------------------------------------------------------------------------
# Core submission
# ---------------------------------------------------------------------------


def submit_batch(config: BatchConfig, api_key: str | None = None) -> anthropic.Anthropic.Messages.Batch:
    """
    Submit a batch job from a BatchConfig.

    Args:
        config:   BatchConfig describing the batch to submit
        api_key:  Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.

    Returns:
        The Batch object returned by the Anthropic API.

    Raises:
        EnvironmentError:  If ANTHROPIC_API_KEY is not set and api_key not provided
        ValueError:        If config validation fails
        APIError:          If the Anthropic API returns an error
    """
    # ---- API key ----
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set.\n"
            "Set it with: $env:ANTHROPIC_API_KEY = 'sk-ant-...'\n"
            "Or pass api_key='sk-ant-...' directly."
        )

    # ---- Validate config ----
    errors = config.validate()
    if errors:
        raise ValueError(
            f"Batch config validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        )

    client = anthropic.Anthropic(api_key=key)

    # ---- Build request list ----
    print(f"[batch/submit] Building {len(config.requests)} requests for model {config.model}...")

    anthropic_requests = []
    for req in config.requests:
        anthropic_requests.append(
            anthropic.types.messages.batch_create_params.Request(
                custom_id=req.custom_id,
                params=anthropic.types.messages.batch_create_params.MessageCreateParamsNonStreaming(
                    model=config.model,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    system=req.system,
                    messages=[{"role": "user", "content": req.user_message}],
                ),
            )
        )

    # ---- Submit ----
    print(f"[batch/submit] Submitting batch '{config.name}'...")
    batch = client.messages.batches.create(requests=anthropic_requests)

    print(f"[batch/submit] Batch submitted successfully!")
    print(f"   Batch ID  : {batch.id}")
    print(f"   Status    : {batch.processing_status}")
    print(f"   Created at: {batch.created_at}")
    print(f"   Expires at: {batch.expires_at}")

    # ---- Persist batch ID ----
    config.save_batch_id(batch.id)
    print(f"[batch/submit] Batch ID saved to: {config.batch_id_path}")

    return batch


def submit_batch_from_yaml(yaml_path: str, api_key: str | None = None) -> anthropic.Anthropic.Messages.Batch:
    """
    Convenience: load a BatchConfig from YAML and submit in one call.

    Args:
        yaml_path: Path to the batch.yaml file
        api_key:   Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.

    Returns:
        The Batch object returned by the Anthropic API.
    """
    print(f"[batch/submit] Loading config from: {yaml_path}")
    config = BatchConfig.from_yaml(yaml_path)
    return submit_batch(config, api_key=api_key)
