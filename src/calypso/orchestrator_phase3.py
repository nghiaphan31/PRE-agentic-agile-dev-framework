"""
orchestrator_phase3.py — Calypso Phase 3 Orchestrator

Reads expert reports from Phase 2 and calls the Synthesizer Agent (SP-008)
to consolidate them into a structured draft backlog.

Usage:
    python src/calypso/orchestrator_phase3.py
    python src/calypso/orchestrator_phase3.py --expert-reports-dir batch_artifacts/expert_reports
    python src/calypso/orchestrator_phase3.py --prd docs/releases/v2.0/DOC-1-v2.0-PRD.md

Output:
    batch_artifacts/draft_backlog.json  — structured backlog items
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import jsonschema

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-5"          # Synthesizer needs stronger reasoning
MAX_TOKENS = 4096
DEFAULT_EXPERT_REPORTS_DIR = "batch_artifacts/expert_reports"
DEFAULT_PRD_PATH = "docs/releases/v2.0/DOC-1-v2.0-PRD.md"
DEFAULT_OUTPUT_PATH = "batch_artifacts/draft_backlog.json"
SCHEMA_PATH = Path(__file__).parent / "schemas" / "backlog_item.json"

# SP-008 Synthesizer Agent system prompt (inline for portability)
SP_008_SYSTEM = """You are the Synthesizer Agent for the Agentic Agile Workbench.

Your role is to consolidate expert review reports into a structured product backlog.

## Input
You will receive:
1. A Product Requirements Document (PRD)
2. Expert reports from 4 agents: architecture_expert, security_expert, ux_expert, qa_expert

## Task
Analyze all expert findings and produce a comprehensive, deduplicated backlog.

## Rules
1. Each backlog item must address at least one expert finding
2. Deduplicate: if multiple experts raise the same issue, create ONE item citing all sources
3. Prioritize: HIGH = blocks core functionality or is a security risk; MEDIUM = important but not blocking; LOW = nice to have
4. Phase assignment: PHASE-A = foundation/infrastructure; PHASE-B = core features; PHASE-C = quality/testing; PHASE-D = advanced features
5. Acceptance criteria must be specific and testable (not vague like "works correctly")
6. Minimum 5 backlog items, maximum 20

## Output Format
Respond ONLY with a valid JSON object. No markdown, no explanation, just JSON:

{
  "version": "1.0",
  "prd_ref": "<prd_path>",
  "generated_at": "<ISO8601>",
  "items": [
    {
      "id": "BL-001",
      "title": "<concise title, max 120 chars>",
      "description": "<detailed description>",
      "acceptance_criteria": ["<testable criterion 1>", "<testable criterion 2>"],
      "source_experts": ["<expert_role>"],
      "priority": "HIGH|MEDIUM|LOW",
      "phase": "PHASE-A|PHASE-B|PHASE-C|PHASE-D"
    }
  ]
}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_schema() -> dict | None:
    """Load the backlog item JSON schema."""
    if not SCHEMA_PATH.exists():
        print(f"WARNING: Schema not found at {SCHEMA_PATH}. Skipping validation.", file=sys.stderr)
        return None
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_expert_reports(reports_dir: str) -> list[dict]:
    """Load all expert report JSON files from the reports directory."""
    path = Path(reports_dir)
    if not path.exists():
        print(f"ERROR: Expert reports directory not found: {reports_dir}", file=sys.stderr)
        print("Run check_batch_status.py first to retrieve expert reports.", file=sys.stderr)
        sys.exit(1)

    reports = []
    for json_file in sorted(path.glob("*.json")):
        if json_file.name.endswith("_raw.txt"):
            continue
        try:
            with open(json_file, encoding="utf-8") as f:
                report = json.load(f)
            reports.append(report)
            print(f"  Loaded: {json_file.name}")
        except json.JSONDecodeError as e:
            print(f"  WARNING: Could not parse {json_file.name}: {e}", file=sys.stderr)

    if not reports:
        print(f"ERROR: No expert reports found in {reports_dir}", file=sys.stderr)
        sys.exit(1)

    return reports


