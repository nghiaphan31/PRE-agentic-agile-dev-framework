"""
sync_detector.py — Synchronization Detection Engine

Detects potential conflicts, redundancies, dependencies, and shared component
overlaps between ideas in the IDEAS-BACKLOG and TECH-SUGGESTIONS-BACKLOG.

Usage:
    from sync_detector import SyncDetector
    detector = SyncDetector()
    report = detector.detect_sync("IDEA-015")
    print(report)
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class OverlapType(Enum):
    """Sync categories as defined in RULE 12.4"""
    CONFLICT = "[CONFLICT]"
    REDUNDANCY = "[REDUNDANCY]"
    DEPENDENCY = "[DEPENDENCY]"
    SHARED_LAYER = "[SHARED_LAYER]"
    NO_OVERLAP = "[NO_OVERLAP]"


class IdeaType(Enum):
    """Track type for an idea"""
    BUSINESS = "BUSINESS"
    TECHNICAL = "TECHNICAL"


@dataclass
class Idea:
    """Represents an idea from either backlog"""
    id: str
    title: str
    status: str
    idea_type: IdeaType
    file_path: Optional[str] = None
    tags: list = field(default_factory=list)
    affected_files: list = field(default_factory=list)
    phase: Optional[str] = None
    target_release: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict, idea_type: IdeaType, file_path: str = None) -> "Idea":
        return cls(
            id=data.get("id", data.get("title", "UNKNOWN")),
            title=data.get("title", "Untitled"),
            status=data.get("status", "[IDEA]"),
            idea_type=idea_type,
            file_path=file_path,
            tags=data.get("tags", []),
            affected_files=data.get("affected_files", []),
            phase=data.get("phase"),
            target_release=data.get("target_release"),
        )


@dataclass
class SyncFinding:
    """A single sync finding between two ideas"""
    candidate_id: str
    candidate_title: str
    overlap_type: OverlapType
    detail: str
    recommendation: str
    severity: str = "MEDIUM"  # HIGH, MEDIUM, LOW


@dataclass
class SyncReport:
    """Complete sync detection report for a new idea"""
    trigger_idea: str
    trigger_title: str
    findings: list
    generated_at: str
    total_candidates: int = 0
    conflicts_found: int = 0
    
    def to_markdown(self) -> str:
        """Generate human-readable sync report"""
        lines = [
            f"## Synchronization Report — {self.trigger_idea}",
            "",
            f"**Generated:** {self.generated_at}",
            f"**Trigger:** {self.trigger_title}",
            "",
            "### Scan Results",
            "",
            "| Candidate | Overlap Type | Detail | Recommendation |",
            "|-----------|--------------|--------|----------------|",
        ]
        
        if not self.findings:
            lines.append("| — | [NO_OVERLAP] | No conflicts detected | — |")
        else:
            for f in self.findings:
                lines.append(f"| {f.candidate_id} | {f.overlap_type.value} | {f.detail} | {f.recommendation} |")
        
        lines.append("")
        if self.conflicts_found > 0:
            lines.append(f"⚠️ **{self.conflicts_found} conflict(s) require human attention.**")
        
        return "\n".join(lines)


class SyncDetector:
    """
    Synchronization detection engine.
    
    Analyzes ideas for potential overlaps including:
    - File/module conflicts (if branches exist)
    - Requirement semantic overlaps
    - Architectural layer conflicts
    - Timeline/dependency issues
    """
    
    IDEAS_BACKLOG_PATH = Path("docs/ideas/IDEAS-BACKLOG.md")
    TECH_BACKLOG_PATH = Path("docs/ideas/TECH-SUGGESTIONS-BACKLOG.md")
    IDEAS_DIR = Path("docs/ideas")
    
    # Architectural layers for SHARED_LAYER detection
    ARCH_LAYERS = {
        "data": ["database", "storage", "cache", "model", "entity", "repository"],
        "api": ["endpoint", "route", "controller", "handler", "api"],
        "auth": ["auth", "permission", "role", "user", "session", "token"],
        "ui": ["ui", "view", "component", "page", "template", "dashboard"],
        "infra": ["deploy", "config", "script", "pipeline", "ci", "infrastructure"],
    }
    
    def __init__(self, ideas_dir: str = "docs/ideas"):
        self.ideas_dir = Path(ideas_dir)
    
    def load_backlog_entries(self) -> list:
        """
        Parse the IDEAS-BACKLOG.md table and return list of idea IDs.
        """
        ideas = []
        
        # Load from IDEAS-BACKLOG
        if self.IDEAS_BACKLOG_PATH.exists():
            content = self.IDEAS_BACKLOG_PATH.read_text()
            # Extract table rows (skip header and separator)
            rows = re.findall(r'\|\s*\[?(IDEA-\d+)\]?\s*\|.*?\|.*?\|.*?\|.*?\|', content)
            for idea_id in rows:
                if idea_id.startswith("IDEA-"):
                    ideas.append(Idea(
                        id=idea_id,
                        title="",
                        status="",
                        idea_type=IdeaType.BUSINESS,
                        file_path=str(self.IDEAS_DIR / f"{idea_id.replace('[', '').replace(']', '')}.md")
                    ))
        
        # Load from TECH-SUGGESTIONS-BACKLOG
        if self.TECH_BACKLOG_PATH.exists():
            content = self.TECH_BACKLOG_PATH.read_text()
            rows = re.findall(r'\|\s*\[?(TECH-\d+)\]?\s*\|.*?\|.*?\|.*?\|', content)
            for idea_id in rows:
                if idea_id.startswith("TECH-"):
                    ideas.append(Idea(
                        id=idea_id,
                        title="",
                        status="",
                        idea_type=IdeaType.TECHNICAL,
                        file_path=str(self.IDEAS_DIR / f"{idea_id.replace('[', '').replace(']', '')}.md")
                    ))
        
        return ideas
    
    def load_idea_details(self, idea_id: str) -> Optional[dict]:
        """Load a single idea's full details from its markdown file"""
        # Try both IDEA and TECH prefixes
        for prefix in ["IDEA-", "TECH-"]:
            if idea_id.startswith(prefix):
                file_path = self.IDEAS_DIR / f"{idea_id}.md"
                if file_path.exists():
                    content = file_path.read_text()
                    return self._parse_idea_frontmatter(content)
        return None
    
    def _parse_idea_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter from idea file"""
        data = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        data[key.strip()] = value.strip()
        return data
    
    def detect_file_overlap(self, idea_a: Idea, idea_b: Idea) -> Optional[OverlapType]:
        """
        Detect if two ideas touch the same files.
        This is a basic version — full git-diff analysis comes in PHASE-C.
        """
        if not idea_a.affected_files or not idea_b.affected_files:
            return None
        
        files_a = set(idea_a.affected_files)
        files_b = set(idea_b.affected_files)
        overlap = files_a & files_b
        
        if overlap:
            return OverlapType.SHARED_LAYER
        return None
    
    def detect_semantic_overlap(self, idea_a: Idea, idea_b: Idea) -> Optional[OverlapType]:
        """
        Detect semantic overlap based on title keywords.
        This is a basic version — full NLP comes in PHASE-C.
        """
        if not idea_a.title or not idea_b.title:
            return None
        
        # Normalize titles for comparison
        title_a = idea_a.title.lower()
        title_b = idea_b.title.lower()
        
        # Extract key words (remove common words)
        stop_words = {"the", "a", "an", "for", "to", "and", "of", "in", "on", "with", "using"}
        words_a = set(re.findall(r'\b\w+\b', title_a)) - stop_words
        words_b = set(re.findall(r'\b\w+\b', title_b)) - stop_words
        
        # Check for shared meaningful words
        shared = words_a & words_b
        
        if len(shared) >= 2:
            # Multiple shared words = potential redundancy
            return OverlapType.REDUNDANCY
        elif len(shared) == 1 and shared:
            # Single shared word = potential shared layer
            return OverlapType.SHARED_LAYER
        
        return None
    
    def detect_arch_layer_overlap(self, idea_a: Idea, idea_b: Idea) -> Optional[OverlapType]:
        """
        Detect if two ideas operate on the same architectural layer.
        """
        if not idea_a.title or not idea_b.title:
            return None
        
        title_a = idea_a.title.lower()
        title_b = idea_b.title.lower()
        
        for layer_name, keywords in self.ARCH_LAYERS.items():
            matches_a = any(kw in title_a for kw in keywords)
            matches_b = any(kw in title_b for kw in keywords)
            
            if matches_a and matches_b:
                return OverlapType.SHARED_LAYER
        
        return None
    
    def detect_dependency(self, idea_a: Idea, idea_b: Idea) -> Optional[OverlapType]:
        """
        Detect if idea_b depends on idea_a completing first.
        """
        if idea_b.status == "[IMPLEMENTING]" and idea_a.status == "[ACCEPTED]":
            # Check if one mentions the other as a dependency
            detail_a = self.load_idea_details(idea_a.id) or {}
            detail_b = self.load_idea_details(idea_b.id) or {}
            
            if "depends" in str(detail_a).lower() or "depends" in str(detail_b).lower():
                return OverlapType.DEPENDENCY
        
        return None
    
    def analyze_overlap(self, idea_a: Idea, idea_b: Idea) -> OverlapType:
        """
        Run all overlap detection methods and return the most severe result.
        Severity order: CONFLICT > REDUNDANCY > DEPENDENCY > SHARED_LAYER > NO_OVERLAP
        """
        # Check file overlap first
        file_overlap = self.detect_file_overlap(idea_a, idea_b)
        if file_overlap:
            return file_overlap
        
        # Check semantic overlap
        semantic_overlap = self.detect_semantic_overlap(idea_a, idea_b)
        if semantic_overlap:
            return semantic_overlap
        
        # Check arch layer overlap
        arch_overlap = self.detect_arch_layer_overlap(idea_a, idea_b)
        if arch_overlap:
            return arch_overlap
        
        # Check dependency
        dependency = self.detect_dependency(idea_a, idea_b)
        if dependency:
            return dependency
        
        return OverlapType.NO_OVERLAP
    
    def suggest_action(self, idea_a: Idea, idea_b: Idea, overlap_type: OverlapType) -> str:
        """Generate recommendation based on overlap type"""
        actions = {
            OverlapType.CONFLICT: f"[CONFLICT] Human must arbitrate -- {idea_a.id} and {idea_b.id} require mutually exclusive changes",
            OverlapType.REDUNDANCY: f"[REDUNDANCY] Merge into single idea -- {idea_a.id} and {idea_b.id} solve the same problem",
            OverlapType.DEPENDENCY: f"[DEPENDENCY] Reorder -- {idea_b.id} depends on {idea_a.id} completing first",
            OverlapType.SHARED_LAYER: f"[SHARED_LAYER] Coordinate timing -- both touch the same component, plan branch merges carefully",
            OverlapType.NO_OVERLAP: "[NO_OVERLAP] No action needed",
        }
        return actions.get(overlap_type, "—")
    
    def detect_sync(self, new_idea_id: str) -> SyncReport:
        """
        Main entry point: detect all potential sync issues for a new idea.
        """
        # Load new idea details
        new_idea = Idea(
            id=new_idea_id,
            title="",
            status="",
            idea_type=IdeaType.BUSINESS if new_idea_id.startswith("IDEA-") else IdeaType.TECHNICAL,
            file_path=str(self.IDEAS_DIR / f"{new_idea_id}.md")
        )
        
        # Get title if file exists
        details = self.load_idea_details(new_idea_id)
        if details:
            new_idea.title = details.get("title", "")
            new_idea.status = details.get("status", "")
            new_idea.target_release = details.get("target_release")
        
        # Get all existing ideas
        all_ideas = self.load_backlog_entries()
        
        # Filter out the new idea itself
        candidates = [i for i in all_ideas if i.id != new_idea_id]
        
        findings = []
        conflicts = 0
        
        for candidate in candidates:
            # Load candidate details
            cand_details = self.load_idea_details(candidate.id)
            if cand_details:
                candidate.title = cand_details.get("title", "")
                candidate.status = cand_details.get("status", "")
            
            # Analyze overlap
            overlap_type = self.analyze_overlap(new_idea, candidate)
            
            if overlap_type != OverlapType.NO_OVERLAP:
                finding = SyncFinding(
                    candidate_id=candidate.id,
                    candidate_title=candidate.title,
                    overlap_type=overlap_type,
                    detail=f"{new_idea.id} and {candidate.id} both address similar concerns",
                    recommendation=self.suggest_action(new_idea, candidate, overlap_type),
                )
                findings.append(finding)
                
                if overlap_type == OverlapType.CONFLICT:
                    conflicts += 1
        
        return SyncReport(
            trigger_idea=new_idea_id,
            trigger_title=new_idea.title or new_idea_id,
            findings=findings,
            generated_at=datetime.now().isoformat(),
            total_candidates=len(candidates),
            conflicts_found=conflicts,
        )
    
    def full_scan(self) -> dict:
        """
        Perform a full scan of all ideas and return a summary.
        Useful for "what else is in flight?" queries.
        """
        all_ideas = self.load_backlog_entries()
        results = {}
        
        for idea in all_ideas:
            if idea.status in ["[IMPLEMENTING]", "[ACCEPTED]", "[REFINING]"]:
                report = self.detect_sync(idea.id)
                if report.findings:
                    results[idea.id] = report
        
        return results


# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sync_detector.py <IDEA-NNN>")
        print("   or: python sync_detector.py --full-scan")
        sys.exit(1)
    
    detector = SyncDetector()
    
    if sys.argv[1] == "--full-scan":
        results = detector.full_scan()
        print(f"## Full Sync Scan Results")
        print(f"**Ideas scanned:** {len(results)}")
        print("")
        for idea_id, report in results.items():
            print(report.to_markdown())
            print("")
    else:
        idea_id = sys.argv[1]
        report = detector.detect_sync(idea_id)
        print(report.to_markdown())
