@echo off
title Antimagist - Push to GitHub
cd /d "C:\Users\nst\.gemini\antigravity\scratch"
echo =====================================================================
echo   Antimagist V5 Singularity - Pushing to GitHub Repository
echo   Target: https://github.com/nassimlachemi659-ai/antimagist
echo =====================================================================
echo.
git push -u origin main
echo.
echo =====================================================================
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Code and README successfully pushed to GitHub!
) else (
    echo [NOTICE] If prompted above, complete your sign-in in browser or token.
)
echo =====================================================================
pause
