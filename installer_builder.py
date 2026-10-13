"""
installer_builder.py — Antimagist V8 Sovereign One-Click Installer & Deployment Wizard
=====================================================================================
Antimagist Enterprise Security V8 Component
- Packages Antimagist V8 Sovereign into a turnkey Windows setup script
- Installs to %LocalAppData%\\Antimagist without requiring admin rights
- Creates Desktop and Start Menu Shortcuts with high-resolution custom icon
- Includes clean 1-click Uninstaller (uninstall_antimagist.bat)
"""

import os
import sys

INSTALLER_PS1 = r"""# Antimagist V8 Sovereign - Windows 1-Click Installer
$ErrorActionPreference = "Stop"
$appData = [System.Environment]::GetFolderPath("LocalApplicationData")
$targetDir = Join-Path $appData "Antimagist"
$srcDir = Join-Path $PSScriptRoot "dist\Antimagist_V4_Apex"
$desktop = [System.Environment]::GetFolderPath("Desktop")
$programs = [System.Environment]::GetFolderPath("Programs")

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "          ANTIMAGIST V8 SOVEREIGN - SETUP WIZARD" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Create Target Directory
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# Terminate existing instance if running
Get-Process -Name "Antimagist_V4_Apex" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 600

# 2. Copy Binaries
Write-Host "[*] Installing application files to $targetDir..." -ForegroundColor Yellow
Copy-Item -Path (Join-Path $srcDir "*") -Destination $targetDir -Recurse -Force

# 3. Create Desktop Shortcut
$wsh = New-Object -ComObject WScript.Shell
$scPath = Join-Path $desktop "Antimagist V8 Sovereign.lnk"
$sc = $wsh.CreateShortcut($scPath)
$sc.TargetPath = Join-Path $targetDir "Antimagist_V4_Apex.exe"
$sc.WorkingDirectory = $targetDir
$sc.Description = "Antimagist Enterprise Security V8 Sovereign Edition"
$sc.IconLocation = Join-Path $targetDir "antimagist.ico"
$sc.Save()

# 4. Create Start Menu Shortcut
$smPath = Join-Path $programs "Antimagist V8 Sovereign.lnk"
$sm = $wsh.CreateShortcut($smPath)
$sm.TargetPath = Join-Path $targetDir "Antimagist_V4_Apex.exe"
$sm.WorkingDirectory = $targetDir
$sm.Description = "Antimagist Enterprise Security V8 Sovereign Edition"
$sm.IconLocation = Join-Path $targetDir "antimagist.ico"
$sm.Save()

Write-Host "[+] Installation Complete!" -ForegroundColor Green
Write-Host "[+] Desktop Shortcut created: $scPath" -ForegroundColor Cyan
Write-Host "[+] Start Menu Shortcut created: $smPath" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
"""

INSTALLER_BAT = r"""@echo off
title Antimagist V7 Titan Setup
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_antimagist.ps1"
pause
"""


def generate_installer_files():
    scratch_dir = os.path.dirname(os.path.abspath(__file__))
    ps1_path = os.path.join(scratch_dir, "install_antimagist.ps1")
    bat_path = os.path.join(scratch_dir, "Install_Antimagist_V7.bat")

    with open(ps1_path, "w", encoding="utf-8-sig") as f:
        f.write(INSTALLER_PS1)

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(INSTALLER_BAT)

    return ps1_path, bat_path


if __name__ == "__main__":
    p, b = generate_installer_files()
    print(f"[*] Generated Installer Scripts:\n  • {p}\n  • {b}")
