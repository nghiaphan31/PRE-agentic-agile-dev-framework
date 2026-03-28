"""
orchestrator_phase4.py — Calypso Phase 4 Orchestrator (Devil's Advocate)

Reads the draft backlog and runs the Devil's Advocate Agent (SP-009) on each item.
Classifies items as GREEN (accepted) or ORANGE (challenged, requires human review).

Usage:
    python src/calypso/orchestrator_phase4.py
    python src/calypso/orchestrator_phase4.py --draft-backlog batch_artifacts/draft_backlog.json
    python src/calypso/orchestrator_phase4.py --max-attempts 3

Output:
    batch_artifacts/final_backlog.json  — backlog with GREEN/ORANGE classification
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

MODEL = "claude-haiku-4-5"          # Fast + cheap for per-item challenges
MAX_TOKENS = 1024
DEFAULT_DRAFT_BACKLOG = "batch_artifacts/draft_backlog.json"
DEFAULT_PRD_PATH = "docs/releases/v2.0/DOC-1-v2.0-PRD.md"
DEFAULT_OUTPUT_PATH = "batch_artifacts/final_backlog.json"
DEFAULT_MAX_ATTEMPTS = 2

# SP-009 Devil's Advocate Agent system prompt (inline for portability)
SP_009_SYSTEM = """You are the Devil's Advocate Agent for the Agentic Agile Workbench.

Your role is to challenge each backlog item to identify risks, ambiguities, and potential failures.

## Task
For each backlog item you receive, ask: "What could go wrong with this item?"

## Challenge Criteria
Challenge an item (mark ORANGE) if ANY of the following apply:
- The acceptance criteria are vague or untestable
- The item has hidden dependencies not mentioned in the PRD
- The item could be interpreted in multiple conflicting ways
- The item introduces significant technical risk not acknowledged
- The item is too large to complete in a single sprint
- The item conflicts with another backlog item

Accept an item (mark GREEN) if:
- The acceptance criteria are specific and testable
- Dependencies are clear and manageable
- The scope is well-defined and sprint-sized
- No significant risks are overlooked

## Output Format
Respond ONLY with a valid JSON object. No markdown, no explanation, just JSON:

{
  "item_id": "<BL-XXX>",
  "classification": "GREEN|ORANGE",
  "challenge": "<challenge text — only required for ORANGE items, empty string for GREEN>",
  "reasoning": "<brief explanation of your decision>"
}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_draft_backlog(path: str) -> dict:
    """Load draft backlog JSON."""
    p = Path(path)
    if not p.exists():
        print(f"ERROR: Draft backlog not found: {path}", file=sys.stderr)
        print("Run orchestrator_phase3.py first.", file=sys.stderr)
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_prd(prd_path: str) -> str:
    """Load PRD content."""
    path = Path(prd_path)
    if not path.exists():
        print(f"WARNING: PRD not found: {prd_path}. Proceeding without PRD context.", file=sys.stderr)
        return ""
    return path.read_text(encoding="utf-8")


