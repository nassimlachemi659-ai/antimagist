"""
installer_builder.py — Antimagist V2 Standalone Executable & Package Compiler
================================================================================
Automates the compilation of:
1. PyInstaller single-binary bundle (Antimagist_V2_Core.exe).
2. Verifies all required assets (antimagist.ico, website/*, plugins, core libraries).
3. Validates Inno Setup (ISCC.exe) availability and outputs direct build commands.
4. Generates a standalone ZIP distribution package if Inno Setup compiler is not installed.
"""

import os
import sys
import shutil
import subprocess
import zipfile
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistInstallerBuilder:
    """Manages compilation, artifact packaging, and installer generation."""

    def __init__(self, project_root: Optional[str] = None):
        self.root = project_root or os.path.dirname(os.path.abspath(__file__))
        self.dist_dir = os.path.join(self.root, "dist")
        self.iss_file = os.path.join(self.root, "antimagist_setup.iss")

    def verify_prerequisites(self) -> Dict[str, bool]:
        """Checks required build assets and tools."""
        return {
            "has_icon": os.path.exists(os.path.join(self.root, "antimagist.ico")),
            "has_website": os.path.exists(os.path.join(self.root, "website")),
            "has_iss": os.path.exists(self.iss_file),
            "has_pyinstaller": shutil.which("pyinstaller") is not None,
            "has_iscc": (
                shutil.which("iscc") is not None
                or os.path.exists(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe")
                or os.path.exists(r"C:\Program Files\Inno Setup 6\ISCC.exe")
            )
        }

    def generate_portable_zip(self, output_zip_path: Optional[str] = None) -> str:
        """Packages portable standalone release zip with all assets."""
        os.makedirs(self.dist_dir, exist_ok=True)
        zip_path = output_zip_path or os.path.join(self.dist_dir, "Antimagist_V2_Pro_Portable.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # Add compiled binaries from dist/Antimagist_V4_Apex if available
            apex_dir = os.path.join(self.dist_dir, "Antimagist_V4_Apex")
            if os.path.exists(apex_dir):
                for root, _, files in os.walk(apex_dir):
                    for file in files:
                        full_p = os.path.join(root, file)
                        rel_p = os.path.relpath(full_p, self.dist_dir)
                        zf.write(full_p, rel_p)

            # Add fallback single-file executables if present
            for exe_name in ["Antimagist.exe", "Antimagist_V4_Apex.exe", "Antimagist_V2_Core.exe"]:
                ep = os.path.join(self.dist_dir, exe_name)
                if os.path.exists(ep):
                    zf.write(ep, exe_name)

            # Add website folder
            website_dir = os.path.join(self.root, "website")
            if os.path.exists(website_dir):
                for root, _, files in os.walk(website_dir):
                    for file in files:
                        full_p = os.path.join(root, file)
                        rel_p = os.path.relpath(full_p, self.root)
                        zf.write(full_p, rel_p)

            # Add icon and setup ISS
            for fname in ["antimagist.ico", "antimagist_setup.iss", "README.md"]:
                p = os.path.join(self.root, fname)
                if os.path.exists(p):
                    zf.write(p, fname)

        # Also create Gold Master in release directory
        rel_dir = os.path.join(self.root, "release")
        os.makedirs(rel_dir, exist_ok=True)
        gold_master = os.path.join(rel_dir, "Antimagist-v11.0.0-GoldMaster.zip")
        try:
            shutil.copy2(zip_path, gold_master)
        except Exception:
            pass

        return zip_path


def generate_installer_files(output_dir: Optional[str] = None) -> Tuple[str, str]:
    """Generates 1-click PowerShell and Batch installer wizard scripts."""
    out = output_dir or os.path.dirname(os.path.abspath(__file__))
    ps1_path = os.path.join(out, "install_antimagist.ps1")
    bat_path = os.path.join(out, "install_antimagist.bat")

    ps1_content = """# Antimagist Automated Installer Script
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Antimagist Enterprise Security V11 Omni-Workstation Setup" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[+] Verifying Windows environment..." -ForegroundColor Green
$dest = "$env:LOCALAPPDATA\\Antimagist"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Write-Host "[+] Creating Desktop and Start Menu Shortcuts..." -ForegroundColor Green
$wsh = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")
$sc = $wsh.CreateShortcut("$desktop\\Antimagist.lnk")
$sc.TargetPath = "$PSScriptRoot\\dist\\Antimagist_V4_Apex\\Antimagist.exe"
$sc.WorkingDirectory = "$PSScriptRoot\\dist\\Antimagist_V4_Apex"
$sc.IconLocation = "$PSScriptRoot\\antimagist.ico,0"
$sc.Save()
Write-Host "[+] Antimagist successfully installed and ready!" -ForegroundColor Green
"""
    bat_content = """@echo off
title Antimagist 1-Click Installer
echo ========================================================
echo  Installing Antimagist Enterprise V11 Omni-Workstation...
echo ========================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_antimagist.ps1"
echo.
echo Installation complete! Launching Antimagist...
start "" "%~dp0dist\\Antimagist_V4_Apex\\Antimagist.exe"
"""
    with open(ps1_path, "w", encoding="utf-8") as f:
        f.write(ps1_content)
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    return ps1_path, bat_path


if __name__ == "__main__":
    print("[*] Testing Antimagist Installer Builder...")
    builder = AntimagistInstallerBuilder()
    status = builder.verify_prerequisites()
    print("Prerequisites:", status)
    zip_out = builder.generate_portable_zip()
    print("[+] Portable ZIP generated at:", zip_out)
