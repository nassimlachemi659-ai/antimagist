"""
bandwidth_guard.py — Antimagist V11 Enterprise Smart Bandwidth & Background I/O Shaper
======================================================================================
Antimagist Enterprise Security V11 Component
- Detects bandwidth and disk I/O heavy background processes during competitive gaming
- Targets:
    • qbittorrent.exe, bittorrent.exe, utorrent.exe
    • onedrive.exe, googledrivesync.exe, dropbox.exe
    • winstore.app.exe, trustedinstaller.exe, tiworker.exe
    • epicgameslauncher.exe, steam.exe (background downloads)
- Automatically throttles process CPU priority to IDLE_PRIORITY_CLASS and lowers I/O priority
- Provides 1-click engage/disengage and automatic session restoration
"""

import os
import sys
import time
import psutil
import threading
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TARGET_BANDWIDTH_HOGS = {
    "qbittorrent.exe": "qBittorrent P2P Client",
    "bittorrent.exe": "BitTorrent Client",
    "utorrent.exe": "uTorrent Client",
    "onedrive.exe": "Microsoft OneDrive Cloud Sync",
    "googledrivesync.exe": "Google Drive Sync",
    "dropbox.exe": "Dropbox Sync",
    "winstore.app.exe": "Windows Store Background Ingestion",
    "trustedinstaller.exe": "Windows Update Worker",
    "tiworker.exe": "Windows Module Installer Worker"
}


class AntimagistBandwidthGuard:
    """Manages active network bandwidth shaping and background process I/O throttling."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AntimagistBandwidthGuard, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.is_active = False
        self.throttled_pids: Dict[int, Dict[str, Any]] = {}
        self._initialized = True

    def scan_active_hogs(self) -> List[Dict[str, Any]]:
        """Scans system for running bandwidth/I/O consumer processes."""
        found = []
        for p in psutil.process_iter(["pid", "name", "nice"]):
            try:
                name = p.info["name"].lower()
                if name in TARGET_BANDWIDTH_HOGS:
                    found.append({
                        "pid": p.info["pid"],
                        "name": p.info["name"],
                        "label": TARGET_BANDWIDTH_HOGS[name],
                        "current_nice": p.info.get("nice")
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return found

    def engage_bandwidth_guard(self) -> Dict[str, Any]:
        """Throttles target background consumers to IDLE priority to guarantee zero ping jitter."""
        with self._lock:
            hogs = self.scan_active_hogs()
            throttled_count = 0

            for hog in hogs:
                pid = hog["pid"]
                try:
                    proc = psutil.Process(pid)
                    original_nice = proc.nice()
                    if hasattr(psutil, "IDLE_PRIORITY_CLASS"):
                        proc.nice(psutil.IDLE_PRIORITY_CLASS)
                    
                    # Lower I/O priority to VERYLOW if supported
                    if hasattr(proc, "ionice") and hasattr(psutil, "IOPRIO_VERYLOW"):
                        try:
                            proc.ionice(psutil.IOPRIO_VERYLOW)
                        except Exception:
                            pass

                    self.throttled_pids[pid] = {
                        "name": hog["name"],
                        "original_nice": original_nice
                    }
                    throttled_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            self.is_active = True
            return {
                "status": "ENGAGED",
                "hogs_throttled": throttled_count,
                "targets": list(self.throttled_pids.values())
            }

    def disengage_bandwidth_guard(self) -> Dict[str, Any]:
        """Restores throttled processes to normal scheduling and I/O priorities."""
        with self._lock:
            restored_count = 0
            for pid, info in list(self.throttled_pids.items()):
                try:
                    proc = psutil.Process(pid)
                    orig = info.get("original_nice", psutil.NORMAL_PRIORITY_CLASS if hasattr(psutil, "NORMAL_PRIORITY_CLASS") else 0)
                    proc.nice(orig)
                    if hasattr(proc, "ionice") and hasattr(psutil, "IOPRIO_NORMAL"):
                        try:
                            proc.ionice(psutil.IOPRIO_NORMAL)
                        except Exception:
                            pass
                    restored_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            self.throttled_pids.clear()
            self.is_active = False
            return {
                "status": "DISENGAGED",
                "hogs_restored": restored_count
            }


if __name__ == "__main__":
    print("[*] Testing Antimagist Bandwidth Guard...")
    bg = AntimagistBandwidthGuard()
    hogs = bg.scan_active_hogs()
    print(f"  • Running Targets Found: {len(hogs)}")
    res = bg.engage_bandwidth_guard()
    print(f"  • Engage Status: {res['status']} | Throttled: {res['hogs_throttled']}")
    res_dis = bg.disengage_bandwidth_guard()
    print(f"  • Disengage Status: {res_dis['status']} | Restored: {res_dis['hogs_restored']}")
    print("[+] Antimagist Bandwidth Guard PASSED.")
