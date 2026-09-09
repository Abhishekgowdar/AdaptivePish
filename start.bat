@echo off
echo ===============================================
echo Starting AdaptivePhish System
echo ===============================================
echo.

echo [1/2] Starting Backend Server...
echo.
start cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo [2/2] Opening Frontend in Browser...
echo.
start frontend\index.html

echo.
echo ===============================================
echo AdaptivePhish is now running!
echo ===============================================
echo.
echo Backend: http://localhost:5000
echo Frontend: Opened in your default browser
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /F /FI "WINDOWTITLE eq *python app.py*" 2>nul
echo Done!
