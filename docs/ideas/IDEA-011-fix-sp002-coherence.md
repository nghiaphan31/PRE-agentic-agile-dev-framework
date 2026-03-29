# IDEA-011: Fix SP-002 / .clinerules Coherence — Root Cause Resolution

**Status:** [IDEA]
**Date:** 2026-03-29
**Author:** Human (flagged during session)
**Category:** [AD-HOC] — Minor release (bug fix / quality)
**Release Tier:** Minor
**Affected Documents:** `.clinerules`, `template/.clinerules`, `prompts/SP-002-clinerules-global.md`, `SP-002` in all deployment targets

---

## 1. Problem Statement

SP-002 (.clinerules) repeatedly fails the pre-commit prompt coherence check:

```
[SP-002] .clinerules (entire file)... FAIL
```

The failures include:
- **P0**: UTF-8 BOM (`\ufeff`) at file start
- **P0**: Em-dash mojibake: `—` → `â€"â€` throughout Rules 5-7
- **P0**: Arrow mojibake: `→` → `Ã¢€š` in RULE 1 CHECK→CREATE→READ→ACT
- **P0**: Literal `\n` backslash-n sequences in RULE 10 GitFlow section (not real newlines)
- **P1**: `.clinerules` root has extra `\x9d` byte (worse corruption than template)
- **P1**: SP-002 double-embedded: `.clinerules` content appears TWICE with different LLM backend values
- **P1**: Second SP-002 embedding missing RULE 10 entirely

**Root cause:** Files saved as UTF-8 but read/copied through a Latin-1/Windows-1252 pipeline, producing double-encoding mojibake.

This is a **persistent recurring problem** — it has been fixed multiple times and keeps reappearing. A root cause fix is needed.

---

## 2. Motivation

SP-002 is the canonical source for `.clinerules` — the most critical governance file in the workbench. Every commit triggers a coherence check against it, and every commit fails.

This is unacceptable for a "simple prompt file." The problem is likely in one of:
1. The copy pipeline when copying from `prompts/SP-002` to `.clinerules` (Windows path handling?)
2. The way the pre-commit hook reads files (encoding issues)
3. The way SP-002 is stored in prompts/ (source corruption)
4. Git operations on Windows (CRLF handling)

We need to identify the actual root cause and fix it permanently.

---

## 3. Proposed Solution

### 3.1 Root Cause Investigation

Create a dedicated debug branch `fix/IDEA-011-sp002-coherence` to investigate:

1. **Check SP-002 in prompts/**: Is the source file already corrupted, or is the corruption introduced during deployment?
2. **Check the copy mechanism**: How does SP-002 get copied to `.clinerules`? (check-prompts-sync.ps1 or manual copy?)
3. **Check the pre-commit hook**: How does it read `.clinerules`? Is the BOM detected?
4. **Check git attributes**: Does `.gitattributes` properly handle line endings?
5. **Check template/.clinerules**: Is the template clean or also corrupted?

### 3.2 Fix Strategy

Once root cause identified, apply one or more of:

| # | Fix | Target |
|---|-----|--------|
| 1 | Remove BOM and re-encode as clean UTF-8 | SP-002, .clinerules, template/.clinerules |
| 2 | Fix mojibake characters (em-dashes, arrows) | All copies |
| 3 | Replace literal `\n` with real newlines in RULE 10 | All copies |
| 4 | Consolidate SP-002 to single embedding | SP-002 |
| 5 | Ensure RULE 10 is complete in both embeddings | SP-002 |
| 6 | Add BOM detection to pre-commit hook | check-prompts-sync.ps1 |
| 7 | Add `.gitattributes` with `* text=auto` | .gitattributes |
| 8 | Add encoding validation to CI | check-prompts-sync.ps1 |

### 3.3 Prevention

To prevent recurrence:
- Add BOM/mojibake detection to pre-commit hook (check-prompts-sync.ps1)
- Add file encoding validation step
- Document the encoding requirements in DOC-4

---

## 4. Affected Files

| File | Status |
|------|--------|
| `.clinerules` (root) | Corrupted — needs fix |
| `template/.clinerules` | Corrupted — needs fix |
| `prompts/SP-002-clinerules-global.md` | Corrupted — needs fix |
| `scripts/check-prompts-sync.ps1` | Needs prevention improvements |
| `.gitattributes` | May need `text=auto` |
| `check-prompts-sync.ps1` | Needs BOM detection |

---

## 5. GitFlow Path

Following ADR-010 Path 2 [AD-HOC] Minor release:

1. Branch: `fix/IDEA-011-sp002-coherence` from `develop`
2. Investigate root cause
3. Apply fixes
4. Update DOC-1 (minimal — it's a bug fix, not a feature)
5. Update DOC-2 (technical: encoding requirements)
6. Update DOC-3 (implementation steps)
7. Update DOC-4 (Operations Guide — encoding prevention)
8. Update DOC-5 (Release Notes — bug fix v2.3.1)
9. Full QA: run `check-prompts-sync.ps1` — must show ALL PASS
10. Merge to `develop`
11. Release: tag `v2.3.1` on `main`

---

## 6. Open Questions

1. Is the corruption in the SP-002 source file, or introduced during deployment?
2. Does the Windows copy pipeline introduce Latin-1 conversions?
3. Should we add `.gitattributes` with explicit UTF-8 settings?
4. Should we add a pre-commit encoding validation step?

---

## 7. Notes

- This is [AD-HOC] Minor — bug fix, no Calypso pipeline needed
- ADR-010 applies: must update all 5 canonical docs
- GitFlow enforced: feature branch → develop → main → tag
