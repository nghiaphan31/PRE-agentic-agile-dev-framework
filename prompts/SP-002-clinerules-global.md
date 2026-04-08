---
id: SP-002
name: Global Roo Code Directives (.clinerules)
version: 2.7.0
last_updated: 2026-03-30
status: active
hors_git: false
target_type: roo_clinerules
target_file: .clinerules
target_field: "Entire file — replace all content"
target_location: >
  File `.clinerules` at the root of the project.
  This file is automatically read by Roo Code and injected above
  each user prompt, for all sessions and all modes.
  No manual action required after modification (Roo Code re-reads at each session).
depends_on:
  - SP-005: "The Git rules in RULE 5 assume that the Developer knows the commit protocol defined in SP-005"
  - SP-007: "The XML tags listed in RULE 6 must be identical to those listed in SP-007"
changelog:
  - version: 2.7.0
    date: 2026-03-30
    change: "Added RULE 11-14: Ideation Intake, Sync Awareness, DOC-3 Execution, Tech Suggestions Backlog"
  - version: 2.6.0
    date: 2026-03-29
    change: "Fix SP-002 coherence — remove BOM, fix mojibake (em-dash, arrow), fix literal \\n in RULE 10, consolidate double embedding"
  - version: 2.5.0
    date: 2026-03-28
    change: "Added RULE 9 — Cold Zone Firewall memory access protocol"
  - version: 2.4.0
    date: 2026-03-24
    change: "Added RULE 7 — large file generation chunking protocol"
  - version: 2.1.0
    date: 2026-03-24
    change: "i18n — Full translation to English"
  - version: 2.0.0
    date: 2026-03-23
    change: "Arbitration v2.0 — RULE 1 updated with explicit CHECK->CREATE->READ->ACT sequence"
  - version: 1.0.0
    date: 2026-03-23
    change: Initial creation — 6 rules
---

# SP-002 — Global Roo Code Directives (.clinerules)

## Prompt Content

> Copy this text exactly as the complete content of the `.clinerules` file.

