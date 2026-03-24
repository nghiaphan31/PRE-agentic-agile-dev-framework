# RESUME GUIDE — Session Resume Protocol
## Agentic Agile Workbench — Assembly Phases 0 to 12

**Execution tracker:** [`EXECUTION-TRACKER.md`](./EXECUTION-TRACKER.md)
**Implementation plan:** [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md)
**Version:** 1.0.0
**Created:** 2026-03-23

---

## 5-STEP RESUME PROTOCOL

> To be executed **at the start of each session**, without exception, regardless of how long the interruption lasted.

### STEP R1 — Read the Current State (30 seconds)

Open [`EXECUTION-TRACKER.md`](./EXECUTION-TRACKER.md) and read **only** the `CURRENT STATE` section:

```
Last updated          : [DATE]
Current phase         : [Phase X — Name]
Last completed step   : [X.Y — Description]
Next action           : [Exact step to resume from]
Active blockers       : [None | Description]
Last Git commit       : [hash — message]
Active LLM backend    : [Ollama | Proxy Gemini | Claude API]
Target project        : [Path]
```

**→ The "Next action" indicates exactly where to resume.**

---

### STEP R2 — Verify the Actual System State (2 minutes)

Run the checks corresponding to the current phase:

#### If Phase 0-1 (Infrastructure):
```powershell
# Check Tailscale
tailscale status

# Check SSH to calypso
ssh calypso "ollama list"
```

#### If Phase 2-5 (Git Project + Memory Bank):
```powershell
# Check the Git repository
cd [PROJECT_PATH]
git log --oneline -5
git status

# Check the Memory Bank
Test-Path "memory-bank/activeContext.md"
Get-Content "memory-bank/activeContext.md"
```

#### If Phase 6-8 (Proxy + Roo Code):
```powershell
# Check that the proxy can start
cd [PROJECT_PATH]
.\venv\Scripts\Activate.ps1
python -c "import fastapi, uvicorn, pyperclip; print('OK')"

# Check Ollama from pc
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

#### If Phase 9-12 (Tests + Prompts):
```powershell
# Check Git state
cd [PROJECT_PATH]
git log --oneline -10

# Check key files
Test-Path ".clinerules"
Test-Path ".roomodes"
Test-Path "proxy.py"
Test-Path "prompts/README.md"
```

---

### STEP R3 — Reconcile if Necessary (if discrepancy detected)

If the actual system state **differs** from what the tracker indicates:

1. **The tracker is ahead of reality** (e.g.: step marked `[x]` but file is missing):
   - Reset the step to `[ ]` in the tracker
   - Resume from that step

2. **Reality is ahead of the tracker** (e.g.: file exists but step not checked):
   - Verify the step's validation criterion
   - If validated → check `[x]` in the tracker
   - Continue to the next unchecked step

3. **Unresolved blocker from the previous session**:
   - Read the `BLOCKERS AND DECISIONS` section of the tracker
   - Apply the documented resolution, or find a new solution
   - Update the blocker status

---

### STEP R4 — Resume Implementation

1. Navigate in [`EXECUTION-TRACKER.md`](./EXECUTION-TRACKER.md) to the current phase
2. Find the first step with status `[ ]` or `[-]`
3. Open [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md) at the corresponding section for detailed instructions
4. Execute the step
5. Verify the validation criterion
6. Check `[x]` in the tracker once validated

---

### STEP R5 — Update the Tracker at End of Session

Before closing, **mandatory** updates:

1. **`CURRENT STATE` section** — update all fields
2. **`Progress summary` table** — update step counters
3. **`SESSION LOG` section** — add an entry for the session
4. **`BLOCKERS AND DECISIONS` section** — document any new blocker

---

## QUICK REFERENCE — DEPENDENCIES BETWEEN PHASES

```
Phase 0 (Clean VS Code)
    └─→ Phase 4 (Roo Code must be installed to load .roomodes)
    └─→ Phase 8 (Roo Code must be configured)

Phase 1 (Ollama on calypso)
    └─→ Phase 3 (ollama create uadf-agent requires Ollama installed)
    └─→ Phase 8 Mode 1 (Roo Code → Ollama requires Ollama active)

Phase 2 (Git Repository)
    └─→ ALL subsequent phases (everything is versioned in this repository)

Phase 3 (Modelfile)
    └─→ Phase 8 Mode 1 (uadf-agent must exist)
    └─→ Phase 11 SP-001 (Modelfile ↔ SP-001 consistency)

Phase 4 (.roomodes)
    └─→ Phase 9 RBAC Tests
    └─→ Phase 11 SP-003 to SP-006

Phase 5 (Memory Bank + .clinerules)
    └─→ Phase 9 (Memory Bank tests)
    └─→ Phase 11 SP-002

Phase 6 (proxy.py)
    └─→ Phase 7 (Gem Gemini uses the proxy)
    └─→ Phase 8 Mode 2
    └─→ Phase 11 SP-007

Phase 7 (Gem Gemini)
    └─→ Phase 8 Mode 2 (full test)
    └─→ Phase 9 E2E Test Mode 2

