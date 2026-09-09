@echo off
echo Stopping AdaptivePhish Backend...

REM Kill all Python processes running app.py
taskkill /F /FI "WINDOWTITLE eq *python*" /FI "MEMUSAGE gt 100000" 2>nul
taskkill /F /IM python.exe 2>nul

echo.
echo All backend processes stopped
echo.
pause
