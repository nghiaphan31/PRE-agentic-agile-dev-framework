# Document 5: Application Agile Process Manual
## How to develop an application project with the Agentic Agile Workbench

**Project Name:** Agentic Agile Workbench
**Version:** 2.0
**Date:** 2026-03-23
**References:** DOC1-PRD v2.0, DOC2-Architecture v2.0, DOC3-Plan v3.0, DOC4-Guide-Deploiement v1.0

---

## Preamble: Why This Document?

Documents DOC1 to DOC4 describe **the workbench itself**: its requirements, its architecture, its installation, its deployment. They do not describe **how to work with the workbench** to produce application or business software.

This document answers the question: **"I have the workbench operational. How do I develop my project?"**

It covers:
1. The **Agile process** adapted to agentic development
2. The **nomenclature and templates** of all artifacts in an application project
3. The **anti-risk mechanisms** specific to agentic development (memory loss, hallucination, multi-sessions over several months)
4. The **open upstream phase**: how to transform unstructured narrative ideas into structured artifacts
5. The **traceability and versioning** of the entire process

### Convention: Ready-to-Copy-Paste Prompts

This document uses a visual convention to distinguish explanations from operational actions.

`PROMPT` blocks are **prompts ready to copy-paste into Roo Code**. Each block is **self-contained**: you can copy-paste it without having read the rest of the document, and the agent will execute the complete step autonomously.

**Format of a PROMPT block:**

> **PROMPT [X.Y] — [Title]**
> **Required Roo Code mode:** `[mode-slug]`
> **Complexity:** [Simple (1 send, autonomous agent) | Iterative (human/agent dialogue) | Sequential (several prompts to chain)]
> **Copy-paste the block below as-is:**

```markdown
[Prompt text — self-contained, ready to paste into Roo Code]
```

*-> Artifact produced: `path/file.md`*

### Distinction: User Prompts (this document) vs System Prompts (`template/prompts/`)

This document contains **User Prompts** — operational instructions that **the human sends to the agent** to trigger a precise step of the Agile workflow (Sprint Planning, User Story development, etc.).

They are distinct from the **System Prompts** stored in `template/prompts/` (files SP-001 to SP-007), which configure the identity and behavioral rules of the AI agents. The latter are deployed in technical files (`.clinerules`, `.roomodes`, `Modelfile`) and apply permanently, in the background, for all sessions.

| | User Prompts (this document) | System Prompts (`template/prompts/`) |
| :--- | :--- | :--- |
| **Role** | Trigger a workflow action | Configure the agent's identity and rules |
| **Used by** | The human (copy-paste into Roo Code) | The AI agent (automatically, in the background) |
| **Scope** | One precise task, one session | All sessions, all modes |
| **Target** | Roo Code chat interface | `.clinerules`, `.roomodes`, `Modelfile`, Gemini Gem |
| **Frequency** | At each workflow step | Once deployed, then maintenance |

---

## Table of Contents

1. Process Overview
2. Phase 0 - Open Upstream: From Idea to Artifacts
3. Phase 1 - Framing: Project Initialization
4. Phase 2 - Development Sprints
5. Phase 3 - Delivery and Maintenance
6. Artifact Nomenclature
7. Artifact Templates
8. Agentic Anti-Risk Mechanisms
9. Session Protocols
10. Project Dashboard

---

## 1. Process Overview

### 1.1 Fundamental Principles

The process rests on **four non-negotiable principles**:

| Principle | Description | Workbench Mechanism |
| :--- | :--- | :--- |
| **Persistent Memory** | All context is written, never assumed to be memorized | Memory Bank (7 `.md` files) |
| **Total Traceability** | Every artifact is versioned with its history | Git + Conventional Commits |
| **Progressive Convergence** | Narrative inputs mature toward structured artifacts | Phase 0 -> Phase 1 -> Phase 2 |
| **Defense in Depth** | Each rule is redundant (`.clinerules` + `roleDefinition` + protocols) | `.clinerules` + `.roomodes` |

### 1.2 Process Map

```
+-------------------------------------------------------------------------+
|                    PHASE 0 - OPEN UPSTREAM                              |
|                                                                          |
|  Narrative, unstructured, disorganized inputs                           |
|  (emails, notes, conversations, existing code, vague ideas)             |
|                                                                          |
|  -> Artifact: BRIEF-001 (Raw Narrative Vision)                          |
|  -> Artifact: BRIEF-002 (Structured Synthesis)                          |
|  -> Artifact: BRIEF-003 (Launch Decision)                               |
+----------------------------------+--------------------------------------+
                                   | Convergence
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 1 - FRAMING                                     |
|                                                                          |
|  Project initialization, Memory Bank, initial backlog                   |
|                                                                          |
|  -> Artifact: PRJ-001 (Project Brief)                                   |
|  -> Artifact: PRJ-002 (Initial Architecture)                            |
|  -> Artifact: PRJ-003 (Initial Backlog)                                 |
|  -> Artifact: PRJ-004 (Tech Context)                                    |
+----------------------------------+--------------------------------------+
                                   | Iteration
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 2 - SPRINTS (repeated N times)                 |
|                                                                          |
|  Sprint Planning -> Development -> Tests -> Review -> Retrospective     |
|                                                                          |
|  -> Artifact: SPR-XXX-001 (Sprint Backlog)                              |
|  -> Artifact: SPR-XXX-002 (User Stories)                                |
|  -> Artifact: SPR-XXX-003 (Source Code)                                 |
|  -> Artifact: SPR-XXX-004 (Test Report)                                 |
|  -> Artifact: SPR-XXX-005 (Sprint Review)                               |
|  -> Artifact: SPR-XXX-006 (Retrospective)                               |
+----------------------------------+--------------------------------------+
                                   | Delivery
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 3 - DELIVERY & MAINTENANCE                     |
|                                                                          |
|  -> Artifact: REL-XXX-001 (Release Notes)                               |
|  -> Artifact: REL-XXX-002 (User Documentation)                          |
|  -> Artifact: REL-XXX-003 (Deployment Runbook)                          |
+-------------------------------------------------------------------------+
```

### 1.3 Roles and Responsibilities by Phase

| Phase | Primary Persona | Secondary Personas | Deliverables |
| :--- | :--- | :--- | :--- |
| Phase 0 - Upstream | Product Owner | Developer | BRIEF-001, BRIEF-002, BRIEF-003 |
| Phase 1 - Framing | Product Owner | Developer, Scrum Master | PRJ-001 to PRJ-004 |
| Phase 2 - Sprint Planning | Product Owner | Scrum Master | SPR-XXX-001, SPR-XXX-002 |
| Phase 2 - Development | Developer | — | SPR-XXX-003 |
| Phase 2 - Tests | QA Engineer | Developer | SPR-XXX-004 |
| Phase 2 - Review | Product Owner | Scrum Master | SPR-XXX-005 |
| Phase 2 - Retrospective | Scrum Master | All | SPR-XXX-006 |
| Phase 3 - Delivery | Developer | QA Engineer | REL-XXX-001 to REL-XXX-003 |

---

## 2. Phase 0 - Open Upstream: From Idea to Artifacts

### 2.1 Why an Open Upstream Phase?

Software development rarely starts with a structured specification. It starts with:
- A 3-line email: "We need a tool to manage our customer orders"
- A conversation: "The problem is that sales reps enter data twice"
- Existing code without documentation: "Here's what we have, it needs to be redone properly"
- Disorganized notes across multiple documents
- A vague idea that evolves through discussions

**The workbench must accept these inputs as-is** and progressively transform them into structured artifacts. That is the role of Phase 0.

> **Golden rule of Phase 0:** Never force a premature structure. Let understanding mature before structuring.

### 2.2 Inputs Accepted in Phase 0

| Input Type | Example | Processing |
| :--- | :--- | :--- |
| **Free narrative text** | Email, note, meeting minutes | Copy as-is into BRIEF-001 |
| **Existing code** | Legacy repository, scripts, prototypes | Developer audit -> BRIEF-002 |
| **Oral conversation** | Transcription, meeting notes | Copy as-is into BRIEF-001 |
| **Word/PDF document** | Partial specification, functional spec | Extract text -> BRIEF-001 |
| **Mockups/Wireframes** | Images, screenshots | Describe in text -> BRIEF-001 |
| **Vague idea** | "I want something like Trello but for..." | Product Owner dialogue -> BRIEF-001 |

### 2.3 Phase 0 Maturation Process

---

#### Step 0.1 — Collect raw inputs

> **PROMPT 0.1 — Collect raw inputs**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Simple — 1 send, replace [RAW INPUTS] with your data before sending
> **Copy-paste the block below as-is, then replace [RAW INPUTS]:**

```markdown
Create the file docs/brief/BRIEF-001-vision-narrative.md with the following content,
copied exactly as-is without reformulating:

---
# BRIEF-001 - Raw Narrative Vision
**Creation date:** [DATE]
**Created by:** Product Owner
**Status:** Draft

## Raw Inputs

### Input 1 - [Source: email / meeting / note / existing code]
**Date:** [DATE]
**Author:** [NAME]

[RAW INPUTS -- paste here emails, notes, conversations, descriptions as-is]

## Addition History
| Date | Source | Summary |
| :--- | :--- | :--- |
| [DATE] | [SOURCE] | [SUMMARY IN 1 LINE] |
---

Commit with: 'docs(brief): initial narrative vision - upstream phase'
```

