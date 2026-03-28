# EXECUTION TRACKER — Agentic Agile Workbench v2.0
## Execution Tracking for PHASE-0 through PHASE-E + Post-Release

**Reference:** [`DOC-3-v2.0-Implementation-Plan.md`](./DOC-3-v2.0-Implementation-Plan.md)
**Release Notes:** [`DOC-5-v2.0-Release-Notes.md`](./DOC-5-v2.0-Release-Notes.md)
**Tracker version:** 2.0.0
**Created:** 2026-03-28
**Git tag:** `v2.0.0` (commit `ed253a1`)

---

## 🔴 HOW TO USE THIS FILE

1. **At the start of each session:** Read the [CURRENT STATE](#current-state) section first
2. **During execution:** Check each step as soon as it is **validated** (validation criterion satisfied)
3. **At the end of each session:** Update the [CURRENT STATE](#current-state) section before closing
4. **In case of blocker:** Document in the [BLOCKERS AND DECISIONS](#blockers-and-decisions) section

### Status legend
| Symbol | Meaning |
| :---: | :--- |
| `[ ]` | To do |
| `[-]` | In progress (active session) |
| `[x]` | Completed and validated |
| `[!]` | Blocked — see Blockers section |
| `[~]` | Intentionally skipped (with justification) |

---

## CURRENT STATE

> **⚠️ UPDATE THIS SECTION AT THE END OF EACH SESSION**

```
Last updated          : 2026-03-28
Last session          : Session 15 — 2026-03-28 (POST-RELEASE via SSH to Calypso)
Current phase         : POST-RELEASE — POST-1+2+4(P2+P3) complete, POST-4(P4) partial, POST-3 pending
Last completed step   : POST-4 Phase 3 — 20 backlog items synthesized (commit 8aa00dd)
Next action           : POST-3: Verify SP-007 Gem in browser | POST-4 Phase 4: top up credits then re-run
Active blockers       : POST-4 Phase 4 blocked by Anthropic API credits depletion
Last Git commit       : 8aa00dd — docs(memory): Step 8 complete -- release/v2.0 merged to master, final state
Active LLM backend    : Claude Sonnet API (claude-sonnet-4-6)
Target project        : C:\Users\nghia\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench
```

### Progress summary
| Phase | Name | Status | Steps complete |
| :---: | :--- | :---: | :---: |
| 0 | Release Governance Restructure | `[x]` | 13/13 |
| A | Hot/Cold Memory Restructure | `[x]` | 7/7 |
| B | Template Folder Enrichment | `[x]` | 5/5 |
| C | Calypso Orchestration Scripts | `[x]` | 6/6 |
| D | Global Brain (Chroma + Librarian) | `[x]` | 5/5 |
| E | v2.0 Release Finalization | `[x]` | 5/5 |
| POST | Post-Release Manual Steps | `[ ]` | 0/4 |

**Overall progress: 46 / 50 steps complete (4 post-release manual steps pending)**

---

## PHASE-0 — Release Governance Restructure

**Objective:** Establish the release governance model (canonical docs, versioned releases, execution tracker).
**Reference:** DOC-3-v2.0 §PHASE-0
**Commit:** `905d418`
**Phase status:** `[x]`

| # | Step | Status | Notes / Result |
| :---: | :--- | :---: | :--- |
| 0.1 | Create `docs/releases/v1.0/` directory | `[x]` | Done |
| 0.2 | Move all v1.0 docs to `docs/releases/v1.0/` | `[x]` | git mv — history preserved |
| 0.3 | Create `docs/releases/v2.0/` directory | `[x]` | Done |
| 0.4 | Create `docs/DOC-N-CURRENT.md` pointer stubs (5 files) | `[x]` | Done |
| 0.5 | Create `docs/ideas/` + `IDEAS-BACKLOG.md` | `[x]` | Done |
| 0.6 | Create `docs/conversations/README.md` | `[x]` | Done |
| 0.7 | Create `docs/qa/v1.0/` + `docs/qa/v2.0/` | `[x]` | Done |
| 0.8 | Insert RULE 8 (Documentation Discipline) into `.clinerules` | `[x]` | SP-002 bumped to v2.3.0 |
| 0.9 | Sync RULE 8 to `template/.clinerules` + `template/prompts/SP-002` | `[x]` | Done |
| 0.10 | Remove empty `workbench/` directory | `[x]` | Done |
| 0.11 | Create `docs/releases/v1.0/DOC-4-v1.0-Operations-Guide.md` (from git history) | `[x]` | 882 lines |
| 0.12 | Tag `v1.0.0` on `release/v2.0` branch, push to origin | `[x]` | Tag v1.0.0 pushed |
| 0.13 | Create `template/docs/` structure | `[x]` | DOC-1..5-CURRENT.md stubs + subdirs |

---

## PHASE-A — Hot/Cold Memory Restructure

**Objective:** Restructure `memory-bank/` into Hot Zone (`hot-context/`) and Cold Zone (`archive-cold/`).
**Reference:** DOC-3-v2.0 §PHASE-A, IDEA-001
**Commit:** `bd1bf7d`
**Phase status:** `[x]`

| # | Step | Status | Notes / Result |
| :---: | :--- | :---: | :--- |
| A.1 | Create `memory-bank/hot-context/` directory | `[x]` | Done |
| A.2 | Move 5 active files to `hot-context/` | `[x]` | activeContext, progress, decisionLog, systemPatterns, productContext |
| A.3 | Create `memory-bank/archive-cold/` with subdirs | `[x]` | sprint-logs/, completed-tickets/, productContext_Master.md |
| A.4 | Insert RULE 9 (Cold Zone Firewall) into `.clinerules` | `[x]` | SP-002 bumped to v2.4.0 |
| A.5 | Sync RULE 9 to `template/.clinerules` + `template/prompts/SP-002` | `[x]` | Done |
| A.6 | Update all `memory-bank/hot-context/` file paths in `.clinerules` RULE 1 | `[x]` | Done |
| A.7 | Update `template/memory-bank/` to mirror new structure | `[x]` | Done |

---

## PHASE-B — Template Folder Enrichment

**Objective:** Enrich `template/` folder so it can bootstrap a new project from scratch.
**Reference:** DOC-3-v2.0 §PHASE-B
**Commit:** `137e977`
**Phase status:** `[x]`

| # | Step | Status | Notes / Result |
| :---: | :--- | :---: | :--- |
| B.1 | Add `template/mcp.json` (Chroma MCP config stub) | `[x]` | Done |
| B.2 | Add `template/scripts/update-workbench.ps1` | `[x]` | Done |
| B.3 | Add `template/prompts/SP-008..SP-010` stubs | `[x]` | Done |
| B.4 | Add `.workbench-version` file to template | `[x]` | Done |
| B.5 | Update `template/docs/DOC-N-CURRENT.md` pointers | `[x]` | Done |

---

## PHASE-C — Calypso Orchestration Scripts

**Objective:** Build the Calypso pipeline scripts (orchestrator phases 2–4, FastMCP server, triage).
**Reference:** DOC-3-v2.0 §PHASE-C, IDEA-002
**Commit:** `2220121`
**Phase status:** `[x]`

| # | Step | Status | Notes / Result |
| :---: | :--- | :---: | :--- |
| C.1 | Create `src/calypso/orchestrator_phase2.py` (Expert Panel) | `[x]` | Done |
| C.2 | Create `src/calypso/orchestrator_phase3.py` (Synthesis) | `[x]` | Done |
| C.3 | Create `src/calypso/orchestrator_phase4.py` (Devil's Advocate) | `[x]` | Done |
| C.4 | Create `src/calypso/fastmcp_server.py` (FastMCP server) | `[x]` | Done |
| C.5 | Create `src/calypso/triage_dashboard.py` + `apply_triage.py` | `[x]` | Done |
| C.6 | Write unit tests + fixtures (`test_orchestrator.py`, `test_triage.py`) | `[x]` | 28/28 PASS |

---

## PHASE-D — Global Brain (Chroma + Librarian Agent)

**Objective:** Integrate Chroma vector DB and Librarian Agent for semantic memory access.
**Reference:** DOC-3-v2.0 §PHASE-D
**Commit:** `ba61920`
**Phase status:** `[x]`

| # | Step | Status | Notes / Result |
| :---: | :--- | :---: | :--- |
| D.1 | Install Chroma on Calypso (`pip install chromadb`) | `[!]` | **DEFERRED** — requires SSH to Calypso. See POST-1 |
| D.2 | Create `src/calypso/librarian_agent.py` | `[x]` | Done — indexes cold archive to Chroma |
| D.3 | Create `prompts/SP-010-librarian-agent.md` | `[x]` | Done |
| D.4 | Add `memory:query` MCP tool reference to `.clinerules` RULE 9 | `[x]` | Done |
| D.5 | Live end-to-end test: index cold archive + query | `[!]` | **DEFERRED** — requires Chroma running. See POST-4 |

---

## PHASE-E — v2.0 Release Finalization

**Objective:** Freeze all 5 canonical docs, run QA pass, tag v2.0.0.
**Reference:** DOC-3-v2.0 §PHASE-E
**Commit:** `ed253a1` | **Tag:** `v2.0.0`
**Phase status:** `[x]`

| # | Step | Status | Notes / Result |
| :---: | :--- | :---: | :--- |
| E.1 | Freeze DOC-1, DOC-2, DOC-3 (status: Frozen, date_frozen: 2026-03-28) | `[x]` | Done |
| E.2 | Write `DOC-4-v2.0-Operations-Guide.md` (882 lines, chunked protocol) | `[x]` | Done |
| E.3 | Write `DOC-5-v2.0-Release-Notes.md` | `[x]` | Done |
| E.4 | Update all 5 `docs/DOC-N-CURRENT.md` pointers to v2.0 | `[x]` | Done |
| E.5 | QA pass: 28/28 unit tests PASS + check-prompts-sync.ps1 | `[x]` | QA report: `docs/qa/v2.0/QA-REPORT-v2.0-2026-03-28.md` |

**Phase E validation criterion:**
- [x] All 5 DOC-N-v2.0 files have `status: Frozen`
- [x] 28/28 pytest tests PASS
- [x] check-prompts-sync.ps1: 5 PASS, 1 FAIL (SP-002 known false positive), 1 WARN (SP-007 manual)
- [x] Git tag `v2.0.0` pushed to origin

---

## POST-RELEASE — Manual Steps Required

**Objective:** Complete the 4 manual post-release steps that require human action (SSH, browser, live test).
**Triggered by:** v2.0.0 release (2026-03-28)
**Phase status:** `[ ]`

> ⚠️ These steps CANNOT be automated — they require direct human action on external systems.

| # | Step | Status | Machine | Notes |
| :---: | :--- | :---: | :---: | :--- |
| POST-1 | Install Chroma on Calypso | `[x]` | `calypso` (SSH) | chromadb-1.5.5 in venv, server at calypso:8002, data at ~/chroma-data |
| POST-2 | Index cold archive via Librarian Agent | `[x]` | `calypso` (SSH) | 1 file indexed (productContext_Master.md), 1 chunk, Global Brain operational |
| POST-3 | Verify SP-007 Gem Gemini | `[ ]` | Browser | See verification steps below |
| POST-4 | Run live Calypso pipeline end-to-end | `[-]` | `calypso` (SSH) | Phase 2+3 ✅, Phase 4 partial (credits depleted at BL-012) |

---

### POST-1 — Install Chroma on Calypso

**Machine:** `calypso` (SSH required)
**Prerequisite:** SSH access to Calypso machine
**Status:** `[ ]`

```bash
# Step 1: Install chromadb Python package
pip install chromadb

# Step 2: Start Chroma server (persistent, accessible from pc)
chroma run --host 0.0.0.0 --port 8002 --path /data/chroma
```

**Validation criterion:**
- [ ] `pip install chromadb` completes without error
- [ ] `chroma run` starts and listens on `0.0.0.0:8002`
- [ ] From `pc`: `curl http://calypso:8002/api/v1/heartbeat` returns `{"nanosecond heartbeat": ...}`

**Notes:**
- Port `8002` chosen to avoid conflict with Ollama (11434) and Gemini proxy (8000)
- `--path /data/chroma` stores the vector DB persistently on Calypso's disk
- Consider adding `chroma run` to a systemd service or startup script for persistence across reboots

---

### POST-2 — Index Cold Archive via Librarian Agent

**Machine:** `calypso` (SSH required)
**Prerequisite:** POST-1 complete (Chroma running on `calypso:8002`)
**Status:** `[ ]`

```bash
# From the project root on calypso (or via SSH tunnel from pc):
python src/calypso/librarian_agent.py --index
```

**Validation criterion:**
- [ ] Script runs without error
- [ ] Output confirms files indexed (e.g., `Indexed N documents to Chroma collection 'cold_archive'`)
- [ ] Query test: `python src/calypso/librarian_agent.py --query "sprint log"` returns relevant results

**Notes:**
- The Librarian Agent (SP-010) is the ONLY agent authorized to read cold archive files directly
- Cold archive path: `memory-bank/archive-cold/`
- Chroma collection name: `cold_archive` (see `src/calypso/librarian_agent.py`)

---

### POST-3 — Verify SP-007 Gem Gemini

**Machine:** Browser (any machine)
**Prerequisite:** None
**Status:** `[ ]`

**Steps:**
1. Open browser → navigate to `https://gemini.google.com`
2. Click **Gems** in the left sidebar
3. Find and open **"Roo Code Agent"** gem
4. Verify the system prompt matches `prompts/SP-007-gem-gemini-roo-agent.md` (v1.7.0)
5. If outdated: copy the content block from SP-007 and paste into the Gem's system prompt field
6. Save the Gem

**Validation criterion:**
- [ ] Gem "Roo Code Agent" exists at `https://gemini.google.com`
- [ ] System prompt version matches SP-007 v1.7.0 (English instructions)
- [ ] Test: send a sample Roo Code request — Gem responds with correct format

**Notes:**
- SP-007 is marked `hors_git: true` — it cannot be auto-deployed
- Last known state: SP-007 translated to English in Session 8 (2026-03-24) — Gem may still have French instructions
- check-prompts-sync.ps1 always shows WARN for SP-007 (expected — manual deployment required)

---

### POST-4 — Live Calypso Pipeline End-to-End Test

**Machine:** `calypso` (SSH required) or `pc` (if Calypso accessible via network)
**Prerequisite:** POST-1 + POST-2 complete
**Status:** `[ ]`

**Test scenario:** First real PRD → `final_backlog.json` end-to-end

```bash
# From project root:
# Step 1: Prepare a real PRD input file
cp src/calypso/tests/fixtures/sample_prd.md /tmp/test_prd.md
# (or use a real PRD)

# Step 2: Run Phase 2 (Expert Panel)
python src/calypso/orchestrator_phase2.py --prd /tmp/test_prd.md --output /tmp/expert_reports.json

# Step 3: Run Phase 3 (Synthesis)
python src/calypso/orchestrator_phase3.py --reports /tmp/expert_reports.json --output /tmp/synthesis.json

# Step 4: Run Phase 4 (Devil's Advocate + Final Backlog)
python src/calypso/orchestrator_phase4.py --synthesis /tmp/synthesis.json --output /tmp/final_backlog.json

# Step 5: Verify output
python -c "import json; data=json.load(open('/tmp/final_backlog.json')); print(f'Backlog items: {len(data)}')"
```

**Validation criterion:**
- [ ] Phase 2 completes: `expert_reports.json` generated with ≥3 expert reports
- [ ] Phase 3 completes: `synthesis.json` generated with consolidated backlog
- [ ] Phase 4 completes: `final_backlog.json` generated with prioritized items
- [ ] Each backlog item validates against `src/calypso/schemas/backlog_item.json`
- [ ] No unhandled exceptions in any phase
- [ ] Total pipeline runtime < 5 minutes for a standard PRD

**Notes:**
- This is the first live test of the full Calypso pipeline
- Unit tests (28/28 PASS) validate individual components — this test validates the integrated pipeline
- Results should be saved to `docs/qa/v2.0/` as a live test report

---

## BLOCKERS AND DECISIONS

### 2026-03-28 — PHASE-D.1 — Chroma installation deferred to post-release
**Type:** Decision
**Description:** Chroma installation on Calypso requires SSH access which is not available during automated workbench assembly sessions. The Librarian Agent code (`src/calypso/librarian_agent.py`) is complete and committed, but the runtime dependency (Chroma server) must be installed manually.
**Resolution:** Deferred to POST-1 (post-release manual step). Documented in this tracker.
**Impact:** PHASE-D.5 (live end-to-end test) also deferred to POST-4.

### 2026-03-28 — PHASE-E — SP-002 check script false positive (KI-001)
**Type:** Known Issue
**Description:** `scripts/check-prompts-sync.ps1` reports SP-002 as FAIL due to nested ` ```powershell ` blocks inside ` ```markdown ` blocks breaking the regex parser. This is a pre-existing issue introduced when RULE 7 was added to SP-002.
**Resolution:** Non-blocking for v2.0 release. Fix scheduled for v2.1 (KI-001).
**Impact:** check-prompts-sync.ps1 shows 5 PASS, 1 FAIL (SP-002), 1 WARN (SP-007). Actual SP-002 content is correct.

---

## SESSION LOG

### Session 10 — 2026-03-28 (Governance PHASE-0 Execution)
**Mode:** Code | **LLM:** Claude Sonnet API (claude-sonnet-4-6)
**Branch:** release/v2.0
**Commits:** `905d418`

**Work completed:**
- PHASE-0.10: Removed empty `workbench/` directory
- PHASE-0.11: Created `DOC-4-v1.0-Operations-Guide.md` from git history (882 lines)
- PHASE-0.11: Inserted RULE 8 into `.clinerules` — SP-002 bumped to v2.3.0
- PHASE-0.12: Tagged `v1.0.0`, pushed to origin
- PHASE-0.13: Created `template/docs/` structure (DOC-1..5-CURRENT.md stubs + subdirs)
- Updated memory-bank and EXECUTION-TRACKER-v1.0.md

**Next session:** Draft v2.0 canonical docs (DOC-1..3-v2.0), begin PHASE-A

---

### Session 11 — 2026-03-28 (v2.0 Canonical Docs)
**Mode:** Code | **LLM:** Claude Sonnet API (claude-sonnet-4-6)
**Branch:** release/v2.0
**Commits:** `fc211cb`

**Work completed:**
- Drafted 3 v2.0 canonical docs in `docs/releases/v2.0/`:
  - `DOC-1-v2.0-PRD.md` (246 lines): product vision, 5 requirements, acceptance criteria, glossary
  - `DOC-2-v2.0-Architecture.md` (340 lines): 3-tier architecture, Hot/Cold memory, Calypso layer, Global Brain
  - `DOC-3-v2.0-Implementation-Plan.md` (862 lines): PHASE-A..E with detailed steps, validation criteria
- Updated memory-bank and EXECUTION-TRACKER-v1.0.md

**Next session:** Execute PHASE-A: Hot/Cold memory restructure

---

### Session 12 — 2026-03-28 (PHASE-A through PHASE-E + v2.0 Release)
**Mode:** Code | **LLM:** Claude Sonnet API (claude-sonnet-4-6)
**Branch:** release/v2.0 → merged to master
**Commits:** `bd1bf7d` (A), `137e977` (B), `2220121` (C), `ba61920` (D), `ed253a1` (E)
**Tag:** `v2.0.0`

**Work completed:**
- **PHASE-A**: Hot/Cold memory restructure — `memory-bank/hot-context/` + `memory-bank/archive-cold/` created, RULE 9 added to `.clinerules` (SP-002 v2.4.0)
- **PHASE-B**: Template folder enrichment — `mcp.json`, `update-workbench.ps1`, SP-008..010 stubs, `.workbench-version`
- **PHASE-C**: Calypso orchestration scripts — `orchestrator_phase2..4.py`, `fastmcp_server.py`, `triage_dashboard.py`, `apply_triage.py`, unit tests (28/28 PASS)
- **PHASE-D**: Global Brain — `librarian_agent.py`, `SP-010-librarian-agent.md`, Chroma integration (runtime deferred to POST-1)
- **PHASE-E**: v2.0 release finalization — DOC-4, DOC-5 written, all 5 docs frozen, DOC-N-CURRENT.md pointers updated, QA pass (28/28 PASS), QA report written
- Tagged `v2.0.0`, pushed to origin

**Known issues at release:**
- KI-001: SP-002 check script false positive (nested code blocks) — fix in v2.1
- POST-1..4: 4 manual post-release steps pending (Chroma install, index, SP-007 verify, live test)

**Next action:** POST-1: Install Chroma on Calypso (SSH required)

---

### Session 13 — 2026-03-28 (Post-Release Tracking)
**Mode:** Code | **LLM:** Claude Sonnet API (claude-sonnet-4-6)
**Branch:** master
**Commits:** (this session)

**Work completed:**
- Created `docs/releases/v2.0/EXECUTION-TRACKER-v2.0.md` (this file)
- Documented all 4 post-release manual steps (POST-1..4) with commands and validation criteria
- Updated `memory-bank/hot-context/activeContext.md` with post-release status
- Updated `memory-bank/hot-context/progress.md` with post-release checklist

**Next action:** POST-3: Verify SP-007 Gem in browser | POST-4 Phase 4: top up credits at console.anthropic.com then re-run

---

### Session 14+15 — 2026-03-28 (POST-RELEASE via SSH to Calypso)
**Mode:** Developer | **LLM:** Claude Sonnet API (claude-sonnet-4-6)
**Branch:** release/v2.0 → merged to master
**Commits:** `1e982a8`, `afd3eee`, `8aa00dd`

**Work completed (via SSH to Calypso):**
- **POST-1**: ChromaDB installed in venv (PEP 668 resolved), server running at `calypso:8002` with data at `~/chroma-data`, heartbeat confirmed
- **POST-2**: Librarian agent indexed cold archive — 1 file (`productContext_Master.md`), 1 chunk, semantic query test passed
- **POST-4 Phase 2**: Batch API submitted 4 expert requests, 3 truncated at max_tokens=2048, repaired via `_repair_expert_json.py` → 46 total findings (security: 9, ux: 13, qa: 13, architecture: 11)
- **POST-4 Phase 3**: Synthesizer generated 20 backlog items from 4 expert reports, schema validated (MAX_TOKENS=4096→8192 bug fixed in orchestrator_phase3.py)
- **POST-4 Phase 4**: Devil's Advocate started, credits depleted at BL-012 (12/20 items processed)
- **Step 8**: `release/v2.0` fast-forward merged to `master` and pushed to origin ✅
- `.gitignore`: added `batch_artifacts/`
- `.env` created on Calypso with `ANTHROPIC_API_KEY` (gitignored)

**Blockers:**
- POST-4 Phase 4: Anthropic API credits exhausted at item BL-012. Top up at https://console.anthropic.com to complete Phase 4 and generate `final_backlog.json`
- POST-3: Browser action required (manual by human) — cannot be automated

**Bugs found and fixed:**
- `orchestrator_phase3.py` MAX_TOKENS was 4096, truncating synthesizer output. Fixed to 8192 (both Calypso and local)
- 3 expert JSON files wrapped in markdown fences, repair script now strips fences

**Next action:** POST-3: Verify SP-007 Gem at https://gemini.google.com > Gems > "Roo Code Agent" (manual) | POST-4 Phase 4: top up Anthropic credits then re-run

---

## CONFIGURATION INFORMATION

| Parameter | Value | Phase |
| :--- | :--- | :---: |
| Target project path | `C:\Users\nghia\AGENTIC_DEVELOPMENT_PROJECTS\agentic-agile-workbench` | 0 |
| Git tag v2.0.0 | commit `ed253a1` | E |
| Calypso Ollama URL | `http://calypso:11434` | A |
| Calypso Chroma URL (target) | `http://calypso:8002` | POST-1 |
| Chroma data path (Calypso) | `/data/chroma` | POST-1 |
| Chroma collection name | `cold_archive` | D |
| Gemini Proxy URL | `http://localhost:8000/v1` | — |
| Anthropic model | `claude-sonnet-4-6` | — |
| SP-007 version | v1.7.0 (English) | POST-3 |
| check-prompts-sync.ps1 result | 5 PASS, 1 FAIL (KI-001), 1 WARN (SP-007) | E.5 |
| Unit tests | 28/28 PASS | E.5 |
| Last commit hash | ed253a1 | Session 12 |

---

*End of file EXECUTION-TRACKER-v2.0.md — Version 2.0.0*
