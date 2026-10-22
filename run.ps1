$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..."
    py -m venv venv
}

Write-Host "Installing/updating dependencies..."
& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host ""
Write-Host "Starting Security Incident Triage Tool..."
& ".\venv\Scripts\python.exe" -m src.main
