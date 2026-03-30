# Technical Suggestions Backlog

**Last triage:** [DATE]
**Next triage:** At [VERSION] release planning

## How to Use

- Technical suggestions are "How" proposals from humans or agents
- They are parked here, NOT injected directly into the PRD or architecture
- At architecture review time, the Architect evaluates each suggestion
- Accepted suggestions may update `systemPatterns.md` and/or DOC-2
- This file is NOT part of the 5 canonical docs — it feeds them
- Refinement sessions are logged in `docs/conversations/REFINEMENT-YYYY-MM-DD-{id}.md`

## Status Legend

| Status | Meaning |
|--------|---------|
| `[SUGGESTED]` | Captured, not yet evaluated |
| `[EVALUATING]` | Architect is analyzing feasibility |
| `[ACCEPTED]` | Approved — will update DOC-2 or systemPatterns.md |
| `[REJECTED]` | Will not implement (reason documented) |
| `[INTEGRATED]` | Incorporated into DOC-2, systemPatterns.md, or source code |

## Classification

| Type | Meaning |
|------|---------|
| `[TECH]` | Technical "How" — implementation approach, technology choice |
| `[ARCH]` | Architectural — system design, component relationships |
| `[INFRA]` | Infrastructure — deployment, tooling, environment |
| `[CODE]` | Code quality — refactoring, patterns, technical debt |

## Backlog

| ID | Title | Source | Captured | Status | Type | Disposition |
|----|-------|--------|----------|--------|------|-------------|
| — | — | — | — | — | — | — |

---

## New Technical Suggestion Template

When a new technical suggestion is captured, create a file: `docs/ideas/TECH-SUGGESTION-NNN.md`

```markdown
---
id: TECH-001
title: [Title]
status: [SUGGESTED]
source: [Who suggested]
captured: [YYYY-MM-DD]
captured_by: [Which agent received it]
type: [TECH|ARCH|INFRA|CODE]
---

## Raw Suggestion

[Exact words from human or agent]

## Classification Rationale

[Why this is a technical suggestion, not a business requirement]

## Evaluation (filled by Architect)

**Feasibility:** [HIGH|MEDIUM|LOW|PENDING]

**Impact:**
- [ ] systemPatterns.md update required: [YES/NO]
- [ ] DOC-2 update required: [YES/NO]
- [ ] Source code impact: [describe]

**Risk:** [LOW|MEDIUM|HIGH]

**Sync Overlap:** [Any existing ideas this overlaps with]

## Decision

[ACCEPTED/REJECTED/NEEDS_MORE_INFO] — [Date] — [By whom]

## Implementation Notes (if accepted)

[How to implement, what to update, where]