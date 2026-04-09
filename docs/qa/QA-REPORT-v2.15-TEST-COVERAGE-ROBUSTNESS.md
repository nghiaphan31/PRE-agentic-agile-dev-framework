# QA Report — v2.15 Test Coverage & Robustness Review

**Date:** 2026-04-09  
**Reviewer:** QA Engineer  
**Mode:** qa-engineer  
**Scope:** Test coverage, script robustness, automation reliability, QA report history  
**Sources:** `src/calypso/tests/`, `scripts/`, `.github/workflows/`, `.githooks/pre-receive`, prior QA reports

---

## Executive Summary

| Domain | Status | Critical | Major | Minor |
|--------|--------|----------|-------|-------|
| Test Coverage | ❌ CRITICAL GAPS | 4 | 3 | 4 |
| Script Robustness | ⚠️ PARTIAL | 1 | 2 | 3 |
| Automation Reliability | ⚠️ PARTIAL | 1 | 3 | 2 |
| QA Report History | ✅ RESOLVED | 0 | 0 | 0 |
| **TOTAL** | | **6** | **8** | **9** |

---

## Part 1: Test Coverage Review

### 1.1 Existing Test Files

| File | Tests | Coverage Area |
|------|-------|---------------|
| `src/calypso/tests/test_ideation_pipeline.py` | 18 test methods | IntakeAgent, SyncDetector, BranchTracker, ExecutionTracker, Pipeline integration |
| `src/calypso/tests/test_orchestrator.py` | 11 test methods | orchestrator_phase2/3/4 (batch request building, synthesis, validation, challenge_item) |
| `src/calypso/tests/test_triage.py` | 11 test methods | triage_dashboard, apply_triage (checkbox parsing, formatting, dry-run) |

### Finding TC-001 — NO Tests for Branch Naming Enforcement [CRITICAL]

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **Rule Reference** | RULE 10.1 branch table, ADR-006-AMEND-001 |

**Description:**

There are **zero tests** for branch naming enforcement. No tests verify:
- Correct branch type parsing (`feature/`, `lab/`, `bugfix/`, `hotfix/`, `stabilization/`)
- Timebox-first pattern validation (`feature/{Timebox}/{IDEA-NNN}-{slug}`)
- Forbidden direct commits to `main`, `develop`, or `stabilization/*`
- `develop-vX.Y` → `stabilization/vX.Y` transition (ADR-006-AMEND-001)

`BranchTracker.from_branch_name()` exists (tested in `test_branch_type_parsing`) but the enforcement logic (what makes a branch name valid vs invalid per RULE 10.1) is not tested.

**Suggested Fix:**

Add `test_branch_tracker.py` with:
```python
def test_branch_type_parsing_feature_with_timebox():
    """Feature branches must use timebox-first pattern."""
    branch = Branch.from_branch_name("feature/2026-Q2/IDEA-042-auth")
    assert branch.branch_type == BranchType.FEATURE
    assert branch.idea_id == "IDEA-042"

def test_invalid_feature_branch_no_timebox():
    """Feature branch without timebox should be flagged."""
    # Per TECH-005 hybrid naming, old pattern should be warned
    with pytest.warns(UserWarning):
        branch = Branch.from_branch_name("feature/IDEA-042-auth")

def test_stabilization_branch_parsing():
    """stabilization/vX.Y should be recognized."""
    branch = Branch.from_branch_name("stabilization/v2.16")
    assert branch.branch_type == BranchType.STABILIZATION

def test_hotfix_ticket_pattern():
    """hotfix/T-NNN-slug pattern per RULE 10.1."""
    branch = Branch.from_branch_name("hotfix/T-202-DB-Leak")
    assert branch.branch_type == BranchType.HOTFIX
    assert branch.ticket_id == "T-202"
```

---

### Finding TC-002 — NO Tests for DOC-CURRENT Pointer Updates [CRITICAL]

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **Rule Reference** | RULE 12.7 (R-CANON-7), QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md F-01 |

**Description:**

There are **zero tests** for DOC-CURRENT pointer consistency. No tests verify:
- All three cumulative DOC-*-CURRENT.md (DOC-1, DOC-2, DOC-4) point to the **same** release version
- Release-specific DOC-*-CURRENT.md (DOC-3, DOC-5) point to their respective correct versions
- Pointers are updated atomically during release

QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md documents that DOC-1/2/4-CURRENT point to v2.13 while DOC-3/5-CURRENT point to v2.15 — a live inconsistency that would be caught by such tests.

**Suggested Fix:**

Add `test_doc_pointers.py`:
```python
def test_cumulative_doc_pointers_all_match():
    """DOC-1, DOC-2, DOC-4 must all point to same release."""
    doc1 = read_pointer("docs/DOC-1-CURRENT.md")
    doc2 = read_pointer("docs/DOC-2-CURRENT.md")
    doc4 = read_pointer("docs/DOC-4-CURRENT.md")
    assert doc1.version == doc2.version == doc4.version

def test_release_specific_doc_pointers_exist():
    """DOC-3 and DOC-5 CURRENT pointers must exist."""
    assert Path("docs/DOC-3-CURRENT.md").exists()
    assert Path("docs/DOC-5-CURRENT.md").exists()

def test_pointer_target_file_exists():
    """Each DOC-CURRENT.md must point to a file that exists."""
    for doc_type in ["DOC-1", "DOC-2", "DOC-3", "DOC-4", "DOC-5"]:
        pointer = read_pointer(f"docs/{doc_type}-CURRENT.md")
        assert Path(pointer.file_path).exists(), f"{doc_type} target missing"
```

---

### Finding TC-003 — NO Tests for SP-002 Synchronization [CRITICAL]

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **Rule Reference** | RULE 6.2, RULE 18 (SP-002 sync protocol) |

**Description:**

