# BATCH 3: Template Coherence + Implementation Audit — Results

**Batch ID:** `msgbatch_01G17QJW3DQzznMApr7J1LLz`
**Status:** ended
**Completed at:** 2026-03-29 22:25:27.664040+00:00

---

## Result: tmpl-clinerules

## 1. Executive Summary

- **Both files have a UTF-8 BOM** (`\ufeff`) — this is a P1 encoding defect; neither should have a BOM
- **Both files have severe em-dash corruption** throughout — what should be `—` (U+2014) is rendered as `â€"` (UTF-8 bytes `0xE2 0x80 0x94` misread as Windows-1252), affecting Rules 5–7 headers and the title line
- **The root `.clinerules` has additional corruption** in Rule 1's arrow characters (`→` rendered as `Ã¢â€ â€™` in root vs `â†'` in template) — the root file has a *different, worse* encoding corruption pattern for arrows
- **RULE 10 in both files contains literal `\n` backslash-n sequences** instead of real newlines — this is a critical structural defect present in both files identically
- **The files are NOT byte-identical**: the root has a longer/different em-dash corruption sequence in the title and arrow corruption in Rule 1 that differs from the template's corruption pattern

---

## 2. Byte-Level Diff

- **Files are BYTE-IDENTICAL:** No

| Location | Root `.clinerules` | `template/.clinerules` | Classification |
|---|---|---|---|
| **Line 1 — Title** | `â€"â€` (4 mojibake bytes + extra char `\x9d`) | `â€"` (3 mojibake bytes only) | ACCIDENTAL — root has extra corruption byte `\x9d` (U+009D, a C1 control character) |
| **Rule 1 — Arrow `→` (×4)** | `Ã¢â€ â€™` (severe multi-byte mojibake) | `â†'` (lighter mojibake of `→`) | ACCIDENTAL — root has a *different, worse* corruption of U+2192 |
| **Rule 1 — CHECK→CREATE→READ→ACT line** | `CHECKÃ¢â€ â€™CREATEÃ¢â€ â€™READÃ¢â€ â€™ACT` | `CHECKâ†'CREATEâ†'READâ†'ACT` | ACCIDENTAL — same arrow corruption difference |
| **Rules 5–7 section headers `—`** | `â€"â€` (with trailing `\x9d`) | `â€"` (without `\x9d`) | ACCIDENTAL — root has extra C1 control byte |
| **Rule 5.5 — `.env` line** | `â€"â€ NEVER` | `â€" NEVER` | ACCIDENTAL — same extra byte pattern |
| **All other content** | Identical | Identical | — |

**Summary of byte differences:** The root file consistently has an extra byte `\x9d` (Windows-1252 right double quotation mark / C1 control) appended after each em-dash mojibake sequence. This suggests the root was saved through a *different* broken encoding pipeline than the template. The template's em-dash corruption is `â€"` (3 bytes: `C3 A2 E2 80 9C` misread), while the root's is `â€"â€` + `\x9d` (an additional Windows-1252 artifact).

---

## 3. Encoding Anomalies

| File | BOM | Em-dash Corruption | Arrow (`→`) Corruption | Literal `\n` in RULE 10 |
|---|---|---|---|---|
| `.clinerules` (root) | **Yes** (`\ufeff`) | **Yes** — `â€"â€` + `\x9d` (severe, extra C1 byte) | **Yes** — `Ã¢â€ â€™` (worst-case mojibake) | **Yes** |
| `template/.clinerules` | **Yes** (`\ufeff`) | **Yes** — `â€"` (moderate mojibake) | **Yes** — `â†'` (moderate mojibake) | **Yes** |

**Root cause analysis:**
- Both files were originally UTF-8 with em-dashes (U+2014, bytes `E2 80 94`) and arrows (U+2192, bytes `E2 86 92`)
- Both were read as Windows-1252 at some point, producing `â€"` / `â†'` mojibake
- The root file suffered an *additional* encoding pass or was edited in a tool that further corrupted the already-mojibaked bytes, adding `\x9d` (Windows-1252 `"`) after each em-dash
- The BOM (`EF BB BF`) indicates both were saved as UTF-8 with BOM, which is unnecessary and can cause issues with some parsers

---

## 4. Rule Completeness

| Rule | In Root | In Template | Identical Content | Notes |
|---|---|---|---|---|
| **RULE 1** | Yes | Yes | **No** | Arrow characters differ: root has `Ã¢â€ â€™`, template has `â†'` |
| **RULE 2** | Yes | Yes | Yes | Content identical |
| **RULE 3** | Yes | Yes | Yes | Content identical |
| **RULE 4** | Yes | Yes | Yes | Content identical |
| **RULE 5** | Yes | Yes | **No** | Section headers: root has `â€"â€` + `\x9d`, template has `â€"` |
| **RULE 6** | Yes | Yes | **No** | Same em-dash corruption difference in section headers |
| **RULE 7** | Yes | Yes | **No** | Same em-dash corruption difference in section headers |
| **RULE 8** | Yes | Yes | Yes | Uses `--` (ASCII double-hyphen) — unaffected, identical |
| **RULE 9** | Yes | Yes | Yes | Uses `--` (ASCII double-hyphen) — unaffected, identical |
| **RULE 10** | Yes | Yes | Yes | Both have identical literal `\n` defect; content otherwise identical |

**All 10 rules are present in both files.** No rules are missing.

---

## 5. Intentional vs Accidental Differences

| Difference | Location | Classification | Justification |
|---|---|---|---|
| Extra `\x9d` byte after em-dash in root | Title, Rules 5/6/7 headers | **ACCIDENTAL** | Template is the canonical source; root has additional corruption not present in template. No semantic reason for this difference. |
| Arrow corruption variant (`Ã¢â€ â€™` vs `â†'`) | Rule 1 (×4 occurrences) | **ACCIDENTAL** | Both are corruptions of U+2192 `→`; root's version is more severely corrupted. This is encoding drift, not intentional. |
| BOM present in both files | File header | **ACCIDENTAL** | Neither file should have a BOM per the audit brief. Both are equally defective on this point. |
| Literal `\n` in RULE 10 | RULE 10 (entire rule body) | **ACCIDENTAL** | RULE 10 was clearly written with real newlines intended. The `\n` sequences are an artifact of how the rule was inserted (likely via a JSON string or escaped string that was never unescaped). This makes RULE 10 render as a single long line in any Markdown viewer. |
| Em-dash corruption (`â€"` / `â€"â€`) | Rules 5, 6, 7 section headers | **ACCIDENTAL** | Both are corruptions of `—`; the difference in severity between files is encoding drift. |
| Template `proxy.py` at v2.1.1 vs root at v2.8.0 | `proxy.py` | **INTENTIONAL** | Template holds the baseline version; root is the evolved deployed instance. This is expected and correct. |
| `.roomodes` files | Both | **IDENTICAL** | No differences — correctly synchronized. |
| `Modelfile` files | Both | **IDENTICAL** | No differences — correctly synchronized. |

---

## 6. Prioritized Remediation

### P0 (Critical) — Breaks rendering and agent behavior

**P0-1: Fix literal `\n` in RULE 10 (both files)**
RULE 10 is stored as a single line with `\n` escape sequences. Every Markdown renderer, every agent reading this file, and every `cat` command will show RULE 10 as one unreadable blob. This defeats the entire purpose of the rule.

