# Document 4: Workbench Deployment Guide
## How to use this template on a new project or an existing codebase

**Project Name:** Agentic Agile Workbench
**Version:** 1.0
**Date:** 2026-03-23
**References:** DOC1-PRD-Workbench-Requirements.md v2.0, DOC2-ARCH-Workbench-Technical-Design.md v2.0, DOC3-BUILD-Workbench-Assembly-Phases.md v3.0

---

## 1. Understanding What This Repository Is (and Is Not)

### 1.1 This Repository = The Workbench, Not the Product

The most important distinction to understand before any deployment:

```
agentic-agile-workbench/   ← YOU ARE HERE
│                                     This is the WORKBENCH
│
│  workbench/          ← The workbench blueprints (DOC1, DOC2, DOC3, DOC4)
│  prompts/        ← The workbench tools (system prompts SP-001 to SP-007)
│  proxy.py        ← A workbench machine (Roo Code <-> Gemini Chrome bridge)
│  .roomodes       ← The workbench worker roles (4 Agile personas)
│  .clinerules     ← The workbench rulebook (6 mandatory rules)
│  scripts/        ← The workbench utility scripts
│
└── It produces PROJECTS (separate repositories, in other folders)
```

**This repository contains no application code.** It contains the rules, tools, processes and system prompts that enable developing any project in an agentic, agile and versioned manner.

**Analogy:** Think of it as a carpentry workshop. The workshop contains the tools (saws, planes, hammers), workbenches, and safety rules. The furniture produced (the projects) are separate entities that leave the workshop once completed.

### 1.2 What This Repository Contains

| File / Folder | Role in the Workbench | Analogy |
| :--- | :--- | :--- |
| `workbench/DOC1-PRD-*.md` | Requirements of the workbench itself | Workbench manual |
| `workbench/DOC2-Architecture-*.md` | Technical architecture of the workbench | Machine blueprints |
| `workbench/DOC3-Plan-Implementation-*.md` | Workbench installation guide | Assembly instructions |
| `workbench/DOC4-Guide-Deploiement-*.md` | This document — how to use the workbench | User manual |
| `template/prompts/SP-001 to SP-007` | Canonical system prompts | Worker job descriptions |
| `.roomodes` | Definition of the 4 Agile personas | Workbench org chart |
| `.clinerules` | 6 mandatory rules for all modes | Internal regulations |
| `template/proxy.py` | Roo Code ↔ Gemini Chrome bridge | Relay machine |
| `scripts/` | Utility scripts | Automated tools |

### 1.3 What This Repository Does NOT Contain

- ❌ Your application source code (that lives in the project repository)
- ❌ Your project's Memory Bank (that lives in the project repository)
- ❌ Your project's QA reports (that lives in the project repository)
- ❌ Your project's User Stories (that lives in the project's Memory Bank)

### 1.4 Why Version This Repository?

This repository will evolve over time. You will update it when:
- A `.clinerules` rule proves insufficient or ambiguous → you fix it here
- You add a new persona (e.g.: DevOps Engineer, Architect) → you add it in `.roomodes` and `prompts/`
- You improve `template/proxy.py` (new timeout, better error handling) → you update it here
- You discover a more effective Memory Bank pattern → you update the templates in `.clinerules`

**Every workbench improvement benefits all future projects.** That is the value of separating the workbench from the projects.

---

## 2. Overview: Workbench vs Projects

```
┌─────────────────────────────────────────────────────────────────┐
│                    le workbench WORKBENCH (this repository)     │
│                                                                  │
│  .roomodes  .clinerules  prompts/  proxy.py  scripts/  workbench/   │
│                                                                  │
│  Versioned, enriched, shared across all projects                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Deployment (file copy)
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
┌─────────────────────┐   ┌─────────────────────────────────────┐
│   NEW PROJECT       │   │   EXISTING PROJECT (spaghetti code) │
│                     │   │                                     │
│  my-new-project/    │   │  my-legacy-project/                 │
│  ├── .roomodes      │   │  ├── src/  (existing code)          │
│  ├── .clinerules    │   │  ├── .roomodes  (added)             │
│  ├── proxy.py       │   │  ├── .clinerules  (added)           │
│  ├── prompts/       │   │  ├── proxy.py  (added)              │
│  ├── memory-bank/   │   │  ├── prompts/  (added)              │
│  │   (empty → filled)│  │  ├── memory-bank/  (audit first)    │
│  └── src/  (to create)│  │  └── docs/qa/  (added)            │
└─────────────────────┘   └─────────────────────────────────────┘
```

