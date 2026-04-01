"""
submit_batch2_gov.py
--------------------
BATCH 2: Governance Coherence Audit

Submits 3 parallel requests to the Anthropic Batch API to audit:
1. .clinerules vs SP-002 embedded rules
2. template/.clinerules vs root .clinerules
3. prompts/README.md vs actual SP files

Usage (from workspace root):
    python docs/qa/v2.6/submit_batch2_gov.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to docs/qa/v2.6/BATCHES/batch_id_2_gov.txt
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
BATCH_ID_FILE = BATCH_DIR / "batch_id_2_gov.txt"

# ---------------------------------------------------------------------------
# Helper: load file
# ---------------------------------------------------------------------------
def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Load files
# ---------------------------------------------------------------------------
print("Loading files for Governance Coherence audit...")

CLINERULES_ROOT = load(".clinerules")
CLINERULES_TEMPLATE = load("template/.clinerules")
SP002 = load("prompts/SP-002-clinerules-global.md")
SP003 = load("prompts/SP-003-persona-product-owner.md")
SP004 = load("prompts/SP-004-persona-scrum-master.md")
SP005 = load("prompts/SP-005-persona-developer.md")
SP006 = load("prompts/SP-006-persona-qa-engineer.md")
ROOMODES = load(".roomodes")
PROMPTS_README = load("prompts/README.md")

print("Files loaded successfully.")

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a Senior Technical Writer conducting a governance coherence audit.

Compare the SOURCE file against the DEPLOYMENT file and identify any discrepancies.
Classify severity: P0 (critical), P1 (important), P2 (nice to have).

Output format:
```
## 1. Executive Summary
3-5 bullet points

## 2. Findings

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
# Build requests
# ---------------------------------------------------------------------------
REQUESTS = [
    {
        "custom_id": "gov-clinerules-sp002",
        "title": ".clinerules vs SP-002 Embedded Rules",
        "source": CLINERULES_ROOT,
        "deployment": SP002,
    },
    {
        "custom_id": "gov-template-root",
        "title": "template/.clinerules vs root .clinerules",
        "source": CLINERULES_TEMPLATE,
        "deployment": CLINERULES_ROOT,
    },
    {
        "custom_id": "gov-sp-readme",
        "title": "prompts/README.md vs SP Registry",
        "source": PROMPTS_README,
        "deployment": f"SP-003:\n{SP003[:2000]}\n\nSP-004:\n{SP004[:2000]}\n\nSP-005:\n{SP005[:2000]}\n\nSP-006:\n{SP006[:2000]}",
    },
]

# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Anthropic(api_key=api_key)

print(f"\nSubmitting BATCH 2: Governance Coherence with {len(REQUESTS)} requests to model {MODEL}...")

batch_requests = []
for req in REQUESTS:
    prompt = f"""## Audit Request: {req['title']}

### SOURCE (Deployment Target)
```
{req['source'][:12000]}
```

### DEPLOYMENT (Current State)
```
{req['deployment'][:12000]}
```

Compare SOURCE vs DEPLOYMENT and identify discrepancies."""

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

batch = client.messages.batches.create(requests=batch_requests)
batch_id = batch.id
print(f"[OK] Batch submitted successfully!")
print(f"    Batch ID  : {batch_id}")
print(f"    Status    : in_progress")
BATCH_DIR.mkdir(parents=True, exist_ok=True)
BATCH_ID_FILE.write_text(batch_id, encoding="utf-8")
print(f"[OK] batch_id saved to {BATCH_ID_FILE}")
print(f"\nRun retrieve_batch2.py after 1-4 hours to get results.")
