# Central System Prompts Registry — UADF
## Single Source of Truth for All System Prompts

**Project:** Unified Agentic Development Framework (UADF)
**Maintained by:** Developer / Scrum Master (via RULE 6 of `.clinerules`)
**Last updated:** 2026-03-24

---

## Fundamental Distinction: System Prompts vs User Prompts

This repository contains two categories of prompts that have radically different roles.
It is essential not to confuse them.

### System Prompts (this `prompts/` folder)

The SP-XXX files in this folder are **System Prompts**: they configure
the identity, behavioral rules, and permissions of AI agents.

- **Who writes them?** The Developer or Scrum Master (system maintenance)
- **Who reads them?** The AI agent (automatically, at the start of each session)
- **When are they active?** Permanently, in the background, for all sessions
- **Where are they deployed?** In technical configuration files:
  `.clinerules`, `.roomodes`, `Modelfile`, or the Gemini web interface
- **Example:** SP-002 defines the 6 mandatory rules the agent must always follow

### User Prompts (PROMPT blocks in `workbench/DOC5-GUIDE-Project-Development-Process.md`)

The `PROMPT` blocks in DOC5 are **User Prompts**: they are operational
instructions that the human copies and pastes into Roo Code to trigger a specific
step in the Agile workflow.

- **Who writes them?** The human (copy-paste from DOC5)
- **Who reads them?** The AI agent (upon receiving the human's message)
- **When are they active?** Only when sent, for a specific task
- **Where are they used?** In the Roo Code chat interface
- **Example:** PROMPT 4.2 triggers the Sprint Planning for a specific sprint

### Comparison Table

| Criterion | System Prompts (SP-XXX) | User Prompts (PROMPT DOC5) |
| :--- | :--- | :--- |
| **Role** | Configure the agent | Trigger an action |
| **Author** | System maintainer | End user |
| **Frequency** | Once (then maintenance) | At each workflow step |
| **Target** | Technical config files | Roo Code chat interface |
| **Scope** | All sessions | One session / one task |
| **Versioning** | Git + SP-XXX changelog | Integrated in DOC5 (versioned with DOC5) |
| **Modification** | Formal procedure (RULE 6) | Edit DOC5 directly |

---

## Fundamental Principle

This `prompts/` folder is the **single source of truth** for all system prompts in the UADF system.

**Any modification to a prompt must:**
1. Start from this folder (modify the canonical SP-XXX file)
2. Be propagated to its deployment target (config file or web interface)
3. Be committed to Git with a `chore(prompts): ...` message

**Never directly modify** `.roomodes`, `.clinerules`, the `Modelfile`, or the Gemini Gem without updating the corresponding canonical file in this folder.

---

## Prompt Inventory

| ID | File | Name | Deployment Target | Out of Git |
| :--- | :--- | :--- | :--- | :---: |
| **SP-001** | `SP-001-ollama-modelfile-system.md` | System Prompt Ollama Modelfile | `Modelfile` SYSTEM block | No |
| **SP-002** | `SP-002-clinerules-global.md` | Global Roo Code Directives | `.clinerules` (entire file) | No |
| **SP-003** | `SP-003-persona-product-owner.md` | Persona Product Owner | `.roomodes` > `customModes[0].roleDefinition` | No |
| **SP-004** | `SP-004-persona-scrum-master.md` | Persona Scrum Master | `.roomodes` > `customModes[1].roleDefinition` | No |
| **SP-005** | `SP-005-persona-developer.md` | Persona Developer | `.roomodes` > `customModes[2].roleDefinition` | No |
| **SP-006** | `SP-006-persona-qa-engineer.md` | Persona QA Engineer | `.roomodes` > `customModes[3].roleDefinition` | No |
| **SP-007** | `SP-007-gem-gemini-roo-agent.md` | Gem Gemini Chrome "Roo Code Agent" | gemini.google.com > Gems > "Roo Code Agent" > Instructions | **YES** |

---

## Prompt Modification Procedure

```
1. Open the corresponding SP-XXX-*.md file in this folder
2. Modify the prompt content
3. Increment the version (e.g.: 1.0.0 -> 1.1.0)
4. Add an entry in the file's changelog
5. Check dependencies (depends_on field) and update linked prompts
6. Propagate to the target:
   - File in the repository: copy the content into the target file
   - Gemini Gem (SP-007): copy manually into the Gemini web interface
7. Commit ALL modified files:
   git add prompts/ .clinerules .roomodes Modelfile  (depending on what changed)
   git commit -m "chore(prompts): update SP-XXX - [description]"
```

---

## Critical Dependencies

- **SP-007 depends on `proxy.py`**: if the prompt format changes in proxy.py, SP-007 must be updated AND manually re-deployed in Gemini
- **SP-002 depends on SP-005**: the Git rules in .clinerules assume the Developer knows the commit protocol
- **SP-007 depends on SP-002**: the XML tags listed in the Gem must be identical to those expected by Roo Code
- **SP-001 requires recompilation**: after modification, run `ollama create uadf-agent -f Modelfile`
