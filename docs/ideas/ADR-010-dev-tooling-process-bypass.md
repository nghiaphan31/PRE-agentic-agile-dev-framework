# ADR-010: Ad-Hoc Idea Governance — From Discovery to Release

**Date:** 2026-03-29
**Status:** Accepted
**Deciders:** Human, Architect mode

---

## Context

During the v2.3 coherence audit (2026-03-28/29), we discovered and fixed several issues with the Anthropic Batch API submission and retrieval pipeline — through trial and error. These lessons crystallized into a reusable toolkit (IDEA-009).

This raised a governance question: **when an idea emerges ad-hoc during operational work (not from a planned PRD), what is the path to production?**

The standard process (DOC-1 → DOC-2 → DOC-3 → Calypso pipeline → QA → release) is designed for structured, PRD-driven development. It was not designed for:
- Ideas discovered mid-session during operational work
- Infrastructure improvements extracted from lessons learned
- Product/business improvements that emerge from conversation
- New feature ideas that don't require expert batch review

---

## Decision

### Core Principle: All Ideas, Regardless of Origin, Follow a Release Path

Every IDEA — whether discovered ad-hoc or formally planned — **must** follow the GitFlow release model and update **all 5 canonical docs** (DOC-1 through DOC-5). The difference is the **process intensity** and **which path** it takes.

### DOC-1 and DOC-2 Coherency — Non-Negotiable

**At all times, DOC-1 (PRD) and DOC-2 (Architecture) must be fully coherent, self-contained, and complete.** There must never be any blind spot from a requirements perspective (DOC-1) or an architecture perspective (DOC-2).

For every idea (structured or ad-hoc):
- **DOC-1** must capture all applicable requirements — nothing undocumented
- **DOC-2** must describe the complete architecture — no implicit assumptions
- When DOC-1 changes, DOC-2 must be reviewed for coherency
- When DOC-2 changes, DOC-1 must be verified for completeness
- No feature, fix, or improvement may be "in production" without DOC-1 and DOC-2 being aligned and up-to-date

### Two Governance Paths

#### Path 1: Structured (Full Process) — `[STRUCTURED]`
For IDEAS that originate from a formal PRD or product discovery.

**Process:**
1. Formal triage → accepted in release scope
2. DOC-1: Atomic business requirements written
3. DOC-2: Technical architecture documented
4. DOC-3: Implementation plan with phases/steps
5. `develop-vX.Y` branch created
6. Calypso pipeline: expert batch reviews → synthesizer → devil's advocate → librarian
7. TDD development
8. Full QA pass against DOC-1 acceptance criteria
9. DOC-4 (Operations Guide) updated
10. DOC-5 (Release Notes) written
11. All 5 docs aligned and frozen
12. GitFlow release: merge `develop-vX.Y` → `main`, tag, delete `develop-vX.Y`

---

#### Path 2: Ad-Hoc (Lightweight Process) — `[AD-HOC]`
For IDEAS that emerge reactively during operational work.

**Origin examples:**
- An infrastructure improvement discovered during an audit session
- A product improvement suggested during a conversation
- A business process change identified during daily work
- A new feature idea that doesn't require expert batch analysis

**Process:**
1. **Capture** — IDEA written with full description, motivation, affected docs
2. **Triage** — Architect analyzes the idea and recommends a **release tier**:
   - **Minor release (patch/minor):** Bug fixes, small improvements, developer tooling, low-risk changes. Can skip Calypso pipeline.
   - **Medium release (feature):** New features, product improvements, architectural changes. May use Calypso pipeline partially.
   - **Major release:** Significant architectural changes, new epic-level features. Must follow full process.
3. **ADR** — Write an ADR documenting the process decision and release tier
4. **Branch** — Create `feature/IDEA-NNN-slug` from `develop`
5. **DOC-1 through DOC-5** — All 5 canonical docs updated and aligned:
   - DOC-1: Minimal PRD (can be lightweight for minor releases)
   - DOC-2: Technical impact assessment
   - DOC-3: Implementation plan (scaled to release tier)
   - DOC-4: Operations Guide updated
   - DOC-5: Release Notes written
6. **Implement** — Build on feature branch
7. **Test** — **Thorough and complete test phase** (not optional for ad-hoc):
   - For minor: unit tests + integration tests
   - For medium: unit tests + integration tests + QA review
   - For major: full QA pass + stakeholder sign-off
8. **Librarian** — Trigger Librarian Agent to index lessons learned into cold archive
9. **Merge** — Fast-forward or squash merge to `develop`
10. **Release** — Merge `develop` → `main`, tag `vX.Y.Z`, update DOC-N-CURRENT.md pointers

### Release Tier Guidelines

| Tier | Trigger | Examples | Process |
|------|---------|---------|---------|
| **Minor** | Small, low-risk, localized | Bug fixes, dev-tooling improvements, doc updates, template improvements | Skip Calypso pipeline; lightweight DOC-1/2/3; unit + integration tests |
| **Medium** | New feature or moderate scope | New Calypso phase, new agent type, product workflow change | Partial/full Calypso; full DOC-1/2/3; QA review |
| **Major** | Architectural, epic-level | New epic, fundamental architecture change, new subsystem | Full process; stakeholder sign-off |

### GitFlow Non-Negotiable

Regardless of tier, **GitFlow is always enforced**:
- All 5 canonical docs (DOC-1 through DOC-5) must be updated and aligned
- `develop` is the integration branch — never directly on `main`
- Release tags mark production state on `main`
- `develop-vX.Y` (scoped) or `develop` (wild) — chosen based on scope formality

---

## Consequences

### Positive
- Fast path for low-risk improvements without bureaucratic overhead
- Clear decision framework: ad-hoc ideas get a proper release tier
- GitFlow and canonical docs always maintained
- No idea falls through the cracks

### Negative
- Some overhead even for minor improvements (DOC-4/5 updates)
- Risk of over-categorizing: "it's minor" becoming an excuse to skip tests
- Architect must make judgment calls on release tier

### Mitigation
- **Mandatory ADR** for every ad-hoc idea — documents tier decision and rationale
- **Thorough tests** required regardless of tier — no skipping the test phase
- **All 5 docs** must be updated — no partial documentation
- Annual review of tier assignment consistency

---

## Notes

This ADR should be read alongside:
- **RULE 8** (Documentation Discipline) — which allows lightweight governance-only commits but does NOT allow skipping release documentation
- **RULE 10** (GitFlow Enforcement) — which is non-negotiable regardless of process path
- **ADR-006** (GitFlow branching model) — which defines main/develop/develop-vX.Y
- **IDEA-009** (Generic Anthropic Batch API Toolkit) — the specific case that triggered this ADR
- **DOC-4-v2.0-Operations-Guide.md** — where ad-hoc process should be documented
- **DOC-5-v2.0-Release-Notes.md** — where every release (including minor) must be documented

---

## Metadata

| Field | Value |
|-------|-------|
| category | Process Governance |
| applies_to | All IDEA processing, all release tiers |
| review_trigger | Any IDEA marked [AD-HOC] |
| created_from | IDEA-009 batch toolkit implementation |
