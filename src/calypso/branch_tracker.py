"""
BranchTracker — Active branch monitoring for le workbench

Monitors all active feature branches, tracks their status, and reports
on branch lifecycle (created, merged, deleted).

Usage:
    tracker = BranchTracker()
    tracker.scan()
    print(tracker.get_active_branches())
"""

import subprocess
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
from enum import Enum


class BranchType(Enum):
    """Branch type classification"""
    FEATURE = "feature"
    HOTFIX = "hotfix"
    DEVELOP = "develop"
    MAIN = "main"
    RELEASE = "release"
    UNKNOWN = "unknown"


class BranchStatus(Enum):
    """Branch lifecycle status"""
    ACTIVE = "active"
    MERGED = "merged"
    DELETED = "deleted"
    STALE = "stale"


@dataclass
class Branch:
    """Represents a Git branch with metadata"""
    name: str
    branch_type: BranchType
    status: BranchStatus
    created_at: Optional[datetime] = None
    last_commit_date: Optional[datetime] = None
    last_commit_hash: Optional[str] = None
    commit_message: Optional[str] = None
    idea_id: Optional[str] = None  # Extracted from branch name
    base_branch: Optional[str] = None
    is_detached: bool = False

    @classmethod
    def from_branch_name(cls, name: str) -> "Branch":
        """Parse branch name to extract metadata"""
        branch_type = cls._parse_branch_type(name)
        idea_id = cls._extract_idea_id(name)
        return cls(
            name=name,
            branch_type=branch_type,
            status=BranchStatus.ACTIVE,
            idea_id=idea_id,
        )

    @staticmethod
    def _parse_branch_type(name: str) -> BranchType:
        """Parse branch type from name"""
        if name.startswith("feature/"):
            return BranchType.FEATURE
        elif name.startswith("hotfix/"):
            return BranchType.HOTFIX
        elif name == "develop":
            return BranchType.DEVELOP
        elif name == "main" or name == "master":
            return BranchType.MAIN
        elif name.startswith("release/"):
            return BranchType.RELEASE
        else:
            return BranchType.UNKNOWN

    @staticmethod
    def _extract_idea_id(name: str) -> Optional[str]:
        """
        Extract IDEA-NNN from branch name or commit message.

        Supports multiple patterns:
        - Branch names: feature/IDEA-019-conversation-logging
        - Merge messages: Merge branch 'feature/IDEA-019-conversation-logging'
        - Squash merge prefix: IDEA-019: Implement feature...
        - Standalone: IDEA-019
        """
        # Pattern 1: Branch name with IDEA-NNN
        match = re.search(r'(?:feature/|fix/)(IDEA-\d+)', name)
        if match:
            return match.group(1)

        # Pattern 2: Merge message - Extract from branch reference
        match = re.search(r"Merge branch '[^']*?(IDEA-\d+)", name)
        if match:
            return match.group(1)

        # Pattern 3: Squash merge commit prefix
        match = re.match(r'^(IDEA-\d+):', name.strip())
        if match:
            return match.group(1)

        # Pattern 4: Generic IDEA-NNN anywhere in string
        match = re.search(r'(IDEA-\d+)', name)
        return match.group(1) if match else None

    @staticmethod
    def extract_from_commit_message(message: str) -> Optional[str]:
        """
        Extract IDEA-NNN from a commit message.

        Args:
            message: The commit message to parse

        Returns:
            IDEA-NNN if found, None otherwise.
        """
        # Try squash-merge prefix first
        match = re.match(r'^(IDEA-\d+):', message.strip())
        if match:
            return match.group(1)

        # Try to find in branch reference within merge message
        match = re.search(r"Merge branch '[^']*?(IDEA-\d+)", message)
        if match:
            return match.group(1)

        # Generic pattern
        match = re.search(r'(IDEA-\d+)', message)
        return match.group(1) if match else None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "branch_type": self.branch_type.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_commit_date": self.last_commit_date.isoformat() if self.last_commit_date else None,
            "last_commit_hash": self.last_commit_hash,
            "commit_message": self.commit_message,
            "idea_id": self.idea_id,
            "base_branch": self.base_branch,
            "is_detached": self.is_detached,
        }