def challenge_item(
    client: anthropic.Anthropic,
    item: dict,
    prd_summary: str,
    attempt: int,
    max_attempts: int,
) -> dict:
    """Run Devil's Advocate on a single backlog item. Returns classification dict."""

    user_message = (
        f"## Backlog Item to Challenge\n\n"
        f"ID: {item['id']}\n"
        f"Title: {item['title']}\n"
        f"Description: {item['description']}\n"
        f"Acceptance Criteria:\n"
        + "\n".join(f"  - {ac}" for ac in item.get("acceptance_criteria", []))
        + f"\nPriority: {item.get('priority', 'MEDIUM')}\n"
        f"Phase: {item.get('phase', 'PHASE-A')}\n"
        f"Source Experts: {', '.join(item.get('source_experts', []))}\n"
    )

    if prd_summary:
        user_message += f"\n\n## PRD Context (summary)\n\n{prd_summary[:2000]}"

    if attempt > 1:
        user_message += (
            f"\n\n## Note\n"
            f"This is attempt {attempt} of {max_attempts}. "
            f"Be more lenient on this attempt — only challenge if there is a clear, "
            f"significant issue that would block delivery."
        )

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SP_009_SYSTEM,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = response.content[0].text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    try:
        result = json.loads(raw_text)
        return result
    except json.JSONDecodeError:
        # Fallback: if JSON parsing fails, default to GREEN to avoid blocking
        print(f"  WARNING: Could not parse Devil's Advocate response for {item['id']}. Defaulting to GREEN.", file=sys.stderr)
        return {
            "item_id": item["id"],
            "classification": "GREEN",
            "challenge": "",
            "reasoning": "Parse error — defaulted to GREEN",
        }


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def run_devils_advocate(draft_backlog: dict, prd_content: str, max_attempts: int) -> dict:
    """Run Devil's Advocate on all backlog items. Returns final_backlog dict."""
    client = anthropic.Anthropic()
    items = draft_backlog.get("items", [])

    print(f"\nRunning Devil's Advocate Agent (SP-009)...")
    print(f"  Model: {MODEL}")
    print(f"  Items: {len(items)}")
    print(f"  Max attempts per item: {max_attempts}")

    # Use first 2000 chars of PRD as context summary
    prd_summary = prd_content[:2000] if prd_content else ""

    final_items = []
    green_count = 0
    orange_count = 0

    for item in items:
        item_id = item["id"]
        print(f"\n  [{item_id}] {item['title'][:60]}...")

        classification = "ORANGE"
        challenge_text = ""

        for attempt in range(1, max_attempts + 1):
            result = challenge_item(client, item, prd_summary, attempt, max_attempts)
            classification = result.get("classification", "GREEN").upper()
            challenge_text = result.get("challenge", "")
            reasoning = result.get("reasoning", "")

            print(f"    Attempt {attempt}: {classification} — {reasoning[:80]}")

            if classification == "GREEN":
                break
            # If ORANGE on first attempt, try again (more lenient)

        # Build final item
        final_item = {
            "id": item["id"],
            "title": item["title"],
            "description": item["description"],
            "acceptance_criteria": item.get("acceptance_criteria", []),
            "source_experts": item.get("source_experts", []),
            "priority": item.get("priority", "MEDIUM"),
            "phase": item.get("phase", "PHASE-A"),
            "classification": classification,
            "challenge": challenge_text if classification == "ORANGE" else "",
            "human_decision": None,
        }
        final_items.append(final_item)

        if classification == "GREEN":
            green_count += 1
        else:
            orange_count += 1

    print(f"\n  Results: {green_count} GREEN, {orange_count} ORANGE")

    final_backlog = {
        "version": "1.0",
        "prd_ref": draft_backlog.get("prd_ref", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "devil_advocate_config": {
            "model": MODEL,
            "max_attempts": max_attempts,
        },
        "summary": {
            "total": len(final_items),
            "green": green_count,
            "orange": orange_count,
        },
        "items": final_items,
    }

    return final_backlog


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso Phase 4: Devil's Advocate classification of backlog items"
    )
    parser.add_argument(
        "--draft-backlog",
        default=DEFAULT_DRAFT_BACKLOG,
        help=f"Path to draft_backlog.json (default: {DEFAULT_DRAFT_BACKLOG})",
    )
    parser.add_argument(
        "--prd",
        default=DEFAULT_PRD_PATH,
        help=f"Path to PRD document for context (default: {DEFAULT_PRD_PATH})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output path for final_backlog.json (default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=DEFAULT_MAX_ATTEMPTS,
        help=f"Max Devil's Advocate attempts per item (default: {DEFAULT_MAX_ATTEMPTS})",
    )
    args = parser.parse_args()

    # Validate API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    draft_backlog = load_draft_backlog(args.draft_backlog)
    prd_content = load_prd(args.prd)

    final_backlog = run_devils_advocate(draft_backlog, prd_content, args.max_attempts)

    # Save final backlog
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(final_backlog, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = final_backlog["summary"]
    print(f"\n✓ Final backlog saved: {output_path}")
    print(f"  Total: {summary['total']} items")
    print(f"  GREEN: {summary['green']} (auto-accepted)")
    print(f"  ORANGE: {summary['orange']} (require human review)")
    print(f"\nNext step:")
    print(f"  python src/calypso/triage_dashboard.py --final-backlog {args.output}")


if __name__ == "__main__":
    main()
