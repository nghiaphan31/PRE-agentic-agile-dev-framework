<#
.SYNOPSIS
    Updates this project from the agentic-agile-workbench.

.DESCRIPTION
    This file is deployed into application projects by the
    agentic-agile-workbench. It serves as the entry point to trigger
    an update of the project from a new version of the workbench.

    It delegates execution to the canonical script deploy-workbench-to-project.ps1
    located at the root of the workbench.

    PREREQUISITES:
    ==============
    The agentic-agile-workbench repository must be cloned locally.
    Recommended structure:
      $env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\
        ├── agentic-agile-workbench\   (the workbench)
        └── PROJECTS\this-project\     (this project)

.PARAMETER WorkbenchPath
    Absolute path to the root of the agentic-agile-workbench repository.
    Default: deduced from the canonical folder structure.

.EXAMPLE
    # Update from the workbench (path deduced automatically)
    .\scripts\update-workbench.ps1

.EXAMPLE
    # Update with explicit path to the workbench
    .\scripts\update-workbench.ps1 -WorkbenchPath "C:\Dev\agentic-agile-workbench"

.NOTES
    File deployed automatically by deploy-workbench-to-project.ps1 (workbench root).
    Do not modify this file directly — modify the canonical script in the workbench.
#>

param(
    [string]$WorkbenchPath = ""
)

$ErrorActionPreference = "Stop"

# Path of this project (root = parent of scripts/)
$ProjectPath = Split-Path -Parent $PSScriptRoot

# Deduce the workbench path if not provided
if (-not $WorkbenchPath) {
    # Canonical structure: ..\agentic-agile-workbench\ is a sibling of the project's parent folder
    $ProjectsRoot = Split-Path -Parent $ProjectPath
    $WorkbenchPath = Join-Path $ProjectsRoot "agentic-agile-workbench"
}

$CanonicalScript = Join-Path $WorkbenchPath "deploy-workbench-to-project.ps1"

Write-Host ""
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "  update-workbench.ps1 — Update from the workbench" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project   : $ProjectPath" -ForegroundColor White
Write-Host "  Workbench : $WorkbenchPath" -ForegroundColor White
Write-Host "  Script    : deploy-workbench-to-project.ps1" -ForegroundColor White
Write-Host ""

if (-not (Test-Path $CanonicalScript)) {
    Write-Host "ERROR: Canonical script not found at:" -ForegroundColor Red
    Write-Host "  $CanonicalScript" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "  1. Clone the workbench: git clone https://github.com/nghiaphan31/agentic-agile-workbench.git"
    Write-Host "  2. Or specify the path: .\scripts\update-workbench.ps1 -WorkbenchPath `"path\to\workbench`""
    Write-Host ""
    exit 1
}

Write-Host "Delegating to the canonical script..." -ForegroundColor Cyan
Write-Host ""

& $CanonicalScript -ProjectPath $ProjectPath -Update
