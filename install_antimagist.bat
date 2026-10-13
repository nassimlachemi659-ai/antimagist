@echo off
title Antimagist 1-Click Installer
echo ========================================================
echo  Installing Antimagist Enterprise V11 Omni-Workstation...
echo ========================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_antimagist.ps1"
echo.
echo Installation complete! Launching Antimagist...
start "" "%~dp0dist\Antimagist_V4_Apex\Antimagist.exe"
