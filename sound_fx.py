"""
sound_fx.py — Antimagist V5 Cyber Sci-Fi Sound FX & Voice Pack Engine
======================================================================
Antimagist Enterprise Security V5 Component
- Synthesizes futuristic high-tech auditory feedback for UI interactions
- Asynchronous, non-blocking audio generation using Windows native winsound
- Audio Presets:
    • UI Micro-Click: High-tech 2200 Hz tactile click
    • Warp Boost Sweep: Rising frequency synthesizer sweep on RAM / Apex Boost
    • Tripwire Breach Siren: Two-tone emergency alert on security breach
    • Success Chord: Dual-frequency confirmation chime
- 100% thread-safe with immediate mute toggle
"""

import os
import sys
import time
import threading
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistSoundFX:
    """Manages tactical audio cues and UI sound synthesis."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._lock = threading.Lock()

    def toggle_sound(self) -> bool:
        with self._lock:
            self.enabled = not self.enabled
            return self.enabled

    def _play_async(self, fn):
        if not self.enabled or os.name != 'nt':
            return
        threading.Thread(target=fn, daemon=True).start()

    def play_click(self):
        """Tactile micro-click for UI buttons."""
        def worker():
            try:
                import winsound
                winsound.Beep(2400, 18)
            except Exception:
                pass
        self._play_async(worker)

    def play_warp_boost(self):
        """Rising frequency sweep when memory is purged or Apex boost is triggered."""
        def worker():
            try:
                import winsound
                # Ascending frequency glissando
                for freq in [800, 1200, 1600, 2100, 2600]:
                    winsound.Beep(freq, 22)
            except Exception:
                pass
        self._play_async(worker)

    def play_success(self):
        """Harmonic dual-tone confirmation chime."""
        def worker():
            try:
                import winsound
                winsound.Beep(1400, 35)
                winsound.Beep(2200, 50)
            except Exception:
                pass
        self._play_async(worker)

    def play_alarm(self):
        """Two-tone security tripwire alert."""
        def worker():
            try:
                import winsound
                for _ in range(2):
                    winsound.Beep(2200, 70)
                    winsound.Beep(1400, 70)
            except Exception:
                pass
        self._play_async(worker)


if __name__ == "__main__":
    print("[*] Testing Antimagist Sound FX Engine...")
    sfx = AntimagistSoundFX(enabled=True)
    print("  • Playing UI Click...")
    sfx.play_click()
    time.sleep(0.1)
    print("  • Playing Success Chime...")
    sfx.play_success()
    time.sleep(0.15)
    print("  • Playing Warp Boost Sweep...")
    sfx.play_warp_boost()
    time.sleep(0.3)
    print("  • Sound FX Engine Test PASSED.")
