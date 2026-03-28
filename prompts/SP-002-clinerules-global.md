---


id: SP-002


name: Global Roo Code Directives (.clinerules)


version: 2.5.0


last_updated: 2026-03-28


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


  - version: 2.4.0


    date: 2026-03-24


    change: "Added RULE 7 — large file generation chunking protocol"


  - version: 2.1.0


    date: 2026-03-24


    change: "i18n — Full translation to English. All French prose translated; technical identifiers and commit format prefixes unchanged."


  - version: 2.0.0


    date: 2026-03-23


    change: "Arbitration v2.0 — RULE 1 updated with explicit CHECK->CREATE->READ->ACT sequence (4 numbered steps). Replaces the former implicit formulation."


  - version: 1.0.0


    date: 2026-03-23


    change: Initial creation — 6 rules (Memory Bank x4, Git, Prompt Consistency)


---





# SP-002 — Global Roo Code Directives (.clinerules)





## Prompt Content





> Copy this text exactly as the complete content of the `.clinerules` file.





```markdown
# PROTOCOL le workbench —” MANDATORY DIRECTIVES (ALL SESSIONS, ALL MODES)







## RULE 1 : MANDATORY READ AT THE START OF EACH SESSION



Before any action, you MUST execute the following sequence in this exact order:







1. CHECK : Does memory-bank/activeContext.md exist?



   - If NO â†’ proceed to the CREATE step



   - If YES â†’ proceed to the READ step



2. CREATE (if absent) : Immediately create memory-bank/activeContext.md AND memory-bank/progress.md



   using the templates defined at the bottom of this file.



3. READ : Read memory-bank/hot-context/activeContext.md then memory-bank/hot-context/progress.md



4. ACT : Process the user's request







This CHECKâ†’CREATEâ†’READâ†’ACT sequence is NON-NEGOTIABLE and applies to ALL sessions.







## RULE 2 : MANDATORY WRITE AT THE CLOSE OF EACH TASK



Before closing any task (before attempt_completion), you MUST update:



1. memory-bank/activeContext.md  (new state, next action)



2. memory-bank/progress.md       (check off completed features)







If an architecture decision was made during the session:



3. memory-bank/decisionLog.md    (ADR with date, context, decision, consequences)







## RULE 3 : CONTEXTUAL READ BASED ON THE TASK



- Before modifying the architecture: read memory-bank/systemPatterns.md



- Before executing build/test commands: read memory-bank/techContext.md



- At the start of a sprint or new feature: read memory-bank/productContext.md







## RULE 4 : NO EXCEPTIONS TO RULES 1-3



These rules apply to ALL modes and ALL sessions, without exception.







## RULE 5 : MANDATORY AND SELF-CONTAINED GIT VERSIONING



This rule applies to all modes with access to the terminal (developer, scrum-master).







### 5.1 —” What MUST be versioned



EVERYTHING must be versioned under Git, without exception:



- Application source code (src/, app/, etc.)



- System scripts (proxy.py, scripts/start-proxy.ps1, etc.)



- Configuration files (Modelfile, .roomodes, .clinerules, requirements.txt)



- The Memory Bank (memory-bank/*.md)



- System prompts (prompts/SP-*.md and prompts/README.md)



- Plans and architecture documents (workbench/*.md)



- QA reports (docs/qa/*.md)







### 5.2 —” When to commit



You MUST execute a Git commit in the following situations:



- After creating or modifying a code file



- After updating the Memory Bank



- After modifying .roomodes, .clinerules, Modelfile or any file in prompts/



- After modifying proxy.py or any other script



- Before closing a task (before attempt_completion)







### 5.3 —” Commit message format (Conventional Commits)



You MUST use the Conventional Commits format:



- feat(scope): description     -> New feature



- fix(scope): description      -> Bug fix



- docs(memory): description    -> Memory Bank update



- docs(plans): description     -> Documentation update



- chore(config): description   -> Configuration change



- chore(prompts): description  -> System prompt modification



- refactor(scope): description -> Refactoring without functional change



- test(scope): description     -> Adding or modifying tests







### 5.4 —” Git commands to use



  git add .



  git commit -m "type(scope): description concise"







### 5.5 —” What must NOT be versioned



- The venv/ folder (local Python environment)



- .env files (API keys —” NEVER in Git)



- __pycache__/ files and *.pyc



- Logs (*.log)







## RULE 6 : PROMPT REGISTRY CONSISTENCY



This rule applies to developer and scrum-master modes.







### 6.1 —” Before any commit touching an artifact linked to a prompt



If you modify one of the following files: proxy.py, .roomodes, .clinerules, Modelfile



you MUST check whether the change impacts a system prompt in prompts/.







### 6.2 —” Verification procedure



1. Read prompts/README.md to identify the affected prompt



2. Open the corresponding SP-XXX file in prompts/



3. If the prompt content must change: modify SP-XXX, increment its version



4. If SP-007 (Gem Gemini) is impacted: add a warning in the commit:



   "MANUAL DEPLOYMENT REQUIRED: update the Gem Gemini with SP-007"



5. Include the modified prompts/ files in the same commit as the target files







### 6.3 —” Example commit with prompt update



  git add proxy.py prompts/SP-007-gem-gemini-roo-agent.md



  git commit -m "chore(prompts): mise a jour SP-007 suite modification proxy.py - DEPLOIEMENT MANUEL REQUIS"







## RULE 7: LARGE FILE GENERATION —” MANDATORY CHUNKING PROTOCOL



This rule applies to all modes that generate or write large files (>500 lines).







### 7.1 —” When this rule applies



Whenever a file to be written exceeds approximately 500 lines, you MUST use the chunking protocol instead of attempting a single write_to_file call.







### 7.2 —” Chunking protocol



1. Split the content into logical chunks of 400-500 lines each



2. Write each chunk to a numbered temp file: `_temp_chunk_01.md`, `_temp_chunk_02.md`, etc.



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







### 7.3 —” Why this protocol is mandatory



Single write_to_file calls on large files frequently fail silently or produce truncated output. The chunking protocol guarantees complete and correct file generation regardless of file size.










## RULE 8: DOCUMENTATION DISCIPLINE -- MANDATORY GOVERNANCE PROTOCOL


This rule applies to all modes and all sessions, without exception.





### 8.1 -- The Two Spaces


- `docs/releases/vX.Y/` files with status **Frozen** are READ-ONLY for all agents. Never modify them.


- `docs/releases/vX.Y/` files with status **Draft** or **In Review** may be modified ONLY by Architect or Product Owner persona.


- `memory-bank/` files are agent-writable -- update them freely as working memory.





### 8.2 -- Idea Capture Mandate


When you identify a new requirement, improvement, or architectural change NOT in current release scope:


1. DO NOT modify the current release's canonical docs (DOC-1..5).


2. ADD an entry to `docs/ideas/IDEAS-BACKLOG.md` with status [IDEA].


3. CREATE `docs/ideas/IDEA-{NNN}-{slug}.md` with description, motivation, and affected documents.


4. INFORM the human that a new idea has been captured.





### 8.3 -- Conversation Log Mandate


When saving an AI conversation output:


1. Save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`


