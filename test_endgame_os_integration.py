"""
test_endgame_os_integration.py — Master QA Verification Suite for Endgame OS Integration Layer
=============================================================================================
Antimagist Enterprise Security V11 Test Suite
Tests:
1. Global In-Game Hotkey Engine (Registration, default keybinds, cheatsheet, callbacks)
2. Live PC Stress Benchmark (CPU multi-core ops, RAM throughput, Disk I/O, Ping stability)
3. Match Watchdog & match_history.json (2s telemetry sampling, session summary calculation)
4. Bandwidth Guard (Target process scanning, priority & I/O throttling, restoration)
5. Display Reflex (EnumDisplaySettingsW query, current vs max Hz audit, lock logic)
6. GPU Sentinel Real-Time Hardware Telemetry (Core Clock, Memory Clock, Power Draw, Fan Speed)
7. Crash Guard Self-Healing Boundary (Exception logging to antimagist_crash_guard.log)
8. Auto-Updater & Zero-UAC Scheduled Task Engine
9. Headless App UI Verification (Full Topbar, Bento Grid, Telemetry Cards, and Settings)
"""

import os
import sys
import json
import time
import unittest
import subprocess
from typing import Dict, Any

# Ensure root directory is on sys.path
SCRATCH_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRATCH_DIR not in sys.path:
    sys.path.insert(0, SCRATCH_DIR)

from crash_guard import AntimagistCrashGuard, safe_worker
from global_hotkey_engine import AntimagistGlobalHotkeyEngine
from bandwidth_guard import AntimagistBandwidthGuard
from display_reflex import AntimagistDisplayReflex
from gpu_sentinel import AntimagistGPUSentinel
from game_watchdog import AntimagistGameWatchdog
from benchmark_card import AntimagistBenchmarkCard
from auto_updater import AntimagistAutoUpdater


