"""
triage_dashboard.py — Calypso Triage Dashboard Generator

Reads the final backlog (with GREEN/ORANGE classification) and generates
a human-readable Markdown triage dashboard with checkboxes for ORANGE items.

Usage:
    python src/calypso/triage_dashboard.py
    python src/calypso/triage_dashboard.py --final-backlog batch_artifacts/final_backlog.json
    python src/calypso/triage_dashboard.py --output batch_artifacts/triage_dashboard.md

Output:
    batch_artifacts/triage_dashboard.md  — human triage dashboard
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_FINAL_BACKLOG = "batch_artifacts/final_backlog.json"
DEFAULT_OUTPUT_PATH = "batch_artifacts/triage_dashboard.md"

PRIORITY_EMOJI = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
PHASE_LABEL = {
    "PHASE-A": "Foundation",
    "PHASE-B": "Core Features",
    "PHASE-C": "Quality & Testing",
    "PHASE-D": "Advanced Features",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_final_backlog(path: str) -> dict:
    """Load final backlog JSON."""
    p = Path(path)
    if not p.exists():
        print(f"ERROR: Final backlog not found: {path}", file=sys.stderr)
        print("Run orchestrator_phase4.py first.", file=sys.stderr)
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def format_acceptance_criteria(criteria: list[str]) -> str:
    """Format acceptance criteria as a markdown list."""
    if not criteria:
        return "  *(no acceptance criteria defined)*\n"
    return "".join(f"  - {ac}\n" for ac in criteria)


def generate_dashboard(backlog: dict) -> str:
    """Generate the triage dashboard markdown."""
    items = backlog.get("items", [])
    summary = backlog.get("summary", {})
    prd_ref = backlog.get("prd_ref", "unknown")
    generated_at = backlog.get("generated_at", datetime.now(timezone.utc).isoformat())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    green_items = [i for i in items if i.get("classification") == "GREEN"]
    orange_items = [i for i in items if i.get("classification") == "ORANGE"]

    lines = []

    # Header
    lines.append("# Calypso Triage Dashboard\n")
    lines.append(f"**Generated:** {now}  \n")
    lines.append(f"**PRD:** `{prd_ref}`  \n")
    lines.append(f"**Backlog generated at:** {generated_at}  \n")
    lines.append("\n---\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Status | Count | Action Required |\n")
    lines.append("|--------|-------|----------------|\n")
    lines.append(f"| 🟢 GREEN | {len(green_items)} | None — auto-accepted |\n")
    lines.append(f"| 🟠 ORANGE | {len(orange_items)} | **Human review required** |\n")
    lines.append(f"| **Total** | **{len(items)}** | |\n")
    lines.append("\n")

    if orange_items:
        lines.append("> ⚠️ **Action required:** Review ORANGE items below and check either `ACCEPT` or `REJECT` for each.\n")
        lines.append("> After completing your review, run:\n")
        lines.append("> ```\n")
        lines.append("> python src/calypso/apply_triage.py\n")
        lines.append("> ```\n")
        lines.append("\n---\n")

    # ORANGE items section (requires human action)
    if orange_items:
        lines.append("## 🟠 ORANGE Items — Human Review Required\n")
        lines.append(
            "> For each item below, check **one** box: `ACCEPT` to include in the backlog, "
            "`REJECT` to discard.\n\n"
        )

        for item in orange_items:
            item_id = item["id"]
            priority = item.get("priority", "MEDIUM")
            phase = item.get("phase", "PHASE-A")
            phase_label = PHASE_LABEL.get(phase, phase)
            priority_emoji = PRIORITY_EMOJI.get(priority, "⚪")

            lines.append(f"### {item_id}: {item['title']}\n")
            lines.append(f"**Priority:** {priority_emoji} {priority} | **Phase:** {phase} ({phase_label})  \n")
            lines.append(f"**Source experts:** {', '.join(item.get('source_experts', []))}  \n\n")
            lines.append(f"**Description:**  \n{item['description']}\n\n")
            lines.append(f"**Acceptance Criteria:**  \n")
            lines.append(format_acceptance_criteria(item.get("acceptance_criteria", [])))
            lines.append(f"\n**⚠️ Devil's Advocate Challenge:**  \n")
            lines.append(f"> {item.get('challenge', 'No challenge text provided.')}\n\n")
            lines.append(f"**Your Decision:**  \n")
            lines.append(f"- [ ] ACCEPT — Include this item in the backlog  \n")
            lines.append(f"- [ ] REJECT — Discard this item  \n")
            lines.append("\n---\n")

    # GREEN items section (informational)
    if green_items:
        lines.append("## 🟢 GREEN Items — Auto-Accepted\n")
        lines.append(
            "> These items passed the Devil's Advocate review and are automatically included "
            "in the backlog. No action required.\n\n"
        )
        lines.append("| ID | Title | Priority | Phase |\n")
        lines.append("|----|-------|----------|-------|\n")

        for item in green_items:
            item_id = item["id"]
            title = item["title"][:70] + ("..." if len(item["title"]) > 70 else "")
            priority = item.get("priority", "MEDIUM")
            phase = item.get("phase", "PHASE-A")
            priority_emoji = PRIORITY_EMOJI.get(priority, "⚪")
            lines.append(f"| {item_id} | {title} | {priority_emoji} {priority} | {phase} |\n")

        lines.append("\n")

    # Footer instructions
    lines.append("---\n")
    lines.append("## Instructions\n\n")
    lines.append("1. Review each ORANGE item above\n")
    lines.append("2. For each ORANGE item, check **exactly one** box: `ACCEPT` or `REJECT`\n")
    lines.append("3. Save this file\n")
    lines.append("4. Run `apply_triage.py` to apply your decisions:\n")
    lines.append("   ```\n")
    lines.append("   python src/calypso/apply_triage.py\n")
    lines.append("   ```\n")
    lines.append("5. `apply_triage.py` will update `memory-bank/hot-context/systemPatterns.md` ")
    lines.append("and `productContext.md` with accepted items\n")

    return "".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso: Generate human triage dashboard from final backlog"
    )
    parser.add_argument(
        "--final-backlog",
        default=DEFAULT_FINAL_BACKLOG,
        help=f"Path to final_backlog.json (default: {DEFAULT_FINAL_BACKLOG})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output path for triage_dashboard.md (default: {DEFAULT_OUTPUT_PATH})",
    )
    args = parser.parse_args()

    backlog = load_final_backlog(args.final_backlog)
    dashboard = generate_dashboard(backlog)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dashboard, encoding="utf-8")

    items = backlog.get("items", [])
    orange_count = sum(1 for i in items if i.get("classification") == "ORANGE")
    green_count = sum(1 for i in items if i.get("classification") == "GREEN")

    print(f"\n✓ Triage dashboard saved: {output_path}")
    print(f"  GREEN (auto-accepted): {green_count}")
    print(f"  ORANGE (review needed): {orange_count}")

    if orange_count > 0:
        print(f"\n⚠️  Action required: Open {output_path} and check boxes for {orange_count} ORANGE item(s)")
        print(f"   Then run: python src/calypso/apply_triage.py")
    else:
        print(f"\n✓ No ORANGE items — all items auto-accepted. Run apply_triage.py to update memory bank.")
        print(f"   python src/calypso/apply_triage.py")


if __name__ == "__main__":
    main()
