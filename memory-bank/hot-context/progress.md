# Project Progress

**Last updated:** 2026-04-02T17:30:00Z
**Session:** s2026-04-01-architect-001
**Plan:** PLAN-2026-04-01-001

## le workbench Infrastructure

### Setup Phase
- [x] Phase 0: Clean VS Code + Roo Code base (fresh reinstall)
- [x] Phase 1: Ollama + models installed (14b and 8b — deviations 32b→14b and 7b→8b)
- [x] Phase 2: Git repository initialized with complete .gitignore
- [x] Phase 3: Custom Modelfile (uadf-agent, T=0.15, ctx=131072, base 14b)
- [x] Phase 4: .roomodes (4 Agile personas with Git rules)
- [x] Phase 5: Memory Bank (7 files) + .clinerules (9 rules)
- [x] Phase 6: proxy.py v2.1.1 (Gemini Chrome server, SSE)
- [x] Phase 7: Gem Gemini Chrome configured
- [x] Phase 8: Roo Code 3-mode LLM switcher — completed
- [x] Phase 9: End-to-end tests validated
- [x] Phase 10: Anthropic Claude Sonnet API configured (operational — used for Batch API reviews)
- [x] Phase 11: prompts/ registry synchronized (SP-001..006 PASS, SP-007 WARN manual)
- [x] Phase 12: check-prompts-sync.ps1 v2 + pre-commit hook operational

## Product Features

### Epic 0: Release Governance Model
- [x] Governance model designed (universal: workbench + application projects)
- [x] PLAN-release-governance.md written (931 lines, 15 sections)
- [x] Human approval of plan
- [x] PHASE-0: Governance restructure — ALL 13 STEPS COMPLETE (commit 905d418)
- [x] Draft v2.0 canonical docs (DOC-1..3-v2.0) — commit fc211cb
- [x] PHASE-A: Hot/Cold memory restructure (IDEA-001) — commit bd1bf7d
- [x] PHASE-B: Template folder enrichment — commit 137e977
- [x] PHASE-C: Calypso orchestration scripts (IDEA-002) — commit 2220121
- [x] PHASE-D: Global Brain (Chroma/Librarian Agent) — commit ba61920
- [x] PHASE-E: v2.0 release finalization — DOC-4, DOC-5, QA pass, tag v2.0.0

### Epic 1: Agentic Agile Workbench Architecture (DOC6)
- [x] DOC6-PRD-AGENTIC-AGILE-PROCESS.md drafted (first Gemini conversation)
- [x] _Agentic Workbench Architecture Explained .md drafted (second Gemini conversation)
- [x] Batch 1 — DOC6 Expert Review submitted + retrieved → DOC6-REVIEW-RESULTS.md
- [x] Batch 2 — Second-Pass Vision Analysis submitted + retrieved → DOC6-REVIEW-RESULTS2.md
- [ ] DOC6 revision: fix P0 issues (conversational framing, PRD naming, systemPatterns.md genesis, glossary)
- [x] Migration Phase A: restructure memory-bank/ into Hot/Cold architecture (= PHASE-A above)
- [x] Migration Phase B: enrich template/ folder (= PHASE-B above)
- [x] Migration Phase C: build Calypso orchestration scripts (= PHASE-C above)
- [x] Migration Phase D: Global Brain (= PHASE-D above)
- [x] SP-008 Synthesizer Agent system prompt
- [x] SP-009 Devil's Advocate Agent system prompt
- [x] SP-010 Librarian Agent system prompt

### Epic 2: Governance Enhancement v2.5 (PLAN-2026-04-01-001)
- [x] PLAN-2026-04-01-001 created (governance plan v2.5)
- [x] Branch created: governance/PLAN-2026-04-01-001-ideation-release-v2
- [x] Phase 1: Add session-checkpoint.md to hot-context/
- [x] Phase 1: Implement APPEND ONLY for decisionLog.md
- [x] Phase 1: Update progress.md with session metadata
- [ ] Phase 1: Archive TECH-SUGGESTIONS into IDEAS-BACKLOG
- [ ] Phase 2: Implement heartbeat every 5 minutes
- [ ] Phase 2: Test crash recovery
- [ ] Phase 3: MCP integration (v3.0 scope)
- [ ] Target: Release v2.5

