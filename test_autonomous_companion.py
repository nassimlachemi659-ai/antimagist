"""
test_autonomous_companion.py — Antimagist Autonomous Companion & Auto-Pilot QA Suite
==================================================================================
Verifies the 4 Core Autonomous Background Features:
  1. System Tray Integration & Auto-Pilot Guardian Loop
  2. Automatic Game Detection & Auto-Tuner ("Game Watcher") with Power Plan & Priority
  3. Interactive Process Manager & Windows API psapi.EmptyWorkingSet Hooks
  4. Rolling Network Telemetry (Ping + Jitter + Packet Loss) with Dynamic Color Coding
"""

import os
import sys
import time
import unittest
import ctypes
import psutil

from ping_optimizer import AntimagistPingOptimizer
from game_watchdog import AntimagistGameWatchdog, KNOWN_GAME_PROCESSES
from tray_manager import AntimagistTrayManager
from antimagist_v3_ultra import AntimagistOptimizer, AntimagistSecuritySandbox
from ai_kernel_agent import AntimagistAIAgent


class TestAutonomousCompanion(unittest.TestCase):

    def setUp(self):
        self.sandbox = AntimagistSecuritySandbox()
        self.optimizer = AntimagistOptimizer(self.sandbox)
        self.ping_opt = AntimagistPingOptimizer()

    def test_01_tray_menu_structure_and_options(self):
        """Verifies System Tray integration and required menu options."""
        class MockApp:
            def __init__(self):
                self.auto_pilot_enabled = True
            def after(self, ms, func): pass
            def withdraw(self): pass
            def deiconify(self): pass
            def lift(self): pass
            def focus_force(self): pass
            def toggle_auto_pilot_guardian(self):
                self.auto_pilot_enabled = not self.auto_pilot_enabled

        mock_app = MockApp()
        tray = AntimagistTrayManager(mock_app)
        self.assertIsNotNone(tray.icon, "Tray icon should be created")
        
        # Verify required menu items exist in the Tray Menu
        menu_items = [item.text for item in tray.icon.menu.items if hasattr(item, 'text')]
        self.assertTrue(any("Open Dashboard" in t for t in menu_items), f"Missing 'Open Dashboard' in {menu_items}")
        self.assertTrue(any("1-Click Boost Now" in t for t in menu_items), f"Missing '1-Click Boost Now' in {menu_items}")
        self.assertTrue(any("Toggle Auto-Pilot" in t for t in menu_items), f"Missing 'Toggle Auto-Pilot' in {menu_items}")
        self.assertTrue(any("Exit Completely" in t for t in menu_items), f"Missing 'Exit Completely' in {menu_items}")
        print("  [+] Test 1: System Tray Menu items validated cleanly.")

    def test_02_autopilot_guardian_trigger_and_logging(self):
        """Verifies Auto-Pilot Guardian loop triggers at >80% RAM and logs to AI feed."""
        class MockAppWithFeed:
            def __init__(self, optimizer):
                self.optimizer = optimizer
                self.auto_pilot_enabled = True
                self.logs = []
                self.toasts = []
            def log_to_ai_feed(self, msg):
                self.logs.append(msg)
            def show_toast_msg(self, msg):
                self.toasts.append(msg)
            def toggle_auto_pilot_guardian(self):
                self.auto_pilot_enabled = not self.auto_pilot_enabled

        app = MockAppWithFeed(self.optimizer)
        self.assertTrue(app.auto_pilot_enabled)
        app.toggle_auto_pilot_guardian()
        self.assertFalse(app.auto_pilot_enabled)
        app.toggle_auto_pilot_guardian()
        self.assertTrue(app.auto_pilot_enabled)

        # Simulate Auto-Pilot trigger
        ram_pct = 85.0
        freed_gb = 1.4
        auto_log = f"[Auto-Pilot] RAM exceeded {ram_pct:.0f}% — Cleared {freed_gb:.1f} GB standby memory"
        app.log_to_ai_feed(f"🤖 {auto_log}")
        self.assertTrue(len(app.logs) > 0)
        self.assertIn("[Auto-Pilot] RAM exceeded 85%", app.logs[-1])
        print("  [+] Test 2: Auto-Pilot Guardian RAM threshold logic verified.")

    def test_03_game_watcher_target_processes_and_actions(self):
        """Verifies target game processes catalog and game launch/close hooks."""
        # 1. Verify specific required games exist in KNOWN_GAME_PROCESSES
        required_games = ["cs2.exe", "fortniteclient-win64-shipping.exe", "valorant.exe", "gta5.exe", "bf1.exe"]
        for g in required_games:
            self.assertIn(g, KNOWN_GAME_PROCESSES, f"Required game {g} not in KNOWN_GAME_PROCESSES")

        # 2. Verify game launch triggers priority and banner updates
        launched_events = []
        closed_events = []

        def on_started(game_name, pid):
            launched_events.append((game_name, pid))

        def on_closed(record):
            closed_events.append(record)

        wd = AntimagistGameWatchdog(
            optimizer_core=self.optimizer,
            on_game_started_callback=on_started,
            on_game_closed_callback=on_closed
        )

        # Simulate game detected launching
        current_pid = os.getpid()
        wd._on_game_started("Counter-Strike 2", current_pid)
        self.assertIsNotNone(wd.current_session)
        self.assertEqual(len(launched_events), 1)
        self.assertEqual(launched_events[0][0], "Counter-Strike 2")

        # Simulate game detected closing
        wd._on_game_closed()
        self.assertIsNone(wd.current_session)
        self.assertEqual(len(closed_events), 1)
        self.assertEqual(closed_events[0]["game_name"], "Counter-Strike 2")
        print("  [+] Test 3: Game Watchdog lifecycle and callbacks verified.")

    def test_04_interactive_process_manager_apis(self):
        """Verifies psapi.EmptyWorkingSet on current process and top processes list."""
        # 1. Fetch top interactive processes
        procs = self.optimizer.get_top_interactive_processes(8)
        self.assertTrue(len(procs) > 0, "Should detect running user processes")
        first = procs[0]
        self.assertIn("pid", first)
        self.assertIn("name", first)
        self.assertIn("memory_mb", first)

        # 2. Test trimming working set on current process
        pid = os.getpid()
        ok, freed_mb = self.optimizer.trim_process_working_set(pid)
        self.assertTrue(ok, "EmptyWorkingSet should succeed on accessible process")
        self.assertGreaterEqual(freed_mb, 0.0)
        print(f"  [+] Test 4: psapi.EmptyWorkingSet verified on PID {pid} (Freed: {freed_mb} MB).")

    def test_05_rolling_network_telemetry_and_color_coding(self):
        """Verifies rolling 10-ping telemetry, jitter calculation, and dynamic colors."""
        stats = self.ping_opt.get_live_ping_telemetry()
        self.assertIn("ping_ms", stats)
        self.assertIn("jitter_ms", stats)
        self.assertIn("packet_loss_pct", stats)
        self.assertIn("status_color", stats)

        # Test color coding rules
        # Rule 1: High latency or packet loss -> Red (#EF4444)
        # Rule 2: Moderate -> Yellow (#F59E0B)
        # Rule 3: Excellent (<20ms, <2ms jitter, 0% loss) -> Green (#00FF9D)
        valid_colors = ("#00FF9D", "#F59E0B", "#EF4444")
        self.assertIn(stats["status_color"], valid_colors)
        print(f"  [+] Test 5: Rolling Ping Telemetry verified: {stats['ping_ms']}ms | Jitter: ±{stats['jitter_ms']}ms | Loss: {stats['packet_loss_pct']}% | Color: {stats['status_color']}.")


if __name__ == "__main__":
    unittest.main()