---

## 3. Deployment on a New Project

### 3.1 Prerequisites

Before starting, the workbench must be installed and functional on your machine (phases 0-12 of DOC3). In particular:
- Ollama with `uadf-agent` available (Mode 1) OR proxy.py started (Mode 2) OR Anthropic key configured (Mode 3)
- VS Code with the Roo Code extension installed

### 3.2 Step 1 — Create the New Project Repository

```powershell
# Canonical structure:
# $env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\
# ├── agentic-agile-workbench\   ← THE WORKBENCH (master template, do not modify)
# └── PROJECTS\                  ← All application projects
#     └── my-new-project\

$Atelier = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench"
$Projet  = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-new-project"

# Create the new project folder (under PROJECTS\, separate from the workbench)
New-Item -Path $Projet -ItemType Directory -Force
cd $Projet

# Initialize Git
git init
git branch -M main
```

> **Important:** The new project is a Git repository **separate** from the workbench. The workbench (`agentic-agile-workbench/`) is the **protected master template** — never create a project inside it. All application projects live under `AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\`.

### 3.3 Step 2 — Deploy the Workbench Files

The deployment script automatically copies all necessary files and creates the Memory Bank:

```powershell
# One-command deployment (from anywhere)
$Atelier = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench"
$Projet  = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-new-project"

& "$Atelier\template\scripts\deploy-to-project.ps1" -ProjectPath $Projet
```

The script deploys: `.roomodes`, `.clinerules`, `Modelfile`, `proxy.py`, `requirements.txt`, `prompts/`, `scripts/`, `memory-bank/` (7 empty files), `docs/qa/`.

### 3.4 Step 3 — Create the `.gitignore`

Create `.gitignore` at the project root:

```
# Python environment
venv/
__pycache__/
*.pyc
*.pyo

# API keys — NEVER in Git
.env
*.env

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

### 3.5 Step 4 — Initialize the Memory Bank

> **This step is automated by the `deploy-to-project.ps1` script** (section 3.3). The Memory Bank (7 files) and `docs/qa/` are created automatically. Skip directly to step 5.

If you need to recreate manually:

```powershell
$Projet = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-new-project"

New-Item -Path "$Projet\memory-bank" -ItemType Directory
@("projectBrief.md","productContext.md","systemPatterns.md","techContext.md",
  "activeContext.md","progress.md","decisionLog.md") | ForEach-Object {
    New-Item -Path "$Projet\memory-bank\$_" -ItemType File
}
New-Item -Path "$Projet\docs\qa" -ItemType Directory -Force
New-Item -Path "$Projet\docs\qa\.gitkeep" -ItemType File
```

### 3.6 Step 5 — Fill in `memory-bank/projectBrief.md`

This is **the only mandatory manual step** before opening Roo Code. Open `memory-bank/projectBrief.md` and fill in:

```markdown
# Project Brief

## Project Vision
[2-3 sentences describing what this project does and for whom]

## Main Objectives
1. [Objective 1 — measurable]
2. [Objective 2 — measurable]
3. [Objective 3 — measurable]

## Non-Goals (What this project does NOT do)
- [Non-goal 1 — important to prevent scope creep]
- [Non-goal 2]

## Constraints
- [Technical constraint: e.g.: must run on Python 3.11+]
- [Business constraint: e.g.: must comply with GDPR]

## Stakeholders
- Product Owner: [Your name]
- Target users: [Description of end users]
```

> **Why fill this in manually?** Roo Code cannot invent your project's vision. This is the only information you must provide. Everything else (architecture, code, tests, documentation) will be generated by the agent.

