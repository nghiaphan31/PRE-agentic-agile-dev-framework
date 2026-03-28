# Project Progress

**Last updated:** 2026-03-28

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
- [-] POST-4: Live Calypso pipeline — Phase 2 (4 expert reports ✅), Phase 3 (20 backlog items ✅), Phase 4 (API credits depleted at 12/20 items — blocked)

## v2.1 Backlog
- [ ] Fix orchestrator_phase3.py MAX_TOKENS 4096→8192 (done on Calypso, pending local commit)
- [ ] Fix SP-002 check script regex (nested code blocks false positive, KI-001)
- [ ] DOC6 revision: fix P0 issues
- [ ] Add `batch_artifacts/` to .gitignore (done)

## Legend
- [ ] To do  |  [-] In progress  |  [x] Done
