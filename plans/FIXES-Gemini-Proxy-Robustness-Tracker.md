# Fix Tracker — Gemini Proxy Robustness Improvements
## Agentic Agile Workbench

**Source reviews:**
- Review 1: `plans/REVIEW-Gemini-Proxy-Path-Robustness.md` + `plans/REVIEW-Gemini-Proxy-Path-Robustness-Part2.md`
- Review 2: `plans/REVIEW2-Gemini-Proxy-Path-Robustness-After-Fixes.md` — POST-FIX VERIFICATION (FIX-001 to FIX-012)
- Review 3: `plans/REVIEW3-Gemini-Proxy-Path-Robustness-After-Review2-Fixes.md` ← **POST-FIX VERIFICATION (FIX-013 to FIX-019)**

**Created:** 2026-03-23
**Last updated:** 2026-03-23
**Status:** ✅ 12/12 fixes from Review 1 applied | ✅ 7/7 fixes from Review 2 applied | ⏳ 3/3 fixes from Review 3 pending (FIX-020, FIX-021, FIX-022)

---

## HOW TO USE THIS FILE

This file is the **single source of truth** for tracking the application of all recommended fixes from the robustness review. It is designed to survive across multiple Roo sessions, multiple days, and multiple human operators.

**At the start of any session working on these fixes:**
1. Read this file first
2. Identify the next pending fix (first `[ ]` item in the relevant priority group)
3. Apply the fix
4. Update the checkbox to `[x]` and fill in the "Applied" date and commit hash
5. Commit this file with the fix: `git commit -m "fix(proxy): FIX-XXX — [description]"`

**At the end of any session:**
- Ensure this file is committed with the latest status
- The Git history of this file IS the audit trail

---

## P0 — Blocking Fixes (apply before any regular use of proxy mode)

### FIX-001 — Proxy console: add "NOUVELLE conversation" instruction
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP-006 (Gemini conversation mode ambiguity — history duplication)
- **What to do:** In [`chat_completions()`](template/proxy.py) function, replace the single-line console print:
  ```python
  print(f"[{ts}] PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C")
  ```
  With a multi-line version that explicitly instructs the human to use a NEW conversation:
  ```python
  print(f"[{ts}] ══════════════════════════════════════════════════")
  print(f"[{ts}] PROMPT COPIE ({len(formatted)} chars) — ACTIONS REQUISES :")
  print(f"         1. Chrome → gemini.google.com → Gem 'Roo Code Agent'")
  print(f"         2. ⚠️  NOUVELLE conversation (ou effacer l'historique existant)")
  print(f"         3. Ctrl+V pour coller le prompt")
  print(f"         4. Attendre la fin de la reponse Gemini")
  print(f"         5. Ctrl+A puis Ctrl+C pour copier TOUTE la reponse")
  print(f"         ⚠️  Ne pas utiliser le presse-papiers pour autre chose !")
  print(f"         Timeout dans {TIMEOUT_SECONDS}s...")
  ```
- **Verification:** Start proxy, send a test request from Roo Code, confirm the new multi-line message appears in console with the "NOUVELLE conversation" warning.
- **Applied:** [x] Date: 2026-03-23 | Commit: fceb6fd

---

