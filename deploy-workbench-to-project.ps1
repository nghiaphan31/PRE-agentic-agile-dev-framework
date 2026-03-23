<#
.SYNOPSIS
    agentic-agile-workbench — Déploie l'établi vers un projet applicatif.

.DESCRIPTION
    Copie les fichiers template/ de l'établi vers un projet cible.
    En mode -Update, met à jour un projet existant depuis une nouvelle version de l'établi.
    Écrit .workbench-version dans le projet cible pour traçabilité.

    Ce script est le script CANONIQUE de l'établi. Il doit être exécuté depuis
    la racine du dépôt agentic-agile-workbench.

    Un script de rappel (update-workbench.ps1) est déployé dans scripts/ de chaque
    projet applicatif. Ce script de rappel redirige vers ce script canonique pour
    toute mise à jour ultérieure.

.PARAMETER ProjectPath
    Chemin absolu vers le dossier racine du projet applicatif cible.

.PARAMETER Update
    Mode mise à jour : met à jour un projet existant depuis la nouvelle version de l'établi.

.PARAMETER DryRun
    Simule le déploiement sans rien copier. Affiche ce qui serait fait.

.EXAMPLE
    # Déploiement initial sur un nouveau projet
    # Structure canonique : $env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\
    #   ├── agentic-agile-workbench\   (l'établi — ce dépôt)
    #   └── PROJECTS\mon-nouveau-projet\   (le projet applicatif)
    $Projet = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\mon-nouveau-projet"
    .\deploy-workbench-to-project.ps1 -ProjectPath $Projet

.EXAMPLE
    # Mise à jour d'un projet existant après une nouvelle version de l'établi
    $Projet = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\mon-projet"
    .\deploy-workbench-to-project.ps1 -ProjectPath $Projet -Update

.EXAMPLE
    # Simulation sans modification
    $Projet = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\mon-projet"
    .\deploy-workbench-to-project.ps1 -ProjectPath $Projet -DryRun
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,

    [switch]$Update = $false,
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

# --- Chemins ---
# Ce script vit à la racine de l'établi. template/ est un sous-dossier direct.
$WorkbenchRoot = $PSScriptRoot
$TemplatePath  = Join-Path $WorkbenchRoot "template"
$WorkbenchVersion = (Get-Content (Join-Path $WorkbenchRoot "VERSION") -Raw).Trim()

# Fichiers et dossiers à copier depuis template/
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
Write-Host "  agentic-agile-workbench — Déploiement v$WorkbenchVersion" -ForegroundColor Cyan
if ($DryRun) { Write-Host "  MODE SIMULATION (aucune modification)" -ForegroundColor Yellow }
if ($Update)  { Write-Host "  MODE MISE À JOUR" -ForegroundColor Yellow }
Write-Host ("=" * 60)
Write-Host ""

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERREUR : Le dossier projet '$ProjectPath' n'existe pas." -ForegroundColor Red
    Write-Host "Créez d'abord le dossier et initialisez Git :"
    Write-Host "  git init '$ProjectPath'"
    exit 1
}

# Vérifier si Git est initialisé dans le projet
if (-not (Test-Path (Join-Path $ProjectPath ".git"))) {
    Write-Host "AVERTISSEMENT : Aucun dépôt Git détecté dans '$ProjectPath'." -ForegroundColor Yellow
    Write-Host "Il est fortement recommandé d'initialiser Git avant le déploiement :"
    Write-Host "  cd '$ProjectPath' && git init"
    $confirm = Read-Host "Continuer quand même ? (o/N)"
    if ($confirm -ne "o" -and $confirm -ne "O") { exit 0 }
}

# En mode Update, vérifier la version actuelle du projet
if ($Update) {
    $ProjectVersionFile = Join-Path $ProjectPath ".workbench-version"
    if (Test-Path $ProjectVersionFile) {
        $CurrentVersion = (Get-Content $ProjectVersionFile -Raw).Trim()
        Write-Host "Version actuelle dans le projet : $CurrentVersion"
        Write-Host "Nouvelle version de l'établi    : $WorkbenchVersion"
        Write-Host ""
        if ($CurrentVersion -eq $WorkbenchVersion) {
            Write-Host "Le projet est déjà à jour (v$WorkbenchVersion)." -ForegroundColor Green
            exit 0
        }
    } else {
        Write-Host "Aucun fichier .workbench-version trouvé — déploiement initial." -ForegroundColor Yellow
    }
}

# --- Copie des fichiers ---
$CopiedCount = 0
$SkippedCount = 0

Write-Host "Fichiers à déployer :"
Write-Host ""