### 3.7 Step 6 — First Commit

```powershell
cd "$Projet"
git add .
git commit -m "chore(init): project initialization with workbench v2.0"
```

### 3.8 Step 7 — Open in VS Code and Start

```powershell
code "$Projet"
```

In VS Code:
1. Select the **"Product Owner"** mode in Roo Code
2. Send: `Read projectBrief.md and create the first User Stories in memory-bank/productContext.md`
3. The agent reads the vision, creates the User Stories, commits automatically

**The workbench is operational on your new project.**

---

## 4. Deployment on an Existing Codebase (Spaghetti Code)

### 4.1 Why It's Different

With a new project, the Memory Bank is empty and fills up progressively. With an existing project, the Memory Bank must be filled **first** — before any refactoring — so the agent understands what it is going to modify.

**Risk without this step:** The agent refactors without understanding the hidden dependencies of the spaghetti code → it breaks existing functionality.

### 4.2 Step 1 — Open the Existing Project

```powershell
# If the legacy project is already in AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\
$Projet = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-legacy-project"
# Otherwise, adapt the path to the current project location
cd $Projet

# If Git is not yet initialized
git init
git add .
git commit -m "chore(init): initial state before le workbench refactoring"
```

> **Committing the initial state is critical.** This creates a safe rollback point if the refactoring goes in the wrong direction.

### 4.3 Step 2 — Copy the Workbench Files

Identical to the "New Project" case (section 3.3):

```powershell
$Atelier = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench"
$Projet  = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-legacy-project"
# (or the current path of the legacy project if different)

& "$Atelier\template\scripts\deploy-to-project.ps1" -ProjectPath $Projet
```

### 4.4 Step 3 — Create the Memory Bank (with existing context)

```powershell
New-Item -Path "$Projet" -Name "memory-bank" -ItemType Directory
# Create the 7 files (identical to section 3.5)
```

### 4.5 Step 4 — Audit the Existing Code (CRITICAL)

This is **the most important step** for an existing project. It does not exist for a new project.

Open VS Code on the project, select the **"Developer"** mode in Roo Code, and send:

```
Perform a complete audit of the source code in this project.
For each point below, document your findings in the indicated file:

1. In memory-bank/projectBrief.md:
   - What is the main function of this project?
   - Who are the apparent target users?
   - What are the visible technical constraints?

2. In memory-bank/systemPatterns.md:
   - What is the folder architecture?
   - What naming conventions are used (even if inconsistent)?
   - What technical patterns are used (even if poorly implemented)?
   - What anti-patterns do you identify? (tight coupling, duplication, etc.)
   - What are the critical dependencies between modules?

3. In memory-bank/techContext.md:
   - What is the language and version?
   - What are the dependencies (requirements.txt, package.json, etc.)?
   - What are the commands to run and test the project?
   - Are there required environment variables?

4. In memory-bank/decisionLog.md:
   - Document the apparent architecture decisions (even implicit ones)
   - Note the identified technical debts

Commit each Memory Bank file as you go.
```

> **Why let the agent do the audit?** The agent reads the code without preconceptions. It identifies the real patterns (not the ones you think you implemented). It documents in a structured and versioned manner. You can correct its conclusions if necessary.

### 4.6 Step 5 — Define the Refactoring Strategy

After the audit, select the **"Product Owner"** mode and send:

```
Read memory-bank/systemPatterns.md and memory-bank/projectBrief.md.
Based on the identified anti-patterns and the project vision,
create the refactoring User Stories in memory-bank/productContext.md.

Each User Story must:
- Address a specific anti-pattern identified in the audit
- Have measurable acceptance criteria
- Be independent of the others (so it can be delivered separately)
- Be ordered by priority (dependencies first)
```

### 4.7 Step 6 — Refactoring Guided by User Stories

Refactoring is done User Story by User Story, in the order defined by the Product Owner:

