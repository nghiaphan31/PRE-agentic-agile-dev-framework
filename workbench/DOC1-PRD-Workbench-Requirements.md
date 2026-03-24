# Document 1: Product Requirements Document (PRD)
## Agentic Agile Workbench

**Project Name:** Agentic Agile Workbench
**Version:** 2.0 — Refactored (atomic requirements, integrated trade-offs)
**Date:** 2026-03-23
**Author:** Senior Architecture — Synthesis mychen76 LAAW + Gemini Chrome Proxy
**Status:** Approved

---

## 1. Context and Strategic Vision

This PRD synthesizes two complementary sources of inspiration:

1. **The LAAW Blueprint (mychen76)**: A local, sovereign agentic development environment, orchestrated by specialized AI agents with persistent memory and Agile rituals.
2. **The Gemini Chrome Proxy**: A network-clipboard bridge mechanism allowing Roo Code to leverage the power of Gemini Web for free via minimal human intervention (copy-paste).

The objective is to define a **unified and enriched** system that combines the local sovereignty of LAAW with the flexibility of a hybrid LLM backend (local Ollama OR Gemini Chrome via proxy OR Claude Sonnet via direct API), while maintaining Agile rigor and contextual memory persistence.

---

## 2. Foundational Requirement (REQ-000)

> **REQ-000 — Root Requirement of the Unified System**
>
> The overall system must provide an operational agentic development environment on a Windows laptop (`pc`) with VS Code, relying on a dedicated headless Linux server (`calypso`) for local LLM inference, both machines connected via Tailscale. The system must be capable of:
> - Orchestrating specialized AI agents according to Agile roles (Product Owner, Scrum Master, QA Engineer, Developer)
> - Maintaining absolute context continuity between sessions via persistent memory in auditable Markdown files
> - Executing complex development tasks relying on a **switchable** LLM backend: either a local model (Ollama on `calypso` via Tailscale) for total sovereignty, or Gemini Chrome via a local API proxy for free cloud power, or Claude Sonnet via direct Anthropic API for full automation
> - Ensuring that Roo Code remains the central agentic execution engine in all three operating modes, without modification of its native behavior

---

## 3. Hierarchical Requirements Breakdown

### 3.1 Domain 1 — Agentic Engine & Foundation Models (REQ-1.x)

#### REQ-1.0 — Local LLM Inference Capability
The system must be capable of executing LLM inferences on the private local network (Tailscale), via Ollama installed on the Linux server `calypso` (RTX 5060 Ti 16 GB). The Ollama API is accessible from the laptop `pc` at `http://calypso:11434` via the Tailscale network.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-1.1** | **Main model optimized for Tool Calling** | The Ollama model used as the main agent must be `mychen76/qwen3_cline_roocode:32b`, specifically fine-tuned for Roo Code tool calling. No fallback model is planned — model availability on Ollama Hub is an installation precondition. | The agent emits valid JSON requests to the Roo Code API without syntax or formatting errors on 10 consecutive test requests. |
| **REQ-1.2** | **Minimum context window of 128K tokens** | The `num_ctx` parameter in the Ollama Modelfile must be configured to exactly `131072` (128K tokens). This value is non-negotiable: it allows simultaneous loading of the project source code AND the 7 Memory Bank files into the agent's context. | `ollama show uadf-agent --modelfile` displays `PARAMETER num_ctx 131072`. |
| **REQ-1.3** | **Inference determinism** | Generation parameters must be locked in the Modelfile to eliminate hallucinations during code generation: `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`. These values are fixed and cannot be modified by the user at runtime. | `ollama show uadf-agent --modelfile` displays the 4 parameters with the exact values above. |
| **REQ-1.4** | **Boomerang Tasks delegation** | The system must allow the main agent (32B) to delegate sub-tasks to a lightweight secondary model (`qwen3:7b`) via Roo Code's "Boomerang Tasks" workflow, then integrate the output into its own decision loop. | The 32B agent can create a Boomerang sub-task, the 7B model executes it, and the result is returned to the 32B agent without human intervention. |

---

### 3.2 Domain 2 — Hybrid LLM Backend & Gemini Chrome Proxy (REQ-2.x)

#### REQ-2.0 — LLM Backend Switchability
The system must allow the user to switch Roo Code's LLM backend between the three modes (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) by modifying only the "API Provider" parameter in Roo Code settings, without modifying Roo Code's behavior or the Memory Bank structure.

##### REQ-2.1 — Sub-domain: Local Proxy Server (Interception)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.1.1** | **Local FastAPI server on localhost:8000** | A local Python web server (FastAPI + uvicorn) must listen on `localhost:8000`. It must start in less than 3 seconds after executing `python proxy.py`. | `Invoke-WebRequest http://localhost:8000/health` returns HTTP 200 with `{"status":"ok"}` within 3 seconds of startup. |
| **REQ-2.1.2** | **Exact emulation of OpenAI Chat Completions format** | The proxy must expose the `POST /v1/chat/completions` and `GET /v1/models` endpoints in OpenAI format. Roo Code configured in "OpenAI Compatible" mode with `Base URL: http://localhost:8000/v1` must connect without error. | Roo Code sends a request to the proxy and receives a response without connection or format error messages. |
| **REQ-2.1.3** | **Separate extraction of system prompt and user prompt** | The proxy must parse the `messages` array from the JSON request and extract separately: (a) the `system` role message, (b) `user` role messages, (c) `assistant` role messages (history). This extraction must work even if the array contains a multi-turn history of N messages. | For a `messages` array of 10 elements (1 system + 4 user + 5 assistant), the 3 categories are correctly identified and separated. |
| **REQ-2.1.4** | **"Dedicated Gem" mode: system prompt filtering** | When the environment variable `USE_GEM_MODE=true` (default value), the proxy must omit the `system` role message when copying to the clipboard. Only `user` and `assistant` messages are transmitted. | With `USE_GEM_MODE=true`, the text copied to the clipboard contains no content from the `system` message. The size reduction is measurable (≥ 50% for a standard Roo Code system prompt). |
| **REQ-2.1.5** | **Cleaning of base64 content (images)** | The proxy must detect any `content` element of type `array` containing `{"type": "image_url", ...}` objects and replace them with the exact literal string: `[IMAGE OMITTED - Not supported by clipboard proxy]`. | A request containing a base64 image is processed without error. The clipboard contains the replacement message instead of the image. |

