<#
.SYNOPSIS
    le workbench - Verification of coherence between canonical system prompts and deployed artifacts.
    REQ-8.1, REQ-8.3, REQ-8.4 | DA-013

.DESCRIPTION
    Compares the content of each canonical SP (prompts/SP-XXX-*.md) with the corresponding
    deployed artifact. Uses normalized comparison (CRLF->LF, trim).
    SP-007 (Gem Gemini) is excluded from automatic verification with a warning.
    Returns exit code 0 if everything is synchronized, 1 if desynchronization detected.
#>

param(
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PromptsDir = Join-Path $ProjectRoot "prompts"
$PassCount = 0
$FailCount = 0
$WarnCount = 0

function Normalize-Text {
    param([string]$Text)
    # Normalization: CRLF -> LF, trim spaces/line breaks at start/end
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n").Trim()
}

function Extract-PromptContent {
    param([string]$SpFile)
    # Extract content between ```markdown or ``` tags (first code block)
    $content = Get-Content $SpFile -Raw -Encoding UTF8
    if ($content -match '(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n```') {
        return Normalize-Text $Matches[1]
    }
    return $null
}

function Show-Diff {
    param([string]$Expected, [string]$Actual, [string]$Label)
    $expLines = $Expected -split "`n"
    $actLines = $Actual -split "`n"
    $maxLines = [Math]::Max($expLines.Count, $actLines.Count)
    $diffLines = @()
    for ($i = 0; $i -lt [Math]::Min($maxLines, 20); $i++) {
        $e = if ($i -lt $expLines.Count) { $expLines[$i] } else { "" }
        $a = if ($i -lt $actLines.Count) { $actLines[$i] } else { "" }
        if ($e -ne $a) {
            $diffLines += "  Line $($i+1):"
            $diffLines += "    SP (expected) : $e"
            $diffLines += "    Deployed      : $a"
        }
    }
    if ($diffLines.Count -gt 0) {
        Write-Host "  First differences:" -ForegroundColor Yellow
        $diffLines | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
}

Write-Host ""
Write-Host ("=" * 60)
Write-Host "  le workbench - Prompt Coherence Verification" -ForegroundColor Cyan
Write-Host ("=" * 60)

# --- SP-001 : Modelfile ---
Write-Host ""
Write-Host "[SP-001] Modelfile SYSTEM block..." -NoNewline
$ModelfilePath = Join-Path $ProjectRoot "Modelfile"
$Sp001Path = Join-Path $PromptsDir "SP-001-ollama-modelfile-system.md"
if (-not (Test-Path $ModelfilePath)) {
    Write-Host " SKIP (Modelfile not found)" -ForegroundColor Yellow
    $WarnCount++
} else {
    $spContent = Extract-PromptContent $Sp001Path
    $modelfileRaw = Get-Content $ModelfilePath -Raw -Encoding UTF8
    if ($modelfileRaw -match '(?s)SYSTEM\s+"""(.*?)"""') {
        $deployedContent = Normalize-Text $Matches[1]
        if ($spContent -eq $deployedContent) {
            Write-Host " PASS" -ForegroundColor Green
            $PassCount++
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            Show-Diff $spContent $deployedContent "SP-001"
            $FailCount++
        }
    } else {
        Write-Host " FAIL (SYSTEM block not found in Modelfile)" -ForegroundColor Red
        $FailCount++
    }
}

# --- SP-002 : .clinerules ---
Write-Host "[SP-002] .clinerules (entire file)..." -NoNewline
$ClinerPath = Join-Path $ProjectRoot ".clinerules"
$Sp002Path = Join-Path $PromptsDir "SP-002-clinerules-global.md"
if (-not (Test-Path $ClinerPath)) {
    Write-Host " SKIP (.clinerules not found)" -ForegroundColor Yellow
    $WarnCount++
} else {
    $spContent = Extract-PromptContent $Sp002Path
    $deployedContent = Normalize-Text (Get-Content $ClinerPath -Raw -Encoding UTF8)
    if ($spContent -eq $deployedContent) {
        Write-Host " PASS" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " FAIL" -ForegroundColor Red
        Show-Diff $spContent $deployedContent "SP-002"
        $FailCount++
    }
}

# --- SP-003 to SP-006 : .roomodes ---
$RoomodesPath = Join-Path $ProjectRoot ".roomodes"
$SpPersonas = @(
    @{ Id = "SP-003"; File = "SP-003-persona-product-owner.md"; Slug = "product-owner"; Index = 0 },
    @{ Id = "SP-004"; File = "SP-004-persona-scrum-master.md"; Slug = "scrum-master"; Index = 1 },
    @{ Id = "SP-005"; File = "SP-005-persona-developer.md"; Slug = "developer"; Index = 2 },
    @{ Id = "SP-006"; File = "SP-006-persona-qa-engineer.md"; Slug = "qa-engineer"; Index = 3 }
)

if (-not (Test-Path $RoomodesPath)) {
    Write-Host "[SP-003..006] .roomodes not found - SKIP" -ForegroundColor Yellow
    $WarnCount += 4
} else {
    $roomodesJson = Get-Content $RoomodesPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($persona in $SpPersonas) {
        Write-Host "[$($persona.Id)] .roomodes > $($persona.Slug) roleDefinition..." -NoNewline
        $spFile = Join-Path $PromptsDir $persona.File
        $spContent = Extract-PromptContent $spFile
        $mode = $roomodesJson.customModes | Where-Object { $_.slug -eq $persona.Slug }
        if ($null -eq $mode) {
            Write-Host " FAIL (slug '$($persona.Slug)' not found in .roomodes)" -ForegroundColor Red
            $FailCount++
        } else {
            $deployedContent = Normalize-Text $mode.roleDefinition
            if ($spContent -eq $deployedContent) {
                Write-Host " PASS" -ForegroundColor Green
                $PassCount++
            } else {
                Write-Host " FAIL" -ForegroundColor Red
                Show-Diff $spContent $deployedContent $persona.Id
                $FailCount++
            }
        }
    }
}

# --- SP-007 : Gem Gemini (outside Git - manual verification) ---
Write-Host ""
Write-Host "[SP-007] Gem Gemini 'Roo Code Agent'..." -NoNewline
Write-Host " WARNING (manual deployment required)" -ForegroundColor Yellow
Write-Host "  -> Verify manually at https://gemini.google.com > Gems > 'Roo Code Agent'"
Write-Host "  -> Compare with: prompts/SP-007-gem-gemini-roo-agent.md"
$WarnCount++

# --- Summary ---
Write-Host ""
Write-Host ("=" * 60)
Write-Host "  SUMMARY: $PassCount PASS | $FailCount FAIL | $WarnCount WARN" -ForegroundColor $(if ($FailCount -gt 0) { "Red" } elseif ($WarnCount -gt 0) { "Yellow" } else { "Green" })
Write-Host ("=" * 60)
Write-Host ""

if ($FailCount -gt 0) {
    Write-Host "FAILURE: $FailCount prompt(s) desynchronized. Commit blocked." -ForegroundColor Red
    Write-Host "Action required: update the deployed artifacts to match the canonical SPs." -ForegroundColor Red
    exit 1
} else {
    Write-Host "SUCCESS: All verifiable prompts are synchronized." -ForegroundColor Green
    exit 0
}
