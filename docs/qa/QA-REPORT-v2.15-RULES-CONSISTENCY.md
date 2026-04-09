# QA Report — v2.15 Rules & Scripts Consistency Review

**Date:** 2026-04-09  
**Reviewer:** Code Agent  
**Scope:** Rules (`.clinerules`, `.roomodes`, `prompts/SP-002`) and Scripts consistency with ADR-006-AMEND-001 (stabilization/vX.Y naming)  

---

## Files Reviewed

| Category | Files |
|---|---|
| Rules | `.clinerules`, `prompts/SP-002-clinerules-global.md`, `.roomodes`, `prompts/README.md` |
| GitHub Actions | `.github/workflows/release-gate.yml`, `.github/workflows/canonical-docs-check.yml` |
| Scripts | `scripts/check-prompts-sync.ps1`, `scripts/rebuild_sp002.py`, `scripts/detect-merged-features.py` |
| Hooks | `.githooks/pre-receive` |
| Governance | `memory-bank/hot-context/decisionLog.md` (ADR-006-AMEND-001) |

---

## Finding F-001: release-gate.yml Uses `develop-v*` Instead of `stabilization/v*`

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **File** | `.github/workflows/release-gate.yml` |
| **Lines** | 6, 41 |
| **Rule Reference** | ADR-006-AMEND-001: "`develop-vX.Y` → `stabilization/vX.Y`" (decisionLog.md line 117); RULE 10.1 branch table |

### Description

The `release-gate.yml` workflow triggers on `develop-v*` branches:

```yaml
on:
  push:
    branches:
      - 'develop-v*'   # ← WRONG: should be 'stabilization/v*'
```

And the version extraction logic uses `develop-v`:

```yaml
VERSION="${GITHUB_REF#refs/heads/develop-v}"  # ← WRONG: should be stabilization/v
```

### Expected Behavior (ADR-006-AMEND-001)

ADR-006-AMEND-001 explicitly states:
- "`develop-vX.Y` → `stabilization/vX.Y`" — all agents MUST use `stabilization/vX.Y` (decisionLog.md line 128)
- `release/vX.Y.Z` pattern is deprecated and must not be created (line 130)

### Consequence

If a `stabilization/v2.16` branch is created for the next release, the `release-gate.yml` workflow will **NOT trigger** on it, bypassing all P0 blocker checks.

### Suggested Fix

```yaml
on:
  push:
    branches:
      - 'stabilization/v*'
```

```yaml
VERSION="${GITHUB_REF#refs/heads/stabilization/v}"
```

---

## Finding F-002: canonical-docs-check.yml Uses `develop-v*` Instead of `stabilization/v*`

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **File** | `.github/workflows/canonical-docs-check.yml` |
| **Lines** | 10–11 |
| **Rule Reference** | ADR-006-AMEND-001; RULE 12.4 GitHub Actions enforcement |

### Description

```yaml
on:
  push:
    branches:
      - 'develop-v*'  # ← WRONG: should be 'stabilization/v*'
```

### Consequence

The canonical docs coherence check will not run on `stabilization/v*` branches, allowing documentation drift to go undetected during release preparation.

### Suggested Fix

```yaml
on:
  push:
    branches:
      - 'stabilization/v*'
```

---

## Finding F-003: Pre-receive Hook Has Wrong DOC-3/DOC-5 Line Count Minimums

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **File** | `.githooks/pre-receive` |
| **Lines** | 102–104 |
| **Rule Reference** | RULE 12.1 R-CANON-0 minimum line counts |

### Description

The pre-receive hook hardcodes wrong minimums for release-specific docs:

```bash
declare -A MIN_LINES_CUMULATIVE=(
  ["DOC-1"]=500
  ["DOC-2"]=500
  ["DOC-3"]=300   # ← WRONG: DOC-3 is release-specific, min is 100
  ["DOC-4"]=300
  ["DOC-5"]=200   # ← WRONG: DOC-5 is release-specific, min is 50
)
```

