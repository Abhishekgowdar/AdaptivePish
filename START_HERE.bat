@echo off
chcp 65001 >nul 2>&1
REM Set UTF-8 encoding for emojis

echo ============================================================
echo       AdaptivePhish - AI Phishing Detector
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend Server...
echo.
echo Please wait 30-60 seconds for AI models to load...
echo.

REM Start backend in same window
cd backend
start /B python app.py
cd ..

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Try multiple times to check if backend is ready
set /a attempts=0
:check_backend
set /a attempts+=1
curl -s http://localhost:5000/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Backend is ready!
    goto open_browser
)
if %attempts% LSS 20 (
    echo Still loading... (%attempts%/20)
    timeout /t 3 /nobreak >nul
    goto check_backend
)

echo.
echo Backend may still be starting. Opening browser anyway...

:open_browser
echo.
echo [2/2] Opening Browser...
echo.

REM Open browser
start http://localhost:5000

echo.
echo ============================================================
echo     AdaptivePhish is Running!
echo ============================================================
echo.
echo Frontend:  http://localhost:5000
echo API Docs:  http://localhost:5000/docs
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Keep window open
pause