*-> Artifact produced: `docs/brief/BRIEF-001-vision-narrative.md`*

---

#### Step 0.2 — Structured analysis

> **PROMPT 0.2 — Structured analysis of raw inputs**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple — 1 send, the agent produces BRIEF-002 autonomously
> **Copy-paste the block below as-is:**

```markdown
Read docs/brief/BRIEF-001-vision-narrative.md.
Identify and list in docs/brief/BRIEF-002-synthese-structuree.md:
- The mentioned features (even implicitly)
- The identifiable target users
- The technical or business constraints
- The ambiguities and open questions
- What is apparently out of scope
Do not make any decisions. Only document what you understand.
Commit with: 'docs(brief): structured synthesis upstream phase'
```

*-> Artifact produced: `docs/brief/BRIEF-002-synthese-structuree.md`*

---

#### Step 0.3 — Clarification of ambiguities

> **PROMPT 0.3 — Clarification of ambiguities**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Iterative — question/answer dialogue until all critical ambiguities are resolved
> **Copy-paste the block below as-is:**

```markdown
Read docs/brief/BRIEF-002-synthese-structuree.md.
For each ambiguity listed in the "Ambiguities and Open Questions" section,
ask me one precise question.
Wait for my answer before moving to the next one.
Update BRIEF-002 with each answer obtained, marking the question as "Resolved".
```

*-> Iterative dialogue until critical ambiguities are resolved. BRIEF-002 updated.*

---

#### Step 0.4 — GO/NO-GO launch decision

> **PROMPT 0.4 — GO/NO-GO launch decision**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Simple — 1 send, the agent creates BRIEF-003 and commits the 3 artifacts
> **Copy-paste the block below as-is:**

```markdown
Based on docs/brief/BRIEF-001-vision-narrative.md and
docs/brief/BRIEF-002-synthese-structuree.md,
create docs/brief/BRIEF-003-decision-lancement.md with:
- The GO / NO-GO / HOLD decision
- The launch conditions if HOLD
- The decision date
- The identified risks and their mitigation
- The validated scope for launch

Commit the 3 BRIEF files with the message:
'docs(brief): upstream phase complete - decision [GO/NO-GO]'
```

*-> Artifact produced: `docs/brief/BRIEF-003-decision-lancement.md`*
*-> Git commit of the 3 BRIEF artifacts*

---

### 2.4 Phase 0 Exit Criteria

Phase 0 is complete when:
- [ ] BRIEF-001 exists and contains all raw inputs
- [ ] BRIEF-002 exists and lists features, users, constraints, ambiguities
- [ ] All critical ambiguities are resolved (or documented as accepted)
- [ ] BRIEF-003 contains a GO decision
- [ ] The 3 files are committed in Git

> **If the decision is NO-GO or HOLD:** Archive the BRIEF files in `docs/brief/archive/` and commit. The project can resume later starting from these artifacts.

---

## 3. Phase 1 - Framing: Project Initialization

### 3.1 Objective

Transform the GO decision from Phase 0 into a structured and operational project base: Memory Bank filled, initial architecture defined, initial backlog created.

### 3.2 Framing Sequence

---

#### Step 1.1 — Memory Bank Initialization

> **PROMPT 1.1 — Memory Bank Initialization**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Simple — 1 send, the agent fills projectBrief.md and productContext.md
> **Copy-paste the block below as-is:**

```markdown
Read docs/brief/BRIEF-002-synthese-structuree.md and
docs/brief/BRIEF-003-decision-lancement.md.

Fill the following Memory Bank files:

1. memory-bank/projectBrief.md:
   - Project vision (2-3 synthetic sentences)
   - Main objectives (measurable)
   - Explicit Non-Goals
   - Identified constraints
   - Stakeholders

2. memory-bank/productContext.md:
   - Identified user personas
   - First User Stories (standard format)
   - Prioritized initial backlog

Commit with: 'feat(memory): Memory Bank initialization from upstream phase'
```

*-> Artifacts updated: `memory-bank/projectBrief.md`, `memory-bank/productContext.md`*

---

#### Step 1.2 — Initial Architecture

> **PROMPT 1.2 — Initial project architecture**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple — 1 send, the agent proposes the architecture and updates the Memory Bank
> **Copy-paste the block below as-is:**

```markdown
Read memory-bank/projectBrief.md and memory-bank/productContext.md.

Propose an initial architecture in docs/architecture/PRJ-002-architecture-initiale.md:
- Recommended technical stack (with justification)
- Project folder structure
- Retained architectural patterns
- Architecture decisions (ADR format)
- Identified external dependencies

Update memory-bank/systemPatterns.md and memory-bank/techContext.md.
Update memory-bank/decisionLog.md with the ADRs.
Commit with: 'feat(architecture): initial architecture + Memory Bank updated'
```

*-> Artifact produced: `docs/architecture/PRJ-002-architecture-initiale.md`*
*-> Artifacts updated: `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, `memory-bank/decisionLog.md`*

---

#### Step 1.3 — Architecture Validation

> **PROMPT 1.3 — Architecture validation by the Product Owner**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Iterative — the agent lists any inconsistencies, dialogue if corrections needed
> **Copy-paste the block below as-is:**

```markdown
Read docs/architecture/PRJ-002-architecture-initiale.md.
Verify that the proposed architecture is consistent with:
- The vision in memory-bank/projectBrief.md
- The identified constraints
- The Non-Goals

If inconsistencies exist, list them.
If the architecture is validated, update docs/brief/BRIEF-003-decision-lancement.md
with the mention 'Architecture validated on [DATE]' and commit.
```

*-> Artifact updated: `docs/brief/BRIEF-003-decision-lancement.md` (validation mention)*

---

#### Step 1.4 — Structured Initial Backlog

> **PROMPT 1.4 — Creation of the initial MoSCoW backlog**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Simple — 1 send, the agent creates the structured backlog with MoSCoW prioritization
> **Copy-paste the block below as-is:**

```markdown
Based on memory-bank/productContext.md and the validated architecture,
create docs/backlog/PRJ-003-backlog-initial.md with:

