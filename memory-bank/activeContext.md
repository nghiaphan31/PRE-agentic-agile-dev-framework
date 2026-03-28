---
# Active Context
**Last updated:** 2026-03-28
**Active mode:** Code
**Active LLM backend:** Claude Sonnet API (claude-sonnet-4-6)

## Current task
v2.0 canonical docs drafted. Ready to execute PHASE-A (Hot/Cold memory restructure).

## Last result
### v2.0 Canonical Docs Drafted (Session 2026-03-28)

Three v2.0 canonical docs created on `release/v2.0` branch (commit fc211cb):

- **[`docs/releases/v2.0/DOC-1-v2.0-PRD.md`](docs/releases/v2.0/DOC-1-v2.0-PRD.md)** (246 lines, Draft)
  - Product vision: semi-autonomous asynchronous factory
  - 5 requirements: REQ-2.1..2.5 (governance, hot/cold memory, template, calypso, global brain)
  - Detailed acceptance criteria per requirement
  - Glossary of v2.0 terms

- **[`docs/releases/v2.0/DOC-2-v2.0-Architecture.md`](docs/releases/v2.0/DOC-2-v2.0-Architecture.md)** (340 lines, Draft)
  - 3-tier architecture: Tier 1 (Roo Code), Tier 2 (Calypso), Tier 3 (Cloud APIs)
  - Hot/Cold memory architecture with Cold Zone Firewall
  - Calypso orchestration layer: 7 scripts + FastMCP server
  - Global Brain: Chroma vector DB + Librarian Agent
  - v2.0 directory structure + SP registry additions (SP-008, SP-009, SP-010)

- **[`docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md`](docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md)** (862 lines, Draft)
  - PHASE-0: COMPLETE
  - PHASE-A: Hot/Cold memory (steps A.1..A.7)
  - PHASE-B: Template enrichment (steps B.1..B.4)
  - PHASE-C: Calypso scripts (steps C.1..C.11)
  - PHASE-D: Global Brain (steps D.1..D.8)
  - PHASE-E: v2.0 release finalization

## Next step(s)
- [ ] PHASE-A: Hot/Cold memory restructure
  - A.1: Create memory-bank/hot-context/ and archive-cold/ directories
  - A.2: git mv 5 files to hot-context/
  - A.3: Add RULE 9 (Cold Zone Firewall) to .clinerules
  - A.4: Update RULE 1 to reference hot-context/ paths
  - A.5: Create scripts/memory-archive.ps1
  - A.6: Update memory bank templates in .clinerules
  - A.7: Commit and push
- [ ] PHASE-B: Template folder enrichment
- [ ] PHASE-C: Calypso orchestration scripts
- [ ] PHASE-D: Global Brain / Librarian Agent
- [ ] PHASE-E: v2.0 release finalization

## Blockers / Open questions
- SP-002 check script regex issue (nested code blocks) — low priority, non-blocking
- Chroma vector DB installation on Calypso required for PHASE-D (manual step)
- SP-008, SP-009, SP-010 system prompts to be written during PHASE-C and PHASE-D

## Last Git commit
fc211cb docs(v2.0): draft DOC-1, DOC-2, DOC-3 for v2.0 release
---