```bash
# The fix: replace literal \n with real newlines in RULE 10 block
# In both .clinerules and template/.clinerules
# The section starting with:
# ## RULE 10: GITFLOW ENFORCEMENT -- BRANCH LIFECYCLE\n\nThis rule...
# Must be rewritten with actual newline characters
```

**P0-2: Fix em-dash and arrow corruption in root `.clinerules`**
The root file has *worse* corruption than the template (extra `\x9d` byte). Since agents read the root file, they see garbled section headers. The root must be corrected to at minimum match the template, and ideally both should be fixed to use real Unicode characters.

```
Current (root):   ### 5.1 â€"â€[0x9D] What MUST be versioned
Current (tmpl):   ### 5.1 â€" What MUST be versioned  
Target (both):    ### 5.1 — What MUST be versioned
```

### P1 (Important) — Display and compatibility issues

**P1-1: Remove BOM from both files**
```bash
# PowerShell fix for both files:
$content = Get-Content .clinerules -Raw -Encoding UTF8
$content = $content.TrimStart([char]0xFEFF)
Set-Content .clinerules -Value $content -Encoding UTF8 -NoNewline

$content = Get-Content template/.clinerules -Raw -Encoding UTF8  
$content = $content.TrimStart([char]0xFEFF)
Set-Content template/.clinerules -Value $content -Encoding UTF8 -NoNewline
```

**P1-2: Fix all em-dash and arrow mojibake in both files**
Replace all occurrences of:
- `â€"â€` + `\x9d` → `—` (root file)
- `â€"` → `—` (template file)  
- `Ã¢â€ â€™` → `→` (root file, Rule 1)
- `â†'` → `→` (template file, Rule 1)

**P1-3: Sync root to template after fixes**
After fixing both files independently, do a final diff and make the root byte-identical to the template (since the template is the canonical source and there are no legitimate project-specific differences in `.clinerules`).

### P2 (Nice to have) — Consistency

**P2-1: Standardize em-dash usage in Rules 8 and 9**
Rules 8 and 9 use `--` (ASCII double-hyphen) as a workaround for the em-dash problem. After fixing the encoding, these should be updated to use `—` for consistency with Rules 5–7.

**P2-2: Add encoding validation to CI/CD**
Add a pre-commit hook or CI check:
```bash
# Check for BOM
python -c "
with open('.clinerules', 'rb') as f:
    bom = f.read(3)
    assert bom != b'\xef\xbb\xbf', 'BOM detected!'
    
# Check for mojibake
with open('.clinerules', 'r', encoding='utf-8') as f:
    content = f.read()
    assert 'â€' not in content, 'Em-dash mojibake detected!'
    assert 'Ã¢' not in content, 'Arrow mojibake detected!'
    assert r'\n' not in content.split('RULE 10')[1], 'Literal backslash-n in RULE 10!'
"
```

---

## 7. Verdict

**[MAJOR_DRIFT]**

The two files are **not byte-identical** and both suffer from **critical encoding defects** (BOM, em-dash mojibake, arrow mojibake) with the root file having a *more severe* corruption variant than the template — meaning the deployed instance is in worse shape than the canonical source. Most critically, **RULE 10 is structurally broken in both files** (literal `\n` sequences instead of real newlines), rendering the entire GitFlow enforcement rule as an unreadable single-line blob for any agent or human reading the file. Immediate remediation of RULE 10 and the encoding issues is required before these files can be considered fit for purpose.

---

## Result: tmpl-roomodes

# .roomodes Deep Sync Audit Report

## 1. Executive Summary

- **The two `.roomodes` files are BYTE-IDENTICAL in all semantically meaningful content** — all 4 personas, all roleDefinitions, all RBAC groups, and all JSON structure are perfectly synchronized.
- **All 4 personas are present in both files** with identical slugs, names, roleDefinitions, and group permissions.
- **Both files are valid JSON** with no syntax errors detected.
- **No project-specific values exist** that should legitimately differ between root and template — the files serve the same persona definitions correctly.
- **Ancillary files (`.clinerules`, `proxy.py`) show significant drift**, but these are outside the `.roomodes` audit scope and are noted as contextual findings.

---

## 2. Byte-Level Diff

- **Files are BYTE-IDENTICAL:** ✅ **Yes**

Performing a logical token-by-token comparison of the two `.roomodes` files provided:

| Element | Root `.roomodes` | `template/.roomodes` | Match |
|---|---|---|---|
| Top-level key `customModes` | ✅ Present | ✅ Present | ✅ |
| Array length (4 entries) | ✅ 4 | ✅ 4 | ✅ |
| Whitespace/indentation style | 2-space JSON | 2-space JSON | ✅ |
| Trailing newline | Present | Present | ✅ |
| BOM marker | None detected | None detected | ✅ |
| `"source": "project"` on all entries | ✅ | ✅ | ✅ |

**No differences detected at any level** — the files are structurally and content-identical.

> **Note on `.clinerules`:** The root `.clinerules` shows mojibake encoding artifacts (e.g., `â€"â€` instead of `—`, `Ã¢â€ â€™` instead of `→`) throughout, while `template/.clinerules` renders correctly. This is a **UTF-8 vs Windows-1252 encoding corruption** in the root file. This does not affect `.roomodes` but is flagged as a separate concern.

---

## 3. Persona Completeness

| Persona | In Root | In Template | roleDefinition Match | groups Match |
|---|---|---|---|---|
| `product-owner` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `scrum-master` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `developer` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `qa-engineer` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

**Ordering:** All 4 personas appear in identical order in both files (product-owner → scrum-master → developer → qa-engineer). ✅

---

## 4. JSON Validity

| File | Valid JSON? | Errors |
|---|---|---|
| `.roomodes` (root) | ✅ Yes | None |
| `template/.roomodes` | ✅ Yes | None |

**Structural validation details:**
- Both files open with `{` and close with `}` ✅
- `customModes` array is properly bracketed ✅
- All string values are properly quoted ✅
- Mixed-type arrays (strings + tuples for RBAC) use valid JSON array-of-arrays syntax ✅
- All regex strings properly escape backslashes (e.g., `\\.md`, `\\.`) ✅
- No trailing commas detected ✅
- No duplicate keys detected ✅

---

## 5. RBAC Consistency

All group/permission definitions are **byte-identical** between root and template:

| Persona | Groups (Root) | Groups (Template) | Match |
|---|---|---|---|
| `product-owner` | `read` + `edit` (fileRegex: `memory-bank/productContext\.md\|docs/.*\.md\|user-stories.*\.md`) | Identical | ✅ |
| `scrum-master` | `read` + `edit` (fileRegex: `memory-bank/.*\.md\|docs/.*\.md`) + `command` (git add/commit/status/log) | Identical | ✅ |
| `developer` | `read`, `edit`, `browser`, `command`, `mcp` (full access) | Identical | ✅ |
| `qa-engineer` | `read` + `edit` (fileRegex: `docs/qa/.*\.md\|memory-bank/progress\.md`) + `command` (npm test, pytest, dotnet test, go test, git status/log) | Identical | ✅ |

