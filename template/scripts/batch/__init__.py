"""
scripts.batch — Generic Anthropic Batch API Toolkit

A reusable toolkit for submitting, polling, and retrieving results from
the Anthropic Batch API. Designed for document review, coherence auditing,
and any parallel LLM task pipeline.

This is the TEMPLATE VERSION — bundled with new projects generated from
the workbench template. The canonical source is in scripts/batch/ at
the workbench root.

Usage:
    from scripts.batch import BatchConfig, submit_batch, retrieve_results

Modules:
    config  — BatchConfig dataclass and YAML loader
    submit  — Batch submission logic
    retrieve — Result retrieval and parsing
    poll    — Polling utility
    cli     — Command-line interface
    generate — Batch script generator
"""

from scripts.batch.config import BatchConfig, RequestSpec
from scripts.batch.submit import submit_batch, submit_batch_from_yaml
from scripts.batch.retrieve import RequestResult, retrieve_results, save_results_markdown, retrieve_and_save
from scripts.batch.poll import poll_until_complete

__all__ = [
    "BatchConfig",
    "RequestSpec",
    "submit_batch",
    "submit_batch_from_yaml",
    "RequestResult",
    "retrieve_results",
    "save_results_markdown",
    "retrieve_and_save",
    "poll_until_complete",
]