Phase 8 (3-mode switcher)
    └─→ Phase 9 (tests for all 3 modes)

Phase 9 (E2E Tests)
    └─→ Phase 10 (Mode 3 Claude tested here)

Phase 10 (Anthropic API)
    └─→ Phase 9 E2E Test Mode 3 (if not done)

Phase 11 (Prompts registry)
    └─→ Phase 12 (check-prompts-sync.ps1 verifies the SPs)

Phase 12 (pre-commit hook)
    └─→ End — complete system
```

---

## QUICK REFERENCE — SOURCE FILES TO USE

> For each phase, use the files from the `agentic-agile-workbench` repository as the canonical source.
> **Do not manually copy from DOC3** — the `template/` files are the up-to-date reference version.

| Phase | File to create in the project | Canonical source in the workbench |
| :---: | :--- | :--- |
| 3 | `Modelfile` | [`template/Modelfile`](../template/Modelfile) |
| 4 | `.roomodes` | [`template/.roomodes`](../template/.roomodes) |
| 5 | `.clinerules` | [`template/.clinerules`](../template/.clinerules) |
| 6 | `proxy.py` | [`template/proxy.py`](../template/proxy.py) ← **v2.1.0** |
| 6 | `requirements.txt` | [`template/requirements.txt`](../template/requirements.txt) |
| 6 | `scripts/start-proxy.ps1` | [`template/scripts/start-proxy.ps1`](../template/scripts/start-proxy.ps1) |
| 7 | Gem Gemini Instructions | [`template/prompts/SP-007-gem-gemini-roo-agent.md`](../template/prompts/SP-007-gem-gemini-roo-agent.md) |
| 11 | `prompts/` (entire folder) | [`template/prompts/`](../template/prompts/) |
| 12 | `scripts/check-prompts-sync.ps1` | [`template/scripts/check-prompts-sync.ps1`](../template/scripts/check-prompts-sync.ps1) |

> **⚠️ Difference between DOC3 and template/:** DOC3 contains the `proxy.py` v2.0 code (original reference version).
> The `template/proxy.py` file is at version **v2.1.0** with 10 robustness fixes.
> Always use `template/proxy.py` for deployment.

---

## QUICK REFERENCE — VERIFICATION COMMANDS BY PHASE

### Phase 0
```powershell
git --version
python --version
pip --version
```

### Phase 1
```bash
# On calypso (SSH)
ollama --version
ollama list
sudo systemctl show ollama | grep Environment
```
```powershell
# On pc
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

### Phase 2
```powershell
git log --oneline
git status
Get-ChildItem -Name
```

### Phase 3
```bash
# On calypso
ollama show uadf-agent --modelfile | grep -E "num_ctx|temperature"
```

### Phase 4
```powershell
# Verify that .roomodes is valid JSON
Get-Content ".roomodes" | ConvertFrom-Json | Select-Object -ExpandProperty customModes | Select-Object slug, name
```

### Phase 5
```powershell
Get-ChildItem "memory-bank/" -Name
Get-Content "memory-bank/activeContext.md"
Get-Content "memory-bank/progress.md"
```

### Phase 6
```powershell
.\venv\Scripts\Activate.ps1
python proxy.py &
Start-Sleep 2
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
Invoke-RestMethod -Uri "http://localhost:8000/v1/models" -Method Get
```

### Phase 7
```
# Manual verification in Chrome:
# 1. Open https://gemini.google.com > Gems > "Roo Code Agent"
# 2. Send: "Read the file memory-bank/activeContext.md"
# 3. Verify that the response contains ONLY <read_file>...</read_file>
```