2. Add entry to `docs/conversations/README.md` with triage status "Not yet triaged"


3. Never edit a conversation file after creation.





### 8.4 -- Release Document References


Always use full qualified ID: "See DOC-2.3.1" not "See the architecture document."





### 8.5 -- Execution Tracking


After each work session:


1. Update `docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md` with session log entry.


2. Update `memory-bank/progress.md` with current checkbox state.


3. These two files must be consistent at end of every session.







## RULE 9: COLD ZONE FIREWALL -- MANDATORY MEMORY ACCESS PROTOCOL



### 9.1 -- Hot Zone (Read Directly)

Files in `memory-bank/hot-context/` are read directly by the agent at session start (RULE 1).



### 9.2 -- Cold Zone (MCP Only)

Files in `memory-bank/archive-cold/` MUST NOT be read directly by the agent.

All access to cold archive MUST go through the `memory:query` MCP tool:

  memory:query("your semantic query here")



### 9.3 -- Why This Rule Exists

Direct reading of cold archive files would:

1. Flood the context window with stale historical data

2. Cause "Lost in the Middle" errors on large projects

3. Defeat the purpose of the Hot/Cold architecture



### 9.4 -- Exception

The Librarian Agent (SP-010) is the ONLY agent authorized to read cold archive files

directly, for the purpose of indexing them into the vector database.



## RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE

This rule applies to ALL modes. It is NON-NEGOTIABLE.

### 10.1 -- Branch Definitions

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `master` | Production state —” frozen after each release tag | NEVER commit directly after tag |
| `release/vX.Y` | Release branch —” all planned work for vX.Y | CLOSED after merge to master |
| `release/vX.Y+1` | Next release branch | ACTIVE —” all new work lands here |
| `hotfix/vX.Y.Z` | Emergency fixes from production tag | Merged to master + active release |

### 10.2 -- Forbidden Actions

- **NEVER** commit directly on `master` after a release tag
- **NEVER** commit on a `release/vX.Y` branch after it has been merged to `master`
- **NEVER** commit feature work directly on a release branch —” use feature branches
- **ALL** new development (features, refactors, fixes) MUST target `release/vX.Y+1` or a feature branch derived from it

