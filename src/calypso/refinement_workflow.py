"""
refinement_workflow.py — Refinement Session Management

Manages the refinement workflow for ideas:
- Determines whether refinement should be sync or async based on complexity
- Creates refinement session logs
- Updates idea status through the state machine

Usage:
    from refinement_workflow import RefinementWorkflow
    workflow = RefinementWorkflow()
    result = workflow.determine_mode(idea_id)
    if result.mode == "synchronous":
        workflow.start_sync_session(idea_id, conversation)
    else:
        workflow.create_async_refinement_doc(idea_id)
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class RefinementMode(Enum):
    """Refinement approach based on complexity score"""
    ASYNC = "asynchronous"  # Document exchange
    HYBRID = "hybrid"        # Quick sync, then async
    SYNC = "synchronous"     # Live conversation


class IdeaState(Enum):
    """Idea lifecycle states"""
    RAW = "RAW"
    INTAKE_PROCESSING = "INTAKE_PROCESSING"
    REFINING = "REFINING"
    EVALUATING = "EVALUATING"
    REFINED = "REFINED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    IMPLEMENTING = "IMPLEMENTING"
    READY_FOR_QA = "READY_FOR_QA"
    RELEASED = "RELEASED"


@dataclass
class ComplexityScore:
    """Complexity scoring for refinement mode determination"""
    score: int  # 1-10
    factors: list
    recommendation: RefinementMode
    
    @classmethod
    def calculate(cls, idea_data: dict) -> "ComplexityScore":
        """
        Calculate complexity score based on idea attributes.
        Returns a score 1-10 and recommended refinement mode.
        """
        score = 0
        factors = []
        
        title = idea_data.get("title", "").lower()
        description = idea_data.get("description", "")
        
        # Title-based heuristics
        complexity_indicators = [
            ("architecture", 2),
            ("system", 1),
            ("refactor", 2),
            ("integration", 2),
            ("api", 1),
            ("database", 1),
            ("security", 2),
            ("performance", 2),
            ("scale", 2),
            ("multi", 1),
            ("cross", 1),
        ]
        
        for indicator, weight in complexity_indicators:
            if indicator in title:
                score += weight
                factors.append(f"Title contains '{indicator}' (+{weight})")
        
        # Description length
        desc_len = len(description)
        if desc_len > 500:
            score += 2
            factors.append(f"Long description ({desc_len} chars) (+2)")
        elif desc_len > 200:
            score += 1
            factors.append(f"Medium description ({desc_len} chars) (+1)")
        
        # Check for cross-cutting concerns
        cross_cutting = ["auth", "logging", "error handling", "caching", "transactions"]
        for concern in cross_cutting:
            if concern in title or concern in description.lower():
                score += 1
                factors.append(f"Cross-cutting concern: {concern} (+1)")
        
        # Cap at 10
        score = min(score, 10)
        
        # Determine mode based on score
        if score <= 3:
            mode = RefinementMode.ASYNC
        elif score <= 6:
            mode = RefinementMode.HYBRID
        else:
            mode = RefinementMode.SYNC
        
        return cls(score=score, factors=factors, recommendation=mode)


@dataclass
class RefinementSession:
    """Represents a refinement session"""
    idea_id: str
    mode: RefinementMode
    started_at: str
    status: str = "in_progress"
    participants: list = None
    discussion_log: list = None
    parked_technical: list = None
    final_requirements: list = None
    
    def __post_init__(self):
        if self.participants is None:
            self.participants = []
        if self.discussion_log is None:
            self.discussion_log = []
        if self.parked_technical is None:
            self.parked_technical = []
        if self.final_requirements is None:
            self.final_requirements = []
    
    def add_discussion_turn(self, speaker: str, content: str, is_technical: bool = False):
        """Add a discussion turn to the log"""
        self.discussion_log.append({
            "speaker": speaker,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "is_technical": is_technical,
        })
        
        if is_technical:
            self.park_technical(content)
    
    def park_technical(self, content: str):
        """Extract and park a technical suggestion"""
        self.parked_technical.append({
            "text": content,
            "timestamp": datetime.now().isoformat(),
        })
    
    def add_requirement(self, requirement: str):
        """Add a refined requirement"""
        self.final_requirements.append({
            "text": requirement,
            "timestamp": datetime.now().isoformat(),
        })
    
    def to_markdown(self) -> str:
        """Generate refinement session log in markdown format"""
        lines = [
            f"## Refinement Log — {self.idea_id}",
            "",
            f"**Date:** {self.started_at}",
            f"**Mode:** {self.mode.value.capitalize()}",
            f"**Status:** {self.status}",
            "",
            "### Participants",
        ]
        
        if self.participants:
            for p in self.participants:
                lines.append(f"- {p}")
        else:
            lines.append("- (not recorded)")
        
        lines.extend(["", "### Discussion Summary", "", "| Turn | Speaker | Content | Technical? |", "|:-----|---------|---------|:---------:|"])
        
        for i, turn in enumerate(self.discussion_log, 1):
            content_preview = turn["content"][:60] + "..." if len(turn["content"]) > 60 else turn["content"]
            content_preview = content_preview.replace("|", "\\|").replace("\n", " ")
            tech_marker = "✅" if turn.get("is_technical") else "—"
            lines.append(f"| {i} | {turn['speaker']} | {content_preview} | {tech_marker} |")
        
        if self.parked_technical:
            lines.extend(["", "### Parked Technical Suggestions", ""])
            for i, tech in enumerate(self.parked_technical, 1):
                lines.append(f"{i}. {tech['text']}")
        
        if self.final_requirements:
            lines.extend(["", "### Final Requirements", ""])
            for i, req in enumerate(self.final_requirements, 1):
                lines.append(f"{i}. {req['text']}")
        
        lines.extend(["", "---", ""])
        
        return "\n".join(lines)


class RefinementWorkflow:
    """
    Manages the refinement workflow for ideas.
    
    Per the governance model:
    - Orchestrator determines refinement mode based on complexity score
    - Hybrid mode: quick sync, then async document refinement
    - All refinement sessions logged to docs/conversations/REFINEMENT-YYYY-MM-DD-{id}.md
    """
    
    IDEAS_DIR = Path("docs/ideas")
    CONVERSATIONS_DIR = Path("docs/conversations")
    
    def __init__(self, ideas_dir: str = "docs/ideas", conversations_dir: str = "docs/conversations"):
        self.ideas_dir = Path(ideas_dir)
        self.conversations_dir = Path(conversations_dir)
    
    def load_idea(self, idea_id: str) -> Optional[dict]:
        """Load idea details from its markdown file"""
        file_path = self.ideas_dir / f"{idea_id}.md"
        if not file_path.exists():
            return None
        
        content = file_path.read_text()
        return self._parse_frontmatter(content)
    
    def _parse_frontmatter(self, content: str) -> dict:
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
                # Also capture description (first non-frontmatter section)
                rest = parts[2].strip()
                if "## Description" in rest:
                    desc_start = rest.find("## Description") + len("## Description")
                    data["description"] = rest[desc_start:].strip().split("\n## ")[0].strip()
        return data
    
    def determine_mode(self, idea_id: str) -> ComplexityScore:
        """
        Determine the appropriate refinement mode for an idea.
        Called by Orchestrator to decide: sync, async, or hybrid.
        """
        idea_data = self.load_idea(idea_id)
        if not idea_data:
            return ComplexityScore(
                score=5,  # Default medium complexity
                factors=["Could not load idea file, assuming default"],
                recommendation=RefinementMode.HYBRID
            )
        
        return ComplexityScore.calculate(idea_data)
    
    def start_sync_session(self, idea_id: str, participants: list = None) -> RefinementSession:
        """
        Start a synchronous (live conversation) refinement session.
        Returns a session object that will accumulate discussion turns.
        """
        session = RefinementSession(
            idea_id=idea_id,
            mode=RefinementMode.SYNC,
            started_at=datetime.now().isoformat(),
            participants=participants or ["Human", "Orchestrator"],
        )
        return session
    
    def create_async_refinement_doc(self, idea_id: str) -> Path:
        """
        Create an async refinement document for the idea.
        Returns the path to the created file.
        """
        self.CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"REFINEMENT-{date_str}-{idea_id}.md"
        filepath = self.CONVERSATIONS_DIR / filename
        
        template = f"""# Refinement Session — {idea_id}