There are **zero tests** that verify `.clinerules` and `prompts/SP-002-clinerules-global.md` are byte-for-byte identical. No tests cover:
- The `rebuild_sp002.py --check` exit code behavior
- The SP-002 version increment protocol
- The `check-prompts-sync.ps1` PowerShell script

`scripts/rebuild_sp002.py` is well-implemented (proper normalization, exit codes, footer extraction) but has no test coverage. If the script's logic changes, there is no regression detection.

**Suggested Fix:**

Add `test_sp002_sync.py`:
```python
def test_rebuild_sp002_check_exit_code():
    """rebuild_sp002.py --check should exit 0 when synced."""
    result = subprocess.run(
        ["python", "scripts/rebuild_sp002.py", "--check"],
        capture_output=True
    )
    assert result.returncode == 0

def test_sp002_and_clinerules_identical():
    """SP-002 code block must match .clinerules byte-for-byte."""
    # Use the same normalization as rebuild_sp002.py
    clinerules = Path(".clinerules").read_text()
    sp002_block = extract_sp002_code_block()
    assert normalize(clinerules) == normalize(sp002_block)

def test_sp002_footer_contains_deployment_notes():
    """SP-002 must have ## Deployment Notes section."""
    content = Path("prompts/SP-002-clinerules-global.md").read_text()
    assert "## Deployment Notes" in content
```

---

### Finding TC-004 — NO Tests for Handoff Protocol [CRITICAL]

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **Rule Reference** | RULE 16 (Mandatory Handoff Protocol) |

**Description:**

There are **zero tests** for the handoff protocol. No tests verify:
- `handoff-state.md` schema compliance (RULE 16.1)
- Required fields: `handoff_id`, `from_agent.mode`, `task_completion.status`, `next_action.recommendation`
- Orchestrator acknowledgment flow (`acknowledged: true` set by Orchestrator)
- Mode switching behavior (`switch_mode("orchestrator")`)

QA-REPORT-v2.15-HUMAN-JOURNEY-GITFLOW.md Finding MS-003 confirms: "There is no GitHub Actions workflow that validates `handoff-state.md` schema" — and there are no unit tests either.

**Suggested Fix:**

Add `test_handoff_protocol.py`:
```python
def test_handoff_state_schema_required_fields():
    """RULE 16.1 handoff schema must have all required fields."""
    handoff = load_handoff_state()
    required = ["handoff_id", "from_agent", "task_completion", "next_action"]
    for field in required:
        assert field in handoff, f"Missing required field: {field}"

def test_handoff_id_format():
    """handoff_id must follow H-{timestamp}-{sequence} format."""
    handoff = load_handoff_state()
    assert re.match(r"^H-\d+-\d+$", handoff["handoff_id"])

def test_next_action_recommendation_valid():
    """next_action.recommendation must be valid value."""
    handoff = load_handoff_state()
    valid = ["continue", "handoff", "escalate", "complete"]
    assert handoff["next_action"]["recommendation"] in valid

def test_orchestrator_receipt_schema():
    """Orchestrator receipt must have received_at and acknowledged."""
    handoff = load_handoff_state()
    if "orchestrator_receipt" in handoff:
        assert "received_at" in handoff["orchestrator_receipt"]
        assert "acknowledged" in handoff["orchestrator_receipt"]
```

---

### Finding TC-005 — NO Tests for Mode Switching [CRITICAL]

| Property | Value |
|---|---|
| **Severity** | CRITICAL |
| **Rule Reference** | RULE 16.5, TECH-006 (Dummy Task Mode Switch) |

**Description:**

There are **zero tests** for mode switching functionality. No tests cover:
- `switch_mode()` tool invocation behavior
- Autonomous mode switching (no human approval required per TECH-006)
- Mode validation (only valid mode slugs accepted)
- Default mode selection logic

The `.roomodes` file defines 4 Scrum modes but RULE 16.5 references "Orchestrator" as a built-in mode. There is no test to verify this distinction or the auto-switch instruction's scope.

**Suggested Fix:**

Add `test_mode_switching.py` (requires mocking the Roo Code environment):
```python
def test_valid_mode_slugs_accepted():
    """switch_mode should accept valid mode slugs."""
    valid_modes = ["orchestrator", "product-owner", "scrum-master", "developer", "qa-engineer"]
    for mode in valid_modes:
        result = switch_mode(mode)
        assert result.success, f"Failed to switch to {mode}"

def test_orchestrator_is_builtin_not_in_roomodes():
    """Orchestrator is built-in per RULE 16.5, not in .roomodes."""
    roomodes = json.loads(Path(".roomodes").read_text())
    mode_slugs = [m["slug"] for m in roomodes.get("customModes", [])]
    assert "orchestrator" not in mode_slugs

def test_invalid_mode_rejected():
    """switch_mode should reject invalid mode slugs."""
    with pytest.raises(ValueError):
        switch_mode("nonexistent-mode")
```

---

### Finding TC-006 — Existing Tests Are Unit-Only, No Integration Tests [MAJOR]

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Files** | `src/calypso/tests/test_ideation_pipeline.py`, `test_orchestrator.py`, `test_triage.py` |

**Description:**

All existing tests are **unit tests** that mock dependencies:
- `IntakeAgent` tests use no mocks but don't test file I/O
- `orchestrator_phase4` tests mock `anthropic.Anthropic` class
- `apply_triage` tests use `tempfile.TemporaryDirectory` but don't test actual file paths

There are **no integration tests** that:
- Test the full Calypso pipeline end-to-end (intake → refinement → triage → execution)
- Verify file writes to actual `docs/ideas/` and `memory-bank/` directories
- Test the Git integration (branch scanning, tag detection) against a real `.git` repository
- Verify the `checkpoint_heartbeat.py --log-conversation` flow against `docs/conversations/`

**Suggested Fix:**

