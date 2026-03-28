"""
Calypso — Tier 2 Orchestration Layer for the Agentic Agile Workbench.

This package implements the asynchronous factory pipeline:
  Phase 2: Dispatch PRD to Anthropic Batch API (Committee of Experts)
  Phase 3: Synthesize expert reports into draft backlog (Synthesizer Agent)
  Phase 4: Challenge backlog items (Devil's Advocate Agent)
  Triage:  Human arbitration dashboard + apply decisions

Entry points:
  orchestrator_phase2.py  -- submit batch job
  check_batch_status.py   -- poll + retrieve results
  orchestrator_phase3.py  -- synthesize draft backlog
  orchestrator_phase4.py  -- devil's advocate classification
  triage_dashboard.py     -- generate human triage dashboard
  apply_triage.py         -- apply human decisions to memory bank
  fastmcp_server.py       -- MCP server exposing tools to Roo Code
"""

__version__ = "0.1.0"