```
For each User Story:

1. Developer Mode:
   "Implement User Story US-XXX defined in memory-bank/productContext.md.
    Read systemPatterns.md first to respect the target conventions.
    Commit after each significant modification."

2. QA Engineer Mode:
   "Test the changes from User Story US-XXX.
    Write the report in docs/qa/test-US-XXX-[DATE].md."

3. Scrum Master Mode:
   "Update memory-bank/progress.md to mark US-XXX as done.
    Identify any impediments."
```

> **Why User Story by User Story?** Spaghetti code has hidden dependencies. Refactoring in small versioned increments allows detecting regressions immediately and rolling back if necessary (`git revert`).

---

## 5. What Stays in the Workbench vs What Goes in the Project

This table is the reference for knowing where each file should live:

| File / Folder | Stays in Workbench | Goes in Each Project | Notes |
| :--- | :---: | :---: | :--- |
| `workbench/DOC1/DOC2/DOC3/DOC4` | ✅ | ❌ | Workbench documentation — not project documentation |
| `.roomodes` | ✅ (template) | ✅ (copy) | Copied, can be adapted per project |
| `.clinerules` | ✅ (template) | ✅ (copy) | Copied, can be adapted per project |
| `Modelfile` | ✅ (template) | ✅ (copy) | Copied if Ollama Mode is used |
| `template/proxy.py` | ✅ (template) | ✅ (copy) | Copied if Gemini Mode is used |
| `requirements.txt` | ✅ (template) | ✅ (copy) | Copied if Gemini Mode is used |
| `scripts/` | ✅ (template) | ✅ (copy) | Copied to each project |
| `template/prompts/SP-*.md` | ✅ (source of truth) | ✅ (copy) | Copied — the project has its own versioned copy |
| `template/prompts/README.md` | ✅ (template) | ✅ (copy) | Copied |
| `memory-bank/` | ❌ | ✅ (specific) | Unique per project — never copy from one project to another |
| `src/` (application code) | ❌ | ✅ (specific) | Unique per project |
| `docs/qa/` | ❌ | ✅ (specific) | Project-specific QA reports |

### 5.1 Why Copy Files Rather Than Reference Them?

You might think about using Git submodules or symbolic links to avoid duplication. **Do not do this.** Here is why:

- **Independence:** Each project must be able to evolve independently. If you improve `.clinerules` in the workbench, you choose when and whether to update each project.
- **Traceability:** The version of `.clinerules` used in a project is versioned in that project. You know exactly which version of the workbench was active when a bug was introduced.
- **Simplicity:** No inter-repository dependencies to manage. Each project is self-contained.

---

## 6. Dashboard of the 3 LLM Modes by Use Case

| Mode | Recommended Use Case | Advantage | Disadvantage |
| :--- | :--- | :--- | :--- |
| **Mode 1 — Local Ollama** | Daily development, repetitive tasks, simple code | Free, offline, 100% automatic | Slower than Claude, variable quality on complex tasks |
| **Mode 2 — Gemini Proxy** | Complex tasks when Ollama is insufficient, without API budget | Free, high quality | Manual copy-paste required for each request |
| **Mode 3 — Claude API** | Complex refactoring, architecture, critical decisions | Best quality, 100% automatic | Pay per use |

**Practical recommendation:**
- Start in Mode 1 (Ollama) for simple tasks
- Switch to Mode 3 (Claude) for architecture decisions and complex refactoring
- Use Mode 2 (Gemini) as a free alternative to Mode 3 if budget is a constraint

---

## 7. Project Lifecycle with the Workbench

> **Reference:** The complete process (phases, artifacts, nomenclature, agentic anti-risks) is described in **[DOC5] `workbench/DOC5-GUIDE-Project-Development-Process.md`**. This document (DOC4) covers only the workbench deployment. DOC5 covers how to work with the workbench once deployed.