- The identified Epics (functional groupings)
- The User Stories of each Epic (standard format)
- The MoSCoW prioritization (Must/Should/Could/Won't)
- The dependencies between User Stories
- The complexity estimate (T-shirt sizing: XS/S/M/L/XL)

Update memory-bank/productContext.md with the structured backlog.
Commit with: 'feat(backlog): structured initial backlog with MoSCoW prioritization'
```

*-> Artifact produced: `docs/backlog/PRJ-003-backlog-initial.md`*
*-> Artifact updated: `memory-bank/productContext.md`*

---

### 3.3 Phase 1 Exit Criteria

- [ ] `memory-bank/projectBrief.md` filled and validated
- [ ] `memory-bank/productContext.md` contains the initial backlog
- [ ] `memory-bank/systemPatterns.md` contains the initial architecture
- [ ] `memory-bank/techContext.md` contains the stack and commands
- [ ] `docs/architecture/PRJ-002-architecture-initiale.md` exists
- [ ] `docs/backlog/PRJ-003-backlog-initial.md` exists with MoSCoW prioritization
- [ ] All files committed in Git

---

## 4. Phase 2 - Development Sprints

### 4.1 Sprint Structure

A sprint lasts **1 to 2 weeks**. It follows the standard Scrum cycle adapted to agentic development:

```
SPRINT PLANNING (Start of sprint)
  Duration: 1-2 hours
  Personas: Product Owner + Scrum Master
  Artifact: SPR-XXX-001 (Sprint Backlog)

DEVELOPMENT (Sprint body)
  Duration: 80% of the sprint
  Persona: Developer
  Artifact: SPR-XXX-003 (Source Code + commits)
  Rule: 1 User Story = N commits = 1 delivery

TESTS (End of development)
  Duration: 15% of the sprint
  Persona: QA Engineer
  Artifact: SPR-XXX-004 (Test Report)

SPRINT REVIEW (End of sprint)
  Duration: 1 hour
  Personas: Product Owner + Scrum Master
  Artifact: SPR-XXX-005 (Sprint Review)

RETROSPECTIVE (After the review)
  Duration: 30 minutes
  Persona: Scrum Master
  Artifact: SPR-XXX-006 (Retrospective)

MEMORY BANK UPDATE (Mandatory before closing)
  Persona: Scrum Master
  Files: activeContext.md, progress.md
  Commit: 'docs(memory): sprint XXX closure'
```

### 4.2 Sprint Planning

> **PROMPT 4.2 — Sprint Planning**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Simple — 1 send, replace [NNN] with the sprint number (e.g.: 001)
> **Copy-paste the block below as-is, then replace [NNN]:**

```markdown
Read memory-bank/productContext.md and memory-bank/progress.md.

Create docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md with:
- The sprint objective (Sprint Goal - 1 sentence)
- The User Stories selected from the backlog (with their ID)
- The estimated capacity (in points or days)
- The acceptance criteria of each US
- The identified technical dependencies

Update memory-bank/activeContext.md with the Sprint Goal.
Commit with: 'feat(sprint-[NNN]): sprint planning - [Sprint Goal]'
```

*-> Artifact produced: `docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md`*
*-> Artifact updated: `memory-bank/activeContext.md`*

---

### 4.3 User Story Development

**Mandatory 5-step protocol:**

```
STEP D.1 - MEMORY BANK READING (mandatory)
  Read: activeContext.md, systemPatterns.md, techContext.md

STEP D.2 - USER STORY UNDERSTANDING
  Read: docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md
  Identify: acceptance criteria, dependencies

STEP D.3 - IMPLEMENTATION
  Code the User Story
  Commit after each significant sub-task
  Commit format: 'feat(US-XXX): [description]'

STEP D.4 - MEMORY BANK UPDATE
  Update: activeContext.md (current state)
  If architecture decision: update decisionLog.md

STEP D.5 - FINAL COMMIT
  git add .
  git commit -m 'feat(US-XXX): complete implementation - [description]'
```

> **PROMPT 4.3 — User Story Development**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple — 1 send, replace [NNN] and [XXX] before sending
> **Copy-paste the block below as-is, then replace [NNN] and [XXX]:**

```markdown
Read memory-bank/activeContext.md, memory-bank/systemPatterns.md
and memory-bank/techContext.md.

Implement User Story US-[XXX] defined in
docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md.

Respect the conventions from memory-bank/systemPatterns.md.
Commit after each sub-task with the format 'feat(US-XXX): [description]'.
Update memory-bank/activeContext.md after each sub-task.
Before closing, commit memory-bank/ with 'docs(memory): US-XXX implemented'.
```

*-> Artifact produced: source code in `src/` (successive commits)*
*-> Artifact updated: `memory-bank/activeContext.md`*

---

### 4.4 Tests

> **PROMPT 4.4 — Sprint Test Report**
> **Required Roo Code mode:** `qa-engineer`
> **Complexity:** Sequential — the agent tests each US of the sprint and documents the results
> **Copy-paste the block below as-is, then replace [NNN]:**

```markdown
Read docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md
to know the acceptance criteria of each US.

For each User Story in the sprint:
1. Run the existing automated tests
2. Verify each acceptance criterion
3. Document the results in
   docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md

Commit with: 'test(sprint-[NNN]): test report - [NNN] US tested'
```

*-> Artifact produced: `docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md`*

---

### 4.5 Sprint Review

> **PROMPT 4.5 — Sprint Review**
> **Required Roo Code mode:** `product-owner`
> **Complexity:** Simple — 1 send, the agent creates the review and updates the backlog
> **Copy-paste the block below as-is, then replace [NNN]:**

```markdown
Read docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md.

Create docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md with:
- The delivered US (validated by tests)
- The undelivered US (with reason)
- The sprint velocity (delivered points / planned points)
- Feedback on the delivered features
- Backlog adjustments (new US, re-prioritization)

Update memory-bank/productContext.md with the backlog adjustments.
Commit with: 'docs(sprint-[NNN]): sprint review - velocity [X]%'
```

*-> Artifact produced: `docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md`*
*-> Artifact updated: `memory-bank/productContext.md`*

---

### 4.6 Retrospective

> **PROMPT 4.6 — Sprint Retrospective**
> **Required Roo Code mode:** `scrum-master`
> **Complexity:** Simple — 1 send, the agent creates the retro and closes the sprint in the Memory Bank
> **Copy-paste the block below as-is, then replace [NNN]:**

```markdown
Read docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md
and memory-bank/activeContext.md.

Create docs/sprints/sprint-[NNN]/SPR-[NNN]-006-retrospective.md with:
- What worked well (Keep)
- What needs to be improved (Improve)
- What needs to be stopped (Stop)
- Concrete actions for the next sprint
- Identified impediments and their resolution

Update memory-bank/progress.md (check off completed US).
Update memory-bank/activeContext.md (end-of-sprint state).

Commit with: 'docs(memory): sprint [NNN] closure - [X] US delivered'
```

*-> Artifact produced: `docs/sprints/sprint-[NNN]/SPR-[NNN]-006-retrospective.md`*
*-> Artifacts updated: `memory-bank/progress.md`, `memory-bank/activeContext.md`*

---

## 5. Phase 3 - Delivery and Maintenance

### 5.1 Release Preparation

> **PROMPT 5.1 — Release Notes**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple — 1 send, replace [VERSION] with the SemVer number (e.g.: 1.0.0)
> **Copy-paste the block below as-is, then replace [VERSION]:**

```markdown
Read memory-bank/progress.md to identify the features delivered
since the last release.

Create docs/releases/REL-[VERSION]-001-release-notes.md with:
- The version (SemVer format: MAJOR.MINOR.PATCH)
- The release date
- The new features (with reference to the US)
- The bug fixes
- The breaking changes (if MAJOR)
- The migration instructions (if applicable)

Commit with: 'docs(release): release notes v[VERSION]'
```

*-> Artifact produced: `docs/releases/REL-[VERSION]-001-release-notes.md`*

---

### 5.2 User Documentation

> **PROMPT 5.2 — User Documentation**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple — 1 send, replace [VERSION] before sending
> **Copy-paste the block below as-is, then replace [VERSION]:**

```markdown
Based on the features delivered in docs/releases/REL-[VERSION]-001-release-notes.md,
create or update docs/releases/REL-[VERSION]-002-documentation-utilisateur.md.

The documentation must cover:
- Quick start guide
- Description of each feature
- Usage examples
- FAQ

Commit with: 'docs(release): user documentation v[VERSION]'
```

*-> Artifact produced: `docs/releases/REL-[VERSION]-002-documentation-utilisateur.md`*

---

### 5.3 Deployment Runbook

> **PROMPT 5.3 — Deployment Runbook**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple — 1 send, replace [VERSION] before sending
> **Copy-paste the block below as-is, then replace [VERSION]:**

```markdown
Create docs/releases/REL-[VERSION]-003-runbook-deploiement.md with:
- System prerequisites
- Deployment steps (numbered, precise)
- Required environment variables
- Post-deployment verification commands
- Rollback procedure

Commit with: 'docs(release): deployment runbook v[VERSION]'
```

*-> Artifact produced: `docs/releases/REL-[VERSION]-003-runbook-deploiement.md`*

---

## 6. Artifact Nomenclature

### 6.1 Naming Convention

**General format:** `[CATEGORY]-[NUMBER]-[SHORT-DESCRIPTION].[ext]`

**Categories:**

| Prefix | Category | Phase | Location |
| :--- | :--- | :--- | :--- |
| `BRIEF` | Upstream phase artifacts | Phase 0 | `docs/brief/` |
| `PRJ` | Project framing artifacts | Phase 1 | `docs/architecture/`, `docs/backlog/` |
| `SPR` | Sprint artifacts | Phase 2 | `docs/sprints/sprint-[NNN]/` |
| `QA` | Test reports | Phase 2 | `docs/sprints/sprint-[NNN]/` or `docs/qa/` |
| `REL` | Release artifacts | Phase 3 | `docs/releases/` |
| `ADR` | Architecture Decision Records | All | `memory-bank/decisionLog.md` |
| `US` | User Stories | Phase 1-2 | `memory-bank/productContext.md` |

### 6.2 Complete Artifact Nomenclature

#### Phase 0 Artifacts - Upstream

| Artifact ID | File Name | Description | Responsible Persona |
| :--- | :--- | :--- | :--- |
| `BRIEF-001` | `BRIEF-001-vision-narrative.md` | Unstructured raw inputs | Product Owner |
| `BRIEF-002` | `BRIEF-002-synthese-structuree.md` | Structured analysis of inputs | Developer |
| `BRIEF-003` | `BRIEF-003-decision-lancement.md` | GO/NO-GO decision with conditions | Product Owner |

#### Phase 1 Artifacts - Framing

| Artifact ID | File Name | Description | Responsible Persona |
| :--- | :--- | :--- | :--- |
| `PRJ-001` | `memory-bank/projectBrief.md` | Vision, objectives, Non-Goals | Product Owner |
| `PRJ-002` | `PRJ-002-architecture-initiale.md` | Architecture, stack, initial ADRs | Developer |
| `PRJ-003` | `PRJ-003-backlog-initial.md` | Epics, US, MoSCoW prioritization | Product Owner |
| `PRJ-004` | `memory-bank/techContext.md` | Stack, commands, env variables | Developer |

#### Phase 2 Artifacts - Sprint

| Artifact ID | File Name | Description | Responsible Persona |
| :--- | :--- | :--- | :--- |
| `SPR-[NNN]-001` | `SPR-[NNN]-001-sprint-backlog.md` | Selected US, Sprint Goal | Product Owner |
| `SPR-[NNN]-002` | `SPR-[NNN]-002-user-stories.md` | US detail (if not in backlog) | Product Owner |
| `SPR-[NNN]-003` | Source code in `src/` | US implementation | Developer |
| `SPR-[NNN]-004` | `SPR-[NNN]-004-rapport-tests.md` | Test results, bugs | QA Engineer |
| `SPR-[NNN]-005` | `SPR-[NNN]-005-sprint-review.md` | Velocity, delivered US, feedback | Product Owner |
| `SPR-[NNN]-006` | `SPR-[NNN]-006-retrospective.md` | Keep/Improve/Stop, actions | Scrum Master |

#### Phase 3 Artifacts - Release

| Artifact ID | File Name | Description | Responsible Persona |
| :--- | :--- | :--- | :--- |
| `REL-[VER]-001` | `REL-[VER]-001-release-notes.md` | Changelog, new features | Developer |
| `REL-[VER]-002` | `REL-[VER]-002-documentation-utilisateur.md` | User guide | Developer |
| `REL-[VER]-003` | `REL-[VER]-003-runbook-deploiement.md` | Deployment procedure | Developer |

#### Memory Bank Artifacts (Persistent)

| File | Update Frequency | Responsible Persona |
| :--- | :--- | :--- |
| `memory-bank/projectBrief.md` | Rare (vision change) | Product Owner |
| `memory-bank/productContext.md` | Each sprint (backlog) | Product Owner |
| `memory-bank/systemPatterns.md` | After architecture decision | Developer |
| `memory-bank/techContext.md` | After stack change | Developer |
| `memory-bank/activeContext.md` | **Every session** | All |
| `memory-bank/progress.md` | **Every end of sprint** | Scrum Master |
| `memory-bank/decisionLog.md` | After each ADR | Developer |

### 6.3 Application Project Folder Structure

```
[PROJECT ROOT]
|-- .clinerules                    # Workbench rules (copy from workbench)
|-- .gitignore                     # Git exclusions
|-- .roomodes                      # Agile personas (copy from workbench)
|-- .workbench-version             # Deployed workbench version
|-- Modelfile                      # Ollama config (if Local Mode)
|-- proxy.py                       # Gemini proxy (if Proxy Mode)
|-- requirements.txt               # Python proxy dependencies
|
|-- docs/                          # All documentary artifacts
|   |-- brief/                     # Phase 0 - Upstream
|   |   |-- BRIEF-001-vision-narrative.md
|   |   |-- BRIEF-002-synthese-structuree.md
|   |   |-- BRIEF-003-decision-lancement.md
|   |   +-- archive/               # Archived NO-GO projects
|   |
|   |-- architecture/              # Phase 1 - Framing
|   |   +-- PRJ-002-architecture-initiale.md
|   |
|   |-- backlog/                   # Phase 1 - Backlog
|   |   +-- PRJ-003-backlog-initial.md
|   |
|   |-- sprints/                   # Phase 2 - Sprints
|   |   |-- sprint-001/
|   |   |   |-- SPR-001-001-sprint-backlog.md
|   |   |   |-- SPR-001-004-rapport-tests.md
|   |   |   |-- SPR-001-005-sprint-review.md
|   |   |   +-- SPR-001-006-retrospective.md
|   |   +-- sprint-002/
|   |       +-- ...
|   |
|   |-- qa/                        # QA reports (written by QA Engineer)
|   |   +-- .gitkeep
|   |
|   +-- releases/                  # Phase 3 - Releases
|       |-- REL-1.0.0-001-release-notes.md
|       |-- REL-1.0.0-002-documentation-utilisateur.md
|       +-- REL-1.0.0-003-runbook-deploiement.md
|
|-- memory-bank/                   # Memory Bank - 7 persistent files
|   |-- activeContext.md
|   |-- decisionLog.md
|   |-- productContext.md
|   |-- progress.md
|   |-- projectBrief.md
|   |-- systemPatterns.md
|   +-- techContext.md
|
|-- prompts/                       # Prompts registry (copy from workbench)
|   |-- README.md
|   +-- SP-001 to SP-007
|
|-- scripts/                       # Utility scripts (copy from workbench)
|   |-- check-prompts-sync.ps1
|   +-- start-proxy.ps1
|
+-- src/                           # Application source code
    +-- [project-specific structure]
```

---

## 7. Artifact Templates

### 7.1 Template BRIEF-001 - Narrative Vision

```markdown
# BRIEF-001 - Raw Narrative Vision
**Creation date:** [DATE]
**Created by:** Product Owner
**Status:** Draft

---

## Raw Inputs

> This file contains inputs AS-IS, without reformulation.
> Do not modify the original content. Add new inputs below.

### Input 1 - [Source: email / meeting / note / existing code]
**Date:** [DATE]
**Author:** [NAME]

[PASTE RAW TEXT HERE WITHOUT MODIFICATION]

---

### Input 2 - [Source]
**Date:** [DATE]

[PASTE HERE]

---

## Addition History
| Date | Source | Summary |
| :--- | :--- | :--- |
| [DATE] | [SOURCE] | [SUMMARY IN 1 LINE] |
```

### 7.2 Template BRIEF-002 - Structured Synthesis

```markdown
# BRIEF-002 - Structured Synthesis
**Creation date:** [DATE]
**Based on:** BRIEF-001-vision-narrative.md
**Status:** Under analysis

---

## Identified Features

### Explicit Features (clearly mentioned)
- [F-001] [Description]
- [F-002] [Description]

### Implicit Features (inferred from context)
- [F-I-001] [Description] - *Inferred from: "[quote from BRIEF-001]"*

---

## Identified Target Users

| Persona | Description | Main Needs |
| :--- | :--- | :--- |
| [Name] | [Description] | [Needs] |

---

## Identified Constraints

### Technical Constraints
- [CT-001] [Description]

### Business / Legal Constraints
- [CM-001] [Description]

---

## Apparent Scope

### In Scope
- [Description]

### Out of Scope (apparent)
- [Description]

---

## Ambiguities and Open Questions

| ID | Question | Criticality | Status |
| :--- | :--- | :--- | :--- |
| [Q-001] | [Precise question] | CRITICAL / HIGH / LOW | Open / Resolved |

### Answers to Questions
**Q-001:** [Answer obtained on DATE]

---

## Identified Risks
- [R-001] [Risk description] - Probability: [H/M/L] - Impact: [H/M/L]
```

### 7.3 Template BRIEF-003 - Launch Decision

```markdown
# BRIEF-003 - Launch Decision
**Decision date:** [DATE]
**Decision maker:** [NAME]

---

## Decision

**[ ] GO** - The project is launched
**[ ] NO-GO** - The project is abandoned
**[ ] HOLD** - The project is suspended until [CONDITION]

---

## Justification
[Why this decision?]

---

## Launch Conditions (if HOLD)
- [ ] [Condition 1]
- [ ] [Condition 2]

---

## Accepted Risks
- [R-001] [Description] - Mitigation: [Plan]

---

## Validated Scope for Launch
[Description of the initial validated scope]

---

## History
| Date | Decision | Reason |
| :--- | :--- | :--- |
| [DATE] | [GO/NO-GO/HOLD] | [Reason] |
```

### 7.4 Template SPR-[NNN]-001 - Sprint Backlog

```markdown
# SPR-[NNN]-001 - Sprint [NNN] Backlog
**Sprint:** [NNN]
**Dates:** [START DATE] -> [END DATE]
**Sprint Goal:** [ONE SENTENCE DESCRIBING THE SPRINT OBJECTIVE]
**Capacity:** [X] points / [Y] days

---

## Selected User Stories

### US-[XXX] - [Title]
**Epic:** [Epic Name]
**Priority:** Must / Should / Could
**Complexity:** XS / S / M / L / XL ([X] points)
**Assigned to:** Developer

**As a** [persona]
**I want** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [CA-001] [Measurable criterion]
- [ ] [CA-002] [Measurable criterion]

**Dependencies:** [US-XXX or None]
**Technical notes:** [Implementation constraints]

---

## Summary

| US | Title | Points | Status |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Title] | [X] | To do / In progress / Done |

