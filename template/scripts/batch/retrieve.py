"""
retrieve.py — Batch result retrieval and parsing

Retrieves results from a completed Anthropic Batch job and parses them
into structured RequestResult objects.

Key behaviors (lessons from coherence audit):
    - Handles both "error" and "errored" result types (API inconsistency)
    - Strips markdown code fences from JSON responses
    - Falls back to raw text when JSON parsing fails
    - Saves raw response to _raw.txt for debugging
    - Generates a Markdown report

This is the TEMPLATE VERSION. Canonical source: scripts/batch/retrieve.py
"""

from __future__ import annotations

import json
import os
import sys
import pathlib
from dataclasses import dataclass
from typing import Literal

import anthropic

from scripts.batch.config import BatchConfig


@dataclass
class RequestResult:
    """
    Structured result for a single request in a batch.
    """

    custom_id: str
    status: Literal["succeeded", "errored", "unexpected"]
    text: str | None = None
    error: str | None = None
    error_type: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    raw_response: str = ""


def retrieve_results(config: BatchConfig, api_key: str | None = None) -> list[RequestResult]:
    """
    Retrieve results for a batch from the Anthropic API.

    Args:
        config:   BatchConfig for the batch
        api_key:  Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.

    Returns:
        List of RequestResult objects, one per request in the batch.
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

    batch = client.messages.batches.retrieve(message_batch_id=batch_id)
    print(f"[batch/retrieve] Batch '{batch.id}' status: {batch.processing_status}")

    if batch.processing_status != "ended":
        print(f"[batch/retrieve] Batch is not yet complete. Status: {batch.processing_status}")
        print(f"[batch/retrieve] Run retrieve again later, or use poll_until_complete().")
        return []

    if batch.request_counts:
        print(
            f"[batch/retrieve]   Succeeded: {batch.request_counts.succeeded}  "
            f"Errored: {batch.request_counts.errored}  "
            f"Expired: {batch.request_counts.expired}"
        )

    print(f"[batch/retrieve] Retrieving results...")
    results: list[RequestResult] = []

    for result in client.messages.batches.results(message_batch_id=batch_id):
        results.append(_parse_result(result))

    print(f"[batch/retrieve] Retrieved {len(results)} results.")
    return results


def _parse_result(result: anthropic.Anthropic.Messages.BatchResult) -> RequestResult:
    """
    Parse a single BatchResult from the API into a RequestResult.

    Handles:
        - result.type == "succeeded" / "success" → extract text from content
        - result.type == "errored" / "error" → extract error (API inconsistency)
        - result.type == "expired" / "canceled" → unexpected
        - JSON wrapped in markdown fences → strip fences
    """
    custom_id = result.custom_id
    raw_type = result.result.type

    if raw_type in ("succeeded", "success"):
        message = result.result.message
        input_tokens = message.usage.input_tokens if message.usage else 0
        output_tokens = message.usage.output_tokens if message.usage else 0

        raw_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                raw_text += block.text

        text = _strip_markdown_fences(raw_text)

        return RequestResult(
            custom_id=custom_id,
            status="succeeded",
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            raw_response=raw_text,
        )

    elif raw_type in ("errored", "error"):
        err = result.result.error
        error_type = getattr(err, "type", str(raw_type))
        error_msg = getattr(err, "error", str(err))

        return RequestResult(
            custom_id=custom_id,
            status="errored",
            error=str(error_msg),
            error_type=error_type,
        )

    else:
        return RequestResult(
            custom_id=custom_id,
            status="unexpected",
            error=f"Unexpected result type: {raw_type}",
        )


def _strip_markdown_fences(text: str) -> str:
    """
    Strip markdown code fences from text.

    Anthropic sometimes wraps JSON responses in ```json ... ```.
    """
    stripped = text.strip()
    for fence in ("```json", "```json\n", "```"):
        if stripped.startswith(fence):
            stripped = stripped[len(fence):]
            if stripped.rstrip().endswith("```"):
                stripped = stripped[:stripped.rstrip().rfind("```")]
            break
    return stripped.strip()


def save_results_markdown(
    results: list[RequestResult],
    output_path: str | os.PathLike,
    title: str = "Batch Results",
    batch_id: str | None = None,
) -> None:
    """
    Save a list of RequestResult objects as a formatted Markdown report.
    """
    path = pathlib.Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# {title}", ""]
    if batch_id:
        lines.append(f"**Batch ID:** `{batch_id}`")
    lines.extend(["", "---", ""])

    succeeded = [r for r in results if r.status == "succeeded"]
    errored = [r for r in results if r.status == "errored"]
    unexpected = [r for r in results if r.status == "unexpected"]

    if succeeded:
        lines.append(f"## Succeeded ({len(succeeded)})")
        lines.append("")
        for r in succeeded:
            lines.append(f"### {r.custom_id}")
            lines.append("")
            lines.append(f"**Tokens:** {r.input_tokens:,} in / {r.output_tokens:,} out")
            lines.append("")
            lines.append(r.text or "_No content_")
            lines.append("")
            lines.append("---")
            lines.append("")

    if errored:
        lines.append(f"## Errored ({len(errored)})")
        lines.append("")
        for r in errored:
            lines.append(f"### {r.custom_id}")
            lines.append("")
            lines.append(f"**Error type:** `{r.error_type or 'unknown'}`")
            lines.append(f"```\n{r.error}\n```")
            lines.append("")
            lines.append("---")
            lines.append("")

    if unexpected:
        lines.append(f"## Unexpected ({len(unexpected)})")
        lines.append("")
        for r in unexpected:
            lines.append(f"### {r.custom_id}")
            lines.append(f"```\n{r.error}\n```")
            lines.append("")
            lines.append("---")
            lines.append("")

    # Save raw responses that differ from parsed text
    for r in succeeded:
        if r.raw_response and r.raw_response != r.text:
            raw_path = path.parent / f"{r.custom_id}_raw.txt"
            raw_path.write_text(r.raw_response, encoding="utf-8")

    report = "\n".join(lines)
    path.write_text(report, encoding="utf-8")
    print(f"[batch/retrieve] Report saved to: {path}")
    print(f"[batch/retrieve] Total report size: {len(report):,} characters")


def retrieve_and_save(config: BatchConfig, api_key: str | None = None) -> list[RequestResult]:
    """
    Convenience: retrieve results and save a Markdown report in one call.
    """
    results = retrieve_results(config, api_key=api_key)

    if not results:
        print("[batch/retrieve] No results retrieved (batch may still be processing).")
        return results

    config.output_dir.mkdir(parents=True, exist_ok=True)
    slug = _slugify(config.name)
    output_path = config.output_dir / f"{slug}_REPORT.md"

    save_results_markdown(results, output_path, title=config.name, batch_id=config.load_batch_id())
    return results


def _slugify(text: str) -> str:
    import re
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[_\s]+", "-", slug)
    return slug
