# TECH-005: Timebox-First Branch Naming Convention

**Status:** [IDEA]  
**Captured:** 2026-04-08  
**Source:** Gemini follow-up + User correction  
**Classification:** TECHNICAL (How)  
**Parent:** TECH-004 (Master Traceability Tree)

---

## Summary

A timebox-first branch naming pattern that groups feature branches by temporal context (quarter or sprint) while preserving IDEA traceability via prefix. This replaces the original TECH-005 proposal which incorrectly used IDEA-NNN as the folder structure.

---

## Corrected Pattern

```
feature/{Timebox}/{IDEA-NNN}-{slug}
```

**Examples:**

| Timebox Type | Example Branch |
|-------------|-----------------|
| Quarter | `feature/2026-Q2/IDEA-101-authentication` |
| Sprint | `feature/Sprint-42/IDEA-101-authentication` |

---

## Why Timebox-First is Correct

The original TECH-005 proposal used `feature/{IDEA-NNN}/{YYYY}Q{N}-{slug}`, which creates hundreds of single-branch folders (one per IDEA). This is wrong because:

1. **Zero folder clutter** — One folder per timebox, not per ticket
2. **Auto-archiving** — Old timeboxes collapse out of daily view
3. **Instant ID matching** — `IDEA-101` prefix visible without clicking

---

## Comparison with Alternatives

| Pattern | Example | Strength | Weakness |
|---------|---------|----------|----------|
| **ADR-006** | `feature/IDEA-101-authentication` | Flat structure, simple | No temporal grouping, hundreds of top-level folders |
| **TECH-004** | `feature/2026/Q2/T-101-Auth` | Temporal + ticket | Breaks ADR-006 pattern; non-standard prefix |
| **TECH-005 (corrected)** | `feature/2026-Q2/IDEA-101-authentication` | Temporal grouping + IDEA traceability | Still breaks flat ADR-006 pattern |

---

## Compatibility Analysis

### ADR-006 Pattern
ADR-006 defines feature branches as: `feature/{IDEA-NNN}-{slug}`

### Breaking Change Assessment

**Does TECH-005 break existing branches?**

No — TECH-005 is a **forward-only change**. Existing branches following ADR-006's flat pattern do not need to be renamed. They are compatible as:
- Legacy: `feature/IDEA-101-authentication` (no timebox)
- New: `feature/2026-Q2/IDEA-101-authentication` (with timebox)

### Decision: Replace or Variant?

TECH-005 should **replace** the original incorrect content rather than exist as a v2 variant, because:

1. The original pattern was fundamentally wrong (IDEA-NNN as folder)
2. This is a correction, not a new version
3. No branches have been created using the wrong pattern yet

---

## Recommendation

**Status:** [REFINED] — awaiting ACCEPTED/REJECTED

### If ACCEPTED

Update RULE 10.1 in `.clinerules` and `prompts/SP-002-clinerules-global.md` to use:

```
feature/{Timebox}/{IDEA-NNN}-{slug}
```

Where `{Timebox}` is either:
- `YYYY-QN` (e.g., `2026-Q2`) for quarterly cycles
- `Sprint-NN` (e.g., `Sprint-42`) for sprint-based cycles

### Integration with ADR-006

ADR-006 RULE 10.1 table should be updated to reflect this naming convention. The feature branch row changes from:

| `feature/{IDEA-NNN}-{slug}` | Single feature or fix. | Branch from `develop` or `develop-vX.Y`, merge back via PR, then delete. |

To:

| `feature/{Timebox}/{IDEA-NNN}-{slug}` | Single feature or fix grouped by timebox. | Branch from `develop` or `develop-vX.Y`, merge back via PR, then delete. |

---

## Related

- TECH-004 (Master Traceability Tree) — parent proposal
- ADR-006 (develop/main branching model) — base convention being modified