**Total planned points:** [X]
**Total delivered points:** [Y] *(updated at end of sprint)*
**Velocity:** [Y/X * 100]% *(updated at end of sprint)*
```

### 7.5 Template SPR-[NNN]-004 - Test Report

```markdown
# SPR-[NNN]-004 - Sprint [NNN] Test Report
**Sprint:** [NNN]
**Test date:** [DATE]
**QA Engineer:** [QA Engineer Mode - Roo Code]
**LLM backend used:** [Ollama / Proxy Gemini / Claude API]

---

## Executive Summary

| Metric | Value |
| :--- | :--- |
| US tested | [X] / [Y] planned |
| Tests passed | [X] |
| Tests failed | [X] |
| Critical bugs | [X] |
| Minor bugs | [X] |
| Code coverage | [X]% |

---

## Results by User Story

### US-[XXX] - [Title]
**Overall status:** VALIDATED / REJECTED / PARTIAL

| Acceptance Criterion | Result | Notes |
| :--- | :--- | :--- |
| CA-001: [Description] | PASS / FAIL | [Notes] |
| CA-002: [Description] | PASS / FAIL | [Notes] |

**Test command executed:** `[command]`

**Output:** `[command output]`

---

## Identified Bugs

### BUG-[NNN]-001 - [Title]
**Severity:** CRITICAL / HIGH / MEDIUM / LOW
**Related US:** US-[XXX]
**Reproduction steps:**
1. [Step 1]
2. [Step 2]
**Expected behavior:** [Description]
**Observed behavior:** [Description]
**Status:** Open / Fixed / Accepted

---

## QA Recommendation
**[ ] Sprint validated** - All critical US pass the tests
**[ ] Sprint rejected** - Critical bugs block delivery
**[ ] Partial delivery** - [X] US validated out of [Y]
```

### 7.6 Template SPR-[NNN]-005 - Sprint Review

```markdown
# SPR-[NNN]-005 - Sprint [NNN] Review
**Sprint:** [NNN]
**Date:** [DATE]
**Participants:** Product Owner, Scrum Master