Add `tests/integration/` directory with integration tests that:
- Use a temporary Git repository (` tempfile.TemporaryDirectory` + `git init`)
- Create actual IDEA files and verify they appear in `IDEAS-BACKLOG.md`
- Test branch detection against the temp repo

---

### Finding TC-007 — Test Coverage for Calypso Components is Incomplete [MAJOR]

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **Untested Files** | `intake_agent.py`, `sync_detector.py`, `branch_tracker.py`, `execution_tracker.py`, `triage_dashboard.py`, `apply_triage.py` |

**Description:**

Only **partial coverage** exists for Calypso components:

| File | Test File | Tested Methods |
|------|-----------|---------------|
| `intake_agent.py` | test_ideation_pipeline.py | `score()`, `determine_mode()`, `process_intake()`, `generate_idea_file()` |
| `sync_detector.py` | test_ideation_pipeline.py | `detect_sync()` (partial), `load_backlog_entries()` |
| `branch_tracker.py` | test_ideation_pipeline.py | `scan()`, `get_active_branches()`, `from_branch_name()` |
| `execution_tracker.py` | test_ideation_pipeline.py | `generate_draft()`, `_parse_ideas_backlog()` |
| `triage_dashboard.py` | test_triage.py | `generate_dashboard()`, `load_final_backlog()` |
| `apply_triage.py` | test_triage.py | `parse_checkbox_decisions()`, `format_item_for_systempatterns()`, `format_item_for_productcontext()` |

**Untested methods** include:
- `IntakeAgent.classify_idea()` — not tested directly
- `SyncDetector.detect_sync()` — returns a report but report structure not validated
- `BranchTracker.get_report()` — tested for string format but not content correctness
- `ExecutionTracker._parse_ideas_backlog()` — tested it returns a list but not content
- `apply_triage.apply_decisions()` — only dry-run tested, actual file writing not tested

**Suggested Fix:**

Add targeted tests for untested methods, particularly `apply_decisions()` with real file writes (non-dry-run mode in a temp directory).

---

### Finding TC-008 — No Tests for `scripts/detect-merged-features.py` [MAJOR]

| Property | Value |
|---|---|
| **Severity** | MAJOR |
| **File** | `scripts/detect-merged-features.py` |

**Description:**

`detect-merged-features.py` is a complex script with:
- Tag parsing (`get_last_release_tag()`, `parse_version_from_tag()`)
- Git log parsing (`get_merged_features_since_tag()`)
- Feature detection with deduplication
- Release scope auto-creation (`create_next_release_scope()`)
- CLI argument parsing

There are **zero tests** for this script. If the Git log parsing logic changes, there is no regression detection.

**Suggested Fix:**

Add `tests/test_detect_merged_features.py`:
```python
def test_parse_version_from_tag():
    """Parse major/minor from tag like v2.11.0."""
    assert parse_version_from_tag("v2.11.0") == (2, 11)
    assert parse_version_from_tag("v1.0.0") == (1, 0)

def test_extract_identifiers_idea():
    """Extract IDEA-NNN from branch name."""
    idea_id, tech_id, feature_id = extract_identifiers("feature/2026-Q2/IDEA-042-auth")
    assert idea_id == "IDEA-042"
    assert feature_id == "IDEA-042"

def test_extract_identifiers_tech():
    """Extract TECH-NNN from branch name."""
    idea_id, tech_id, feature_id = extract_identifiers("lab/2026-Q2/TECH-002-auto-detect")
    assert tech_id == "TECH-002"
    assert feature_id == "TECH-002"

def test_is_tracked_branch():
    """Should not track main, develop, master."""
    assert is_tracked_branch("develop") == False
    assert is_tracked_branch("main") == False
    assert is_tracked_branch("feature/IDEA-042") == True
```

---

### Finding TC-009 — No Tests for `scripts/audit_cumulative_docs.py` [MINOR]

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `scripts/audit_cumulative_docs.py` |

**Description:**

`audit_cumulative_docs.py` has:
- Line count minimum enforcement (DOC-1: 500, DOC-2: 500, DOC-4: 300, DOC-3: 100, DOC-5: 50)
- Section extraction (`extract_sections()`, `extract_toc_entries()`)
- Release-specific vs cumulative distinction

No tests verify the minimum line count logic or the section extraction accuracy.

**Suggested Fix:**

Add `tests/test_audit_cumulative_docs.py`:
```python
def test_min_lines_cumulative():
    """Cumulative doc minimums from RULE 12.1."""
    assert MIN_LINES["DOC-1"] == 500
    assert MIN_LINES["DOC-2"] == 500
    assert MIN_LINES["DOC-4"] == 300

def test_min_lines_release_specific():
    """Release-specific doc minimums from RULE 12.1."""
    assert MIN_LINES["DOC-3"] == 100
    assert MIN_LINES["DOC-5"] == 50
```

---

### Finding TC-010 — No Tests for `scripts/checkpoint_heartbeat.py` [MINOR]

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `scripts/checkpoint_heartbeat.py` |

**Description:**

`checkpoint_heartbeat.py` implements:
- Git state capture (`get_git_state()`)
- Checkpoint metadata parsing (`read_checkpoint_metadata()`)
- Slug generation (`generate_slug()`)
- Conversation logging (`log_conversation()`)

No tests cover any of these functions. The conversation logging function writes to `docs/conversations/` — this could be tested with a temp directory.

**Suggested Fix:**

Add `tests/test_checkpoint_heartbeat.py`:
```python
def test_generate_slug():
    """Slug generation from session_id."""
    assert generate_slug("s2026-04-09-code-001") == "2026-04-09-code-001"
    assert generate_slug("s2026-04-09-orchestrator-042") == "2026-04-09-orchestrator-042"

def test_read_checkpoint_metadata_missing_file():
    """Should return empty dict for missing checkpoint."""
    with pytest.raises(FileNotFoundError):
        read_checkpoint_metadata(Path("/nonexistent/checkpoint.md"))
```

