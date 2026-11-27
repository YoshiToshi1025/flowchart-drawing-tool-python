@echo off
cd /d "%~dp0"

REM Check Python
python --version
if errorlevel 1 (
    echo Please install Python first.
    pause
    exit /b 1
)

REM Create virtual environment
if not exist "env\Scripts\python.exe" (
    python -m venv env
    if errorlevel 1 goto error
)

REM Install required packages
env\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error

REM Start application
env\Scripts\python.exe flowchart_tool.py
if errorlevel 1 goto error
exit /b 0

:error
echo An error occurred.
pause
exit /b 1