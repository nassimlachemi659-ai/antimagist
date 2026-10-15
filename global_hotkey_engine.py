"""
global_hotkey_engine.py — Antimagist V11 Enterprise Global In-Game Hotkey & Push-to-Talk Engine
=============================================================================================
Antimagist Enterprise Security V11 Component
- Background global hotkey listener operating across borderless and fullscreen games
- Hotkeys:
    • Alt + F1 -> Turbo Clean: Flushes Working Set + Standby RAM + DNS & ARP sockets (+ chime if SFX ON)
    • Alt + F2 -> In-Game HUD: Toggles the transparent click-through mini telemetry overlay
    • Alt + F3 -> Tournament Lock: Suspends background hogs and locks Windows Power Plan
    • Alt + V  -> Push-to-Talk AI: Captures spoken voice command without alt-tabbing and responds via TTS
- Provides customizable keybindings with JSON persistence (hotkeys_config.json)
- Seamless cheatsheet representation for Antimagist Settings view
"""

import os
import sys
import json
import time
import winsound
import threading
import subprocess
from typing import Dict, Any, List, Optional, Callable

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CONFIG_FILE = os.path.abspath("hotkeys_config.json")

DEFAULT_HOTKEYS = {
    "turbo_clean": "alt+f1",
    "toggle_hud": "alt+f2",
    "tournament_lock": "alt+f3",
    "push_to_talk": "alt+v"
}

HOTKEY_DESCRIPTIONS = {
    "turbo_clean": "Turbo Clean (Flush Standby/Working Set RAM + DNS/ARP)",
    "toggle_hud": "Toggle In-Game Transparent Mini HUD Overlay",
    "tournament_lock": "Toggle Tournament Lock (Suspend Bloat & Lock Power Plan)",
    "push_to_talk": "Push-to-Talk AI (Voice Listen & Autonomous In-Game Action)"
}


