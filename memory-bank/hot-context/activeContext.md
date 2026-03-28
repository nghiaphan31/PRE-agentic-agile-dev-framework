---
# Active Context
**Last updated:** 2026-03-28
**Active mode:** Code
**Active LLM backend:** Claude Sonnet API (claude-sonnet-4-6)

## Current task
POST-RELEASE: Documenting and tracking the 4 manual post-release steps for v2.0.0. Created `docs/releases/v2.0/EXECUTION-TRACKER-v2.0.md` with full step-by-step instructions for POST-1..4.

## Last result
### Session 13: Post-Release Tracking (2026-03-28)

- Created `docs/releases/v2.0/EXECUTION-TRACKER-v2.0.md` (full v2.0 tracker with all phases + post-release steps)
- Documented 4 post-release manual steps with commands, validation criteria, and notes:
  - **POST-1**: Install Chroma on Calypso — `pip install chromadb && chroma run --host 0.0.0.0 --port 8002 --path /data/chroma`
  - **POST-2**: Index cold archive — `python src/calypso/librarian_agent.py --index`
  - **POST-3**: Verify SP-007 Gem Gemini at `https://gemini.google.com` > Gems > "Roo Code Agent"
  - **POST-4**: Live Calypso pipeline end-to-end test (PRD → `final_backlog.json`)

### Previous: PHASE-E: v2.0 Release Finalization (Session 2026-03-28)
- E.1: DOC-1, DOC-2, DOC-3 frozen (status: Frozen, date_frozen: 2026-03-28)
- E.2: `docs/releases/v2.0/DOC-4-v2.0-Operations-Guide.md` written (882 lines, chunked protocol)
- E.3: `docs/releases/v2.0/DOC-5-v2.0-Release-Notes.md` written
- E.4: All 5 `docs/DOC-N-CURRENT.md` pointers updated to v2.0
- E.5: QA pass — 28/28 PASS, QA report: `docs/qa/v2.0/QA-REPORT-v2.0-2026-03-28.md`
- Git tag `v2.0.0` pushed to origin (commit `ed253a1`)

## Next step(s)
- [ ] **POST-1** (manual — SSH to Calypso): `pip install chromadb && chroma run --host 0.0.0.0 --port 8002 --path /data/chroma`
- [ ] **POST-2** (manual — after POST-1): `python src/calypso/librarian_agent.py --index`
- [ ] **POST-3** (manual — browser): Verify SP-007 Gem Gemini at https://gemini.google.com > Gems > "Roo Code Agent" (v1.7.0 English)
- [ ] **POST-4** (manual — after POST-1+2): Live Calypso pipeline PRD → `final_backlog.json` end-to-end test
- [ ] **v2.1 planning**: Fix SP-002 check script regex (KI-001)

## Blockers / Open questions
- POST-1..4 require SSH access to Calypso and/or browser action — cannot be automated
- KI-001: SP-002 check script false positive (nested code blocks) — low priority, fix in v2.1

## Last Git commit
97b765e docs(release): add EXECUTION-TRACKER-v2.0 with post-release manual steps POST-1..4
(previous: ed253a1 — Tag: v2.0.0)
---