```
PHASE 0 - OPEN UPSTREAM (before coding)
│
├── Collect raw narrative inputs (emails, notes, ideas)
├── Product Owner Mode → BRIEF-001 (raw narrative vision)
├── Developer Mode → BRIEF-002 (structured synthesis)
└── Product Owner Mode → BRIEF-003 (GO/NO-GO decision)
    → See DOC5 Section 2

SETUP / FRAMING PHASE (once per project)
│
├── Copy workbench files (this document — DOC4)
├── Initialize the Memory Bank
├── [If existing] Code audit by the Developer
├── Product Owner Mode → PRJ-001 (projectBrief.md)
├── Developer Mode → PRJ-002 (initial architecture)
├── Product Owner Mode → PRJ-003 (initial MoSCoW backlog)
└── First commit
    → See DOC5 Section 3

DEVELOPMENT PHASE (iterative — one sprint = 1-2 weeks)
│
├── Product Owner Mode → SPR-NNN-001 (Sprint Backlog + Sprint Goal)
│
├── Developer Mode (repeated for each User Story)
│   ├── Read Memory Bank (CHECK→CREATE→READ→ACT)
│   ├── Implement the User Story
│   ├── Update Memory Bank
│   └── Commit (feat(US-XXX): ...)
│
├── QA Engineer Mode → SPR-NNN-004 (Test Report)
│   ├── Test the implementations
│   └── Document the bugs
│
├── Product Owner Mode → SPR-NNN-005 (Sprint Review)
│   └── Validate delivered US, adjust the backlog
│
└── Scrum Master Mode → SPR-NNN-006 (Retrospective)
    ├── Update memory-bank/progress.md
    └── Identify impediments
    → See DOC5 Section 4

MAINTENANCE PHASE (ongoing)
│
├── Bugs → QA Engineer Mode (report) + Developer Mode (fix)
├── New features → Product Owner Mode (US) + Developer Mode (impl)
├── Release → Developer Mode → REL-VER-001/002/003
└── Workbench improvements → Update agentic-agile-workbench/
    → See DOC5 Section 5
```

---

## 8. Frequently Asked Questions

### Q: Do I need to recreate the Gemini Gem for each project?

**No.** The "Roo Code Agent" Gemini Gem is configured once in your Google account. It is generic — it responds to Roo Code requests regardless of the project type. You do not need to recreate it.

### Q: Do I need to reinstall Ollama for each project?

**No.** Ollama is a Windows daemon running in the background. The `uadf-agent` model is compiled once. You only need to ensure Ollama is running (icon in the notification area) before opening Roo Code.

### Q: Can I adapt `.roomodes` for a specific project?

**Yes.** For example, if a project requires a "DevOps Engineer" persona, you can add it in the project's copy of `.roomodes`. The workbench is not modified. If the adaptation is useful for all future projects, you can then port it back to the workbench.

### Q: What to do if the agent does not follow the `.clinerules` rules?

1. Verify that `.clinerules` is at the project root (not in a subfolder)
2. Reload VS Code (`Ctrl+Shift+P` > "Developer: Reload Window")
3. If the problem persists, verify that the rule is formulated imperatively and not suggestively

### Q: How to update a project when the workbench evolves?

