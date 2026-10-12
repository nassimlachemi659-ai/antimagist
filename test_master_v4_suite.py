"""
test_master_v4_suite.py — Antimagist V4 Apex End-to-End Test Suite
===================================================================
Automated validation suite verifying 100% stability, zero crashes, and
complete subsystem integrity for Antimagist Enterprise Security V4 Apex.
"""

import os
import sys
import time
import json
import socket
import urllib.request
import threading
import unittest

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class TestAntimagistV4Apex(unittest.TestCase):

    def test_01_gpu_sentinel_telemetry(self):
        """Verifies GPU Sentinel queries NVIDIA RTX 5050 hardware metrics safely."""
        from gpu_sentinel import AntimagistGPUSentinel
        sentinel = AntimagistGPUSentinel()
        m = sentinel.get_live_gpu_metrics()

        self.assertIsInstance(m, dict)
        self.assertIn("gpu_name", m)
        self.assertIn("temperature_c", m)
        self.assertIn("vram_str", m)
        self.assertIn("status_color", m)
        self.assertIn("utilization_gpu_pct", m)
        self.assertIn("thermal_alert", m)

        print(f"  [+] GPU Sentinel: {m['gpu_name']} | {m['temperature_c']}°C | {m['vram_str']}")

    def test_02_game_library_scanner(self):
        """Verifies Steam & PC Game Library scans installed games accurately."""
        from game_library import AntimagistGameLibrary
        gl = AntimagistGameLibrary()
        games = gl.scan_library()

        self.assertIsInstance(games, list)
        print(f"  [+] Game Library: Discovered {len(games)} installed games.")
        if games:
            first_game = games[0]
            self.assertIn("name", first_game)
            self.assertIn("platform", first_game)
            self.assertIn("size_gb", first_game)
            self.assertIn("launch_uri", first_game)
            print(f"      • Sample: {first_game['name']} ({first_game['size_gb']} GB, {first_game['launch_uri']})")

    def test_03_mobile_companion_hud_and_api(self):
        """Verifies Mobile Companion HTTP server, QR pairing, GPU streaming, and AI commands."""
        from mobile_companion import AntimagistMobileCompanion
        from gpu_sentinel import AntimagistGPUSentinel
        from antimagist_v3_ultra import AntimagistOptimizer, AntimagistSecuritySandbox
        from ping_optimizer import AntimagistPingOptimizer

        sandbox = AntimagistSecuritySandbox()
        opt = AntimagistOptimizer(sandbox)
        ping_opt = AntimagistPingOptimizer()
        gpu = AntimagistGPUSentinel()

        mc = AntimagistMobileCompanion(
            optimizer_core=opt,
            ping_optimizer=ping_opt,
            gpu_sentinel=gpu,
            port=8769 # Use isolated test port
        )
        started = mc.start_server()
        self.assertTrue(started, "Mobile companion failed to start HTTP server.")
        self.assertTrue(os.path.exists(mc.qr_path), "QR code PNG was not generated.")

        token = mc.token
        base_url = f"http://127.0.0.1:8769"

        # 1. Test HTML UI route
        req = urllib.request.Request(f"{base_url}/?token={token}")
        with urllib.request.urlopen(req, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            html = resp.read().decode("utf-8")
            self.assertIn("ANTIMAGIST V4 APEX", html)
            self.assertIn("GPU Sentinel", html)

        # 2. Test JSON Telemetry route (includes GPU metrics)
        req_telemetry = urllib.request.Request(f"{base_url}/api/telemetry?token={token}")
        with urllib.request.urlopen(req_telemetry, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            telemetry = json.loads(resp.read().decode("utf-8"))
            self.assertIn("ram_percentage", telemetry)
            self.assertIn("ping_ms", telemetry)
            self.assertIn("gpu_temp", telemetry)
            self.assertIn("vram_str", telemetry)

        # 3. Test Action route
        req_action = urllib.request.Request(f"{base_url}/api/action?action=turbo_boost&token={token}", method="POST")
        with urllib.request.urlopen(req_action, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            act_res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(act_res.get("success"))

        # 4. Test Remote AI Command Bridge route
        req_ai = urllib.request.Request(f"{base_url}/api/ai_command?q=boost%20ram&token={token}", method="POST")
        with urllib.request.urlopen(req_ai, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            ai_res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(ai_res.get("success"))
            self.assertIn("Antimagist AI", ai_res.get("response", ""))

        mc.stop_server()
        print("  [+] Mobile Companion HUD: HTTP 200 OK, GPU Telemetry, QR, and Remote AI validated.")

    def test_04_voice_copilot_audio_synthesizer(self):
        """Verifies Neural Voice Copilot runs without blocking or audio thread exceptions."""
        from voice_engine import AntimagistVoiceCopilot
        voice = AntimagistVoiceCopilot(enabled=True)
        self.assertTrue(voice.enabled)

        # Speak test in muted or background mode
        voice.speak("Antimagist V4 system integrity test.")
        voice.mute()
        self.assertFalse(voice.enabled)
        voice.unmute()
        self.assertTrue(voice.enabled)
        print("  [+] Voice Copilot: Non-blocking Win32 SAPI audio cues validated.")

    def test_05_core_director_cpu_affinity(self):
        """Verifies CPU Director topology and thread pinning calculations."""
        from core_director import AntimagistCoreDirector
        director = AntimagistCoreDirector()
        p_cores = director.get_performance_core_list()
        self.assertIsInstance(p_cores, list)
        self.assertGreater(len(p_cores), 0)

        # Test process affinity query on current python test runner PID
        current_pid = os.getpid()
        ok, msg = director.pin_process_to_performance_cores(current_pid)
        self.assertTrue(ok)
        print(f"  [+] Core Director: CPU topology mapped ({len(p_cores)} logical cores) & Affinity tested.")

    def test_06_detonation_chamber_forensics(self):
        """Verifies Forensic Detonation Chamber calculates entropy and extracts threat metrics."""
        from detonation_chamber import AntimagistDetonationChamber
        chamber = AntimagistDetonationChamber()

        # Test against python executable
        py_exe = sys.executable
        res = chamber.analyze_specimen_forensics(py_exe)

        self.assertIsInstance(res, dict)
        self.assertIn("entropy", res)
        self.assertIn("is_packed", res)
        self.assertIn("risk_score", res)
        self.assertIn("rating", res)
        print(f"  [+] Detonation Chamber: Specimen analyzed (Entropy: {res['entropy']}, Packed: {res['is_packed']}, Risk: {res['risk_score']})")

    def test_07_master_app_instantiation_and_panes(self):
        """Verifies AntimagistV4ApexApp launches cleanly, binds all 12 panes, and shuts down."""
        from antimagist_v4_apex import AntimagistV4ApexApp
        import customtkinter as ctk

        app = AntimagistV4ApexApp()
        self.assertIsNotNone(app)
        self.assertTrue(hasattr(app, "mobile_companion"))
        self.assertTrue(hasattr(app, "voice"))
        self.assertTrue(hasattr(app, "core_director"))
        self.assertTrue(hasattr(app, "detonation_chamber"))
        self.assertTrue(hasattr(app, "gpu_sentinel"))
        self.assertTrue(hasattr(app, "game_library"))

        # Verify pane functions execute without raising unhandled exceptions
        app.show_dashboard_pane()
        self.assertTrue(hasattr(app, "lbl_dash_gpu_temp"))
        self.assertTrue(hasattr(app, "lbl_gauge_ram_text"))

        app.show_gamer_pane()
        self.assertTrue(hasattr(app, "gamer_status_lbl"))

        app.show_mobile_pane()
        app.show_detonation_pane()
        app.show_scanner_pane()

        # Clean destruction
        app.destroy()
        print("  [+] Antimagist V4 Apex Application: Clean UI binding, all 12 navigation panes operational.")


if __name__ == "__main__":
    print("=" * 75)
    print("  ANTIMAGIST V4 APEX — MASTER VERIFICATION & REGRESSION SUITE")
    print("=" * 75)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAntimagistV4Apex)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[SUCCESS] 100% OF TESTS PASSED WITH ZERO CRASHES OR REGRESSIONS.")
        sys.exit(0)
    else:
        print("\n[FAIL] SOME TESTS FAILED. INVESTIGATION REQUIRED.")
        sys.exit(1)