### FIX-002 — SP-007: add `replace_in_file` and `list_files` to Gem instructions
- **Status:** [x] DONE
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + **MANUAL DEPLOYMENT to Gemini Web**
- **Gap addressed:** SP-007 Issue 1 (missing critical XML tags — forces full file rewrites instead of surgical edits)
- **What to do:**
  1. In [`SP-007-gem-gemini-roo-agent.md`](template/prompts/SP-007-gem-gemini-roo-agent.md), add to the "FORMAT DE REPONSE OBLIGATOIRE" section after `<search_files>`:
     ```
     Pour modifier partiellement un fichier existant (PREFERER a write_to_file) :
     <replace_in_file>
     <path>chemin/vers/fichier</path>
     <diff>
     [bloc de recherche et remplacement]
     </diff>
     </replace_in_file>

     Pour lister les fichiers d'un dossier :
     <list_files>
     <path>dossier/a/lister</path>
     <recursive>false</recursive>
     </list_files>
     ```
  2. Add to "REGLES IMPORTANTES":
     ```
     7. Toujours utiliser replace_in_file plutot que write_to_file pour les modifications partielles
     8. Toujours utiliser list_files pour decouvrir la structure du projet avant de coder
     ```
  3. Increment SP-007 version from `1.0.0` to `1.1.0` in the YAML header
  4. Add changelog entry
  5. **MANUALLY deploy to Gemini Web** (gemini.google.com > Gems > "Roo Code Agent" > Edit > paste new instructions > Save)
  6. Commit with message: `chore(prompts): SP-007 v1.1.0 - add replace_in_file + list_files - DEPLOIEMENT MANUEL EFFECTUE`
- **Verification:** In Gemini Gem, send "Modifie la ligne 5 du fichier src/app.py" — Gemini should respond with `<replace_in_file>` not `<write_to_file>`.
- **Applied:** [x] Date: 2026-03-23 | Commit: 62ea897

---

### FIX-003 — Document Boomerang Tasks as unsupported in proxy mode
- **Status:** [x] DONE
- **Files to change:** `workbench/DOC1-PRD-Workbench-Requirements.md`, `workbench/DOC2-ARCH-Workbench-Technical-Design.md`, `workbench/DOC5-GUIDE-Project-Development-Process.md`
- **Gap addressed:** GAP-003 (Boomerang Tasks broken in proxy mode — no warning exists)
- **What to do:**
  1. In [`DOC1-PRD`](workbench/DOC1-PRD-Workbench-Requirements.md) section 5.2 Non-Goals, add:
     ```
     - Le Mode Proxy Gemini ne supporte PAS les Boomerang Tasks (new_task) — deux instances Roo Code
       concurrentes partagent le même presse-papiers, créant un deadlock. Utiliser le Mode Local
       (Ollama) ou le Mode Cloud (Claude API) pour les tâches nécessitant des sous-agents.
     ```
  2. In [`DOC2-ARCH`](workbench/DOC2-ARCH-Workbench-Technical-Design.md) section DA-005, add a note:
     ```
     ⚠️ LIMITATION MODE PROXY : Les Boomerang Tasks ne sont pas supportées en Mode Proxy Gemini.
     Le proxy est un endpoint unique partagé par toutes les instances Roo Code — les requêtes
     concurrentes de l'agent principal et du sous-agent créent un conflit de presse-papiers.
     ```
  3. In [`DOC5-GUIDE`](workbench/DOC5-GUIDE-Project-Development-Process.md) section 9.4 "Protocole de Changement de Backend LLM", add a limitations block (see Part2 section 9 for exact text)
- **Verification:** Search for "Boomerang" in all three docs — each should contain the limitation warning.
- **Applied:** [x] Date: 2026-03-23 | Commit: 51bf71a

---

## P1 — High Priority Fixes (apply before regular use)

### FIX-004 — Proxy: add try/except around `pyperclip.paste()`
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** P-003 (proxy crash if clipboard locked or contains non-text content)
- **What to do:** In [`_wait_clipboard()`](template/proxy.py) function, wrap `pyperclip.paste()` in try/except:
  ```python
  try:
      current = pyperclip.paste()
  except Exception as e:
      print(f"[{ts}] AVERTISSEMENT: Erreur acces presse-papiers: {e}")
      continue
  ```
- **Verification:** Lock clipboard with another app, confirm proxy prints warning and continues polling instead of crashing.
- **Applied:** [x] Date: 2026-03-23 | Commit: 10a4c81

---

