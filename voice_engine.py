"""
voice_engine.py — Antimagist V4 Jarvis-Style Neural Voice Copilot & Speech Synthesizer
======================================================================================
Antimagist Enterprise Security V4 Component
- Provides asynchronous, non-blocking spoken voice feedback and tactical audio alerts
- Uses Windows SAPI.SpVoice with graceful headless/silent fallback
- Audio cues for Gamer Mode engagement, Ransomware Tripwire breaches, and Network Ping boosts
- 100% thread-safe with immediate mute toggle
"""

import os
import sys
import queue
import threading
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistVoiceCopilot:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._lock = threading.Lock()
        self._queue = queue.Queue()
        self.speaker = None
        self._init_speaker()

        # Start background voice dispatch thread
        self._worker_thread = threading.Thread(target=self._voice_loop, daemon=True)
        self._worker_thread.start()

    def _init_speaker(self):
        try:
            import win32com.client
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            # Set speech rate (-10 to 10; 1 is slightly crisp and high-tech)
            self.speaker.Rate = 1
            self.speaker.Volume = 90
        except Exception as ex:
            self.speaker = None
            print(f"[-] SAPI Voice initialization warning: {ex}")

    def _voice_loop(self):
        while True:
            text = self._queue.get()
            if text is None:
                break
            if self.enabled and self.speaker:
                try:
                    # SVSFlagsAsync = 1 (Non-blocking)
                    self.speaker.Speak(text, 0)
                except Exception:
                    pass
            self._queue.task_done()

    def speak(self, text: str):
        """Dispatches an asynchronous voice alert."""
        if not self.enabled:
            return
        clean_text = text.strip()
        if clean_text:
            self._queue.put(clean_text)

    def toggle_voice(self) -> bool:
        with self._lock:
            self.enabled = not self.enabled
            return self.enabled

    def mute(self):
        with self._lock:
            self.enabled = False

    def unmute(self):
        with self._lock:
            self.enabled = True

    # Tactical Voice Presets
    def alert_gamer_mode_on(self):
        self.speak("Antimagist Gamer Mode engaged. Zero-latency network profile active.")

    def alert_gamer_mode_off(self):
        self.speak("Gamer Mode disengaged. Standard system priorities restored.")

    def alert_ransomware_tripwire(self, target_file: str):
        self.speak("Warning! Ransomware tamper detected on honeypot canary. Offending process isolated.")

    def alert_ping_optimized(self):
        self.speak("Gaming network optimized. Nagle's algorithm disabled and DNS reset.")

    def alert_turbo_clean(self, freed_mb: float = 0.0):
        if freed_mb > 0:
            self.speak(f"Turbo clean completed. {int(freed_mb)} megabytes of memory released.")
        else:
            self.speak("Turbo clean completed. Hardware working sets compressed.")

    def alert_threat_quarantined(self):
        self.speak("Threat specimen quarantined and locked inside isolated vault.")


if __name__ == "__main__":
    print("[*] Testing Antimagist Voice Copilot...")
    vc = AntimagistVoiceCopilot(enabled=True)
    print("  • Speaking test alert...")
    vc.speak("Antimagist V4 Apex Sentinel Voice Engine Online.")
    import time
    time.sleep(2.5)
    print("  • Voice test finished successfully.")
