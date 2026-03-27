Here is the complete, detailed restructuring of your Agentic Agile Workbench architecture. The content has been logically consolidated so that all deep dives, artifacts, and system prompts are grouped within their respective phases. No details have been summarized or omitted.

---

# The Agentic Agile Workbench: Complete Architecture

Here is the detailed, step-by-step mapping of this hybrid system, which combines the thinking power of the Asynchronous Factory with the execution rigor of the local Workbench. This modeling clearly separates the upstream (work preparation) from the downstream (code execution).



## Part 1: The Greenfield Pipeline (From Idea to Code)

### Phase 1: Ingestion, Scoping, and Ideation (The Business Spark)
The goal is to freeze the human intention before launching the machine. This phase is a true "Synchronous Ideation Workshop", responding exactly to the vision of a rich, demanding exchange purely oriented towards "Business". It forces the human to give birth to a perfect, exhaustive vision devoid of any technical bias, through maieutics and confrontation.

* **Actor(s):** Human (Product Manager or Sponsor) facing the Lead PM Agent (AI Orchestrator) and a dynamic swarm of Senior AI Agents (e.g., UX Researcher, Legal Expert, Domain Expert).
* **Environment & Mode:** Local (Your machine) -> Cloud. Rich conversational interface (Advanced chatbot or real-time voice interface). Synchronous, highly interactive, and iterative process.
* **Input Artifacts:** The human's raw idea, mental draft, or initial pitch.
* **Detailed Action (The Cycle):**
    1.  **The Spark & The Casting:** The human submits their initial idea. The system analyzes the domain and instantly "recruits" the relevant agents.
    2.  **The Interrogation (The Challenge):** At a rapid pace, the agents question the human to hunt down blind spots.
    3.  **The Anti-Technical Guardrail:** If the human attempts to steer the "How", the Lead PM immediately realigns them to the fundamental user need.
    4.  **Iterative Atomization:** As the human answers, the agents structure the thought live, breaking down ideas into strict user journeys and atomic business rules.
* **Output Artifacts:**
    * The `projectBrief.md` (The Constitution): Automatically generated at the end, summarizing the essence of the project (Elevator Pitch, KPIs, mission).
    * The PRD payload ready to be sent to the API.
* **Passing Criterion (Scope Lock Gate):** The Lead PM Agent presents the final PRD. The human reads it and gives their formal validation (Approval). The business scope is then "frozen", the human system can disconnect, and the PRD is shipped to Phase 2.

#### The Ideation Memory Bank (Long Term Storage)
To immunize this phase against LLM amnesia and hallucinations, the synchronous exchange is anchored in a persistent local file system (e.g., `/ideation_board/`). At the beginning of each session, the Lead PM Agent has the obligation to read these files before speaking.

1.  `ideation_state.md` (The Resumption Marker): Contains the exact summary of the last exchange, pending questions, and the objective of the current session.
2.  `draft_prd.md` (The Business Deliverable): The central working document. The PRD under construction, updated silently in the background.
3.  `domain_lexicon.md` (The Dictionary): The business dictionary ensuring semantic alignment.
4.  `tech_parking_lot.md` (The Technical Dump): Stores the human's implementation proposals to reassure them, but excludes them from the business PRD.

#### Phase 1 System Prompt: The Lead PM Agent
> **ROLE AND MISSION**
> You are the Lead Product Manager Agent. You facilitate a demanding business ideation workshop with the Human Sponsor. Your mission is to extract, challenge, and structure the business need to build an atomic and exhaustive Product Requirements Document (PRD). You act as the orchestrator of a "Business Board" of AI experts.
>
> **RULES OF CONDUCT (GUARDRAILS)**
> * **Zero Technical (Anti-Solutioning):** The PRD must only contain the "What" and the "Why". If the human proposes a "How", isolate it politely in the `tech_parking_lot.md` and refocus on the functional need.
> * **Only One Question at a Time:** Never overwhelm the human. Always end your turn to speak with a single, incisive, closed, or restricted-choice question to advance the decision.
> * **The Socratic Pace:** Be direct, professional, and fast. Use maieutics to reveal blind spots, edge cases, and contradictions.
> * **Call to Experts:** If the discussion touches on a specific domain, virtually bring in an expert from your "Board" to ask a pointed question, but keep the role of primary moderator.
>
> **MEMORY MANAGEMENT PROCESS (MANDATORY CYCLE)**
> At each session start or subject change, you must STRICTLY:
> * **READ:** Check the state in `ideation_state.md` and the vocabulary in `domain_lexicon.md`.
> * **ANALYZE:** Compare the human's response with the current content of `draft_prd.md`.
> * **WRITE:** Silently update the local files before answering the human.
>
> **COMMUNICATION STYLE**
> Your tone is empathetic but clinical. You value the human's contribution, but you are ruthless on logical clarity.