### FIX-005 — Proxy: add request counter to console output
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** P-002 (human cannot distinguish which request is pending when multiple arrive)
- **What to do:** Add a module-level counter and include it in the console output:
  ```python
  _request_counter = 0

  @app.post("/v1/chat/completions")
  async def chat_completions(request: ChatRequest):
      global _request_counter
      _request_counter += 1
      req_num = _request_counter
      ts = datetime.now().strftime("%H:%M:%S")
      print(f"\n{'='*60}\n[{ts}] REQUETE #{req_num} | modele: {request.model} | stream: {request.stream}")
      ...
  ```
- **Verification:** Send 3 consecutive requests — console shows REQUEST #1, #2, #3.
- **Applied:** [x] Date: 2026-03-23 | Commit: 521baa9

---

### FIX-006 — Proxy: add minimum content length check
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP-005 (accidental clipboard overwrite with short content silently corrupts response)
- **What to do:** In [`_wait_clipboard()`](template/proxy.py), after detecting hash change, add:
  ```python
  if len(current) < 20:
      print(f"[{ts}] AVERTISSEMENT: Contenu trop court ({len(current)} chars): {repr(current[:50])}")
      print(f"[{ts}] Verifiez que vous avez copie la reponse Gemini complete (Ctrl+A puis Ctrl+C)")
  ```
- **Verification:** Copy a 5-char string while proxy is polling — warning should appear but response still transmitted (non-blocking by design).
- **Applied:** [x] Date: 2026-03-23 | Commit: 713403c

---

### FIX-007 — Test and document HTTP 408 behavior in Roo Code
- **Status:** [x] DONE
- **Files to change:** `workbench/DOC5-GUIDE-Project-Development-Process.md` section 9.6
- **Gap addressed:** GAP-004 (timeout recovery undefined)
- **What to do:**
  1. Test: Set `TIMEOUT_SECONDS=10` in proxy, send a request from Roo Code, do NOT copy anything for 10 seconds. Observe what Roo Code does (retries? aborts? shows error?).
  2. Document the observed behavior in DOC5 section 9.6 "Protocole de Gestion des Erreurs d'Agent":
     ```
     Timeout proxy (HTTP 408) :
     -> Comportement observé de Roo Code : [FILL IN AFTER TESTING]
     -> Action corrective : [FILL IN AFTER TESTING]
     ```
- **Verification:** Behavior documented in DOC5 with actual observed Roo Code response.
- **Applied:** [x] Date: 2026-03-23 | Commit: 8bfc3d1

---

### FIX-008 — Proxy: add MAX_HISTORY_CHARS truncation
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP-001 (clipboard size explosion on long conversations)
- **What to do:** Add a `MAX_HISTORY_CHARS` environment variable (default: 40000) and truncate oldest messages in `_format_prompt()` if the total exceeds the limit:
  ```python
  MAX_HISTORY_CHARS = int(os.getenv("MAX_HISTORY_CHARS", "40000"))

  def _format_prompt(messages: List[MessageContent]) -> str:
      parts = []
      for msg in messages:
          content = _clean_content(msg.content)
          if not content.strip():
              continue
          if msg.role == "system":
              if USE_GEM_MODE:
                  continue
              parts.append("[SYSTEM PROMPT]\n" + content)
          elif msg.role == "user":
              parts.append("[USER]\n" + content)
          elif msg.role == "assistant":
              parts.append("[ASSISTANT]\n" + content)
      
      full = "\n\n---\n\n".join(parts)
      if len(full) > MAX_HISTORY_CHARS:
          # Keep the last N chars, truncate from the beginning
          truncated = full[-MAX_HISTORY_CHARS:]
          # Find the first complete section boundary
          boundary = truncated.find("[USER]")
          if boundary > 0:
              truncated = "[...HISTORIQUE TRONQUE...]\n\n---\n\n" + truncated[boundary:]
          print(f"  AVERTISSEMENT: Historique tronque ({len(full)} -> {len(truncated)} chars)")
          return truncated
      return full
  ```
- **Verification:** Send a conversation with 20+ turns — clipboard content stays under 40,000 chars with truncation notice.
- **Applied:** [x] Date: 2026-03-23 | Commit: dbd43d7

---

## P2 — Medium Priority Fixes (quality improvements)