---

## Sprint Goal
[Sprint Goal reminder]
**Achieved:** YES / NO / PARTIALLY

---

## Delivered User Stories

| US | Title | Points | Validated by QA |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Title] | [X] | YES / NO |

**Velocity:** [X] delivered points / [Y] planned points = [Z]%

---

## Undelivered User Stories

| US | Title | Reason | Action |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Title] | [Reason] | Carry over to next sprint / Abandon |

---

## Feedback on Features
[Observations on the delivered features]

---

## Backlog Adjustments
- [US-XXX]: Re-prioritized from Should -> Must (reason: [])
- [US-YYY]: New US added (reason: [])
- [US-ZZZ]: Abandoned (reason: [])

---

## Release Decision
**[ ] Release planned** for version [X.Y.Z]
**[ ] No release** - Continue sprints
```

### 7.7 Template SPR-[NNN]-006 - Retrospective

```markdown
# SPR-[NNN]-006 - Sprint [NNN] Retrospective
**Sprint:** [NNN]
**Date:** [DATE]
**Facilitated by:** Scrum Master

---

## Keep - What worked well
- [Description]
- [Description]

## Improve - What needs to be improved
- [Description] -> Action: [Concrete action]
- [Description] -> Action: [Concrete action]

## Stop - What needs to be stopped
- [Description]

---

## Actions for the Next Sprint

| Action | Responsible | Deadline |
| :--- | :--- | :--- |
| [Description] | [Persona] | Sprint [NNN+1] |

---

## Identified Impediments

| Impediment | Impact | Resolution |
| :--- | :--- | :--- |
| [Description] | [Impact] | [Resolution plan] |

---

## Sprint Metrics
- Velocity: [X] points
- Average velocity (last 3 sprints): [Y] points
- Trend: Rising / Stable / Declining
```

---

## 8. Agentic Anti-Risk Mechanisms

### 8.1 Agentic Risk Catalog

Agentic development presents specific risks absent from classical human development. This catalog identifies them and describes the countermeasures integrated into the workbench.

| Risk ID | Risk | Probability | Impact | Main Countermeasure |
| :--- | :--- | :--- | :--- | :--- |
| **RA-001** | Context loss between sessions | VERY HIGH | CRITICAL | Memory Bank + CHECK->CREATE->READ->ACT sequence |
| **RA-002** | Code hallucination | HIGH | CRITICAL | Temperature 0.15 + deterministic Modelfile |
| **RA-003** | Architecture drift over several months | HIGH | HIGH | `systemPatterns.md` + ADRs in `decisionLog.md` |
| **RA-004** | Inconsistency across long sessions | HIGH | HIGH | `activeContext.md` updated every session |
| **RA-005** | Silent regression | MEDIUM | CRITICAL | Mandatory QA tests + versioned reports |
| **RA-006** | Loss of product vision | MEDIUM | HIGH | `projectBrief.md` immutable unless explicit decision |
| **RA-007** | Undetected code duplication | MEDIUM | MEDIUM | `systemPatterns.md` + Developer review |
| **RA-008** | Untraced architecture decisions | HIGH | HIGH | `decisionLog.md` + RULE 2 `.clinerules` |
| **RA-009** | Prompt injection / behavioral drift | LOW | CRITICAL | `.clinerules` + RBAC `.roomodes` |
| **RA-010** | Working on wrong code version | MEDIUM | HIGH | Mandatory Git + frequent commits |

---

### 8.2 RA-001 - Context Loss Between Sessions

**Risk description:** An LLM has no memory between two sessions. Without an explicit mechanism, each session starts from scratch. On a multi-month project, this leads to inconsistencies, re-implementations, contradictions.

**Integrated countermeasures:**

```
LEVEL 1 - Mandatory startup sequence (RULE 1 .clinerules)
  The agent MUST read activeContext.md and progress.md before any action
  If the files do not exist, it creates them from the templates

LEVEL 2 - Mandatory update at closure (RULE 2 .clinerules)
  The agent MUST update activeContext.md before attempt_completion
  activeContext.md contains: current task, last result, next action

LEVEL 3 - Thematic context according to the task (RULE 3 .clinerules)
  Before architecture modification: read systemPatterns.md
  Before build/test commands: read techContext.md
  At sprint start: read productContext.md

LEVEL 4 - Redundancy in roleDefinitions (.roomodes)
  The Developer has the READ->CODE->UPDATE->COMMIT protocol inscribed
  in its roleDefinition - even if .clinerules is not read
```

**Resume protocol after long interruption (> 1 week):**

> **PROMPT RA-001 -- Resume after interruption**
> **Required Roo Code mode:** `scrum-master`
> **Complexity:** Simple -- 1 send, replace [X] with the number of days of interruption
> **Copy-paste the block below as-is, then replace [X]:**

```markdown
I am resuming the project after [X] days of interruption.
Read in this order:
1. memory-bank/activeContext.md
2. memory-bank/progress.md
3. memory-bank/projectBrief.md
4. memory-bank/productContext.md

Then generate a project status summary:
- Where are we?
- What was the last task in progress?
- What are the next actions?
- Are there any identified blockers?

Update activeContext.md with the resume date.
Commit with: 'docs(memory): project resume after [X] days - [DATE]'
```

---

### 8.3 RA-002 - Code Hallucination

**Risk description:** An LLM can generate syntactically correct but functionally wrong code, invent non-existent APIs, or produce implementations that seem plausible but do not work.

**Integrated countermeasures:**

```
LEVEL 1 - Determinism parameters (Ollama Modelfile)
  temperature 0.15 (quasi-deterministic)
  min_p 0.03, top_p 0.95, repeat_penalty 1.1
  Drastically reduces "creative" unfounded responses

LEVEL 2 - Mandatory QA tests after each US
  The QA Engineer runs real tests (not simulated)
  Acceptance criteria are verified one by one
  Bugs are documented in SPR-[NNN]-004

LEVEL 3 - Frequent commits with descriptive messages
  Each sub-task is committed separately
  If hallucination detected: git revert to the last clean commit

LEVEL 4 - Memory Bank reading before coding
  systemPatterns.md contains the REAL patterns of the project
  techContext.md contains the REAL tested commands
  The agent codes in coherence with what exists, not what it imagines
```

**Detecting a hallucination:**

```
Warning signs:
- The agent imports a library not in requirements.txt
- The agent calls a function that does not exist in the code
- The agent describes an architecture different from systemPatterns.md
- QA tests systematically fail on a US

Corrective action:
1. git log --oneline -10  (identify the last clean commit)
2. git diff HEAD~1        (see what changed)
3. git revert [hash]      (roll back if necessary)
4. Update activeContext.md with the problem description
5. Relaunch the Developer with more precise context
```

---

### 8.4 RA-003 - Architectural Drift Over Several Months

**Risk description:** On a long project, architecture decisions made in Phase 1 can be forgotten or contradicted by later decisions. Without traceability, the code becomes inconsistent.

**Integrated countermeasures:**

```
LEVEL 1 - decisionLog.md as ADR registry
  Each architecture decision is documented with:
  Date, context, decision made, consequences
  Format: ADR-[NNN] with sequential numbering

LEVEL 2 - systemPatterns.md as living reference
  Updated after each architecture decision
  Contains the CURRENT patterns (not the initial patterns)
  The agent reads this file before any architectural modification

LEVEL 3 - RULE 2 .clinerules
  If an architecture decision is made during the session:
  MANDATORY update of memory-bank/decisionLog.md

LEVEL 4 - Architectural review in Sprint Review
  The Product Owner verifies consistency with the initial vision
  Drifts are identified and documented
```

**Architectural review protocol (every 3 sprints):**

> **PROMPT RA-003 -- Architectural review**
> **Required Roo Code mode:** `developer`
> **Complexity:** Simple -- 1 send, replace [NNN] with the current sprint number
> **Copy-paste the block below as-is, then replace [NNN]:**

```markdown
Read memory-bank/systemPatterns.md, memory-bank/decisionLog.md
and docs/architecture/PRJ-002-architecture-initiale.md.

Compare the initial architecture with the current architecture.
Identify:
- Drifts from the initial architecture
- Implicit decisions not documented in decisionLog.md
- Inconsistent patterns between modules

Document your conclusions in docs/architecture/ARCH-REVIEW-[DATE].md.
Update decisionLog.md with the missing ADRs.
Commit with: 'docs(architecture): architectural review sprint [NNN]'
```

---

### 8.5 RA-004 - Inconsistency Across Long Sessions (Multi-Month)

**Risk description:** On a multi-month project with dozens of sessions, the information in the Memory Bank can become obsolete, contradictory or incomplete.

**Integrated countermeasures:**

```
LEVEL 1 - activeContext.md as "working memory"
  Updated at EVERY session (start and end)
  Always contains the most recent state
  Includes the hash of the last Git commit

LEVEL 2 - progress.md as "dashboard"
  Checklist of phases and features
  Updated at each end of sprint
  Allows seeing at a glance where the project stands

LEVEL 3 - Git versioning of the Memory Bank
  git log --oneline -- memory-bank/ shows the complete history
  In case of doubt: git show [hash]:memory-bank/activeContext.md