#### Phase 1 Artifact Templates

**File 1: `draft_prd.md`**
```markdown
# Product Requirements Document (PRD) - [Project Name]
## 1. Vision and Objectives
* **Problem to solve:** [Clear description of the pain point]
* **Value proposition:** [What the product brings that is unique]
* **KPIs (Success Criteria):** [Objective measures of success]
## 2. User Personas
### Persona 1: [Name/Role]
* **Primary Objective:** [What they want to accomplish]
* **Current frustrations:** [What is blocking them today]
* **Context of use:** [When and how they use the product]
## 3. User Journeys
### Journey: [Journey Name]
* **Trigger:** [The event that launches the journey]
* **Business steps:**
  1. [User action] -> [Business consequence]
  2. [User action] -> [Business consequence]
* **Nominal outcome (Success):** [The expected final state]
## 4. Business Rules and Edge Cases
### Rule: [Rule Name]
* **Description:** [The strict business constraint]
* **Behavior in case of failure:** [What the system must signify]
```

**File 2: `ideation_state.md`**
```markdown
# Ideation State
## Session Status
* **Last update:** [Date]
* **Current subject:** [Ex: Definition of Persona 1]
* **Next question to ask the human:** [The pending question]
## Open points (To be addressed later)
* [Friction point or business question requiring reflection]
```

**File 3: `domain_lexicon.md`**
```markdown
# Business Lexicon
This document guarantees semantic alignment. Each term must be used accurately by the system and the human.
* **[Term 1, ex: Subscriber]:** [Exact definition, ex: User with an active SEPA direct debit mandate].
* **[Term 2]:** [Definition]
```

**File 4: `tech_parking_lot.md`**
```markdown
# Technical Parking
This document stores the human's implementation proposals so as not to lose them, while keeping the PRD strictly focused on business.
* **[Date] - Proposal:** [Ex: Use PostgreSQL for the database]
  * **Underlying business need:** [Ex: Need for complex queries and relational persistence]
```

---

### Phase 2: The Committee of Experts (The Analytical Burst)
The goal is to explore all technical dimensions of the business need at a lower cost. In this asynchronous process, we must abandon the notion of "free text" and treat LLMs as deterministic functions.

* **Actor(s):** Specialized AI Agents (Architecture Agent, Security Agent, UX/UI Agent, QA Agent).
* **Environment & Mode:** Cloud (via Batch API). Asynchronous and strictly Parallel Process.
* **Input Artifacts:** The PRD (`draft_prd.md`) from Phase 1, the Lexicon (`domain_lexicon.md`), and optionally the `tech_parking_lot.md`.
* **Detailed Action:** Each agent awakens independently. It reads the PRD and generates an exhaustive list of constraints, risks, and specifications related solely to its area of expertise. They do not communicate with each other at this stage.
* **Output Artifacts:** A multitude of raw expert reports containing directives that are often redundant or contradictory.
* **Passing Criterion (Gate):** The Batch Cloud manager confirms that 100% of the agents have finished their execution and returned their report. Schema Parsing validates that each response matches the expected JSON schema.

#### Batch Environment Setup
* **Mandatory Output Format:** JSON Mode or Structured Outputs. The agents must not generate any introductory or concluding text.
* **Temperature:** Fixed between 0.1 and 0.2. (Zero creative hallucination; cold, logical deduction).
* **Top-P:** Fixed at 0.1.
* **Context Window:** Maximum. The complete PRD and lexicon must be injected entirely into each request.

#### Anatomy of the System Prompts (Scoping the Experts)
* **The Architecture Agent (The Builder):**
    * *Mission:* Deduce the system components, databases, and information flows necessary to support the PRD.
    * *Negative Constraint:* Do not invent any business functionality. Do not propose a graphical interface.
    * *Analysis Target:* Data volume, concurrency, persistence, third-party integrations.
* **The Security Agent (The Paranoid):**
    * *Mission:* Identify all attack surfaces, sensitive data (PII), and compliance requirements induced by the PRD's user journeys.
    * *Negative Constraint:* Do not choose the database. Do not worry about the user experience.
    * *Analysis Target:* Authentication, authorization, encryption, audit trails.