### FIX-009 — DOC5: add task chunking guidance for proxy mode
- **Status:** [x] DONE
- **File to change:** `workbench/DOC5-GUIDE-Project-Development-Process.md`
- **Gap addressed:** GAP-007 (cognitive load fatigue on long tasks)
- **What to do:** Add a new subsection 9.4.1 "Stratégie de découpage des tâches en Mode Proxy" with guidance on keeping tasks under 10 LLM turns.
- **Applied:** [x] Date: 2026-03-23 | Commit: 3a6c694

---

### FIX-010 — SP-007: make project context agnostic
- **Status:** [x] DONE
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + manual Gemini deployment
- **Gap addressed:** SP-007 Issue 2 (hardcoded UADF context)
- **What to do:** Replace the hardcoded "CONTEXTE DU PROJET" section with a generic instruction to read the Memory Bank for project context.
- **Applied:** [x] Date: 2026-03-23 | Commit: 7c38b41

---

### FIX-011 — DOC5: add proxy mode limitations to section 9.4
- **Status:** [x] DONE
- **File to change:** `workbench/DOC5-GUIDE-Project-Development-Process.md`
- **Gap addressed:** GAP-003, GAP-006, GAP-007 (undocumented limitations)
- **What to do:** Add "LIMITATIONS CONNUES DU MODE PROXY GEMINI" block to section 9.4 (see Part2 section 9 for exact text).
- **Applied:** [x] Date: 2026-03-23 | Commit: 3e9805f

---

### FIX-012 — SP-007: add `browser_action` and `new_task` with usage notes
- **Status:** [x] DONE
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + manual Gemini deployment
- **Gap addressed:** SP-007 Issue 1 (missing tags)
- **What to do:** Add `browser_action` and `new_task` to SP-007 with a note that `new_task` is not supported in proxy mode.
- **Applied:** [x] Date: 2026-03-23 | Commit: d7603c0

---

## Progress Summary (Review 1 — COMPLETE)

| Priority | Total | Done | Remaining |
| :--- | :---: | :---: | :---: |
| P0 — Blocking | 3 | 3 | 0 |
| P1 — High | 5 | 5 | 0 |
| P2 — Medium | 4 | 4 | 0 |
| **TOTAL Review 1** | **12** | **12** | **0** |

---

## Changelog

| Date | Session | Fix Applied | Commit |
| :--- | :--- | :--- | :--- |
| 2026-03-23 | Initial review | Tracker created | — |
| 2026-03-23 | Session 1 | FIX-001 — Console multi-ligne NOUVELLE conversation | fceb6fd |
| 2026-03-23 | Session 2 | FIX-002 — SP-007 v1.1.0 replace_in_file + list_files | 62ea897 |
| 2026-03-23 | Session 3 | FIX-003 — Boomerang Tasks limitation documentée (DOC1+DOC2+DOC5) | 51bf71a |
| 2026-03-23 | Session 4 | FIX-004 — try/except pyperclip.paste() dans _wait_clipboard() | 10a4c81 |
| 2026-03-23 | Session 5 | FIX-005 — Compteur de requetes #N dans la console (P-002) | 521baa9 |
| 2026-03-23 | Session 6 | FIX-006 — Verification longueur minimale contenu colle (GAP-005) | 713403c |
| 2026-03-23 | Session 7 | FIX-007 — Comportement HTTP 408 documenté dans DOC5 section 9.6 (GAP-004) | 8bfc3d1 |
| 2026-03-23 | Session 8 | FIX-008 — MAX_HISTORY_CHARS troncature historique dans _format_prompt() (GAP-001) | dbd43d7 |
| 2026-03-23 | Session 9 | FIX-009 — Subsection 9.4.1 découpage tâches Mode Proxy dans DOC5 (GAP-007) | 3a6c694 |
| 2026-03-23 | Session 10 | FIX-010 — SP-007 v1.2.0 contexte projet agnostique (Memory Bank) — DEPLOIEMENT MANUEL REQUIS | 7c38b41 |
| 2026-03-23 | Session 11 | FIX-011 — LIMITATIONS CONNUES DU MODE PROXY GEMINI ajoutées dans DOC5 section 9.4 (GAP-003, GAP-006, GAP-007) | 3e9805f |
| 2026-03-23 | Session 12 | FIX-012 — SP-007 v1.3.0 browser_action + new_task (avec avertissement proxy) — DEPLOIEMENT MANUEL REQUIS | d7603c0 |
| 2026-03-23 | Review 2 | REVIEW2 written — 3 regressions + 6 new gaps identified (FIX-013 to FIX-019 added) | — |

