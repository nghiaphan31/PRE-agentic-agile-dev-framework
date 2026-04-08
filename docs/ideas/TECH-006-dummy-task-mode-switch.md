# TECH-006: Dummy Session-Start Task for Orchestrator Mode Switch

**ID:** TECH-006
**Title:** Dummy Session-Start Task for Orchestrator Mode Switch
**Source:** Human (direct suggestion)
**Captured:** 2026-04-08
**Status:** [NEEDS_MORE_INFO]
**Type:** technical
**Tier:** Minor
**Target Release:** TBD
**Disposition:** Human reports seeing automatic mode switching — need to verify

---

## Problem Statement

Human wants a workaround for the Roo Code limitation: Orchestrator cannot be set as the default mode programmatically. The human suggested: "having a dummy task at session start that, upon completion, requests a switch to Orchestrator mode."

## Proposed Solution

1. Create a lightweight "session start" dummy task
2. When the dummy task completes, it requests mode switch to Orchestrator
3. Mode switches automatically (if possible) or with human approval

## Technical Analysis

**Initial assumption:** The `switch_mode` tool **requires human approval** — an agent cannot autonomously switch modes.

**Human feedback:** "i thought i did see automatic switch between modes"

**Research needed:** 
- Verify if switch_mode has an automatic mode
- Check Roo Code documentation for auto-switch capability
- Look for any existing examples in the workbench

## Research Questions

- Is there any way to make `switch_mode` automatic (without human approval)?
- Could a VS Code task or extension hook handle this at startup?
- Is there an MCP tool or command that can be triggered programmatically?

## Status History

| Date       | Status | Notes                                      |
|------------|--------|--------------------------------------------|
| 2026-04-08 | [IDEA] | Captured from human suggestion             |
| 2026-04-08 | [NEEDS_MORE_INFO] | Human reports seeing auto switch — verify |
