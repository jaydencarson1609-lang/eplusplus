@echo off
REM Install E++ on Windows

set ROOT=%~dp0
set ROOT=%ROOT:~0,-1%
echo Installing E++ from %ROOT%

REM Quick test
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python is not installed!
    echo Download it free from: https://www.python.org/downloads/
    echo During install, check "Add python.exe to PATH"
    pause
    exit /b 1
)

echo.
echo Python found!
echo.
echo To run E++ scripts:
echo   python epp.py example.epp
echo.
echo Open this folder in VS Code, then press Ctrl+Shift+B to run a .epp file.
echo.
echo Done!
pause
