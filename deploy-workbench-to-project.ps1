<#
.SYNOPSIS
    agentic-agile-workbench — Deploys the workbench to an application project.

.DESCRIPTION
    Copies the template/ files from the workbench to a target project.
    In -Update mode, updates an existing project from a new version of the workbench.
    Writes .workbench-version to the target project for traceability.

    This script is the CANONICAL script of the workbench. It must be executed from
    the root of the agentic-agile-workbench repository.

    A wrapper script (update-workbench.ps1) is deployed in scripts/ of each
    application project. This wrapper script redirects to this canonical script for
    any subsequent updates.

.PARAMETER ProjectPath
    Absolute path to the root folder of the target application project.

.PARAMETER Update
    Update mode: updates an existing project from the new version of the workbench.

.PARAMETER DryRun
    Simulates the deployment without copying anything. Displays what would be done.

.EXAMPLE
    # Initial deployment on a new project
    # Canonical structure: $env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\
    #   ├── agentic-agile-workbench\   (the workbench — this repository)
    #   └── PROJECTS\my-new-project\   (the application project)
    $Project = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-new-project"
    .\deploy-workbench-to-project.ps1 -ProjectPath $Project

.EXAMPLE
    # Update an existing project after a new version of the workbench
    $Project = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-project"
    .\deploy-workbench-to-project.ps1 -ProjectPath $Project -Update

.EXAMPLE
    # Simulation without modification
    $Project = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\my-project"
    .\deploy-workbench-to-project.ps1 -ProjectPath $Project -DryRun
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,

    [switch]$Update = $false,
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

# --- Paths ---
# This script lives at the root of the workbench. template/ is a direct subfolder.
$WorkbenchRoot = $PSScriptRoot
$TemplatePath  = Join-Path $WorkbenchRoot "template"
$WorkbenchVersion = (Get-Content (Join-Path $WorkbenchRoot "VERSION") -Raw).Trim()

# Files and folders to copy from template/
$FilesToCopy = @(
    ".roomodes",
    ".clinerules",
    ".workbench-version",
    "Modelfile",
    "proxy.py",
    "requirements.txt"
)
$FoldersToCopy = @(
    "prompts",
    "scripts"
)

# --- Validation ---
Write-Host ""
Write-Host ("=" * 60)
Write-Host "  agentic-agile-workbench — Deployment v$WorkbenchVersion" -ForegroundColor Cyan
if ($DryRun) { Write-Host "  DRY RUN MODE (no modifications)" -ForegroundColor Yellow }
if ($Update)  { Write-Host "  UPDATE MODE" -ForegroundColor Yellow }
Write-Host ("=" * 60)
Write-Host ""

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project folder '$ProjectPath' does not exist." -ForegroundColor Red
    Write-Host "Create the folder first and initialize Git:"
    Write-Host "  git init '$ProjectPath'"
    exit 1
}

# Check if Git is initialized in the project
if (-not (Test-Path (Join-Path $ProjectPath ".git"))) {
    Write-Host "WARNING: No Git repository detected in '$ProjectPath'." -ForegroundColor Yellow
    Write-Host "It is strongly recommended to initialize Git before deployment:"
    Write-Host "  cd '$ProjectPath' && git init"
    $confirm = Read-Host "Continue anyway? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") { exit 0 }
}

# In Update mode, check the current version of the project
if ($Update) {
    $ProjectVersionFile = Join-Path $ProjectPath ".workbench-version"
    if (Test-Path $ProjectVersionFile) {
        $CurrentVersion = (Get-Content $ProjectVersionFile -Raw).Trim()
        Write-Host "Current version in project : $CurrentVersion"
        Write-Host "New workbench version       : $WorkbenchVersion"
        Write-Host ""
        if ($CurrentVersion -eq $WorkbenchVersion) {
            Write-Host "Project is already up to date (v$WorkbenchVersion)." -ForegroundColor Green
            exit 0
        }
    } else {
        Write-Host "No .workbench-version file found — initial deployment." -ForegroundColor Yellow
    }
}

# --- File copy ---
$CopiedCount = 0
$SkippedCount = 0

Write-Host "Files to deploy:"
Write-Host ""

