# IDEA-031: Fix Major Gaps — Scripts Reliability (P1)

**Status:** [REFINED]
**Created:** 2026-04-09
**Source:** v2.15 consistency review (QA-REPORT-v2.15-CONSISTENCY-SYNTHESIS.md)
**Refined:** 2026-04-09
**Priority:** P1
**Effort:** L
**Target Release:** v2.17

---

## Problem Statement

Multiple automation scripts have reliability issues that cause silent failures, incorrect behavior, or missing functionality:

1. **`checkpoint_heartbeat.py`** — `log_conversation()` writes placeholder template, not actual conversation content
2. **`audit_cumulative_docs.py`** — Hardcoded releases list excludes v2.12-v2.16
3. **`.githooks/pre-receive`** — Cumulative thresholds incorrect for DOC-3 (300→100) and DOC-5 (200→50)

---

## Background

IDEA-031 was created from v2.15 QA synthesis findings. The original IDEA-031 had generic problem statements. This refinement provides specific, actionable details for each gap.

### Release Context

- **Current Released Version:** v2.16.0
- **Current Draft Version:** v2.17 (stabilization/v2.17)
- **Target:** Fix identified gaps before v2.17 release

---

## Gap 1: checkpoint_heartbeat.py — log_conversation() Writes Placeholder Content

### Problem

The `log_conversation()` function (lines 320-429) writes a placeholder template to `docs/conversations/` instead of actual conversation content:

```python
# Lines 347-372: Writes placeholder template
conversation_content = f"""---
conversation_id: {conversation_id}
mode: {source}
...
## Source Reference

This conversation was captured via `checkpoint_heartbeat.py --log-conversation`.

## Notes

<!-- Add conversation summary, key decisions, and outcomes below -->
"""
```

The function extracts metadata (session_id, mode, date) but does NOT capture the actual conversation messages/responses.

### Impact

- RULE 8.3 Conversation Log Mandate requires all conversations be saved
- Currently saves only metadata, not conversation content
- Human cannot review what was actually said
- Conversation mining for ideas is impossible without content

### Proposed Solution

Modify `log_conversation()` to capture actual conversation content:

1. **Option A (Preferred):** Accept conversation content as CLI argument or environment variable
   ```bash
   python checkpoint_heartbeat.py --log-conversation --content "conversation text here"
   ```

2. **Option B:** Read from a temp file written by the agent before calling `--log-conversation`
   ```python
   TEMP_CONVERSATION = Path("memory-bank/hot-context/.temp_conversation.txt")
   ```

3. **Option C:** Add a `--capture` flag that prompts for or reads conversation input

The function should write the actual conversation text, not a placeholder template with `<!-- Add notes -->`.

### Affected Files

- `scripts/checkpoint_heartbeat.py` (lines 320-429)

---

## Gap 2: audit_cumulative_docs.py — Hardcoded Releases List

### Problem

The script has a hardcoded `RELEASES` list that only checks v2.10 and v2.11:

```python
# Line 31
RELEASES = ["v2.10", "v2.11"]
```

This misses all releases from v2.12 through v2.16, meaning cumulative doc validation is incomplete.

### Impact

- Cumulative docs for v2.12-v2.16 are never audited
- Historical regressions can go undetected
- Release gate validation is incomplete

### Proposed Solution

Replace hardcoded list with dynamic detection:

```python
def get_all_releases() -> list[str]:
    """Dynamically detect all releases from docs/releases/ directory."""
    releases_dir = Path("docs/releases")
    if not releases_dir.exists():
        return []
    
    releases = []
    for d in releases_dir.iterdir():
        if d.is_dir() and d.name.startswith("v"):
            releases.append(d.name)
    
    # Sort by version number (newest first)
    releases.sort(key=lambda x: [int(p) for p in x[1:].split(".")], reverse=True)
    return releases

RELEASES = get_all_releases()
```

### Affected Files