LEVEL 4 - Periodic consistency audit (monthly)
```

**Memory Bank consistency audit protocol (monthly):**

> **PROMPT RA-004 -- Memory Bank consistency audit**
> **Required Roo Code mode:** `scrum-master`
> **Complexity:** Sequential -- the agent checks each file and corrects inconsistencies
> **Copy-paste the block below as-is:**

```markdown
Perform a Memory Bank consistency audit.

For each file, verify:
1. projectBrief.md: Is the vision still valid?
2. productContext.md: Is the backlog up to date with the delivered sprints?
3. systemPatterns.md: Do the patterns match the current code?
4. techContext.md: Are the commands and versions up to date?
5. activeContext.md: Does the described state match the Git reality?
6. progress.md: Do the checked boxes match the commits?
7. decisionLog.md: Are all recent decisions documented?

For each inconsistency found, correct the relevant file.
Commit with: 'docs(memory): monthly consistency audit [DATE]'
```

---

### 8.6 RA-005 - Silent Regression

**Risk description:** A Developer modification can break an existing feature without anyone detecting it, especially if tests do not cover all features.

**Integrated countermeasures:**

```
LEVEL 1 - Mandatory QA tests after each US
  The QA Engineer tests not only the new US
  But also the previous US potentially impacted

LEVEL 2 - Atomic commits
  Each US = series of related commits
  git bisect allows identifying the commit that introduced the regression

LEVEL 3 - Versioned test report
  SPR-[NNN]-004 documents the test state at each sprint
  Comparison possible between sprints to detect regressions

LEVEL 4 - Acceptance criteria in the Sprint Backlog
  Each US has precise and testable acceptance criteria
  The QA Engineer verifies each criterion individually
```

---

### 8.7 RA-008 - Untraced Architecture Decisions

**Risk description:** The agent makes implicit architecture decisions (library choice, implementation pattern) without documenting them. These decisions are lost between sessions.

**Integrated countermeasures:**

```
LEVEL 1 - RULE 2 .clinerules (mandatory)
  If an architecture decision was made during the session:
  MANDATORY update of memory-bank/decisionLog.md

LEVEL 2 - Standardized ADR format
  Each ADR contains: Date, Context, Decision, Consequences
  Sequential numbering: ADR-001, ADR-002, ...

LEVEL 3 - Proactive detection by the Developer
  Before choosing a library: check decisionLog.md
  If a similar decision exists: respect it or revise it explicitly
```

**Standard ADR format:**

```markdown
## ADR-[NNN]: [Decision title]
**Date:** [DATE]
**Status:** Proposed / Accepted / Deprecated / Replaced by ADR-[YYY]

**Context:**
[Why this decision was necessary]

**Decision:**
[What was decided]

**Consequences:**
- Advantage: [Description]
- Disadvantage: [Description]
- Impact on: [Relevant files/modules]
```

---

### 8.8 Anti-Risk Summary Table

| Risk | Preventive Mechanism | Detective Mechanism | Corrective Mechanism |
| :--- | :--- | :--- | :--- |
| RA-001 Context loss | Memory Bank + RULE 1 | CHECK->CREATE->READ sequence | Long interruption resume protocol |
| RA-002 Hallucination | T=0.15 + Modelfile | QA tests + git diff | git revert + relaunch with precise context |
| RA-003 Arch drift | decisionLog.md + RULE 2 | Arch review every 3 sprints | ARCH-REVIEW + ADR update |
| RA-004 Multi-month inconsistency | activeContext.md every session | Monthly Memory Bank audit | Correction + docs(memory) commit |
| RA-005 Regression | Mandatory QA tests | SPR-[NNN]-004 compares to previous | git bisect + fix + re-test |
| RA-008 Untraced ADRs | RULE 2 .clinerules | decisionLog.md audit | Retro-documentation of decisions |

---

## 9. Session Protocols

### 9.1 Session Startup Protocol

**Applicable to all sessions, all modes, all personas.**

```
STEP 1 - VERIFICATION (automatic via .clinerules RULE 1)
  The agent verifies the existence of:
  - memory-bank/activeContext.md
  - memory-bank/progress.md

STEP 2 - CREATION if absent
  If one of the files is absent:
  The agent creates it from the template defined in .clinerules
  Then moves to step 3

STEP 3 - READING
  The agent reads in this order:
  1. memory-bank/activeContext.md  (current state)
  2. memory-bank/progress.md       (global progress)

STEP 4 - CONTEXTUAL READING (according to the task)
  If architecture modification planned: read systemPatterns.md
  If build/test commands planned: read techContext.md
  If sprint start: read productContext.md

STEP 5 - ACTION
  The agent processes the user's request
```

> **PROMPT 9.1 -- Session startup (context instruction)**
> **Required Roo Code mode:** `[the mode appropriate to the task]`
> **Complexity:** Simple -- to add at the beginning of any prompt to force context reading
> **Copy-paste this prefix before your request:**

```markdown
Before acting, read memory-bank/activeContext.md and
memory-bank/progress.md to get back into the project context.

[Describe here the task to accomplish]
```

---

### 9.2 Session Closure Protocol

**Applicable before any `attempt_completion`, all modes, all personas.**

```
STEP 1 - UPDATE activeContext.md (mandatory)
  Content to update:
  - Update date
  - Task accomplished during this session
  - Current project state
  - Recommended next action(s)
  - Possible blockers
  - Hash of the last Git commit

STEP 2 - UPDATE progress.md (if features completed)
  Check off the US or phases completed during the session

STEP 3 - UPDATE decisionLog.md (if architecture decision)
  Document any architecture decision made during the session
  Standard ADR format (see section 8.7)

STEP 4 - GIT COMMIT (mandatory)
  git add .
  git commit -m "docs(memory): [session description]"
  The hash of this commit must be noted in activeContext.md
```

---

### 9.3 Resume Protocol After Interruption

**Use this protocol after any interruption > 1 week.**

> **PROMPT 9.3 -- Resume after long interruption**
> **Required Roo Code mode:** `scrum-master`
> **Complexity:** Simple -- 1 send, replace [X] and [DATE]
> **Copy-paste the block below as-is, then replace [X] and [DATE]:**

```markdown
I am resuming the project after [X] days/weeks of interruption.

Perform a resume assessment:

1. Read memory-bank/activeContext.md
   -> What was the last task in progress?
   -> What was the project state?

2. Read memory-bank/progress.md
   -> Which phases/features are completed?
   -> Which are in progress?

3. Run: git log --oneline -10
   -> What are the last commits?
   -> Are there commits not documented in the Memory Bank?

4. Read memory-bank/projectBrief.md
   -> Is the project vision still valid?

5. Generate a resume report in docs/sprints/REPRISE-[DATE].md:
   - Project state at the time of resumption
   - Recommended next actions
   - Risks identified after the interruption

6. Update memory-bank/activeContext.md with the resume date.
7. Commit with: 'docs(memory): project resume after [X] days - [DATE]'
```

---

### 9.4 LLM Backend Switch Protocol

**Use this protocol when switching between the 3 LLM modes.**

```
BEFORE SWITCHING:
  1. Commit the current Memory Bank state
     git add memory-bank/
     git commit -m "docs(memory): save before LLM backend switch"

  2. Note the new backend in activeContext.md
     "Active LLM backend: [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]"

AFTER SWITCHING:
  3. Test the new backend with a simple request
     "Read memory-bank/activeContext.md and summarize the project state."

  4. Verify that the Memory Bank is correctly read
     The summary must match the actual content of the files

WHY THIS PROTOCOL:
  Each LLM backend has different characteristics:
  - Ollama (local): deterministic, may be slower on complex tasks
  - Proxy Gemini: high quality, requires human copy-paste
  - Claude API: high quality, fully automatic, paid
  The Memory Bank guarantees context continuity regardless of the backend.

KNOWN LIMITATIONS OF PROXY GEMINI MODE (to document in activeContext.md):
  - Boomerang Tasks (new_task): NOT SUPPORTED -- use Claude API for tasks
    requiring sub-agents
  - Long tasks (> 10 LLM turns): NOT RECOMMENDED -- split into sub-tasks or
    use Claude API
  - Parallel clipboard use: IMPOSSIBLE during a proxy session
  - Unsupervised execution: IMPOSSIBLE -- continuous human presence required
  - Gemini conversation: ALWAYS use a NEW conversation each session
    (do not continue an existing conversation -- the proxy already sends the full history)