* **The UX/UI Agent (The Empathetic):**
    * *Mission:* Translate the business journeys into concrete interface states and accessibility constraints.
    * *Negative Constraint:* Do not design screens. Do not choose the front-end framework.
    * *Analysis Target:* Perceived loading times, empty state management, visual error feedback, accessibility.
* **The QA Agent (The Destroyer):**
    * *Mission:* Find all logical flaws in the PRD's business rules and anticipate edge cases.
    * *Negative Constraint:* Do not propose an architectural solution.
    * *Analysis Target:* Concurrency of user actions, network interruptions, absurd data inputs, size limits.

#### The Output Contract (The JSON Schema)
| JSON Key | Type | Description |
| :--- | :--- | :--- |
| `domain` | String | The agent's domain (e.g., "Security", "Architecture"). |
| `identified_risks` | Array | List of major technical risks deduced from the PRD. |
| `technical_constraints` | Array | Absolute technical requirements (e.g., "Obligation to encrypt column X"). |
| `proposed_entities` | Array | Data models or necessary components. |
| `edge_cases` | Array | Special cases requiring specific management in the code. |

---

### Phase 3: Synthesis and BDD Translation (The Convergence)
The goal is to transform the chaos of the expert reports into an ordered and testable action plan. The Synthesizer must not act as a "writer", but as a logical compiler.

* **Actor(s):** Synthesizer AI Agent.
* **Environment & Mode:** Cloud (Batch API). Asynchronous Process.
* **Model Setup:** Temperature 0.0 to 0.1. Strict JSON Mode output.
* **Input Artifacts:** The PRD (`draft_prd.md`), the current state of the architecture (`systemPatterns.md`), and the 4 raw JSON expert reports from Phase 2.
* **Detailed Action:** The Synthesizer ingests all reports. It applies a "Priority Matrix" to settle conflicts. It deduplicates requests and breaks the whole down into atomic tasks. Above all, it translates each task into Gherkin syntax (Given-When-Then).
* **Output Artifacts:** A first draft of the technical backlog (`draft_backlog.json`). Proposals for updating the global architecture.
* **Passing Criterion (Gate):** Schema validation (perfect JSON structure with all keys present) and Gherkin Linter (strict adherence to Given/When/Then grammar). Each task must imperatively have an automated testing target (TDD Target).



#### The Priority Matrix (The Arbitration Engine)
| Level | Area of Expertise | Arbitration Rule in case of conflict |
| :--- | :--- | :--- |
| **P0 (Blocking)** | Security & Compliance | Prevails over everything. Any feature violating security is amputated, modified, or rejected. |
| **P1 (Structural)** | Architecture | Prevails over QA and UX. Must integrate into `systemPatterns.md` without technical debt. |
| **P2 (Robustness)** | QA (Quality Assurance) | Prevails over UX. Error and edge case management prioritized over happy path fluidity. |
| **P3 (Interface)** | UX/UI | Applies only if P0, P1, and P2 are respected. |

#### The Output Contract (The Draft Backlog Anatomy)
| JSON Key | Type | Description |
| :--- | :--- | :--- |
| `task_id` | String | Unique generated identifier. |
| `business_origin` | String | Direct reference to the PRD's business journey or rule (Traceability). |
| `arbitration_notes` | Array | Brief explanation if the agent had to override a UX or QA request. |
| `bdd_scenario` | String | The expected behavior in pure Gherkin syntax (Given, When, Then). |
| `tdd_target` | String | The explicit instruction for the future coding agent. |

---

### Phase 4: The Devil's Advocate (The Feasibility Filter)
The goal is to guarantee that the tests imagined by the Synthesizer are actually codable in your environment. This is the true "crash test" of the Asynchronous Factory.

* **Actor(s):** Devil's Advocate AI Agent versus Synthesizer AI Agent.
* **Environment & Mode:** Cloud. Asynchronous Process (Internal debate micro-loop).
* **Input Artifacts:** The draft backlog (`draft_backlog.json`) from Phase 3, and the "Book of Laws" (`systemPatterns.md`).
* **Detailed Action:** The Devil's Advocate reads the draft backlog and attempts to destroy each proposed test using the "Book of Laws".
    1.  **The Attack:** It detects a violation (e.g., impossible to test real network timeout in CI) and sends it back with a `rejection_reason`.
    2.  **The Defense:** The Synthesizer modifies the test to integrate the constraint and resubmits it.
    3.  **Graceful Degradation:** The Synthesizer is allowed a limited number of attempts (e.g., 2). If it fails, the Devil's Advocate isolates the problem with an escalation flag.
