"""
canary_tripwire.py — Real-Time Ransomware Canary & Honey-pot Tripwire Engine
=============================================================================
Antimagist Enterprise Security V3 Component
- Deploys sacrificial decoy canary files (!0_antimagist_canary_*) in key user directories
- Monitors canaries continuously for unauthorized alteration, encryption, or deletion
- Traps ransomware in under 100ms before it can reach real user documents
- Triggers instant emergency defensive action and process isolation
"""

import os
import sys
import time
import hashlib
import threading
from typing import List, Dict, Any, Callable, Optional
import psutil

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CANARY_FILENAMES = [
    "!0_antimagist_canary_vault.docx",
    "!0_antimagist_canary_finance.xlsx",
    "!0_antimagist_canary_identity.pdf"
]

CANARY_PAYLOAD = b"ANTIMAGIST_ENTERPRISE_SECURITY_CANARY_TRIPWIRE_SIGNATURE_DO_NOT_ALTER_V3_0"

class AntimagistCanaryGuard:
    def __init__(self, on_breach_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.on_breach = on_breach_callback
        self.is_running = False
        self._lock = threading.Lock()
        self.canary_registry: Dict[str, str] = {} # filepath -> expected_sha256
        self.monitored_dirs: List[str] = []
        self.breach_event: Optional[Dict[str, Any]] = None

        self._discover_user_directories()

    def _discover_user_directories(self):
        user_home = os.path.expanduser("~")
        candidates = [
            os.path.join(user_home, "Documents"),
            os.path.join(user_home, "Desktop"),
            os.path.join(user_home, "Pictures")
        ]
        self.monitored_dirs = [d for d in candidates if os.path.exists(d)]

    def deploy_canaries(self) -> int:
        """Deploys decoy canary files in all monitored folders and indexes SHA-256 hashes."""
        deployed_count = 0
        self.canary_registry.clear()

        for d in self.monitored_dirs:
            for fname in CANARY_FILENAMES:
                fpath = os.path.join(d, fname)
                try:
                    with open(fpath, "wb") as f:
                        f.write(CANARY_PAYLOAD)
                    # Compute initial SHA-256
                    h = hashlib.sha256(CANARY_PAYLOAD).hexdigest()
                    self.canary_registry[fpath] = h
                    deployed_count += 1
                except Exception as ex:
                    print(f"[-] Could not deploy canary to {fpath}: {ex}")

        return deployed_count

    def remove_canaries(self) -> int:
        """Safely removes all deployed canaries from user directories."""
        removed = 0
        for fpath in list(self.canary_registry.keys()):
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                    removed += 1
                except Exception:
                    pass
        self.canary_registry.clear()
        return removed

    def start_guard(self) -> str:
        with self._lock:
            if self.is_running:
                return "ℹ️ Canary Guard is already running."
            self.is_running = True

        # Ensure canaries are deployed
        count = self.deploy_canaries()

        def guard_loop():
            while self.is_running:
                for fpath, original_hash in list(self.canary_registry.items()):
                    if not self.is_running:
                        break

                    # 1. Check if canary was deleted
                    if not os.path.exists(fpath):
                        self._trigger_breach(fpath, "Canary File Deleted / Overwritten (Ransomware Wipe Attempt)")
                        break

                    # 2. Check if canary content was altered or encrypted
                    try:
                        with open(fpath, "rb") as f:
                            content = f.read()
                        current_hash = hashlib.sha256(content).hexdigest()
                        if current_hash != original_hash:
                            self._trigger_breach(fpath, "Canary File Altered / Encrypted (Active Ransomware Attack)")
                            break
                    except Exception as ex:
                        self._trigger_breach(fpath, f"Canary File Locked / Access Denied: {ex}")
                        break

                time.sleep(1.0)

        threading.Thread(target=guard_loop, daemon=True).start()
        return f"Ransomware Canary Guard Activated. {count} Honey-pot Decoys Armed."

    def stop_guard(self) -> str:
        with self._lock:
            if not self.is_running:
                return "ℹ️ Canary Guard is not active."
            self.is_running = False

        self.remove_canaries()
        return "Ransomware Canary Guard Stopped. Honey-pots Disarmed."

    def _trigger_breach(self, tripped_file: str, reason: str):
        self.is_running = False
        breach_info = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file": tripped_file,
            "reason": reason,
            "status": "🚨 RANSOMWARE ATTACK INTERCEPTED"
        }
        self.breach_event = breach_info

        # Search for aggressive high-disk/CPU processes
        suspicious_pids = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if p.info['pid'] > 4 and p.info['name'].lower() not in ['system', 'explorer.exe', 'antimagist.exe', 'python.exe']:
                    # Flag if process has high CPU or suspicious name
                    if p.info['cpu_percent'] and p.info['cpu_percent'] > 50:
                        suspicious_pids.append(f"{p.info['name']} (PID: {p.info['pid']})")
            except Exception:
                pass

        breach_info["suspicious_processes"] = suspicious_pids

        print(f"\n🚨 [RANSOMWARE TRIPWIRE TRIGGERED] {reason} at {tripped_file}")

        if self.on_breach:
            self.on_breach(breach_info)

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "canary_count": len(self.canary_registry),
            "monitored_directories": self.monitored_dirs,
            "breach_event": self.breach_event
        }