```

> **KNOWN LIMITATIONS OF PROXY GEMINI MODE** (to document in `activeContext.md` when switching):
>
> | Limitation | Detail | Alternative |
> | :--- | :--- | :--- |
> | **Boomerang Tasks (`new_task`): NOT SUPPORTED** | Two concurrent Roo Code instances share the same clipboard -> immediate deadlock | Use Local Mode (Ollama on `calypso`) or Cloud Mode (Claude API) |
> | **Long tasks (> 10 LLM turns): NOT RECOMMENDED** | Clipboard size explodes, human cognitive fatigue | Split into sub-tasks of < 10 turns, or use Claude API |
> | **Parallel clipboard use: IMPOSSIBLE** | Any Ctrl+C during a proxy session overwrites the Gemini response waiting | Do not use the clipboard for anything else during a session |
> | **Unsupervised execution: IMPOSSIBLE** | Continuous human presence required at each LLM turn | Use Local Mode (Ollama on `calypso`) or Cloud Mode (Claude API) |
> | **Gemini conversation: ALWAYS new conversation** | The proxy already sends the full history in the clipboard -- continuing an existing conversation duplicates the history | Open a new Gemini conversation each proxy session |

> **PROMPT 9.4 -- LLM backend switch test**
> **Required Roo Code mode:** `scrum-master`
> **Complexity:** Simple -- 1 send to verify that the new backend reads the Memory Bank correctly
> **Copy-paste the block below as-is:**

```markdown
Read memory-bank/activeContext.md and summarize in 5 points:
1. The current project
2. The last accomplished task
3. The current state
4. The next actions
5. Any blockers
```

---

### 9.4.1 Task Splitting Strategy in Proxy Mode

> **Golden rule of Proxy Mode:** Keep each task under **10 LLM turns** (10 clipboard round-trips). Beyond that, the clipboard size explodes and human cognitive fatigue degrades quality.

#### Why split?

In Proxy Gemini Mode, each LLM turn represents:
- **~30 to 60 seconds** of active human attention (copy-paste)
- **Clipboard growth**: the full history is sent at each turn
- **An increasing risk of human error** with fatigue

A 20-turn task = ~15-20 minutes of continuous attention + risk of clipboard corruption.

#### Splitting rules

| Task size | Estimated LLM turns | Verdict | Action |
| :--- | :---: | :---: | :--- |
| Simple task (1 file, 1 action) | 1-3 | Ideal | Launch directly |
| Medium task (2-3 files, simple logic) | 4-7 | Acceptable | Launch directly |
| Complex task (architecture, multi-file) | 8-10 | Limit | Split if possible |
| Long task (complete US, refactoring) | 10-20 | Too long | **Split mandatory** |
| Very long task (full sprint, migration) | 20+ | Impossible | Use Claude API |

#### How to split a long task

**Principle:** Identify **intermediate delivery points** -- stable states where the code works and can be committed.

```
LONG TASK: "Implement User Story US-042 (JWT authentication)"
  Estimated at 15-20 LLM turns

SPLIT INTO PROXY SUB-TASKS:

  Sub-task A (3-4 turns):
  "Create the User model and database migrations.
   Commit when done."

  Sub-task B (3-4 turns):
  "Implement the POST /auth/login endpoint with JWT generation.
   Use the User model created previously. Commit."

  Sub-task C (3-4 turns):
  "Implement the JWT verification middleware for protected routes.
   Commit."

  Sub-task D (2-3 turns):
  "Write unit tests for the 3 previous components. Commit."
```

#### Warning signals during a proxy session

If you observe any of these signals, **finish the current sub-task and start a new session**:

- The clipboard contains > 30,000 characters (verifiable in the proxy console)
- You have performed > 8 clipboard round-trips
- The Gemini response starts to be truncated or incoherent
- You are having trouble following what the agent is doing
- You accidentally used the clipboard for something else

#### Sub-task closure protocol

Before finishing a sub-task and starting a new one:

```
1. Ask the agent to commit the current state:
   "Commit everything that has been done with a descriptive message."

2. Ask the agent to update activeContext.md:
   "Update memory-bank/activeContext.md with the current state
    and the next sub-task to do."

3. Commit the Memory Bank:
   "git add memory-bank/ && git commit -m 'docs(memory): intermediate state [description]'"

4. Open a new Roo Code session (new Gemini conversation)
   and resume with the next sub-task.
```

> **PROMPT 9.4.1 -- Long task splitting**
> **Required Roo Code mode:** `scrum-master`
> **Complexity:** Simple -- 1 send to get a splitting plan before starting
> **Copy-paste the block below as-is, then replace [TASK DESCRIPTION]:**

```markdown
I am going to use Proxy Gemini Mode for the following task:
[TASK DESCRIPTION]

Before starting, decompose this task into sub-tasks of maximum 5 LLM turns each.
For each sub-task:
- Describe what needs to be done
- Identify the intermediate delivery point (committable state)
- Estimate the number of LLM turns needed

Present the plan as a numbered list.
I will launch each sub-task in a separate proxy session.
```

---

### 9.5 Git Conflict Resolution Protocol

**Use this protocol if Git conflicts appear (rare but possible).**

> **PROMPT 9.5 -- Git conflict resolution**
> **Required Roo Code mode:** `developer`
> **Complexity:** Iterative -- the agent identifies conflicts and proposes resolutions
> **Copy-paste the block below as-is:**

```markdown
A Git conflict has been detected.

1. Run: git status
   -> Identify the conflicting files

2. For each conflicting file:
   - If conflict in memory-bank/: favor the most recent version
   - If conflict in src/: analyze both versions and choose the best
   - If conflict in docs/: merge both versions if possible

3. After resolution:
   git add [resolved files]
   git commit -m 'fix(git): conflict resolution [description]'

4. Update memory-bank/activeContext.md with the conflict description
   and its resolution.
```

---

### 9.6 Agent Error Handling Protocol

**Use this protocol if the agent produces incorrect or incoherent results.**

```
DIAGNOSIS:
  1. Identify the error type:
     - Hallucination (invented code, non-existent API)
     - Inconsistency with Memory Bank (ignores conventions)
     - Context overflow (forgets the beginning of the conversation)
     - RBAC permission error (attempts an out-of-scope action)
     - Proxy timeout (HTTP 408 -- no response copied within the deadline)

