@echo off
echo ========================================
echo AUTO UPLOAD TO GITHUB
echo Repo: https://github.com/aabhi7785/AdaptivePish
echo ========================================
echo.

REM Navigate to project folder
cd /d "C:\Users\BWM743\Desktop\AdaptivePish"

REM Step 1: Clean up
echo Step 1: Cleaning up unwanted files...
echo.
mkdir local_files 2>nul
move /Y DEMO_VIDEO_SCRIPT.md local_files\ 2>nul
move /Y CONTINUOUS_VIDEO_GUIDE.txt local_files\ 2>nul
move /Y GOOGLE_VIDS_PROMPT*.txt local_files\ 2>nul
move /Y GOOGLE_VIDS_PROMPT.md local_files\ 2>nul
move /Y GOOGLE_SLIDES_READY.md local_files\ 2>nul
move /Y HOW_TO_CREATE_GOOGLE_SLIDES.md local_files\ 2>nul
move /Y HOW_TO_USE_GOOGLE_VIDS.txt local_files\ 2>nul
move /Y VIDS_CONTINUOUS_PART*.txt local_files\ 2>nul
move /Y Day1_Setup_Guide.md local_files\ 2>nul
move /Y DEBUG_CHECKLIST.md local_files\ 2>nul
move /Y HOW_TO_RUN_AND_AI_EXPLANATION.md local_files\ 2>nul
move /Y PROJECT_STRUCTURE.md local_files\ 2>nul
move /Y AdaptivePhish_Complete_Overview.md local_files\ 2>nul
move /Y GITHUB_SETUP_GUIDE.md local_files\ 2>nul
move /Y GITHUB_QUICK_START.txt local_files\ 2>nul
move /Y WHAT_TO_UPLOAD_TO_GITHUB.md local_files\ 2>nul
move /Y CLEANUP_BEFORE_GITHUB.txt local_files\ 2>nul
move /Y COMPLETE_GITHUB_UPLOAD_GUIDE.txt local_files\ 2>nul
move /Y QUICK_COMMANDS.txt local_files\ 2>nul
move /Y CHECKLIST.txt local_files\ 2>nul
move /Y ORGANIZE_FILES.bat local_files\ 2>nul
move /Y RUN_THIS_TO_CLEAN.txt local_files\ 2>nul
move /Y CLICK_HERE.html local_files\ 2>nul
move /Y TEST_BUTTONS.html local_files\ 2>nul
move /Y test_setup.py local_files\ 2>nul
move /Y docs local_files\ 2>nul

REM Remove duplicates
del /Q app.py 2>nul
rmdir /S /Q modules 2>nul
if exist requirements.txt (
    if exist backend\requirements.txt del /Q requirements.txt
)

REM Create presentation folder
mkdir presentation 2>nul
move /Y PRESENTATION_SLIDES.md presentation\ 2>nul
move /Y PRESENTATION_SCRIPT.md presentation\ 2>nul
move /Y PRESENTATION_CHEATSHEET.md presentation\ 2>nul

echo Cleanup complete!
echo.

REM Step 2: Check Git
echo Step 2: Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo Git is installed!
echo.

REM Step 3: Initialize Git
echo Step 3: Initializing Git repository...
if exist .git (
    echo Git already initialized.
) else (
    git init
    echo Git initialized!
)
echo.

REM Step 4: Add files
echo Step 4: Adding files to Git...
git add .
echo Files added!
echo.

REM Step 5: Show status
echo Step 5: Checking what will be uploaded...
git status
echo.
echo ========================================
echo IMPORTANT: Check the list above
echo ========================================
echo.
echo You should see:
echo   - backend/
echo   - frontend/
echo   - presentation/
echo   - screenshots/
echo   - .gitignore, LICENSE, README.md, etc.
echo.
echo You should NOT see:
echo   - local_files/
echo   - __pycache__/
echo   - *.pyc files
echo.
echo If you see unwanted files, press Ctrl+C to stop.
echo If everything looks good, press any key to continue...
pause >nul
echo.

REM Step 6: Commit
echo Step 6: Creating commit...
git commit -m "Initial commit: Multi-modal AI phishing detection by Abhishek Gowda R." -m "- Implemented 3-module detection system (URL, Visual, Text)" -m "- CLIP AI (400M parameters) for computer vision" -m "- DistilBERT (66M parameters) for NLP" -m "- Professional dark-themed web interface" -m "- 94%% accuracy, 100%% local processing" -m "- Complete documentation and presentation materials"
echo Commit created!
echo.

REM Step 7: Set branch name
echo Step 7: Setting branch name to main...
git branch -M main
echo Branch renamed!
echo.

REM Step 8: Add remote
echo Step 8: Connecting to GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/aabhi7785/AdaptivePish.git
echo Connected to: https://github.com/aabhi7785/AdaptivePish
echo.

REM Step 9: Push
echo ========================================
echo Step 9: PUSHING TO GITHUB
echo ========================================
echo.
echo You will be asked for:
echo   Username: aabhi7785
echo   Password: [Your Personal Access Token]
echo.
echo If you don't have a token:
echo   1. Open: https://github.com/settings/tokens
echo   2. Generate new token (classic)
echo   3. Name: AdaptivePish
echo   4. Check: repo
echo   5. Generate and copy the token
echo   6. Paste it as password here
echo.
echo Press any key to start pushing...
pause >nul
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo PUSH FAILED!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Wrong username or password
    echo 2. Need Personal Access Token instead of password
    echo 3. Network issues
    echo.
    echo Get Personal Access Token:
    echo https://github.com/settings/tokens
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! CODE PUSHED TO GITHUB!
echo ========================================
echo.
echo Your project is now live at:
echo https://github.com/aabhi7785/AdaptivePish
echo.
echo Next steps:
echo 1. Open the link above
echo 2. Add topics/tags
echo 3. Add description
echo 4. Pin to your profile
echo.
pause