* **Output Artifacts:** The final Backlog (`final_backlog.json`), split into two categories: "Green Tickets" (perfect) and "Orange Tickets" (dead ends).
* **Passing Criterion (Gate):** 100% of tickets have a final status (Green or Orange). No Green ticket has an empty `tdd_target`. The Asynchronous Factory stops.

#### The Output Contract (The Classified Backlog)
| JSON Key | Type | Description |
| :--- | :--- | :--- |
| `task_id` | String | Conserved unique identifier. |
| `status` | String | "GREEN" (Ready for coding agent) or "ORANGE" (Requires a human). |
| `human_escalation_reason` | String | (Only if ORANGE). The exact explanation of the failure to save human time. |
| `bdd_scenario` | String | The validated or corrected behavior. |
| `tdd_target` | String | The technical objective, purged of hallucination, ready to be coded. |
| `architectural_boundaries` | Array | The specific "Laws" that the coding agent will have to respect for this precise ticket. |

---

### Phase 5: Triage (The Human Gate - Human-in-the-Loop)
The flow now descends back to your local machine (the Workbench). The goal is to use human intelligence only where the machine has failed, to unblock the system.

* **Actor(s):** Local Agent (Scrum Master Agent - SP-004) and Human (Lead Tech or Product Owner).
* **Environment & Mode:** Local (In the VS Code interface / Workbench). Synchronous Process.
* **Input Artifacts:** The classified Backlog (`final_backlog.json`) from Phase 4.
* **Detailed Action:** The human receives a notification and ignores the Green Tickets. They open the Orange Tickets (via a dashboard) to read the reason for the dead end. The human arbitrates using one of three options:
    * **Option A: Business Concession:** Modify the `productContext.md` acceptance criteria.
    * **Option B: Architectural Update:** Accept the architectural cost, update `systemPatterns.md`, and log the decision in `decisionLog.md`.
    * **Option C: Manual Exemption:** Force the ticket to GREEN with manual boundaries.
* **Output Artifacts:** The definitive update of the Workbench: `productContext.md` is populated with the clean backlog, and `systemPatterns.md` is updated.
* **Passing Criterion (Gate):** Zero Orange Tickets remain. The human validates the batch is ready. Prompts synchronization ensures local agents have read the latest `systemPatterns.md`.

#### The Anatomy of a Dead End (What the human reads)
* **Business Origin:** "The PRD requires that the user be instantly disconnected on all their devices if they change their password."
* **The Blockage:** "Violation of Rule P1 (Architecture): The current system uses stateless JWTs... Global instant disconnection is technically impossible without major refactoring."
* **The Choice:** 1. Relax the business. 2. Modify the architecture.

---

### Phase 6: TDD Execution (The Development Micro-Cycle)
The major challenge of this phase is tunnel vision. The Developer Agent only has access to an ultra-restricted context to prevent hallucinating global refactorings.



* **Actor(s):** Developer AI Agent (SP-005) and QA AI Agent (SP-006).
* **Environment & Mode:** Local (Interactive VS Code with Gemini Proxy). Synchronous and iterative Process (Fast loops: Red-Green-Refactor).
* **Input Artifacts:** The structured Green Ticket (from `productContext.md`), extracted into the `activeContext.md` file.
* **Detailed Action:** The system extracts a Green Ticket. Its metadata overwrites the `activeContext.md`. The Agent runs the test (Red), writes the code (Green), and refactors, monitored by the QA Agent.
* **Output Artifacts:** Modified source code files. Validated tests.
* **Passing Criterion (Gate):** The interpreter/compiler returns a success. The system updates `progress.md` and `decisionLog.md`, empties `activeContext.md`, and moves to the next ticket.

#### Anatomy of the Green Ticket (The Execution Contract)
1.  **Dependencies:** Context of the Existing.
2.  **BDD Scenarios:** The Behavioral Contract (Given-When-Then).
3.  **TDD Target:** The Test Objective.
4.  **Architectural Boundaries:** The Local Laws.
5.  **Scope Restriction:** The Modification Perimeter.

#### Implementation: Preparing the Active Context File

*As per your request to separate execution commands from file content during implementation:*

Execute the following command in your terminal to create/open the file:
```bash
nano activeContext.md
```