**Date:** {datetime.now().isoformat()}
**Mode:** Asynchronous
**Status:** Awaiting human response

## Idea Summary

[Copy the idea title and description from {idea_id}.md here]

## Questions for Clarification

[Questions from the Orchestrator/PO that need answers]

1. 

## Human Responses

[Space for human to provide answers and details]

## Requirements Captured

[Orchestrator fills this in as responses come in]

## Technical Suggestions Parked

[Any "How" suggestions from the human are parked here for TECH-SUGGESTIONS-BACKLOG]

---

*This document follows the asynchronous refinement workflow. 
Human responds at their convenience. Orchestrator updates requirements as responses arrive.*
"""
        
        filepath.write_text(template)
        return filepath
    
    def complete_session(self, session: RefinementSession, status: str = "completed") -> Path:
        """
        Complete a refinement session and save the log.
        Returns the path to the saved log file.
        """
        session.status = status
        self.CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"REFINEMENT-{date_str}-{session.idea_id}.md"
        filepath = self.CONVERSATIONS_DIR / filename
        
        filepath.write_text(session.to_markdown())
        return filepath
    
    def update_idea_status(self, idea_id: str, new_status: IdeaState):
        """
        Update the status of an idea in its markdown file.
        """
        file_path = self.ideas_dir / f"{idea_id}.md"
        if not file_path.exists():
            return False
        
        content = file_path.read_text()
        
        # Update status in frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # Replace status line
                new_frontmatter = re.sub(
                    r'^status:.*$',
                    f'status: {new_status.value}',
                    frontmatter,
                    flags=re.MULTILINE
                )
                
                new_content = f"---\n{new_frontmatter}\n---\n{body}"
                file_path.write_text(new_content)
        
        return True


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python refinement_workflow.py <idea_id>")
        print("       python refinement_workflow.py <idea_id> --async")
        print("       python refinement_workflow.py <idea_id> --mode-only")
        sys.exit(1)
    
    idea_id = sys.argv[1]
    workflow = RefinementWorkflow()
    
    if "--mode-only" in sys.argv:
        # Just determine and print the refinement mode
        result = workflow.determine_mode(idea_id)
        print(f"## Complexity Analysis for {idea_id}")
        print(f"**Score:** {result.score}/10")
        print(f"**Recommendation:** {result.recommendation.value}")
        if result.factors:
            print("**Factors:**")
            for f in result.factors:
                print(f"  - {f}")
    
    elif "--async" in sys.argv:
        # Create async refinement doc
        path = workflow.create_async_refinement_doc(idea_id)
        print(f"Created async refinement document: {path}")
    
    else:
        # Start a sync session and show the template
        session = workflow.start_sync_session(idea_id)
        print(session.to_markdown())