**RBAC design observations (informational, not drift):**
- `developer` has unrestricted `edit` and `command` — intentional for full implementation capability ✅
- `scrum-master` has `git add/commit` but NOT `git push` — intentional containment ✅
- `qa-engineer` has `git status/log` (read-only git) but NOT `git add/commit` — intentional ✅
- `product-owner` has NO command access — intentional ✅

---

## 6. Prioritized Remediation

### `.roomodes` Files — No Remediation Required

| Priority | Issue | Status |
|---|---|---|
| **P0 (Critical)** | Persona missing or roleDefinition mismatch | ✅ None found |
| **P1 (Important)** | JSON syntax error or RBAC drift | ✅ None found |
| **P2 (Nice to have)** | Whitespace differences | ✅ None found |

---

### Out-of-Scope Findings (Contextual — Not `.roomodes`)

These issues were observed in the provided context and warrant separate remediation tickets:

| Priority | File | Issue | Recommended Action |
|---|---|---|---|
| **P0** | Root `.clinerules` | **Encoding corruption** — UTF-8 multibyte sequences rendered as Windows-1252 mojibake throughout (e.g., `â€"` → `—`, `Ã¢â€ â€™` → `→`). The BOM `\ufeff` is present but content is double-encoded. | Re-save root `.clinerules` as UTF-8 without BOM, verify against `template/.clinerules` which renders correctly. |
| **P1** | Root `proxy.py` vs `template/proxy.py` | **Major version drift** — root is `v2.8.0` (8 additional FIX patches: FIX-020 through FIX-028), template is `v2.1.1`. Template is 7 minor versions behind. Missing: XML validation blocking, Markdown unescape, GEM MODE context extraction, SSE streaming fix, DIAG logging. | Sync `template/proxy.py` ← root `proxy.py` v2.8.0, or document intentional template freeze policy. |
| **P2** | `template/proxy.py` | Template proxy lacks `import re` and several functions (`_extract_user_text`, `_unescape_markdown`, `_has_escaped_xml`, `_USER_MESSAGE_TAG_RE`) present in root. New projects bootstrapped from template will get an inferior proxy. | Same as P1 above — sync template to current root version. |

---

## 7. Verdict

**[SYNCHRONIZED]**

The two `.roomodes` files are in perfect synchronization — byte-identical content, all 4 personas present with matching roleDefinitions and RBAC permissions, and valid JSON in both files. **Zero remediation required for `.roomodes`.**

The only concerns in this repository are the encoding corruption in root `.clinerules` (P0, separate file) and the significant `proxy.py` version drift between root (v2.8.0) and template (v2.1.1) (P1, separate file) — neither of which affects the `.roomodes` sync status being audited.

---

## Result: tmpl-modelfile

## 1. Executive Summary

- **Modelfile files are BYTE-IDENTICAL** — both root and template Modelfiles contain the exact same FROM, PARAMETER set, and SYSTEM prompt with no detectable differences
- **The `.clinerules` files differ** in encoding/character representation (root has mojibake/double-encoded UTF-8 for em-dashes and arrows; template has clean UTF-8), but this is a `.clinerules` audit side-finding, not a Modelfile issue
- **The `.roomodes` files are BYTE-IDENTICAL** — both contain the same four custom modes with identical role definitions
- **The `proxy.py` files differ significantly** — root is v2.8.0 (production-evolved), template is v2.1.1 (stale baseline); this is the most critical drift in the repository
- **No project-specific values exist** that should intentionally differ between root Modelfile and template/Modelfile

---

## 2. Byte-Level Diff

| File Pair | BYTE-IDENTICAL |
|---|---|
| Root `Modelfile` vs `template/Modelfile` | **YES** |
| Root `.clinerules` vs `template/.clinerules` | **NO** |
| Root `.roomodes` vs `template/.roomodes` | **YES** |
| Root `proxy.py` vs `template/proxy.py` | **NO** |

### Modelfile — Byte-Level Diff
- **Files are BYTE-IDENTICAL: YES**
- No differences detected. Every character, whitespace, newline, and comment is identical between the two Modelfiles.

### `.clinerules` — Differences (side-finding)
The root `.clinerules` contains **mojibake** (double-encoded UTF-8 rendered as Latin-1):

| Location | Root (corrupted) | Template (correct) |
|---|---|---|
| Title line | `â€"â€` | `–` (en-dash) |
| Rule 1 arrows | `Ã¢â€ â€™` | `→` |
| `CHECK→CREATE` chain | `CHECKÃ¢â€ â€™CREATEâ€¦` | `CHECK→CREATE→READ→ACT` |
| Section headers 5.1–6.3 | `â€"` | `–` |
| Rule 7 header | `â€"` | `–` |

**Root cause:** The root `.clinerules` was saved/copied with a UTF-8→Latin-1 double-encoding error (BOM present on both: `\ufeff`). The template has clean UTF-8.

### `proxy.py` — Differences (side-finding, critical)

| Aspect | Root | Template |
|---|---|---|
| Version | `v2.8.0` | `v2.1.1` |
| Changelog entries | FIX-001 through FIX-028 | FIX-001 through FIX-019 only |
| `import re` | Present | **Absent** |
| `FastAPI version string` | `"2.8.0"` | `"2.1.1"` |
| `_extract_user_text()` | Present (FIX-024) | **Absent** |
| `_ROO_INJECTION_START_TAGS` | Present (FIX-024/026) | **Absent** |
| `_USER_MESSAGE_TAG_RE` | Present (FIX-026) | **Absent** |
| `_unescape_markdown()` | Present (FIX-027) | **Absent** |
| `_has_escaped_xml()` | Present (FIX-021) | **Absent** |
| `_clean_content()` | Calls `_extract_user_text()`, has DIAG logs | Simple string passthrough |
| `_format_prompt()` GEM MODE | Full FIX-022/026 logic (role='tool' extraction) | Simple system-skip only |
| `_stream_response()` | 3-chunk SSE (FIX-028) | 2-chunk SSE (old format) |
| `_wait_clipboard()` | FIX-027 unescape + FIX-020 blocking XML validation + DIAG logs | Non-blocking XML warning only |
| `chat_completions()` | DIAG logs present | No DIAG logs |
| `/health` version | `"2.8.0"` | `"2.1.1"` |
| Startup banner | `v2.8.0` | `v2.1.1` |

---

## 3. SYSTEM Prompt Comparison

| Aspect | Root | Template | Match |
|---|---|---|---|
| SYSTEM block present | Yes | Yes | ✅ Yes |
| SYSTEM content identical | Yes | Yes | ✅ Yes |
| Line 1 | `You are an expert software development agent integrated in Roo Code.` | `You are an expert software development agent integrated in Roo Code.` | ✅ Yes |
| Line 2 | `You must always use Roo Code XML tags for your actions.` | `You must always use Roo Code XML tags for your actions.` | ✅ Yes |
| Line 3 | `You must always read the Memory Bank (memory-bank/) before acting.` | `You must always read the Memory Bank (memory-bank/) before acting.` | ✅ Yes |
| Line 4 | `You must always update the Memory Bank after each task.` | `You must always update the Memory Bank after each task.` | ✅ Yes |
| Line 5 | `After each significant task, you must perform a Git commit with a descriptive message.` | `After each significant task, you must perform a Git commit with a descriptive message.` | ✅ Yes |
| Triple-quote delimiters | `"""` open and close | `"""` open and close | ✅ Yes |