Once the file is open, paste the following canonical template:
```markdown
# Active Context: Ticket [TICKET-ID]
## 1. Action Scope (Scope Restriction)
**Allowed files for read/write:**
* `src/controllers/authController.ts`
* `tests/authController.test.ts`
* `src/types/auth.d.ts`
*(Do not modify any other file without escalation)*
## 2. Architectural Boundaries
* **Prohibition:** Do not modify the global validation middleware.
* **Constraint:** Use the existing standard hashing function in `src/utils/crypto.ts`.
## 3. Dependencies and Initial State
* The `findUserByEmail` function already exists in `src/models/userModel.ts`.
* The test database is blank at each iteration.
## 4. TDD Target
1. Create the file `authController.test.ts` if it does not exist.
2. Write an integration test that calls the `/api/auth/reset` route with a non-existent email.
3. Assert that the HTTP return is `200 OK` (to prevent User Enumeration) but that no email is sent.
## 5. BDD Contract (Gherkin)
```gherkin
Feature: Secure password reset
  Scenario: Request with an email unknown to the system
    Given the database contains no user with the email "unknown@domain.com"
    When the user submits a reset request for "unknown@domain.com"
    Then the system returns a success status
    And no email is dispatched
    And a security alert log "Reset attempt - Unknown email" is recorded
```

---

## Part 2: The Brownfield Workflow (Reverse Engineering Spaghetti Code)



To transition from a "Greenfield" project to working with existing code, the process is adapted to perform Reverse Engineering and safe refactoring.

### Inverted Phase 1: PRD Extraction (From Code to Business)
* **The Preliminary Action:** An Analyst Agent reads your entire source code and writes a first descriptive draft of the user journeys and rules (`draft_prd_brut.md`).
* **The Synchronous Workshop (The Debate):** The Lead PM Agent questions you to arbitrate between a genuine business intention and a failing technical implementation (technical debt/bugs).
* **The Result:** A pure and validated Business PRD describing what the application *should* do, stripped of technical slag.

#### Implementation: Preparing the Analyst Agent Prompt

*As per your request to separate execution commands:*

Execute the following command to create the prompt file:
```bash
nano prompt_agent_analyste.md
```

Paste the exact content below into the file:
```markdown
ROLE AND MISSION
You are the Analyst Agent (Reverse-Engineer). Your mission is to audit an undocumented codebase ("spaghetti code") to extract the functional intention. You must perform reverse engineering to deduce business rules, user journeys, and personas from the existing functions. Your deliverable is a PRD draft (draft_prd_brut.md).

RULES OF CONDUCT (GUARDRAILS)
Technical Abstraction: You must translate what the code does into business language. If you see an SQL query with a complex join on an Orders and Users table, do not describe the query. Describe the rule: "A user can consult the detailed history of their orders".
Identification of Ambiguities: Legacy code contains bugs and workarounds. If you see illogical logic or erratic behavior (e.g., a forced timeout at 10 seconds for no apparent reason), clearly mark it with the tag [BUSINESS AMBIGUITY] so that the human and the Lead PM can arbitrate later.
Ignore Dead Code: If you identify functions that are never called or obsolete files, do not include them in your functional analysis.

DELIVERABLE STRUCTURE (draft_prd_brut.md)
You must format your analysis strictly adhering to these three sections:
Deduced Personas: List the types of users identified via the role or authentication systems.
Deduced Journeys (User Journeys): The major flows of actions (e.g., "Payment process", "Account creation").
Observed Business Rules: The strict constraints hardcoded (e.g., "Password requires 8 characters", "An order under €10 is refused").

