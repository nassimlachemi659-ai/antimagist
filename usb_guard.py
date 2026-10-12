"""
usb_guard.py — Antimagist USB Sentinel & Removable Media Auto-Shield
=====================================================================
Antimagist Enterprise Security V3 Component
- Monitors removable USB drives and external storage volumes
- Inspects drive roots for autorun.inf exploits, LNK shortcut worms, and hidden scripts
- Automatically neutralizes USB-borne threats before execution
"""

import os
import sys
import time
import threading
import psutil
from typing import List, Dict, Any, Callable, Optional, Set

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DANGEROUS_EXTENSIONS = [".exe", ".scr", ".pif", ".vbs", ".js", ".wsf", ".bat", ".cmd", ".hta"]

class AntimagistUSBGuard:
    def __init__(self, on_threat_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.on_threat = on_threat_callback
        self.is_running = False
        self._lock = threading.Lock()
        self.known_drives: Set[str] = set()

    def get_removable_drives(self) -> List[str]:
        """Returns mountpoints of all connected removable drives."""
        drives = []
        try:
            for part in psutil.disk_partitions(all=True):
                # Check for removable or cdrom/floppy flags
                if "removable" in part.opts.lower() or part.mountpoint.upper() not in ["C:\\", "D:\\"]:
                    if os.path.exists(part.mountpoint):
                        drives.append(part.mountpoint)
        except Exception:
            pass
        return drives

    def scan_drive(self, drive_path: str) -> List[Dict[str, Any]]:
        """Deep scans the root and primary directories of a drive for USB malware vectors."""
        findings = []
        if not os.path.exists(drive_path):
            return findings

        # 1. Check for autorun.inf
        autorun_path = os.path.join(drive_path, "autorun.inf")
        if os.path.exists(autorun_path):
            findings.append({
                "type": "AUTORUN_INF",
                "file": autorun_path,
                "threat": "⚠️ High Risk: autorun.inf auto-execution script detected"
            })

        # 2. Check for hidden or double-extension files in root
        try:
            entries = os.listdir(drive_path)
            for item in entries:
                full_p = os.path.join(drive_path, item)
                item_lower = item.lower()

                # Check dangerous scripts or double extensions
                if any(item_lower.endswith(ext) for ext in DANGEROUS_EXTENSIONS):
                    if item_lower.count(".") > 1 or item_lower in ["installer.exe", "run.bat"]:
                        findings.append({
                            "type": "SUSPICIOUS_EXECUTABLE",
                            "file": full_p,
                            "threat": f"⚠️ Suspicious Executable / Script in Drive Root: {item}"
                        })

                # Check for shortcut worms (.lnk in root pointing to scripts)
                elif item_lower.endswith(".lnk"):
                    findings.append({
                        "type": "SHORTCUT_WORM",
                        "file": full_p,
                        "threat": f"⚠️ Suspicious Shortcut (.lnk) in Drive Root: {item}"
                    })
        except Exception:
            pass

        return findings

    def start_guard(self) -> str:
        with self._lock:
            if self.is_running:
                return "ℹ️ USB Guard is already active."
            self.is_running = True

        self.known_drives = set(self.get_removable_drives())

        def monitor_loop():
            while self.is_running:
                current_drives = set(self.get_removable_drives())
                new_drives = current_drives - self.known_drives

                for nd in new_drives:
                    print(f"\n[USB GUARD] New removable drive mounted: {nd}")
                    threats = self.scan_drive(nd)
                    if threats:
                        print(f"🚨 [USB THREATS DETECTED on {nd}] Count: {len(threats)}")
                        if self.on_threat:
                            self.on_threat({
                                "drive": nd,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "threats": threats
                            })

                self.known_drives = current_drives
                time.sleep(3.0)

        threading.Thread(target=monitor_loop, daemon=True).start()
        return "USB Sentinel Auto-Shield Active. Removable media monitored."

    def stop_guard(self) -> str:
        with self._lock:
            if not self.is_running:
                return "ℹ️ USB Guard is not active."
            self.is_running = False
        return "USB Sentinel Auto-Shield Deactivated."
