#!/usr/bin/env python3
"""
Rebuild prompts/SP-002-clinerules-global.md from .clinerules.

This script is the canonical, cross-platform way to synchronize SP-002
(whose embedded code block must always match .clinerules byte-for-byte).

Usage:
    python scripts/rebuild_sp002.py [--check] [--dry-run]

Options:
    --check   Verify SP-002 matches .clinerules without writing anything.
    --dry-run Show what would be rebuilt without writing to disk.

Exit codes:
    0  SP-002 is synchronized (--check) OR rebuild succeeded (default)
    1  SP-002 differs from .clinerules (--check)
    2  Missing files or other error
"""

import argparse
import re
import sys
from pathlib import Path

SP002_PATH = Path("prompts/SP-002-clinerules-global.md")
CLINERULES_PATH = Path(".clinerules")


def extract_code_block(filepath: Path) -> str:
    """Extract the code block content from SP-002 (everything between the first ``` and last ```)."""
    content = filepath.read_text(encoding="utf-8")
    m = re.search(r"```(?:markdown|python)?\r?\n", content)
    if not m:
        raise ValueError(f"Cannot find opening code block delimiter in {filepath}")
    start = m.end()
    end = content.rfind("```")
    if end == -1:
        raise ValueError(f"Cannot find closing code block delimiter in {filepath}")
    return content[start:end]


def extract_header(filepath: Path) -> str:
    """Extract the header portion of SP-002 (everything up to and including opening ```)."""
    content = filepath.read_text(encoding="utf-8")
    m = re.search(r"```(?:markdown|python)?\r?\n", content)
    if not m:
        raise ValueError(f"Cannot find opening code block delimiter in {filepath}")
    return content[: m.end()]


def extract_footer(filepath: Path) -> str:
    """Extract the footer portion of SP-002 (from ## Deployment Notes to end of file)."""
    content = filepath.read_text(encoding="utf-8")
    marker = "## Deployment Notes"
    marker_pos = content.rfind(marker)
    if marker_pos == -1:
        raise ValueError(f"Cannot find '{marker}' in {filepath}")
    # Find the last ``` before the marker (closing of the code block)
    before_marker = content[:marker_pos]
    last_backticks = before_marker.rfind("```")
    if last_backticks == -1:
        raise ValueError("Cannot find closing ``` before Deployment Notes")
    return content[last_backticks:]


def normalize(s: str) -> str:
    """Normalize line endings and trailing whitespace for comparison."""
    return s.replace("\r\n", "\n").rstrip()


def check() -> bool:
    """Return True if SP-002 code block matches .clinerules."""
    try:
        sp002_block = extract_code_block(SP002_PATH)
        clinerules = CLINERULES_PATH.read_text(encoding="utf-8")
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    normalized_block = normalize(sp002_block)
    normalized_cliner = normalize(clinerules)

    if normalized_block == normalized_cliner:
        print(f"OK: SP-002 code block matches .clinerules ({len(normalized_block)} chars)")
        return True
    else:
        print(f"MISMATCH: SP-002 code block differs from .clinerules", file=sys.stderr)
        print(f"  SP-002 block : {len(normalized_block)} chars", file=sys.stderr)
        print(f"  .clinerules  : {len(normalized_cliner)} chars", file=sys.stderr)
        # Show first difference
        min_len = min(len(normalized_block), len(normalized_cliner))
        for i in range(min_len):
            if normalized_block[i] != normalized_cliner[i]:
                print(f"  First diff at position {i}: SP-002={repr(normalized_block[i])} clinerules={repr(normalized_cliner[i])}", file=sys.stderr)
                break
        return False


def rebuild() -> None:
    """Rebuild SP-002 from header + .clinerules + footer."""
    try:
        header = extract_header(SP002_PATH)
        footer = extract_footer(SP002_PATH)
        clinerules = CLINERULES_PATH.read_text(encoding="utf-8")
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    result = header + clinerules + footer
    SP002_PATH.write_text(result, encoding="utf-8")
    print(f"Rebuilt SP-002: header({len(header)} chars) + .clinerules({len(clinerules)} chars) + footer({len(footer)} chars) = {len(result)} total")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild or verify prompts/SP-002-clinerules-global.md")
    parser.add_argument("--check", action="store_true", help="Verify SP-002 matches .clinerules without writing")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be rebuilt without writing to disk")
    args = parser.parse_args()

    if args.check:
        success = check()
        sys.exit(0 if success else 1)
    elif args.dry_run:
        try:
            header = extract_header(SP002_PATH)
            footer = extract_footer(SP002_PATH)
            clinerules = CLINERULES_PATH.read_text(encoding="utf-8")
        except (FileNotFoundError, ValueError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(2)
        result = header + clinerules + footer
        print(f"DRY-RUN: Would rebuild SP-002 with {len(result)} total chars")
        print(f"  header: {len(header)} chars")
        print(f"  .clinerules: {len(clinerules)} chars")
        print(f"  footer: {len(footer)} chars")
        sys.exit(0)
    else:
        rebuild()
        # Verify after rebuild
        if not check():
            print("WARNING: SP-002 still differs after rebuild!", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