1. Identify what changed in the workbench (consult the workbench's `git log`)
2. Manually copy the modified files to the project
3. Commit in the project with an explicit message: `chore(workbench): update workbench v[X.Y] — [description of change]`

### Q: Can I have multiple projects open simultaneously in VS Code?

**Yes**, via VS Code workspaces. Each project has its own `.roomodes` and `.clinerules`. Roo Code reads the files from the project currently open in VS Code.

---

## 9. Deployment Checklist

### For a New Project

- [ ] Git repository created outside the workbench folder
- [ ] Workbench files copied (`.roomodes`, `.clinerules`, `template/proxy.py`, `scripts/`, `prompts/`)
- [ ] `.gitignore` created (venv/, .env, __pycache__, *.log)
- [ ] Memory Bank initialized (7 files created)
- [ ] `memory-bank/projectBrief.md` filled with the project vision
- [ ] `docs/qa/` created with `.gitkeep`
- [ ] First commit done
- [ ] VS Code opened on the new project
- [ ] Product Owner Mode → first User Stories created

### For an Existing Codebase

- [ ] Initial state committed (`git commit -m "chore(init): initial state before le workbench refactoring"`)
- [ ] Workbench files copied (identical to the previous case)
- [ ] Memory Bank initialized (7 files created)
- [ ] `docs/qa/` created with `.gitkeep`
- [ ] **Code audit performed by the Developer** → Memory Bank filled
- [ ] `memory-bank/projectBrief.md` verified and corrected if necessary
- [ ] `memory-bank/systemPatterns.md` contains the identified anti-patterns
- [ ] Refactoring User Stories created by the Product Owner
- [ ] Refactoring started User Story by User Story

---

## Appendix A — References Table

| Ref. | Type | Title / Identifier | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Internal document | `workbench/DOC1-PRD-Workbench-Requirements.md` | Product Requirements Document v2.0 — defines the REQ-xxx requirements of the le workbench system |
| [DOC2] | Internal document | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Architecture, Solution and Technical Stack v2.0 — justifies technical choices |
| [DOC3] | Internal document | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Complete Sequential Implementation Plan v3.0 — workbench installation guide (Phases 0–12) |
| [DOC4] | Internal document | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | This document — Workbench Deployment Guide for new and existing projects |
| [DOC5] | Internal document | `workbench/DOC5-GUIDE-Project-Development-Process.md` | Application Agile Process Manual v1.0 — read after deployment to know how to develop a project with the workbench |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | Ollama Modelfile system prompt — copied to the project during deployment |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Canonical content of the `.clinerules` file — copied to the project root |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | Product Owner `roleDefinition` — integrated in the project's `.roomodes` |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | Scrum Master `roleDefinition` — integrated in the project's `.roomodes` |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | Developer `roleDefinition` — integrated in the project's `.roomodes` |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | QA Engineer `roleDefinition` — integrated in the project's `.roomodes` |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | "Roo Code Agent" Gemini Gem instructions — manual deployment outside Git |
| [DEPLOY-SCRIPT] | PowerShell Script | `template/template/scripts/deploy-to-project.ps1` | Automated workbench deployment script to a project (parameters: `-ProjectPath`, `-Update`, `-DryRun`) |
| [WORKBENCH-VERSION] | Version file | `template/.workbench-version` | File copied to each project to track the deployed workbench version |
| [VERSION] | Version file | `VERSION` (workbench root) | Current workbench version (SemVer MAJOR.MINOR.PATCH format) |
| [CHANGELOG] | Change log | `CHANGELOG.md` (workbench root) | Workbench version history with project update procedure |
| [GITHUB-WORKBENCH] | GitHub repository | https://github.com/nghiaphan31/agentic-agile-workbench | Workbench GitHub repository — source for cloning and updating the workbench |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | MAJOR.MINOR.PATCH convention used to version the workbench and SP files |

---

## Appendix B — Abbreviations Table

| Abbreviation | Full Form | Explanation |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Timestamped record of an architecture decision. Stored in `memory-bank/decisionLog.md` of the project. |
| **API** | Application Programming Interface | Programming interface. Three APIs in the workbench: Ollama REST (local), OpenAI-compatible (proxy), Anthropic HTTPS (cloud). |
| **DA** | Architecture Decision (Décision d'Architecture) | Identifier for decisions in DOC2 (DA-001 to DA-014). Referenced in DOC3 to justify choices. |
| **GEM** | Gemini Gem | Customized Gemini Web profile with permanent system prompt. "Roo Code Agent" contains SP-007. |
| **Git** | — (proper noun) | Distributed version control system. Each deployed project must be a Git repository. |
| **JSON** | JavaScript Object Notation | Structured data format. Used for `.roomodes` (Agile personas). |
| **LAAW** | Local Agentic Agile Workflow | mychen76 blueprint — source of inspiration for the Memory Bank and Agile personas of the workbench. |
| **LLM** | Large Language Model | Three modes in the workbench: Qwen3-32B (local), Gemini Pro (Google cloud), Claude Sonnet (Anthropic cloud). |
| **PO** | Product Owner | Agile persona — product vision, User Stories, backlog. `product-owner` mode in `.roomodes`. |
| **PRD** | Product Requirements Document | Product requirements document. DOC1 is the workbench PRD. |
| **RBAC** | Role-Based Access Control | Access control by roles. Each Agile persona has a precise permissions matrix. |
| **REQ** | Requirement | Identifier for requirements in DOC1. |
| **SM** | Scrum Master | Pure facilitator Agile persona — Memory Bank + Git only, no code or tests. |
| **SP** | System Prompt | Canonical file in the `template/prompts/` registry with YAML metadata. |
| **SSE** | Server-Sent Events | HTTP server→client streaming protocol. Used by the proxy to return Gemini responses. |
| **le workbench** | Agentic Agile Workbench | Name of the system described in the workbench documents. |
| **VS Code** | Visual Studio Code | Microsoft code editor — main development environment of the workbench. |
| **YAML** | YAML Ain't Markup Language | Human-readable serialization format. Used for the headers of canonical SP files. |

---

## Appendix C — Glossary

| Term | Definition |
| :--- | :--- |
| **Workbench** | This repository (`agentic-agile-workbench`). Contains the reusable tools, rules and processes for developing application projects. Contrasts with the "project" which contains the business code. Analogy: carpentry workshop vs. furniture produced. |
| **Code audit** | Mandatory step when deploying on an existing codebase. The Developer reads the source code and fills the Memory Bank (`systemPatterns.md`, `techContext.md`) with the identified patterns, anti-patterns and technical debts. |
| **Roo Code XML tags** | Roo Code action syntax: `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Any connected LLM must respond with these tags. |
| **Spaghetti code** | Poorly structured source code, without clear architecture, difficult to maintain. Deploying the workbench on spaghetti code requires a prior audit step before any modification. |
| **Initial commit** | First Git commit of a project, made before any workbench deployment. For an existing project: `git commit -m "chore(init): initial state before le workbench refactoring"`. Creates a safe rollback point. |
| **Deployment** | Copying workbench files (`template/`) into an application project. Can be done manually or via `deploy-to-project.ps1`. |
| **deploy-to-project.ps1** | PowerShell script in `template/scripts/` that automates deployment. Parameters: `-ProjectPath` (required), `-Update` (update), `-DryRun` (simulation without writing). |
| **Gemini Gem** | Gemini Web profile with permanent system prompt (SP-007). Created once in the Gemini interface — shared across all projects using Proxy Mode. |
| **Memory Bank** | 7 Markdown files in `memory-bank/` of the project persisting context between sessions. Created during deployment, progressively filled by the Agile personas. |
| **Workbench update** | Process of propagating a new workbench version to existing projects. Triggered by `deploy-to-project.ps1 -Update` or manually. Described in `CHANGELOG.md`. |
| **Cloud Mode** | Roo Code → direct Anthropic API (`claude-sonnet-4-6`). Fully automated, pay per use. |
| **Local Mode** | Roo Code (`pc`) → Ollama `calypso:11434` (Tailscale) → Qwen3-32B. Free, sovereign, private network. |
| **Proxy Mode** | Roo Code → FastAPI proxy `localhost:8000` → clipboard → Gemini Web. Free, requires human copy-paste. |
| **Agile Persona** | Roo Code mode simulating a Scrum role: Product Owner, Scrum Master, Developer, QA Engineer. Each persona has precise RBAC permissions. |
| **Application project** | Git repository containing the business code of an application. Distinct from the workbench. Receives workbench files during deployment. |
| **CHECK→CREATE→READ→ACT sequence** | Mandatory protocol at the start of each Roo Code session in a deployed project. Defined in RULE 1 of `.clinerules`. |
| **SemVer** | Semantic Versioning. MAJOR.MINOR.PATCH format: MAJOR = breaking change, MINOR = new feature, PATCH = fix. Used to version the workbench (`VERSION`) and SP files. |
| **Template** | `template/` directory of the workbench containing all files to copy into application projects. Distinct from `workbench/` which contains the documentation. |
| **`.workbench-version`** | File created at the root of each deployed project, containing the workbench version used (e.g.: `2.0.0`). Allows knowing which workbench version is deployed in each project. |