---

## REVIEW 2 FIXES — From `plans/REVIEW2-Gemini-Proxy-Path-Robustness-After-Fixes.md`

> These fixes address regressions and new gaps found during the post-fix verification (Review 2).
> Apply in order: P0 → P1 → P2.

---

## P0 — Blocking (Review 2) — apply before any regular use of proxy mode

### FIX-013 — SP-007: add exact `replace_in_file` diff format specification
- **Status:** [x] DONE
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + **MANUAL DEPLOYMENT to Gemini Web**
- **Gap addressed:** REG-003 + GAP R1-002 (`replace_in_file` promoted without format spec — always fails in practice)
- **What to do:**
  1. In [`SP-007-gem-gemini-roo-agent.md`](template/prompts/SP-007-gem-gemini-roo-agent.md), replace the `<replace_in_file>` diff placeholder `[bloc de recherche et remplacement]` with the exact format using the literal `<<<<<<< SEARCH`, `:start_line:[N]`, `-------`, `=======`, `>>>>>>> REPLACE` markers.
  2. Add Rule 10 to "REGLES IMPORTANTES": "Le format du diff pour replace_in_file est STRICT — utiliser exactement le format SEARCH/REPLACE. Ne pas utiliser le format unified diff (- / +). Le numero de ligne (:start_line:) est obligatoire."
  3. Increment SP-007 version from `1.3.0` to `1.4.0`
  4. Add changelog entry
  5. **MANUALLY deploy to Gemini Web** (gemini.google.com > Gems > "Roo Code Agent" > Edit > paste new instructions > Save)
  6. Commit with message: `chore(prompts): SP-007 v1.4.0 - add exact replace_in_file diff format - DEPLOIEMENT MANUEL REQUIS`
- **Verification:** In Gemini Gem, send "Modifie la ligne 5 du fichier src/app.py pour changer 'old' en 'new'" — Gemini should respond with `<replace_in_file>` using the SEARCH/REPLACE marker format, NOT unified diff (`-`/`+`).
- **Applied:** [x] Date: 2026-03-23 | Commit: 9cd8707

---

### FIX-014 — Proxy: make short-content check blocking + raise threshold to 100 chars
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** REG-001 (FIX-006 warns but still injects short/garbage content into Roo Code)
- **What to do:** In [`_wait_clipboard()`](template/proxy.py), replace the current non-blocking check (threshold 20, non-blocking) with a blocking version (threshold 100, `initial_hash = _hash(current)` then `continue`). Also update proxy version to `2.0.6` and add changelog entry.
- **Verification:** Copy a 50-char string (e.g., a URL) while proxy is polling — proxy should print warning and continue polling (NOT inject the URL into Roo Code).
- **Applied:** [x] Date: 2026-03-23 | Commit: 411bce3

---

## P1 — High Priority (Review 2)

### FIX-015 — Proxy: add `<new_task>` runtime guard in `_wait_clipboard()`
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP R1-003 (`<new_task>` not blocked at runtime — causes deadlock if Gemini ignores SP-007 Rule 9)
- **What to do:** In [`_wait_clipboard()`](template/proxy.py), after the length check and before `_validate_response()`, add a check: if `"<new_task>" in current`, print a critical error message, reset `initial_hash = _hash(current)`, and `continue` polling. This forces the human to copy a corrected response without `<new_task>`.
- **Verification:** Manually copy a string containing `<new_task>` while proxy is polling — proxy should print the error and continue polling (NOT inject into Roo Code).
- **Applied:** [x] Date: 2026-03-23 | Commit: 20e1485