## v2.0 Release Status
- [x] DOC-1-v2.0-PRD.md — Frozen (2026-03-28)
- [x] DOC-2-v2.0-Architecture.md — Frozen (2026-03-28)
- [x] DOC-3-v2.0-Implementation-Plan.md — Frozen (2026-03-28)
- [x] DOC-4-v2.0-Operations-Guide.md — Frozen (2026-03-28)
- [x] DOC-5-v2.0-Release-Notes.md — Frozen (2026-03-28)
- [x] docs/DOC-N-CURRENT.md pointers → v2.0
- [x] QA report: docs/qa/v2.0/QA-REPORT-v2.0-2026-03-28.md (28/28 PASS)
- [x] Git tag v2.0.0 pushed to origin (commit ed253a1)
- [x] EXECUTION-TRACKER-v2.0.md created with post-release steps

## Post-Release Manual Steps (v2.0)
- [x] POST-1: Install Chroma on Calypso — `chromadb-1.5.5` in venv, server at `calypso:8002`, data at `/home/nghia-phan/chroma-data`
- [x] POST-2: Index cold archive — 1 file indexed, Global Brain operational
- [x] POST-3: Verify SP-007 Gem Gemini (https://gemini.google.com > Gems > "Roo Code Agent" v1.7.0) ✅
- [x] POST-4: Live Calypso pipeline — Phase 2 (4 expert reports ✅), Phase 3 (20 backlog items ✅), Phase 4 (20/20 items ✅ — 12 GREEN, 8 ORANGE)

## v2.1 Release Status

### New Branch Structure (ADR-005)
- [x] `release/v2.1` created from master (c3f4458)
- [x] `master` reset to `origin/master` (v2.0.0 tag — frozen)
- [x] `release/v2.0` closed — no new commits
- [x] ADR-005 captured in decisionLog.md
- [x] RULE 10 (GitFlow Enforcement) added to .clinerules
- [x] IDEA-008: OpenRouter MinMax M2.7 as default LLM with Claude fallback — IMPLEMENTED, merged to release/v2.1 via PR #1 (squash)
- [x] SP-002 coherence FIXED — 6 PASS | 0 FAIL (em-dash corruption, incomplete embedded template, BOM, CRLF normalization)
- [x] `release/v2.1` merged to master (8218a14, --no-ff)
- [x] Tag v2.1.0 created on master
- [x] `release/v2.2` created as active development branch

## v2.1 Release — COMPLETE
- [x] All v2.1 scope implemented and pushed (IDEA-008, SP-002 coherence, ADR-005 GitFlow)
- [x] `docs/releases/v2.1/` canonical docs created (retroactive — hotfix bypassed formal process)
- [x] DOC-N-CURRENT.md pointers updated to v2.1

## v2.2 Release — COMPLETE
- [x] All v2.2 scope implemented and pushed (memory-bank hygiene, DOC6 close, v2.1 retroactive docs)
- [x] `docs/releases/v2.2/` canonical docs created
- [x] DOC-N-CURRENT.md pointers updated to v2.2

## v2.3 Release — COMPLETE

### v2.3 Canonical Docs
- [x] DOC-1-v2.3-PRD.md — Frozen (2026-03-29)
- [x] DOC-2-v2.3-Architecture.md — Frozen (2026-03-29)
- [x] DOC-3-v2.3-Implementation-Plan.md — Frozen (2026-03-29)
- [x] DOC-4-v2.3-Operations-Guide.md — Frozen (2026-03-29)
- [x] DOC-5-v2.3-Release-Notes.md — Frozen (2026-03-29)
- [x] DOC-1..DOC-5 pointers updated to v2.3

### IDEA-009: Generic Anthropic Batch API Toolkit
- [x] IDEA-009 captured in `docs/ideas/IDEA-009-batch-api-toolkit.md`
- [x] `scripts/batch/` canonical implementation (8 modules + 2 templates)
- [x] `template/scripts/batch/` self-contained template bundle (7 modules + 2 templates)
- [x] config.py: BatchConfig dataclass + YAML loader
- [x] submit.py: batch submission with API key validation
- [x] retrieve.py: result retrieval + markdown report generation
- [x] poll.py: polling utility with --poll support
- [x] cli.py: CLI with submit/retrieve/status/poll commands
- [x] generate.py: Jinja2-based script generator
- [x] requirements.txt: added jinja2>=3.1.0, pyyaml>=6.0
- [x] ADR-010: ad-hoc governance with two paths and three release tiers
- [x] Merge feature/IDEA-009-batch-toolkit to develop (squash commit 9abbf83)
- [x] AD-HOC Minor: DOC-1..DOC-5 frozen for v2.3.0 release

### IDEA-011: SP-002 Coherence Fix
- [x] IDEA-011 captured in `docs/ideas/IDEA-011-fix-sp002-coherence.md`
- [x] Added to IDEAS-BACKLOG.md as [AD-HOC] Minor
- [x] Create `fix/IDEA-011-sp002-coherence` branch from develop
- [x] Investigate root cause: UTF-8 BOM, Latin-1 mojibake, literal \n in RULE 10
- [x] Apply fixes to .clinerules, template/.clinerules, SP-002 (no BOM, no mojibake, no literal \n)
- [x] Coherence check: 6 PASS | 0 FAIL | 1 WARN (SP-007 manual)
- [ ] Add BOM/mojibake detection to pre-commit hook (v2.3.1 scope)
- [ ] Update DOC-1..DOC-5 for v2.3.1 release (pending)

### Coherence Audit Infrastructure
- [x] Batch full audit infrastructure created (`plans/batch-full-audit/`)
- [x] submit_batch1_governance.py — 4 requests (SP vs .clinerules/.roomodes/README/template)
- [x] submit_batch2_crossdocs.py — 4 requests (DOC-1..5 intra-release + version drift + pointers)
- [x] submit_batch3_template.py — 6 requests (template sync + implementation vs docs)
- [x] retrieve_batch1/2/3.py — results retrieval scripts
- [x] PLAN-full-coherence-audit.md — architecture plan
- [x] RUNBOOK.md — execution guide
- [x] Submit all 3 batches to Anthropic Batch API
- [x] Wait 1-4 hours for processing
- [x] Retrieve and review BATCH1-GOVERNANCE-REPORT.md
- [x] Retrieve and review BATCH2-CROSSDOCS-REPORT.md
- [x] Retrieve and review BATCH3-TEMPLATE-REPORT.md
- [x] Consolidate findings into docs/qa/v2.3/COHERENCE-AUDIT-v2.3.md

### GitFlow Migration (ADR-006)
- [x] ADR-006 drafted and approved: 3-branch model (main + develop + develop-vX.Y)
- [x] `release/v2.3` renamed to `develop` (wild mainline)
- [x] RULE 10 replaced in `.clinerules` (ADR-006)
- [x] RULE 10 replaced in `template/.clinerules` (ADR-006)
- [x] RULE 10 replaced in `prompts/SP-002-clinerules-global.md` (ADR-006)
- [x] ADR-006 appended to `memory-bank/hot-context/decisionLog.md`
- [ ] Git push `develop` to origin (user must push manually — push denied during session)

## v2.3.0 Release Summary
- Tag v2.3.0 created on develop (commit b3f237c)
- IDEA-009: Batch API toolkit merged
- IDEA-011: SP-002 coherence fixed (6 PASS)
- All 5 canonical docs frozen

## v2.3.1 Next (Pending)
- BOM/mojibake detection in pre-commit hook
- SP-007 Gem Gemini manual deployment
- Push develop to origin and merge to main

### Coherence Audit Infrastructure
- [x] Batch full audit infrastructure created (`plans/batch-full-audit/`)
- [x] submit_batch1_governance.py — 4 requests (SP vs .clinerules/.roomodes/README/template)
- [x] submit_batch2_crossdocs.py — 4 requests (DOC-1..5 intra-release + version drift + pointers)
- [x] submit_batch3_template.py — 6 requests (template sync + implementation vs docs)
- [x] retrieve_batch1/2/3.py — results retrieval scripts
- [x] PLAN-full-coherence-audit.md — architecture plan
- [x] RUNBOOK.md — execution guide
- [x] Submit all 3 batches to Anthropic Batch API
- [x] Wait 1-4 hours for processing
- [x] Retrieve and review BATCH1-GOVERNANCE-REPORT.md
- [x] Retrieve and review BATCH2-CROSSDOCS-REPORT.md
- [x] Retrieve and review BATCH3-TEMPLATE-REPORT.md
- [x] Consolidate findings into docs/qa/v2.3/COHERENCE-AUDIT-v2.3.md

## GitFlow Migration (ADR-006)
- [x] ADR-006 drafted and approved: 3-branch model (main + develop + develop-vX.Y)
- [x] `release/v2.3` renamed to `develop` (wild mainline)
- [x] RULE 10 replaced in `.clinerules` (ADR-006)
- [x] RULE 10 replaced in `template/.clinerules` (ADR-006)
- [x] RULE 10 replaced in `prompts/SP-002-clinerules-global.md` (ADR-006)
- [x] ADR-006 appended to `memory-bank/hot-context/decisionLog.md`
- [ ] Git commit + push `develop` to origin
- [ ] Push `main` + tag `v2.2.0` to origin

## v2.3 Release — COMPLETE

### IDEA-012: Ideation-to-Release Process (ADR-010 Ad-Hoc)

#### IDEA-012A: Foundation (RULE 11-14 + TECH-SUGGESTIONS-BACKLOG)
- [x] TECH-SUGGESTIONS-BACKLOG created in docs/ideas/
- [x] RULE 11 (Ideation Intake) added to .clinerules
- [x] RULE 12 (Synchronization Awareness) added to .clinerules
- [x] RULE 13 (DOC-3 Execution Chapter) added to .clinerules
- [x] RULE 14 (Technical Suggestions Backlog) added to .clinerules
- [x] Template/.clinerules updated with RULE 11-14
- [x] prompts/SP-002 updated with RULE 11-14

#### IDEA-012B: Core Logic (SyncDetector + RefinementWorkflow)
- [x] SyncDetector implemented (src/calypso/sync_detector.py)
- [x] RefinementWorkflow implemented (src/calypso/refinement_workflow.py)
- [x] Integration tests passing
- [x] Status marked as IMPLEMENTED

#### IDEA-012C: Phase 5 QA + Final Fixes
- [x] QA verification (5 acceptance criteria checks) — ✅ PASS
- [x] Bug: BranchTracker.is_release_in_progress() missing — ✅ FIXED at branch_tracker.py:266
- [x] Bug: test_tracker_initialization string vs Path — ✅ FIXED at test_ideation_pipeline.py:94
- [x] Integration tests (19 total) — ✅ 19/19 PASS

## v2.4 Release — COMPLETE

### ADR-012: Canonical Docs Cumulative + GitFlow Enforcement
- [x] ADR-012 captured in `docs/ideas/ADR-012-canonical-docs-cumulative-gitflow-enforcement.md`
- [x] PHASE 1B: v2.3 docs rewritten as cumulative (DOC-1, DOC-2, DOC-3, DOC-5)
- [x] PHASE 1C: v2.4 docs rewritten as cumulative (DOC-1, DOC-2, DOC-3, DOC-5)
- [x] PHASE 1D: All 5 DOC-*-CURRENT.md pointers aligned to v2.4
- [x] PHASE 2: .githooks/pre-receive created with cumulative checks
- [x] PHASE 3: .github/workflows/canonical-docs-check.yml created
- [x] PHASE 4: Hook + CI added to template/, deploy script updated
- [x] PHASE 5: R-CANON rules added to .clinerules (RULE 11, RULE 12), ADR-012 created
- [x] SP-002 rebuilt and synchronized (6 PASS, 0 FAIL, 1 WARN)
- [x] Branch renamed to follow `feature/IDEA-NNN-{slug}` pattern
- [x] PR #2 created and CI fixed (grep → sed for portability)
- [x] PR #2 merged to develop, pushed to origin
- [x] Merge conflict resolved, activeContext updated

## v2.5 Release — COMPLETE

### Epic 2: Governance Enhancement v2.5 (PLAN-2026-04-01-001)
- [x] PLAN-2026-04-01-001 created (governance plan v2.5)
- [x] Branch created: governance/PLAN-2026-04-01-001-ideation-release-v2
- [x] Phase 1: Add session-checkpoint.md to hot-context/
- [x] Phase 1: Implement APPEND ONLY for decisionLog.md
- [x] Phase 1: Update progress.md with session metadata
- [x] Phase 2: Implement heartbeat every 5 minutes (checkpoint_heartbeat.py)
- [x] Phase 2: Test crash recovery
- [x] Phase 3: MCP integration (DEFERRED to v3.0)
- [x] v2.5.0 tag created on develop-v2.5

### ADR-013: Squash Merge Prohibition
- [x] RULE 10.3 updated: forbid squash merge and --delete-branch for traceability
- [x] Committed and pushed to origin

## v2.6 Release — COMPLETE

### Governance Enhancements (PLAN-2026-04-01-001)
- [x] Branch: develop-v2.6 created from develop
- [x] v2.6.0 canonical docs created (DOC-1 through DOC-5)
- [x] DOC-*-CURRENT.md pointers updated to v2.6
- [x] Tag v2.6.0 created on develop-v2.6
- [x] PR #5 created and merged to master
- [x] Develop fast-forwarded to master (per GitFlow RULE 10.4)

### New Rules Added (v2.6)
- [x] MB-1: Memory Bank hot/cold architecture
- [x] MB-2: Session checkpoint on session start
- [x] MB-3: APPEND ONLY for decisionLog.md
- [x] MB-4: Session heartbeat (5-minute crash recovery)
- [x] G-0: Plan-Branch Parity
- [x] D-1: ADR classification

### Artifact ID Schema (v2.6)
- [x] TYPE-YYYY-MM-DD-NNN format for IDEA, TECH, ADR, ENH
- [x] Session IDs: sYYYY-MM-DD-{mode}-{NNN}
- [x] ENH-2026-04-01-001 and ENH-2026-04-01-002 created for deferred items

### Post-Release QA (v2.6)
- [x] Coherence Audit executed (2026-04-02 via Anthropic Batch API)
- [x] 3 batches submitted: Code vs Docs, Governance, Prompt vs .roomodes
- [x] 11 requests processed; results at `docs/qa/v2.6/BATCHES/RESULTS/`
- [x] COHERENCE-AUDIT-v2.6.md consolidated report generated
- **Critical findings:** 14 P0, 17 P1, 14 P2
- **P0 Blockers:** SP-002 sync broken, DOC-1 still DRAFT, heartbeat delivery gap
- **P0 Fix:** `python scripts/rebuild_sp002.py` — then rebuild SP-002

## Legend
- [ ] To do  |  [-] In progress  |  [x] Done
