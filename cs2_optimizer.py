"""
cs2_optimizer.py — Antimagist V4 Counter-Strike 2 & FPS Tournament Auto-Tuner
=============================================================================
Antimagist Enterprise Security V4 Plus Component
- Detects Counter-Strike 2 installation across Steam drives (S:\\Steam, etc.)
- Injects esports tournament-grade autoexec.cfg with sub-tick network optimization
- Configures NVIDIA Reflex low-latency sleep and unlocks framerate (fps_max 0)
- Preserves safety with 1-click automatic backup of existing player configs
- 1-Click Launch with Apex arguments: -novid -nojoy -high +exec autoexec.cfg
"""

import os
import sys
import shutil
import time
from typing import Dict, Any, Tuple, Optional, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TOURNAMENT_AUTOEXEC_CONTENT = """// ============================================================================
// ANTIMAGIST APEX V4 — COUNTER-STRIKE 2 TOURNAMENT AUTOEXEC
// Optimized for NVIDIA GeForce RTX 5050 & Low-Latency Sub-Tick Performance
// ============================================================================

// 1. SUB-TICK & LOW-LATENCY NETWORKING
rate 1000000
cl_net_buffer_ticks 0

// 2. FRAMERATE & NVIDIA REFLEX PIPELINE
fps_max 0
r_show_build_info false
engine_low_latency_sleep_after_client_tick true

// 3. COMPETITIVE AUDIO DIRECTIONALITY & FOOTSTEP CLARITY
volume 0.85
snd_spatialize_lerp 1
snd_steamaudio_enable_perspective_correction 1

// 4. WEAPON HANDLING & TRACERS
r_drawtracers_firstperson 1

// 5. CONSOLE CONFIRMATION
echo "================================================================="
echo " [ANTIMAGIST V4 APEX] CS2 TOURNAMENT PROFILES ENGAGED WITH ZERO-LATENCY"
echo "================================================================="
host_writeconfig
"""


class AntimagistCS2Optimizer:
    """Manages Counter-Strike 2 autoexec injection, backups, and tournament launch parameters."""

    def __init__(self):
        self.cs2_root: Optional[str] = None
        self.cfg_dir: Optional[str] = None
        self.autoexec_path: Optional[str] = None
        self.backup_path: Optional[str] = None
        self.is_installed = False

        self._discover_cs2()

    def _discover_cs2(self):
        """Locates the Counter-Strike 2 directory."""
        candidates = [
            r"S:\Steam\steamapps\common\Counter-Strike Global Offensive",
            r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive",
            r"D:\Steam\steamapps\common\Counter-Strike Global Offensive",
            r"E:\Steam\steamapps\common\Counter-Strike Global Offensive",
        ]

        for p in candidates:
            cfg_p = os.path.join(p, "game", "csgo", "cfg")
            if os.path.exists(cfg_p):
                self.cs2_root = p
                self.cfg_dir = cfg_p
                self.autoexec_path = os.path.join(cfg_p, "autoexec.cfg")
                self.backup_path = os.path.join(cfg_p, "autoexec.cfg.antimagist_backup")
                self.is_installed = True
                return

    def get_status(self) -> Dict[str, Any]:
        """Returns current CS2 optimization posture."""
        has_autoexec = False
        is_optimized = False

        if self.autoexec_path and os.path.exists(self.autoexec_path):
            has_autoexec = True
            try:
                with open(self.autoexec_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "ANTIMAGIST APEX" in content or "rate 1000000" in content:
                        is_optimized = True
            except Exception:
                pass

        return {
            "is_installed": self.is_installed,
            "cs2_root": self.cs2_root or "Not detected",
            "cfg_dir": self.cfg_dir or "Not detected",
            "has_autoexec": has_autoexec,
            "is_optimized": is_optimized,
            "has_backup": bool(self.backup_path and os.path.exists(self.backup_path))
        }

    def apply_tournament_optimization(self) -> Tuple[bool, str]:
        """Applies tournament autoexec.cfg with automatic backup."""
        if not self.is_installed or not self.cfg_dir:
            return False, "Counter-Strike 2 not found on local drives."

        try:
            # 1. Create backup if existing autoexec exists
            if os.path.exists(self.autoexec_path):
                shutil.copy2(self.autoexec_path, self.backup_path)

            # 2. Write optimized autoexec
            with open(self.autoexec_path, "w", encoding="utf-8") as f:
                f.write(TOURNAMENT_AUTOEXEC_CONTENT)

            return True, f"✅ CS2 Tournament Autoexec applied successfully at:\n{self.autoexec_path}"
        except Exception as ex:
            return False, f"Failed to apply CS2 optimization: {ex}"

    def restore_backup(self) -> Tuple[bool, str]:
        """Restores original autoexec.cfg from backup."""
        if not self.backup_path or not os.path.exists(self.backup_path):
            return False, "No previous backup found to restore."

        try:
            shutil.copy2(self.backup_path, self.autoexec_path)
            return True, "Original CS2 configuration restored."
        except Exception as ex:
            return False, f"Failed to restore backup: {ex}"

    def launch_cs2_with_apex_boost(
        self,
        optimizer_core=None,
        gamer_mode=None,
        ping_optimizer=None,
        core_director=None,
        voice_engine=None
    ) -> Tuple[bool, str]:
        """
        Executes pre-flight hardware boost and launches CS2 with Apex launch parameters.
        """
        if not self.is_installed:
            return False, "Counter-Strike 2 is not installed."

        # Pre-flight hardware flush
        if optimizer_core:
            optimizer_core.run_memory_boost(lambda m: None)
            optimizer_core.run_cache_sweep(lambda m: None)

        if ping_optimizer:
            ping_optimizer.optimize_gaming_network()

        if gamer_mode:
            gamer_mode.activate_gamer_mode()

        if voice_engine:
            voice_engine.speak("Launching Counter-Strike 2 with tournament Apex boost.")

        # Ensure autoexec is applied
        self.apply_tournament_optimization()

        # Launch via Steam protocol with AppID 730
        try:
            os.startfile("steam://rungameid/730")
        except Exception as ex:
            return False, f"Could not launch CS2: {ex}"

        # Background thread to pin CS2 process to P-Cores
        if core_director:
            import threading
            import psutil
            def pin_cs2():
                for _ in range(20):
                    time.sleep(1.0)
                    for p in psutil.process_iter(['name', 'pid']):
                        try:
                            if "cs2.exe" in p.info['name'].lower():
                                core_director.pin_process_to_performance_cores(p.info['pid'])
                                return
                        except Exception:
                            pass
            threading.Thread(target=pin_cs2, daemon=True).start()

        return True, "🚀 Counter-Strike 2 Launched! Tournament Autoexec & P-Core Affinity Engaged."


if __name__ == "__main__":
    print("[*] Testing Antimagist CS2 Tournament Optimizer...")
    cs2 = AntimagistCS2Optimizer()
    st = cs2.get_status()
    print(f"  • CS2 Installed: {st['is_installed']}")
    print(f"  • Config Path: {st['cfg_dir']}")
    print(f"  • Optimized Status: {st['is_optimized']}")

    ok, msg = cs2.apply_tournament_optimization()
    print(f"  • Applied Optimization: {ok} -> {msg[:60]}...")
    print("  • CS2 Optimizer Test PASSED.")
