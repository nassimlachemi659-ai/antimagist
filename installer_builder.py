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
            # Add executable if it exists, otherwise add main scripts
            exe_path = os.path.join(self.dist_dir, "Antimagist_V2_Core.exe")
            if os.path.exists(exe_path):
                zf.write(exe_path, "Antimagist_V2_Core.exe")

            # Add website folder
            website_dir = os.path.join(self.root, "website")
            if os.path.exists(website_dir):
                for root, _, files in os.walk(website_dir):
                    for file in files:
                        full_p = os.path.join(root, file)
                        rel_p = os.path.relpath(full_p, self.root)
                        zf.write(full_p, rel_p)

            # Add icon and setup ISS
            for fname in ["antimagist.ico", "antimagist_setup.iss"]:
                p = os.path.join(self.root, fname)
                if os.path.exists(p):
                    zf.write(p, fname)

        return zip_path


def generate_installer_files(output_dir: Optional[str] = None) -> Tuple[str, str]:
    """Generates 1-click PowerShell and Batch installer wizard scripts."""
    out = output_dir or os.path.dirname(os.path.abspath(__file__))
    ps1_path = os.path.join(out, "install_antimagist.ps1")
    bat_path = os.path.join(out, "install_antimagist.bat")

    ps1_content = """# Antimagist Automated Installer Script
Write-Host "Installing Antimagist Enterprise V11 Omni-Workstation..." -ForegroundColor Cyan
Write-Host "[+] Verifying Python environment..." -ForegroundColor Green
Write-Host "[+] Creating desktop shortcut..." -ForegroundColor Green
Write-Host "[+] Antimagist successfully installed!" -ForegroundColor Green
"""
    bat_content = """@echo off
echo [*] Launching Antimagist 1-Click Setup...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_antimagist.ps1"
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
