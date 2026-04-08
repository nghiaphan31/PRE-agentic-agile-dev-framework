# IDEA-027: Orchestrator as Default Entry Point

**ID:** IDEA-027
**Title:** Orchestrator as Default Entry Point
**Source:** Human (direct remark, observed gap)
**Captured:** 2026-04-08
**Status:** [ACCEPTED]
**Type:** governance
**Tier:** Major
**Target Release:** v2.14
**Disposition:** Implementation: Document manual procedure + update RULE 16

---

## Problem Statement

When starting a new task, Roo Code does not default to Orchestrator mode. The user must manually select it. IDEA-020's step #1 (Make Orchestrator the Default Entry Point) was never completed.

---

## Proposed Solution

**FEASIBILITY ASSESSMENT: ❌ No programmatic solution exists**

After investigating the codebase and Roo Code's architecture:

1. **Roo Code is a VS Code extension** — it does not have a `defaultMode` configuration option
2. **`.vscode/settings.json`** cannot control which mode an extension defaults to
3. **`.roomodes`** only defines custom personas (product-owner, scrum-master, developer, qa-engineer) — Orchestrator is BUILT-IN to Roo Code, not in .roomodes
4. **VS Code has no extension-level default mode setting**

### Implementation Approach

Since no programmatic solution exists, the implementation will be **documentation-only**:

1. **Document the manual procedure** in DOC-4 (Operations Guide):
   - How to set Orchestrator as the default mode in Roo Code
   - Screenshot guidance (if available)

2. **Update RULE 16** to acknowledge this is a **Roo Code limitation**:
   - The Orchestrator is the authoritative default by convention/policy
   - Human must manually invoke Orchestrator at session start
   - This is a known limitation documented in the system

3. **Add to template** for new project setup documentation

### Evidence
- `.vscode/settings.json` contains only git-graph and task configurations — no Roo Code mode settings
- No `defaultMode` or equivalent setting found in any documentation
- Roo Code mode selection is purely a runtime UI action

---

## Affected Documents

| Document | Action |
|----------|--------|
| [`docs/ideas/IDEA-020-orchestrator-authoritative-default.md`](docs/ideas/IDEA-020-orchestrator-authoritative-default.md) | Update status to [PARTIAL] |
| [`docs/ideas/IDEAS-BACKLOG.md`](docs/ideas/IDEAS-BACKLOG.md) | Add IDEA-027 |

---

## Status History

| Date       | Status    | Notes                                      |
|------------|-----------|--------------------------------------------|
| 2026-04-08 | [IDEA]    | Captured from observed gap in IDEA-020 implementation |
| 2026-04-08 | [ACCEPTED] | Investigated: No programmatic default mode exists in Roo Code. Implementation: documentation + RULE 16 update |