### 10.3 -- Feature Branch Workflow

All new development (features, bug fixes, refactors) MUST follow this path:

1. Branch from `release/vX.Y+1` â†’ `feature/{IDEA-NNN}-{slug}` or `fix/{description}`
2. Develop and test on the feature branch
3. Commitæˆæžœ to the feature branch
4. Merge via PR to `release/vX.Y+1` (fast-forward or squash)
5. Delete the feature branch after merge

> **Exception:** Governance-only commits (ADRs, RULE additions, docs fixes) that do not change application code MAY be committed directly on the release branch.

### 10.4 -- Release Workflow

1. Create `release/vX.Y` from `master` at start of release cycle
2. All commits for vX.Y land on `release/vX.Y`
3. When ready: tag `vX.Y.0` on `release/vX.Y`, merge to `master`, close `release/vX.Y`
4. Immediately create `release/vX.Y+1` for next cycle

### 10.5 -- Hotfix Exception

For critical production bugs:
1. Branch `hotfix/vX.Y.Z` from the production tag
2. Fix and test on the hotfix branch
3. Merge to `master` and to the active `release/vX.Y` branch
4. Tag `vX.Y.Z` on both branches

### 10.6 -- ADR Reference

This rule is documented as ADR-005 in `memory-bank/hot-context/decisionLog.md`.

---

## MEMORY BANK FILE TEMPLATES




### Template activeContext.md



---



# Active Context



**Last updated:** [DATE]



**Active mode:** [MODE]



**Active LLM backend:** [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]







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







## Infrastructure le workbench



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



> **Why CHECKâ†’CREATEâ†’READâ†’ACT?** Without the prior check, the agent would attempt to read a non-existent file and fail silently. The sequence guarantees that the Memory Bank is always initialized before being read.




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

- `docs/releases/vX.Y/` files with status **Frozen** are READ-ONLY for all agents. Never modify them.

- `docs/releases/vX.Y/` files with status **Draft** or **In Review** may be modified ONLY by Architect or Product Owner persona.

- `memory-bank/` files are agent-writable -- update them freely as working memory.



### 8.2 -- Idea Capture Mandate

When you identify a new requirement, improvement, or architectural change NOT in current release scope:

1. DO NOT modify the current release's canonical docs (DOC-1..5).

2. ADD an entry to `docs/ideas/IDEAS-BACKLOG.md` with status [IDEA].

3. CREATE `docs/ideas/IDEA-{NNN}-{slug}.md` with description, motivation, and affected documents.

4. INFORM the human that a new idea has been captured.



### 8.3 -- Conversation Log Mandate

When saving an AI conversation output:

1. Save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`

2. Add entry to `docs/conversations/README.md` with triage status "Not yet triaged"

3. Never edit a conversation file after creation.



### 8.4 -- Release Document References

Always use full qualified ID: "See DOC-2.3.1" not "See the architecture document."



### 8.5 -- Execution Tracking

After each work session:

1. Update `docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md` with session log entry.

2. Update `memory-bank/progress.md` with current checkbox state.

3. These two files must be consistent at end of every session.




## RULE 9: COLD ZONE FIREWALL -- MANDATORY MEMORY ACCESS PROTOCOL

### 9.1 -- Hot Zone (Read Directly)
Files in `memory-bank/hot-context/` are read directly by the agent at session start (RULE 1).

### 9.2 -- Cold Zone (MCP Only)
Files in `memory-bank/archive-cold/` MUST NOT be read directly by the agent.
All access to cold archive MUST go through the `memory:query` MCP tool:
  memory:query("your semantic query here")

### 9.3 -- Why This Rule Exists
Direct reading of cold archive files would:
1. Flood the context window with stale historical data
2. Cause "Lost in the Middle" errors on large projects
3. Defeat the purpose of the Hot/Cold architecture

### 9.4 -- Exception
The Librarian Agent (SP-010) is the ONLY agent authorized to read cold archive files
directly, for the purpose of indexing them into the vector database.

## MEMORY BANK FILE TEMPLATES





### Template activeContext.md


---


# Active Context


**Last updated:** [DATE]


**Active mode:** [MODE]
**Active LLM backend:** MinMax M2.7 via OpenRouter (default) | Claude Sonnet API (fallback after 3 errors)



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





## Infrastructure le workbench


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


3. Save the file


4. Roo Code re-reads `.clinerules` automatically at each new session — no additional action required





## Impact on Other Prompts





- If RULE 5 is modified: check SP-005 (Developer) and SP-004 (Scrum Master) for consistency


- If RULE 6 is modified: no other prompt impacted


- If the XML tags in RULE 6 change: check SP-007 (Gem Gemini) for consistency