CORRECTION BY TYPE:

  Hallucination:
  -> git revert [last problematic commit]
  -> Relaunch with more precise context and concrete examples
  -> Verify that systemPatterns.md and techContext.md are up to date

  Inconsistency with Memory Bank:
  -> Verify that .clinerules is at the project root
  -> Reload VS Code (Ctrl+Shift+P > "Developer: Reload Window")
  -> Relaunch explicitly reminding to read the Memory Bank

  Context overflow:
  -> Start a new Roo Code session
  -> The new session will re-read the Memory Bank from the start
  -> That is why the Memory Bank must be up to date before each closure

  RBAC error:
  -> Verify that the correct persona is selected in Roo Code
  -> Verify that .roomodes is at the project root
  -> If the persona attempts an out-of-scope action, it must refuse
     and suggest the appropriate persona

  Proxy timeout (HTTP 408):
  -> Observed Roo Code behavior: Roo Code receives an HTTP 408 error
     and displays an error message in the interface ("Request Timeout" or
     "Error communicating with the API"). It does NOT perform automatic retry
     -- the current task is interrupted and the agent waits for a new instruction.
  -> Cause: The human did not copy the Gemini response within the TIMEOUT_SECONDS
     deadline (default: 300s), or used the clipboard for something else while waiting.
  -> Corrective action:
     1. Check in the proxy console the number of the expired request (#N)
     2. Return to Gemini and copy the response if still available
        (Ctrl+A then Ctrl+C on the Gemini response)
     3. If the Gemini response is no longer available: relaunch the same request
        in Roo Code -- the proxy will send a new prompt to Gemini
     4. If timeouts are frequent: increase TIMEOUT_SECONDS in proxy.py
        (e.g.: TIMEOUT_SECONDS = 600 for 10 minutes)
  -> Prevention: Never use the clipboard for anything else while
     a proxy request is waiting (see limitations section 9.4).
```

---

## 10. Project Dashboard

### 10.1 Project Health Indicators

The dashboard is maintained in `memory-bank/progress.md`. It must permanently reflect the real project state.

**Indicators to monitor:**

| Indicator | Source | Update Frequency | Alert Threshold |
| :--- | :--- | :--- | :--- |
| Sprint velocity | SPR-[NNN]-005 | End of sprint | < 50% of target velocity |
| Test coverage | SPR-[NNN]-004 | End of sprint | < 70% |
| Open critical bugs | SPR-[NNN]-004 | Continuous | > 0 |
| Undocumented ADRs | decisionLog.md | Continuous | > 0 |
| Memory Bank up to date | activeContext.md | Each session | > 48h without update |
| Commits without message | git log | Continuous | > 0 "WIP" or empty commits |

---

### 10.2 Extended progress.md Template for Application Project

```markdown
# Project Progress [PROJECT NAME]
**Last updated:** [DATE]
**Current sprint:** [NNN]
**Active LLM backend:** [Ollama / Proxy Gemini / Claude API]

---

## Workbench Infrastructure
- [x] Phase 0: Open upstream - GO decision
- [x] Phase 1: Framing - Memory Bank initialized
- [x] Phase 1: Initial architecture validated
- [x] Phase 1: Initial backlog created
- [ ] Phase 2: Sprint 001 in progress
- [ ] Phase 3: First release

---

## Backlog by Epic

### Epic 1: [Epic Name]
- [x] US-001: [Title] - Sprint 001 - DELIVERED
- [-] US-002: [Title] - Sprint 001 - IN PROGRESS
- [ ] US-003: [Title] - Sprint 002 - PLANNED
- [ ] US-004: [Title] - Backlog - NOT PLANNED

### Epic 2: [Epic Name]
- [ ] US-010: [Title] - Backlog - NOT PLANNED

---

## Sprint History

| Sprint | Dates | Goal | Planned US | Delivered US | Velocity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sprint 001 | [DATE]->[DATE] | [Goal] | [X] | [Y] | [Z]% |

---

## Open Bugs

| ID | Severity | US | Description | Target Sprint |
| :--- | :--- | :--- | :--- | :--- |
| BUG-001-001 | HIGH | US-002 | [Description] | Sprint 002 |

---

## Recent Architecture Decisions
- ADR-001: [Title] - [DATE] - Accepted
- ADR-002: [Title] - [DATE] - Accepted

---

## Legend
- [ ] To do  |  [-] In progress  |  [x] Done
```

---

### 10.3 Quality Checklist per Sprint

To verify at the end of each sprint before starting the next:

**Code Quality:**
- [ ] All sprint US have documented QA tests
- [ ] No open critical bugs
- [ ] Code respects the conventions of `systemPatterns.md`
- [ ] All dependencies are in `requirements.txt` / `package.json`

**Memory Bank Quality:**
- [ ] `activeContext.md` updated with end-of-sprint state
- [ ] `progress.md` updated (US checked off)
- [ ] `decisionLog.md` contains all sprint ADRs
- [ ] `productContext.md` reflects the backlog adjustments from the Sprint Review

**Versioning Quality:**
- [ ] All modified files are committed
- [ ] Commit messages follow the Conventional Commits format
- [ ] No `.env` or `venv/` file in Git
- [ ] `git log --oneline -10` shows descriptive commits

**Artifact Quality:**
- [ ] `SPR-[NNN]-001` (Sprint Backlog) exists and is complete
- [ ] `SPR-[NNN]-004` (Test Report) exists and is signed by QA Engineer
- [ ] `SPR-[NNN]-005` (Sprint Review) exists with the calculated velocity
- [ ] `SPR-[NNN]-006` (Retrospective) exists with the next sprint actions

---

### 10.4 Quick Diagnostic Commands

These commands allow quickly checking the project state:

```powershell
# Git project state
git log --oneline -10
git status

# Verify that the Memory Bank is up to date
Get-Content memory-bank/activeContext.md | Select-Object -First 10

# List all project artifacts
Get-ChildItem docs/ -Recurse -Filter "*.md" | Select-Object Name, LastWriteTime

# Check open bugs in QA reports
Select-String -Path "docs/sprints/**/*.md" -Pattern "Status: Open"

# Verify prompt consistency (workbench)
powershell -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"

# Memory Bank history
git log --oneline -- memory-bank/

# Last update of activeContext.md
git log --oneline -3 -- memory-bank/activeContext.md
```

---

### 10.5 Warning Signals and Corrective Actions

| Warning Signal | Probable Cause | Corrective Action |
| :--- | :--- | :--- |
| The agent ignores the Memory Bank | `.clinerules` absent or misplaced | Verify that `.clinerules` is at the root, reload VS Code |
| The agent hallucinates code | Insufficient context, temperature too high | Read `systemPatterns.md` + `techContext.md` before coding |
| Tests systematically fail | Regression introduced, hallucination | `git bisect` to identify the faulty commit, `git revert` |
| Velocity drops by > 30% | Underestimated complexity, impediments | Immediate retrospective, revise estimates |
| `activeContext.md` is > 48h old | Sessions without Memory Bank update | Memory Bank audit (protocol 9.3) |
| Frequent Git conflicts | Multiple parallel sessions | Always commit before switching sessions |
| Critical bugs accumulate | Insufficient tests, US too broad | Split US, strengthen acceptance criteria |
| Architecture drifts | Undocumented ADRs, obsolete Memory Bank | Architectural review (protocol RA-003) |

---

## Appendix A - Artifacts / Memory Bank / Git Correspondence

| Artifact | File | Commit Format | Persona |
| :--- | :--- | :--- | :--- |
| BRIEF-001 | `docs/brief/BRIEF-001-*.md` | `docs(brief): initial narrative vision` | Product Owner |
| BRIEF-002 | `docs/brief/BRIEF-002-*.md` | `docs(brief): structured synthesis` | Developer |
| BRIEF-003 | `docs/brief/BRIEF-003-*.md` | `docs(brief): launch decision [GO/NO-GO]` | Product Owner |
| PRJ-001 | `memory-bank/projectBrief.md` | `feat(memory): projectBrief initialization` | Product Owner |
| PRJ-002 | `docs/architecture/PRJ-002-*.md` | `feat(architecture): initial architecture` | Developer |
| PRJ-003 | `docs/backlog/PRJ-003-*.md` | `feat(backlog): initial MoSCoW backlog` | Product Owner |
| SPR-NNN-001 | `docs/sprints/sprint-NNN/SPR-NNN-001-*.md` | `feat(sprint-NNN): sprint planning` | Product Owner |
| SPR-NNN-004 | `docs/sprints/sprint-NNN/SPR-NNN-004-*.md` | `test(sprint-NNN): test report` | QA Engineer |
| SPR-NNN-005 | `docs/sprints/sprint-NNN/SPR-NNN-005-*.md` | `docs(sprint-NNN): sprint review` | Product Owner |
| SPR-NNN-006 | `docs/sprints/sprint-NNN/SPR-NNN-006-*.md` | `docs(sprint-NNN): retrospective` | Scrum Master |
| REL-VER-001 | `docs/releases/REL-VER-001-*.md` | `docs(release): release notes vVER` | Developer |
| ADR-NNN | `memory-bank/decisionLog.md` | `docs(memory): ADR-NNN [title]` | Developer |

---

## Appendix B - Process Glossary

| Term | Definition |
| :--- | :--- |
| **Artifact** | Document produced by the Agile process. Each artifact has a unique ID, a template, a responsible persona and a defined location in the project structure. |
| **Open Upstream** | Phase 0 of the process. Accepts unstructured inputs (emails, notes, existing code) and progressively transforms them into structured artifacts via BRIEF-001, BRIEF-002, BRIEF-003. |
| **Progressive Convergence** | Principle by which raw narrative inputs (Phase 0) mature toward increasingly structured artifacts (Phase 1, Phase 2) without forcing a premature structure. |
| **Defense in Depth** | Agentic security principle: each critical rule is inscribed at multiple levels (`.clinerules`, `roleDefinition`, session protocols) so that it is respected even if one level is ignored. |
| **Epic** | Functional grouping of User Stories sharing a common business objective. An Epic can span multiple sprints. |
| **Hallucination** | Behavior of an LLM that generates plausible but incorrect content (invented code, non-existent API, fictional architecture). Main countermeasure: temperature 0.15 + mandatory QA tests. |
| **Impediment** | Obstacle that prevents the team from progressing. Identified by the Scrum Master in the Retrospective. Must have a documented resolution plan. |
| **MoSCoW** | Prioritization method: Must (mandatory), Should (important), Could (desirable), Won't (out of scope). Used for the initial backlog (PRJ-003). |
| **Context Loss** | Agentic risk RA-001. An LLM has no memory between two sessions. The Memory Bank is the main countermeasure mechanism. |
| **Session Protocol** | Sequence of mandatory actions at the start and closure of each Roo Code session. Guarantees context continuity between sessions. |
| **Silent Regression** | Bug introduced by a modification that breaks an existing feature without being immediately detected. Countermeasure: QA tests after each US. |
| **Sprint Goal** | One-sentence sprint objective. Defines what the team commits to deliver. Written in SPR-NNN-001 and in `activeContext.md`. |
| **T-shirt Sizing** | Complexity estimation method: XS (< 1h), S (1-4h), M (4-8h), L (1-3d), XL (> 3d). Used for the initial backlog. |
| **User Story** | Description of a feature from the user's perspective. Format: "As a [persona], I want [action] so that [benefit]". Identified by US-NNN. |
| **Velocity** | Number of points delivered per sprint. Indicator of team capacity. Calculated in SPR-NNN-005. |

---

## Appendix C - References Table

| Ref. | Type | Title / Identifier | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Internal document | `workbench/DOC1-PRD-Workbench-Requirements.md` | Workbench requirements - REQ-xxx referenced in this document |
| [DOC2] | Internal document | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Workbench technical architecture - DA-xxx referenced |
| [DOC3] | Internal document | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Workbench installation plan (Phases 0-12) |
| [DOC4] | Internal document | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Workbench deployment guide on projects |
| [DOC5] | Internal document | `workbench/DOC5-GUIDE-Project-Development-Process.md` | This document - Application Agile process manual |
| [SCRUM] | Standard | Scrum Guide (scrumguides.org) | Official Scrum Guide - reference for ceremonies and roles |
| [MOSCOW] | Method | MoSCoW Prioritization | Must/Should/Could/Won't prioritization method |
| [ADR] | Pattern | Architecture Decision Records (adr.github.io) | Standard format for documenting architecture decisions |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | MAJOR.MINOR.PATCH convention for releases |
| [CONVCOMMITS] | Standard | Conventional Commits (conventionalcommits.org) | Commit message convention: type(scope): description |
| [MEMORY-BANK] | Workbench Component | `memory-bank/` (7 .md files) | Persistent memory system - main countermeasure RA-001 |
| [CLINERULES] | Workbench Component | `.clinerules` (6 mandatory rules) | Session directives - RULE 1 to RULE 6 |
| [ROOMODES] | Workbench Component | `.roomodes` (4 Agile personas) | Personas Product Owner, Scrum Master, Developer, QA Engineer |