# Individual files
foreach ($file in $FilesToCopy) {
    $src = Join-Path $TemplatePath $file
    $dst = Join-Path $ProjectPath $file

    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] $file (not found in template)" -ForegroundColor DarkGray
        $SkippedCount++
        continue
    }

    $exists = Test-Path $dst
    $action = if ($exists) { "UPD " } else { "NEW" }
    $color  = if ($exists) { "Yellow" } else { "Green" }

    Write-Host "  [$action] $file" -ForegroundColor $color

    if (-not $DryRun) {
        Copy-Item $src $dst -Force
    }
    $CopiedCount++
}

# Folders
foreach ($folder in $FoldersToCopy) {
    $src = Join-Path $TemplatePath $folder
    $dst = Join-Path $ProjectPath $folder

    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] $folder/ (not found in template)" -ForegroundColor DarkGray
        $SkippedCount++
        continue
    }

    $exists = Test-Path $dst
    $action = if ($exists) { "UPD " } else { "NEW" }
    $color  = if ($exists) { "Yellow" } else { "Green" }

    Write-Host "  [$action] $folder/" -ForegroundColor $color

    if (-not $DryRun) {
        if ($exists) { Remove-Item $dst -Recurse -Force }
        Copy-Item $src $dst -Recurse -Force
    }
    $CopiedCount++
}

# Write the workbench version to the project
$versionDst = Join-Path $ProjectPath ".workbench-version"
Write-Host "  [VERSION] .workbench-version → $WorkbenchVersion" -ForegroundColor Cyan
if (-not $DryRun) {
    Set-Content $versionDst $WorkbenchVersion -Encoding UTF8
}

# --- Create Memory Bank if absent ---
$MemoryBankPath = Join-Path $ProjectPath "memory-bank"
if (-not (Test-Path $MemoryBankPath)) {
    Write-Host ""
    Write-Host "Creating Memory Bank (7 files)..." -ForegroundColor Cyan
    $mbFiles = @("projectBrief.md", "productContext.md", "systemPatterns.md",
                 "techContext.md", "activeContext.md", "progress.md", "decisionLog.md")
    if (-not $DryRun) {
        New-Item -Path $MemoryBankPath -ItemType Directory | Out-Null
        foreach ($f in $mbFiles) {
            New-Item -Path $MemoryBankPath -Name $f -ItemType File | Out-Null
            Write-Host "  [NEW] memory-bank/$f" -ForegroundColor Green
        }
    } else {
        foreach ($f in $mbFiles) {
            Write-Host "  [NEW] memory-bank/$f" -ForegroundColor Green
        }
    }
}

# --- Create docs/qa/ if absent ---
$DocsQaPath = Join-Path $ProjectPath "docs\qa"
if (-not (Test-Path $DocsQaPath)) {
    Write-Host ""
    Write-Host "Creating docs/qa/..." -ForegroundColor Cyan
    if (-not $DryRun) {
        New-Item -Path $DocsQaPath -ItemType Directory -Force | Out-Null
        New-Item -Path $DocsQaPath -Name ".gitkeep" -ItemType File | Out-Null
        Write-Host "  [NEW] docs/qa/.gitkeep" -ForegroundColor Green
    } else {
        Write-Host "  [NEW] docs/qa/.gitkeep" -ForegroundColor Green
    }
}

# --- Summary ---
Write-Host ""
Write-Host ("=" * 60)
if ($DryRun) {
    Write-Host "  DRY RUN COMPLETE — No modifications made" -ForegroundColor Yellow
} else {
    Write-Host "  DEPLOYMENT COMPLETE" -ForegroundColor Green
    Write-Host "  Workbench v$WorkbenchVersion deployed to: $ProjectPath" -ForegroundColor Green
}
Write-Host ("=" * 60)
Write-Host ""

if (-not $DryRun) {
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Fill in memory-bank/projectBrief.md with the project vision"
    Write-Host "  2. Open the project in VS Code: code '$ProjectPath'"
    Write-Host "  3. Commit the workbench files:"
    Write-Host "     cd '$ProjectPath'"
    Write-Host "     git add ."
    Write-Host "     git commit -m `"chore(workbench): deploy agentic-agile-workbench v$WorkbenchVersion`""
    Write-Host ""
    if ($Update) {
        Write-Host "  4. [UPDATE] Review changes with: git diff" -ForegroundColor Yellow
        Write-Host "     Consult the workbench CHANGELOG.md for details of the changes" -ForegroundColor Yellow
    }
}