---

### Finding TC-011 — No Tests for `scripts/check-prompts-sync.ps1` [MINOR]

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `scripts/check-prompts-sync.ps1` |

**Description:**

`check-prompts-sync.ps1` is a PowerShell script with complex logic:
- SP content extraction (`Extract-PromptContent`)
- Text normalization (CRLF→LF, trim)
- Diff reporting (`Show-Diff`)
- Per-SP validation (SP-001 through SP-006, SP-007 is WARN-only)

There are no PowerShell tests and no Python wrapper tests.

**Suggested Fix:**

Either add Pester tests (PowerShell testing framework) or create a Python wrapper that tests the PowerShell script's output behavior.

---

### Finding TC-012 — No Tests for `.githooks/pre-receive` [MINOR]

| Property | Value |
|---|---|
| **Severity** | MINOR |
| **File** | `.githooks/pre-receive` |

**Description:**

The pre-receive hook implements:
- Canonical doc modification detection
- Feature branch enforcement (`check_feature_branch()`)
- Line count minimums per doc type
- Cumulative vs release-specific doc distinction

No tests verify the hook's behavior against actual Git commits. Testing a pre-receive hook requires a real Git repository with commits.

**Suggested Fix:**

Add shell-based tests using a temp Git repo:
```bash
#!/bin/bash
# tests/githooks/test-pre-receive.sh
git init temp-test-repo
cd temp-test-repo
# ... set up hook ...
# ... create commits and verify hook behavior ...
```

---

## Part 2: Script Robustness Review

### 2.1 `scripts/checkpoint_heartbeat.py`

| Property | Value |
|---|---|
| **Lines** | 487 |
| **Exit codes** | 0 (success), 1 (error) |
| **Dependencies** | Standard library only |

**Robustness Assessment: ⚠️ PARTIAL**

**Strengths:**
- Uses `subprocess.DEVNULL` to suppress git errors (lines 45-76)
- Has `--check` mode for validation
- `log_conversation()` uses timestamp for uniqueness (line 335)
- Updates README.md with new conversation entry

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| CB-001 | `write_heartbeat()` has a bug in the heartbeat log append logic (lines 146-155) — it reassigns `lines` to `content.split('\n')` but then tries to use the popped `lines` variable outside the loop | MAJOR | Lines 146-155 |
| CB-002 | `log_conversation()` writes conversation file but does NOT capture the actual conversation content — it writes a template with placeholder "<!-- Add conversation summary -->" | MAJOR | Lines 346-377 |
| CB-003 | No validation that `CONVERSATIONS_DIR` exists before writing (mkdir is called but only if `parents=True`) | MINOR | Line 344 |

**CB-001 Detail:**

```python
# Line 146-155 - BUG
for line in lines:
    new_lines.append(line)
    if line.strip() == '| Timestamp | Event |':
        # Found header, skip to next and add entries after
        while new_lines and not new_lines[-1].startswith('| '):
            new_lines.append(lines.pop(0) if lines else '')  # Bug: pops from lines but assigns to new_lines
        break
content = '\n'.join(lines) + heartbeat_entry  # Bug: uses original lines variable
```

The bug: after the `for` loop, `lines` still refers to the original array. But inside the `while`, `lines.pop(0)` removes from `lines`, and the result is appended to `new_lines`. Then `content = '\n'.join(lines)` uses the (now modified) `lines` which has had elements popped from it. This would drop content from the file.

**CB-002 Detail:**

The `log_conversation()` function creates a conversation file with a template placeholder:
```
## Notes

<!-- Add conversation summary, key decisions, and outcomes below -->
```

Per RULE 8.3, the purpose is to save AI conversation output. But the function does NOT capture any actual conversation content — it only writes a template. The actual conversation capture would need to be done by the agent manually.

**Suggested Fixes:**

1. Fix the heartbeat append logic to properly reconstruct content
2. Add a parameter to `log_conversation()` that accepts actual conversation text
3. Add a test that calls `log_conversation()` in a temp directory and verifies the output

---

### 2.2 `scripts/rebuild_sp002.py`

| Property | Value |
|---|---|
| **Lines** | 131 |
| **Exit codes** | 0 (synced), 1 (mismatch), 2 (error) |
| **Dependencies** | Standard library only |

**Robustness Assessment: ✅ GOOD**

**Strengths:**
- Clean, well-documented with docstrings
- Proper error handling with `sys.exit(2)` for file errors
- Verifies after rebuild (`--check` after `--check` in `rebuild()`)
- Shows first difference position on mismatch (lines 91-95)
- Normalizes CRLF→LF and trailing whitespace for comparison
- Extracts header, footer, and code block correctly

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| RB-001 | No tests for the script itself (TC-003) | CRITICAL | N/A |
| RB-002 | The `extract_footer()` function uses `content.rfind(marker)` which could fail if "## Deployment Notes" appears multiple times | MINOR | Line 55 |
| RB-003 | No `--dry-run` mode — rebuilds SP-002 even when checking | MINOR | Line 99 |

---

### 2.3 `scripts/check-prompts-sync.ps1`

| Property | Value |
|---|---|
| **Lines** | 172 |
| **Exit codes** | 0 (success), 1 (desync detected) |
| **Dependencies** | PowerShell 5.1+ |

**Robustness Assessment: ⚠️ PARTIAL**

