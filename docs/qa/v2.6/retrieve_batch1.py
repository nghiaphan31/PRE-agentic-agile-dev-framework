"""
retrieve_batch1.py
-----------------
Retrieves results from BATCH 1: Code vs Documentation

Usage (from workspace root):
    python docs/qa/v2.6/retrieve_batch1.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - Batch must have been submitted via submit_batch1_code.py
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BATCH_DIR = pathlib.Path("docs/qa/v2.6/BATCHES")
RESULTS_DIR = BATCH_DIR / "RESULTS"
BATCH_ID_FILE = BATCH_DIR / "batch_id_1_code.txt"
REPORT_FILE = RESULTS_DIR / "BATCH1-CODE-REPORT.md"

# Custom ID to title mapping
CUSTOM_IDS = {
    "code-calypso": "Calypso Phase 2-4 Scripts vs DOC-2 Architecture",
    "code-sync": "SyncDetector + RefinementWorkflow vs DOC-3",
    "code-heartbeat": "Session Heartbeat vs MB-4 Rule",
    "code-memory": "Memory Bank vs DOC-1 PRD",
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Load batch ID
    if not BATCH_ID_FILE.exists():
        print(f"[ERROR] batch_id file not found: {BATCH_ID_FILE}")
        print("Run submit_batch1_code.py first.")
        return
    
    batch_id = BATCH_ID_FILE.read_text(encoding="utf-8").strip()
    print(f"Retrieving batch: {batch_id}")
    
    # Initialize client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    client = anthropic.Anthropic(api_key=api_key)
    
    # Get batch status
    batch = client.messages.batches.retrieve(message_batch_id=batch_id)
    print(f"Batch status: {batch.processing_status}")
    
    if batch.processing_status != "ended":
        print(f"[WAIT] Batch status is '{batch.processing_status}'. Try again in 30 minutes.")
        return
    
    # Retrieve results
    print("Retrieving results...")
    results = client.messages.batches.results(message_batch_id=batch_id)
    
    # Build report
    report = "# BATCH 1: Code vs Documentation Coherence Report\n\n"
    report += f"**Batch ID:** {batch_id}\n"
    report += f"**Completed at:** {batch.expires_at}\n\n"
    report += "---\n\n"
    
    for result in sorted(results, key=lambda r: r.custom_id):
        custom_id = result.custom_id
        title = CUSTOM_IDS.get(custom_id, custom_id)
        
        if result.result.type == "errored":
            report += f"## {title}\n\n"
            report += f"**ERROR:** {result.result.error}\n\n"
            continue
        
        if result.result.type == "succeeded":
            message = result.result.message
            text_content = ""
            for content_block in message.content:
                if hasattr(content_block, 'text'):
                    text_content += content_block.text
            report += f"## {title}\n\n"
            report += text_content
            report += "\n\n---\n\n"
    
    # Save report
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"[OK] Report written to: {REPORT_FILE}")
    print(f"     Total size: {len(report):,} characters")

if __name__ == "__main__":
    main()
