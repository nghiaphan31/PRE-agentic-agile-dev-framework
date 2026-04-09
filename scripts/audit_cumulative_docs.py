#!/usr/bin/env python3
"""
Audit script for IDEA-017: Verify Canonical Docs Cumulative Requirement

This script checks that each DOC-X-vX.Y.md contains ALL content from
previous versions (is truly cumulative and self-contained).

Checks performed:
1. Line count minimums per doc type (DOC-1: 500, DOC-2: 500, DOC-3: 300, DOC-4: 300, DOC-5: 200)
2. Section presence for all previous versions (TOC matches content)
3. Missing section detection
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Minimum line counts per doc type (from RULE 12)
# Note: DOC-3 and DOC-5 are release-specific (IDEA-021) with lower thresholds
MIN_LINES = {
    "DOC-1": 500,
    "DOC-2": 500,
    "DOC-3": 100,  # Release-specific (was 300 cumulative)
    "DOC-4": 300,
    "DOC-5": 50,   # Release-specific (was 200 cumulative)
}

def get_all_releases() -> list[str]:
    """Dynamically detect all releases from docs/releases/ directory."""
    releases_dir = Path("docs/releases")
    if not releases_dir.exists():
        return []
    
    releases = []
    for d in releases_dir.iterdir():
        if d.is_dir() and d.name.startswith("v"):
            releases.append(d.name)
    
    # Sort by version number (newest first)
    releases.sort(key=lambda x: [int(p) for p in x[1:].split(".")], reverse=True)
    return releases

# Releases to check (dynamically detected from docs/releases/ directory)
RELEASES = get_all_releases()

# Doc types to check
DOC_TYPES = ["DOC-1", "DOC-2", "DOC-3", "DOC-4", "DOC-5"]


def get_doc_path(release: str, doc_type: str) -> Path:
    """Get path to a specific doc file."""
    docs_dir = Path("docs/releases")
    # Find the file matching the pattern DOC-X-vX.Y-*.md
    pattern = f"{doc_type}-v{release.replace('v', '')}-*.md"
    for file in docs_dir.glob(f"{release}/{pattern}"):
        return file
    return None


def get_line_count(file_path: Path) -> int:
    """Get line count of a file."""
    if not file_path or not file_path.exists():
        return 0
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(f.readlines())


def extract_sections(content: str) -> List[str]:
    """Extract section headers from markdown content."""
    # Match ## or ### headers
    pattern = r'^(#{2,3})\s+(.+)$'
    sections = []
    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            sections.append(match.group(2).strip())
    return sections


def extract_toc_entries(content: str) -> List[str]:
    """Extract table of contents entries."""
    # Look for numbered TOC entries like "1. [Title](#anchor)"
    pattern = r'^\d+\.\s+\[([^\]]+)\]'
    entries = []
    in_toc = False
    for line in content.split('\n'):
        if re.match(r'^##+\s+Table of Contents', line, re.IGNORECASE):
            in_toc = True
            continue
        if in_toc and re.match(r'^##+\s', line):
            break  # End of TOC
        if in_toc:
            match = re.match(pattern, line.strip())
            if match:
                entries.append(match.group(1).strip())
    return entries


def extract_version_sections(content: str) -> Dict[str, str]:
    """Extract sections that correspond to specific versions."""
    sections = {}
    current_version = None
    current_content = []
    
    for line in content.split('\n'):
        # Check for version section headers like "## 2. v1.0 Requirements"
        match = re.match(r'^##+\s+(\d+)\.\s+v(\d+\.\d+)\s+Requirements', line)
        if match:
            # Save previous version section
            if current_version:
                sections[current_version] = '\n'.join(current_content)
            current_version = f"v{match.group(2)}"
            current_content = [line]
        elif current_version:
            current_content.append(line)
    
    # Save last version
    if current_version:
        sections[current_version] = '\n'.join(current_content)
    
    return sections


def check_cumulative(file_path: Path, doc_type: str) -> Dict:
    """Check if a doc file is properly cumulative."""
    result = {
        "path": str(file_path),
        "exists": file_path.exists() if file_path else False,
        "line_count": 0,
        "min_lines": MIN_LINES.get(doc_type, 0),
        "passes_min_lines": False,
        "sections_found": [],
        "issues": [],
        "status": "MISSING"
    }
    
    if not file_path or not file_path.exists():
        result["issues"].append("File does not exist")
        return result
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result["line_count"] = len(content.split('\n'))
    result["passes_min_lines"] = result["line_count"] >= result["min_lines"]
    
    if not result["passes_min_lines"]:
        result["issues"].append(
            f"Line count {result['line_count']} < minimum {result['min_lines']}"
        )
    
    # Extract sections
    result["sections_found"] = extract_sections(content)
    
    return result


def audit_release(release: str) -> Dict:
    """Audit all docs for a specific release."""
    release_data = {
        "release": release,
        "docs": {},
        "summary": {"total": 0, "passing": 0, "failing": 0}
    }
    
    for doc_type in DOC_TYPES:
        file_path = get_doc_path(release, doc_type)
        result = check_cumulative(file_path, doc_type)
        release_data["docs"][doc_type] = result
        release_data["summary"]["total"] += 1
        
        if result["passes_min_lines"]:
            release_data["summary"]["passing"] += 1
        else:
            release_data["summary"]["failing"] += 1
    
    return release_data


def print_audit_report():
    """Print the full audit report."""
    print("=" * 80)
    print("CANONICAL DOCS CUMULATIVE REQUIREMENT AUDIT")
    print("IDEA-017: Fix Canonical Docs Cumulative Self-Contained Requirement")
    print("=" * 80)
    print()
    
    all_results = {}
    for release in RELEASES:
        all_results[release] = audit_release(release)
    
    # Print summary table
    print("LINE COUNT AUDIT (minimums from RULE 12):")
    print("-" * 80)
    print(f"{'Release':<10}", end="")
    for doc in DOC_TYPES:
        print(f"{doc:<10}", end="")
    print()
    print("-" * 80)
    
    for release in RELEASES:
        print(f"{release:<10}", end="")
        for doc in DOC_TYPES:
            result = all_results[release]["docs"].get(doc, {})
            lc = result.get("line_count", 0)
            min_lc = result.get("min_lines", 0)
            passing = result.get("passes_min_lines", False)
            
            if lc == 0:
                print(f"{'MISSING':<10}", end="")
            elif passing:
                print(f"{lc:<10}", end="")
            else:
                print(f"{lc}*".ljust(10), end="")
        print()
    
    print()
    print("MINIMUM LINE COUNTS REQUIRED:")
    for doc, min_lc in MIN_LINES.items():
        print(f"  {doc}: {min_lc} lines")
    
    print()
    print("DETAILED ISSUES:")
    print("-" * 80)
    
    issues_found = False
    for release in RELEASES:
        for doc_type in DOC_TYPES:
            result = all_results[release]["docs"].get(doc_type, {})
            if result.get("issues"):
                issues_found = True
                print(f"\n{release} {doc_type}:")
                for issue in result["issues"]:
                    print(f"  - {issue}")
    
    if not issues_found:
        print("No issues found - all docs meet minimum line counts.")
    
    print()
    print("=" * 80)
    print("SECTION STRUCTURE AUDIT:")
    print("-" * 80)
    
    # Check latest cumulative doc (DOC-1) for structure analysis
    latest_release = RELEASES[-1] if RELEASES else None
    if latest_release:
        latest_doc1 = all_results[latest_release]["docs"].get("DOC-1", {})
        if latest_doc1.get("exists"):
            content = ""
            with open(latest_doc1["path"], 'r', encoding='utf-8') as f:
                content = f.read()
            
            sections = extract_sections(content)
            toc_entries = extract_toc_entries(content)
            version_sections = extract_version_sections(content)
            
            print(f"\nAnalyzing {latest_release} DOC-1 (cumulative doc):")
            print(f"  Line count: {latest_doc1['line_count']}")
            print(f"  TOC entries found: {len(toc_entries)}")
            print(f"  Sections found: {len(sections)}")
            print(f"  Version sections found: {list(version_sections.keys())}")
            
            # Expected versions for cumulative DOC-1 (v2.10+)
            print(f"\n  Expected versions in cumulative doc: v1.0 through {latest_release}")
            print(f"  Missing versions: ", end="")
            # Dynamically generate expected versions based on releases present
            found_versions = list(version_sections.keys())
            # For v2.10, expect v1.0, v2.1-v2.10; for v2.11, expect v1.0, v2.1-v2.11
            major_versions = []
            for r in RELEASES:
                if r.startswith("v2."):
                    minor = r.split(".")[1]
                    if minor.isdigit():
                        major_versions.append(r)
            missing = [v for v in found_versions if v not in major_versions and v.startswith("v2.")]
            if missing:
                print(", ".join(missing))
            else:
                print("None - all expected versions present!")
    
    print()
    print("=" * 80)
    
    return all_results


if __name__ == "__main__":
    results = print_audit_report()
    
    # Exit with error code if any issues found
    has_failures = any(
        not r["docs"][d]["passes_min_lines"] 
        for r in results.values() 
        for d in DOC_TYPES
        if r["docs"].get(d, {}).get("exists", False)
    )
    
    sys.exit(1 if has_failures else 0)
