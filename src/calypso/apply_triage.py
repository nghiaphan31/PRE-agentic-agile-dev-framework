"""
apply_triage.py — Calypso Triage Decision Applier

Reads the human-reviewed triage_dashboard.md (with checkbox decisions),
updates final_backlog.json with human_decision values, and appends
accepted items to memory-bank/hot-context/systemPatterns.md and productContext.md.

Usage:
    python src/calypso/apply_triage.py
    python src/calypso/apply_triage.py --dashboard batch_artifacts/triage_dashboard.md
    python src/calypso/apply_triage.py --dry-run

Output:
    - batch_artifacts/final_backlog.json updated (human_decision fields set)
    - memory-bank/hot-context/systemPatterns.md updated
    - memory-bank/hot-context/productContext.md updated
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_DASHBOARD = "batch_artifacts/triage_dashboard.md"
DEFAULT_FINAL_BACKLOG = "batch_artifacts/final_backlog.json"
DEFAULT_SYSTEMPATTERNS = "memory-bank/hot-context/systemPatterns.md"
DEFAULT_PRODUCTCONTEXT = "memory-bank/hot-context/productContext.md"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_checkbox_decisions(dashboard_text: str) -> dict[str, str]:
    """
    Parse checkbox decisions from triage_dashboard.md.

    Looks for patterns like:
        ### BL-001: Title
        ...
        - [x] ACCEPT — Include this item in the backlog
        - [ ] REJECT — Discard this item

    Returns dict: {item_id: "ACCEPT" | "REJECT"}
    """
    decisions = {}

    # Split dashboard into per-item sections using ### BL-XXX: as delimiter
    # Each section starts with ### BL-XXX: and ends before the next ### or end of string
    section_pattern = re.compile(r"###\s+(BL-\d+):[^\n]*\n(.*?)(?=\n###\s+BL-|\Z)", re.DOTALL)

    for match in section_pattern.finditer(dashboard_text):
        item_id = match.group(1)
        section_body = match.group(2)

        # Look for checked checkboxes in this section
        # Matches: - [x] ACCEPT ... or - [x] REJECT ...
        accept_checked = bool(re.search(r"- \[x\]\s+ACCEPT", section_body, re.IGNORECASE))
        reject_checked = bool(re.search(r"- \[x\]\s+REJECT", section_body, re.IGNORECASE))

        if accept_checked and not reject_checked:
            decisions[item_id] = "ACCEPT"
        elif reject_checked and not accept_checked:
            decisions[item_id] = "REJECT"
        elif accept_checked and reject_checked:
            print(f"  WARNING: {item_id} has both ACCEPT and REJECT checked. Defaulting to REJECT.", file=sys.stderr)
            decisions[item_id] = "REJECT"
        else:
            print(f"  WARNING: {item_id} has no checkbox checked. Skipping.", file=sys.stderr)

    return decisions


# ---------------------------------------------------------------------------
# Memory bank updates
# ---------------------------------------------------------------------------

def format_item_for_systempatterns(item: dict) -> str:
    """Format a backlog item as a systemPatterns.md entry."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"\n## [{item['id']}] {item['title']}\n",
        f"**Added:** {now}  \n",
        f"**Priority:** {item.get('priority', 'MEDIUM')} | **Phase:** {item.get('phase', 'PHASE-A')}  \n",
        f"**Source:** {', '.join(item.get('source_experts', []))}  \n\n",
        f"{item['description']}\n\n",
        f"**Acceptance Criteria:**\n",
    ]
    for ac in item.get("acceptance_criteria", []):
        lines.append(f"- {ac}\n")
    lines.append("\n---\n")
    return "".join(lines)