@dataclass
class BranchTracker:
    """
    Tracks all active Git branches and their status.
    
    Monitors feature branches, hotfixes, and release branches.
    Extracts IDEA IDs from branch names for traceability.
    """
    repo_path: str = "."
    _branches: dict = field(default_factory=dict)
    _last_scan: Optional[datetime] = None

    def scan(self) -> dict[str, Branch]:
        """
        Scan repository for all branches and update tracker state.
        
        Returns:
            Dictionary of branch_name -> Branch objects
        """
        # Get all local branches
        result = subprocess.run(
            ["git", "branch", "-v"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Git branch scan failed: {result.stderr}")
        
        self._branches.clear()
        current_branch = self._get_current_branch()
        
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            
            # Parse: "* current  abc1234 Message" or "  feature/xyz abc1234 Message"
            is_current = line.startswith("*")
            parts = line[2:].split(None, 2)  # Skip "* " prefix
            
            if len(parts) < 2:
                continue
                
            branch_name = parts[0]
            commit_hash = parts[1]
            commit_msg = parts[2] if len(parts) > 2 else ""
            
            branch = Branch.from_branch_name(branch_name)
            branch.last_commit_hash = commit_hash
            branch.commit_message = commit_msg
            branch.last_commit_date = self._get_commit_date(commit_hash)
            branch.is_detached = current_branch == "HEAD" and is_current
            
            if is_current and current_branch != "HEAD":
                pass  # Current branch is already set from name
            
            self._branches[branch_name] = branch
        
        # Check for merged branches
        self._mark_merged_branches()
        
        # Check for deleted remote branches
        self._mark_stale_branches()
        
        self._last_scan = datetime.now(timezone.utc)
        return self._branches

    def _get_current_branch(self) -> str:
        """Get the currently checked-out branch name"""
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "HEAD"

    def _get_commit_date(self, commit_hash: str) -> Optional[datetime]:
        """Get the date of a specific commit"""
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", commit_hash],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                return datetime.fromisoformat(result.stdout.strip())
            except ValueError:
                return None
        return None

    def _mark_merged_branches(self):
        """Mark branches that have been merged into their base"""
        for branch in self._branches.values():
            if branch.status != BranchStatus.ACTIVE:
                continue
            
            base = self._get_merge_base(branch.name, branch.base_branch or "develop")
            if base:
                # Check if branch is merged (contains no new commits)
                result = subprocess.run(
                    ["git", "log", f"{branch.name}..{base}", "--oneline"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and not result.stdout.strip():
                    branch.status = BranchStatus.MERGED

    def _mark_stale_branches(self):
        """Mark branches with no recent commits (>30 days)"""
        stale_threshold = datetime.now(timezone.utc) - timedelta(days=30)
        
        for branch in self._branches.values():
            if branch.status != BranchStatus.ACTIVE:
                continue
            if branch.last_commit_date:
                # Ensure both datetimes are timezone-aware for comparison
                commit_date = branch.last_commit_date
                if commit_date.tzinfo is None:
                    commit_date = commit_date.replace(tzinfo=timezone.utc)
                if commit_date < stale_threshold:
                    branch.status = BranchStatus.STALE

    def _get_merge_base(self, branch: str, base: str) -> Optional[str]:
        """Get the merge base commit hash between two branches"""
        result = subprocess.run(
            ["git", "merge-base", branch, base],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None

    def get_active_branches(self, branch_type: Optional[BranchType] = None) -> list[Branch]:
        """
        Get all active (non-merged) branches.
        
        Args:
            branch_type: Optional filter by branch type
            
        Returns:
            List of active Branch objects
        """
        active = [b for b in self._branches.values() if b.status == BranchStatus.ACTIVE]
        if branch_type:
            active = [b for b in active if b.branch_type == branch_type]
        return active

    def get_feature_branches(self) -> list[Branch]:
        """Get all active feature branches"""
        return self.get_active_branches(BranchType.FEATURE)

    def get_hotfix_branches(self) -> list[Branch]:
        """Get all active hotfix branches"""
        return self.get_active_branches(BranchType.HOTFIX)

    def get_branch_by_idea(self, idea_id: str) -> Optional[Branch]:
        """Find branch associated with an IDEA ID"""
        for branch in self._branches.values():
            if branch.idea_id == idea_id:
                return branch
        return None

    def get_report(self) -> str:
        """
        Generate a human-readable branch status report.
        
        Returns:
            Markdown-formatted report
        """
        self.scan()
        
        active_features = self.get_feature_branches()
        active_hotfixes = self.get_hotfix_branches()
        merged = [b for b in self._branches.values() if b.status == BranchStatus.MERGED]
        stale = [b for b in self._branches.values() if b.status == BranchStatus.STALE]
        
        lines = [
            "# Branch Tracker Report",
            f"**Scanned:** {self._last_scan.isoformat() if self._last_scan else 'Never'}",
            f"**Total branches:** {len(self._branches)}",
            "",
            "## Active Feature Branches",
            f"**Count:** {len(active_features)}",
            ""
        ]
        
        if active_features:
            for branch in sorted(active_features, key=lambda b: b.last_commit_date or ""):
                age = self._format_age(branch.last_commit_date) if branch.last_commit_date else "unknown"
                lines.append(f"- `{branch.name}` ({branch.idea_id or 'no IDEA'}) — {age}")
        else:
            lines.append("_None_")
        
        lines.extend([
            "",
            "## Active Hotfix Branches",
            f"**Count:** {len(active_hotfixes)}",
            ""
        ])
        
        if active_hotfixes:
            for branch in sorted(active_hotfixes, key=lambda b: b.last_commit_date or ""):
                age = self._format_age(branch.last_commit_date) if branch.last_commit_date else "unknown"
                lines.append(f"- `{branch.name}` — {age}")
        else:
            lines.append("_None_")
        
        lines.extend([
            "",
            "## Merged Branches (Pending Deletion)",
            f"**Count:** {len(merged)}",
            ""
        ])
        
        if merged:
            for branch in merged[:10]:  # Show max 10
                lines.append(f"- `{branch.name}`")
            if len(merged) > 10:
                lines.append(f"_... and {len(merged) - 10} more_")
        else:
            lines.append("_None_")
        
        if stale:
            lines.extend([
                "",
                "## Stale Branches (>30 days inactive)",
                f"**Count:** {len(stale)}",
                ""
            ])
            for branch in stale[:10]:
                lines.append(f"- `{branch.name}`")
            if len(stale) > 10:
                lines.append(f"_... and {len(stale) - 10} more_")
        
        return "\n".join(lines)

    @staticmethod
    def _format_age(dt: Optional[datetime]) -> str:
        """Format a datetime as a human-readable age string"""
        if not dt:
            return "unknown"
        now = datetime.now(timezone.utc)
        # Ensure dt is timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age = now - dt
        if age < timedelta(hours=1):
            return f"{int(age.total_seconds() / 60)}m ago"
        elif age < timedelta(days=1):
            return f"{int(age.total_seconds() / 3600)}h ago"
        elif age < timedelta(days=30):
            return f"{age.days}d ago"
        else:
            return f"{age.days // 30}mo ago"

    def to_dict(self) -> dict:
        """Export full tracker state as dictionary"""
        return {
            "last_scan": self._last_scan.isoformat() if self._last_scan else None,
            "branches": {name: branch.to_dict() for name, branch in self._branches.items()},
            "summary": {
                "total": len(self._branches),
                "active_features": len(self.get_feature_branches()),
                "active_hotfixes": len(self.get_hotfix_branches()),
                "merged": len([b for b in self._branches.values() if b.status == BranchStatus.MERGED]),
                "stale": len([b for b in self._branches.values() if b.status == BranchStatus.STALE]),
            }
        }


def main():
    """CLI entry point"""
    import json
    
    tracker = BranchTracker()
    
    # Check for --report flag
    import sys
    if "--report" in sys.argv or "-r" in sys.argv:
        print(tracker.get_report())
    elif "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps(tracker.to_dict(), indent=2))
    else:
        # Default: scan and show summary
        tracker.scan()
        print(tracker.get_report())


if __name__ == "__main__":
    main()
