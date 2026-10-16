"""
tray_manager.py — Windows System Tray & Silent Background Guard
================================================================
Antimagist Enterprise Security V3 Component
- Minimizes application cleanly into Windows notification area (System Tray)
- Context menu for instant turbo actions, sentinel toggle, and console restore
- Seamless background lifecycle execution
"""

import os
import threading
from typing import Callable, Optional
from PIL import Image, ImageDraw
import pystray

class AntimagistTrayManager:
    def __init__(
        self, 
        app_instance, 
        on_turbo_callback: Optional[Callable[[], None]] = None,
        on_sentinel_toggle_callback: Optional[Callable[[], None]] = None,
        quarantine_dir: str = "C:\\Antimagist_Quarantine"
    ):
        self.app = app_instance
        self.on_turbo = on_turbo_callback
        self.on_sentinel_toggle = on_sentinel_toggle_callback
        self.quarantine_dir = quarantine_dir
        self.icon: Optional[pystray.Icon] = None
        self._is_running = False

        self._setup_tray_icon()

    def _create_shield_image(self) -> Image.Image:
        """Draws a 64x64 high-tech glowing shield icon for the system tray."""
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Outer shield boundary
        draw.polygon([(32, 4), (58, 16), (52, 48), (32, 60), (12, 48), (6, 16)], fill=(0, 240, 255, 255), outline=(0, 255, 157, 255))
        # Inner shield core
        draw.polygon([(32, 12), (50, 22), (46, 44), (32, 53), (18, 44), (14, 22)], fill=(8, 10, 16, 255))
        # Center core glow
        draw.ellipse([(26, 26), (38, 38)], fill=(0, 255, 157, 255))
        return img

    def _setup_tray_icon(self):
        img = self._create_shield_image()

        def restore_action(icon, item):
            self.app.after(0, self.restore_window)

        def turbo_action(icon, item):
            if self.on_turbo:
                threading.Thread(target=self.on_turbo, daemon=True).start()

        def toggle_sentinel_action(icon, item):
            if self.on_sentinel_toggle:
                self.app.after(0, self.on_sentinel_toggle)

        def open_vault_action(icon, item):
            if os.path.exists(self.quarantine_dir):
                os.startfile(self.quarantine_dir)

        def cs2_action(icon, item):
            if hasattr(self.app, 'show_cs2_pane'):
                self.app.after(0, self.app.show_cs2_pane)
                self.app.after(0, self.restore_window)

        def dpc_action(icon, item):
            if hasattr(self.app, 'show_dpc_pane'):
                self.app.after(0, self.app.show_dpc_pane)
                self.app.after(0, self.restore_window)

        def exit_action(icon, item):
            self.stop_tray()
            self.app.after(0, lambda: self.app.destroy())

        def toggle_autopilot_action(icon, item):
            if hasattr(self.app, 'toggle_auto_pilot_guardian'):
                self.app.after(0, self.app.toggle_auto_pilot_guardian)
            elif self.on_sentinel_toggle:
                self.app.after(0, self.on_sentinel_toggle)

        menu = pystray.Menu(
            pystray.MenuItem("🛡️ Open Dashboard", restore_action, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⚡ 1-Click Boost Now", turbo_action),
            pystray.MenuItem("🤖 Toggle Auto-Pilot", toggle_autopilot_action),
            pystray.MenuItem("🎯 CS2 Tournament Mode", cs2_action),
            pystray.MenuItem("📉 Audit DPC Latency", dpc_action),
            pystray.MenuItem("🔒 Quarantine Vault", open_vault_action),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🚪 Exit Completely", exit_action)
        )

        self.icon = pystray.Icon("AntimagistEnterprise", img, "Antimagist Enterprise V11 Omni-Workstation", menu)

    def start_tray(self):
        if not self._is_running and self.icon:
            self._is_running = True
            threading.Thread(target=self.icon.run, daemon=True).start()

    def stop_tray(self):
        if self._is_running and self.icon:
            self._is_running = False
            try:
                self.icon.stop()
            except Exception:
                pass

    def minimize_to_tray(self):
        """Hides the GUI window while keeping background threads and tray icon active."""
        self.app.withdraw()
        try:
            from telemetry_bus import telemetry_bus
            telemetry_bus.trim_own_working_set()
        except Exception:
            pass
        if hasattr(self.app, 'show_toast_msg'):
            self.app.show_toast_msg("Antimagist is running silently in the system tray.")

    def restore_window(self):
        """Restores and focuses the main application window."""
        self.app.deiconify()
        self.app.lift()
        self.app.focus_force()