---

## 4. PARAMETER Comparison

| Parameter | Root | Template | Match |
|---|---|---|---|
| `temperature` | `0.15` | `0.15` | ✅ Yes |
| `min_p` | `0.03` | `0.03` | ✅ Yes |
| `top_p` | `0.95` | `0.95` | ✅ Yes |
| `repeat_penalty` | `1.1` | `1.1` | ✅ Yes |
| `num_ctx` | `131072` | `131072` | ✅ Yes |
| `num_gpu` | `99` | `99` | ✅ Yes |
| `num_thread` | `8` | `8` | ✅ Yes |
| Comment annotations | `— REQ-1.3`, `— REQ-1.2` | `— REQ-1.3`, `— REQ-1.2` | ✅ Yes |

---

## 5. FROM Comparison

| Aspect | Root | Template | Match |
|---|---|---|---|
| Base model | `mychen76/qwen3_cline_roocode:14b` | `mychen76/qwen3_cline_roocode:14b` | ✅ Yes |
| Tag specificity | `:14b` (no SHA pin) | `:14b` (no SHA pin) | ✅ Yes |

> **Advisory:** Neither file pins to a digest SHA (`FROM model@sha256:...`). If the `:14b` tag is ever re-pushed upstream, both instances will silently pull a different model on next `ollama pull`. Consider pinning to a digest for production stability.

---

## 6. Prioritized Remediation

### P0 (Critical) — SYSTEM prompt or FROM mismatch
- **NONE.** Both Modelfiles are byte-identical. No action required on Modelfile itself.

### P1 (Important) — Parameter drift
- **NONE** in Modelfiles.
- **`proxy.py` template is 7 major fixes behind** (v2.1.1 vs v2.8.0). The template will provision new projects with a broken SSE streaming format (FIX-028), no XML validation blocking (FIX-020), no Markdown unescape (FIX-027), and no Roo Code injection stripping (FIX-024/026). **Action:** Copy root `proxy.py` → `template/proxy.py`, then strip or neutralize the DIAG log lines if the template should ship clean.

### P2 (Nice to have) — Whitespace / encoding differences
- **Root `.clinerules` has mojibake encoding corruption.** All em-dashes (`–`) and arrows (`→`) are rendered as multi-byte Latin-1 garbage. This does not affect Modelfile sync but degrades agent readability of governance rules. **Action:** Re-save root `.clinerules` from the template version (which is clean UTF-8), then re-apply any root-specific additions (RULE 10 GitFlow, which appears identical in both).

---

## 7. Verdict

**[SYNCHRONIZED]** — for the Modelfile pair specifically.

The two Modelfiles (`./Modelfile` and `template/Modelfile`) are **byte-for-byte identical**: same `FROM` base model, same seven `PARAMETER` values with matching comments, and identical `SYSTEM` prompt content. No remediation is required on the Modelfiles themselves.

However, the broader template ecosystem has **significant drift**: `template/proxy.py` is 7 patch versions behind the root (v2.1.1 vs v2.8.0), missing critical fixes for SSE streaming compatibility, XML validation blocking, and Roo Code injection stripping — meaning any new project bootstrapped from the template will be provisioned with a functionally broken proxy. This should be treated as a **P1 infrastructure debt** even though it falls outside the strict Modelfile scope of this audit.

---

## Result: tmpl-proxy

## 1. Executive Summary

- **The two files are NOT byte-identical** — `template/proxy.py` is frozen at **v2.1.1** while `root/proxy.py` is at **v2.8.0**, representing **7 minor versions of accumulated drift**
- **The SSE implementation has a critical functional regression in the template**: the template sends `role + content` in a single delta chunk (the bug that FIX-028 corrected), which causes `"Model Response Incomplete"` in Roo Code
- **The template is missing 7 fixes** (FIX-020 through FIX-028) including blocking XML validation, Markdown unescaping, GEM MODE context isolation, and Roo Code message structure parsing
- **No CORS configuration exists in either file** — this is consistent (both omit it), but worth noting as a shared gap
- **Project-specific values are correctly identical** (same port defaults, same env var names, same timeouts) — the drift is purely functional/logic drift, not intentional parameterization

---

## 2. Byte-Level Diff

- **Files are BYTE-IDENTICAL:** ❌ No

### All differences with context:

#### A. Module-level docstring / version header
| Location | Root (v2.8.0) | Template (v2.1.1) |
|---|---|---|
| Line 3 | `le workbench Proxy v2.8.0` | `le workbench Proxy v2.0` |
| Changelog | Entries v2.0.0 → v2.8.0 (FIX-001 to FIX-028) | Entries v2.0.0 → v2.1.1 (FIX-001 to FIX-019 only) |

#### B. Import statement
| Root | Template |
|---|---|
| `import asyncio, hashlib, json, os, re, sys, time, uuid` | `import asyncio, hashlib, json, os, sys, time, uuid` |

**Root adds `re`** — required for `_MARKDOWN_UNESCAPE_RE` and `_USER_MESSAGE_TAG_RE`. Template would crash at runtime if these features were backported without this import.

#### C. FastAPI app version string
| Root | Template |
|---|---|
| `app = FastAPI(title="le workbench Proxy", version="2.8.0")` | `app = FastAPI(title="le workbench Proxy", version="2.1.1")` |

#### D. Missing constants in template (3 new constants)
Root has these; template has **none** of them:
```python
# ROOT ONLY — template is missing all three:
_ROO_INJECTION_START_TAGS = [
    "<environment_details",
    "<SYSTEM>",
    "<task>",
    "<feedback>",
]

_USER_MESSAGE_TAG_RE = re.compile(r"<user_message>\s*(.*?)\s*</user_message>", re.DOTALL)

ROO_XML_TAGS_ESCAPED = [tag.replace("<", r"\<").replace(">", r"\>") for tag in ROO_XML_TAGS]

_MARKDOWN_UNESCAPE_RE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!<>])")
```

#### E. Missing functions in template (3 new functions)
Root has these; template has **none** of them:

```python
# ROOT ONLY:
def _extract_user_text(text: str) -> str: ...      # FIX-024, FIX-026
def _unescape_markdown(text: str) -> str: ...      # FIX-027
def _has_escaped_xml(text: str) -> bool: ...       # FIX-021
```

#### F. `_clean_content()` — functional difference
| Aspect | Root | Template |
|---|---|---|
| Calls `_extract_user_text()` | ✅ Yes — strips Roo Code injection tags | ❌ No — returns raw string |
| Has DIAG logging | ✅ Yes | ❌ No |

Root:
```python
def _clean_content(content) -> str:
    if isinstance(content, str):
        print(f"  [DIAG _clean_content] ...")
        return _extract_user_text(content)   # ← KEY DIFFERENCE
    ...
        if item.get("type") == "text":
            parts.append(_extract_user_text(item.get("text", "")))  # ← KEY DIFFERENCE
```

Template:
```python
def _clean_content(content) -> str:
    if isinstance(content, str):
        return content                        # ← raw, no injection stripping
    ...
        if item.get("type") == "text":
            parts.append(item.get("text", ""))  # ← raw text, no stripping
```