---

### FIX-016 — Proxy: fix `_format_prompt()` truncation fallback for single-message overflow
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** REG-002 (FIX-008 truncation returns raw mid-message content when a single message exceeds `MAX_HISTORY_CHARS`)
- **What to do:** In [`_format_prompt()`](template/proxy.py), add an `else` branch to the truncation block: when `boundary = truncated.find("[USER]")` returns -1 (no `[USER]` found), use `full.rfind("[USER]")` to find the last user message and keep it intact with a truncation header. This ensures Gemini always receives a complete, context-headed message even when a single message exceeds the limit.
- **Verification:** Send a conversation where a single user message exceeds 40,000 chars (e.g., inject a large file content) — proxy should keep the full last `[USER]` message intact with the truncation header, not return a raw mid-message string.
- **Applied:** [x] Date: 2026-03-23 | Commit: 2542856

---

## P2 — Medium Priority (Review 2)

### FIX-017 — Proxy: add `asyncio.Lock()` for clipboard serialization
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP R1-004 (request counter not thread-safe — two concurrent requests both poll the clipboard and both return the same response)
- **What to do:** Add a module-level `_clipboard_lock = asyncio.Lock()`. In `chat_completions()`, wrap the `pyperclip.copy()` + `_wait_clipboard()` block with `async with _clipboard_lock:`. Add a console warning when a request is queued waiting for the lock.
- **Verification:** Send two simultaneous requests — second request should queue and wait, not race with the first.
- **Applied:** [x] Date: 2026-03-23 | Commit: 610afdc

---

### FIX-018 — Proxy: remove "ou effacer l'historique existant" from console instruction
- **Status:** [x] DONE
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP R1-001 (clearing history in existing Gemini conversation may not reload Gem system prompt â€” only "NOUVELLE conversation" is safe)
- **What to do:** In [`chat_completions()`](template/proxy.py), replace the line `"2. ⚠️  NOUVELLE conversation (ou effacer l'historique existant)"` with `"2. ⚠️  TOUJOURS ouvrir une NOUVELLE conversation Gemini"`.
- **Verification:** Console output no longer mentions "effacer l'historique".
- **Applied:** [x] Date: 2026-03-23 | Commit: b61d1ef

---

### FIX-019 — SP-007: fix `browser_action` template (separate examples per action type)
- **Status:** [x] DONE
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + **MANUAL DEPLOYMENT to Gemini Web**
- **Gap addressed:** GAP R1-006 (`browser_action` template shows all optional fields simultaneously — Gemini may include irrelevant fields in every response)
- **What to do:** Replace the single `browser_action` template block with separate minimal examples for each action type (`launch`, `click`, `type`, `screenshot`, `close`). Add note: "N'inclure que les champs pertinents pour l'action choisie."
- **Verification:** In Gemini Gem, send "Ouvre https://example.com" — Gemini should respond with only `<action>launch</action>` and `<url>` fields, no extra fields.
- **Applied:** [x] Date: 2026-03-23 | Commit: 642110d

---

## Progress Summary

| Priority | Total | Done | Remaining |
| :--- | :---: | :---: | :---: |
| **Review 1 — P0 Blocking** | 3 | 3 | 0 |
| **Review 1 — P1 High** | 5 | 5 | 0 |
| **Review 1 — P2 Medium** | 4 | 4 | 0 |
| **Review 2 — P0 Blocking** | 2 | 2 | 0 |
| **Review 2 — P1 High** | 2 | 2 | 0 |
| **Review 2 — P2 Medium** | 3 | 3 | 0 |
| **Review 3 — P2 Medium** | 3 | 0 | **3** |
| **TOTAL** | **22** | **19** | **3** |

---

## Changelog (continued)