COMMUNICATION STYLE
Be factual, descriptive, and neutral. Do not judge the code quality. Limit yourself to exposing what the code accomplishes from the end user's point of view.
```

### Adapted Phase 2: Architectural Audit and Target
* **Gap Analysis:** Architecture and Security Agents compare current code with the validated PRD.
* **Mapping the Existing:** They document the current state (`current_techContext.md`), noting tight coupling, flaws, and lack of tests.
* **Target Definition:** Architecture Agent writes the new `systemPatterns.md`.

### Adapted Phase 3 and 4: The Transition Backlog
* **Characterization Tests:** The Synthesizer creates tickets to "add tests on the existing" to freeze current behavior.
* **Refactoring Slicing:** Once coverage is assured, it creates atomic refactoring tickets.
* **The Devil's Advocate Filter:** Ensures refactoring steps can be executed one by one without making the application unavailable.

### Phase 5 and 6: Surgical Execution (Refactoring Micro-Cycle)
* **Test:** Run characterization tests to prove old code still works.
* **Refactor:** Modify code structure within the restricted perimeter to achieve modularity.
* **Verify:** Rerun the tests to confirm business behavior is intact.

---

## Part 3: Industry Validation & Tooling Context

This architecture reconstructs the state of the art in agentic software engineering (circa early 2026).

### 1. The "Memory Bank" and the Local Workbench
* **Reference:** The "Roo Code Memory Bank" (or "Cline Memory Bank") model.
* **Similarity:** LLMs become amnesiac. This system forces the AI to read Markdown files at the start of tasks and update `progress.md` and `decisionLog.md` at the end. (Implementations found under `roo-code-memory-bank`).

### 2. The Committee of Experts and the Asynchronous Factory
* **ALMAS:** Autonomous LLM-based Multi-Agent Software Engineering orchestrates coding agents aligned with agile roles.
* **Orchestration Engines (LangGraph & CrewAI):** Allow creation of execution graphs where agents pass strict JSON objects with conditional validation loops.

### 3. BDD/TDD Convergence
* **Concept:** "Three Amigos with AI". AI generates an exhaustive BDD contract forcing TDD, literally playing QA Challenger to find flaws before writing code.

### 4. The Global Methodology: BMAD
* **Similarity:** Breakthrough Method of Agile AI-Driven Development advocates an asynchronous "Upstream" phase (PRD/Architecture in Git) and a "Downstream" execution phase (isolated tasks without architectural decision power).

---

## Part 4: The MCP Ecosystem and 3-Tier Architecture

To securely connect these elements and bypass limits like rapid saturation of the context window (GAP-001/GAP-002), the Model Context Protocol (MCP) standard is utilized.

### MCP Server Recommendations
1.  **Context Management (Replacing "Memory Bank"):** `mcp-server-memory`, Chroma MCP, or Mem0 MCP Server. Introduces persistent memory/RAG, eliminating context explosion.
2.  **Git Operations:** `github-mcp-server` or `mcp-server-git`. For safe, structured manipulation.
3.  **Agile Management:** Notion, Jira, Linear, or Slack MCP servers to outsource Sprint artifacts.
4.  **Architecture:** `mermaid-mcp-server` or `excalidraw-architect-mcp` for deterministic diagrams.
5.  **Database Explorer (Ground Truth):** `postgres`, `sqlite`, or `crystaldba/postgres-mcp` for read-only schema inspection and query planning.
6.  **Semantic Code Parser:** Sourcegraph (Cody MCP) or Tree-sitter AST parsers. Crucial for the Analyst Agent to read code semantics without blowing up token limits.
7.  **Test Executor:** `mcp-server-jest`, `mcp-server-pytest`, or `puppeteer` for execution sandboxing.

### The Hybrid Cognitive Architecture
This design separates Hot Memory (working) and Cold Memory (semantic):
* **Hot Perimeter:** The agent loads only files necessary for its immediate task (e.g., via Roo Code Memory Bank MCP).
* **Cold Perimeter:** Archived files leave working memory and are indexed by a Semantic MCP Server (Vector database/RAG).
* **Transparency:** The RAG only ingests textual archive Markdown files, guaranteeing the human retains total mastery and traceability.

### The 3-Tier Architecture (Calypso Integration)



Given hardware constraints (e.g., an RTX 5060 Ti 16GB cannot run 5 frontier models locally), the pipeline is distributed:

* **Tier 1: Your Local Workstation (Interface & Execution)**
    * *Tool:* VS Code with Roo Code / Cline.
    * *Role:* Host the Memory Bank, conduct ideation (Phase 1), execute Green Tickets (Phase 6).
* **Tier 2: Calypso (Orchestrator / Router)**
    * *Role:* Orchestration server. Prepares prompts, manages the Devil's Advocate loop. Uses its 16GB VRAM to run fast routing/validation models (e.g., Llama-4 8B) or manage vectorization.
    * *Custom FastMCP Server:* Exposes tools like `launch_factory(prd_path)`, `check_batch_status(job_id)`, and `retrieve_backlog(job_id)` to your local IDE.
* **Tier 3: The Cloud (Cognitive Engine)**
    * *Tool:* Anthropic API (Claude 4.6 Sonnet via Batch API).
    * *Role:* Produce raw intelligence, processing the complex JSON requests.

**Benefits:** Secures API keys on Calypso, enables true asynchronous processing, and drastically reduces API costs by leveraging Batch pricing.

---

Would you like me to guide you through creating the `mcp.json` configuration file to officially link your first three local servers (Memory Bank, Postgres, and AST Parser) to your IDE?