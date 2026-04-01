"""
submit_batch3_prompt.py
-----------------------
BATCH 3: Prompt vs Deployment Coherence Audit

Submits 4 parallel requests to the Anthropic Batch API to audit:
1. SP-003 (product-owner) vs .roomodes product-owner
2. SP-004 (scrum-master) vs .roomodes scrum-master
3. SP-005 (developer) vs .roomodes developer
4. SP-006 (qa-engineer) vs .roomodes qa-engineer

Usage (from workspace root):
    python docs/qa/v2.6/submit_batch3_prompt.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to docs/qa/v2.6/BATCHES/batch_id_3_prompt.txt
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
BATCH_ID_FILE = BATCH_DIR / "batch_id_3_prompt.txt"

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
print("Loading files for Prompt vs Deployment Coherence audit...")

ROOMODES = load(".roomodes")
SP003 = load("prompts/SP-003-persona-product-owner.md")
SP004 = load("prompts/SP-004-persona-scrum-master.md")
SP005 = load("prompts/SP-005-persona-developer.md")
SP006 = load("prompts/SP-006-persona-qa-engineer.md")

print("Files loaded successfully.")

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a Senior Technical Writer conducting a prompt-vs-deployment coherence audit.

Compare the PROMPT FILE (the system prompt as deployed in Roo Code) against the ROOMODES FILE (the canonical persona definition).
Identify any discrepancies in roleDefinition, rules, commands, or constraints.
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
        "custom_id": "prompt-productowner",
        "title": "SP-003 (product-owner) vs .roomodes product-owner",
        "prompt": SP003,
        "roomodes": ROOMODES,
        "persona": "product-owner",
    },
    {
        "custom_id": "prompt-scrummaster",
        "title": "SP-004 (scrum-master) vs .roomodes scrum-master",
        "prompt": SP004,
        "roomodes": ROOMODES,
        "persona": "scrum-master",
    },
    {
        "custom_id": "prompt-developer",
        "title": "SP-005 (developer) vs .roomodes developer",
        "prompt": SP005,
        "roomodes": ROOMODES,
        "persona": "developer",
    },
    {
        "custom_id": "prompt-qaengineer",
        "title": "SP-006 (qa-engineer) vs .roomodes qa-engineer",
        "prompt": SP006,
        "roomodes": ROOMODES,
        "persona": "qa-engineer",
    },
]

# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Anthropic(api_key=api_key)

print(f"\nSubmitting BATCH 3: Prompt vs Deployment with {len(REQUESTS)} requests to model {MODEL}...")

batch_requests = []
for req in REQUESTS:
    prompt = f"""## Audit Request: {req['title']}

### PROMPT FILE (SP)
```
{req['prompt']}
```

### ROOMODES DEPLOYMENT (extract the {req['persona']} section)
```
{req['roomodes']}
```

Compare the roleDefinition, rules, and constraints for the {req['persona']} persona between PROMPT and ROOMODES.
Identify any discrepancies in wording, missing rules, or conflicting requirements."""

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
print(f"\nRun retrieve_batch3.py after 1-4 hours to get results.")