def format_item_for_productcontext(item: dict) -> str:
    """Format a backlog item as a productContext.md user story entry."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"\n### [{item['id']}] {item['title']}\n",
        f"**Status:** To Do | **Priority:** {item.get('priority', 'MEDIUM')} | **Added:** {now}  \n\n",
        f"{item['description']}\n\n",
        f"**Acceptance Criteria:**\n",
    ]
    for ac in item.get("acceptance_criteria", []):
        lines.append(f"- [ ] {ac}\n")
    lines.append("\n")
    return "".join(lines)


def append_to_file(file_path: str, content: str, dry_run: bool) -> None:
    """Append content to a file."""
    path = Path(file_path)
    if not path.exists():
        print(f"  WARNING: {file_path} does not exist. Creating it.", file=sys.stderr)
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    if dry_run:
        print(f"  [DRY RUN] Would append {len(content)} chars to {file_path}")
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] Updated: {file_path}")


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def apply_decisions(
    dashboard_path: str,
    backlog_path: str,
    systempatterns_path: str,
    productcontext_path: str,
    dry_run: bool,
) -> None:
    """Main logic: parse decisions, update backlog, update memory bank."""

    # Load dashboard
    dashboard_file = Path(dashboard_path)
    if not dashboard_file.exists():
        print(f"ERROR: Triage dashboard not found: {dashboard_path}", file=sys.stderr)
        print("Run triage_dashboard.py first, then review and check boxes.", file=sys.stderr)
        sys.exit(1)
    dashboard_text = dashboard_file.read_text(encoding="utf-8")

    # Load final backlog
    backlog_file = Path(backlog_path)
    if not backlog_file.exists():
        print(f"ERROR: Final backlog not found: {backlog_path}", file=sys.stderr)
        sys.exit(1)
    with open(backlog_file, encoding="utf-8") as f:
        backlog = json.load(f)

    items = backlog.get("items", [])

    # Parse checkbox decisions
    print("\nParsing checkbox decisions from triage dashboard...")
    decisions = parse_checkbox_decisions(dashboard_text)
    print(f"  Found {len(decisions)} decision(s): {decisions}")

    # Separate items by classification
    green_items = [i for i in items if i.get("classification") == "GREEN"]
    orange_items = [i for i in items if i.get("classification") == "ORANGE"]

    # Check for unchecked ORANGE items
    unchecked = [i["id"] for i in orange_items if i["id"] not in decisions]
    if unchecked:
        print(f"\nWARNING: {len(unchecked)} ORANGE item(s) have no decision: {unchecked}", file=sys.stderr)
        print("These items will be skipped (not added to memory bank).", file=sys.stderr)

    # Build accepted items list (GREEN auto-accepted + ORANGE with ACCEPT decision)
    accepted_items = list(green_items)  # All GREEN items are auto-accepted
    rejected_items = []

    for item in orange_items:
        decision = decisions.get(item["id"])
        if decision == "ACCEPT":
            item["human_decision"] = "ACCEPT"
            accepted_items.append(item)
        elif decision == "REJECT":
            item["human_decision"] = "REJECT"
            rejected_items.append(item)
        else:
            item["human_decision"] = None  # No decision made

    # Update backlog with human decisions
    print(f"\nUpdating final_backlog.json...")
    if not dry_run:
        backlog_file.write_text(json.dumps(backlog, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [OK] Updated: {backlog_path}")
    else:
        print(f"  [DRY RUN] Would update: {backlog_path}")

    # Append accepted items to systemPatterns.md
    print(f"\nUpdating systemPatterns.md ({len(accepted_items)} accepted items)...")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sp_header = f"\n\n<!-- Calypso triage applied: {now} -->\n"
    sp_content = sp_header + "".join(format_item_for_systempatterns(i) for i in accepted_items)
    append_to_file(systempatterns_path, sp_content, dry_run)

    # Append accepted items to productContext.md
    print(f"\nUpdating productContext.md ({len(accepted_items)} accepted items)...")
    pc_header = f"\n\n## Backlog Items (from Calypso — {now})\n"
    pc_content = pc_header + "".join(format_item_for_productcontext(i) for i in accepted_items)
    append_to_file(productcontext_path, pc_content, dry_run)

    # Summary
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}[DONE] Triage applied successfully!")
    print(f"  Accepted (GREEN auto + ORANGE ACCEPT): {len(accepted_items)}")
    print(f"  Rejected (ORANGE REJECT): {len(rejected_items)}")
    print(f"  Skipped (no decision): {len(unchecked)}")
    print(f"\nNext steps:")
    print(f"  1. Review memory-bank/hot-context/systemPatterns.md")
    print(f"  2. Review memory-bank/hot-context/productContext.md")
    print(f"  3. Commit the changes:")
    print(f"     git add .")
    print(f"     git commit -m \"feat(backlog): apply Calypso triage -- {len(accepted_items)} items accepted\"")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Calypso: Apply human triage decisions to memory bank"
    )
    parser.add_argument(
        "--dashboard",
        default=DEFAULT_DASHBOARD,
        help=f"Path to reviewed triage_dashboard.md (default: {DEFAULT_DASHBOARD})",
    )
    parser.add_argument(
        "--final-backlog",
        default=DEFAULT_FINAL_BACKLOG,
        help=f"Path to final_backlog.json (default: {DEFAULT_FINAL_BACKLOG})",
    )
    parser.add_argument(
        "--systempatterns",
        default=DEFAULT_SYSTEMPATTERNS,
        help=f"Path to systemPatterns.md (default: {DEFAULT_SYSTEMPATTERNS})",
    )
    parser.add_argument(
        "--productcontext",
        default=DEFAULT_PRODUCTCONTEXT,
        help=f"Path to productContext.md (default: {DEFAULT_PRODUCTCONTEXT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without writing any files",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN MODE — no files will be modified\n")

    apply_decisions(
        dashboard_path=args.dashboard,
        backlog_path=args.final_backlog,
        systempatterns_path=args.systempatterns,
        productcontext_path=args.productcontext,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