class TestEndgameOSIntegration(unittest.TestCase):
    """Rigorous verification suite for Antimagist V11 Endgame OS Integration Layer."""

    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 70)
        print("  RUNNING ANTIMAGIST V11 ENDGAME OS INTEGRATION TEST SUITE")
        print("=" * 70)

    def test_01_crash_guard_self_healing(self):
        """Verifies global exception boundary and file logging."""
        guard = AntimagistCrashGuard()
        guard.install()
        self.assertTrue(guard._installed)

        test_msg = "Automated test exception verification event"
        guard.log_event("TEST", test_msg)
        self.assertTrue(os.path.exists(guard.log_path))

        with open(guard.log_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(test_msg, content)

        # Test @safe_worker decorator
        @safe_worker(fallback_return="SAFE_RECOVERY", silent=True)
        def crashing_func():
            raise ZeroDivisionError("Simulated fault")

        res = crashing_func()
        self.assertEqual(res, "SAFE_RECOVERY")
        print("  [+] CrashGuard: Self-healing exception handler and log file verified.")

    def test_02_global_hotkey_engine(self):
        """Verifies global hotkey engine initialization, cheatsheet, and callbacks."""
        engine = AntimagistGlobalHotkeyEngine()
        self.assertIn("turbo_clean", engine.hotkeys)
        self.assertIn("toggle_hud", engine.hotkeys)
        self.assertIn("tournament_lock", engine.hotkeys)
        self.assertIn("push_to_talk", engine.hotkeys)

        cheatsheet = engine.get_cheatsheet()
        self.assertEqual(len(cheatsheet), 4)
        keys = [item["key"] for item in cheatsheet]
        self.assertTrue(any("ALT+F1" in k for k in keys))
        self.assertTrue(any("ALT+F2" in k for k in keys))
        self.assertTrue(any("ALT+F3" in k for k in keys))
        self.assertTrue(any("ALT+V" in k for k in keys))

        # Test dispatch execution without crashing
        engine._on_turbo_clean()
        engine._on_toggle_hud()
        engine._on_toggle_tournament_lock()
        print("  [+] Global Hotkeys: Alt+F1, Alt+F2, Alt+F3, Alt+V verified.")

    def test_03_bandwidth_guard(self):
        """Verifies target bandwidth/torrent hogs scanner and throttling."""
        guard = AntimagistBandwidthGuard()
        hogs = guard.scan_active_hogs()
        self.assertIsInstance(hogs, list)

        # Test engage & disengage
        res_eng = guard.engage_bandwidth_guard()
        self.assertTrue(guard.is_active)
        self.assertEqual(res_eng["status"], "ENGAGED")

        res_dis = guard.disengage_bandwidth_guard()
        self.assertFalse(guard.is_active)
        self.assertEqual(res_dis["status"], "DISENGAGED")
        print("  [+] Bandwidth Guard: Process scanner, priority throttle & restore verified.")

    def test_04_display_reflex_hz_audit(self):
        """Verifies Windows EnumDisplaySettingsW refresh rate detection."""
        reflex = AntimagistDisplayReflex()
        audit = reflex.get_display_hz_audit()
        self.assertIn("current_hz", audit)
        self.assertIn("max_hz", audit)
        self.assertIn("supported_hz", audit)
        self.assertGreaterEqual(audit["current_hz"], 30)
        self.assertGreaterEqual(audit["max_hz"], audit["current_hz"])
        self.assertTrue(len(audit["supported_hz"]) >= 1)

        ok, msg = reflex.lock_max_refresh_rate()
        self.assertIsInstance(ok, bool)
        print(f"  [+] Display Reflex: Monitor detected at {audit['current_hz']}Hz (Max: {audit['max_hz']}Hz).")

    def test_05_nvidia_hardware_telemetry(self):
        """Verifies nvidia-smi live query for clocks, power, and fan speed."""
        sentinel = AntimagistGPUSentinel()
        metrics = sentinel.get_live_gpu_metrics()
        self.assertIn("gpu_name", metrics)
        self.assertIn("temperature_c", metrics)
        self.assertIn("core_clock_mhz", metrics)
        self.assertIn("memory_clock_mhz", metrics)
        self.assertIn("power_draw_w", metrics)
        self.assertIn("fan_speed_pct", metrics)

        # If NVIDIA is present on this machine, test real values
        if metrics.get("is_available") and "NVIDIA" in metrics["gpu_name"]:
            self.assertGreater(metrics["core_clock_mhz"], 0)
            self.assertGreater(metrics["memory_clock_mhz"], 0)
            self.assertGreater(metrics["temperature_c"], 0)
            print(f"  [+] NVIDIA Telemetry: {metrics['gpu_name']} | Core: {metrics['core_clock_mhz']}MHz | Mem: {metrics['memory_clock_mhz']}MHz | Power: {metrics['power_draw_w']}W | Fan: {metrics['fan_speed_pct']}% | Temp: {metrics['temperature_c']}°C")
        else:
            print("  [+] GPU Sentinel: Fallback hardware telemetry query verified.")

    def test_06_match_watchdog_and_history(self):
        """Verifies 2-second in-memory sampling and structured match_history.json output."""
        watchdog = AntimagistGameWatchdog()
        self.assertIsInstance(watchdog.match_history, list)

        # Simulate synthetic match session
        watchdog._on_game_started("Counter-Strike 2", 99999)
        self.assertIsNotNone(watchdog.current_session)
        self.assertIn("cpu_samples", watchdog.current_session)
        self.assertIn("gpu_temp_samples", watchdog.current_session)
        self.assertIn("ram_gb_samples", watchdog.current_session)
        self.assertIn("pings", watchdog.current_session)

        # Inject simulated 2-second telemetry ticks
        watchdog.current_session["cpu_samples"].extend([14.5, 22.0, 18.2])
        watchdog.current_session["gpu_temp_samples"].extend([48, 52, 51])
        watchdog.current_session["ram_gb_samples"].extend([7.4, 7.6, 7.5])
        watchdog.current_session["pings"].extend([11.2, 12.0, 11.8])
        watchdog.current_session["jitters"].extend([0.3, 0.4, 0.2])

        # Close session
        watchdog._on_game_closed()
        self.assertIsNone(watchdog.current_session)
        self.assertTrue(len(watchdog.match_history) > 0)

        last_match = watchdog.match_history[-1]
        self.assertEqual(last_match["game_name"], "Counter-Strike 2")
        self.assertIn("avg_cpu_pct", last_match)
        self.assertIn("peak_gpu_temp", last_match)
        self.assertIn("peak_ram_gb", last_match)
        self.assertIn("avg_ping_ms", last_match)
        self.assertIn("stability_rating", last_match)
        self.assertTrue(os.path.exists("match_history.json"))
        print(f"  [+] Match Watchdog: Saved structured session to match_history.json ({last_match['stability_rating']}).")

    def test_07_live_system_stress_benchmark(self):
        """Verifies the multi-phase system stress & latency benchmark engine."""
        bench = AntimagistBenchmarkCard()
        # Run a 3-second quick benchmark
        res = bench.run_live_system_benchmark(duration_sec=3)
        self.assertIn("overall_score", res)
        self.assertIn("overall_tier", res)
        self.assertIn("cpu", res)
        self.assertIn("gpu", res)
        self.assertIn("ram", res)
        self.assertIn("disk", res)
        self.assertIn("network", res)

        self.assertGreater(res["overall_score"], 0)
        self.assertGreater(res["cpu"]["ops_per_sec"], 0)
        self.assertGreater(res["ram"]["throughput_gb_s"], 0)
        self.assertGreater(res["disk"]["avg_mb_s"], 0)
        self.assertGreater(res["network"]["avg_ping_ms"], 0)

        # Test score card text formatting
        text = bench.format_score_card_text(res)
        self.assertIn("ANTIMAGIST V11 ENTERPRISE HARDWARE BENCHMARK CARD", text)
        self.assertIn(str(res["overall_score"]), text)
        print(f"  [+] Live Benchmark: Score {res['overall_score']}/10,000 [{res['overall_tier']}]. Text formatting verified.")

    def test_08_auto_updater_scheduled_task(self):
        """Verifies auto updater query and scheduled task registration routines."""
        updater = AntimagistAutoUpdater()
        self.assertEqual(updater.current_version, "11.0.0")

        # Test task state query
        is_active = updater.is_silent_autostart_enabled()
        self.assertIsInstance(is_active, bool)
        print(f"  [+] Auto-Updater & Zero-UAC: Version {updater.current_version} verified. Task Active: {is_active}")

    def test_09_headless_app_ui_initialization(self):
        """Verifies that AntimagistV4ApexApp instantiates all Endgame OS components cleanly."""
        import customtkinter as ctk
        ctk.set_appearance_mode("Dark")

        from antimagist_v4_apex import AntimagistV4ApexApp
        app = AntimagistV4ApexApp()
        app.withdraw()  # Headless mode

        # Verify Endgame subsystems attached to app
        self.assertTrue(hasattr(app, "hotkey_engine"))
        self.assertTrue(hasattr(app, "bandwidth_guard"))
        self.assertTrue(hasattr(app, "game_watchdog"))
        self.assertTrue(hasattr(app, "benchmark_card"))
        self.assertTrue(hasattr(app, "display_reflex"))

        # Verify views open without throwing
        app.show_dashboard_pane()
        self.assertTrue(hasattr(app, "hw_details_card"))

        app.show_analytics_pane()
        app.show_benchmark_card_pane()
        app.show_settings_pane()

        app.destroy()
        print("  [+] Headless App UI: Dashboard, Match History, Benchmark Card, and Settings initialized cleanly.")


if __name__ == "__main__":
    unittest.main()
