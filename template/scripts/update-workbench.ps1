<#
.SYNOPSIS
    Met à jour ce projet depuis l'établi agentic-agile-workbench.

.DESCRIPTION
    Ce fichier est déployé dans les projets applicatifs par l'établi
    agentic-agile-workbench. Il sert de point d'entrée pour déclencher
    une mise à jour du projet depuis une nouvelle version de l'établi.

    Il délègue l'exécution au script canonique deploy-workbench-to-project.ps1
    situé à la racine de l'établi.

    PRÉREQUIS :
    ===========
    Le dépôt agentic-agile-workbench doit être cloné localement.
    Structure recommandée :
      $env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\
        ├── agentic-agile-workbench\   (l'établi)
        └── PROJECTS\ce-projet\        (ce projet)

.PARAMETER WorkbenchPath
    Chemin absolu vers la racine du dépôt agentic-agile-workbench.
    Par défaut : déduit depuis la structure canonique des dossiers.

.EXAMPLE
    # Mise à jour depuis l'établi (chemin déduit automatiquement)
    .\scripts\update-workbench.ps1

.EXAMPLE
    # Mise à jour avec chemin explicite vers l'établi
    .\scripts\update-workbench.ps1 -WorkbenchPath "C:\Dev\agentic-agile-workbench"

.NOTES
    Fichier déployé automatiquement par deploy-workbench-to-project.ps1 (racine de l'établi).
    Ne pas modifier ce fichier directement — modifier le script canonique dans l'établi.
#>

param(
    [string]$WorkbenchPath = ""
)

$ErrorActionPreference = "Stop"

# Chemin de ce projet (racine = parent de scripts/)
$ProjectPath = Split-Path -Parent $PSScriptRoot

# Déduire le chemin de l'établi si non fourni
if (-not $WorkbenchPath) {
    # Structure canonique : ..\agentic-agile-workbench\ est un sibling du dossier parent du projet
    $ProjectsRoot = Split-Path -Parent $ProjectPath
    $WorkbenchPath = Join-Path $ProjectsRoot "agentic-agile-workbench"
}

$CanonicalScript = Join-Path $WorkbenchPath "deploy-workbench-to-project.ps1"

Write-Host ""
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "  update-workbench.ps1 — Mise à jour depuis l'établi" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""
Write-Host "  Projet      : $ProjectPath" -ForegroundColor White
Write-Host "  Établi      : $WorkbenchPath" -ForegroundColor White
Write-Host "  Script      : deploy-workbench-to-project.ps1" -ForegroundColor White
Write-Host ""

if (-not (Test-Path $CanonicalScript)) {
    Write-Host "ERREUR : Script canonique introuvable à :" -ForegroundColor Red
    Write-Host "  $CanonicalScript" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions :" -ForegroundColor Yellow
    Write-Host "  1. Cloner l'établi : git clone https://github.com/nghiaphan31/agentic-agile-workbench.git"
    Write-Host "  2. Ou spécifier le chemin : .\scripts\update-workbench.ps1 -WorkbenchPath `"chemin\vers\etabli`""
    Write-Host ""
    exit 1
}

Write-Host "Délégation vers le script canonique..." -ForegroundColor Cyan
Write-Host ""

& $CanonicalScript -ProjectPath $ProjectPath -Update
