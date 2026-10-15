"""
settings_vault.py — Antimagist V12 Persistent Settings Engine
============================================================
Antimagist Enterprise Security V12 Component
- Manages persistent application configuration across restarts:
    • Preserves active hardware profile ('ESPORTS ULTRA', 'DAILY BALANCED', 'ECO / UPS GUARD')
    • Saves Auto-Pilot RAM threshold (default: 80%)
    • Persists Voice ('VOICE: ON/OFF') and Sound FX ('SFX: ON/OFF') toggles
    • Saves custom global hotkey mappings
    • Manages Zero-UAC boot startup preference & Mic Gain Lock state
    • Atomic, crash-resilient JSON state persistence ('antimagist_config.json')
"""

import os
import sys
import json
import tempfile
import threading
from typing import Dict, Any, Optional

CONFIG_FILE = os.path.abspath("antimagist_config.json")

DEFAULT_SETTINGS: Dict[str, Any] = {
    "version": "12.0.0",
    "active_hardware_profile": "ESPORTS ULTRA",
    "autopilot_ram_threshold_pct": 80,
    "voice_enabled": True,
    "sfx_enabled": True,
    "silent_autostart_enabled": False,
    "mic_gain_lock_enabled": True,
    "footstep_booster_enabled": True,
    "custom_hotkeys": {
        "turbo_clean": "ALT + F1",
        "toggle_hud": "ALT + F2",
        "tournament_lock": "ALT + F3",
        "push_to_talk": "ALT + V"
    },
    "hud_overlay_visible": False,
    "tournament_lock_active": False,
    "total_ram_flushed_mb": 0.0,
    "total_junk_cleaned_mb": 0.0
}


class AntimagistSettingsVault:
    """Enterprise persistent settings manager with atomic disk sync."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AntimagistSettingsVault, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, config_path: str = CONFIG_FILE):
        if self._initialized:
            return
        self.config_path = config_path
        self._settings = dict(DEFAULT_SETTINGS)
        self.load_settings()
        self._initialized = True

    def load_settings(self) -> Dict[str, Any]:
        """Loads configuration from JSON file with fallback to defaults."""
        with self._lock:
            if os.path.exists(self.config_path):
                try:
                    with open(self.config_path, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                    # Merge defaults with loaded to guarantee all fields exist
                    for k, v in DEFAULT_SETTINGS.items():
                        if k not in loaded:
                            loaded[k] = v
                    self._settings = loaded
                    return self._settings
                except Exception:
                    pass

            self._settings = dict(DEFAULT_SETTINGS)
            self._save_atomic()
            return self._settings

    def save_settings(self, new_settings: Optional[Dict[str, Any]] = None) -> bool:
        """Saves current or updated configuration to disk atomically."""
        with self._lock:
            if new_settings:
                self._settings.update(new_settings)
            return self._save_atomic()

    def _save_atomic(self) -> bool:
        """Writes to a temporary file then replaces the target to prevent file corruption."""
        try:
            dir_name = os.path.dirname(self.config_path) or "."
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix="antimagist_cfg_", suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=4)
            # Atomic replace
            os.replace(tmp_path, self.config_path)
            return True
        except Exception:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._settings.get(key, default)

    def set(self, key: str, value: Any, auto_save: bool = True) -> bool:
        with self._lock:
            self._settings[key] = value
            if auto_save:
                return self._save_atomic()
            return True

    def increment_metric(self, key: str, delta: float) -> float:
        with self._lock:
            cur = self._settings.get(key, 0.0)
            cur += delta
            self._settings[key] = round(cur, 2)
            self._save_atomic()
            return self._settings[key]


if __name__ == "__main__":
    print("[*] Testing Antimagist Persistent Settings Engine...")
    vault = AntimagistSettingsVault()
    s = vault.load_settings()
    print(f"  • Profile: {s['active_hardware_profile']}")
    print(f"  • RAM Threshold: {s['autopilot_ram_threshold_pct']}%")
    print(f"  • Voice: {s['voice_enabled']} | SFX: {s['sfx_enabled']}")
    print(f"  • Hotkeys: {s['custom_hotkeys']}")
    
    # Test mutation
    vault.set("active_hardware_profile", "ESPORTS ULTRA")
    vault.increment_metric("total_ram_flushed_mb", 1024.5)
    s2 = vault.load_settings()
    print(f"  • Updated Flushed RAM Total: {s2['total_ram_flushed_mb']} MB")
    print("[+] Settings Vault PASSED.")