# Fichiers individuels
foreach ($file in $FilesToCopy) {
    $src = Join-Path $TemplatePath $file
    $dst = Join-Path $ProjectPath $file

    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] $file (absent du template)" -ForegroundColor DarkGray
        $SkippedCount++
        continue
    }

    $exists = Test-Path $dst
    $action = if ($exists) { "MAJ " } else { "NOUVEAU" }
    $color  = if ($exists) { "Yellow" } else { "Green" }

    Write-Host "  [$action] $file" -ForegroundColor $color

    if (-not $DryRun) {
        Copy-Item $src $dst -Force
    }
    $CopiedCount++
}

# Dossiers
foreach ($folder in $FoldersToCopy) {
    $src = Join-Path $TemplatePath $folder
    $dst = Join-Path $ProjectPath $folder

    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] $folder/ (absent du template)" -ForegroundColor DarkGray
        $SkippedCount++
        continue
    }

    $exists = Test-Path $dst
    $action = if ($exists) { "MAJ " } else { "NOUVEAU" }
    $color  = if ($exists) { "Yellow" } else { "Green" }

    Write-Host "  [$action] $folder/" -ForegroundColor $color

    if (-not $DryRun) {
        if ($exists) { Remove-Item $dst -Recurse -Force }
        Copy-Item $src $dst -Recurse -Force
    }
    $CopiedCount++
}

# Écrire la version de l'établi dans le projet
$versionDst = Join-Path $ProjectPath ".workbench-version"
Write-Host "  [VERSION] .workbench-version → $WorkbenchVersion" -ForegroundColor Cyan
if (-not $DryRun) {
    Set-Content $versionDst $WorkbenchVersion -Encoding UTF8
}

# --- Créer la Memory Bank si absente ---
$MemoryBankPath = Join-Path $ProjectPath "memory-bank"
if (-not (Test-Path $MemoryBankPath)) {
    Write-Host ""
    Write-Host "Création de la Memory Bank (7 fichiers)..." -ForegroundColor Cyan
    $mbFiles = @("projectBrief.md", "productContext.md", "systemPatterns.md",
                 "techContext.md", "activeContext.md", "progress.md", "decisionLog.md")
    if (-not $DryRun) {
        New-Item -Path $MemoryBankPath -ItemType Directory | Out-Null
        foreach ($f in $mbFiles) {
            New-Item -Path $MemoryBankPath -Name $f -ItemType File | Out-Null
            Write-Host "  [NOUVEAU] memory-bank/$f" -ForegroundColor Green
        }
    } else {
        foreach ($f in $mbFiles) {
            Write-Host "  [NOUVEAU] memory-bank/$f" -ForegroundColor Green
        }
    }
}

# --- Créer docs/qa/ si absent ---
$DocsQaPath = Join-Path $ProjectPath "docs\qa"
if (-not (Test-Path $DocsQaPath)) {
    Write-Host ""
    Write-Host "Création de docs/qa/..." -ForegroundColor Cyan
    if (-not $DryRun) {
        New-Item -Path $DocsQaPath -ItemType Directory -Force | Out-Null
        New-Item -Path $DocsQaPath -Name ".gitkeep" -ItemType File | Out-Null
        Write-Host "  [NOUVEAU] docs/qa/.gitkeep" -ForegroundColor Green
    } else {
        Write-Host "  [NOUVEAU] docs/qa/.gitkeep" -ForegroundColor Green
    }
}

# --- Résumé ---
Write-Host ""
Write-Host ("=" * 60)
if ($DryRun) {
    Write-Host "  SIMULATION TERMINÉE — Aucune modification effectuée" -ForegroundColor Yellow
} else {
    Write-Host "  DÉPLOIEMENT TERMINÉ" -ForegroundColor Green
    Write-Host "  Établi v$WorkbenchVersion déployé dans : $ProjectPath" -ForegroundColor Green
}
Write-Host ("=" * 60)
Write-Host ""

if (-not $DryRun) {
    Write-Host "Prochaines étapes :" -ForegroundColor Cyan
    Write-Host "  1. Remplir memory-bank/projectBrief.md avec la vision du projet"
    Write-Host "  2. Ouvrir le projet dans VS Code : code '$ProjectPath'"
    Write-Host "  3. Commiter les fichiers de l'établi :"
    Write-Host "     cd '$ProjectPath'"
    Write-Host "     git add ."
    Write-Host "     git commit -m `"chore(workbench): déploiement établi agentic-agile-workbench v$WorkbenchVersion`""
    Write-Host ""
    if ($Update) {
        Write-Host "  4. [MISE À JOUR] Vérifier les changements avec : git diff" -ForegroundColor Yellow
        Write-Host "     Consulter CHANGELOG.md de l'établi pour les détails des changements" -ForegroundColor Yellow
    }
}
