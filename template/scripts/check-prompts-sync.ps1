<#
.SYNOPSIS
    le workbench — Verification de coherence des system prompts canoniques vs artefacts deployes.
    REQ-8.1, REQ-8.3, REQ-8.4 | DA-013

.DESCRIPTION
    Compare le contenu de chaque SP canonique (prompts/SP-XXX-*.md) avec l'artefact
    deploye correspondant. Utilise une comparaison normalisee (CRLF->LF, trim).
    SP-007 (Gem Gemini) est exclu de la verification automatique avec avertissement.
    Retourne exit code 0 si tout est synchronise, 1 si desynchronisation detectee.
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
    # Normalisation : CRLF -> LF, trim espaces/sauts de ligne en debut/fin
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n").Trim()
}

function Extract-PromptContent {
    param([string]$SpFile)
    # Extraire le contenu entre les balises ```markdown ou ``` (premier bloc de code)
    $content = Get-Content $SpFile -Raw -Encoding UTF8
    if ($content -match "(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n```") {
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
            $diffLines += "  Ligne $($i+1):"
            $diffLines += "    SP (attendu) : $e"
            $diffLines += "    Deploye      : $a"
        }
    }
    if ($diffLines.Count -gt 0) {
        Write-Host "  Premieres differences :" -ForegroundColor Yellow
        $diffLines | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
}

Write-Host ""
Write-Host ("=" * 60)
Write-Host "  le workbench — Verification Coherence Prompts" -ForegroundColor Cyan
Write-Host ("=" * 60)

# --- SP-001 : Modelfile ---
Write-Host ""
Write-Host "[SP-001] Modelfile bloc SYSTEM..." -NoNewline
$ModelfilePath = Join-Path $ProjectRoot "Modelfile"
$Sp001Path = Join-Path $PromptsDir "SP-001-ollama-modelfile-system.md"
if (-not (Test-Path $ModelfilePath)) {
    Write-Host " SKIP (Modelfile absent)" -ForegroundColor Yellow
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
        Write-Host " FAIL (bloc SYSTEM introuvable dans Modelfile)" -ForegroundColor Red
        $FailCount++
    }
}

# --- SP-002 : .clinerules ---
Write-Host "[SP-002] .clinerules (fichier entier)..." -NoNewline
$ClinerPath = Join-Path $ProjectRoot ".clinerules"
$Sp002Path = Join-Path $PromptsDir "SP-002-clinerules-global.md"
if (-not (Test-Path $ClinerPath)) {
    Write-Host " SKIP (.clinerules absent)" -ForegroundColor Yellow
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

# --- SP-003 a SP-006 : .roomodes ---
$RoomodesPath = Join-Path $ProjectRoot ".roomodes"
$SpPersonas = @(
    @{ Id = "SP-003"; File = "SP-003-persona-product-owner.md"; Slug = "product-owner"; Index = 0 },
    @{ Id = "SP-004"; File = "SP-004-persona-scrum-master.md"; Slug = "scrum-master"; Index = 1 },
    @{ Id = "SP-005"; File = "SP-005-persona-developer.md"; Slug = "developer"; Index = 2 },
    @{ Id = "SP-006"; File = "SP-006-persona-qa-engineer.md"; Slug = "qa-engineer"; Index = 3 }
)

if (-not (Test-Path $RoomodesPath)) {
    Write-Host "[SP-003..006] .roomodes absent — SKIP" -ForegroundColor Yellow
    $WarnCount += 4
} else {
    $roomodesJson = Get-Content $RoomodesPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($persona in $SpPersonas) {
        Write-Host "[$($persona.Id)] .roomodes > $($persona.Slug) roleDefinition..." -NoNewline
        $spFile = Join-Path $PromptsDir $persona.File
        $spContent = Extract-PromptContent $spFile
        $mode = $roomodesJson.customModes | Where-Object { $_.slug -eq $persona.Slug }
        if ($null -eq $mode) {
            Write-Host " FAIL (slug '$($persona.Slug)' introuvable dans .roomodes)" -ForegroundColor Red
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

# --- SP-007 : Gem Gemini (hors Git — verification manuelle) ---
Write-Host ""
Write-Host "[SP-007] Gem Gemini 'Roo Code Agent'..." -NoNewline
Write-Host " AVERTISSEMENT (deploiement manuel requis)" -ForegroundColor Yellow
Write-Host "  -> Verifier manuellement sur https://gemini.google.com > Gems > 'Roo Code Agent'"
Write-Host "  -> Comparer avec : prompts/SP-007-gem-gemini-roo-agent.md"
$WarnCount++

# --- Resume ---
Write-Host ""
Write-Host ("=" * 60)
Write-Host "  RESUME : $PassCount PASS | $FailCount FAIL | $WarnCount WARN" -ForegroundColor $(if ($FailCount -gt 0) { "Red" } elseif ($WarnCount -gt 0) { "Yellow" } else { "Green" })
Write-Host ("=" * 60)
Write-Host ""

if ($FailCount -gt 0) {
    Write-Host "ECHEC : $FailCount prompt(s) desynchronise(s). Commit bloque." -ForegroundColor Red
    Write-Host "Action requise : mettre a jour les artefacts deployes pour correspondre aux SP canoniques." -ForegroundColor Red
    exit 1
} else {
    Write-Host "SUCCES : Tous les prompts verifiables sont synchronises." -ForegroundColor Green
    exit 0
}