| Date | Session | Fix Applied | Commit |
| :--- | :--- | :--- | :--- |
| 2026-03-23 | Review 2 | REVIEW2 written - 3 regressions + 6 new gaps identified (FIX-013 to FIX-019 added) | -- |
| 2026-03-23 | Session 13 | FIX-013 — SP-007 v1.4.0 format exact diff SEARCH/REPLACE pour replace_in_file + Regle 10 — DEPLOIEMENT MANUEL REQUIS | 9cd8707 |
| 2026-03-23 | Session 14 | FIX-014 — Verification longueur minimale BLOQUANTE (seuil 100 chars) dans _wait_clipboard() — proxy v2.0.6 (REG-001) | 411bce3 |
| 2026-03-23 | Session 15 | FIX-015 — Garde runtime <new_task> bloquant dans _wait_clipboard() — proxy v2.0.7 (GAP R1-003) | 20e1485 |
| 2026-03-23 | Session 16 | FIX-016 — Fallback troncature _format_prompt() pour message unique > MAX_HISTORY_CHARS — proxy v2.0.8 (REG-002) | 2542856 |
| 2026-03-23 | Session 17 | FIX-017 — asyncio.Lock() serialisation presse-papiers + avertissement file d'attente — proxy v2.0.9 (GAP R1-004) | 610afdc |
| 2026-03-23 | Session 18 | FIX-018 — Suppression "ou effacer l'historique existant" → TOUJOURS NOUVELLE conversation — proxy v2.1.0 (GAP R1-001) | b61d1ef |
| 2026-03-23 | Session 19 | FIX-019 — SP-007 v1.5.0 exemples browser_action separes par type d'action — DEPLOIEMENT MANUEL REQUIS (GAP R1-006) | 642110d |
| 2026-03-23 | Review 3 | REVIEW3 written — 1 minor regression + 5 residual gaps — FIX-020 to FIX-022 identified (0 blocking, 0 high, 3 medium) | bae81f2 |

---

## REVIEW 3 FIXES — From `plans/REVIEW3-Gemini-Proxy-Path-Robustness-After-Review2-Fixes.md`

> These fixes address the minor regression and low-priority gaps found during Review 3.
> All are P2 (medium/quality improvements) — no blocking or high-priority gaps remain.
> Apply in order: FIX-020 → FIX-021 → FIX-022.

---

## P2 — Medium Priority (Review 3)

### FIX-020 — Proxy: update version strings to v2.1.0
- **Status:** [ ] PENDING
- **File to change:** `template/proxy.py`
- **Gap addressed:** REG-001 (FIX-018 updated changelog comment to v2.1.0 but forgot to update the version strings in startup banner, /health endpoint, and FastAPI app version — all still show v2.0.9)
- **What to do:** In [`proxy.py`](template/proxy.py), update three version strings:
  1. Line 60: `app = FastAPI(title="le workbench Proxy", version="2.0.9")` → `version="2.1.0"`
  2. Line 227: `return {"status": "ok", "proxy": "le workbench", "version": "2.0.9", ...}` → `"version": "2.1.0"`
  3. Line 230: `print(f"{'='*60}\n  le workbench PROXY v2.0.9 | ...")` → `v2.1.0`
  4. Add changelog entry: `v2.1.0 - 2026-03-23 : FIX-020 — Correction des chaines de version (v2.0.9 -> v2.1.0) dans banner, /health et FastAPI app`
- **Verification:** Start proxy, confirm startup banner shows `v2.1.0`. Call `/health` endpoint, confirm `"version": "2.1.0"`.
- **Applied:** [ ] Date: — | Commit: —

---

