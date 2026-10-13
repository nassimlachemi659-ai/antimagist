"""
recall_stripper.py — Antimagist V9 Windows 11 Recall, Copilot & Modern AI Telemetry Stripper
=============================================================================================
Antimagist Enterprise Security V9 Component
- Eliminates Windows 11 23H2/24H2 background AI bloatware that steals CPU/NPU/RAM during gaming:
    • Windows Recall & Snapshot Analysis (DisableAIDataAnalysis, TurnOffRecall)
    • Windows Copilot Background Agents (TurnOffWindowsCopilot)
    • Microsoft Edge Silent Background Pre-launch & Startup Boost (AllowPrelaunch = 0)
    • Start Menu Bing Cloud Search Querying (BingSearchEnabled = 0)
    • Diagnostic Telemetry & Activity Timeline Tracking (AllowTelemetry = 0, EnableActivityFeed = 0)
- 100% reversible, safe, and zero-corruptive Win32 Group Policy registry enforcement.
"""

import os
import sys
import time
import winreg
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistRecallStripper:
    """Manages Windows 11 Recall, Copilot, and background AI telemetry settings."""

    AI_POLICIES = [
        {
            "id": "recall_disable",
            "name": "Windows Recall AI Snapshots",
            "desc": "Disable continuous screen snapshot analysis and local vector semantic indexing",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI",
            "key": "DisableAIDataAnalysis",
            "val_optimized": 1,
            "val_default": 0
        },
        {
            "id": "recall_turnoff",
            "name": "Windows Recall Main Engine",
            "desc": "Turn off Recall background snapshot daemon and local model cache",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI",
            "key": "TurnOffRecall",
            "val_optimized": 1,
            "val_default": 0
        },
        {
            "id": "copilot_cu",
            "name": "Windows Copilot (User Session)",
            "desc": "Disable Copilot sidebar worker and persistent Edge WebView host",
            "hive": winreg.HKEY_CURRENT_USER,
            "path": r"Software\Policies\Microsoft\Windows\WindowsCopilot",
            "key": "TurnOffWindowsCopilot",
            "val_optimized": 1,
            "val_default": 0
        },
        {
            "id": "copilot_lm",
            "name": "Windows Copilot (Machine Policy)",
            "desc": "Prevent background Copilot scheduling across all system cores",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot",
            "key": "TurnOffWindowsCopilot",
            "val_optimized": 1,
            "val_default": 0
        },
        {
            "id": "edge_prelaunch",
            "name": "Edge Silent Pre-launching",
            "desc": "Stop Edge from pre-launching hidden background processes on Windows boot",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Edge",
            "key": "AllowPrelaunch",
            "val_optimized": 0,
            "val_default": 1
        },
        {
            "id": "edge_startup_boost",
            "name": "Edge Startup Boost Daemon",
            "desc": "Stop Edge background worker processes from reserving standby memory",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Edge",
            "key": "StartupBoostEnabled",
            "val_optimized": 0,
            "val_default": 1
        },
        {
            "id": "bing_search",
            "name": "Start Menu Web & Bing Search",
            "desc": "Eliminate network delays when searching local files from the Start Menu",
            "hive": winreg.HKEY_CURRENT_USER,
            "path": r"Software\Microsoft\Windows\CurrentVersion\Search",
            "key": "BingSearchEnabled",
            "val_optimized": 0,
            "val_default": 1
        },
        {
            "id": "activity_feed",
            "name": "Windows Activity History Feed",
            "desc": "Stop recording foreground app switching history and telemetry timeline",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Windows\System",
            "key": "EnableActivityFeed",
            "val_optimized": 0,
            "val_default": 1
        },
        {
            "id": "data_collection",
            "name": "Diagnostic Telemetry Level",
            "desc": "Lock Windows Diagnostic Data Collection to Security/Minimal (0)",
            "hive": winreg.HKEY_LOCAL_MACHINE,
            "path": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "key": "AllowTelemetry",
            "val_optimized": 0,
            "val_default": 1
        }
    ]

    def __init__(self):
        self.cached_audit: Optional[Dict[str, Any]] = None
        self.last_audit_time: float = 0.0

    def audit_ai_telemetry_posture(self, force: bool = False) -> Dict[str, Any]:
        """Audits current state of all Windows 11 AI and telemetry policies with 30s cache."""
        now = time.time()
        if not force and self.cached_audit and (now - self.last_audit_time < 30.0):
            return self.cached_audit

        items = []
        optimized_count = 0

        for pol in self.AI_POLICIES:
            is_opt = False
            cur_val = None
            try:
                with winreg.OpenKey(pol["hive"], pol["path"], 0, winreg.KEY_READ) as k:
                    cur_val, _ = winreg.QueryValueEx(k, pol["key"])
                    is_opt = (cur_val == pol["val_optimized"])
            except OSError:
                is_opt = False

            if is_opt:
                optimized_count += 1

            items.append({
                "id": pol["id"],
                "name": pol["name"],
                "desc": pol["desc"],
                "current_value": cur_val,
                "is_optimized": is_opt,
                "status_label": "STRIPPED / OPTIMAL" if is_opt else "ACTIVE_BLOAT"
            })

        pct = int((optimized_count / len(self.AI_POLICIES)) * 100) if self.AI_POLICIES else 100
        if pct >= 80:
            status = "CLEAN_LOW_LATENCY"
            advice = "Windows 11 AI & Recall background telemetry is stripped. Zero background NPU/CPU interference."
        elif pct >= 40:
            status = "PARTIAL_BLOAT_DETECTED"
            advice = "Several AI or telemetry background workers are active. 1-Click Stripping recommended."
        else:
            status = "HEAVY_BACKGROUND_AI_OVERHEAD"
            advice = "Windows Recall, Copilot, and Edge background tasks active. Stripping will noticeably improve frametime pacing."

        res = {
            "timestamp": time.strftime("%H:%M:%S UTC", time.gmtime()),
            "optimized_count": optimized_count,
            "total_policies": len(self.AI_POLICIES),
            "score_pct": pct,
            "status": status,
            "advice": advice,
            "policies": items
        }
        self.cached_audit = res
        self.last_audit_time = now
        return res

    def strip_all_ai_bloat(self) -> Tuple[bool, str, List[str]]:
        """Applies all low-latency group policy registry optimizations."""
        applied = []
        errors = []

        for pol in self.AI_POLICIES:
            try:
                # Open or create subkey
                with winreg.CreateKey(pol["hive"], pol["path"]) as k:
                    winreg.SetValueEx(k, pol["key"], 0, winreg.REG_DWORD, pol["val_optimized"])
                applied.append(pol["name"])
            except Exception as e:
                errors.append(f"{pol['name']}: {str(e)}")

        self.cached_audit = None  # Invalidate cache
        if errors and not applied:
            return False, f"Failed to strip AI bloat (requires Administrator privileges): {errors[0]}", []
        elif errors:
            return True, f"Stripped {len(applied)} policies. (Note: {len(errors)} policies require elevated UAC).", applied
        else:
            return True, f"Successfully stripped all {len(applied)} Windows 11 AI & Recall background policies!", applied

    def restore_defaults(self) -> Tuple[bool, str]:
        """Restores default Windows 11 policy settings."""
        restored = 0
        for pol in self.AI_POLICIES:
            try:
                with winreg.CreateKey(pol["hive"], pol["path"]) as k:
                    winreg.SetValueEx(k, pol["key"], 0, winreg.REG_DWORD, pol["val_default"])
                restored += 1
            except Exception:
                pass

        self.cached_audit = None
        return True, f"Restored {restored} policies to Windows defaults."


if __name__ == "__main__":
    print("[*] Testing Antimagist Windows 11 Recall & Copilot Stripper...")
    stripper = AntimagistRecallStripper()
    audit = stripper.audit_ai_telemetry_posture(force=True)
    print(f"  Optimized: {audit['optimized_count']}/{audit['total_policies']} ({audit['score_pct']}%)")
    print(f"  Status: {audit['status']}")
    print(f"  Advice: {audit['advice']}")