Per RULE 12.1 R-CANON-0:
- Cumulative (DOC-1: 500, DOC-2: 500, DOC-4: 300)
- Release-specific (DOC-3: 100, DOC-5: 50)

### Consequence

- DOC-3 (a 100-line release-specific doc) is incorrectly held to a 300-line threshold
- DOC-5 (a 50-line release-specific doc) is incorrectly held to a 200-line threshold
- Valid release-specific docs could be rejected; the check is stricter than the rules

### Suggested Fix

```bash
# Cumulative docs only
declare -A MIN_LINES_CUMULATIVE=(
  ["DOC-1"]=500
  ["DOC-2"]=500
  ["DOC-4"]=300
)

# Release-specific docs (separate table)
declare -A MIN_LINES_RELEASE_SPECIFIC=(
  ["DOC-3"]=100
  ["DOC-5"]=50
)
```

---

## Finding F-004: Pre-receive Hook Has No Branch Naming Enforcement

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **File** | `.githooks/pre-receive` |
| **Lines** | 56–58 (only `feature/` and `fix/` checked) |
| **Rule Reference** | RULE 10.1 branch table; ADR-006-AMEND-001 |

### Description

The pre-receive hook only checks for `feature/` and `fix/` branches:

```bash
branch=$(git branch --contains "$commit" --format='%(refname:short)' | grep -E '^feature/|^fix/' || true)
```

Per RULE 10.1, the full branch type table is:

| Type | Pattern | Enforcement |
|---|---|---|
| main | `main` | Frozen |
| develop | `develop` | Long-lived |
| Stabilization | `stabilization/vX.Y` | Permanent artifact |
| Feature | `feature/{Timebox}/{IDEA-NNN}-{slug}` | Via PR |
| Lab | `lab/{Timebox}/{slug}` | Via PR or archive |
| Bugfix | `bugfix/{Timebox}/{Ticket}-{slug}` | Via PR |
| Hotfix | `hotfix/{Ticket}` | From production tag |

### Consequence

- `lab/` and `bugfix/` branches are not recognized as valid for canonical doc modifications
- `stabilization/v*` branches are not recognized
- Someone could commit directly to `develop` or `main` and bypass the feature branch requirement

### Suggested Fix

Expand the branch pattern check to match RULE 10.1:

```bash
branch=$(git branch --contains "$commit" --format='%(refname:short)' | \
  grep -E '^feature/|^lab/|^bugfix/|^stabilization/|^develop$|^main$' || true)
```

Also add a direct commit check:

```bash
# Reject direct commits to main, develop, stabilization/*
if [[ "$branch" == "main" ]] || [[ "$branch" == "develop" ]] || [[ "$branch" == stabilization/* ]]; then
  echo "ERROR: Direct commit to $branch is not allowed" >&2
  exit 1
fi
```

---

## Finding F-005: .roomodes Missing Orchestrator Mode Reference

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `.roomodes` |
| **Lines** | 1–53 |
| **Rule Reference** | RULE 16.5 "Orchestrator as Default Entry Point" |

### Description

`.roomodes` defines only 4 Scrum roles:
1. Product Owner
2. Scrum Master
3. Developer
4. QA Engineer

RULE 16.5 states: "**Auto-Switch Instruction:** At the start of each session, invoke `switch_mode("orchestrator")` to automatically transfer control to the Orchestrator mode."

The Orchestrator is described as a "built-in" mode, but `.roomodes` contains no reference to it, creating a documentation gap.

### Suggested Fix

Add an Orchestrator entry to `.roomodes` or at minimum a comment explaining it's built-in:

```json
{
  "note": "Orchestrator mode (switch_mode 'orchestrator') is a built-in mode per RULE 16. 
           It is NOT defined in .roomodes. See SP-010 for the Librarian Agent system prompt."
}
```

---

## Finding F-006: prompts/README.md SP-002 Version Mismatch

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `prompts/README.md` |
| **Line** | 71 |
| **Rule Reference** | RULE 6.2 SP-002 version increment protocol |

### Description