def load_prd(prd_path: str) -> str:
    """Load PRD content."""
    path = Path(prd_path)
    if not path.exists():
        print(f"ERROR: PRD not found: {prd_path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def build_synthesis_prompt(prd_content: str, prd_path: str, reports: list[dict]) -> str:
    """Build the user message for the Synthesizer Agent."""
    parts = [
        f"## PRD Document\n\nPath: {prd_path}\n\n{prd_content}",
        "\n\n---\n\n## Expert Reports\n",
    ]

    for report in reports:
        expert_id = report.get("expert_id", "unknown")
        summary = report.get("summary", "No summary provided.")
        findings = report.get("findings", [])

        parts.append(f"\n### {expert_id}\n\n**Summary:** {summary}\n\n**Findings:**\n")
        for i, finding in enumerate(findings, 1):
            parts.append(
                f"{i}. [{finding.get('severity', 'INFO')}] {finding.get('category', 'general')}: "
                f"{finding.get('description', '')} "
                f"→ Recommendation: {finding.get('recommendation', '')} "
                f"→ Backlog suggestion: {finding.get('backlog_suggestion', 'N/A')}\n"
            )

    parts.append(
        f"\n\n---\n\nPlease synthesize the above into a structured backlog JSON. "
        f"Use prd_ref: \"{prd_path}\" and generated_at: \"{datetime.now(timezone.utc).isoformat()}\"."
    )

    return "".join(parts)


def validate_backlog(backlog: dict, schema: dict | None) -> bool:
    """Validate the backlog structure."""
    if not isinstance(backlog, dict):
        print("ERROR: Backlog is not a JSON object.", file=sys.stderr)
        return False

    if "items" not in backlog:
        print("ERROR: Backlog missing 'items' field.", file=sys.stderr)
        return False

    items = backlog["items"]
    if len(items) < 5:
        print(f"WARNING: Only {len(items)} backlog items (minimum 5 recommended).", file=sys.stderr)

    if schema is None:
        return True

    # Build a wrapper schema for the full backlog document
    wrapper_schema = {
        "type": "object",
        "required": ["version", "prd_ref", "generated_at", "items"],
        "properties": {
            "version": {"type": "string"},
            "prd_ref": {"type": "string"},
            "generated_at": {"type": "string"},
            "items": {
                "type": "array",
                "items": schema,
            },
        },
    }

    try:
        jsonschema.validate(instance=backlog, schema=wrapper_schema)
        return True
    except jsonschema.ValidationError as e:
        print(f"WARNING: Schema validation failed: {e.message}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def synthesize_backlog(prd_content: str, prd_path: str, reports: list[dict]) -> dict:
    """Call Synthesizer Agent to produce draft backlog."""
    client = anthropic.Anthropic()

    user_message = build_synthesis_prompt(prd_content, prd_path, reports)

    print(f"\nCalling Synthesizer Agent (SP-008)...")
    print(f"  Model: {MODEL}")
    print(f"  Expert reports: {len(reports)}")

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SP_008_SYSTEM,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = response.content[0].text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    try:
        backlog = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"ERROR: Synthesizer returned invalid JSON: {e}", file=sys.stderr)
        # Save raw response for debugging
        debug_file = Path(DEFAULT_OUTPUT_PATH).parent / "synthesizer_raw.txt"
        debug_file.parent.mkdir(parents=True, exist_ok=True)
        debug_file.write_text(raw_text, encoding="utf-8")
        print(f"Raw response saved to: {debug_file}", file=sys.stderr)
        sys.exit(1)

    return backlog


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso Phase 3: Synthesize expert reports into draft backlog"
    )
    parser.add_argument(
        "--expert-reports-dir",
        default=DEFAULT_EXPERT_REPORTS_DIR,
        help=f"Directory containing expert reports (default: {DEFAULT_EXPERT_REPORTS_DIR})",
    )
    parser.add_argument(
        "--prd",
        default=DEFAULT_PRD_PATH,
        help=f"Path to PRD document (default: {DEFAULT_PRD_PATH})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output path for draft_backlog.json (default: {DEFAULT_OUTPUT_PATH})",
    )
    args = parser.parse_args()

    # Validate API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    print("Loading expert reports...")
    reports = load_expert_reports(args.expert_reports_dir)
    print(f"  Loaded {len(reports)} expert report(s)")

    prd_content = load_prd(args.prd)

    backlog = synthesize_backlog(prd_content, args.prd, reports)

    schema = load_schema()
    valid = validate_backlog(backlog, schema)

    # Save backlog
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(backlog, indent=2, ensure_ascii=False), encoding="utf-8")

    item_count = len(backlog.get("items", []))
    print(f"\n✓ Draft backlog saved: {output_path}")
    print(f"  Items: {item_count}")
    print(f"  Schema valid: {valid}")
    print(f"\nNext step:")
    print(f"  python src/calypso/orchestrator_phase4.py --draft-backlog {args.output}")


if __name__ == "__main__":
    main()