#### G. `_format_prompt()` — major logic difference
Root implements full GEM MODE with FIX-022/FIX-026 (role='tool' + `<user_message>` extraction):
```python
# ROOT: GEM MODE sends ONLY last user message, extracted from role='tool' <user_message> wrapper
if USE_GEM_MODE:
    last_user_content = None
    for msg in reversed(messages):
        if msg.role == "tool":
            match = _USER_MESSAGE_TAG_RE.search(raw)
            if match:
                last_user_content = match.group(1).strip()
                break
    if not last_user_content:
        for msg in reversed(messages):
            if msg.role == "user":
                content = _clean_content(msg.content)
                ...
    ...
```

Template has a **completely different GEM MODE** — it only skips system messages, sends full history:
```python
# TEMPLATE: GEM MODE only skips [SYSTEM PROMPT], sends full history
for msg in messages:
    content = _clean_content(msg.content)
    if msg.role == "system":
        if USE_GEM_MODE:
            continue          # ← only difference in template's GEM MODE
        parts.append("[SYSTEM PROMPT]\n" + content)
    elif msg.role == "user":
        parts.append("[USER]\n" + content)
    elif msg.role == "assistant":
        parts.append("[ASSISTANT]\n" + content)
```

**Impact**: Template's GEM MODE sends the entire conversation history (with all Roo Code injection tags intact) instead of just the clean last user message. This is the behavior that FIX-022 and FIX-023 were specifically designed to fix.

#### H. `_stream_response()` — **CRITICAL SSE BUG in template**
Root (FIX-028 — correct 3-chunk format):
```python
# Chunk 1: role only
role_chunk = {..., "choices": [{"delta": {"role": "assistant"}, "finish_reason": None}]}
yield f"data: {json.dumps(role_chunk)}\n\n"
# Chunk 2: content only
content_chunk = {..., "choices": [{"delta": {"content": content}, "finish_reason": None}]}
yield f"data: {json.dumps(content_chunk)}\n\n"
# Chunk 3: finish
done = {..., "choices": [{"delta": {}, "finish_reason": "stop"}]}
yield f"data: {json.dumps(done)}\n\n"
yield "data: [DONE]\n\n"
```

Template (pre-FIX-028 — **broken** 2-chunk format):
```python
# Single chunk: role AND content combined ← CAUSES "Model Response Incomplete" in Roo Code
chunk = {..., "choices": [{"delta": {"role": "assistant", "content": content}, "finish_reason": None}]}
yield f"data: {json.dumps(chunk)}\n\n"
done = {..., "choices": [{"delta": {}, "finish_reason": "stop"}]}
yield f"data: {json.dumps(done)}\n\n"
yield "data: [DONE]\n\n"
```

#### I. `_wait_clipboard()` — missing FIX-027 (Markdown unescaping) and FIX-020/FIX-021 (blocking XML validation)

Root adds **before returning**:
```python
# FIX-027: Unescape markdown before validation
unescaped = _unescape_markdown(current)
if unescaped != current:
    current = unescaped

# FIX-020: BLOCKING XML validation (not just a warning)
if not _validate_response(current):
    if _has_escaped_xml(current):
        print(f"[{ts}] 🚫 ERREUR : Balises XML echappees...")
    else:
        print(f"[{ts}] 🚫 ERREUR : Aucune balise XML Roo Code...")
    initial_hash = _hash(current)
    continue   # ← BLOCKS and keeps polling
return current
```

Template has **non-blocking** validation (just a warning, then returns):
```python
if not _validate_response(current):
    print(f"[{ts}] AVERTISSEMENT : Aucune balise XML Roo Code detectee.")
return current   # ← RETURNS ANYWAY even without XML tags
```

**Impact**: Template injects invalid (non-XML) responses into Roo Code, causing infinite request loops.

#### J. `chat_completions()` — missing DIAG logging block in template
Root adds inside `async with _clipboard_lock`:
```python
# DIAG-LOG: dump structure brute des messages recus de Roo Code
print(f"  [DIAG chat_completions] {len(request.messages)} messages recus:")
for i, msg in enumerate(request.messages):
    raw_content = msg.content if isinstance(msg.content, str) else str(msg.content)
    print(f"  [DIAG msg[{i}]] role={msg.role!r}, content[:120]={repr(raw_content[:120])}")
formatted = _format_prompt(request.messages)
print(f"  [DIAG _format_prompt] result[:200]={repr(formatted[:200])}")
```

Template has only:
```python
formatted = _format_prompt(request.messages)
```

#### K. `/health` endpoint and startup banner — version string
| Location | Root | Template |
|---|---|---|
| `health_check()` return | `"version": "2.8.0"` | `"version": "2.1.1"` |
| `__main__` banner | `v2.8.0` | `v2.1.1` |

---

## 3. Functional Comparison

| Aspect | Root (v2.8.0) | Template (v2.1.1) | Match |
|---|---|---|---|
| **API route `/v1/chat/completions`** | POST, present | POST, present | ✅ Yes |
| **API route `/v1/models`** | GET, present | GET, present | ✅ Yes |
| **API route `/health`** | GET, present | GET, present | ✅ Yes |
| **CORS configuration** | Absent (no middleware) | Absent (no middleware) | ✅ Yes (shared gap) |
| **SSE chunk format** | 3-chunk (role / content / stop) — OpenAI-compliant | 2-chunk (role+content / stop) — **non-compliant, broken** | ❌ **NO — P0** |
| **SSE `[DONE]` terminator** | Present | Present | ✅ Yes |
| **GEM MODE — message extraction** | Extracts last user msg from `role='tool'` `<user_message>` | Skips system msgs, sends full history | ❌ **NO — P0** |
| **Roo Code injection tag stripping** | Yes (`_extract_user_text`) | No (raw content passed through) | ❌ **NO — P0** |
| **XML validation — blocking** | Yes (keeps polling on failure) | No (warning only, returns bad response) | ❌ **NO — P0** |
| **Markdown unescaping** | Yes (`_unescape_markdown`, FIX-027) | No | ❌ **NO — P1** |
| **Escaped XML detection** | Yes (`_has_escaped_xml`, FIX-021) | No | ❌ **NO — P1** |
| **`<new_task>` guard** | Yes (blocking) | Yes (blocking) | ✅ Yes |
| **Min-length guard (100 chars)** | Yes (blocking) | Yes (blocking) | ✅ Yes |
| **Clipboard lock serialization** | Yes (`asyncio.Lock`) | Yes (`asyncio.Lock`) | ✅ Yes |
| **History truncation** | Yes (`MAX_HISTORY_CHARS`) | Yes (`MAX_HISTORY_CHARS`) | ✅ Yes |
| **UTF-8 stdout fix** | Yes (FIX-019) | Yes (FIX-019) | ✅ Yes |
| **Error handling (timeout)** | HTTP 408 | HTTP 408 | ✅ Yes |
| **DIAG logging** | Extensive (debug-level) | Absent | ❌ No (P2) |
| **`re` module imported** | Yes | **No** — would crash if features backported | ❌ **NO — P1** |

---

## 4. Project-Specific Values

