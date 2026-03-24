# le workbench Proxy — Startup script
# Usage: .\scripts\start-proxy.ps1
# Prerequisites: venv/ created with pip install -r requirements.txt

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$VenvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
if (-not (Test-Path $VenvActivate)) {
    Write-Host "ERROR: Python virtual environment not found." -ForegroundColor Red
    Write-Host "Create it with:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

& $VenvActivate

$ProxyScript = Join-Path $ProjectRoot "proxy.py"
if (-not (Test-Path $ProxyScript)) {
    Write-Host "ERROR: proxy.py not found in $ProjectRoot" -ForegroundColor Red
    Write-Host "Verify that the workbench deployment is complete." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting le workbench Proxy v2.1.0..." -ForegroundColor Green
Write-Host "URL: http://localhost:8000/v1" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
python proxy.py
