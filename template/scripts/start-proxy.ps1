# le workbench Proxy — Script de demarrage
# Usage : .\scripts\start-proxy.ps1
# Prerequis : venv/ cree avec pip install -r requirements.txt

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$VenvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
if (-not (Test-Path $VenvActivate)) {
    Write-Host "ERREUR : Environnement virtuel Python introuvable." -ForegroundColor Red
    Write-Host "Creez-le avec :" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

& $VenvActivate

$ProxyScript = Join-Path $ProjectRoot "proxy.py"
if (-not (Test-Path $ProxyScript)) {
    Write-Host "ERREUR : proxy.py introuvable dans $ProjectRoot" -ForegroundColor Red
    Write-Host "Verifiez que le deploiement de l'etabli est complet." -ForegroundColor Yellow
    exit 1
}

Write-Host "Demarrage le workbench Proxy v2.1.0..." -ForegroundColor Green
Write-Host "URL : http://localhost:8000/v1" -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arreter." -ForegroundColor DarkGray
python proxy.py