```markdown
# PROTOCOL le workbench — MANDATORY DIRECTIVES (ALL SESSIONS, ALL MODES)




## RULE 1 : MANDATORY READ AT THE START OF EACH SESSION



Before any action, you MUST execute the following sequence in this exact order:




1. CHECK : Does memory-bank/activeContext.md exist?


   - If NO → proceed to the CREATE step


   - If YES → proceed to the READ step


2. CREATE (if absent) : Immediately create memory-bank/activeContext.md AND memory-bank/progress.md


   using the templates defined at the bottom of this file.


3. READ : Read memory-bank/hot-context/activeContext.md then memory-bank/hot-context/progress.md


4. ACT : Process the user’s request




This CHECK→CREATE→READ→ACT sequence is NON-NEGOTIABLE and applies to ALL sessions.




## RULE 2 : MANDATORY WRITE AT THE CLOSE OF EACH TASK



Before closing any task (before attempt_completion), you MUST update:


1. memory-bank/activeContext.md  (new state, next action)


2. memory-bank/progress.md       (check off completed features)


3. memory-bank/decisionLog.md    (ADR with date, context, decision, consequences)


4. docs/ideas/IDEAS-BACKLOG.md  (update status for any IDEA whose status was modified or decisions made during this session)


5. docs/ideas/TECH-SUGGESTIONS-BACKLOG.md  (update status for any TECH suggestion whose status was modified or decisions made during this session)

> **Note:** If SP-002 (.clinerules) was modified, increment its version per RULE 6.2 protocol.

> **Clarification:** If an agent completes work on an IDEA (whether accepting, refining, implementing, etc.), it MUST update that IDEA's status in the backlog before closing the task.




## RULE 3 : CONTEXTUAL READ BASED ON THE TASK



- Before modifying the architecture: read memory-bank/systemPatterns.md


- Before executing build/test commands: read memory-bank/techContext.md


- At the start of a sprint or new feature: read memory-bank/productContext.md




## RULE 4 : NO EXCEPTIONS TO RULES 1-3



These rules apply to ALL modes and ALL sessions, without exception.




## RULE 5 : MANDATORY AND SELF-CONTAINED GIT VERSIONING



This rule applies to all modes with access to the terminal (developer, scrum-master).




### 5.1 — What MUST be versioned



EVERYTHING must be versioned under Git, without exception:


- Application source code (src/, app/, etc.)


- System scripts (proxy.py, scripts/start-proxy.ps1, etc.)


- Configuration files (Modelfile, .roomodes, .clinerules, requirements.txt)


- The Memory Bank (memory-bank/*.md)


- System prompts (prompts/SP-*.md and prompts/README.md)


- Plans and architecture documents (plans/ and workbench/*.md)


- QA reports (docs/qa/*.md)


- Canonical documentation (docs/releases/*/ and docs/DOC-*-CURRENT.md)


- The workbench template (template/)


- Git hooks (.githooks/)


- Git attributes and configuration (.gitattributes, .gitignore)




### 5.2 — When to commit



You MUST execute a Git commit in the following situations:


- After creating or modifying a code file


- After updating the Memory Bank


- After modifying .roomodes, .clinerules, Modelfile or any file in prompts/


- After modifying proxy.py or any other script


- Before closing a task (before attempt_completion)




### 5.3 — Commit message format (Conventional Commits)



You MUST use the Conventional Commits format:


- feat(scope): description     -> New feature


- fix(scope): description      -> Bug fix


- docs(memory): description    -> Memory Bank update


- docs(plans): description     -> Documentation update


- chore(config): description   -> Configuration change


- chore(prompts): description  -> System prompt modification


- refactor(scope): description -> Refactoring without functional change


- test(scope): description     -> Adding or modifying tests




### 5.4 — Git commands to use


  git add .


  git commit -m "type(scope): description concise"


### 5.5 — What must NOT be versioned



- The venv/ folder (local Python environment)


- .env files (API keys — NEVER in Git)


- __pycache__/ files and *.pyc


- Logs (*.log)




## RULE 6 : PROMPT REGISTRY CONSISTENCY



This rule applies to developer and scrum-master modes.




### 6.1 — Before any commit touching an artifact linked to a prompt



If you modify one of the following files: proxy.py, .roomodes, .clinerules, Modelfile


you MUST check whether the change impacts a system prompt in prompts/.




### 6.2 — Verification procedure



1. Read prompts/README.md to identify the affected prompt


2. Open the corresponding SP-XXX file in prompts/


3. If the prompt content must change: modify SP-XXX, increment its version


4. If SP-007 (Gem Gemini) is impacted: add a warning in the commit:


   "MANUAL DEPLOYMENT REQUIRED: update the Gem Gemini with SP-007"


5. Include the modified prompts/ files in the same commit as the target files

   **File concatenation:** Never use PowerShell for file concatenation. The pattern `(Get-Content a) + (Get-Content b) | Set-Content out` silently produces a 1-line file with exit code 0 — no error is raised. Use Python instead (see `scripts/rebuild_sp002.py` for the canonical implementation).

   **SP-002 (.clinerules sync):** Use `python scripts/rebuild_sp002.py` — the SP-002 code block must always match `.clinerules` byte-for-byte. Always verify with `git diff prompts/SP-002-clinerules-global.md` before committing.




### 6.3 — Example commit with prompt update


  git add proxy.py prompts/SP-007-gem-gemini-roo-agent.md


  git commit -m "chore(prompts): mise a jour SP-007 suite modification proxy.py - DEPLOIEMENT MANUEL REQUIS"




## RULE 7: LARGE FILE GENERATION — MANDATORY CHUNKING PROTOCOL



This rule applies to all modes that generate or write large files (>500 lines).




### 7.1 — When this rule applies



Whenever a file to be written exceeds approximately 500 lines, you MUST use the chunking protocol instead of attempting a single write_to_file call.




### 7.2 — Chunking protocol



1. Split the content into logical chunks of 400-500 lines each


2. Write each chunk to a numbered temp file: _temp_chunk_01.md, _temp_chunk_02.md, etc.


3. Verify each temp file was written successfully before proceeding


4. Assemble the final file using PowerShell:


   ```powershell


   Get-Content _temp_chunk_01.md, _temp_chunk_02.md, _temp_chunk_03.md | Set-Content target-file.md -Encoding UTF8


   ```


5. Verify the assembled file (line count, spot-check content)


6. Delete all temp chunk files:


   ```powershell


   Remove-Item _temp_chunk_*.md


   ```




### 7.3 — Why this protocol is mandatory



Single write_to_file calls on large files frequently fail silently or produce truncated output. The chunking protocol guarantees complete and correct file generation regardless of file size.






## RULE 8: DOCUMENTATION DISCIPLINE -- MANDATORY GOVERNANCE PROTOCOL


This rule applies to all modes and all sessions, without exception.



### 8.1 -- The Two Spaces

- docs/releases/vX.Y/ files with status **Frozen** are READ-ONLY for all agents. Never modify them.

- docs/releases/vX.Y/ files with status **Draft** or **In Review** may be modified ONLY by Architect or Product Owner persona.

- memory-bank/ files are agent-writable -- update them freely as working memory.



### 8.2 -- Idea Capture Mandate

When you identify a new requirement, improvement, or architectural change NOT in current release scope:


1. DO NOT modify the current release’s canonical docs (DOC-1..5).

2. ADD an entry to docs/ideas/IDEAS-BACKLOG.md with status [IDEA].

3. CREATE docs/ideas/IDEA-{NNN}-{slug}.md with description, motivation, and affected documents.

4. INFORM the human that a new idea has been captured.




### 8.3 -- Conversation Log Mandate

When saving an AI conversation output:


1. Save to docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md

2. Add entry to docs/conversations/README.md with triage status “Not yet triaged”

3. Never edit a conversation file after creation.




### 8.4 -- Release Document References

Always use full qualified ID: “See DOC-2.3.1” not “See the architecture document.”



### 8.5 -- Execution Tracking

After each work session:


1. Update docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md with session log entry.

2. Update memory-bank/progress.md with current checkbox state.

3. These two files must be consistent at end of every session.






## RULE 9: COLD ZONE FIREWALL -- MANDATORY MEMORY ACCESS PROTOCOL



### 9.1 -- Hot Zone (Read Directly)

Files in memory-bank/hot-context/ are read directly by the agent at session start (RULE 1).

### 9.2 -- Cold Zone (MCP Only)

Files in memory-bank/archive-cold/ MUST NOT be read directly by the agent.

All access to cold archive MUST go through the memory:query MCP tool:

  memory:query("your semantic query here")


### 9.3 -- Why This Rule Exists

Direct reading of cold archive files would:

1. Flood the context window with stale historical data

2. Cause “Lost in the Middle” errors on large projects

3. Defeat the purpose of the Hot/Cold architecture


### 9.4 -- Exception

The Librarian Agent (SP-010) is the ONLY agent authorized to read cold archive files

directly, for the purpose of indexing them into the vector database.




## RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE

This rule applies to ALL modes. It is NON-NEGOTIABLE.

### 10.1 -- Branch Definitions

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| main | Production state. **Frozen.** Only receives merge commits from develop-vX.Y at release time. Tags mark releases. | Never deleted. Never committed to directly. |
| develop | **Wild mainline.** Ad-hoc features, experiments, quick fixes. No formal scope. | Long-lived. Never deleted. Always the base for develop-vX.Y. |
| develop-vX.Y | **Scoped backlog.** Created when IDEAs are formally triaged for vX.Y. All release-scope work lands here. | Created at release planning. Never deleted after merge — kept for traceability. |
| feature/{IDEA-NNN}-{slug} | Single feature or fix. | Branch from develop or develop-vX.Y, merge back via PR. Never deleted — kept for traceability. |
| hotfix/vX.Y.Z | Emergency production fix. | Branched from production tag on main. Merged to main and develop. Never deleted — kept for traceability. |

### 10.2 -- Forbidden Actions

- **NEVER** commit directly on main after a release tag
- **NEVER** commit on a branch that has been merged to main (use a new branch instead)
- **NEVER** commit feature work directly on a release or main branch -- use feature branches
- **ALL** new development (features, refactors, fixes) MUST target develop, develop-vX.Y, or a feature branch derived from them

### 10.3 -- Feature Branch Workflow

All new development (features, bug fixes, refactors) MUST follow this path:

1. Branch from develop (ad-hoc) or develop-vX.Y (scoped) -> feature/{IDEA-NNN}-{slug} or fix/{description}
2. Develop and test on the feature branch
3. Commit results to the feature branch
4. Merge via PR to the source branch (fast-forward merge preferred, NO squash merge)
5. **Keep** the feature branch after merge — never delete it (traceability requirement)
6. **NEVER** use `--delete-branch` when merging PRs — the branch MUST be kept for traceability
7. **Prefer fast-forward or regular merge** over squash merge to preserve full commit history on the feature branch

> **Exception:** Governance-only commits (ADRs, RULE additions, docs fixes) that do not change application code MAY be committed directly on develop.

### 10.4 -- Release Workflow

1. Create develop-vX.Y from develop when IDEAs are formally triaged for vX.Y
2. All vX.Y-scope commits land on develop-vX.Y
3. When ready: create frozen docs in docs/releases/vX.Y/, tag vX.Y.0 on develop-vX.Y, merge to main
4. **Keep** develop-vX.Y after merge — never delete it (traceability requirement)
5. **Fast-forward develop to main** immediately after release merge:
   ```
   git checkout develop && git merge --ff main
   ```
   This restores the invariant: develop is always at or ahead of main, never behind.
6. Continue on develop for the next release cycle

### 10.5 -- Hotfix Exception

For critical production bugs:
1. Branch hotfix/vX.Y.Z from the production tag on main
2. Fix and test on the hotfix branch
3. Merge to main and to develop
4. Tag vX.Y.Z on both branches
5. **Keep** the hotfix branch after merge — never delete it (traceability requirement)

### 10.6 -- ADR Reference

This rule is documented as ADR-006 in memory-bank/hot-context/decisionLog.md.




## RULE 11: SYNCHRONIZATION AWARENESS — MANDATORY FOR ALL AGENTS

Before starting any significant implementation step, check for parallel work that might
overlap with yours. The Orchestrator runs sync detection at every intake — pay attention.

11.1 — Pre-implementation check: Read the DOC-3 execution chapter to see what other
       feature branches are active and what files they modify.

11.2 — Overlap detection: If your implementation touches files modified by another
       active branch, inform the human immediately. Do not create merge conflicts.

11.3 — Merge coordination: Do not merge a branch that creates conflicts with another
       active branch. Coordinate with the other developer (or human).

11.4 — Sync categories (from Orchestrator scan):
       - 🔴 CONFLICT: Two ideas require mutually exclusive changes — human must arbitrate
       - 🟡 REDUNDANCY: Two ideas solve the same problem — merge into single idea
       - 🔵 DEPENDENCY: Idea B needs Idea A first — reorder, communicate
       - 🟠 SHARED_LAYER: Multiple ideas touch same component — coordinate timing
       - 🟢 NO_OVERLAP: No conflicts detected — proceed normally

11.5 — On-demand scan: If the human asks "what else is in flight?", run a full scan
       of all active ideas and present a sync report.

11.6 — Branch merge: On-demand merging (continuous integration) — merge as soon as
       a feature is ready, do not wait for scheduled windows.




## RULE 12: CANONICAL DOCS — CUMULATIVE + RELEASE-SPECIFIC + GITHUB ACTIONS ENFORCEMENT

This rule applies to all modes. It is NON-NEGOTIABLE.


### 12.1 -- Documentation Classification

**R-CANON-0**: Canonical docs are classified into two types:

| Type | Documents | Requirement |
|------|-----------|-------------|
| **Cumulative** | DOC-1 (PRD), DOC-2 (Architecture), DOC-4 (Operations) | Fully self-contained — complete history up to vX.Y |
| **Release-Specific** | DOC-3 (Implementation Plan), DOC-5 (Release Notes) | Only this release's content — historical preserved in `docs/releases/vX.Y/` |

**R-CANON-A**: Historical release-specific docs (DOC-3/DOC-5) are preserved in their respective `docs/releases/vX.Y/` directories.

Minimum line counts:
- **Cumulative docs:** DOC-1 >= 500 lines, DOC-2 >= 500 lines, DOC-4 >= 300 lines
- **Release-specific docs:** DOC-3 >= 100 lines, DOC-5 >= 50 lines


### 12.2 -- GitFlow Rules for Canonical Docs

**R-CANON-1**: Canonical docs on `develop`: Only via feature branch (`feature/canon-doc-*`)

**R-CANON-2**: Canonical docs on `develop-vX.Y`: Only via feature branch scoped to that release

**R-CANON-3**: Direct commits on `develop` or `develop-vX.Y` to canonical docs are **FORBIDDEN**

**R-CANON-4**: Exception: Governance-only commits (ADRs, RULE additions) MAY be committed directly per RULE 10.3 exception


### 12.3 -- Consistency Rules

**R-CANON-5**: All 3 cumulative docs (DOC-1, DOC-2, DOC-4) MUST be updated together for any release

**R-CANON-6**: When merging to `develop-vX.Y`, the 3 cumulative DOC-*-vX.Y-*.md files must exist and be consistent. DOC-3 and DOC-5 are release-specific and updated independently per release.

**R-CANON-7**: The `DOC-*-CURRENT.md` pointer files for cumulative docs (DOC-1, DOC-2, DOC-4) MUST all point to the same release version. DOC-3-CURRENT and DOC-5-CURRENT point to their respective latest release-specific files.


### 12.4 -- Enforcement

Canonical docs enforcement is enforced by:
- **Git pre-receive hook** at `.githooks/pre-receive`
- **GitHub Actions CI** at `.github/workflows/canonical-docs-check.yml`
- These are deployed to new projects via `deploy-workbench-to-project.ps1`



## RULE 13: IDEATION INTAKE — MANDATORY FOR ALL AGENTS

Every human input that is not directly related to the agent's current task MUST be routed
to the Orchestrator Agent for intake processing.

13.1 — Detection: If the human expresses an idea, request, or remark that is outside the
       scope of your current task, it is an off-topic input.

13.2 — Routing: Route to Orchestrator with: raw idea text, your agent context, human's
       exact words. Do not say "I'll look into it" — route immediately.

13.3 — Acknowledgment: The Orchestrator will handle acknowledgment to the human.
       Do NOT ignore the input.

13.4 — Intake: The Orchestrator will assign an IDEA/TECH ID, classify the idea
       (business or technical), add it to the correct backlog, run sync detection,
       and inform the human with routing confirmation and sync opportunities.

13.5 — Classification:
       - BUSINESS (WHAT): User needs, features, product improvements → IDEAS-BACKLOG
       - TECHNICAL (HOW): Implementation approaches, technology choices → TECH-SUGGESTIONS-BACKLOG

13.6 — Refinement options: After intake, the human chooses:
       - [A] Refine now — structured requirement/feasibility session
       - [B] Park for later — marked DEFERRED
       - [C] Sync first — resolve overlap with existing ideas before refining




## RULE 14: DOC-3 EXECUTION CHAPTER — LIVE AT ALL TIMES
The DOC-3 execution tracking chapter is NOT a post-hoc summary. It is a live document
updated continuously throughout the implementation phase.

13.1 — End of session update: Before attempt_completion, update ALL THREE:
       - DOC-3 execution chapter (current step status per IDEA)
       - memory-bank/progress.md (checkbox states)
       - docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md (session log)

13.2 — Consistency: These three files must ALWAYS be consistent with each other.
       If you update one, update all three.

13.3 — Status accuracy: Never mark a step as complete if:
       - Tests are failing
       - QA has not validated it
       - The feature branch has not been merged

13.4 — Tool-assisted generation: The AI generates a draft execution report at session
       end. The human reviews and approves before commit. Never commit execution status
       without human visibility.

13.5 — Pre-release freeze: 5 days before target release:
       - Day -5: Scope freeze (all ideas not REFINED deferred)
       - Day -4: Documentation coherence (DOC-1..DOC-5 aligned)
       - Day -3: Code coherence (all branches merged, full QA pass)
       - Day -2: Dry run release (RC1 tag, full test suite)
       - Day -1: Final review (human approves, vX.Y.0 tag applied)
       - Day 0: Announcement (DOC-5 published, GitHub release created)

13.6 — Hotfix priority: A hotfix ALWAYS interrupts a planned release. Branch from
       the production tag on main, fix, merge to main AND develop, then resume release.

13.7 — Refinement logging: Every refinement session produces a log entry in
       docs/conversations/REFINEMENT-YYYY-MM-DD-{id}.md with discussion summary,
       parked technical suggestions, final requirements, and status transitions.




## RULE 15: TECHNICAL SUGGESTIONS BACKLOG

Technical suggestions ("How" proposals) are tracked separately from business requirements
("What" proposals). They do NOT go directly into PRD or architecture — they are parked,
evaluated, and integrated appropriately.

14.1 — Capture: When a human proposes a technical solution (technology choice,
       implementation approach), park it in TECH-SUGGESTIONS-BACKLOG.md.

14.2 — Routing: Technical suggestions go to TECH-SUGGESTIONS-BACKLOG.md. Business
       requirements go to IDEAS-BACKLOG.md. Never mix the two tracks.

14.3 — Evaluation: The Architect evaluates technical suggestions for feasibility,
       impact, and risk. Decision: ACCEPTED / REJECTED / NEEDS_MORE_INFO.

14.4 — Integration: Accepted technical suggestions may update systemPatterns.md,
       DOC-2, or source code. They do NOT automatically become requirements.

14.5 — Creates requirements: If a technical suggestion generates business needs,
       it routes back to IDEAS-BACKLOG as a separate idea.




---

## MEMORY BANK FILE TEMPLATES




### Template activeContext.md



---



# Active Context



**Last updated:** [DATE]



**Active mode:** [MODE]



**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)



LLM Backend: minmax (default via OpenRouter)



Consecutive Errors: 0



Fallback State: Not triggered



## Current task



[Description of the current task]



## Last result



[Result of the last action]



## Next step(s)



- [ ] [Next immediate action]



## Blockers / Open questions



[None | Description of the blocker]



## Last Git commit



[Short hash and message of the last commit]



---





### Template progress.md



---



# Project Progress



**Last updated:** [DATE]



## le workbench Infrastructure



### Setup Phase
- [ ] Phase 0 : Clean VS Code + Roo Code base
- [ ] Phase 1 : Ollama + models
- [ ] Phase 2 : Git repository initialized
- [ ] Phase 3 : Custom Modelfile
- [ ] Phase 4 : .roomodes (Agile personas)
- [ ] Phase 5 : Memory Bank + .clinerules
- [ ] Phase 6 : proxy.py (Gemini Chrome)
- [ ] Phase 7 : Gem Gemini configured
- [ ] Phase 8 : Roo Code 3-mode switcher
- [ ] Phase 9 : End-to-end tests validated
- [ ] Phase 10 : Anthropic Claude API configured
- [ ] Phase 11 : prompts/ registry initialized
- [ ] Phase 12 : check-prompts-sync.ps1 + pre-commit hook




## Product Features



### Epic 1 : [To be defined]


- [ ] [Feature to be defined]



## Legend

- [ ] To do  |  [-] In progress  |  [x] Done




---





## Notes

> **Why CHECK→CREATE→READ→ACT?** Without the prior check, the agent would attempt to read a non-existent file and fail silently. The sequence guarantees that the Memory Bank is always initialized before being read.
```

## Deployment Notes

1. Open `.clinerules` at the root of the project
2. Replace **all content** with the text above (section "Prompt Content")
3. Save the file (ensure UTF-8 encoding without BOM)
4. Roo Code re-reads `.clinerules` automatically at each new session — no additional action required


## Impact on Other Prompts

- If RULE 5 is modified: check SP-005 (Developer) and SP-004 (Scrum Master) for consistency
- If RULE 6 is modified: no other prompt impacted
- If the XML tags in RULE 6 change: check SP-007 (Gem Gemini) for consistency
