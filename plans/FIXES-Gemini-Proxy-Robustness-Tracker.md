# Fix Tracker — Gemini Proxy Robustness Improvements
## Agentic Agile Workbench

**Source review:** `plans/REVIEW-Gemini-Proxy-Path-Robustness.md` + `plans/REVIEW-Gemini-Proxy-Path-Robustness-Part2.md`  
**Created:** 2026-03-23  
**Last updated:** 2026-03-23
**Status:** 🟡 2/12 fixes applied

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
- **Applied:** [x] Date: 2026-03-23 | Commit: PENDING

---

### FIX-003 — Document Boomerang Tasks as unsupported in proxy mode
- **Status:** [ ] PENDING
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
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

## P1 — High Priority Fixes (apply before regular use)

### FIX-004 — Proxy: add try/except around `pyperclip.paste()`
- **Status:** [ ] PENDING
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
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-005 — Proxy: add request counter to console output
- **Status:** [ ] PENDING
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
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-006 — Proxy: add minimum content length check
- **Status:** [ ] PENDING
- **File to change:** `template/proxy.py`
- **Gap addressed:** GAP-005 (accidental clipboard overwrite with short content silently corrupts response)
- **What to do:** In [`_wait_clipboard()`](template/proxy.py), after detecting hash change, add:
  ```python
  if len(current) < 20:
      print(f"[{ts}] AVERTISSEMENT: Contenu trop court ({len(current)} chars): {repr(current[:50])}")
      print(f"[{ts}] Verifiez que vous avez copie la reponse Gemini complete (Ctrl+A puis Ctrl+C)")
  ```
- **Verification:** Copy a 5-char string while proxy is polling — warning should appear but response still transmitted (non-blocking by design).
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-007 — Test and document HTTP 408 behavior in Roo Code
- **Status:** [ ] PENDING
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
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-008 — Proxy: add MAX_HISTORY_CHARS truncation
- **Status:** [ ] PENDING
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
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

## P2 — Medium Priority Fixes (quality improvements)

### FIX-009 — DOC5: add task chunking guidance for proxy mode
- **Status:** [ ] PENDING
- **File to change:** `workbench/DOC5-GUIDE-Project-Development-Process.md`
- **Gap addressed:** GAP-007 (cognitive load fatigue on long tasks)
- **What to do:** Add a new subsection 9.4.1 "Stratégie de découpage des tâches en Mode Proxy" with guidance on keeping tasks under 10 LLM turns.
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-010 — SP-007: make project context agnostic
- **Status:** [ ] PENDING
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + manual Gemini deployment
- **Gap addressed:** SP-007 Issue 2 (hardcoded UADF context)
- **What to do:** Replace the hardcoded "CONTEXTE DU PROJET" section with a generic instruction to read the Memory Bank for project context.
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-011 — DOC5: add proxy mode limitations to section 9.4
- **Status:** [ ] PENDING
- **File to change:** `workbench/DOC5-GUIDE-Project-Development-Process.md`
- **Gap addressed:** GAP-003, GAP-006, GAP-007 (undocumented limitations)
- **What to do:** Add "LIMITATIONS CONNUES DU MODE PROXY GEMINI" block to section 9.4 (see Part2 section 9 for exact text).
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

### FIX-012 — SP-007: add `browser_action` and `new_task` with usage notes
- **Status:** [ ] PENDING
- **File to change:** `template/prompts/SP-007-gem-gemini-roo-agent.md` + manual Gemini deployment
- **Gap addressed:** SP-007 Issue 1 (missing tags)
- **What to do:** Add `browser_action` and `new_task` to SP-007 with a note that `new_task` is not supported in proxy mode.
- **Applied:** [ ] Date: ___________ | Commit: ___________

---

## Progress Summary

| Priority | Total | Done | Remaining |
| :--- | :---: | :---: | :---: |
| P0 — Blocking | 3 | 2 | 1 |
| P1 — High | 5 | 0 | 5 |
| P2 — Medium | 4 | 0 | 4 |
| **TOTAL** | **12** | **2** | **10** |

---

## Changelog

| Date | Session | Fix Applied | Commit |
| :--- | :--- | :--- | :--- |
| 2026-03-23 | Initial review | Tracker created | — |
| 2026-03-23 | Session 1 | FIX-001 — Console multi-ligne NOUVELLE conversation | fceb6fd |
| 2026-03-23 | Session 2 | FIX-002 — SP-007 v1.1.0 replace_in_file + list_files | PENDING |

---

## How to Start the Next Session

Copy this prompt into Roo Code (any mode) to resume work on these fixes:

```
Lis le fichier plans/FIXES-Gemini-Proxy-Robustness-Tracker.md.
Identifie le prochain fix PENDING dans l'ordre P0 → P1 → P2.
Applique ce fix selon les instructions détaillées dans le tracker.
Une fois appliqué, mets à jour le tracker (checkbox + date + commit hash) et commite les deux fichiers ensemble.
```