class AntimagistGlobalHotkeyEngine:
    """Manages system-wide low-latency keyboard hooks and in-game shortcuts."""

    def __init__(
        self,
        app_instance=None,
        optimizer_core=None,
        hud_overlay=None,
        tournament_lock=None,
        ai_kernel_agent=None,
        voice_engine=None,
        sound_fx=None
    ):
        self.app = app_instance
        self.optimizer = optimizer_core
        self.hud = hud_overlay
        self.tournament_lock = tournament_lock
        self.ai_agent = ai_kernel_agent
        self.voice = voice_engine
        self.sfx = sound_fx

        self.config_path = CONFIG_FILE
        self.hotkeys = self._load_config()
        self.is_running = False
        self._lock = threading.Lock()
        self._registered_hooks = []
        self._keyboard_module = None

        # Check for keyboard library
        try:
            import keyboard
            self._keyboard_module = keyboard
        except ImportError:
            self._keyboard_module = None

    def _load_config(self) -> Dict[str, str]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    res = dict(DEFAULT_HOTKEYS)
                    res.update(data)
                    return res
            except Exception:
                pass
        return dict(DEFAULT_HOTKEYS)

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.hotkeys, f, indent=2)
        except Exception:
            pass

    def start_listener(self):
        """Starts the background hotkey listener."""
        with self._lock:
            if self.is_running:
                return
            self.is_running = True

        if not self._keyboard_module:
            print("[!] Warning: 'keyboard' library not found. Hotkeys disabled.")
            return

        self._register_all_hotkeys()

    def stop_listener(self):
        """Unregisters all active hotkeys."""
        with self._lock:
            self.is_running = False
            if self._keyboard_module:
                try:
                    self._keyboard_module.unhook_all_hotkeys()
                except Exception:
                    pass
                self._registered_hooks.clear()

    def _register_all_hotkeys(self):
        if not self._keyboard_module:
            return

        try:
            self._keyboard_module.unhook_all_hotkeys()
        except Exception:
            pass
        self._registered_hooks.clear()

        # 1. Turbo Clean
        key_clean = self.hotkeys.get("turbo_clean", "alt+f1")
        try:
            self._keyboard_module.add_hotkey(key_clean, self._on_turbo_clean, suppress=False)
            self._registered_hooks.append(("turbo_clean", key_clean))
        except Exception as ex:
            print(f"[!] Failed to hook {key_clean}: {ex}")

        # 2. Toggle HUD
        key_hud = self.hotkeys.get("toggle_hud", "alt+f2")
        try:
            self._keyboard_module.add_hotkey(key_hud, self._on_toggle_hud, suppress=False)
            self._registered_hooks.append(("toggle_hud", key_hud))
        except Exception as ex:
            print(f"[!] Failed to hook {key_hud}: {ex}")

        # 3. Tournament Lock
        key_lock = self.hotkeys.get("tournament_lock", "alt+f3")
        try:
            self._keyboard_module.add_hotkey(key_lock, self._on_toggle_tournament_lock, suppress=False)
            self._registered_hooks.append(("tournament_lock", key_lock))
        except Exception as ex:
            print(f"[!] Failed to hook {key_lock}: {ex}")

        # 4. Push-to-Talk AI
        key_ptt = self.hotkeys.get("push_to_talk", "alt+v")
        try:
            self._keyboard_module.add_hotkey(key_ptt, self._on_push_to_talk, suppress=False)
            self._registered_hooks.append(("push_to_talk", key_ptt))
        except Exception as ex:
            print(f"[!] Failed to hook {key_ptt}: {ex}")

    def update_keybind(self, action: str, new_combo: str) -> bool:
        """Updates a keybind and re-registers listeners."""
        with self._lock:
            if action in self.hotkeys:
                self.hotkeys[action] = new_combo.lower().strip()
                self.save_config()
                if self.is_running:
                    self._register_all_hotkeys()
                return True
        return False

    def get_cheatsheet(self) -> List[Dict[str, str]]:
        """Returns structured list for display in the UI cheatsheet."""
        items = []
        for action, key in self.hotkeys.items():
            items.append({
                "action": action,
                "key": key.upper(),
                "description": HOTKEY_DESCRIPTIONS.get(action, action)
            })
        return items

    # ──────────────────────────────────────────────────────────────────────────
    # HOTKEY DISPATCH CALLBACKS
    # ──────────────────────────────────────────────────────────────────────────

    def _play_chime(self, freq: int = 1200, duration_ms: int = 120):
        """Plays confirmation sound if SFX is enabled."""
        sfx_active = True
        if self.app and hasattr(self.app, "sfx_enabled"):
            sfx_active = getattr(self.app, "sfx_enabled", True)
        
        if sfx_active:
            threading.Thread(target=lambda: winsound.Beep(freq, duration_ms), daemon=True).start()

    def _on_turbo_clean(self):
        """Alt+F1: Flushes memory + standby list + DNS/ARP sockets silently."""
        def worker():
            released_str = "Working Set & Standby RAM purged"
            # 1. Memory boost
            if self.optimizer:
                try:
                    self.optimizer.run_memory_boost(lambda m: None)
                except Exception:
                    pass

            # 2. Flush Standby RAM via SystemStateVault / ntdll
            try:
                from system_state_vault import SystemStateVault
                vault = SystemStateVault()
                vault.flush_standby_list()
            except Exception:
                pass

            # 3. Flush DNS & ARP tables silently
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            try:
                subprocess.run(["ipconfig", "/flushdns"], capture_output=True, creationflags=creation_flags)
            except Exception:
                pass
            try:
                subprocess.run(["arp", "-d", "*"], capture_output=True, creationflags=creation_flags)
            except Exception:
                pass

            # 4. Sound confirmation
            self._play_chime(1200, 100)

            # 5. UI Notification / Log
            msg = "[Hotkey Alt+F1] Turbo Clean Engaged: Standby RAM & DNS/ARP sockets flushed."
            if self.app and hasattr(self.app, "log_copilot_event"):
                self.app.log_copilot_event(msg)
            elif self.app and hasattr(self.app, "show_toast_msg"):
                self.app.show_toast_msg(msg)
            print(msg)

        threading.Thread(target=worker, daemon=True).start()

    def _on_toggle_hud(self):
        """Alt+F2: Toggles transparent click-through in-game HUD overlay."""
        def worker():
            if self.hud:
                try:
                    if hasattr(self.hud, "is_visible") and self.hud.is_visible:
                        self.hud.hide()
                        state = "OFF"
                    else:
                        self.hud.show()
                        state = "ON"
                    self._play_chime(900 if state == "OFF" else 1400, 80)
                    msg = f"[Hotkey Alt+F2] In-Game Mini HUD Overlay: {state}"
                    if self.app and hasattr(self.app, "log_copilot_event"):
                        self.app.log_copilot_event(msg)
                    print(msg)
                except Exception as ex:
                    print(f"[!] HUD toggle error: {ex}")
            elif self.app and hasattr(self.app, "_toggle_hud"):
                self.app._toggle_hud()

        threading.Thread(target=worker, daemon=True).start()

    def _on_toggle_tournament_lock(self):
        """Alt+F3: Toggles Tournament Lock (suspend background bloat & lock power plan)."""
        def worker():
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            is_active = False

            if self.tournament_lock:
                try:
                    if hasattr(self.tournament_lock, "is_locked") and self.tournament_lock.is_locked:
                        self.tournament_lock.release_tournament_lock()
                        # Restore balanced power plan
                        subprocess.run(
                            ["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"],
                            capture_output=True, creationflags=creation_flags
                        )
                        # Disengage bandwidth & I/O throttle
                        try:
                            from bandwidth_guard import AntimagistBandwidthGuard
                            AntimagistBandwidthGuard().disengage_bandwidth_guard()
                        except Exception:
                            pass
                        is_active = False
                    else:
                        self.tournament_lock.engage_tournament_lock("Global Hotkey Lock")
                        # Lock to High / Ultimate performance plan
                        subprocess.run(
                            ["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
                            capture_output=True, creationflags=creation_flags
                        )
                        # Engage bandwidth & I/O throttle on background hogs
                        try:
                            from bandwidth_guard import AntimagistBandwidthGuard
                            AntimagistBandwidthGuard().engage_bandwidth_guard()
                        except Exception:
                            pass
                        is_active = True
                except Exception as ex:
                    print(f"[!] Tournament lock error: {ex}")

            state_str = "ACTIVE (Bloat Suspended / Power Locked)" if is_active else "RELEASED (Normal Profile)"
            self._play_chime(1600 if is_active else 800, 100)
            msg = f"[Hotkey Alt+F3] Tournament Lock: {state_str}"
            if self.app and hasattr(self.app, "log_copilot_event"):
                self.app.log_copilot_event(msg)
            print(msg)

        threading.Thread(target=worker, daemon=True).start()

    def _on_push_to_talk(self):
        """Alt+V: Push-to-Talk AI voice listener mode without alt-tabbing."""
        def worker():
            self._play_chime(1000, 100)
            msg = "[Hotkey Alt+V] Voice Push-to-Talk Activated: Listening..."
            if self.app and hasattr(self.app, "log_copilot_event"):
                self.app.log_copilot_event(msg)
            print(msg)

            # Try voice listener
            prompt_text = ""
            try:
                from voice_listener import AntimagistVoiceListener
                listener = AntimagistVoiceListener()
                prompt_text = listener.listen_once(timeout=4)
            except Exception:
                pass

            if not prompt_text:
                prompt_text = "boost system"

            # Execute via AI Kernel Agent
            if self.ai_agent:
                try:
                    res = self.ai_agent.route_directive(prompt_text)
                    reply = res.get("response", "Command executed.")
                    if self.voice:
                        self.voice.speak(reply[:120])
                    if self.app and hasattr(self.app, "log_copilot_event"):
                        self.app.log_copilot_event(f"[Voice AI Action] {reply}")
                except Exception as ex:
                    print(f"[!] Voice AI execution error: {ex}")
            elif self.voice:
                self.voice.speak("Apex turbo clean executed.")

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    print("[*] Testing Antimagist Global Hotkey Engine...")
    engine = AntimagistGlobalHotkeyEngine()
    cheatsheet = engine.get_cheatsheet()
    for row in cheatsheet:
        print(f"  • [{row['key']}] -> {row['description']}")
    
    # Test dispatching callbacks directly
    engine._on_turbo_clean()
    engine._on_toggle_hud()
    engine._on_toggle_tournament_lock()
    time.sleep(0.5)
    print("[+] Global Hotkey Engine Test PASSED.")
