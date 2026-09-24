@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv venv
)

echo Installing/updating dependencies...
venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo Starting Security Incident Triage Tool...
echo.
venv\Scripts\python.exe -m src.main

pause