`prompts/README.md` line 71 shows:

```
| **SP-002** | v2.8.0 | 2026-04-09 | ...
```

But `prompts/SP-002-clinerules-global.md` line 4 shows:

```yaml
version: 2.9.0
```

### Consequence

The registry is out of sync with the actual file. An agent reading `prompts/README.md` would see v2.8.0 but the actual deployed version is v2.9.0.

### Suggested Fix

Update `prompts/README.md` line 71:

```
| **SP-002** | v2.9.0 | 2026-04-09 | ...
```

---

## Finding F-007: check-prompts-sync.ps1 — No Explicit Branch Naming Check

| Property | Value |
|---|---|
| **Severity** | INFO |
| **File** | `scripts/check-prompts-sync.ps1` |
| **Lines** | 1–172 |
| **Rule Reference** | RULE 5 Git versioning |

### Description

`check-prompts-sync.ps1` does not verify that the canonical prompts are on the correct branch before allowing modification. Per RULE 5, prompts must be versioned under Git, but there's no branch-level enforcement in the script.

This is informational — it's a script-level check, not a governance rule enforcement issue.

---

## Summary Table

| ID | Severity | File | Issue | ADR-006 Ref |
|---|---|---|---|---|
| F-001 | **CRITICAL** | `.github/workflows/release-gate.yml` | Uses `develop-v*` instead of `stabilization/v*` | ADR-006-AMEND-001 |
| F-002 | **CRITICAL** | `.github/workflows/canonical-docs-check.yml` | Uses `develop-v*` instead of `stabilization/v*` | ADR-006-AMEND-001 |
| F-003 | **MAJOR** | `.githooks/pre-receive` | Wrong DOC-3/DOC-5 minimum line counts (300/200 vs 100/50) | RULE 12.1 |
| F-004 | **MAJOR** | `.githooks/pre-revoke` | No full branch naming enforcement (missing `stabilization/`, `lab/`, `bugfix/`) | RULE 10.1 |
| F-005 | **MINOR** | `.roomodes` | Orchestrator mode not mentioned despite RULE 16 default | RULE 16.5 |
| F-006 | **MINOR** | `prompts/README.md` | SP-002 version shows v2.8.0, actual is v2.9.0 | RULE 6.2 |
| F-007 | **INFO** | `scripts/check-prompts-sync.ps1` | No branch naming check — informational only | RULE 5 |

---

## Items Confirmed Correct

- ✅ `.clinerules` vs `prompts/SP-002-clinerules-global.md`: byte-for-byte identical (rebuild script confirms)
- ✅ `scripts/rebuild_sp002.py`: produces correct output (exit code 0)
- ✅ ADR-006-AMEND-001 `develop-vX.Y` → `stabilization/vX.Y` correctly applied in:
  - `.clinerules` RULE 10.1
  - `prompts/SP-002-clinerules-global.md` RULE 10.1
  - `memory-bank/hot-context/systemPatterns.md`
  - `template/.clinerules`
  - `template/prompts/SP-002-clinerules-global.md`
  - `docs/releases/v2.15/*` docs
- ✅ `master` → `main` rename correctly applied throughout
- ✅ `release/vX.Y.Z` concept excised from rules and docs
- ✅ RULE 12.4 GitHub Actions enforcement documented (canonical-docs-check.yml + pre-receive hook)

---

## Action Items

| Priority | Owner | Action |
|---|---|---|
| P0 | Developer | Fix `release-gate.yml`: `develop-v*` → `stabilization/v*` |
| P0 | Developer | Fix `canonical-docs-check.yml`: `develop-v*` → `stabilization/v*` |
| P1 | Developer | Fix `.githooks/pre-receive` DOC-3/DOC-5 minimum line counts (100/50) |
| P1 | Developer | Add full branch naming enforcement to `.githooks/pre-receive` |
| P2 | Developer | Update `.roomodes` to mention Orchestrator built-in mode |
| P2 | Scrum Master | Update `prompts/README.md` SP-002 version to v2.9.0 |