##### REQ-2.2 — Sub-domain: Clipboard Transfer (Uplink)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.2.1** | **Injection into Windows clipboard in less than 500ms** | After receiving and processing the request from Roo Code, the proxy must copy the formatted text to the Windows system clipboard via `pyperclip.copy()`. | The delay between receiving the HTTP request and the text being available in the clipboard is less than 500ms (measured by `Get-Clipboard` immediately after). |
| **REQ-2.2.2** | **Readable format with explicit separators** | The text copied to the clipboard must use the following separators: `[SYSTEM PROMPT]\n{content}` (if `USE_GEM_MODE=false`), `[USER]\n{content}`, `[ASSISTANT]\n{content}`. Sections are separated by `\n\n---\n\n`. | A human can visually identify the system/user/assistant sections in the clipboard in less than 5 seconds. |
| **REQ-2.2.3** | **Timestamped console notification** | The proxy must display in the console: (a) the time in `HH:MM:SS` format, (b) the prompt size in characters, (c) the 5 numbered action instructions for the user, (d) the remaining timeout delay. | The console displays these 4 elements for each request received. |

##### REQ-2.3 — Sub-domain: Response Wait and Capture (Downlink)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.3.1** | **Asynchronous clipboard polling every second** | The proxy must monitor the clipboard via an `asyncio` loop with `await asyncio.sleep(POLLING_INTERVAL)` (default: 1.0 second). The loop must not block the main FastAPI thread. | During polling, the FastAPI server still responds to `GET /health` without delay. |
| **REQ-2.3.2** | **Change detection by MD5 hash comparison** | The proxy must calculate `MD5(initial_copied_content)` at the time of copying, then compare with `MD5(current_clipboard_content)` at each polling iteration. Detection is triggered as soon as the two hashes differ. | Detection occurs within 2 seconds of the user copying the Gemini response (maximum 1 polling cycle). |
| **REQ-2.3.3** | **Configurable timeout with HTTP 408 response** | If no clipboard change is detected within the `TIMEOUT_SECONDS` delay (default: 300 seconds), the proxy must return an HTTP 408 (Request Timeout) response to Roo Code with the message: `"Timeout: Relancez votre requête dans Roo Code."` | With `TIMEOUT_SECONDS=5` (test), the proxy returns HTTP 408 after 5 seconds without user action. |
| **REQ-2.3.4** | **Validation of Roo Code XML tag presence** | After detecting a clipboard change, the proxy must verify the presence of at least one of the following Roo Code XML tags in the captured content: `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, `<ask_followup_question>`, `<replace_in_file>`, `<list_files>`, `<search_files>`, `<browser_action>`, `<new_task>`. If no tag is present, a warning is displayed in the console (non-blocking). | With a valid Gemini response, no warning. With text without XML tags, the warning is displayed but the response is still transmitted to Roo Code. |

##### REQ-2.4 — Sub-domain: Re-injection to Roo Code

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.4.1** | **SSE streaming support in a single chunk** | The proxy must detect if the request contains `"stream": true` and return a Server-Sent Events (SSE) format response with: (1) a content chunk, (2) an end chunk with `"finish_reason": "stop"`, (3) the `data: [DONE]` line. If `"stream": false`, return a complete non-streamed JSON response. | Roo Code configured with streaming enabled receives the response without error. Roo Code configured without streaming also receives the response without error. |
| **REQ-2.4.2** | **Complete OpenAI JSON format for non-streamed response** | The non-streamed JSON response must contain exactly the fields: `id` (format `chatcmpl-proxy-{8 hex chars}`), `object` (`"chat.completion"`), `created` (Unix timestamp), `model` (value of the `model` field from the request), `choices[0].index` (`0`), `choices[0].message.role` (`"assistant"`), `choices[0].message.content` (raw Gemini content), `choices[0].finish_reason` (`"stop"`), `usage.prompt_tokens` (`0`), `usage.completion_tokens` (`0`), `usage.total_tokens` (`0`). | The JSON response is parseable by Roo Code without deserialization error. |
| **REQ-2.4.3** | **HTTP 200 response with Content-Type application/json** | The HTTP response must have status 200 OK and the `Content-Type: application/json` header for the non-streamed response, or `Content-Type: text/event-stream` for the SSE response. | Response headers are correct in both modes. |
| **REQ-2.4.4** | **Complete preservation of Gemini content** | The content of the Gemini response (including Roo Code XML tags) must be transmitted as-is in `choices[0].message.content`, without any modification, deletion, addition, or character transformation. | The content in `choices[0].message.content` is identical (byte-for-byte) to the content copied from Gemini. |

---

### 3.3 Domain 3 — Agility & Role Segregation (REQ-3.x)

#### REQ-3.0 — Virtual Agile Team
The system must simulate a complete Scrum team via Roo Code Custom Modes, each with distinct and non-overlapping responsibilities, behaviors, and access permissions.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-3.1** | **4 Agile personas in `.roomodes`** | The `.roomodes` file must define exactly 4 Custom Modes with the slugs: `product-owner`, `scrum-master`, `developer`, `qa-engineer`. Each mode must have a `roleDefinition` (behavioral system prompt) and permission `groups`. | The 4 modes appear in the Roo Code mode selector after loading `.roomodes`. |
| **REQ-3.2** | **Strict permission segregation (RBAC)** | The permissions of each persona are defined by the following matrix (see section 4.1). No persona can access resources outside its matrix. | RBAC test: the Product Owner cannot create a `.py` file. The QA Engineer cannot modify `src/`. The Scrum Master cannot execute test commands. |
| **REQ-3.3** | **Behavioral refusal of out-of-scope actions** | Each persona must explicitly refuse requests outside its role and suggest the appropriate persona. This refusal is inscribed in the `roleDefinition` of each mode. | If the `product-owner` mode receives "Write Python code", it responds by refusing and suggesting switching to `developer` mode. |
| **REQ-3.4** | **Scrum Master: pure facilitator without test execution** | The Scrum Master can read all files (including `docs/qa/`), write to `memory-bank/` and `docs/`, and execute only Git commands (`git add`, `git commit`, `git status`, `git log`). It cannot execute test commands or modify source code. | The Scrum Master can read a QA report in `docs/qa/` but cannot execute `pytest` or `npm test`. |

---

### 3.4 Domain 4 — Persistence & Memory Bank (REQ-4.x)

#### REQ-4.0 — Persistent Contextual Memory
The system must maintain absolute context continuity between development sessions via a structured, versionable, and human-readable Markdown file system.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-4.1** | **Storage in `memory-bank/` versioned under Git** | All contextual memory must reside in the `memory-bank/` directory at the project root. This directory must be included in Git tracking (not excluded by `.gitignore`). | `git ls-files memory-bank/` lists the 7 Memory Bank files. |
| **REQ-4.2** | **Mandatory sequence CHECK → CREATE → READ → ACT** | At each session startup, the agent must follow this exact and non-negotiable sequence: (1) CHECK the existence of `activeContext.md` and `progress.md`. (2) If absent: CREATE immediately from the templates defined in `.clinerules`, then proceed to step 3. (3) READ `activeContext.md` then `progress.md`. (4) ACT on the user's request. This sequence applies to all modes and all sessions without exception. | After closing and reopening VS Code, the agent reads `activeContext.md` before any action. If files are manually deleted, the agent recreates them from templates before acting. |
| **REQ-4.3** | **Mandatory update before task closure** | Before executing `attempt_completion`, the agent must mandatorily update: (a) `activeContext.md` with the current state and next action, (b) `progress.md` with validated features. If an architecture decision was made: (c) `decisionLog.md` with a timestamped ADR. | The Git history shows a Memory Bank update commit before each code commit. |
| **REQ-4.4** | **7 distinct and non-overlapping thematic files** | The Memory Bank must be composed of exactly these 7 files, each with a unique responsibility: `projectBrief.md` (vision, non-goals, constraints), `productContext.md` (user stories, backlog), `systemPatterns.md` (architecture, conventions), `techContext.md` (stack, commands, env variables), `activeContext.md` (current task, current state), `progress.md` (phase and feature checklist), `decisionLog.md` (timestamped ADRs). | The 7 files exist in `memory-bank/` with non-redundant content. |
| **REQ-4.5** | **Git versioning of all Memory Bank modifications** | Any modification to a `memory-bank/*.md` file must be included in a Git commit with a message in the format `docs(memory): {description}`. | `git log --oneline -- memory-bank/` shows commits with the `docs(memory):` prefix. |

---

### 3.5 Domain 5 — Gemini Chrome Configuration (REQ-5.x)

#### REQ-5.0 — Gemini Web Interface Preparation
For the proxy to work end-to-end, the Gemini Chrome interface must be configured to respond in the format expected by Roo Code.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-5.1** | **Dedicated "Roo Code Agent" Gem with complete system prompt** | A "Gem" profile must be created in Gemini Web (gemini.google.com > Gems) with the exact name "Roo Code Agent". The Gem instructions must contain the entirety of the Roo Code system prompt defined in `template/prompts/SP-007-gem-gemini-roo-agent.md`. | The "Roo Code Agent" Gem exists in the Gemini interface. Its instructions correspond exactly to the content of `template/prompts/SP-007-gem-gemini-roo-agent.md`. |
| **REQ-5.2** | **Gemini responses exclusively in Roo Code XML tags** | The Gem must be configured to respond only with Roo Code XML tags, without courtesy text before the first tag or after the last. | On 5 test requests, Gemini responds with valid XML tags without extraneous text. |
| **REQ-5.3** | **Multi-turn conversation history maintenance** | The Gem must take into account the conversation history transmitted by the proxy in the clipboard to ensure response coherence across multiple consecutive exchanges. | A sequence of 3 related requests (create file → modify file → test file) produces coherent responses without repetition or contradiction. |

---

### 3.6 Domain 6 — Direct Cloud Mode via Anthropic API (REQ-6.x)

#### REQ-6.0 — Direct Connection to Anthropic Claude API
The system must allow Roo Code to connect directly to the official Anthropic API to use Claude Sonnet as the LLM backend, without intermediate proxy or human intervention.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-6.1** | **Valid Anthropic API key stored securely** | The user must have a valid Anthropic API key in the format `sk-ant-api03-...`. This key must be stored exclusively in the encrypted settings of the Roo Code extension (VS Code SecretStorage). | The API key is functional (successful connection test). It does not appear in any project file (`.env`, `.clinerules`, `.roomodes`, `memory-bank/`, etc.). |
| **REQ-6.2** | **Model `claude-sonnet-4-6` as reference** | Roo Code must be configured to use the model `claude-sonnet-4-6`. This model natively responds to Roo Code XML tags without additional response format configuration. **Maintenance note:** Periodically check the list of available models at https://docs.anthropic.com/en/docs/about-claude/models and update this document with the latest stable version of the Sonnet family. | Roo Code sends a request to `claude-sonnet-4-6` and receives a response with valid XML tags. |
| **REQ-6.3** | **Connection via Roo Code's native "Anthropic" provider** | The connection to the Anthropic API must use the native "Anthropic" provider integrated in Roo Code, without any proxy or middleware. The endpoint is `https://api.anthropic.com`. | Roo Code connects directly to `api.anthropic.com`. No local proxy process is required. |
| **REQ-6.4** | **Absolute prohibition on API key versioning** | The Anthropic API key must never appear in any project file, versioned or not. It is stored exclusively in VS Code SecretStorage (encrypted, not accessible from the file system). | `git grep "sk-ant"` in the repository returns zero results. |

---

### 3.7 Domain 7 — Central System Prompt Registry (REQ-7.x)

#### REQ-7.0 — Centralized System Prompt Registry
The system must maintain a `prompts/` directory containing a canonical and up-to-date version of each system prompt used in the workbench, with precise identification of its deployment target.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-7.1** | **7 canonical SP files in `prompts/`** | The `prompts/` directory must contain exactly 7 canonical files named `SP-001-ollama-modelfile-system.md` to `SP-007-gem-gemini-roo-agent.md`, plus a `README.md` index file. Each SP file must have a YAML header with the fields: `id`, `name`, `version` (MAJOR.MINOR.PATCH format), `last_updated`, `status`, `target_type`, `target_file`, `target_field`, `target_location`, `depends_on`, `changelog`. | `Get-ChildItem prompts/` lists 8 files (7 SP + README). Each SP has a valid YAML header with all required fields. |
| **REQ-7.2** | **Unambiguous identification of the deployment target** | Each SP file must specify: (a) `target_file`: exact path of the target file (e.g.: `Modelfile`, `.clinerules`, `.roomodes`), (b) `target_field`: exact field in the target file (e.g.: `SYSTEM block`, `entire file`, `customModes[2].roleDefinition`), (c) `target_location`: deployment procedure in natural language. For SP-007 (Gemini Gem, external to Git): `hors_git: true` and documented manual procedure. | A developer can deploy any SP without ambiguity by reading only its canonical file. |
| **REQ-7.3** | **Mandatory consistency before commit (RULE 6)** | Any modification to an artifact linked to a prompt (`template/proxy.py`, `.roomodes`, `.clinerules`, `Modelfile`) must trigger a verification and update of the corresponding SP file in `prompts/`. This obligation is inscribed in RULE 6 of `.clinerules`. | A commit modifying `.clinerules` without updating `template/prompts/SP-002-clinerules-global.md` is blocked by the pre-commit hook (REQ-8.2). |
| **REQ-7.4** | **Semantic versioning of prompts** | Each SP file must maintain a `changelog` with semantic version number (MAJOR.MINOR.PATCH) and description of modifications. The version is incremented with each modification: PATCH for minor correction, MINOR for rule addition, MAJOR for complete overhaul. | The `changelog` field of each SP contains at least one entry. The version in the YAML header corresponds to the last entry in the changelog. |
| **REQ-7.5** | **Documented manual deployment for SP-007** | SP-007 (Gemini Gem) being external to Git, its manual deployment procedure must be documented in the SP-007 file itself. Any commit modifying SP-007 must include the mention `MANUAL DEPLOYMENT REQUIRED` in the commit message. | SP-007 contains `hors_git: true` in its YAML header. RULE 6.2 of `.clinerules` requires the mention in the commit message. |

---

### 3.8 Domain 8 — Automatic Prompt Consistency Verification (REQ-8.x)

#### REQ-8.0 — Automatic Detection of Prompt/Artifact Desynchronization
The system must provide an automatic mechanism for detecting desynchronizations between the canonical SP files in the `prompts/` registry and their deployed target artifacts (`.clinerules`, `.roomodes`, `Modelfile`).

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-8.1** | **PowerShell script `template/template/scripts/check-prompts-sync.ps1`** | A PowerShell script must compare the content of each canonical SP file with its deployed target artifact. The comparison must be normalized: (a) line ending normalization (`\r\n` → `\n` via PowerShell double quotes), (b) JSON deserialization for `.roomodes` before extracting the `roleDefinition`, (c) extraction of content between the markdown code block tags of the SP file via robust regex. The script returns exit code 0 if everything is synchronized, exit code 1 if desynchronization is detected. | `.\scripts\check-prompts-sync.ps1` returns exit code 0 after a clean installation. Returns exit code 1 if `.clinerules` is modified without updating SP-002. |
| **REQ-8.2** | **Blocking Git pre-commit hook** | A Git hook `.git/hooks/pre-commit` must automatically call `check-prompts-sync.ps1` before each commit and block the commit (exit code 1) if a desynchronization is detected. The blocking message must indicate which SP is desynchronized. | A commit with `.clinerules` modified but SP-002 not updated is blocked with an explanatory message. A commit with both files updated passes without blocking. |
| **REQ-8.3** | **Verification report with readable diff** | The script must produce a structured report with: (a) status per SP (`[SYNC]` in green or `[DESYNC]` in red), (b) SP file name and target artifact name, (c) in case of desynchronization: display of the first 200 characters of the canonical SP content AND the deployed content to allow visual identification of the difference. | A user can identify in less than 10 seconds which prompt is desynchronized and what the approximate difference is. |
| **REQ-8.4** | **Exclusion of SP-007 from automatic verification** | SP-007 (Gemini Gem, external to Git) must be excluded from automatic verification. The script must display `[MANUAL] SP-007: MANUAL VERIFICATION REQUIRED` in magenta without blocking the commit. This message counts as a warning, not an error. | The script displays the `[MANUAL]` message for SP-007 but returns exit code 0 if the other SPs are synchronized. |

---

## 4. Traceability Matrices

### 4.1 RBAC Permission Matrix by Persona

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| Read all files (`read`) | ✅ | ✅ | ✅ | ✅ |
| Write `memory-bank/productContext.md` | ✅ | ✅ | ✅ | ❌ |
| Write `memory-bank/*.md` (all) | ❌ | ✅ | ✅ | ❌ |
| Write `docs/*.md` (documentation) | ✅ | ✅ | ✅ | ❌ |
| Write `docs/qa/*.md` (QA reports) | ❌ | ❌ | ❌ | ✅ |
| Write source code (`src/`, `*.py`, etc.) | ❌ | ❌ | ✅ | ❌ |
| General terminal execution (`command`) | ❌ | ❌ | ✅ | ❌ |
| Execute Git commands only | ❌ | ✅ | ✅ | ❌ |
| Execute test commands | ❌ | ❌ | ✅ | ✅ |
| Browser access (`browser`) | ❌ | ❌ | ✅ | ✅ |
| MCP access (`mcp`) | ❌ | ❌ | ✅ | ❌ |

**Git commands authorized for the Scrum Master:** `git add`, `git commit`, `git status`, `git log` only.
**Test commands authorized for the QA Engineer:** `npm test`, `npm run test`, `pytest`, `python -m pytest`, `dotnet test`, `go test`, `git status`, `git log`.

### 4.2 Requirements Traceability Matrix

| Requirement ID | Domain | Priority | Dependencies |
| :--- | :--- | :--- | :--- |
| REQ-000 | Foundational | CRITICAL | — |
| REQ-1.0 | Local Engine | HIGH | REQ-000 |
| REQ-1.1 | Local Engine — Model | HIGH | REQ-1.0 |
| REQ-1.2 | Local Engine — Context | HIGH | REQ-1.0 |
| REQ-1.3 | Local Engine — Determinism | HIGH | REQ-1.0 |
| REQ-1.4 | Local Engine — Boomerang | MEDIUM | REQ-1.1 |
| REQ-2.0 | Hybrid Proxy | HIGH | REQ-000 |
| REQ-2.1.1 | Proxy — Server | CRITICAL | REQ-2.0 |
| REQ-2.1.2 | Proxy — OpenAI Format | CRITICAL | REQ-2.1.1 |
| REQ-2.1.3 | Proxy — Message extraction | HIGH | REQ-2.1.1 |
| REQ-2.1.4 | Proxy — System prompt filtering | MEDIUM | REQ-2.1.3 |
| REQ-2.1.5 | Proxy — Image cleaning | MEDIUM | REQ-2.1.3 |
| REQ-2.2.1 | Proxy — Clipboard uplink | CRITICAL | REQ-2.1.3 |
| REQ-2.2.2 | Proxy — Readable format | HIGH | REQ-2.2.1 |
| REQ-2.2.3 | Proxy — Console notification | HIGH | REQ-2.2.1 |
| REQ-2.3.1 | Proxy — Async polling | CRITICAL | REQ-2.2.1 |
| REQ-2.3.2 | Proxy — MD5 hash detection | CRITICAL | REQ-2.3.1 |
| REQ-2.3.3 | Proxy — Timeout HTTP 408 | HIGH | REQ-2.3.1 |
| REQ-2.3.4 | Proxy — XML tag validation | MEDIUM | REQ-2.3.2 |
| REQ-2.4.1 | Proxy — SSE Streaming | CRITICAL | REQ-2.3.2 |
| REQ-2.4.2 | Proxy — OpenAI JSON Format | CRITICAL | REQ-2.4.1 |
| REQ-2.4.3 | Proxy — HTTP Headers | CRITICAL | REQ-2.4.1 |
| REQ-2.4.4 | Proxy — Content preservation | HIGH | REQ-2.4.1 |
| REQ-3.0 | Agility | HIGH | REQ-000 |
| REQ-3.1 | Agility — 4 personas | HIGH | REQ-3.0 |
| REQ-3.2 | Agility — RBAC | HIGH | REQ-3.1 |
| REQ-3.3 | Agility — Behavioral refusal | MEDIUM | REQ-3.2 |
| REQ-3.4 | Agility — SM pure facilitator | HIGH | REQ-3.2 |
| REQ-4.0 | Memory | HIGH | REQ-000 |
| REQ-4.1 | Memory — Git Storage | CRITICAL | REQ-4.0 |
| REQ-4.2 | Memory — CHECK→CREATE→READ→ACT sequence | CRITICAL | REQ-4.1 |
| REQ-4.3 | Memory — Write before closure | CRITICAL | REQ-4.1 |
| REQ-4.4 | Memory — 7 thematic files | HIGH | REQ-4.1 |
| REQ-4.5 | Memory — Git versioning | MEDIUM | REQ-4.1 |
| REQ-5.0 | Gemini Config | HIGH | REQ-2.0 |
| REQ-5.1 | Gemini — Dedicated Gem | CRITICAL | REQ-5.0 |
| REQ-5.2 | Gemini — XML Format | CRITICAL | REQ-5.1 |
| REQ-5.3 | Gemini — Multi-turn history | HIGH | REQ-5.1 |
| REQ-6.0 | Direct Cloud API | HIGH | REQ-000 |
| REQ-6.1 | Cloud — Secure API key | CRITICAL | REQ-6.0 |
| REQ-6.2 | Cloud — Model claude-sonnet-4-6 | CRITICAL | REQ-6.0 |
| REQ-6.3 | Cloud — Native Roo Code provider | CRITICAL | REQ-6.0 |
| REQ-6.4 | Cloud — API key versioning prohibition | CRITICAL | REQ-6.1 |
| REQ-7.0 | Prompt Registry | HIGH | REQ-000 |
| REQ-7.1 | Registry — 7 canonical SP files | HIGH | REQ-7.0 |
| REQ-7.2 | Registry — Unambiguous targets | CRITICAL | REQ-7.1 |
| REQ-7.3 | Registry — Consistency before commit | CRITICAL | REQ-7.1, REQ-5.x |
| REQ-7.4 | Registry — Semantic versioning | HIGH | REQ-7.1 |
| REQ-7.5 | Registry — Manual deployment SP-007 | HIGH | REQ-7.2, REQ-5.x |
| REQ-8.0 | Consistency Verification | HIGH | REQ-7.0 |
| REQ-8.1 | Verification — Normalized PowerShell script | HIGH | REQ-7.1, REQ-7.2 |
| REQ-8.2 | Verification — Blocking pre-commit hook | HIGH | REQ-8.1 |
| REQ-8.3 | Verification — Report with readable diff | MEDIUM | REQ-8.1 |
| REQ-8.4 | Verification — SP-007 exclusion | HIGH | REQ-7.5, REQ-8.1 |

---

## 5. Constraints and Non-Goals

### 5.1 Constraints

- The system relies on two machines: the Windows laptop `pc` (VS Code, Roo Code, Chrome, proxy.py) and the headless Linux server `calypso` (Ollama, LLM models, RTX 5060 Ti 16 GB), connected via Tailscale. No paid cloud infrastructure is required (except Cloud Mode which involves Anthropic API costs per usage).
- The Gemini Chrome proxy relies on minimal human intervention (copy-paste): it is not a fully automated system.
- The quality of responses in Gemini Chrome mode depends on the availability and behavior of the Gemini web interface (outside the system's control).
- Cloud Mode (Claude API) involves per-usage costs according to current Anthropic pricing.
- The Ollama model `mychen76/qwen3_cline_roocode:32b` is an external dependency without a documented fallback — its availability on Ollama Hub is an installation precondition.

### 5.2 Non-Goals

- This system does NOT aim to automate copy-pasting to Gemini Chrome (no browser automation like Selenium).
- This system does NOT aim to manage multi-user projects or distributed environments.
- This system does NOT aim to support LLM models other than the three modes documented in this version 1.0.
- This system does NOT aim to replace a real Agile project management tool (Jira, Linear, etc.) — it simulates Agile roles for AI-assisted development.
- The Proxy Gemini Mode does NOT support Boomerang Tasks (`new_task`) — two concurrent Roo Code instances share the same clipboard, creating a deadlock. Use Local Mode (Ollama) or Cloud Mode (Claude API) for tasks requiring sub-agents.

### 5.3 Comparative Table of the 3 LLM Modes

| Criterion | Local Mode (Ollama) | Proxy Mode (Gemini Chrome) | Cloud Mode (Claude API) |
| :--- | :--- | :--- | :--- |
| **Cost** | Free | Free | Paid (per usage) |
| **Human intervention** | None | Copy-paste per request | None |
| **Reasoning quality** | High (32B local) | Very high (Gemini Pro) | Very high (Claude Sonnet) |
| **Speed** | Depends on hardware | Depends on human | Fast (direct API) |
| **Data sovereignty** | Total (100% local) | Partial (data sent to Google) | Partial (data sent to Anthropic) |
| **Availability** | Always (Tailscale active) | Requires Chrome + Google account | Requires Internet + API key |
| **Streaming** | Native Ollama | SSE in a single chunk (proxy) | Native Anthropic |
| **Roo Code configuration** | Provider: Ollama | Provider: OpenAI Compatible | Provider: Anthropic |
| **PRD Requirements** | REQ-1.x | REQ-2.x, REQ-5.x | REQ-6.x |

---

## Appendix A — References Table

| Ref. | Type | Title / Identifier | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Internal document | `workbench/DOC1-PRD-Workbench-Requirements.md` | This document — Product Requirements Document v2.0 |
| [DOC2] | Internal document | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Architecture, Solution and Technical Stack v2.0 |
| [DOC3] | Internal document | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Complete Sequential Implementation Plan v3.0 (Phases 0–12) |
| [DOC4] | Internal document | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Workbench Deployment Guide for new and existing projects |
| [DOC5] | Internal document | `workbench/DOC5-GUIDE-Project-Development-Process.md` | Agile Application Process Manual v1.0 — process, artifact nomenclature, agentic anti-risks, session protocols |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | System prompt of the Ollama Modelfile (SYSTEM block) |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Canonical content of the `.clinerules` file (6 imperative rules) |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | `roleDefinition` of the Product Owner persona in `.roomodes` |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | `roleDefinition` of the Scrum Master persona in `.roomodes` |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | `roleDefinition` of the Developer persona in `.roomodes` |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` of the QA Engineer persona in `.roomodes` |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Instructions for the Gemini Gem "Roo Code Agent" (manual deployment, outside Git) |
| [LAAW] | External source | LAAW Blueprint — mychen76 | "Local Agentic Agile Workflow" Blueprint — main source of inspiration for the Memory Bank and Agile personas |
| [PROXY] | External source | Gemini Chrome API Proxy | Network-clipboard bridge mechanism allowing Roo Code to use Gemini Web for free |
| [OLLAMA] | External tool | https://ollama.com | Local LLM inference engine, manages Qwen3 models |
| [ANTHROPIC] | External API | https://api.anthropic.com | Official Anthropic API for Claude Sonnet |
| [GEMINI] | External interface | https://gemini.google.com | Google's Gemini web interface, used in Chrome Proxy mode |
| [ROOCODE] | VS Code extension | Roo Code (VS Code extension) | Central agentic execution engine — orchestrates all components |
| [OPENAI-FMT] | Standard | OpenAI Chat Completions Format | `/v1/chat/completions` API standard emulated by the proxy for Roo Code compatibility |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | MAJOR.MINOR.PATCH versioning convention used for SP files and the workbench |

---

## Appendix B — Abbreviations Table

| Abbreviation | Full Form | Explanation |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Timestamped record of an architecture decision with context, decision made, and consequences. Stored in `memory-bank/decisionLog.md`. |
| **API** | Application Programming Interface | Programming interface allowing two software systems to communicate. Here: Ollama API (local), Anthropic API (cloud), OpenAI API (emulated format). |
| **ASGI** | Asynchronous Server Gateway Interface | Python standard for asynchronous web servers. Uvicorn is an ASGI server used by FastAPI. |
| **DA** | Architecture Decision | Identifier for architecture decisions in DOC2 (e.g.: DA-001, DA-014). Each DA justifies a technical choice and references the PRD requirements addressed. |
| **GEM** | Gemini Gem | Custom profile in the Gemini Web interface (gemini.google.com > Gems) containing a dedicated system prompt. Here: "Roo Code Agent" with SP-007. |
| **Git** | — (proper noun) | Distributed version control system. Used to version source code, the Memory Bank, and configuration files. |
| **GPU** | Graphics Processing Unit | Graphics processor used to accelerate inference of local LLM models via Ollama. |
| **HTTP** | HyperText Transfer Protocol | Web communication protocol. The proxy listens on HTTP (localhost:8000). The Anthropic API uses HTTPS. |
| **HTTPS** | HTTP Secure | Encrypted version of HTTP. Used for connections to the Anthropic API and Gemini Web. |
| **JSON** | JavaScript Object Notation | Structured text data format. Used for `.roomodes`, OpenAI API responses, and proxy requests. |
| **LAAW** | Local Agentic Agile Workflow | Local agentic development blueprint created by mychen76, main source of inspiration for the Memory Bank and Agile personas of the workbench. |
| **LLM** | Large Language Model | Large language model. Examples: Qwen3-32B (local via Ollama), Gemini Pro (Google cloud), Claude Sonnet (Anthropic cloud). |
| **MD5** | Message Digest 5 | Hashing algorithm used by the proxy to detect clipboard changes (before/after hash comparison). |
| **MCP** | Model Context Protocol | Roo Code extension protocol allowing integration of external tools. Accessible only to the Developer persona. |
| **NTFS** | New Technology File System | Windows file system used to store the Memory Bank and configuration files. |
| **PO** | Product Owner | Agile persona responsible for product vision, User Stories, and backlog. Corresponds to the `product-owner` mode in `.roomodes`. |
| **PRD** | Product Requirements Document | Product requirements document. This document (DOC1) defines all atomic requirements of the workbench system. |
| **RBAC** | Role-Based Access Control | Role-based access control. Each Agile persona has a precise permission matrix defining what it can read, write, and execute. |
| **REQ** | Requirement | Identifier for requirements in this PRD (e.g.: REQ-000, REQ-2.1.4). Format: REQ-{domain}.{sub-domain}. |
| **REST** | Representational State Transfer | Architectural style for web APIs. Ollama exposes a REST API on localhost:11434. |
| **SM** | Scrum Master | Pure facilitator Agile persona: manages the Memory Bank and Git commits, but does not code and does not execute tests. |
| **SP** | System Prompt | Canonical file from the `template/prompts/` registry containing a system prompt with YAML metadata (id, version, target, changelog). |
| **SSE** | Server-Sent Events | Unidirectional HTTP streaming protocol (server → client). The proxy returns Gemini responses in SSE when `stream: true`. |
| **the workbench** | Agentic Agile Workbench | Name of the system described in this document. Combines Roo Code, Ollama, the Gemini Chrome proxy, and the Anthropic API in a unified agentic development environment. |
| **VRAM** | Video Random Access Memory | Graphics card memory. The Qwen3-32B model requires 8+ GB of VRAM for optimal GPU inference. |
| **VS Code** | Visual Studio Code | Microsoft code editor, the workbench's primary development environment. |
| **YAML** | YAML Ain't Markup Language | Human-readable data serialization format. Used for the headers of canonical SP files. |

---

## Appendix C — Glossary

| Term | Definition |
| :--- | :--- |
| **Agentic agent** | AI program capable of executing autonomous actions (reading/writing files, executing commands, calling APIs) in response to natural language instructions, without human intervention at each step. |
| **Workbench** | This repository (`agentic-agile-workbench`). Contains the reusable tools, rules, and processes for developing application projects. Contrasts with the "project" which contains the business code. |
| **Roo Code XML tags** | Special syntax used by Roo Code to trigger actions: `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Any LLM connected to Roo Code must respond with these tags. |
| **Boomerang Tasks** | Roo Code mechanism allowing the main agent (32B) to delegate a sub-task to a secondary model (7B), then retrieve the result in its own decision loop. |
| **Clipboard** | Temporary memory area of Windows (Ctrl+C / Ctrl+V). The proxy uses the clipboard as a communication channel between Roo Code and Gemini Web. |
| **Git Commit** | Versioned snapshot of the repository state. Each significant modification (code, Memory Bank, configuration) must be the subject of a commit with a descriptive message in Conventional Commits format. |
| **Conventional Commits** | Commit message convention: `type(scope): description`. Types used: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`. |
| **Determinism** | Property of an LLM to produce stable and reproducible responses. Achieved by fixing `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` in the Modelfile. |
| **Context window** | Maximum number of tokens an LLM can process simultaneously. Fixed at 128K tokens (`num_ctx 131072`) to allow loading of source code AND the Memory Bank. |
| **Fine-tuning** | Additional training of an LLM model on specific data. `mychen76/qwen3_cline_roocode:32b` is fine-tuned for Roo Code Tool Calling. |
| **Gemini Gem** | Custom profile in the Gemini Web interface containing a permanent system prompt. The "Roo Code Agent" Gem contains SP-007 and responds exclusively with Roo Code XML tags. |
| **Git pre-commit hook** | Script automatically executed by Git before each commit. Used to verify prompt consistency (REQ-8.2) and block the commit if desynchronization is detected. |
| **Memory Bank** | System of 7 Markdown files in `memory-bank/` that persist context between Roo Code sessions. Replaces the LLM's volatile memory with durable and auditable memory. |
| **Modelfile** | Ollama configuration file defining the base model, inference parameters, and system prompt. Compiled with `ollama create uadf-agent -f Modelfile`. |
| **Cloud Mode** | Roo Code configuration using the direct Anthropic API (`claude-sonnet-4-6`). Fully automated, paid per usage, requires an API key. |
| **Local Mode** | Roo Code configuration using Ollama locally (`mychen76/qwen3_cline_roocode:32b`). Free, sovereign, works offline. |
| **Proxy Mode** | Roo Code configuration using the local FastAPI proxy that relays requests to Gemini Web via the clipboard. Free, requires human intervention (copy-paste). |
| **Agile Persona** | Roo Code mode simulating a Scrum role: Product Owner, Scrum Master, Developer, QA Engineer. Each persona has a `roleDefinition` (behavior) and `groups` (RBAC permissions). |
| **Polling** | Periodic state checking technique. The proxy checks the clipboard every second (`asyncio.sleep(1.0)`) to detect the Gemini response. |
| **Proxy** | Network intermediary. Here: local FastAPI server (`template/proxy.py`) that intercepts Roo Code requests, relays them to Gemini Web via the clipboard, and returns the response to Roo Code. |
| **Prompt registry** | `template/prompts/` directory containing the canonical and versioned versions of all workbench system prompts. Single source of truth. |
| **CHECK→CREATE→READ→ACT sequence** | Mandatory protocol at the start of each Roo Code session: (1) check the existence of Memory Bank files, (2) create them if absent, (3) read them, (4) act on the request. Defined in RULE 1 of `.clinerules`. |
| **SemVer** | Semantic Versioning. MAJOR.MINOR.PATCH format: MAJOR = breaking change, MINOR = backward-compatible new feature, PATCH = bug fix. |
| **System Prompt** | Permanent instructions given to an LLM before any user interaction. Defines the behavior, rules, and constraints of the agent. |
| **Token** | LLM processing unit. Approximately 0.75 words in English. The 128K token window ≈ 96,000 words ≈ a medium-sized novel. |
| **Tool Calling** | Capability of an LLM to call external functions/tools by generating structured requests (JSON or XML). `mychen76/qwen3_cline_roocode:32b` is fine-tuned for Roo Code Tool Calling. |
| **VS Code SecretStorage** | Encrypted storage mechanism built into VS Code. Used to store the Anthropic API key securely, without ever writing it to a file. |