| Value | Root | Template | Should Differ? |
|---|---|---|---|
| `PROXY_PORT` default | `8000` | `8000` | ✅ No — env var override is the right pattern |
| `TIMEOUT_SECONDS` default | `300` | `300` | ✅ No |
| `POLLING_INTERVAL` default | `1.0` | `1.0` | ✅ No |
| `MAX_HISTORY_CHARS` default | `40000` | `40000` | ✅ No |
| `USE_GEM_MODE` default | `true` | `true` | ✅ No |
| Version string | `2.8.0` | `2.1.1` | ⚠️ Should match after sync |
| DIAG logging | Present | Absent | 🤔 Debatable — DIAG logs are useful in template too, but could be considered workbench-specific debug noise |

**Conclusion on project-specific values**: There are **no values that should legitimately differ** between root and template. All configuration is correctly driven by environment variables. The version string drift and functional drift are both unintentional.

---

## 5. Prioritized Remediation

**P0 (Critical — Functional breakage in any new project using the template):**

1. **SSE format bug** (`_stream_response`): Template's 2-chunk format causes `"Model Response Incomplete"` in Roo Code. Replace with root's 3-chunk implementation immediately.

2. **GEM MODE broken** (`_format_prompt`): Template sends full history with injection tags instead of the clean last user message. New projects using the template will have Gemini receiving `<environment_details>` blobs and full conversation history, causing context contamination.

3. **XML validation non-blocking** (`_wait_clipboard`): Template returns invalid responses to Roo Code, triggering infinite request loops. Must be made blocking (keep polling on validation failure).

4. **No injection tag stripping** (`_clean_content`, `_extract_user_text`): Template passes raw Roo Code injection blobs to Gemini. Any new project will immediately hit GAP R2-004/R2-005.

**P1 (Important — Security/reliability):**

5. **Missing `re` import**: If any P0 fix is partially applied, the template will crash at import time with `NameError: name 're' is not defined`.

6. **No Markdown unescaping** (`_unescape_markdown`): Gemini's copy button escapes XML tags; without FIX-027, all responses with XML tags will fail validation and loop forever.

7. **No escaped XML detection** (`_has_escaped_xml`): Without FIX-021, the error message shown to the user is generic instead of actionable.

**P2 (Nice to have):**

