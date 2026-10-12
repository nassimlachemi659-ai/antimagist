r"""
context_menu.py — Windows Explorer Right-Click Integration ("Scan with Antimagist")
==================================================================================
Antimagist Enterprise Security V3 Component
- Registers user-level shell extension in HKCU\Software\Classes\*\shell\AntimagistScan
- Adds '🛡️ Scan with Antimagist Enterprise' to Windows right-click context menu
- Enables seamless 1-click scanning for any executable, archive, or script
- Requires zero administrator privileges (operates inside HKCU)
"""

import os
import sys
import winreg
from typing import Tuple

REG_SHELL_KEY = r"Software\Classes\*\shell\AntimagistScan"

class AntimagistContextMenu:
    def __init__(self, exe_path: str = "", icon_path: str = ""):
        self.exe_path = os.path.abspath(exe_path or sys.executable)
        self.icon_path = os.path.abspath(icon_path or "antimagist.ico")

    def is_installed(self) -> bool:
        """Checks if the context menu entry exists in the user registry."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_SHELL_KEY, 0, winreg.KEY_READ):
                return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def install_context_menu(self) -> Tuple[bool, str]:
        """Registers the context menu item in HKCU."""
        try:
            # 1. Create main key
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_SHELL_KEY) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Scan with Antimagist Enterprise")
                if os.path.exists(self.icon_path):
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f'"{self.icon_path}"')
                elif os.path.exists(self.exe_path):
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f'"{self.exe_path}",0')

            # 2. Create command subkey
            cmd_key_path = f"{REG_SHELL_KEY}\\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as cmd_key:
                cmd_val = f'"{self.exe_path}" "%1"'
                winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, cmd_val)

            return True, "Successfully registered 'Scan with Antimagist Enterprise' in Windows Explorer."
        except Exception as ex:
            return False, f"Failed to register context menu: {ex}"

    def uninstall_context_menu(self) -> Tuple[bool, str]:
        """Removes the context menu entry from HKCU."""
        try:
            # Delete command subkey first
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{REG_SHELL_KEY}\\command")
            except FileNotFoundError:
                pass

            # Delete main shell key
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_SHELL_KEY)
            except FileNotFoundError:
                pass

            return True, "Successfully removed context menu entry from Windows Explorer."
        except Exception as ex:
            return False, f"Failed to remove context menu: {ex}"