### Phase 8
```powershell
# Mode 1 — Verify Ollama accessible
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET

# Mode 2 — Verify proxy active
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

### Phase 9
```powershell
Test-Path "src/hello.py"
git log --oneline -5
Get-Content "memory-bank/activeContext.md"
Get-ChildItem "docs/qa/" -Name
```

### Phase 10
```powershell
# Verify absence of API key in files
Select-String -Path "*.py", "*.md", "*.json", "*.txt", "*.env" -Pattern "sk-ant-api" -Recurse
# Must return NO results
```

### Phase 11
```powershell
Get-ChildItem "prompts/" -Name
# Must display 8 files: README.md + SP-001 to SP-007
```

### Phase 12
```powershell
powershell.exe -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"
# Must display: 6 PASS | 0 FAIL | 1 WARN
```

---

## COMMON RESUME SCENARIOS

### Scenario A — Resume after short interruption (< 1 day)

1. Read `CURRENT STATE` in the tracker
2. Run the checks for the current phase (section above)
3. Resume at the "Next action"

### Scenario B — Resume after long interruption (> 1 week)

1. Read `CURRENT STATE` in the tracker
2. Read the `SESSION LOG` (last entry)
3. Run **all** checks for completed phases to confirm state
4. Verify that Tailscale is active and `calypso` is accessible
5. Verify that the Git repository is clean (`git status`)
6. Resume at the "Next action"

### Scenario C — Resume on a new machine

1. Clone the `agentic-agile-workbench` repository
2. Read `CURRENT STATE` in the tracker
3. Identify the target project (section `CONFIGURATION INFORMATION`)
4. Clone or access the target project repository
5. Recreate the pre-commit hook if Phase 12 is complete (step 12.2)
6. Recreate the Python environment (`python -m venv venv && pip install -r requirements.txt`)
7. Resume at the "Next action"

### Scenario D — Blocked on a step

1. Document the blocker in the `BLOCKERS AND DECISIONS` section of the tracker
2. Mark the step with `[!]` in the tracker
3. Update `CURRENT STATE` with the blocker
4. Consult [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md) for the phase's troubleshooting notes
5. If the blocker is on `calypso`: check `sudo systemctl status ollama` and the logs
6. If the blocker is on the proxy: check the Python logs and `pip list`
7. Once resolved: update the blocker status, reset the step to `[ ]`, resume

### Scenario E — Regression (a validated step no longer works)

1. Identify the affected phase
2. Reset the affected steps to `[ ]` in the tracker
3. Document in `BLOCKERS AND DECISIONS`
4. Run the phase checks (section above)
5. Resume from the first failing step

---

## CRITICAL ATTENTION POINTS

> These points are the most frequent causes of failure or confusion during a resume.

### 1. Tailscale must be active BEFORE any operation on `calypso`
```powershell
tailscale status
# calypso must appear as an active peer
```
If Tailscale is inactive, all Ollama operations (Phases 1, 3, 8 Mode 1) will fail.

### 2. The Python virtual environment must be activated BEFORE launching proxy.py
```powershell
.\venv\Scripts\Activate.ps1
# The prompt must display (venv)
python proxy.py
```
Without activation, `import fastapi` will fail.

### 3. The pre-commit hook is NOT versioned in Git
After a `git clone` of the target project, recreate the hook manually (step 12.2 of DOC3).
The hook is in `.git/hooks/pre-commit` — this folder is excluded from Git.

### 4. The Anthropic API key must NEVER be in a file
It is stored only in VS Code SecretStorage.
Verification: `Select-String -Pattern "sk-ant-api" -Recurse` → must return empty.

### 5. Use template/proxy.py (v2.1.0), not the code from DOC3 (v2.0)
DOC3 contains the original reference version v2.0 for documentation purposes.
The deployable file is [`template/proxy.py`](../template/proxy.py) (v2.1.0 with 10 fixes).

### 6. The Gem Gemini must be recreated manually if the Google account changes
SP-007 is the only prompt that cannot be versioned in Git.
Source: [`template/prompts/SP-007-gem-gemini-roo-agent.md`](../template/prompts/SP-007-gem-gemini-roo-agent.md).

### 7. After each significant step: Git commit
The tracker records commit hashes for each phase.
If a hash is missing, run `git log --oneline -5` to find it.

---

## TRACKING FILES STRUCTURE

```
workbench/
├── EXECUTION-TRACKER.md   ← THIS FILE IS THE SOURCE OF TRUTH FOR STATE
│                             Update at the end of each session
├── RESUME-GUIDE.md        ← THIS FILE (resume protocol)
│                             Do not modify except to correct errors
└── DOC3-BUILD-Workbench-Assembly-Phases.md
                           ← Detailed instructions for each step
                             Read-only reference during implementation
```

---

## TRACKER UPDATE — COPY-PASTE TEMPLATES

### Updating the CURRENT STATE section

```markdown
## CURRENT STATE

> **⚠️ UPDATE THIS SECTION AT THE END OF EACH SESSION**

```
Last updated          : YYYY-MM-DD
Last session          : Session N — YYYY-MM-DD
Current phase         : Phase X — [Phase name]
Last completed step   : X.Y — [Short description]
Next action           : Phase X, Step X.Z — [Description]
Active blockers       : [None | Description of the blocker]
Last Git commit       : [abc1234] — [commit message]
Active LLM backend    : [Ollama uadf-agent | Proxy Gemini | Claude API | Not configured]
Target project        : C:\Users\[user]\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\[project-name]
```
```

### Adding an entry to SESSION LOG

```markdown
### Session N — YYYY-MM-DD — [~Xh]
**Phases worked:** Phase X to Phase Y
**Steps completed:** X.1, X.2, X.3, Y.1, Y.2
**Last commit:** abc1234 — feat(scope): description
**State at end of session:** [Precise description of the system state]
**Next action:** Phase Y, Step Y.3 — [Description]
**Blockers:** [None | Description and status]
```

### Adding a blocker to BLOCKERS AND DECISIONS

```markdown
### YYYY-MM-DD — Phase X.Y — [Short blocker title]
**Type:** Blocker
**Description:** [What happened exactly]
**Resolution:** [How resolved, or "Pending — [next attempt]"]
**Impact:** [Phases X, Y affected]
```

---

*End of file RESUME-GUIDE.md — Version 1.0.0*