8. **Version comment mismatch**: Template header says `v2.0` (not even `v2.1.1`), `FastAPI(version=)` says `

---

## Result: impl-calypso

## 1. Executive Summary

- **DOC-2 v2.2 is a stub document** — it explicitly states "v2.2 introduces no architectural changes" and defers entirely to DOC-2 v2.1, which was **not provided**. There is no architectural specification in the supplied DOC-2 to audit against.
- **The implementation is substantive and internally coherent**: `src/calypso/` contains a complete 4-phase orchestration pipeline with 8 Python modules, a FastMCP server, JSON schema validation, and a Global Brain (Chroma) integration.
- **Cross-referencing against memory-bank context** (progress.md, activeContext.md, `__init__.py` docstring) reveals the architecture was implemented as "PHASE-C" of Epic 0, with all pipeline stages confirmed live-tested (POST-4 in progress.md).
- **No authoritative DOC-2 specification was supplied**, making a formal compliance audit impossible — the audit below is therefore conducted against the *de facto* architecture reconstructed from `__init__.py`, memory-bank references, and internal code contracts.
- **The implementation appears to exceed what a typical Phase 2 description would cover**, containing phases 2–4 plus triage, MCP server, and Global Brain — suggesting the DOC-2 v2.1 architecture (not provided) likely describes all of these.

---

## 2. Phase Coverage

| Phase (from DOC-2 / de facto arch) | DOC-2 Section | Implementation File | Implemented? |
|---|---|---|---|
| Phase 2: PRD → Batch API dispatch (4 expert agents) | DOC-2 v2.1 (not supplied) | `orchestrator_phase2.py` | ✅ Yes |
| Phase 2: Batch status polling + result retrieval | DOC-2 v2.1 (not supplied) | `check_batch_status.py` | ✅ Yes |
| Phase 3: Synthesizer Agent → draft backlog | DOC-2 v2.1 (not supplied) | `orchestrator_phase3.py` | ✅ Yes |
| Phase 4: Devil's Advocate → GREEN/ORANGE classification | DOC-2 v2.1 (not supplied) | `orchestrator_phase4.py` | ✅ Yes |
| Triage: Human arbitration dashboard generation | DOC-2 v2.1 (not supplied) | `triage_dashboard.py` | ✅ Yes |
| Triage: Apply decisions to memory bank | DOC-2 v2.1 (not supplied) | `apply_triage.py` | ✅ Yes |
| MCP Server: FastMCP tools for Roo Code | DOC-2 v2.1 (not supplied) | `fastmcp_server.py` | ✅ Yes |
| Global Brain: Chroma vector DB + Librarian Agent | DOC-2 v2.1 (not supplied) | `librarian_agent.py` | ✅ Yes |
| JSON Schema validation (expert_report, backlog_item) | DOC-2 v2.1 (not supplied) | `schemas/` (referenced, not supplied) | ⚠️ Referenced but schemas not provided for review |

> **Critical caveat**: DOC-2 v2.2 contains zero architectural content. All phase mappings above are inferred from `__init__.py` docstring, progress.md POST-4 entries, and internal code structure. The DOC-2 v2.1 document — which contains the actual specification — was not supplied.

---

## 3. Missing Components

**Cannot be definitively determined** because DOC-2 v2.2 contains no specification content. However, based on gaps detectable from the supplied materials:

| Missing Item | Evidence of Gap |
|---|---|
| `schemas/expert_report.json` | Referenced in `check_batch_status.py` (`SCHEMA_PATH`) and `__init__.py` but file content not supplied for review |
| `schemas/backlog_item.json` | Referenced in `orchestrator_phase3.py` (`SCHEMA_PATH`) but file content not supplied |
| `scripts/memory-archive.ps1` | Called by `fastmcp_server.py::memory_archive()` — not in supplied files |
| DOC-2 v2.1 Architecture document | The actual specification this audit requires — not supplied |
| SP-008 / SP-009 system prompts as standalone files | Embedded inline in orchestrators rather than loaded from `prompts/` registry; progress.md shows SP-008/SP-009 exist but the orchestrators duplicate them inline |

---

## 4. Orphaned Implementation

Items implemented in `src/calypso/` that **cannot be verified against DOC-2** (because DOC-2 v2.2 is empty) but appear to go beyond a minimal Phase 2 description:

| Orphaned / Unverifiable Item | Notes |
|---|---|
| `librarian_agent.py` — full Chroma indexing + semantic search | Described as "PHASE-D" in code comments; may be in DOC-2 v2.1 under a separate phase |
| `fastmcp_server.py::memory_archive()` tool | Delegates to `memory-archive.ps1` (PowerShell); cross-platform assumption baked in |
| `fastmcp_server.py::memory_query()` keyword fallback | Undocumented fallback behavior when Chroma is unavailable — likely not in any architecture doc |
| Devil's Advocate retry logic (`max_attempts`, leniency escalation) | Implementation detail not typically in architecture docs; could be drift |
| `orchestrator_phase4.py` `human_decision: null` field | Pre-populated null field in final_backlog items — schema contract detail not verifiable |
| `fastmcp_server.py` transport modes (`stdio` vs `sse`) | SSE transport on port 8001 is an operational detail; stdio is the Roo Code integration path |

---

## 5. JSON Schema Consistency

**The schema files themselves were not supplied**, so a direct content audit is impossible. What can be assessed from code references:

| Schema | Referenced In | Expected Fields (from code) | Consistency Assessment |
|---|---|---|---|
| `schemas/expert_report.json` | `check_batch_status.py` | `expert_id`, `expert_role`, `prd_ref`, `generated_at`, `findings[]` (category, severity, description, recommendation, backlog_suggestion), `summary` | ✅ Internally consistent — all fields match the system prompts in `orchestrator_phase2.py` |
| `schemas/backlog_item.json` | `orchestrator_phase3.py` | `id`, `title`, `description`, `acceptance_criteria[]`, `source_experts[]`, `priority`, `phase` | ✅ Internally consistent — matches SP-008 output format and `apply_triage.py` field access |
| `final_backlog.json` (no schema file) | `orchestrator_phase4.py`, `triage_dashboard.py`, `apply_triage.py` | Adds `classification`, `challenge`, `human_decision` to backlog_item fields | ⚠️ No schema file for final_backlog — schema coverage is incomplete |

**Key schema concern**: The `final_backlog.json` format (output of Phase 4) has no corresponding schema file in `schemas/`. The `apply_triage.py` parser relies on `classification` and `human_decision` fields that are not schema-validated anywhere in the pipeline.

---

## 6. Prioritized Remediation

**P0 (Critical):**
- **DOC-2 v2.1 was not supplied** — the actual architectural specification is missing from this audit. The audit cannot confirm or deny compliance without it. **Obtain and supply `docs/releases/v2.1/DOC-2-v2.1-Architecture.md`** before treating any finding below as authoritative.
- **DOC-2 v2.2 is a content-free stub** — it should either contain the full architecture (by inclusion/reference) or explicitly embed the v2.1 content. A frozen architecture document that says only "no changes, see v2.1" is an audit anti-pattern.

**P1 (Important):**
- **SP-008 and SP-009 system prompts are duplicated inline** in `orchestrator_phase3.py` and `orchestrator_phase4.py` respectively, rather than loaded from the `prompts/` registry (SP-008, SP-009 files confirmed to exist per progress.md). This creates a drift risk: if prompts are updated in `prompts/`, the orchestrators will silently use stale versions.
- **No schema for `final_backlog.json`** — Phase 4 output and the triage pipeline consume this format without schema validation. Add `schemas/final_backlog.json` and wire it into `orchestrator_phase4.py` and `apply_triage.py`.
- **`memory_archive()` tool is PowerShell-only** (`powershell.exe` hardcoded) — this breaks on Linux/macOS Calypso hosts, which is the deployment target per `techContext.md` (`calypso:11434`, `calypso:8002`).

**P2 (Nice to have):**
- `check_batch_status.py` strips markdown fences with a fragile heuristic (`lines[-1] == "```"`). Should use a regex or dedicated fence-stripper shared across all three orchestrators (same pattern repeated in phases 2, 3, 4).
- `orchestrator_phase4.py` uses `claude-haiku-4-5` for Devil's Advocate but the model name format (`-4-5` suffix) is non-standard — verify this matches the actual Anthropic model ID to avoid silent API errors.
- `fastmcp_server.py` version is hardcoded as `"0.1.0"` and does not match `__init__.py`'s `__version__ = "0.1.0"` — acceptable now but should be sourced from a single location.

---

## 7. Verdict

**[MAJOR_DRIFT]** — but the drift is between the *audit request* and the *supplied documents*, not between the implementation and the architecture.

DOC-2 v2.2 contains zero architectural content (it is a one-paragraph stub deferring to v2.1), and DOC-2 v2.1 was not supplied. **It is therefore impossible to render a meaningful CONSISTENT / MINOR_DRIFT / MAJOR_DRIFT verdict on implementation compliance.** What *can* be said is that the `src/calypso/` implementation is internally coherent, all pipeline stages are implemented and cross-reference correctly, and the only verifiable gaps are the missing `final_backlog.json` schema and the inline duplication of SP-008/SP-009 prompts. To complete this audit properly, supply `docs/releases/v2.1/DOC-2-v2.1-Architecture.md`.

---

## Result: impl-memory

## 1. Executive Summary

- **DOC-2 v2.2 is a tombstone document**: it contains zero architectural content of its own, explicitly deferring 100% to DOC-2 v2.1 via a "no architectural changes" delta statement — making it impossible to audit memory-bank/ against DOC-2 v2.2 directly without the v2.1 source
- **The actual memory-bank/ structure is internally coherent**: six hot-context files are present and populated, and archive-cold/ exists with at least one file (`productContext_Master.md`)
- **A critical reference chain is broken**: DOC-2 v2.2 points to `docs/releases/v2.1/DOC-2-v2.1-Architecture.md` as the authoritative source, but that document was not provided — the audit cannot confirm whether the actual file structure matches the v2.1 specification
- **Undocumented files exist in memory-bank/**: `projectBrief.md` and `techContext.md` sit at the root of `memory-bank/` (not inside `hot-context/`), and their placement is not verifiable against any provided architectural spec
- **RULE 9 HOT/COLD boundary cannot be validated**: `.clinerules` content was not provided in the audit inputs

---

## 2. Directory Structure Comparison

| DOC-2 Describes | File/Dir Exists? | Path | Notes |
|---|---|---|---|
| `hot-context/activeContext.md` | **Yes** | `memory-bank/hot-context/activeContext.md` | Present, populated, last updated 2026-03-28T22:22:00Z |
| `hot-context/progress.md` | **Yes** | `memory-bank/hot-context/progress.md` | Present, populated, last updated 2026-03-28T20:37:00Z |
| `hot-context/productContext.md` | **Yes** | `memory-bank/hot-context/productContext.md` | Present; partially template-stub (US-001, US-002 unpopulated) |
| `hot-context/systemPatterns.md` | **Yes** | `memory-bank/hot-context/systemPatterns.md` | Present but **entirely template-stub** — all fields are placeholders |
| `hot-context/techContext.md` | **⚠️ Ambiguous** | `memory-bank/techContext.md` (root level) | File exists but at **wrong path** — root of memory-bank/, not inside hot-context/ |
| `hot-context/decisionLog.md` | **Yes** | `memory-bank/hot-context/decisionLog.md` | Present, populated with ADR-001 through ADR-006 |
| `archive-cold/` directory | **Yes** | `memory-bank/archive-cold/` | Exists |
| `archive-cold/productContext_Master.md` | **Yes** | `memory-bank/archive-cold/productContext_Master.md` | Present; body is empty (stub awaiting sprint-end archive) |
| `archive-cold/sprint-logs/` | **Cannot confirm** | `memory-bank/archive-cold/sprint-logs/` | No sprint log files provided in audit inputs; `librarian_agent.py` references this path, implying it should exist |
| `archive-cold/completed-tickets/` | **Cannot confirm** | `memory-bank/archive-cold/completed-tickets/` | Referenced in `librarian_agent.py` FILE_TYPE_MAP but not confirmed present |

> **Root cause of "Cannot confirm" rows**: DOC-2 v2.2 contains no Section 4 content — it is a pure delta document that says "see v2.1." The v2.1 document was not supplied. The table above is reconstructed from implicit evidence in the codebase (script constants, path references in `librarian_agent.py`, `fastmcp_server.py`, `apply_triage.py`).

---

## 3. Missing from DOC-2

Files/directories that **exist in memory-bank/** but are **not described in the provided DOC-2 v2.2**:

| File | Path | Severity | Analysis |
|---|---|---|---|
| `projectBrief.md` | `memory-bank/projectBrief.md` | **P1** | Root-level file, entirely template-stub. Not referenced in any DOC-2 content. Placement outside `hot-context/` suggests it predates the Hot/Cold restructure (PHASE-A) or was intentionally kept at root — but no architectural rationale is documented. |
| `techContext.md` | `memory-bank/techContext.md` | **P0** | This file is **substantively populated** (LLM backend config, fallback logic, tech stack) but lives at the **wrong level**. The Calypso scripts reference `memory-bank/hot-context/techContext.md` implicitly (via `DEFAULT_SYSTEMPATTERNS` and `DEFAULT_PRODUCTCONTEXT` patterns), and the Hot/Cold architecture implies all active context belongs in `hot-context/`. This is a **structural misplacement**. |

---

## 4. Missing from Implementation

Content that **DOC-2 describes** (or that the architecture implies) but does **not exist** in the confirmed memory-bank/ inventory:

| Expected Item | Expected Path | Severity | Analysis |
|---|---|---|---|
| `archive-cold/sprint-logs/` directory | `memory-bank/archive-cold/sprint-logs/` | **P1** | `librarian_agent.py` hardcodes `FILE_TYPE_MAP = {"sprint-logs": "sprint_log", ...}` and `memory-archive.ps1` is described as appending to `archive-cold/sprint-logs/sprint-NNN.md`. Directory existence unconfirmed. |
| `archive-cold/completed-tickets/` directory | `memory-bank/archive-cold/completed-tickets/` | **P1** | Same source: `FILE_TYPE_MAP` in `librarian_agent.py` maps `"completed-tickets"` to `"ticket"` type. Directory existence unconfirmed. |
| DOC-2 v2.1 Architecture (the actual spec) | `docs/releases/v2.1/DOC-2-v2.1-Architecture.md` | **P0** | DOC-2 v2.2 explicitly states this is the authoritative architecture document. Without it, no formal Section 4 specification exists to audit against. The entire audit is operating on inferred architecture from code artifacts. |
| `hot-context/techContext.md` | `memory-bank/hot-context/techContext.md` | **P0** | The populated `techContext.md` exists at root level (`memory-bank/techContext.md`) rather than inside `hot-context/`. The hot-context directory is missing this file at the correct path. |

---

## 5. Hot/Cold Boundary

**Assessment: CANNOT FULLY VALIDATE — `.clinerules` not provided**

What can be determined from available evidence:

| Dimension | Finding |
|---|---|
| **RULE 9 in .clinerules** | Not provided in audit inputs — cannot confirm rule text or HOT/COLD boundary definition |
| **Architectural intent** | Clearly established: `hot-context/` = active working memory (read/write by agents); `archive-cold/` = read-only cold storage (access via `memory:query` MCP tool only) |
| **Cold archive enforcement** | `productContext_Master.md` header correctly states `READ-ONLY for agents — access via memory:query MCP tool only` — boundary is documented at file level |
| **Hot context write paths** | `apply_triage.py` correctly writes to `memory-bank/hot-context/systemPatterns.md` and `memory-bank/hot-context/productContext.md` — consistent with HOT boundary |
| **`memory_archive()` tool** | `fastmcp_server.py` correctly delegates to `scripts/memory-archive.ps1` for hot→cold rotation — boundary transition is tool-mediated, not direct agent write |
| **Structural violation** | `memory-bank/techContext.md` at root level is **outside both HOT and COLD zones** — it is in a boundary-undefined location, which is an implicit RULE 9 violation regardless of rule text |
| **`memory-bank/projectBrief.md`** | Same issue — root-level placement is architecturally undefined |

**Verdict on HOT/COLD boundary**: The *intent* is correctly implemented in the Calypso tooling. The *structural violation* is the two root-level files (`techContext.md`, `projectBrief.md`) that belong in `hot-context/` but were never migrated during PHASE-A.

---

## 6. Prioritized Remediation

### P0 — Critical

| # | Issue | Action |
|---|---|---|
| P0-1 | **`memory-bank/techContext.md` at wrong path** — substantively populated file is outside `hot-context/`, breaking the HOT/COLD boundary and making it invisible to agents that read `hot-context/` | Move to `memory-bank/hot-context/techContext.md`; update any hardcoded path references; git commit |
| P0-2 | **DOC-2 v2.2 has no Section 4** — the document is a tombstone that defers to v2.1, but v2.1 was not provided for this audit | Retrieve `docs/releases/v2.1/DOC-2-v2.1-Architecture.md` and re-run this audit against the actual specification |

### P1 — Important

| # | Issue | Action |
|---|---|---|
| P1-1 | **`memory-bank/projectBrief.md` at root level** — template-stub file outside both HOT and COLD zones; either migrate to `hot-context/` or document why it lives at root | Decide: move to `hot-context/projectBrief.md` OR document root-level placement as intentional in DOC-2 v2.3 |
| P1-2 | **`archive-cold/sprint-logs/` existence unconfirmed** — `memory-archive.ps1` and `librarian_agent.py` depend on this directory; if absent, first sprint archive will fail silently | Confirm directory exists (with `.gitkeep` if empty); create if missing |
| P1-3 | **`archive-cold/completed-tickets/` existence unconfirmed** — same dependency pattern as sprint-logs | Same remediation as P1-2 |
| P1-4 | **`hot-context/systemPatterns.md` is entirely a template stub** — all fields are placeholders (`[Paste your project directory tree here]`, `[convention]`, etc.) despite the project being at v2.2 | Populate with actual system patterns; `apply_triage.py` will append to it but the base content is misleading |

### P2 — Nice to Have

| # | Issue | Action |
|---|---|---|
| P2-1 | **`hot-context/productContext.md` has unpopulated template stubs** — US-001 and US-002 are blank templates alongside the real US-003 | Remove or fill blank US-001/US-002 stubs to avoid agent confusion |
| P2-2 | **`decisionLog.md` has mixed CRLF/LF and encoding issues** — ADR-006 entry contains raw `\r\n` escape sequences in the stored text (visible as literal `\r\n` in the file) | Normalize line endings: `git config core.autocrlf false` + re-save file |
| P2-3 | **`archive-cold/productContext_Master.md` body is empty** — the file exists but contains only the header comment and an empty sprint entries placeholder | No immediate action needed (correct state for a project that hasn't completed a sprint archive yet); add a note in DOC-2 v2.3 that this is expected initial state |

---

## 7. Verdict

**[MAJOR_DRIFT]**

DOC-2 v2.2 is architecturally vacuous — it contains no Section 4 content whatsoever, making a formal compliance audit impossible without retrieving the v2.1 document it defers to. Beyond the documentation gap, the implementation has a confirmed structural violation: `techContext.md` (a substantively populated, actively-used file) is misplaced at `memory-bank/` root rather than `memory-bank/hot-context/`, placing it outside the defined HOT/COLD boundary zones entirely. Two additional root-level files (`projectBrief.md`) compound this boundary ambiguity, and at least two expected cold-archive subdirectories (`sprint-logs/`, `completed-tickets/`) could not be confirmed as existing.

---

