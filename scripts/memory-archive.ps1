<#
.SYNOPSIS
    le workbench - Memory Archive Script
    Rotates hot-context files to cold archive at sprint end.

.DESCRIPTION
    At sprint end, this script:
    1. Appends hot-context/activeContext.md to archive-cold/sprint-logs/sprint-NNN.md
    2. Appends hot-context/productContext.md to archive-cold/productContext_Master.md
    3. Resets hot-context/activeContext.md and hot-context/productContext.md to blank stubs
    4. Prints confirmation message

.PARAMETER SprintNumber
    The sprint number being archived (e.g., 1, 2, 3...)
    If not provided, auto-detects from existing sprint log files.

.EXAMPLE
    .\scripts\memory-archive.ps1 -SprintNumber 1
    .\scripts\memory-archive.ps1  # auto-detect sprint number
#>

param(
    [int]$SprintNumber = 0
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$HotContext = Join-Path $ProjectRoot "memory-bank\hot-context"
$ColdArchive = Join-Path $ProjectRoot "memory-bank\archive-cold"
$SprintLogs = Join-Path $ColdArchive "sprint-logs"
$ProductContextMaster = Join-Path $ColdArchive "productContext_Master.md"

# Auto-detect sprint number if not provided
if ($SprintNumber -eq 0) {
    $existingLogs = Get-ChildItem $SprintLogs -Filter "sprint-*.md" -ErrorAction SilentlyContinue
    $SprintNumber = $existingLogs.Count + 1
}

$SprintPadded = $SprintNumber.ToString("000")
$SprintLogFile = Join-Path $SprintLogs "sprint-$SprintPadded.md"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host ""
Write-Host "============================================================"
Write-Host "  le workbench - Memory Archive"
Write-Host "  Sprint: $SprintNumber | Timestamp: $Timestamp"
Write-Host "============================================================"
Write-Host ""

# Step 1: Archive activeContext.md to sprint log
$ActiveContextFile = Join-Path $HotContext "activeContext.md"
if (Test-Path $ActiveContextFile) {
    $activeContent = Get-Content $ActiveContextFile -Raw -Encoding UTF8
    $sprintHeader = @"

---

## Sprint $SprintNumber Archive — $Timestamp

### activeContext.md

$activeContent

"@
    Add-Content -Path $SprintLogFile -Value $sprintHeader -Encoding UTF8
    Write-Host "[OK] activeContext.md archived to sprint-$SprintPadded.md"
} else {
    Write-Host "[WARN] activeContext.md not found at $ActiveContextFile"
}

# Step 2: Archive productContext.md to productContext_Master.md
$ProductContextFile = Join-Path $HotContext "productContext.md"
if (Test-Path $ProductContextFile) {
    $productContent = Get-Content $ProductContextFile -Raw -Encoding UTF8
    $productHeader = @"

---

## Sprint $SprintNumber — $Timestamp

$productContent

"@
    Add-Content -Path $ProductContextMaster -Value $productHeader -Encoding UTF8
    Write-Host "[OK] productContext.md archived to productContext_Master.md"
} else {
    Write-Host "[WARN] productContext.md not found at $ProductContextFile"
}

# Step 3: Reset activeContext.md to blank stub
$activeStub = @"
---
# Active Context
**Last updated:** $(Get-Date -Format "yyyy-MM-dd")
**Active mode:** [MODE]
**Active LLM backend:** [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]

## Current task
[Start of Sprint $($SprintNumber + 1) — define current task]

## Last result
[Sprint $SprintNumber archived. See memory-bank/archive-cold/sprint-logs/sprint-$SprintPadded.md]

## Next step(s)
- [ ] [Define first action of Sprint $($SprintNumber + 1)]

## Blockers / Open questions
[None]

## Last Git commit
[To be filled]
---
"@
Set-Content -Path $ActiveContextFile -Value $activeStub -Encoding UTF8
Write-Host "[OK] activeContext.md reset to blank stub"

# Step 4: Reset productContext.md to blank stub
$productStub = @"
# Product Context

## Current Sprint User Stories

### Sprint $($SprintNumber + 1) — [Dates TBD]

#### US-001: [Title]
**As a** [persona]
**I want** [action]
**So that** [benefit]
**Acceptance criteria:**
- [ ] [Criterion 1]

## Backlog (Upcoming Sprints)
- [Feature to be defined]
"@
Set-Content -Path $ProductContextFile -Value $productStub -Encoding UTF8
Write-Host "[OK] productContext.md reset to blank stub"

Write-Host ""
Write-Host "============================================================"
Write-Host "  Archive complete. Sprint $SprintNumber archived."
Write-Host "  Sprint log: memory-bank/archive-cold/sprint-logs/sprint-$SprintPadded.md"
Write-Host "  Next: start Sprint $($SprintNumber + 1)"
Write-Host "============================================================"
Write-Host ""

# Step 5: Trigger Librarian Agent to index new archive content
$LibrarianScript = Join-Path $ProjectRoot "src\calypso\librarian_agent.py"
$NewFiles = @(
    (Join-Path $ColdArchive "sprint-logs\sprint-$SprintPadded.md"),
    $ProductContextMaster
)

if (Test-Path $LibrarianScript) {
    Write-Host "Triggering Librarian Agent to index new archive content..."
    $fileArgs = $NewFiles | Where-Object { Test-Path $_ } | ForEach-Object { "--files"; $_ }
    if ($fileArgs) {
        try {
            $result = & python $LibrarianScript --index @fileArgs 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[OK] Librarian Agent indexing complete."
                Write-Host $result
            } else {
                Write-Host "[WARN] Librarian Agent exited with code $LASTEXITCODE (Chroma may not be running)."
                Write-Host "       Run manually: python src/calypso/librarian_agent.py --index"
            }
        } catch {
            Write-Host "[WARN] Librarian Agent failed: $_"
            Write-Host "       Run manually: python src/calypso/librarian_agent.py --index"
        }
    } else {
        Write-Host "[WARN] No new archive files found to index."
    }
} else {
    Write-Host "[WARN] librarian_agent.py not found at $LibrarianScript"
    Write-Host "       Ensure PHASE-C is complete and src/calypso/ exists."
}

Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Review memory-bank/hot-context/activeContext.md (reset to stub)"
Write-Host "  2. Define Sprint $($SprintNumber + 1) goals in productContext.md"
Write-Host "  3. Commit the archive:"
Write-Host "     git add memory-bank/"
Write-Host "     git commit -m `"docs(memory): archive Sprint $SprintNumber to cold archive`""
Write-Host ""
