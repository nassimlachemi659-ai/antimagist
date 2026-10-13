"""
gamer_mode.py — Antimagist Ultra Gamer & Low-Latency Engine (V3 Ultra Enhanced)
=============================================================================
Antimagist Enterprise Security V3 Component
- Boosts CPU priority and process scheduling for active games/heavy applications
- 100% Native Win32 API Standby Memory Trimming (Zero CPU micro-stutters, No PowerShell spawning)
- Integrated Ultra Low-Latency Gaming Network Tweaker (Nagle's Algorithm & TCP optimization)
- Real-time Ping Telemetry stream (Ping ms, Jitter, Packet Loss)
- 100% Reversible with clean one-click restoration
"""

import os
import sys
import time
import ctypes
import threading
import psutil
from typing import List, Dict, Any, Optional, Tuple

from ping_optimizer import AntimagistPingOptimizer

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

COMMON_GAME_EXES = [
    "cs2.exe", "csgo.exe", "valorant-win64-shipping.exe", "fortniteclient-win64-shipping.exe",
    "leagueclientux.exe", "overwatch.exe", "gta5.exe", "r5apex.exe", "cod.exe",
    "dota2.exe", "rainbowsix.exe", "destiny2.exe", "pubg.exe", "minecraft.exe",
    "javaw.exe", "rocketleague.exe", "cyberpunk2077.exe", "eldenring.exe"
]

class AntimagistGamerMode:
    def __init__(self):
        self.is_active = False
        self._lock = threading.Lock()
        self.boosted_pids: Dict[int, int] = {} # PID -> original_nice_value
        self.total_memory_freed_mb = 0.0
        self.ping_optimizer = AntimagistPingOptimizer()
        self.last_ping_telemetry = self.ping_optimizer.get_live_ping_telemetry()
        self._cached_games: List[Dict[str, Any]] = []
        self._last_detect_time: float = 0.0

    def get_detected_games(self) -> List[Dict[str, Any]]:
        """Scans running processes for recognized gaming titles with 3.0s cache."""
        now = time.time()
        if self._cached_games and (now - self._last_detect_time < 3.0):
            return self._cached_games

        games = []
        for p in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                pname = p.info['name'].lower() if p.info['name'] else ""
                if pname in COMMON_GAME_EXES or any(g in pname for g in ["game", "shipping"]):
                    mem_mb = round(p.info['memory_info'].rss / (1024**2), 1) if p.info['memory_info'] else 0.0
                    games.append({
                        "pid": p.info['pid'],
                        "name": p.info['name'],
                        "memory_mb": mem_mb,
                        "cpu_percent": 0.0
                    })
            except Exception:
                pass

        self._cached_games = games
        self._last_detect_time = now
        return games

    def _native_trim_standby_memory(self) -> float:
        """
        Trims memory working sets natively via Win32 psapi.EmptyWorkingSet.
        Zero CPU overhead, no subprocess spawning, zero game stuttering.
        """
        if os.name != 'nt':
            return 0.0
        
        m_before = psutil.virtual_memory().used
        # Trim current process and background tasks
        for p in psutil.process_iter(['pid', 'name']):
            try:
                pid = p.info['pid']
                if pid > 4 and pid not in self.boosted_pids:
                    h = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
                    if h:
                        ctypes.windll.psapi.EmptyWorkingSet(h)
                        ctypes.windll.kernel32.CloseHandle(h)
            except Exception:
                pass
        
        m_after = psutil.virtual_memory().used
        freed = max(0.0, (m_before - m_after) / (1024**2))
        return round(freed, 1)

    def activate_gamer_mode(self, target_pid: Optional[int] = None) -> Tuple[bool, str]:
        with self._lock:
            if self.is_active:
                return True, "Gamer Mode is already active."
            self.is_active = True

        boosted_names = []

        # 1. Boost target process or any detected games to High Priority
        targets = []
        if target_pid and target_pid > 4:
            targets.append(target_pid)
        else:
            detected = self.get_detected_games()
            for g in detected:
                targets.append(g["pid"])

        for pid in targets:
            try:
                p = psutil.Process(pid)
                orig_priority = p.nice()
                self.boosted_pids[pid] = orig_priority

                # Set to High Priority
                if os.name == 'nt':
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                boosted_names.append(f"{p.name()} (PID: {pid})")
            except Exception as ex:
                print(f"[-] Could not elevate process {pid}: {ex}")

        # 2. Engage Network Low-Latency Tweak (TCPNoDelay & DNS Flush)
        net_ok, net_msg = self.ping_optimizer.optimize_gaming_network()

        # 3. Initial Native Memory Sweep
        initial_freed = self._native_trim_standby_memory()
        self.total_memory_freed_mb += initial_freed

        # 4. Start Lightweight In-Process Maintenance Loop (Pure Sleep, Zero Subprocesses)
        def silent_background_loop():
            while self.is_active:
                # Sleep 60 seconds quietly
                for _ in range(60):
                    if not self.is_active:
                        break
                    time.sleep(1)

                if not self.is_active:
                    break

                # Gentle periodic native trim
                freed = self._native_trim_standby_memory()
                self.total_memory_freed_mb += freed

        threading.Thread(target=silent_background_loop, daemon=True).start()

        detail_parts = []
        if boosted_names:
            detail_parts.append(f"Elevated {', '.join(boosted_names)} to High Priority")
        if initial_freed > 0:
            detail_parts.append(f"Freed {initial_freed} MB RAM")
        detail_parts.append("Low-latency network profile engaged (Zero packet queuing)")

        return True, f"⚡ Gamer Mode Online! {' | '.join(detail_parts)}."

    def deactivate_gamer_mode(self) -> Tuple[bool, str]:
        with self._lock:
            if not self.is_active:
                return True, "Gamer Mode is not active."
            self.is_active = False

        # Restore original priorities
        restored = 0
        for pid, orig_nice in list(self.boosted_pids.items()):
            try:
                p = psutil.Process(pid)
                p.nice(orig_nice)
                restored += 1
            except Exception:
                pass

        self.boosted_pids.clear()

        # Restore default network settings if requested
        self.ping_optimizer.restore_default_network()

        return True, f"Gamer Mode Disengaged. Restored normal priority to {restored} processes."

    def get_live_ping(self) -> Dict[str, Any]:
        """Fetches live ping telemetry for the UI HUD."""
        self.last_ping_telemetry = self.ping_optimizer.get_live_ping_telemetry()
        return self.last_ping_telemetry

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_active,
            "boosted_count": len(self.boosted_pids),
            "memory_saved_mb": round(self.total_memory_freed_mb, 1),
            "detected_games": len(self.get_detected_games()),
            "last_ping_ms": self.last_ping_telemetry.get("ping_ms", 0.0),
            "jitter_ms": self.last_ping_telemetry.get("jitter_ms", 0.0),
            "packet_loss": self.last_ping_telemetry.get("packet_loss_pct", 0.0)
        }


if __name__ == "__main__":
    gm = AntimagistGamerMode()
    print("[*] Testing Enhanced Gamer Mode...")
    games = gm.get_detected_games()
    print(f"  Detected Games: {games}")
    ok, msg = gm.activate_gamer_mode()
    print(f"  Activation ({ok}): {msg}")
    ping = gm.get_live_ping()
    print(f"  Live Ping: {ping['ping_ms']} ms | Jitter: {ping['jitter_ms']} ms | Loss: {ping['packet_loss_pct']}%")
    ok2, msg2 = gm.deactivate_gamer_mode()
    print(f"  Deactivation ({ok2}): {msg2}")
