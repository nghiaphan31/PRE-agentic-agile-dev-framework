"""
detect-merged-features.py — Detect and add all features merged to develop since last release tag

This script detects ALL merged feature/fix/hotfix branches to develop since
the last release tag and automatically adds them to the next release scope.

Usage:
    # Detect all merged features and add to release scope
    python scripts/detect-merged-features.py

    # Detect since specific tag
    python scripts/detect-merged-features.py --tag v2.10.0

    # Show verbose output
    python scripts/detect-merged-features.py --verbose

    # Dry run (don't write any files)
    python scripts/detect-merged-features.py --dry-run

Exit codes:
    0 - Success
    1 - Error (tag not found, git failure, etc.)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class MergedFeature:
    """
    Represents a branch detected from a merge to develop.

    Attributes:
        idea_id: IDEA-NNN if the branch has one, None otherwise
        tech_id: TECH-NNN if the branch has one, None otherwise
        branch_name: Full branch name
        feature_id: Identifier for scope - IDEA-NNN, TECH-NNN, or branch name
        commit_hash: Full commit SHA
        commit_message: Full commit message
        commit_date: ISO-formatted commit date
    """
    idea_id: Optional[str]
    tech_id: Optional[str]
    branch_name: Optional[str]
    feature_id: str
    commit_hash: str
    commit_message: str
    commit_date: str


# ---------------------------------------------------------------------------
# Core detection logic
# ---------------------------------------------------------------------------


def get_last_release_tag() -> Optional[str]:
    """Find the most recent v*.*.* tag."""
    result = subprocess.run(
        ["git", "tag", "--list", "v*.*.*", "--sort=-version:refname"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split("\n")[0]
    return None


def extract_branch_name(text: str) -> Optional[str]:
    """Extract branch name from merge commit message."""
    match = re.search(r"Merge branch '([^']+)'", text)
    return match.group(1) if match else None


def extract_identifiers(branch_name: str) -> tuple[Optional[str], Optional[str], str]:
    """
    Extract IDEA-NNN and TECH-NNN from branch name.

    Returns:
        (idea_id, tech_id, feature_id) where feature_id is the best identifier
    """
    idea_match = re.search(r'(IDEA-\d+)', branch_name)
    tech_match = re.search(r'(TECH-\d+)', branch_name)

    idea_id = idea_match.group(1) if idea_match else None
    tech_id = tech_match.group(1) if tech_match else None

    # Priority: IDEA > TECH > full branch name
    if idea_id:
        return idea_id, tech_id, idea_id
    if tech_id:
        return idea_id, tech_id, tech_id

    return idea_id, tech_id, branch_name


def is_tracked_branch(branch_name: str) -> bool:
    """
    Check if a branch should be tracked for release scope.

    Returns True for ALL branches merged to develop - any merge represents
    work done that may need to be included in the next release scope.
    """
    # Don't track develop or main itself
    if branch_name in ("develop", "main", "master"):
        return False
    return True


def get_merged_features_since_tag(tag: str, target_branch: str = "develop") -> list[MergedFeature]:
    """
    Get ALL feature branches merged to target_branch since the given tag.

    Args:
        tag: The starting tag (exclusive)
        target_branch: The branch to query (default: "develop")

    Returns:
        List of MergedFeature objects for all merged branches.
    """
    # Get merge commits since the tag
    result = subprocess.run(
        [
            "git", "log", f"{tag}..{target_branch}",
            "--first-parent", "--merges",
            "--format=%H|%s|%P|%ci"
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[ERROR] Git log failed: {result.stderr}", file=sys.stderr)
        return []

    features: dict[str, MergedFeature] = {}

    for line in result.stdout.strip().split("\n"):
        if not line:
            continue

        parts = line.split("|")
        if len(parts) < 3:
            continue

        commit_hash = parts[0]
        commit_message = parts[1]
        parents = parts[2].split()
        commit_date = parts[3] if len(parts) > 3 else ""

        # Only process merge commits
        if len(parents) < 2:
            continue

        # Extract branch name
        branch_name = extract_branch_name(commit_message)

        # Only track meaningful branches
        if not branch_name or not is_tracked_branch(branch_name):
            continue

        # Extract identifiers
        idea_id, tech_id, feature_id = extract_identifiers(branch_name)

        # Deduplicate by feature_id
        if feature_id not in features:
            features[feature_id] = MergedFeature(
                idea_id=idea_id,
                tech_id=tech_id,
                branch_name=branch_name,
                feature_id=feature_id,
                commit_hash=commit_hash,
                commit_message=commit_message,
                commit_date=commit_date,
            )

    return list(features.values())


def get_next_release_scope() -> Optional[Path]:
    """
    Find or determine the next release scope document.

    Returns:
        Path to the next release scope doc, or None.
    """
    releases_dir = Path("docs/releases")
    if not releases_dir.exists():
        return None

    # Look for highest version among existing release dirs
    highest_version = (0, 0)
    for d in releases_dir.iterdir():
        if d.is_dir():
            match = re.match(r'^v(\d+)\.(\d+)$', d.name)
            if match:
                version = (int(match.group(1)), int(match.group(2)))
                if version > highest_version:
                    highest_version = version

    # Determine next version
    major, minor = highest_version
    next_version = f"v{major}.{minor + 1}"

    next_dir = releases_dir / next_version
    next_doc = next_dir / f"DOC-3-{next_version}-Implementation-Plan.md"

    return next_doc


def add_feature_to_scope(feature_id: str, scope_doc: Path, dry_run: bool = False) -> bool:
    """
    Add a detected feature to the release scope document.

    Args:
        feature_id: The feature identifier to add
        scope_doc: Path to the release scope DOC-3 file
        dry_run: If True, don't write changes

    Returns:
        True if added successfully
    """
    if not scope_doc.exists():
        print(f"[WARN] Scope doc not found: {scope_doc}", file=sys.stderr)
        return False

    content = scope_doc.read_text(encoding="utf-8")

    # Check if already in scope
    if feature_id in content:
        return True

    # Find insertion point - look for feature list
    lines = content.split("\n")
    insert_idx = None

    # Find the Features section header
    for i, line in enumerate(lines):
        if re.match(r'^##+\s+.*[Ff]eatures?', line):
            insert_idx = i + 1
            break

    if insert_idx is None:
        print(f"[WARN] Could not find Features section in {scope_doc.name}", file=sys.stderr)
        return False

    # Build the new entry
    new_entry = f"- [ ] {feature_id} — [ADDED BY TECH-002 DETECTOR]"

    # Insert after existing items
    while insert_idx < len(lines) and re.match(r'^-\s*\[[ x]\]\s*', lines[insert_idx]):
        insert_idx += 1

    lines.insert(insert_idx, new_entry)

    if not dry_run:
        scope_doc.write_text("\n".join(lines), encoding="utf-8")

    print(f"[{'DRY-RUN' if dry_run else 'ADDED'}] {feature_id} -> {scope_doc.name}")
    return True


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def generate_report(features: list[MergedFeature], tag: Optional[str]) -> str:
    """Generate a human-readable report of detected features."""
    lines = [
        "# Merged Features Detection Report",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Since tag:** {tag or 'beginning'}",
        f"**Target branch:** develop",
        f"**Features detected:** {len(features)}",
        "",
    ]

    if not features:
        lines.append("_No features detected._")
    else:
        lines.extend([
            "## Detected Features",
            "",
            "| # | Feature ID | Branch |",
            "|:--|------------|--------|",
        ])
        for i, f in enumerate(sorted(features, key=lambda x: x.feature_id), 1):
            lines.append(f"| {i} | `{f.feature_id}` | `{f.branch_name}` |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Detect features merged to develop since last release tag.",
    )
    parser.add_argument("--tag", "-t", help="Starting tag (exclusive). Default: most recent v*.*.* tag")
    parser.add_argument("--branch", "-b", default="develop", help="Target branch (default: develop)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Don't write any files")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Find the tag
    tag = args.tag
    if not tag:
        tag = get_last_release_tag()
        if not tag:
            print("[ERROR] No release tags found. Use --tag to specify.", file=sys.stderr)
            return 1
        if args.verbose:
            print(f"[INFO] Using last release tag: {tag}")

    # Get merged features
    features = get_merged_features_since_tag(tag, args.branch)

    if not features:
        print("[INFO] No features detected.")
        return 0

    # Output report
    if args.json:
        import json
        print(json.dumps({
            "tag": tag,
            "branch": args.branch,
            "features": [
                {
                    "idea_id": f.idea_id,
                    "tech_id": f.tech_id,
                    "feature_id": f.feature_id,
                    "branch_name": f.branch_name,
                    "commit_hash": f.commit_hash[:7],
                }
                for f in features
            ],
        }, indent=2))
    else:
        print(generate_report(features, tag))

    # Auto-add to next release scope
    print("")
    scope_doc = get_next_release_scope()
    if scope_doc:
        print(f"[INFO] Adding features to: {scope_doc.name}")
        for f in features:
            add_feature_to_scope(f.feature_id, scope_doc, dry_run=args.dry_run)
    else:
        print("[WARN] Could not determine next release scope document")

    return 0


if __name__ == "__main__":
    sys.exit(main())