### FIX-021 — SP-007: add explicit "7 dashes" note to Rule 10
- **Status:** [ ] PENDING
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + **MANUAL DEPLOYMENT to Gemini Web**
- **Gap addressed:** GAP R2-001 (SP-007 diff format does not explicitly state the dash count for the `-------` separator — Gemini may generate 6 or 8 dashes instead of 7, causing `apply_diff` to fail)
- **What to do:**
  1. In [`SP-007-gem-gemini-roo-agent.md`](template/prompts/SP-007-gem-gemini-roo-agent.md), update Rule 10 to add: "Le separateur est exactement **7 tirets** : `-------` (sept tirets, ni plus ni moins)."
  2. Also update the "REGLES DU FORMAT DIFF" block to add: "- Le separateur entre SEARCH et REPLACE est exactement 7 tirets : `-------`"
  3. Increment SP-007 version from `1.5.0` to `1.6.0`
  4. Add changelog entry
  5. **MANUALLY deploy to Gemini Web** (gemini.google.com > Gems > "Roo Code Agent" > Edit > paste new instructions > Save)
  6. Commit with message: `chore(prompts): SP-007 v1.6.0 - separateur 7 tirets explicite dans Regle 10 - DEPLOIEMENT MANUEL REQUIS`
- **Verification:** In Gemini Gem, send "Modifie la ligne 5 du fichier src/app.py" — Gemini should respond with exactly 7 dashes in the diff separator.
- **Applied:** [ ] Date: — | Commit: —

---

### FIX-022 — SP-007: add `ask_followup_question` template
- **Status:** [ ] PENDING
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + **MANUAL DEPLOYMENT to Gemini Web**
- **Gap addressed:** GAP R2-005 (`ask_followup_question` not documented in SP-007 FORMAT DE REPONSE OBLIGATOIRE — Gemini may use free text instead of the tag when asking clarifying questions)
- **What to do:**
  1. In [`SP-007-gem-gemini-roo-agent.md`](template/prompts/SP-007-gem-gemini-roo-agent.md), add to the "FORMAT DE REPONSE OBLIGATOIRE" section (after `attempt_completion`, before `browser_action`):
     ```
     Pour poser une question de clarification :
     <ask_followup_question>
     <question>La question a poser</question>
     <follow_up>
     <suggest>Suggestion de reponse 1</suggest>
     <suggest>Suggestion de reponse 2</suggest>
     </follow_up>
     </ask_followup_question>
     ```
  2. Increment SP-007 version from `1.6.0` to `1.7.0` (or from `1.5.0` to `1.6.0` if FIX-021 not yet applied — apply FIX-021 first)
  3. Add changelog entry
  4. **MANUALLY deploy to Gemini Web**
  5. Commit with message: `chore(prompts): SP-007 v1.7.0 - ajout template ask_followup_question - DEPLOIEMENT MANUEL REQUIS`
- **Verification:** In Gemini Gem, send "J'ai besoin d'une clarification sur le projet" — Gemini should respond with `<ask_followup_question>` tag, not free text.
- **Applied:** [ ] Date: — | Commit: —

---

## How to Start the Next Session (Review 3 Fixes)

Copy this prompt into Roo Code (any mode) to resume work on Review 3 fixes:

```
Lis le fichier plans/FIXES-Gemini-Proxy-Robustness-Tracker.md.
Identifie le prochain fix PENDING dans la section "REVIEW 2 FIXES", ordre P0 -> P1 -> P2.
Applique ce fix selon les instructions detaillees dans le tracker.
Une fois applique, mets a jour le tracker (checkbox + date + commit hash) et commite les deux fichiers ensemble.
```

---

## How to Start the Next Session (Review 3 Fixes)

Copy this prompt into Roo Code (any mode) to resume work on Review 3 fixes:

```
Lis le fichier plans/FIXES-Gemini-Proxy-Robustness-Tracker.md.
Identifie le prochain fix PENDING dans la section "REVIEW 3 FIXES", ordre FIX-020 -> FIX-021 -> FIX-022.
Applique ce fix selon les instructions detaillees dans le tracker.
Une fois applique, mets a jour le tracker (checkbox + date + commit hash) et commite les deux fichiers ensemble.
Note: FIX-021 et FIX-022 modifient SP-007 et necessitent un DEPLOIEMENT MANUEL sur Gemini Web.
```