- `scripts/audit_cumulative_docs.py` (line 31)

---

## Gap 3: .githooks/pre-receive — Incorrect Cumulative Thresholds

### Problem

The pre-receive hook has incorrect minimum line counts for cumulative DOC-3 and DOC-5 when the `cumulative:true` flag is set:

```bash
# Lines 100-106: Incorrect thresholds for cumulative docs
DOC-1) min_lines=500 ;;
DOC-2) min_lines=500 ;;
DOC-3) min_lines=300 ;;   # Should be 100 (DOC-3 is release-specific per IDEA-021)
DOC-4) min_lines=300 ;;
DOC-5) min_lines=200 ;;   # Should be 50 (DOC-5 is release-specific per IDEA-021)
```

Per IDEA-021 and RULE 12, DOC-3 and DOC-5 are **release-specific**, not cumulative:
- DOC-3 minimum: 100 lines (not 300)
- DOC-5 minimum: 50 lines (not 200)

### Impact

- Pre-receive hook incorrectly rejects valid release-specific DOC-3/DOC-5 files
- Valid releases could be blocked
- Confusion about which thresholds apply

### Proposed Solution

Fix the thresholds in the `check_doc_format()` function:

```bash
# Lines 99-106: Fix cumulative thresholds
case "$doc_name" in
  DOC-1) min_lines=500 ;;
  DOC-2) min_lines=500 ;;
  DOC-3) min_lines=100 ;;   # Release-specific, not cumulative
  DOC-4) min_lines=300 ;;
  DOC-5) min_lines=50 ;;   # Release-specific, not cumulative
  *) min_lines=100 ;;
esac
```

### Affected Files

- `.githooks/pre-receive` (lines 100-106)

---

## Summary of Changes

| Gap | File | Issue | Fix |
|-----|------|-------|-----|
| 1 | `scripts/checkpoint_heartbeat.py` | `log_conversation()` writes placeholder | Capture actual conversation content |
| 2 | `scripts/audit_cumulative_docs.py` | Hardcoded `RELEASES = ["v2.10", "v2.11"]` | Dynamic detection from `docs/releases/` |
| 3 | `.githooks/pre-receive` | Cumulative thresholds 300/200 for DOC-3/5 | Fix to 100/50 (release-specific) |

---

## Affected Files

### Modified (3 files)
- `scripts/checkpoint_heartbeat.py`
- `scripts/audit_cumulative_docs.py`
- `.githooks/pre-receive`

### No new files required

---

## Dependencies

- IDEA-021 (Release-Specific DOC-3/5) — defines thresholds used here
- RULE 8.3 (Conversation Log Mandate) — defines requirement for conversation capture

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking conversation logging | Low | Medium | Test with dry-run before deploying |
| Pre-receive hook blocking valid commits | Medium | High | Fix thresholds, test on a feature branch |
| Missing new releases in audit | Medium | Low | Dynamic detection handles future releases |

---

## Acceptance Criteria

- [ ] `checkpoint_heartbeat.py --log-conversation` writes actual conversation content (not placeholder)
- [ ] `audit_cumulative_docs.py` audits all releases dynamically (v2.10 through latest)
- [ ] `.githooks/pre-receive` enforces correct thresholds: DOC-3 ≥ 100, DOC-5 ≥ 50 (release-specific)
- [ ] All 3 scripts pass test validation
- [ ] Pre-receive hook test passes on a feature branch

---

## Implementation Notes

1. **checkpoint_heartbeat.py**: Consider adding a `--dry-run` flag to test without writing
2. **audit_cumulative_docs.py**: Add `--releases` CLI arg to override dynamic detection if needed
3. **pre-receive hook**: Test with `git log` simulation before deploying to production

---

## Status History

- 2026-04-09: Created from v2.15 consistency review (8 major issues)
- 2026-04-09: Refined — identified 3 specific gaps with exact line references and proposed solutions

---
