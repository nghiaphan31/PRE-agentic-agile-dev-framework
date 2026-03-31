---
# Active Context

**Last updated:** 2026-03-31T21:03:00Z
**Active mode:** Code
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minmax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `develop`
- Last commit: `cd4db9e` — feat(v2.5): create v2.5 canonical docs (DOC-1..DOC-5) and update pointers
- HEAD: v2.5.0 tag on master

## Release Status
- **v2.5.0 RELEASED** ✅
- Tag: `v2.5.0` on master
- Master merged from `develop-v2.5`
- Develop fast-forwarded to master

## Current task
**ADR-012 Canonical Docs Cumulative + GitFlow Enforcement — MERGED to develop**

Completed:
1. ✅ PHASE 1B: v2.3 docs rewritten as cumulative (DOC-1, DOC-2, DOC-3, DOC-5)
2. ✅ PHASE 1C: v2.4 docs rewritten as cumulative (DOC-1, DOC-2, DOC-3, DOC-5)
3. ✅ PHASE 1D: All 5 DOC-*-CURRENT.md pointers aligned to v2.4
4. ✅ PHASE 1E: Committed on feature/ADR-012-canonical-docs-cumulative
5. ✅ PHASE 2: .githooks/pre-receive created with cumulative checks
6. ✅ PHASE 3: .github/workflows/canonical-docs-check.yml created
7. ✅ PHASE 4: Hook + CI added to template/, deploy script updated
8. ✅ PHASE 5: R-CANON rules added to .clinerules (RULE 11, RULE 12), ADR-012 created
9. ✅ SP-002 rebuilt and synchronized (6 PASS, 0 FAIL, 1 WARN)
10. ✅ Branch renamed to follow `feature/IDEA-NNN-{slug}` pattern
11. ✅ Pushed to origin with PR created (#2)
12. ✅ CI fixed (grep → sed for portability), re-run SUCCESS
13. ✅ PR #2 merged to develop

## Last Git commit
`7d56bb2` fix(ci): replace grep -oP \\K with sed for GitHub Actions portability

## Recent commits (merged from feature branch)
- `7d56bb2` fix(ci): replace grep -oP \\K with sed for GitHub Actions portability
- `45a3b08` docs(memory): update activeContext -- branch renamed, PR #2 created
- `49a9081` docs(memory): update activeContext -- canonical docs governance complete
- `0614417` chore(prompts): rebuild SP-002 after .clinerules RULE 11/12 additions
- `f118c8d` feat(governance): implement canonical docs cumulative + GitFlow enforcement

## PR Status
- **PR #2**: https://github.com/nghiaphan31/agentic-agile-workbench/pull/2 — **MERGED**

## Key files created/modified
- .githooks/pre-receive (NEW)
- .github/workflows/canonical-docs-check.yml (NEW)
- deploy-workbench-to-project.ps1 (MODIFIED)
- .clinerules / template/.clinerules (MODIFIED)
- docs/releases/v2.3/DOC-{1,2,3,5}-v2.3-*.md (MODIFIED - cumulative)
- docs/releases/v2.4/DOC-{1,2,3,5}-v2.4-*.md (MODIFIED/CREATED - cumulative)
- docs/DOC-*-CURRENT.md (MODIFIED)
- docs/ideas/ADR-012-canonical-docs-cumulative-gitflow-enforcement.md (NEW)

## Next step(s)
- [ ] Fast-forward develop to main after release freeze (per RULE 10.4)

## Next step(s)
- [ ] Return to wild development on develop
- [ ] develop-v2.5 branch can be kept for traceability (per RULE 10.3)

## ADR-013: Squash Merge Prohibition
- [x] RULE 10.3 updated: forbid squash merge and --delete-branch for traceability
- [x] Committed as `6856e66` and pushed to origin
- [ ] Consider closing orphaned VSCode tabs (_temp_chunk_*, _rebuild_*)

## Blockers / Open questions
- SP-007 Gem Gemini requires manual deployment at https://gemini.google.com > Gems

## Coherence Status (SP-002 v2.7.0)
- SP-001 (Modelfile): PASS
- SP-002 (.clinerules): PASS (v2.7.0 — RULE 6 mandates rebuild_sp002.py)
- SP-003 (.roomodes product-owner): PASS
- SP-004 (.roomodes scrum-master): PASS
- SP-005 (.roomodes developer): PASS
- SP-006 (.roomodes qa-engineer): PASS
- SP-007 (Gem Gemini): WARN (manual deployment required)

## Ideation-to-Release — Key Decisions
| Decision | Choice |
|----------|--------|
| Intake Agent | Orchestrator (any agent can route) |
| Refinement approach | Orchestrator decides based on complexity score |
| Branch merge | On-demand (continuous integration) |
| Hotfix priority | Always interrupts planned release |
| DOC-3 tracking | Tool-assisted (AI drafts, human approves) |
| SP-002 sync | Always use `python scripts/rebuild_sp002.py` |

---
