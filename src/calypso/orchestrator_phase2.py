"""
orchestrator_phase2.py — Calypso Phase 2 Orchestrator

Reads a PRD document and dispatches it to the Anthropic Batch API
with 4 expert agents (architecture, security, UX, QA).

Usage:
    python src/calypso/orchestrator_phase2.py --prd docs/releases/v2.0/DOC-1-v2.0-PRD.md
    python src/calypso/orchestrator_phase2.py --prd docs/releases/v2.0/DOC-1-v2.0-PRD.md --output-dir batch_artifacts/

Output:
    batch_artifacts/batch_id_phase2.txt  — Anthropic Batch job ID
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL = "claude-haiku-4-5"          # Cost-efficient for batch expert reviews
MAX_TOKENS = 2048
DEFAULT_OUTPUT_DIR = "batch_artifacts"

EXPERT_AGENTS = [
    {
        "id": "architecture_expert",
        "role": "architecture_expert",
        "system": (
            "You are a senior software architect with 15 years of experience. "
            "Your task is to review a Product Requirements Document (PRD) and identify "
            "technical feasibility issues, architectural risks, scalability concerns, "
            "and missing technical specifications. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "expert_id": "architecture_expert",\n'
            '  "expert_role": "architecture_expert",\n'
            '  "prd_ref": "<prd_path>",\n'
            '  "generated_at": "<ISO8601>",\n'
            '  "findings": [\n'
            '    {\n'
            '      "category": "<string>",\n'
            '      "severity": "HIGH|MEDIUM|LOW|INFO",\n'
            '      "description": "<string>",\n'
            '      "recommendation": "<string>",\n'
            '      "backlog_suggestion": "<optional string>"\n'
            "    }\n"
            "  ],\n"
            '  "summary": "<string>"\n'
            "}"
        ),
    },
    {
        "id": "security_expert",
        "role": "security_expert",
        "system": (
            "You are a senior application security engineer with expertise in OWASP Top 10, "
            "data privacy (GDPR, CCPA), and secure software development. "
            "Your task is to review a PRD and identify security risks, authentication/authorization gaps, "
            "data privacy concerns, and missing security requirements. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "expert_id": "security_expert",\n'
            '  "expert_role": "security_expert",\n'
            '  "prd_ref": "<prd_path>",\n'
            '  "generated_at": "<ISO8601>",\n'
            '  "findings": [\n'
            '    {\n'
            '      "category": "<string>",\n'
            '      "severity": "HIGH|MEDIUM|LOW|INFO",\n'
            '      "description": "<string>",\n'
            '      "recommendation": "<string>",\n'
            '      "backlog_suggestion": "<optional string>"\n'
            "    }\n"
            "  ],\n"
            '  "summary": "<string>"\n'
            "}"
        ),
    },
    {
        "id": "ux_expert",
        "role": "ux_expert",
        "system": (
            "You are a senior UX designer and accessibility specialist. "
            "Your task is to review a PRD and identify user experience gaps, accessibility issues (WCAG 2.1), "
            "workflow clarity problems, and missing user-facing requirements. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "expert_id": "ux_expert",\n'
            '  "expert_role": "ux_expert",\n'
            '  "prd_ref": "<prd_path>",\n'
            '  "generated_at": "<ISO8601>",\n'
            '  "findings": [\n'
            '    {\n'
            '      "category": "<string>",\n'
            '      "severity": "HIGH|MEDIUM|LOW|INFO",\n'
            '      "description": "<string>",\n'
            '      "recommendation": "<string>",\n'
            '      "backlog_suggestion": "<optional string>"\n'
            "    }\n"
            "  ],\n"
            '  "summary": "<string>"\n'
            "}"
        ),
    },
    {
        "id": "qa_expert",
        "role": "qa_expert",
        "system": (
            "You are a senior QA engineer and test architect. "
            "Your task is to review a PRD and identify testability issues, incomplete acceptance criteria, "
            "missing edge cases, and requirements that are not verifiable. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "expert_id": "qa_expert",\n'
            '  "expert_role": "qa_expert",\n'
            '  "prd_ref": "<prd_path>",\n'
            '  "generated_at": "<ISO8601>",\n'
            '  "findings": [\n'
            '    {\n'
            '      "category": "<string>",\n'
            '      "severity": "HIGH|MEDIUM|LOW|INFO",\n'
            '      "description": "<string>",\n'
            '      "recommendation": "<string>",\n'
            '      "backlog_suggestion": "<optional string>"\n'
            "    }\n"
            "  ],\n"
            '  "summary": "<string>"\n'
            "}"
        ),
    },
]


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def read_prd(prd_path: str) -> str:
    """Read and return PRD content."""
    path = Path(prd_path)
    if not path.exists():
        print(f"ERROR: PRD file not found: {prd_path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def build_batch_requests(prd_content: str, prd_path: str) -> list[dict]:
    """Build the JSONL batch request list for all 4 expert agents."""
    now = datetime.now(timezone.utc).isoformat()
    requests = []

    user_message = (
        f"Please review the following Product Requirements Document (PRD) "
        f"and provide your expert analysis.\n\n"
        f"PRD path: {prd_path}\n"
        f"Review timestamp: {now}\n\n"
        f"---\n\n{prd_content}"
    )

    for agent in EXPERT_AGENTS:
        # Inject prd_ref and generated_at into system prompt
        system = agent["system"].replace("<prd_path>", prd_path).replace("<ISO8601>", now)

        requests.append({
            "custom_id": agent["id"],
            "params": {
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "system": system,
                "messages": [
                    {"role": "user", "content": user_message}
                ],
            },
        })

    return requests


def submit_batch(requests: list[dict], output_dir: str, prd_path: str) -> str:
    """Submit batch to Anthropic API and save batch ID."""
    client = anthropic.Anthropic()

    print(f"\nSubmitting batch with {len(requests)} expert agents...")
    print(f"  Model: {MODEL}")
    print(f"  PRD: {prd_path}")
    print(f"  Agents: {', '.join(a['id'] for a in EXPERT_AGENTS)}")

    # Build MessageBatchParam objects
    batch_params = []
    for req in requests:
        batch_params.append(
            anthropic.types.message_create_params.MessageCreateParamsNonStreaming(
                custom_id=req["custom_id"],
                params=req["params"],
            )
        )

    batch = client.messages.batches.create(requests=batch_params)
    batch_id = batch.id

    # Save batch ID
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    batch_id_file = output_path / "batch_id_phase2.txt"
    batch_id_file.write_text(batch_id, encoding="utf-8")

    # Save batch metadata
    metadata = {
        "batch_id": batch_id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "prd_ref": prd_path,
        "model": MODEL,
        "agents": [a["id"] for a in EXPERT_AGENTS],
        "status": "submitted",
    }
    metadata_file = output_path / "batch_metadata_phase2.json"
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"\n✓ Batch submitted successfully!")
    print(f"  Batch ID: {batch_id}")
    print(f"  Saved to: {batch_id_file}")
    print(f"\nEstimated completion: within 24 hours (typically 15-60 minutes)")
    print(f"Check status with:")
    print(f"  python src/calypso/check_batch_status.py --batch-id-file {batch_id_file}")

    return batch_id


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso Phase 2: Submit PRD to Anthropic Batch API for expert review"
    )
    parser.add_argument(
        "--prd",
        required=True,
        help="Path to the PRD document (e.g., docs/releases/v2.0/DOC-1-v2.0-PRD.md)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for batch artifacts (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    # Validate API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    prd_content = read_prd(args.prd)
    requests = build_batch_requests(prd_content, args.prd)
    batch_id = submit_batch(requests, args.output_dir, args.prd)

    return batch_id


if __name__ == "__main__":
    main()
