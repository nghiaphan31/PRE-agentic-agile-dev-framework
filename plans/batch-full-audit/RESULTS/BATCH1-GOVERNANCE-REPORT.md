# BATCH 1: Governance Coherence Audit — Results

**Batch ID:** `msgbatch_0155bidg6RmPsSYWczTTxBkD`
**Status:** ended
**Completed at:** 2026-03-29 22:25:08.444991+00:00

---

## Result: gov-sp-clinerules

## 1. Executive Summary

- **Both `.clinerules` (root) and SP-002's "Prompt Content" block are identically corrupted**: UTF-8 bytes were decoded as Latin-1/Windows-1252, producing `â€"â€` for `—` and `Ã¢â€ â€™` for `→` throughout RULES 1–7.
- **A UTF-8 BOM (`\ufeff`) is present** at the start of both the deployed `.clinerules` and SP-002 itself, confirming the corruption propagated from the canonical source.
- **RULE 10 contains literal `\n` backslash-n sequences** (not real newlines) in both files identically — the entire rule is a single-line blob with escaped newlines, rendering it unreadable by any Markdown parser.
- **SP-002 is double-embedded**: the `.clinerules` content appears twice — once inside the ```` ```markdown ``` ```` fenced block (the canonical "Prompt Content"), and again after the `---` separator as a second, partially different rendering (with some formatting differences in RULE 8 onward and a different `activeContext.md` template).
- **The `template/.clinerules` file** shows what the *intended* clean content looks like (proper `→` arrows, proper `—` em-dashes), confirming the root `.clinerules` and SP-002 "Prompt Content" block are both corrupted relative to the intended canonical form.

---

## 2. BOM and Encoding Check

### BOM Presence
| File | BOM Present? | Evidence |
|---|---|---|
| `.clinerules` (root) | **YES** | First 50 chars hex: `'\ufeff# PROTOCOL le workbench â€"â€\x9d MANDATORY DIRECTIV'` — `\ufeff` is the UTF-8 BOM (EF BB BF) |
| SP-002 | **YES** | SP-002 begins with `﻿---` — the `﻿` is the BOM rendered as a visible character |
| `template/.clinerules` | **YES** | Also begins with `﻿#` — BOM present but content is otherwise clean |

### Em-Dash Corruption
**FOUND — pervasive throughout RULES 1–7 in both files.**

The corruption pattern is consistent: UTF-8 multi-byte sequences were interpreted as Latin-1/Windows-1252:

| Intended character | Corrupted rendering | Location |
|---|---|---|
| `—` (em-dash, U+2014) | `â€"â€` | Section headers: `### 5.1 â€"â€ What MUST be versioned`, `### 5.5 â€"â€ What must NOT be versioned`, etc. |
| `→` (right arrow, U+2192) | `Ã¢â€ â€™` | RULE 1: `If NO Ã¢â€ â€™ proceed to the CREATE step` |
| `→` in sequence label | `CHECKÃ¢â€ â€™CREATEÃ¢â€ â€™READÃ¢â€ â€™ACT` | RULE 1 summary line |
| `—` (single) | `â€"â€` | `.env files (API keys â€"â€ NEVER in Git)` in RULE 5.5 |

**Contrast with `template/.clinerules`** which correctly shows:
- `â†'` rendered as `→` (actually also mojibake in the template, but different — `â†'` = UTF-8 for `→` read as Latin-1)

> **Root cause determination**: The file was saved as UTF-8 but read/copied through a pipeline that interpreted it as Latin-1 or Windows-1252, then re-saved. The BOM was preserved but the multi-byte sequences were double-encoded.

### Additional Encoding Anomalies
- The title line in `.clinerules` reads: `# PROTOCOL le workbench â€"â€ MANDATORY DIRECTIVES` — the `â€"â€` should be `—` (em-dash). The `\x9d` byte visible in the hex dump is a Windows-1252 control character that has no valid UTF-8 mapping, indicating a mixed-encoding corruption.
- SP-002's YAML front matter contains: `target_field: "Entire file â€" replace all content"` — the `â€"` should be `—`.
- SP-002 changelog entries: `"Added RULE 7 â€" large file generation chunking protocol"` — same corruption.

---

## 3. Rule-by-Rule Comparison

