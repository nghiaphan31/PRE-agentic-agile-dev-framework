"""
submit_batch1_code.py
---------------------
BATCH 1: Code vs Documentation Coherence Audit

Submits 4 parallel requests to the Anthropic Batch API to audit:
1. Calypso Phase 2-4 scripts vs DOC-2 Architecture
2. SyncDetector + RefinementWorkflow vs DOC-3 Implementation Plan
3. Session heartbeat (checkpoint_heartbeat.py) vs MB-4 rule
4. Memory Bank structure vs DOC-1 PRD

Usage (from workspace root):
    python docs/qa/v2.6/submit_batch1_code.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to docs/qa/v2.6/BATCHES/batch_id_1_code.txt
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
TEMPERATURE = 0.3
BATCH_DIR = pathlib.Path("docs/qa/v2.6/BATCHES")
BATCH_ID_FILE = BATCH_DIR / "batch_id_1_code.txt"

# ---------------------------------------------------------------------------
# Helper: load file with error checking
# ---------------------------------------------------------------------------
def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Load all files to audit
# ---------------------------------------------------------------------------
print("Loading files for Code vs Documentation audit...")

# Code files
CALYPSO_ORCHESTRATOR = load("src/calypso/orchestrator_phase2.py")[:8000]
CALYPSO_SYNC = load("src/calypso/sync_detector.py")[:6000]
CALYPSO_REFINEMENT = load("src/calypso/refinement_workflow.py")[:6000]
CHECKPOINT_HEARTBEAT = load("scripts/checkpoint_heartbeat.py")[:4000]

# Documentation
DOC2_ARCHITECTURE = load("docs/releases/v2.6/DOC-2-v2.6-Architecture.md")[:10000]
DOC3_IMPLEMENTATION = load("docs/releases/v2.6/DOC-3-v2.6-Implementation-Plan.md")[:10000]
DOC1_PRD = load("docs/releases/v2.6/DOC-1-v2.6-PRD.md")[:10000]
CLINERULES = load(".clinerules")[:8000]

# Memory Bank
MEMORY_HOT_CONTEXT = load("memory-bank/hot-context/activeContext.md")[:4000]
MEMORY_PROGRESS = load("memory-bank/hot-context/progress.md")[:4000]

print("Files loaded successfully.")

# ---------------------------------------------------------------------------
# System prompt for code auditor
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a Senior Software Architect conducting a rigorous code-vs-documentation coherence audit.

For each audit request:
1. Compare the CODE section with the DOCUMENTATION section
2. Identify specific discrepancies (missing features, undocumented behavior, drift)
3. Classify severity: P0 (critical), P1 (important), P2 (nice to have)
4. Provide file:line references where possible

Output format:
```
## 1. Executive Summary
3-5 bullet points

## 2. Findings
Detailed findings with file:line references

## 3. Inconsistencies Found
| Severity | Location | Description | Expected | Actual |
|---|---|---|---|---|

## 4. Prioritized Remediation
- **P0 (Critical):** ...
- **P1 (Important):** ...
- **P2 (Nice to have):** ...

## 5. Verdict
[CONSISTENT] / [MINOR_ISSUES] / [MAJOR_INCONSISTENCIES]
```"""

# ---------------------------------------------------------------------------
# Build the 4 audit requests
# ---------------------------------------------------------------------------
REQUESTS = [
    {
        "custom_id": "code-calypso",
        "title": "Calypso Phase 2-4 Scripts vs DOC-2 Architecture",
        "code": CALYPSO_ORCHESTRATOR,
        "doc": DOC2_ARCHITECTURE,
    },
    {
        "custom_id": "code-sync",
        "title": "SyncDetector + RefinementWorkflow vs DOC-3",
        "code": CALYPSO_SYNC + "\n\n" + CALYPSO_REFINEMENT,
        "doc": DOC3_IMPLEMENTATION,
    },
    {
        "custom_id": "code-heartbeat",
        "title": "Session Heartbeat vs MB-4 Rule",
        "code": CHECKPOINT_HEARTBEAT,
        "doc": CLINERULES,
    },
    {
        "custom_id": "code-memory",
        "title": "Memory Bank vs DOC-1 PRD",
        "code": MEMORY_HOT_CONTEXT + "\n\n" + MEMORY_PROGRESS,
        "doc": DOC1_PRD,
    },
]

# ---------------------------------------------------------------------------
# Submit to Anthropic Batch API
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Anthropic(api_key=api_key)

print(f"\nSubmitting BATCH 1: Code vs Documentation with {len(REQUESTS)} requests to model {MODEL}...")

# Build batch requests
batch_requests = []
for req in REQUESTS:
    prompt = f"""## Audit Request: {req['title']}

### CODE TO AUDIT
```
{req['code']}
```

### DOCUMENTATION TO COMPARE AGAINST
```
{req['doc']}
```

---

Perform the audit and produce the structured report."""

    batch_requests.append(
        anthropic.types.messages.batch_create_params.Request(
            custom_id=req["custom_id"],
            params=anthropic.types.messages.batch_create_params.MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
        )
    )

# Submit batch
batch = client.messages.batches.create(requests=batch_requests)
batch_id = batch.id
print(f"[OK] Batch submitted successfully!")
print(f"    Batch ID  : {batch_id}")
print(f"    Status    : in_progress")

# Save batch_id for retrieval
BATCH_DIR.mkdir(parents=True, exist_ok=True)
BATCH_ID_FILE.write_text(batch_id, encoding="utf-8")
print(f"[OK] batch_id saved to {BATCH_ID_FILE}")
print(f"\nRun retrieve_batch1.py after 1-4 hours to get results.")
