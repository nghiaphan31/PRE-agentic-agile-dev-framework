"""
test_triage.py — Unit tests for triage_dashboard.py and apply_triage.py.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add src/ to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from calypso.triage_dashboard import generate_dashboard, load_final_backlog
from calypso.apply_triage import parse_checkbox_decisions, format_item_for_systempatterns, format_item_for_productcontext

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Sample data helpers
# ---------------------------------------------------------------------------

def make_final_backlog(green_count: int = 2, orange_count: int = 2) -> dict:
    """Create a sample final backlog for testing."""
    items = []
    for i in range(1, green_count + 1):
        items.append({
            "id": f"BL-{i:03d}",
            "title": f"Green item {i}",
            "description": f"Description for green item {i}.",
            "acceptance_criteria": [f"Criterion {i}.1", f"Criterion {i}.2"],
            "source_experts": ["architecture_expert"],
            "priority": "HIGH",
            "phase": "PHASE-A",
            "classification": "GREEN",
            "challenge": "",
            "human_decision": None,
        })
    for i in range(green_count + 1, green_count + orange_count + 1):
        items.append({
            "id": f"BL-{i:03d}",
            "title": f"Orange item {i}",
            "description": f"Description for orange item {i}.",
            "acceptance_criteria": [f"Criterion {i}.1"],
            "source_experts": ["qa_expert"],
            "priority": "MEDIUM",
            "phase": "PHASE-B",
            "classification": "ORANGE",
            "challenge": f"This item has vague acceptance criteria.",
            "human_decision": None,
        })
    return {
        "version": "1.0",
        "prd_ref": "test_prd.md",
        "generated_at": "2026-03-28T12:00:00Z",
        "summary": {"total": len(items), "green": green_count, "orange": orange_count},
        "items": items,
    }


# ---------------------------------------------------------------------------
# Tests: triage_dashboard.py
# ---------------------------------------------------------------------------

class TestTriageDashboard(unittest.TestCase):
    """Tests for triage_dashboard.py"""

    def test_generate_dashboard_contains_header(self):
        """Dashboard should contain the header."""
        backlog = make_final_backlog(2, 1)
        dashboard = generate_dashboard(backlog)
        self.assertIn("Calypso Triage Dashboard", dashboard)

    def test_generate_dashboard_green_items(self):
        """Dashboard should list GREEN items in a table."""
        backlog = make_final_backlog(3, 0)
        dashboard = generate_dashboard(backlog)
        self.assertIn("GREEN Items", dashboard)
        self.assertIn("BL-001", dashboard)
        self.assertIn("BL-002", dashboard)

    def test_generate_dashboard_orange_items_with_checkboxes(self):
        """Dashboard should show ORANGE items with ACCEPT/REJECT checkboxes."""
        backlog = make_final_backlog(1, 2)
        dashboard = generate_dashboard(backlog)
        self.assertIn("ORANGE Items", dashboard)
        self.assertIn("- [ ] ACCEPT", dashboard)
        self.assertIn("- [ ] REJECT", dashboard)

    def test_generate_dashboard_no_orange(self):
        """Dashboard with no ORANGE items should not show ORANGE section."""
        backlog = make_final_backlog(3, 0)
        dashboard = generate_dashboard(backlog)
        self.assertNotIn("ORANGE Items", dashboard)

    def test_generate_dashboard_summary_counts(self):
        """Dashboard summary should show correct counts."""
        backlog = make_final_backlog(3, 2)
        dashboard = generate_dashboard(backlog)
        self.assertIn("3", dashboard)  # GREEN count
        self.assertIn("2", dashboard)  # ORANGE count

    def test_generate_dashboard_challenge_text(self):
        """Dashboard should include Devil's Advocate challenge text for ORANGE items."""
        backlog = make_final_backlog(0, 1)
        dashboard = generate_dashboard(backlog)
        self.assertIn("vague acceptance criteria", dashboard)


# ---------------------------------------------------------------------------
# Tests: apply_triage.py
# ---------------------------------------------------------------------------

