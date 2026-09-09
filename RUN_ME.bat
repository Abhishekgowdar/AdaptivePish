@echo off
REM AdaptivePhish - Windows Launcher (Double-click this!)

echo ===============================================
echo    AdaptivePhish - AI Phishing Detector
echo ===============================================
echo.

cd /d "%~dp0"

python run.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Press any key to exit...
    pause >nul
)
