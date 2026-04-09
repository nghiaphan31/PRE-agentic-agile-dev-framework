# TECH-007 — Mechanical `--no-ff` Merge Enforcement

**Captured:** 2026-04-09
**Refined:** 2026-04-09
**Status:** [REFINED]
**Selected Option:** Option A — GitHub Actions Workflow
**Complexity:** 3/10

---

## Problem Statement

RULE 10.3 mandates `--no-ff` merge strategy for all feature branch merges, requiring a merge commit to always be created even when fast-forward would be possible. This requirement is documented but has **zero mechanical enforcement**:

| Gap | Current State |
|-----|---------------|
| GitHub Actions workflow | None |
| Pre-receive hook | None |
| Branch protection rules | Unknown / unchecked |
| Validation at merge time | No |

The `--no-ff` enforcement ensures traceability by preserving the branch topology history in the git graph.

---

## Selected Solution: Option A — GitHub Actions Workflow

A workflow that runs on pull request merges to verify that the merge commit has exactly 2 parents (indicating a true merge commit, not a fast-forward).

**Implementation:**
- `.github/workflows/require-merge-commit.yml`
- Trigger on `pull_request` with `types: [closed]`
- When merged AND target branch matches protection rules, check `git log --merges` for 2-parent commit
- Fail workflow with clear error if fast-forward was used

**Rationale:** Simple to deploy, no server-side changes needed, works on GitHub.com, visible in PR checks.

---

## Affected Files

| File | Action |
|------|--------|
| `.github/workflows/require-merge-commit.yml` | Create |
| `docs/ideas/TECH-007-no-ff-enforcement.md` | Update |

---

## Related Documents

- RULE 10.3 — Feature Branch Workflow (`.clinerules`)
- ADR-006 — GitFlow Branch Lifecycle
- ADR-019 — `--no-ff` acceptance record
- ADR-020 — `--no-ff` acceptance record
- `.github/workflows/canonical-docs-check.yml` — Reference for existing workflow pattern

---

## Technical Notes

A true merge commit always has exactly 2 parents (the branch tip and the merge base). A fast-forward has 1 parent.

```bash
# Check if a commit is a merge commit
git cat-file -p <commit> | wc -l
# Merge commit has "parent" line twice

# Verify merge has 2 parents
git log --merges -1 --format="%P" <merge-commit>
```

---

## Next Steps

- [x] Evaluate Option A/B/C with development team — **Option A selected**
- [x] Assess GitHub Enterprise vs GitHub.com for pre-receive hook support — **GitHub Actions works on GitHub.com**
- [ ] Implement `.github/workflows/require-merge-commit.yml` (requires Developer mode)
- [ ] Test workflow against sample PRs

---

## Implementation Specification

### `.github/workflows/require-merge-commit.yml`

```yaml
name: Require Merge Commit

on:
  pull_request:
    types: [closed]

jobs:
  check-merge-commit:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Get target branch
        run: |
          echo "TARGET_BRANCH=${{ github.event.pull_request.base.ref }}" >> $GITHUB_ENV
          
      - name: Check for merge commit
        run: |
          # Get the merge commit SHA
          MERGE_SHA=${{ github.event.pull_request.merge_commit_sha }}
          
          if [[ -z "$MERGE_SHA" ]]; then
            echo "::error::No merge commit SHA found. PR may have been fast-forwarded."
            echo "::error::RULE 10.3 requires --no-ff merge strategy."
            exit 1
          fi
          
          # Verify it has exactly 2 parents
          PARENT_COUNT=$(git cat-file -p "$MERGE_SHA" | grep -c "^parent")
          
          if [[ "$PARENT_COUNT" -ne 2 ]]; then
            echo "::error::Merge commit $MERGE_SHA has $PARENT_COUNT parents (expected 2)."
            echo "::error::This indicates a fast-forward merge, which violates RULE 10.3."
            echo "::error::Please re-merge using --no-ff flag."
            exit 1
          fi
          
          echo "✓ Merge commit verified: $MERGE_SHA (2 parents)"
```

---

*Technical suggestion — refined and ready for implementation*
