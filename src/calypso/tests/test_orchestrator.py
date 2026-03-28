"""
test_orchestrator.py — Unit tests for Calypso orchestration scripts.

Tests use fixtures from tests/fixtures/ and mock the Anthropic API
to avoid real API calls during testing.
"""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src/ to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from calypso.orchestrator_phase2 import build_batch_requests, read_prd, EXPERT_AGENTS
from calypso.orchestrator_phase3 import (
    build_synthesis_prompt,
    load_expert_reports,
    validate_backlog,
)
from calypso.orchestrator_phase4 import load_draft_backlog

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestOrchestratorPhase2(unittest.TestCase):
    """Tests for orchestrator_phase2.py"""

    def test_read_prd_success(self):
        """read_prd() should return file content for existing file."""
        prd_path = str(FIXTURES_DIR / "sample_prd.md")
        content = read_prd(prd_path)
        self.assertIn("Sample PRD", content)
        self.assertIn("REQ-1", content)

    def test_read_prd_missing_file(self):
        """read_prd() should exit with error for missing file."""
        with self.assertRaises(SystemExit):
            read_prd("/nonexistent/path/prd.md")

    def test_build_batch_requests_count(self):
        """build_batch_requests() should return one request per expert agent."""
        prd_content = "# Test PRD\n\nSome content."
        requests = build_batch_requests(prd_content, "test_prd.md")
        self.assertEqual(len(requests), len(EXPERT_AGENTS))

    def test_build_batch_requests_structure(self):
        """Each batch request should have custom_id and params."""
        prd_content = "# Test PRD\n\nSome content."
        requests = build_batch_requests(prd_content, "test_prd.md")
        for req in requests:
            self.assertIn("custom_id", req)
            self.assertIn("params", req)
            self.assertIn("model", req["params"])
            self.assertIn("messages", req["params"])
            self.assertIn("system", req["params"])

    def test_build_batch_requests_expert_ids(self):
        """Batch requests should have correct expert IDs."""
        prd_content = "# Test PRD"
        requests = build_batch_requests(prd_content, "test_prd.md")
        custom_ids = {r["custom_id"] for r in requests}
        expected_ids = {"architecture_expert", "security_expert", "ux_expert", "qa_expert"}
        self.assertEqual(custom_ids, expected_ids)


class TestOrchestratorPhase3(unittest.TestCase):
    """Tests for orchestrator_phase3.py"""

    def test_load_expert_reports(self):
        """load_expert_reports() should load JSON files from fixtures dir."""
        reports = load_expert_reports(str(FIXTURES_DIR))
        # Should load sample_expert_report.json (and sample_backlog.json is not an expert report)
        self.assertGreater(len(reports), 0)

    def test_build_synthesis_prompt_contains_prd(self):
        """build_synthesis_prompt() should include PRD content."""
        prd_content = "# My PRD\n\nREQ-1: Do something."
        reports = [{"expert_id": "architecture_expert", "findings": [], "summary": "OK"}]
        prompt = build_synthesis_prompt(prd_content, "test.md", reports)
        self.assertIn("My PRD", prompt)
        self.assertIn("REQ-1", prompt)

    def test_build_synthesis_prompt_contains_expert_findings(self):
        """build_synthesis_prompt() should include expert findings."""
        prd_content = "# PRD"
        reports = [{
            "expert_id": "security_expert",
            "summary": "Security looks weak.",
            "findings": [{
                "category": "auth",
                "severity": "HIGH",
                "description": "No authentication specified.",
                "recommendation": "Add OAuth2.",
                "backlog_suggestion": "Implement OAuth2 login",
            }],
        }]
        prompt = build_synthesis_prompt(prd_content, "test.md", reports)
        self.assertIn("security_expert", prompt)
        self.assertIn("No authentication specified", prompt)

    def test_validate_backlog_valid(self):
        """validate_backlog() should return True for valid backlog."""
        backlog_path = FIXTURES_DIR / "sample_backlog.json"
        with open(backlog_path, encoding="utf-8") as f:
            backlog = json.load(f)
        result = validate_backlog(backlog, None)  # No schema validation
        self.assertTrue(result)

    def test_validate_backlog_missing_items(self):
        """validate_backlog() should return False for backlog without items."""
        result = validate_backlog({"version": "1.0"}, None)
        self.assertFalse(result)

    def test_validate_backlog_too_few_items(self):
        """validate_backlog() should warn for fewer than 5 items."""
        backlog = {
            "version": "1.0",
            "prd_ref": "test.md",
            "generated_at": "2026-01-01T00:00:00Z",
            "items": [{"id": "BL-001", "title": "Test"}],
        }
        # Should not raise, just warn
        result = validate_backlog(backlog, None)
        self.assertTrue(result)


class TestOrchestratorPhase4(unittest.TestCase):
    """Tests for orchestrator_phase4.py"""

    def test_load_draft_backlog(self):
        """load_draft_backlog() should load the sample backlog fixture."""
        backlog_path = str(FIXTURES_DIR / "sample_backlog.json")
        backlog = load_draft_backlog(backlog_path)
        self.assertIn("items", backlog)
        self.assertGreater(len(backlog["items"]), 0)

    def test_load_draft_backlog_missing(self):
        """load_draft_backlog() should exit for missing file."""
        with self.assertRaises(SystemExit):
            load_draft_backlog("/nonexistent/backlog.json")

    @patch("calypso.orchestrator_phase4.anthropic.Anthropic")
    def test_challenge_item_green(self, mock_anthropic_class):
        """challenge_item() should return GREEN classification."""
        from calypso.orchestrator_phase4 import challenge_item

        # Mock Anthropic client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "item_id": "BL-001",
            "classification": "GREEN",
            "challenge": "",
            "reasoning": "Item is well-defined.",
        }))]
        mock_client.messages.create.return_value = mock_response

        item = {
            "id": "BL-001",
            "title": "Test item",
            "description": "A well-defined item.",
            "acceptance_criteria": ["Criterion 1", "Criterion 2"],
            "priority": "HIGH",
            "phase": "PHASE-A",
            "source_experts": ["architecture_expert"],
        }

        result = challenge_item(mock_client, item, "", 1, 2)
        self.assertEqual(result["classification"], "GREEN")

    @patch("calypso.orchestrator_phase4.anthropic.Anthropic")
    def test_challenge_item_orange(self, mock_anthropic_class):
        """challenge_item() should return ORANGE classification with challenge text."""
        from calypso.orchestrator_phase4 import challenge_item

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "item_id": "BL-002",
            "classification": "ORANGE",
            "challenge": "Acceptance criteria are vague.",
            "reasoning": "Cannot verify 'works correctly'.",
        }))]
        mock_client.messages.create.return_value = mock_response

        item = {
            "id": "BL-002",
            "title": "Vague item",
            "description": "Do something.",
            "acceptance_criteria": ["Works correctly"],
            "priority": "MEDIUM",
            "phase": "PHASE-B",
            "source_experts": ["qa_expert"],
        }

        result = challenge_item(mock_client, item, "", 1, 2)
        self.assertEqual(result["classification"], "ORANGE")
        self.assertIn("vague", result["challenge"].lower())


if __name__ == "__main__":
    unittest.main()
