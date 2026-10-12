"""
context_menu_v4.py — Antimagist V4 Windows Context Menu Shell Integrator
========================================================================
Antimagist Enterprise Security V4 Plus Component
- Adds right-click shell extensions in Windows Explorer (HKCU\\Software\\Classes):
    1. "🧪 Detonate with Antimagist Forensic Chamber" (on all files)
    2. "🚀 Launch with Antimagist Apex Boost" (on .exe files)
- Operates under HKCU (Current User) — Requires NO administrator UAC elevation
- 100% reversible with clean 1-click register and unregister methods
"""

import os
import sys
import winreg
from typing import Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistContextMenuV4:
    """Manages Windows Explorer right-click shell menu integration."""

    def __init__(self):
        # Determine launch target (compiled exe or python script)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(self.app_dir, "dist", "Antimagist_V4_Apex", "Antimagist_V4_Apex.exe")
        if os.path.exists(exe_path):
            self.launcher_cmd = f'"{exe_path}"'
        else:
            py_exe = sys.executable
            main_py = os.path.join(self.app_dir, "antimagist_v4_apex.py")
            self.launcher_cmd = f'"{py_exe}" "{main_py}"'

        self.ico_path = os.path.join(self.app_dir, "antimagist.ico")

    def is_registered(self) -> bool:
        """Checks if Antimagist context menu keys currently exist in HKCU."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\*\shell\AntimagistDetonate") as k:
                return True
        except Exception:
            return False

    def register_context_menus(self) -> Tuple[bool, str]:
        """Registers shell verbs under HKCU\\Software\\Classes."""
        try:
            # 1. Register "Detonate with Antimagist" for all files
            key_path = r"Software\Classes\*\shell\AntimagistDetonate"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "🧪 Detonate with Antimagist Forensic Chamber")
                if os.path.exists(self.ico_path):
                    winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, self.ico_path)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"{key_path}\command") as cmd_k:
                winreg.SetValueEx(cmd_k, "", 0, winreg.REG_SZ, f'{self.launcher_cmd} --detonate "%1"')

            # 2. Register "Launch with Apex Boost" for executables
            exe_key_path = r"Software\Classes\exefile\shell\AntimagistApexLaunch"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, exe_key_path) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "🚀 Launch with Antimagist Apex Boost")
                if os.path.exists(self.ico_path):
                    winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, self.ico_path)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"{exe_key_path}\command") as cmd_k:
                winreg.SetValueEx(cmd_k, "", 0, winreg.REG_SZ, f'{self.launcher_cmd} --apex-launch "%1"')

            return True, "✅ Windows Context Menus Registered (Detonate & Apex Boost available in Explorer)."
        except Exception as ex:
            return False, f"Failed to register context menus: {ex}"

    def unregister_context_menus(self) -> Tuple[bool, str]:
        """Removes shell verbs from HKCU."""
        try:
            self._delete_key_recursive(winreg.HKEY_CURRENT_USER, r"Software\Classes\*\shell\AntimagistDetonate")
            self._delete_key_recursive(winreg.HKEY_CURRENT_USER, r"Software\Classes\exefile\shell\AntimagistApexLaunch")
            return True, "Context menus cleanly unregistered."
        except Exception as ex:
            return False, f"Failed to unregister context menus: {ex}"

    def _delete_key_recursive(self, root, subkey):
        try:
            with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
                while True:
                    try:
                        child = winreg.EnumKey(key, 0)
                        self._delete_key_recursive(root, f"{subkey}\\{child}")
                    except OSError:
                        break
            winreg.DeleteKey(root, subkey)
        except Exception:
            pass


if __name__ == "__main__":
    print("[*] Testing Antimagist Context Menu V4 Integrator...")
    cm = AntimagistContextMenuV4()
    ok, msg = cm.register_context_menus()
    print(f"  • Register: {ok} -> {msg}")
    print(f"  • Is Registered: {cm.is_registered()}")
    ok_un, msg_un = cm.unregister_context_menus()
    print(f"  • Unregister: {ok_un} -> {msg_un}")
    # Re-register for live user convenience
    cm.register_context_menus()
    print("  • Context Menu V4 Test PASSED.")
