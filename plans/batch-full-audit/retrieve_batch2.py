"""
retrieve_batch2.py
------------------
Retrieves results from BATCH 2: Cross-Document Coherence Audit.

Usage (from workspace root):
    python plans/batch-full-audit/retrieve_batch2.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - Batch must have been submitted via submit_batch2_crossdocs.py
    - batch_id_2_crossdocs.txt must exist

Output:
    - Prints batch status to stdout
    - Writes results to plans/batch-full-audit/RESULTS/BATCH2-CROSSDOCS-REPORT.md
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BATCH_DIR = pathlib.Path("plans/batch-full-audit")
RESULTS_DIR = BATCH_DIR / "RESULTS"
BATCH_ID_FILE = BATCH_DIR / "batch_id_2_crossdocs.txt"
OUTPUT_FILE = RESULTS_DIR / "BATCH2-CROSSDOCS-REPORT.md"

# ---------------------------------------------------------------------------
# Load batch ID
# ---------------------------------------------------------------------------
if not BATCH_ID_FILE.exists():
    raise FileNotFoundError(
        f"batch_id file not found: {BATCH_ID_FILE}\n"
        "Run submit_batch2_crossdocs.py first to submit the batch."
    )

batch_id = BATCH_ID_FILE.read_text(encoding="utf-8").strip()
print(f"Loaded batch_id: {batch_id}")

# ---------------------------------------------------------------------------
# Retrieve batch results
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY environment variable is not set.\n"
        "Set it with: $env:ANTHROPIC_API_KEY = 'sk-ant-...'"
    )

client = anthropic.Anthropic(api_key=api_key)

print(f"\nRetrieving batch status...")
batch = client.messages.batches.retrieve(message_batch_id=batch_id)

print(f"   Batch ID  : {batch.id}")
print(f"   Status    : {batch.processing_status}")
print(f"   Created at: {batch.created_at}")
print(f"   Expires at: {batch.expires_at}")

# ---------------------------------------------------------------------------
# Check if complete
# ---------------------------------------------------------------------------
if batch.processing_status != "ended":
    print(f"\n[WAIT] Batch status is '{batch.processing_status}'.")
    print(f"       Try again in 30 minutes.")
    print(f"       The batch will complete within 24 hours (typically 1-4 hours).")
    exit(1)

# ---------------------------------------------------------------------------
# Retrieve results
# ---------------------------------------------------------------------------
print(f"\nBatch complete! Retrieving results...")
results = client.messages.batches.results(message_batch_id=batch_id)

# ---------------------------------------------------------------------------
# Build the report
# ---------------------------------------------------------------------------
report = f"""# BATCH 2: Cross-Document Coherence Audit — Results

**Batch ID:** `{batch_id}`
**Status:** {batch.processing_status}
**Completed at:** {batch.expires_at}

---

"""

custom_ids = [
    "xd-doc12-v22",
    "xd-doc23-v22",
    "xd-version-drift",
    "xd-current-pointers",
]

for result in results:
    custom_id = result.custom_id
    print(f"\nProcessing result: {custom_id}")
    
    if result.type == "error":
        report += f"""## Result: {custom_id}

**Status:** ERROR

```
{result.error}
```

---

"""
        continue
    
    # Get the response text
    response_text = result.content[0].text
    
    report += f"""## Result: {custom_id}

{response_text}

---

"""

# ---------------------------------------------------------------------------
# Write the report
# ---------------------------------------------------------------------------
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(report, encoding="utf-8")

print(f"\n[OK] Results written to: {OUTPUT_FILE}")
print(f"     Total report size: {len(report):,} characters")