class TestApplyTriage(unittest.TestCase):
    """Tests for apply_triage.py"""

    def test_parse_checkbox_accept(self):
        """parse_checkbox_decisions() should detect ACCEPT checkbox."""
        dashboard_text = """
### BL-003: Orange item 3

Some description.

**Your Decision:**
- [x] ACCEPT — Include this item in the backlog
- [ ] REJECT — Discard this item
"""
        decisions = parse_checkbox_decisions(dashboard_text)
        self.assertEqual(decisions.get("BL-003"), "ACCEPT")

    def test_parse_checkbox_reject(self):
        """parse_checkbox_decisions() should detect REJECT checkbox."""
        dashboard_text = """
### BL-004: Orange item 4

Some description.

**Your Decision:**
- [ ] ACCEPT — Include this item in the backlog
- [x] REJECT — Discard this item
"""
        decisions = parse_checkbox_decisions(dashboard_text)
        self.assertEqual(decisions.get("BL-004"), "REJECT")

    def test_parse_checkbox_multiple_items(self):
        """parse_checkbox_decisions() should handle multiple items."""
        dashboard_text = """
### BL-003: Item 3

**Your Decision:**
- [x] ACCEPT — Include this item in the backlog
- [ ] REJECT — Discard this item

---

### BL-004: Item 4

**Your Decision:**
- [ ] ACCEPT — Include this item in the backlog
- [x] REJECT — Discard this item
"""
        decisions = parse_checkbox_decisions(dashboard_text)
        self.assertEqual(decisions.get("BL-003"), "ACCEPT")
        self.assertEqual(decisions.get("BL-004"), "REJECT")

    def test_parse_checkbox_no_decision(self):
        """parse_checkbox_decisions() should skip items with no checkbox checked."""
        dashboard_text = """
### BL-005: Item 5

**Your Decision:**
- [ ] ACCEPT — Include this item in the backlog
- [ ] REJECT — Discard this item
"""
        decisions = parse_checkbox_decisions(dashboard_text)
        self.assertNotIn("BL-005", decisions)

    def test_format_item_for_systempatterns(self):
        """format_item_for_systempatterns() should produce valid markdown."""
        item = {
            "id": "BL-001",
            "title": "Test item",
            "description": "A test description.",
            "acceptance_criteria": ["Criterion 1", "Criterion 2"],
            "priority": "HIGH",
            "phase": "PHASE-A",
            "source_experts": ["architecture_expert"],
        }
        result = format_item_for_systempatterns(item)
        self.assertIn("BL-001", result)
        self.assertIn("Test item", result)
        self.assertIn("Criterion 1", result)
        self.assertIn("Criterion 2", result)

    def test_format_item_for_productcontext(self):
        """format_item_for_productcontext() should produce valid markdown with checkboxes."""
        item = {
            "id": "BL-002",
            "title": "Another item",
            "description": "Another description.",
            "acceptance_criteria": ["AC 1"],
            "priority": "MEDIUM",
            "phase": "PHASE-B",
            "source_experts": ["qa_expert"],
        }
        result = format_item_for_productcontext(item)
        self.assertIn("BL-002", result)
        self.assertIn("- [ ] AC 1", result)

    def test_apply_decisions_dry_run(self):
        """apply_decisions() in dry-run mode should not write any files."""
        from calypso.apply_triage import apply_decisions

        backlog = make_final_backlog(1, 1)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Write final backlog
            backlog_path = tmpdir / "final_backlog.json"
            backlog_path.write_text(json.dumps(backlog), encoding="utf-8")

            # Write dashboard with ACCEPT decision for BL-002
            dashboard_text = """
### BL-002: Orange item 2

**Your Decision:**
- [x] ACCEPT — Include this item in the backlog
- [ ] REJECT — Discard this item
"""
            dashboard_path = tmpdir / "triage_dashboard.md"
            dashboard_path.write_text(dashboard_text, encoding="utf-8")

            sp_path = tmpdir / "systemPatterns.md"
            pc_path = tmpdir / "productContext.md"

            # Dry run — should not create sp_path or pc_path
            apply_decisions(
                dashboard_path=str(dashboard_path),
                backlog_path=str(backlog_path),
                systempatterns_path=str(sp_path),
                productcontext_path=str(pc_path),
                dry_run=True,
            )

            # Files should NOT be created in dry run
            self.assertFalse(sp_path.exists())
            self.assertFalse(pc_path.exists())


if __name__ == "__main__":
    unittest.main()