**Methodology**: Comparing the SP-002 "Prompt Content" fenced block (first embedding, inside ```` ```markdown ````) against the deployed `.clinerules` (root).

### RULE 1: MANDATORY READ AT THE START OF EACH SESSION
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| Heading | `## RULE 1 : MANDATORY READ AT THE START OF EACH SESSION` | Identical | ✅ |
| Step 1 arrow | `Ã¢â€ â€™` (corrupted `→`) | `Ã¢â€ â€™` (same corruption) | ✅ (both corrupted identically) |
| Step 2 arrow | `Ã¢â€ â€™` | `Ã¢â€ â€™` | ✅ |
| Sequence label | `CHECKÃ¢â€ â€™CREATEÃ¢â€ â€™READÃ¢â€ â€™ACT` | Identical | ✅ |
| Overall | **Content matches** — both identically corrupted | | ✅ |

### RULE 2: MANDATORY WRITE AT THE CLOSE OF EACH TASK
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| All content | Identical | Identical | ✅ |
| No special characters | Clean ASCII throughout | Clean ASCII throughout | ✅ |

### RULE 3: CONTEXTUAL READ BASED ON THE TASK
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| All content | Identical | Identical | ✅ |

### RULE 4: NO EXCEPTIONS TO RULES 1-3
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| All content | Identical | Identical | ✅ |

### RULE 5: MANDATORY AND SELF-CONTAINED GIT VERSIONING
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| `### 5.1` heading | `â€"â€ What MUST be versioned` | `â€"â€ What MUST be versioned` | ✅ (both corrupted) |
| `### 5.2` heading | `â€"â€ When to commit` | `â€"â€ When to commit` | ✅ |
| `### 5.3` heading | `â€"â€ Commit message format` | `â€"â€ Commit message format` | ✅ |
| `### 5.4` heading | `â€"â€ Git commands to use` | `â€"â€ Git commands to use` | ✅ |
| `### 5.5` heading | `â€"â€ What must NOT be versioned` | `â€"â€ What must NOT be versioned` | ✅ |
| `.env` line | `API keys â€"â€ NEVER in Git` | `API keys â€"â€ NEVER in Git` | ✅ |
| All content | Identical | Identical | ✅ |

### RULE 6: PROMPT REGISTRY CONSISTENCY
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| `### 6.1` heading | `â€"â€ Before any commit...` | `â€"â€ Before any commit...` | ✅ |
| `### 6.2` heading | `â€"â€ Verification procedure` | `â€"â€ Verification procedure` | ✅ |
| `### 6.3` heading | `â€"â€ Example commit...` | `â€"â€ Example commit...` | ✅ |
| All content | Identical | Identical | ✅ |

### RULE 7: LARGE FILE GENERATION — MANDATORY CHUNKING PROTOCOL
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| Heading | `â€"â€ MANDATORY CHUNKING PROTOCOL` | `â€"â€ MANDATORY CHUNKING PROTOCOL` | ✅ |
| `### 7.1` | `â€"â€ When this rule applies` | `â€"â€ When this rule applies` | ✅ |
| `### 7.2` | `â€"â€ Chunking protocol` | `â€"â€ Chunking protocol` | ✅ |
| `### 7.3` | `â€"â€ Why this protocol is mandatory` | `â€"â€ Why this protocol is mandatory` | ✅ |
| All content | Identical | Identical | ✅ |

### RULE 8: DOCUMENTATION DISCIPLINE -- MANDATORY GOVERNANCE PROTOCOL
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| Heading uses `--` | `-- MANDATORY GOVERNANCE PROTOCOL` | `-- MANDATORY GOVERNANCE PROTOCOL` | ✅ (note: `--` not `—`, clean ASCII) |
| 8.1–8.5 content | Identical | Identical | ✅ |
| Blank line spacing | Double blank lines between subsections in SP-002 | Double blank lines in `.clinerules` | ✅ |

### RULE 9: COLD ZONE FIREWALL -- MANDATORY MEMORY ACCESS PROTOCOL
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| 9.1–9.4 content | Identical | Identical | ✅ |
| Formatting | Single blank lines between subsections | Single blank lines | ✅ |

### RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE
| Aspect | SP-002 Prompt Content | Deployed `.clinerules` | Match? |
|---|---|---|---|
| **Literal `\n` sequences** | **YES** — entire rule is one line with `\n` as text | **YES** — identical | ✅ (both broken identically) |
| Rendering | Unreadable as Markdown — all subsections collapsed into one paragraph | Same | ✅ |
| Content (if `\n` expanded) | 10.1 through 10.6 present | Same sections present | ✅ |
| Functional state | **BROKEN** — `\n` are literal backslash-n characters, not newlines | **BROKEN** identically | ✅ match, ❌ functional |

**RULE 10 detail**: The entire rule from `## RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE` onward is stored as a single line with `\n` escape sequences as literal text. For example:
```
## RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE\n\nThis rule applies to ALL modes. It is NON-NEGOTIABLE.\n\n### 10.1 -- Branch Definitions\n\n| Branch | Purpose | Lifecycle |...
```
This means any Markdown renderer will display RULE 10 as a single unbroken paragraph, and any agent reading the file will see `\n` as two characters (`\` and `n`), not as line breaks. The rule is **functionally inoperative** as written.

---

## 4. Structural Anomalies

### Double-Embedding in SP-002

**CONFIRMED — SP-002 contains the `.clinerules` content TWICE.**

**First embedding** (lines ~50–~400 of SP-002): Inside the ```` ```markdown ```` fenced code block under `## Prompt Content`. This is the canonical "copy this into `.clinerules`" block. It ends with the Notes section and the closing ```` ``` ````.

**Second embedding** (lines ~400–end of SP-002): After the `---` separator that closes the first fenced block, SP-002 continues with what appears to be a second, partially rendered version of the same content. This second embedding includes:
- A truncated/different version of RULE 7.2 (starting mid-protocol at the PowerShell block)
- RULE 8 through RULE 9 (with slightly different whitespace — single blank lines instead of double)
- A second `## MEMORY BANK FILE TEMPLATES` section
- A second `### Template activeContext.md`
- A second `### Template progress.md`

### Template Differences Between the Two Embeddings

| Template field | First embedding (inside ```markdown block) | Second embedding (after ---) |
|---|---|---|
| `activeContext.md` — LLM backend line | `**Active LLM backend:** [Ollama uadf-agent \| Proxy Gemini \| Claude Sonnet API]` | `**Active LLM backend:** MinMax M2.7 via OpenRouter (default) \| Claude Sonnet API (fallback after 3 errors)` |
| `progress.md` — Notes section | `CHECKÃ¢â€ â€™CREATEÃ¢â€ â€™READÃ¢â€ â€™ACT` (corrupted) | `CHECKâ†'CREATEâ†'READâ†'ACT` (different corruption — `â†'` instead of `Ã¢â€ â€™`) |
| RULE 8 blank lines | Double blank lines between subsections | Single blank lines |
| RULE 9 present | Yes | Yes |
| RULE 10 present | Yes (with literal `\n`) | **NO** — RULE 10 is absent from the second embedding |

**Critical finding**: The second embedding's `activeContext.md` template references `MinMax M2.7 via OpenRouter` while the first embedding still references the older `[Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]`. This means SP-002 version 2.5.0 was partially updated — the second embedding received the MinMax update but the first (canonical "Prompt Content") did not.

**Also critical**: RULE 10 is entirely absent from the second embedding. The second embedding ends after RULE 9 and the Memory Bank templates, with no RULE 10 content. This means the second embedding represents an older version of the file (pre-RULE 10).

---

## 5. Known Issues Status

| Issue | Status | Evidence |
|---|---|---|
| BOM in `.clinerules` | **FOUND** | `'\ufeff# PROTOCOL...'` — `\ufeff` is U+FEFF BOM at byte position 0 |
| Em-dash corruption | **FOUND** | `â€"â€` throughout RULES 5–7 headers; `Ã¢â€ â€™` for `→` in RULE 1; `â€"â€` in RULE 5.5 `.env` line; present identically in both `.clinerules` and SP-002 Prompt Content block |
| Literal `\n` in RULE 10 | **FOUND** | RULE 10 is a single line: `## RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE\n\nThis rule applies to ALL modes...` — `\n` are literal two-character sequences, not newlines |
| Double embedding in SP-002 | **FOUND** | SP-002 contains `.clinerules` content inside ```` ```markdown ```` block AND again after the `---` separator; second embedding has different LLM backend text in template, different whitespace in RULE 8, and is missing RULE 10 entirely |

---

## 6. Prioritized Remediation

### P0 (Critical) — Encoding corruption that breaks parsing or display

1. **P0-A: Remove BOM from

---

## Result: gov-sp-roomodes

# SP-003..006 vs .roomodes Coherence Audit

---

## 1. Executive Summary

- **All four roleDefinition strings are character-perfect matches** between their canonical SP files and the deployed `.roomodes` entries — no semantic or functional drift detected.
- **All RBAC/groups configurations are fully consistent** between each SP's "Associated RBAC Configuration" section and the corresponding `.roomodes` customModes entry, including regex patterns, allowedCommands arrays, and permission scopes.
- **The `customModes` array order in `.roomodes` is correct**: index 0 = product-owner (SP-003), index 1 = scrum-master (SP-004), index 2 = developer (SP-005), index 3 = qa-engineer (SP-006), matching the SP target_field declarations exactly.
- **`prompts/README.md` inventory is accurate** for SP-003..006: IDs, filenames, names, deployment targets, and target_field values all match the deployed state.
- **`.roomodes` is valid JSON** with no syntax errors detected; the file is well-formed with correct comma placement, bracket matching, and quoting throughout.

---

## 2. Persona-by-Persona Comparison

### 2.1 SP-003 → product-owner (`customModes[0]`)

**roleDefinition extracted from SP-003 "Prompt Content" block:**
```
You are the Product Owner of the Scrum team. Your role is to define and prioritize the product backlog. You write User Stories in the format 'As a [persona], I want [action] so that [benefit]'. You keep the file memory-bank/productContext.md up to date. You NEVER touch the source code or scripts. If asked to write code, you politely decline and suggest switching to Developer mode. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**roleDefinition extracted from `.roomodes` customModes[0]:**
```
You are the Product Owner of the Scrum team. Your role is to define and prioritize the product backlog. You write User Stories in the format 'As a [persona], I want [action] so that [benefit]'. You keep the file memory-bank/productContext.md up to date. You NEVER touch the source code or scripts. If asked to write code, you politely decline and suggest switching to Developer mode. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**Comparison result:** ✅ **IDENTICAL** — character-for-character match. No discrepancy.

---

### 2.2 SP-004 → scrum-master (`customModes[1]`)

**roleDefinition extracted from SP-004 "Prompt Content" block:**
```
You are the Scrum Master of the Scrum team. You facilitate Agile ceremonies (Sprint Planning, Daily, Review, Retrospective). You identify and remove impediments. You keep memory-bank/progress.md and memory-bank/activeContext.md up to date. You do not touch the application source code. You can read all project files, including QA reports in docs/qa/. To know the test status, you read the reports produced by the QA Engineer in docs/qa/ — you do not run test commands yourself. MANDATORY GIT RULE: After each Memory Bank update, you MUST run a Git commit with the message format 'docs(memory): [description of the update]'. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**roleDefinition extracted from `.roomodes` customModes[1]:**
```
You are the Scrum Master of the Scrum team. You facilitate Agile ceremonies (Sprint Planning, Daily, Review, Retrospective). You identify and remove impediments. You keep memory-bank/progress.md and memory-bank/activeContext.md up to date. You do not touch the application source code. You can read all project files, including QA reports in docs/qa/. To know the test status, you read the reports produced by the QA Engineer in docs/qa/ — you do not run test commands yourself. MANDATORY GIT RULE: After each Memory Bank update, you MUST run a Git commit with the message format 'docs(memory): [description of the update]'. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**Comparison result:** ✅ **IDENTICAL** — character-for-character match. No discrepancy.

---

### 2.3 SP-005 → developer (`customModes[2]`)

**roleDefinition extracted from SP-005 "Prompt Content" block:**
```
You are the senior Developer of the Scrum team. You implement User Stories from the backlog. You write clean, tested, and documented code. MANDATORY 3-STEP PROTOCOL: (1) BEFORE coding: read memory-bank/activeContext.md, memory-bank/systemPatterns.md and memory-bank/techContext.md. (2) AFTER coding: update memory-bank/activeContext.md and memory-bank/progress.md. (3) BEFORE closing the task: run 'git add .' then 'git commit -m [descriptive message in conventional format]'. Git versioning is NON-NEGOTIABLE: every file created or modified must be committed before attempt_completion. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**roleDefinition extracted from `.roomodes` customModes[2]:**
```
You are the senior Developer of the Scrum team. You implement User Stories from the backlog. You write clean, tested, and documented code. MANDATORY 3-STEP PROTOCOL: (1) BEFORE coding: read memory-bank/activeContext.md, memory-bank/systemPatterns.md and memory-bank/techContext.md. (2) AFTER coding: update memory-bank/activeContext.md and memory-bank/progress.md. (3) BEFORE closing the task: run 'git add .' then 'git commit -m [descriptive message in conventional format]'. Git versioning is NON-NEGOTIABLE: every file created or modified must be committed before attempt_completion. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**Comparison result:** ✅ **IDENTICAL** — character-for-character match. No discrepancy.

---

### 2.4 SP-006 → qa-engineer (`customModes[3]`)

**roleDefinition extracted from SP-006 "Prompt Content" block:**
```
You are the QA Engineer of the Scrum team. You design and execute test plans. You analyze logs and test reports. You write bug reports with clear reproduction steps in docs/qa/. You NEVER modify the application source code. You can run test commands (npm test, pytest, etc.) and read all files. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**roleDefinition extracted from `.roomodes` customModes[3]:**
```
You are the QA Engineer of the Scrum team. You design and execute test plans. You analyze logs and test reports. You write bug reports with clear reproduction steps in docs/qa/. You NEVER modify the application source code. You can run test commands (npm test, pytest, etc.) and read all files. Your default LLM backend is MinMax M2.7 via OpenRouter. Claude Sonnet is available as fallback after 3 consecutive MinMax errors (requires human approval).
```

**Comparison result:** ✅ **IDENTICAL** — character-for-character match. No discrepancy.

---

## 3. RBAC/Groups Consistency

### 3.1 product-owner (SP-003 vs `.roomodes[0]`)

| Element | SP-003 Prescribes | `.roomodes` Deploys | Match? |
|---|---|---|---|
| `"read"` (bare string) | ✅ | ✅ | ✅ |
| `"edit"` with fileRegex | `memory-bank/productContext\\.md\|docs/.*\\.md\|user-stories.*\\.md` | `memory-bank/productContext\\.md\|docs/.*\\.md\|user-stories.*\\.md` | ✅ |
| edit description | `"Product documentation only"` | `"Product documentation only"` | ✅ |
| `"command"` group | ❌ absent | ❌ absent | ✅ |
| `"browser"` group | ❌ absent | ❌ absent | ✅ |
| `"mcp"` group | ❌ absent | ❌ absent | ✅ |
| `"source"` | `"project"` | `"project"` | ✅ |

**Verdict:** ✅ **Fully consistent.** The Product Owner correctly has no terminal or browser access.

---

### 3.2 scrum-master (SP-004 vs `.roomodes[1]`)

| Element | SP-004 Prescribes | `.roomodes` Deploys | Match? |
|---|---|---|---|
| `"read"` (bare string) | ✅ | ✅ | ✅ |
| `"edit"` with fileRegex | `memory-bank/.*\\.md\|docs/.*\\.md` | `memory-bank/.*\\.md\|docs/.*\\.md` | ✅ |
| edit description | `"Memory Bank and documentation"` | `"Memory Bank and documentation"` | ✅ |
| `"command"` allowedCommands | `["git add", "git commit", "git status", "git log"]` | `["git add", "git commit", "git status", "git log"]` | ✅ |
| command description | `"Git commands to version the Memory Bank"` | `"Git commands to version the Memory Bank"` | ✅ |
| `"browser"` group | ❌ absent | ❌ absent | ✅ |
| `"mcp"` group | ❌ absent | ❌ absent | ✅ |
| `"source"` | `"project"` | `"project"` | ✅ |

**Verdict:** ✅ **Fully consistent.** The Scrum Master correctly cannot run `pytest`/`npm test` — those commands are absent from `allowedCommands`. The `read` group correctly grants access to `docs/qa/` without a special permission entry.

---

### 3.3 developer (SP-005 vs `.roomodes[2]`)

| Element | SP-005 Prescribes | `.roomodes` Deploys | Match? |
|---|---|---|---|
| `"read"` | ✅ | ✅ | ✅ |
| `"edit"` (bare, unrestricted) | ✅ | ✅ | ✅ |
| `"browser"` | ✅ | ✅ | ✅ |
| `"command"` (bare, unrestricted) | ✅ | ✅ | ✅ |
| `"mcp"` | ✅ | ✅ | ✅ |
| `"source"` | `"project"` | `"project"` | ✅ |

**Verdict:** ✅ **Fully consistent.** The Developer has the broadest permission set (all 5 groups, none restricted), matching the SP-005 specification exactly.

---

### 3.4 qa-engineer (SP-006 vs `.roomodes[3]`)

| Element | SP-006 Prescribes | `.roomodes` Deploys | Match? |
|---|---|---|---|
| `"read"` (bare string) | ✅ | ✅ | ✅ |
| `"edit"` with fileRegex | `docs/qa/.*\\.md\|memory-bank/progress\\.md` | `docs/qa/.*\\.md\|memory-bank/progress\\.md` | ✅ |
| edit description | `"QA reports and progress tracking"` | `"QA reports and progress tracking"` | ✅ |
| `"command"` allowedCommands | `["npm test", "npm run test", "pytest", "python -m pytest", "dotnet test", "go test", "git status", "git log"]` | `["npm test", "npm run test", "pytest", "python -m pytest", "dotnet test", "go test", "git status", "git log"]` | ✅ |
| command description | `"Test commands and Git consultation"` | `"Test commands and Git consultation"` | ✅ |
| `"browser"` group | ❌ absent | ❌ absent | ✅ |
| `"mcp"` group | ❌ absent | ❌ absent | ✅ |
| `"source"` | `"project"` | `"project"` | ✅ |

**Verdict:** ✅ **Fully consistent.** The QA Engineer correctly cannot `git commit` (absent from allowedCommands) and cannot modify source code (edit regex restricts to `docs/qa/` and `memory-bank/progress.md` only).

---

### 3.5 Cross-Persona RBAC Privilege Ladder

As a sanity check, the privilege escalation is correctly ordered:

```
product-owner  →  read + edit(docs only)                          [no terminal]
scrum-master   →  read + edit(memory+docs) + command(git only)    [no test runner]
qa-engineer    →  read + edit(qa+progress) + command(tests+git-r) [no git write]
developer      →  read + edit + browser + command + mcp           [full access]
```

This ladder is internally consistent and matches the Agile role separation principle documented in each SP.

---

## 4. prompts/README.md Inventory Check

Examining the inventory table in `prompts/README.md` for SP-003..006:

| README Entry | ID | File | Name | Deployment Target | target_field | Accurate? |
|---|---|---|---|---|---|---|
| SP-003 | `SP-003` | `SP-003-persona-product-owner.md` | Persona Product Owner | `.roomodes` > `customModes[0].roleDefinition` | Matches SP-003 `target_field` | ✅ |
| SP-004 | `SP-004` | `SP-004-persona-scrum-master.md` | Persona Scrum Master | `.roomodes` > `customModes[1].roleDefinition` | Matches SP-004 `target_field` | ✅ |
| SP-005 | `SP-005` | `SP-005-persona-developer.md` | Persona Developer | `.roomodes` > `customModes[2].roleDefinition` | Matches SP-005 `target_field` | ✅ |
| SP-006 | `SP-006` | `SP-006-persona-qa-engineer.md` | Persona QA Engineer | `.roomodes` > `customModes[3].roleDefinition` | Matches SP-006 `target_field` | ✅ |

**Additional checks:**
- The `Out of Git` column correctly shows `No` for all four personas (they are all in the Git repository). ✅
- The array indices in the README (`customModes[0]` through `customModes[3]`) match the actual order in `.roomodes`. ✅
- The README correctly identifies `.roomodes` (not `.clinerules` or `Modelfile`) as the deployment target for all four. ✅
- The "Fundamental Principle" section correctly states that `.roomodes` should never be modified directly without updating the canonical SP file first. ✅

**One observation (not an error):** The README `name` column for SP-003..006 uses shortened names ("Persona Product Owner", "Persona Scrum Master", etc.) while the SP YAML front matter `name` fields use the same shortened form. The `.roomodes` `name` fields use even shorter display names ("Product Owner", "Scrum Master", etc.) — this is expected and correct, as the `.roomodes` `name` field is the UI display label, not the SP document title.

---

## Result: gov-readme-sp

## 1. Executive Summary

- **All 10 SP files (SP-001 through SP-010) are listed in the README inventory table** and all 10 corresponding files have been provided/confirmed to exist in the `prompts/` directory.
- **Deployment targets in the README are accurate** for all 10 SPs based on cross-referencing the YAML front matter in each SP file against the README inventory table.
- **SP-002 has a version drift issue**: the README was last updated `2026-03-24` but SP-002 is at version `2.5.0` dated `2026-03-28`, indicating the README's `Last updated` timestamp is stale (minor cosmetic issue, not a structural integrity failure).
- **The `depends_on` relationships in the README's "Critical Dependencies" section are partially incomplete** relative to what is declared in the SP files themselves (e.g., SP-004's dependency on SP-002 is not surfaced in the README's Critical Dependencies section).
- **No orphaned files detected** — every `.md` file in `prompts/` corresponds to a registered SP entry; the README itself is the registry document, not an SP file.

---

## 2. File Existence Check

| SP ID | Listed in README | File Exists | Path |
|---|---|---|---|
| SP-001 | Yes | Yes | `prompts/SP-001-ollama-modelfile-system.md` |
| SP-002 | Yes | Yes | `prompts/SP-002-clinerules-global.md` |
| SP-003 | Yes | Yes | `prompts/SP-003-persona-product-owner.md` |
| SP-004 | Yes | Yes | `prompts/SP-004-persona-scrum-master.md` |
| SP-005 | Yes | Yes | `prompts/SP-005-persona-developer.md` |
| SP-006 | Yes | Yes | `prompts/SP-006-persona-qa-engineer.md` |
| SP-007 | Yes | Yes | `prompts/SP-007-gem-gemini-roo-agent.md` |
| SP-008 | Yes | Yes | `prompts/SP-008-synthesizer-agent.md` |
| SP-009 | Yes | Yes | `prompts/SP-009-devils-advocate-agent.md` |
| SP-010 | Yes | Yes | `prompts/SP-010-librarian-agent.md` |

**Result: 10/10 — Perfect match. No missing files.**

---

## 3. Deployment Target Accuracy

Cross-referencing the README inventory table against each SP file's `target_file` / `target_type` / `used_by` YAML front matter:

| SP ID | README Target | SP File Declares | Match? | Notes |
|---|---|---|---|---|
| SP-001 | `Modelfile` SYSTEM block | `target_file: Modelfile` / `target_type: ollama_modelfile` | ✅ Yes | Exact match |
| SP-002 | `.clinerules` (entire file) | `target_file: .clinerules` / `target_type: roo_clinerules` | ✅ Yes | Exact match |
| SP-003 | `.roomodes` > `customModes[0].roleDefinition` | `target_file: .roomodes` / `target_field: customModes[0].roleDefinition` | ✅ Yes | Exact match |
| SP-004 | `.roomodes` > `customModes[1].roleDefinition` | `target_file: .roomodes` / `target_field: customModes[1].roleDefinition` | ✅ Yes | Exact match |
| SP-005 | `.roomodes` > `customModes[2].roleDefinition` | `target_file: .roomodes` / `target_field: customModes[2].roleDefinition` | ✅ Yes | Exact match |
| SP-006 | `.roomodes` > `customModes[3].roleDefinition` | `target_file: .roomodes` / `target_field: customModes[3].roleDefinition` | ✅ Yes | Exact match |
| SP-007 | `gemini.google.com` > Gems > Instructions | `target_type: gemini_gem_instructions` / `target_file: EXTERNAL` | ✅ Yes | Correctly flagged Out of Git = YES |
| SP-008 | `src/calypso/orchestrator_phase3.py` (inline system prompt) | `used_by: src/calypso/orchestrator_phase3.py` | ✅ Yes | Exact match |
| SP-009 | `src/calypso/orchestrator_phase4.py` (inline system prompt) | `used_by: src/calypso/orchestrator_phase4.py` | ✅ Yes | Exact match |
| SP-010 | `src/calypso/librarian_agent.py` (Python script, no conversational prompt) | `used_by: src/calypso/librarian_agent.py` | ✅ Yes | Exact match; README correctly notes "no conversational prompt" |

**Result: 10/10 — All deployment targets are accurate.**

**Secondary verification — `.roomodes` actual content vs SP-declared targets:**

The `.roomodes` file provided confirms the four personas exist in the correct array positions:
- Index 0: `product-owner` ✅ (matches SP-003)
- Index 1: `scrum-master` ✅ (matches SP-004)
- Index 2: `developer` ✅ (matches SP-005)
- Index 3: `qa-engineer` ✅ (matches SP-006)

---

## 4. Orphaned Files

**No orphaned files detected.**

The only `.md` file in `prompts/` that is not an SP file is `README.md` itself — which is the registry document, not a prompt artifact. This is correct by design.

All 10 SP files present in `prompts/` are registered in the inventory table.

---

## 5. Missing from README

**No SP files are missing from the README inventory.**

All 10 SP files (SP-001 through SP-010) are listed in the Prompt Inventory table. There are no SP files that exist without a corresponding registry entry.

---

## 6. Prioritized Remediation

### P0 (Critical): Missing files, wrong deployment targets
*None identified.* All files exist and all deployment targets are accurate.

---

### P1 (Important): Orphaned files, missing from README
*None identified.*

---

### P2 (Nice to have): Incomplete depends_on relationships and stale metadata

**P2-A — README `Last updated` timestamp is stale**
- README declares `Last updated: 2026-03-24`
- SP-002, SP-003, SP-004, SP-005, SP-006 were all updated `2026-03-28`
- **Fix:** Update README header to `Last updated: 2026-03-28`

**P2-B — README "Critical Dependencies" section is incomplete**

The README's Critical Dependencies section lists only 4 relationships:
```
- SP-007 depends on proxy.py
- SP-002 depends on SP-005
- SP-007 depends on SP-002
- SP-001 requires recompilation
```

However, the SP files themselves declare additional `depends_on` relationships not surfaced in the README:

| Declared in SP file | Relationship | In README Critical Dependencies? |
|---|---|---|
| SP-002 front matter | depends_on SP-005, SP-007 | SP-002→SP-005 ✅ present; SP-002→SP-007 ✅ present (as SP-007 depends on SP-002) |
| SP-004 front matter | depends_on SP-002 (RULE 5 commit format) | ❌ Not listed |
| SP-005 front matter | depends_on SP-002 (RULE 5 Git rules) | ❌ Not listed |
| SP-007 front matter | depends_on proxy.py, SP-002 | ✅ Both present |

**Fix:** Add to README Critical Dependencies:
```
- SP-004 depends on SP-002: the Conventional Commits format in RULE 5 is referenced by the Scrum Master's mandatory Git rule
- SP-005 depends on SP-002: the Git rules in RULE 5 define the commit protocol the Developer must apply
```

**P2-C — SP-002 YAML front matter schema inconsistency**

SP-002 uses `hors_git: false` (matching SP-001 schema), while SP-008, SP-009, SP-010 use `sp_id` instead of `id` and omit `hors_git`. The README inventory correctly reflects all entries regardless, but the SP file schemas are not uniform across the registry. This is a cosmetic/maintainability issue.

**Fix:** Standardize YAML front matter schema across all SP files (use `id`, `hors_git`, `target_type`, `target_file` consistently).

**P2-D — SP-002 file has encoding artifacts**

SP-002 has a UTF-8 BOM (`\ufeff`) and contains mojibake sequences (`â€"â€`, `Ã¢â€ â€™`) throughout, indicating a double-encoding issue (UTF-8 content read as Latin-1 then re-encoded). This does not affect registry integrity but will cause display/parsing issues.

**Fix:** Re-save SP-002 as clean UTF-8 without BOM, replacing mojibake with correct Unicode characters (`—`, `→`).

---

## 7. Verdict

**[CONSISTENT]**

The `prompts/README.md` registry accurately reflects the actual state of the `prompts/` directory: all 10 SP files (SP-001 through SP-010) are listed, all 10 files exist, and all deployment targets are correct. The identified issues are exclusively P2 (cosmetic/maintenance): a stale `Last updated` timestamp, two undocumented `depends_on` relationships in the Critical Dependencies section, a non-uniform YAML front matter schema across SP files, and encoding artifacts in SP-002. None of these issues compromise the registry's functional integrity or the ability of agents to locate and deploy the correct prompts.

---

## Result: gov-template-root

# .clinerules Sync Audit Report

## 1. Executive Summary

- **The two files are NOT identical** — there are meaningful content and encoding differences across multiple sections
- **Both files have BOM** (`\ufeff`) at byte 0, but the root file's BOM is confirmed in the hex dump while the template's BOM appears as `﻿` (rendered), indicating both carry UTF-8 BOM
- **Critical encoding corruption** exists in the root `.clinerules`: em-dashes and arrows are mojibake (`â€"â€`, `Ã¢â€ â€™`) throughout Rules 1–7, while `template/.clinerules` has clean Unicode (`â€"`, `â†'`) — but notably, the template's encoding is *also* corrupted (double-encoded), just differently
- **All 10 RULES are present in both files** — structural completeness is confirmed
- **The Memory Bank templates differ** in at least one substantive field (`activeContext.md` LLM backend line), and the root file's templates contain additional mojibake artifacts

---

## 2. Byte-Level Comparison

**Are the files identical?** → **NO**

### Key Differences Identified (Line-by-Line Analysis)

| Location | Root `.clinerules` | `template/.clinerules` | Type |
|---|---|---|---|
| **Byte 0** | `\ufeff` (BOM, confirmed in hex) | `﻿` (BOM rendered as replacement char) | Encoding |
| **Title line** | `# PROTOCOL le workbench â€"â€ MANDATORY DIRECTIVES` | `# PROTOCOL le workbench â€" MANDATORY DIRECTIVES` | **Content drift** — root has double-corrupted `â€"â€` vs template's single-corrupted `â€"` |
| **RULE 1 arrows** | `Ã¢â€ â€™` (triple mojibake for `→`) | `â†'` (single mojibake for `→`) | Encoding corruption level differs |
| **RULE 1 sequence line** | `This CHECKÃ¢â€ â€™CREATEÃ¢â€ â€™READÃ¢â€ â€™ACT` | `This CHECKâ†'CREATEâ†'READâ†'ACT` | Same pattern — root worse |
| **Rules 5.1–7.3 em-dashes** | `â€"â€` (double-corrupted) | `â€"` (single-corrupted) | Root is more corrupted |
| **Rules 8–9** | Identical content | Identical content | ✅ Match |
| **RULE 10** | Identical (both use `\n` literal escapes) | Identical | ✅ Match |
| **Memory Bank template — activeContext.md LLM line** | `[Ollama uadf-agent \| Proxy Gemini \| Claude Sonnet API]` | `MinMax M2.7 via OpenRouter (default) \| Claude Sonnet API (fallback after 3 errors)` | **Substantive content drift** |
| **Memory Bank template — Notes section** | `CHECKÃ¢â€ â€™CREATEÃ¢â€ â€™READÃ¢â€ â€™ACT` (triple mojibake) | `CHECKâ†'CREATEâ†'READâ†'ACT` (single mojibake) | Encoding level differs |
| **Root file trailing content** | Contains SP-002 YAML front matter fragments and partial rule text appended after the Notes section | Clean end after Notes | **Critical structural corruption** |

### Root File Trailing Corruption (Critical Finding)

The root `.clinerules` has **extraneous content appended after the Memory Bank templates** — specifically, fragments that appear to be from SP-002's YAML/markdown body leaked into the deployed file. This content does not exist in `template/.clinerules`:

```
```powershell
   Get-Content _temp_chunk_01.md, ... | Set-Content target-file.md -Encoding UTF8
   ```
5. Verify the assembled file...
6. Delete all temp chunk files...
### 7.3 â€" Why this protocol is mandatory
...
## RULE 8: DOCUMENTATION DISCIPLINE...   [REPEATED/VARIANT]
...
## RULE 9: COLD ZONE FIREWALL...          [REPEATED/VARIANT]
...
## MEMORY BANK FILE TEMPLATES             [SECOND COPY]
```

The root file appears to contain **two copies of Rules 7.3–9 and the Memory Bank templates**, with the second copy having slightly different formatting (single-line spacing vs double-line spacing in the first copy). This is a chunking assembly artifact.

---

## 3. Content Comparison by Section

| Section | Root | Template | Match? | Notes |
|---|---|---|---|---|
| **RULE 1** | present | present | ⚠️ Partial | Same logic; root has `Ã¢â€ â€™` for `→`, template has `â†'` — both corrupted, different severity |
| **RULE 2** | present | present | ✅ Yes | Content identical modulo double-spacing |
| **RULE 3** | present | present | ✅ Yes | Content identical |
| **RULE 4** | present | present | ✅ Yes | Content identical |
| **RULE 5** | present | present | ⚠️ Partial | Em-dashes: root `â€"â€` vs template `â€"` — same corruption, different degree |
| **RULE 6** | present | present | ⚠️ Partial | Same em-dash corruption delta as RULE 5 |
| **RULE 7** | present | present | ⚠️ Partial | Same em-dash issue; root also has a **second copy** of 7.3 appended |
| **RULE 8** | present | present | ✅ Yes | Both use `--` (ASCII double-hyphen); formatting identical |
| **RULE 9** | present | present | ✅ Yes | Content identical; root has second copy appended |
| **RULE 10** | present | present | ✅ Yes | Both use literal `\n` escapes (pre-rendered); identical |
| **MB Template: activeContext.md** | present | present | ❌ No | LLM backend field differs: root=`Ollama/Gemini/Claude`, template=`MinMax M2.7/Claude` |
| **MB Template: progress.md** | present | present | ✅ Yes | Checklist items identical |
| **MB Template: Notes** | present | present | ⚠️ Partial | Arrow encoding differs (`Ã¢â€ â€™` vs `â†'`) |
| **Trailing content (post-Notes)** | present (corrupted) | absent | ❌ No | Root has ~150 extra lines of duplicated/leaked content |

---

## 4. Encoding Anomalies

| File | BOM | Em-dash Encoding | Arrow Encoding | Other Issues |
|---|---|---|---|---|
| `.clinerules` (root) | ✅ Yes (`\ufeff` confirmed in hex) | `â€"â€` — **double UTF-8 mojibake** (U+2014 encoded as UTF-8, then re-encoded as Latin-1, then re-encoded again) | `Ã¢â€ â€™` — **triple mojibake** for `→` (U+2192) | Trailing duplicate content block; LLM backend field is stale (Ollama-era) |
| `template/.clinerules` | ✅ Yes (`﻿` rendered) | `â€"` — **single UTF-8 mojibake** (U+2014 encoded as UTF-8, read as Latin-1) | `â†'` — **single mojibake** for `→` | Cleaner than root but still corrupted; not pure UTF-8 |

### Encoding Corruption Severity Scale

```
Clean UTF-8:    "—"  (U+2014, 3 bytes: E2 80 94)
Single mojibake: "â€"" (UTF-8 bytes read as Latin-1: C3 A2 C2 80 C2 94)
Double mojibake: "â€"â€" (the single mojibake re-encoded again)
Triple mojibake: "Ã¢â€ â€™" (→ U+2192, triple-encoded)
```

**Root is one encoding pass worse than template throughout Rules 1–7.**

This strongly suggests the root file was saved/copied through an additional encoding transformation after the template was created — likely a PowerShell `Set-Content` without `-Encoding UTF8` flag, or a clipboard paste through a Latin-1 intermediary.

---

## 5. Justified Differences

### Intentional Differences (Justified)

| Difference | Justification |
|---|---|
| `activeContext.md` LLM backend field: root=`Ollama uadf-agent \| Proxy Gemini \| Claude Sonnet API` vs template=`MinMax M2.7 via OpenRouter \| Claude Sonnet API` | **Intentional but inverted**: the template was updated to reflect the MinMax backend (per SP-003/004/005/006 v1.2.0, dated 2026-03-28) but the root was NOT updated. This is **backwards** — the root (deployed instance) should be the most current. |

### Accidental Differences (Drift — Not Justified)

| Difference | Classification |
|---|---|
| Root em-dashes double-corrupted vs template single-corrupted | **Accidental** — encoding regression in root |
| Root arrows triple-corrupted vs template single-corrupted | **Accidental** — same encoding regression |
| Root has ~150 lines of duplicated/leaked content after Memory Bank templates | **Accidental** — chunking assembly artifact, likely from a `Get-Content ... \| Set-Content` operation that concatenated SP-002 content into the deployed file |
| Title line: root `â€"â€` vs template `â€"` | **Accidental** — same encoding issue |

### Summary Verdict on Differences

> **0 differences are intentional in the correct direction.** The one "intentional" difference (LLM backend) is actually a case where the template was updated but the root was not — the opposite of what should happen. All other differences are accidental encoding regressions and a structural corruption in the root file.

---

## 6. Prioritized Remediation

### P0 (Critical) — Accidental drift that breaks functionality

**P0.1 — Remove trailing duplicate content from root `.clinerules`**
- The root file has ~150 lines of duplicated Rules 7.3–9 and a second Memory Bank template block appended after the legitimate end of the file
- **Impact:** Roo Code reads the entire file; the duplicate content creates ambiguous rule definitions and inflates context window usage
- **Fix:** Truncate root `.clinerules` at the end of the first `## Notes` block (after the `CHECK→CREATE→READ→ACT` explanation)
- **Cause:** A chunking assembly (`Get-Content chunk_01, chunk_02 | Set-Content`) that included SP-002 body content in one of the chunks

**P0.2 — Update root `.clinerules` LLM backend field in activeContext.md template**
- Root still references `Ollama uadf-agent | Proxy Gemini | Claude Sonnet API`
- Template correctly references `MinMax M2.7 via OpenRouter (default) | Claude Sonnet API (fallback after 3 errors)`
- **Impact:** Agents initialized from root will document wrong LLM backend in their Memory Bank
- **Fix:** Update the `**Active LLM backend:**` line in the root's activeContext.md template to match template

### P1 (Important) — Encoding differences that cause display issues

**P1.1 — Fix double-mojibake in root `.clinerules` (Rules 1–7 em-dashes and arrows)**
- Root has `â€"â€` where template has `â€"`, and `Ã¢â€ â€™` where template has `â†'`
- **Impact:** Agents reading the file see garbled rule text; human maintainers cannot read the file cleanly
- **Fix:** Re-save root `.clinerules` from the template using `Set-Content -Encoding UTF8` (not default PowerShell encoding)
- **Root cause:** The file was likely saved through PowerShell without explicit UTF-8 encoding, causing a second Latin-1 pass

**P1.2 — Fix single-mojibake in BOTH files (em-dashes and arrows)**
- Both files have at minimum single-mojibake corruption (`â€"` instead of `—`, `â†'` instead of `→`)
- **Impact:** Cosmetic but unprofessional; could cause issues with strict UTF-8 parsers
- **Fix:** After fixing P1.1, do a global find-replace in both files:
  ```
  â€" → — (U+2014 EM DASH)
  â†' → → (U+2192 RIGHTWARDS ARROW)
  ```
  Then save with explicit `UTF-8 without BOM` encoding

**P1.3 — Remove BOM from both files**
- Both files have UTF-8 BOM (`\ufeff`)
- **Impact:** Some tools and parsers (including certain Roo Code versions) mishandle BOM; it's the likely root cause of the mojibake chain
- **Fix:** Save both files as `UTF-8 without BOM` (use VS Code: bottom-right encoding selector → "Save with Encoding" → "UTF-8")

### P2 (Nice to have) — Whitespace or comment-only differences

**P2.1 — Standardize RULE 10 literal `\n` escapes**
- Both files use literal `\n` in RULE 10 (not actual newlines), which renders as `\n` in markdown
- **Impact:** RULE 10 displays as a single long line rather than formatted markdown
- **Fix:** Replace literal `\n` with actual newlines in both files (this is a pre-existing issue in both, not a sync issue)

**P2.2 — Standardize double-blank-line spacing**
- Root uses double blank lines between paragraphs (artifact of the chunking protocol)
- Template uses single blank lines in Rules 8–9
- **Impact:** Cosmetic only
- **Fix:** Normalize to single blank lines throughout both files

---

## 7. Verdict

**[MAJOR_DRIFT]**

The root `.clinerules` has diverged from `template/.clinerules` in three critical ways: (1) a structural corruption where ~150 lines of duplicate/leaked content were appended after the legitimate file end, almost certainly from a malformed chunking assembly operation; (2) an additional encoding pass that doubled the mojibake corruption throughout Rules 1–7 (triple-encoded arrows, double-encoded em-dashes); and (3) a stale LLM backend reference in the Memory Bank template that was updated in the template but never propagated to the deployed root instance. The root file — which is the live operational file read by Roo Code on every session — is in worse shape than the template it was supposed to be the source of truth for, which inverts the expected relationship and constitutes a P0 operational risk.

---