**Strengths:**
- Normalizes text (CRLF→LF, trim)
- Extracts code blocks with regex (`(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n````)
- Shows first 20 diff lines on failure
- Handles SP-007 as manual (WARN, not FAIL)
- Returns proper exit codes

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| CPS-001 | The regex for extracting code blocks uses `(?:markdown|python|)` which means empty string is also valid — could match something unexpected | MINOR | Line 34 |
| CPS-002 | No `--verbose` flag implementation despite being declared in `param()` | MINOR | Line 14 |
| CPS-003 | The Modelfile extraction regex `'SYSTEM\s+"""(.*?)"""'` assumes triple-double-quote format — may not match other formats | MINOR | Line 77 |
| CPS-004 | Does not handle BOM (Byte Order Mark) — if Modelfile or .clinerules has BOM, comparison could fail silently | MINOR | N/A |

---

### 2.4 `scripts/detect-merged-features.py`

| Property | Value |
|---|---|
| **Lines** | 564 |
| **Exit codes** | 0 (success), 1 (error) |
| **Dependencies** | Standard library only |

**Robustness Assessment: ⚠️ PARTIAL**

**Strengths:**
- Well-structured with dataclasses for `MergedFeature`
- Proper error handling in subprocess calls
- `--dry-run` mode available
- `--json` output option for machine consumption
- Tag-creation mode with auto-scope creation
- Deduplicates features by `feature_id`

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| DMF-001 | No tests (TC-008) | CRITICAL | N/A |
| DMF-002 | `create_next_release_scope()` hardcodes the skeleton DOC-3 content — if RULE 12 changes (e.g., new required sections), this skeleton becomes stale | MAJOR | Lines 329-376 |
| DMF-003 | The `get_merged_features_since_tag()` uses `--first-parent --all` which may miss merges from deleted branches | MINOR | Line 138 |
| DMF-004 | `add_feature_to_scope()` inserts at first checkbox line — could insert in wrong place if there are multiple checkbox lists in the file | MINOR | Lines 243-263 |
| DMF-005 | The release scope detection logic (`get_next_release_scope()`) looks for the highest version directory — but this could be wrong if v2.15 exists but is not the "current draft" | MINOR | Lines 189-217 |

---

### 2.5 `scripts/audit_cumulative_docs.py`

| Property | Value |
|---|---|
| **Lines** | 285 |
| **Exit codes** | 0 (pass), 1 (fail) |
| **Dependencies** | Standard library only |

**Robustness Assessment: ⚠️ PARTIAL**

**Strengths:**
- Minimum line count enforcement per RULE 12.1
- Properly distinguishes cumulative vs release-specific docs
- Section extraction for TOC validation
- Exits with error code on failure

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| ACD-001 | `RELEASES = ["v2.10", "v2.11"]` is hardcoded — won't auto-detect v2.15 | MAJOR | Line 31 |
| ACD-002 | The `extract_toc_entries()` function has a bug: it sets `in_toc = True` on any `## Table of Contents` match but only breaks on `##+` (2+ hashes) — a `##` header in the TOC itself would break parsing | MINOR | Lines 72-83 |
| ACD-003 | No `--verbose` flag | MINOR | N/A |
| ACD-004 | The script checks minimum line counts but does NOT verify that content is actually cumulative (i.e., that v2.15 includes v2.14 content) | MINOR | Lines 111-142 |

**ACD-001 Detail:**

Per QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md, v2.15 has been released but `audit_cumulative_docs.py` only checks v2.10 and v2.11. This means the script would not detect the missing v2.15 cumulative docs.

---

## Part 3: Automation Robustness Review

### 3.1 GitHub Actions Workflows

#### `release-gate.yml` — Assessment: ⚠️ PARTIAL

**P0 Blocker Checks (✅ Correct):**
- P0-1: SP-002 sync (byte-for-byte comparison with `diff -q`)
- P0-2: Canonical docs minimum line counts (cumulative: 500/500/300, release-specific: 100/50)
- P0-3: Cumulative DOC pointer consistency (DOC-1, DOC-2, DOC-4 must all match)
- P0-4: Cumulative flag verification (`cumulative: true` in front matter)
- P0-5: Release-specific flag verification

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| RG-001 | Workflow triggers on `develop-v*` instead of `stabilization/v*` — will NOT run on next release branch | CRITICAL | Line 6 |
| RG-002 | Version extraction hardcodes `develop-v` prefix — will produce wrong version string on `stabilization/v*` | MAJOR | Line 41 |
| RG-003 | P0-1 SP-002 sync uses `sed '1s/^\xEF\xBB\xBF//'` for BOM removal — this only works for UTF-8 BOM at start of file, not for BOM in SP-002 mid-content | MINOR | Line 71 |
| RG-004 | Missing fast-forward develop step in summary (line 247 says "Merge to main (fast-forward)" but RULE 10.5 requires also fast-forwarding develop to main) | MINOR | Lines 244-248 |

---

#### `canonical-docs-check.yml` — Assessment: ⚠️ PARTIAL

**Correct Elements:**
- Cumulative vs release-specific doc distinction (lines 46-50 for cumulative, lines 86-89 for release-specific)
- Pointer consistency check
- Line count minimums (correctly differentiated: 500/500/300 for cumulative, 100/50 for release-specific)
- Cumulative flag verification

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| CDC-001 | Triggers on `develop-v*` instead of `stabilization/v*` — will not run on release preparation branches | CRITICAL | Line 11 |
| CDC-002 | Triggers on `push` to `main` — per RULE 10.2, no commits should be made directly to `main` (frozen). This means the check would never catch a direct `main` commit because such a commit should not exist | MINOR | Line 12 |

---

#### `release-consistency-check.yml` — Assessment: ⚠️ PARTIAL

**Correct Elements:**
- RELEASE.md schema validation ( CHECK 1-2)
- Git tag consistency (CHECK 3)
- DOC-5-CURRENT.md consistency (CHECK 4)
- Frozen docs existence (CHECK 5)
- EXECUTION-TRACKER existence (CHECK 7)

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| RCC-001 | PR trigger uses `develop-v*` instead of `stabilization/v*` — will not run on release preparation PRs | CRITICAL | Line 5 |
| RCC-002 | CHECK 6 (Draft version branch existence) does NOT verify branch naming — could accept a `develop-v*` branch which is now deprecated | MAJOR | Lines 215-236 |
| RCC-003 | CHECK 5 parses the Released Versions table but the parsing logic (lines 182-205) is fragile — relies on specific table format with `|` separators | MINOR | Lines 182-205 |

---

#### `detect-merged-features.yml` — Assessment: ✅ GOOD

**Correct Elements:**
- Triggers on PR close to `develop`, push to `develop`, schedule (daily), and tag creation
- Uses `--tag-creation` mode when triggered by tag creation
- Installs dependencies with `pip install -r requirements.txt`
- Uses `peter-evans/create-pull-request` for automated PR creation

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| DMF-WF-001 | Triggers on `develop` but not on `stabilization/v*` — feature detection after branch creation from stabilization would be missed | MINOR | Line 5 |
| DMF-WF-002 | Schedule cron runs daily at 02:00 UTC — if a release is in progress, this could create a PR mid-release | MINOR | Line 9 |

---

### 3.2 Pre-Receive Hook

**`.githooks/pre-receive` — Assessment: ⚠️ PARTIAL**

**Correct Elements:**
- Canonical doc modification detection (CANON_PATTERNS)
- Feature branch enforcement for canonical doc changes
- Cumulative flag parsing from front matter
- Release-specific minimum thresholds (DOC-3: 100, DOC-5: 50) — correctly applied in `check_doc_format()` lines 115-127

**Issues:**

| ID | Issue | Severity | Location |
|----|-------|----------|----------|
| PRH-001 | `MIN_LINES_CUMULATIVE` table incorrectly includes DOC-3 and DOC-5 with 100/50 values — but this table is used for cumulative docs only, while the case statement below (lines 99-106) also incorrectly applies 300/200 to DOC-3/DOC-5 for cumulative docs | MAJOR | Lines 19-25, 99-106 |
| PRH-002 | Branch pattern check only recognizes `feature/` and `fix/` — missing `lab/`, `bugfix/`, `stabilization/`, `hotfix/` | MAJOR | Line 58 |
| PRH-003 | No check for direct commits to `main`, `develop`, or `stabilization/*` | MAJOR | Line 56-72 |
| PRH-004 | No `--no-ff` merge enforcement — RULE 10.3 requires `--no-ff` but the hook doesn't verify merge commit structure | MINOR | N/A |
| PRH-005 | The hook uses `git branch --contains` which may not work correctly for merge commits across all Git versions | MINOR | Line 58 |

**PRH-001 Detail:**

The hook declares `MIN_LINES_CUMULATIVE` with DOC-3=100 and DOC-5=50 (lines 22-23), but then uses a `case` statement that applies cumulative thresholds (300 and 200) to DOC-3 and DOC-5 when `cumulative_flag == "true"` (lines 102-104):

```bash
# Lines 99-106 - BUG
case "$doc_name" in
  DOC-1) min_lines=500 ;;
  DOC-2) min_lines=500 ;;
  DOC-3) min_lines=300 ;;  # Wrong for cumulative=true, should be 100
  DOC-4) min_lines=300 ;;
  DOC-5) min_lines=200 ;;  # Wrong for cumulative=true, should be 50
```

The initial `MIN_LINES_CUMULATIVE` associative array has the correct values (100/50) but is never actually used — only the `case` statement is used for cumulative docs. This means the pre-receive hook would incorrectly reject a cumulative DOC-3 with 150 lines (valid per RULE 12.1) as being "delta-based".

---

## Part 4: QA Report History — Previous Issues Resolution

### 4.1 QA Reports Reviewed

| Report | Date | Finding Count | Status |
|--------|------|---------------|--------|
| `QA-REPORT-v2.13-revalidation-2026-04-08.md` | 2026-04-08 | ~12 | Prior release review |
| `QA-REPORT-v2.15-RULES-CONSISTENCY.md` | 2026-04-09 | 7 (F-001 to F-007) | This review cycle |
| `QA-REPORT-v2.15-CANONICAL-DOCS-CONSISTENCY.md` | 2026-04-09 | 6 (F-01 to F-06) | This review cycle |
| `QA-REPORT-v2.15-HUMAN-JOURNEY-GITFLOW.md` | 2026-04-09 | 22 (HJ-001 to MS-003) | This review cycle |

### 4.2 Resolution Status of Prior QA Findings

| Finding | From | Severity | Status |
|---------|------|----------|--------|
| F-001: release-gate.yml uses `develop-v*` | QA-REPORT-v2.15-RULES | CRITICAL | **UNRESOLVED** — still present in current code |
| F-002: canonical-docs-check.yml uses `develop-v*` | QA-REPORT-v2.15-RULES | CRITICAL | **UNRESOLVED** |
| F-003: Pre-receive hook wrong DOC-3/DOC-5 line counts | QA-REPORT-v2.15-RULES | MAJOR | **PARTIALLY RESOLVED** — hook logic has the bug (PRH-001), release-gate.yml correctly fixed, canonical-docs-check.yml correctly fixed |
| F-004: Pre-receive hook no branch naming enforcement | QA-REPORT-v2.15-RULES | MAJOR | **UNRESOLVED** — still missing `lab/`, `bugfix/`, `stabilization/` |
| F-005: .roomodes missing Orchestrator mode | QA-REPORT-v2.15-RULES | MINOR | **UNRESOLVED** |
| F-006: prompts/README.md SP-002 version mismatch | QA-REPORT-v2.15-RULES | MINOR | **UNRESOLVED** |
| GF-001: release-gate.yml trigger | QA-REPORT-v2.15-HUMAN | CRITICAL | **UNRESOLVED** (same as F-001) |
| GF-002: canonical-docs-check.yml trigger | QA-REPORT-v2.15-HUMAN | CRITICAL | **UNRESOLVED** (same as F-002) |
| GF-003: release-consistency-check.yml trigger | QA-REPORT-v2.15-HUMAN | CRITICAL | **NEW** — found in this review |
| GF-004: release-gate.yml version extraction | QA-REPORT-v2.15-HUMAN | MAJOR | **UNRESOLVED** |
| F-01: DOC-CURRENT pointers stale | QA-REPORT-v2.15-CANON | CRITICAL | **UNRESOLVED** — still pointing to v2.13 |
| F-02: v2.10-v2.13 cumulative docs missing | QA-REPORT-v2.15-CANON | MAJOR | **UNRESOLVED** |
| F-03: v2.15 release docs DRAFT status | QA-REPORT-v2.15-CANON | MINOR | **UNRESOLVED** |

### 4.3 Quality Trajectory Assessment

| Metric | Assessment |
|--------|------------|
| **Bugs Fixed vs Introduced** | 🟡 MIXED — Same CRITICAL issues persist across 3 consecutive QA reports (F-001, F-002 unchanged since first reported) |
| **Test Coverage** | 🔴 REGRESSION — No new tests added; coverage gaps (TC-001 through TC-012) were not addressed |
| **Automation Reliability** | 🟡 PARTIAL — release-gate.yml has correct P0 checks but wrong trigger; pre-receive hook has correct min lines but wrong case statement |
| **Documentation Quality** | 🟡 MIXED — QA reports are comprehensive (22+ findings in HUMAN-JOURNEY), but findings are not actioned |
| **Regression Risk** | 🔴 HIGH — Without tests for SP-002 sync, DOC-CURRENT pointers, branch naming, handoff protocol, and mode switching, future changes could break these systems undetected |

**Trajectory:** The quality infrastructure (rules, scripts, workflows) is well-designed but has **accumulated 6+ release cycles of unfixed issues**. Without test coverage for critical paths, the risk of breaking changes is increasing.

---

## Part 5: Consolidated Findings Summary

### 5.1 All Findings by Severity

| ID | Domain | Severity | File(s) | Issue | Status |
|----|--------|----------|---------|-------|--------|
| TC-001 | Test Coverage | **CRITICAL** | N/A | NO tests for branch naming enforcement | **NEW** |
| TC-002 | Test Coverage | **CRITICAL** | N/A | NO tests for DOC-CURRENT pointer updates | **NEW** |
| TC-003 | Test Coverage | **CRITICAL** | N/A | NO tests for SP-002 synchronization | **NEW** |
| TC-004 | Test Coverage | **CRITICAL** | N/A | NO tests for handoff protocol | **NEW** |
| TC-005 | Test Coverage | **CRITICAL** | N/A | NO tests for mode switching | **NEW** |
| TC-006 | Test Coverage | **MAJOR** | test_*.py | All tests are unit-only, no integration tests | **NEW** |
| TC-007 | Test Coverage | **MAJOR** | test_*.py | Incomplete coverage of Calypso components | **NEW** |
| TC-008 | Test Coverage | **MAJOR** | detect-merged-features.py | No tests for detect-merged-features.py | **NEW** |
| TC-009 | Test Coverage | **MINOR** | audit_cumulative_docs.py | No tests for audit_cumulative_docs.py | **NEW** |
| TC-010 | Test Coverage | **MINOR** | checkpoint_heartbeat.py | No tests for checkpoint_heartbeat.py | **NEW** |
| TC-011 | Test Coverage | **MINOR** | check-prompts-sync.ps1 | No tests for check-prompts-sync.ps1 | **NEW** |
| TC-012 | Test Coverage | **MINOR** | pre-receive | No tests for pre-receive hook | **NEW** |
| RB-001 | Script Robustness | **CRITICAL** | rebuild_sp002.py | No test coverage for the sync script | Duplicate of TC-003 |
| CB-001 | Script Robustness | **MAJOR** | checkpoint_heartbeat.py | Heartbeat append logic bug (lines 146-155) | **NEW** |
| CB-002 | Script Robustness | **MAJOR** | checkpoint_heartbeat.py | log_conversation() writes template, not actual conversation | **NEW** |
| DMF-001 | Script Robustness | **CRITICAL** | detect-merged-features.py | No test coverage | Duplicate of TC-008 |
| DMF-002 | Script Robustness | **MAJOR** | detect-merged-features.py | Hardcoded skeleton DOC-3 content | **NEW** |
| ACD-001 | Script Robustness | **MAJOR** | audit_cumulative_docs.py | Hardcoded RELEASES list (v2.10, v2.11 only) | **NEW** |
| RG-001 | Automation | **CRITICAL** | release-gate.yml | Triggers on `develop-v*` not `stabilization/v*` | UNRESOLVED (F-001) |
| CDC-001 | Automation | **CRITICAL** | canonical-docs-check.yml | Triggers on `develop-v*` not `stabilization/v*` | UNRESOLVED (F-002) |
| RCC-001 | Automation | **CRITICAL** | release-consistency-check.yml | PR trigger uses `develop-v*` | **NEW** (GF-003) |
| RG-002 | Automation | **MAJOR** | release-gate.yml | Version extraction hardcodes `develop-v` | UNRESOLVED (GF-004) |
| PRH-001 | Automation | **MAJOR** | pre-receive | Case statement applies wrong min lines for cumulative DOC-3/DOC-5 | **NEW** |
| PRH-002 | Automation | **MAJOR** | pre-receive | Branch pattern only checks `feature/` and `fix/` | UNRESOLVED (F-004) |
| PRH-003 | Automation | **MAJOR** | pre-receive | No direct commit check for main/develop/stabilization/* | **NEW** |
| DMF-002 | Automation | **MINOR** | detect-merged-features.yml | Triggers on develop but not stabilization/v* | MINOR |

### 5.2 New Findings (Not in Prior QA Reports)

| ID | Severity | Issue |
|----|----------|-------|
| TC-001 | CRITICAL | NO tests for branch naming enforcement |
| TC-002 | CRITICAL | NO tests for DOC-CURRENT pointer updates |
| TC-003 | CRITICAL | NO tests for SP-002 synchronization |
| TC-004 | CRITICAL | NO tests for handoff protocol |
| TC-005 | CRITICAL | NO tests for mode switching |
| TC-006 | MAJOR | All tests are unit-only, no integration tests |
| TC-007 | MAJOR | Incomplete coverage of Calypso components |
| TC-008 | MAJOR | No tests for detect-merged-features.py |
| CB-001 | MAJOR | checkpoint_heartbeat.py heartbeat append bug |
| CB-002 | MAJOR | checkpoint_heartbeat.py log_conversation() writes template |
| DMF-002 | MAJOR | detect-merged-features.py hardcoded skeleton DOC-3 |
| ACD-001 | MAJOR | audit_cumulative_docs.py hardcoded RELEASES list |
| PRH-001 | MAJOR | pre-receive case statement wrong min lines for cumulative DOC-3/DOC-5 |
| PRH-003 | MAJOR | pre-receive no direct commit check for main/develop/stabilization/* |
| RCC-001 | CRITICAL | release-consistency-check.yml uses `develop-v*` |

---

## Part 6: Action Items

### P0 — Critical (Must Fix Before Next Release)

| Priority | Owner | Action | Finding |
|----------|-------|--------|---------|
| P0 | QA Engineer | Add tests for SP-002 synchronization (rebuild_sp002.py) | TC-003 |
| P0 | QA Engineer | Add tests for DOC-CURRENT pointer consistency | TC-002 |
| P0 | QA Engineer | Add tests for branch naming enforcement (RULE 10.1) | TC-001 |
| P0 | QA Engineer | Add tests for handoff protocol (RULE 16) | TC-004 |
| P0 | QA Engineer | Add tests for mode switching (RULE 16.5) | TC-005 |
| P0 | Developer | Fix release-gate.yml trigger: `develop-v*` → `stabilization/v*` | RG-001 (UNRESOLVED) |
| P0 | Developer | Fix canonical-docs-check.yml trigger: `develop-v*` → `stabilization/v*` | CDC-001 (UNRESOLVED) |
| P0 | Developer | Fix release-consistency-check.yml: add `stabilization/v*` to PR branches | RCC-001 |
| P0 | Developer | Fix release-gate.yml version extraction: `develop-v` → `stabilization/v` | RG-002 (UNRESOLVED) |

### P1 — Major (Fix in v2.16)

| Priority | Owner | Action | Finding |
|----------|-------|--------|---------|
| P1 | QA Engineer | Add integration tests (temp Git repo, actual file I/O) | TC-006 |
| P1 | QA Engineer | Add tests for detect-merged-features.py | TC-008 |
| P1 | QA Engineer | Improve coverage of Calypso components | TC-007 |
| P1 | Developer | Fix pre-receive hook case statement: cumulative DOC-3=100, DOC-5=50 | PRH-001 |
| P1 | Developer | Expand pre-receive hook branch patterns: add `lab/`, `bugfix/`, `stabilization/`, `hotfix/` | PRH-002 (UNRESOLVED) |
| P1 | Developer | Add direct commit check to pre-receive hook (main, develop, stabilization/*) | PRH-003 |
| P1 | Developer | Fix checkpoint_heartbeat.py heartbeat append bug | CB-001 |
| P1 | Developer | Enhance checkpoint_heartbeat.py log_conversation() to capture actual content | CB-002 |
| P1 | Developer | Fix audit_cumulative_docs.py hardcoded RELEASES list | ACD-001 |
| P1 | Developer | Fix detect-merged-features.py hardcoded skeleton DOC-3 | DMF-002 |

### P2 — Minor (Fix When Convenient)

| Priority | Owner | Action | Finding |
|----------|-------|--------|---------|
| P2 | QA Engineer | Add tests for checkpoint_heartbeat.py | TC-010 |
| P2 | QA Engineer | Add tests for audit_cumulative_docs.py | TC-009 |
| P2 | QA Engineer | Add tests for check-prompts-sync.ps1 | TC-011 |
| P2 | QA Engineer | Add tests for pre-receive hook | TC-012 |
| P2 | Developer | Add `--dry-run` mode to rebuild_sp002.py | RB-003 |
| P2 | Developer | Add `--verbose` flag to check-prompts-sync.ps1 | CPS-002 |
| P2 | Developer | Add BOM handling to release-gate.yml SP-002 sync check | RG-003 |
| P2 | Developer | Add fast-forward develop step to release-gate.yml summary | RG-004 |

---

## Part 7: Items Confirmed Correct

### Scripts
- ✅ `scripts/rebuild_sp002.py`: Correct normalization, exit codes, error handling
- ✅ `scripts/check-prompts-sync.ps1`: Correct SP-001 through SP-006 extraction, SP-007 WARN handling

### GitHub Actions
- ✅ `release-gate.yml`: P0 blocker checks (SP-002 sync, line counts, pointer consistency, flags) are all correct
- ✅ `canonical-docs-check.yml`: Cumulative vs release-specific minimum line count differentiation is correct (500/500/300 vs 100/50)
- ✅ `detect-merged-features.yml`: Correct trigger conditions and tag-creation mode

### Pre-Receive Hook
- ✅ Line count minimums for release-specific docs (DOC-3: 100, DOC-5: 50) are correctly applied in the non-cumulative path

### Test Files
- ✅ `test_ideation_pipeline.py`: Tests IntakeAgent, SyncDetector, BranchTracker, ExecutionTracker
- ✅ `test_orchestrator.py`: Tests orchestrator_phase2/3/4 with mocked Anthropic API
- ✅ `test_triage.py`: Tests triage_dashboard and apply_triage with temp directory isolation

---

**End of QA Report**

**Report generated:** 2026-04-09  
**QA Engineer:** Mode qa-engineer  
**Model:** minimax/minimax-m2.7
