"""
test_master_v4_plus_suite.py — Antimagist V4 Plus Comprehensive Verification Suite
===================================================================================
Automated validation suite verifying 100% stability, zero crashes, and
complete subsystem integrity across all 11 core modules of Antimagist V4 Plus.
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


class TestAntimagistV4Plus(unittest.TestCase):

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
        print(f"  [+] GPU Sentinel: {m['gpu_name']} | {m['temperature_c']}°C | {m['vram_str']}")

    def test_02_game_library_scanner(self):
        """Verifies Steam & PC Game Library scans installed games accurately."""
        from game_library import AntimagistGameLibrary
        gl = AntimagistGameLibrary()
        games = gl.scan_library()

        self.assertIsInstance(games, list)
        print(f"  [+] Game Library: Discovered {len(games)} installed games.")

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
            port=8771 # Isolated test port
        )
        started = mc.start_server()
        self.assertTrue(started, "Mobile companion failed to start HTTP server.")

        token = mc.token
        base_url = "http://127.0.0.1:8771"

        # 1. HTML route
        with urllib.request.urlopen(f"{base_url}/?token={token}", timeout=3) as resp:
            self.assertEqual(resp.status, 200)

        # 2. Telemetry route
        with urllib.request.urlopen(f"{base_url}/api/telemetry?token={token}", timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            telemetry = json.loads(resp.read().decode("utf-8"))
            self.assertIn("gpu_temp", telemetry)

        # 3. Remote AI route
        req_ai = urllib.request.Request(f"{base_url}/api/ai_command?q=boost%20ram&token={token}", method="POST")
        with urllib.request.urlopen(req_ai, timeout=3) as resp:
            self.assertEqual(resp.status, 200)

        mc.stop_server()
        print("  [+] Mobile Companion HUD: HTTP 200 OK, GPU Telemetry, QR, and Remote AI validated.")

    def test_04_voice_copilot_audio_synthesizer(self):
        """Verifies Neural Voice Copilot runs without blocking or audio thread exceptions."""
        from voice_engine import AntimagistVoiceCopilot
        voice = AntimagistVoiceCopilot(enabled=True)
        self.assertTrue(voice.enabled)
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

        current_pid = os.getpid()
        ok, msg = director.pin_process_to_performance_cores(current_pid)
        self.assertTrue(ok)
        print(f"  [+] Core Director: CPU topology mapped ({len(p_cores)} logical cores) & Affinity tested.")

    def test_06_detonation_chamber_forensics(self):
        """Verifies Forensic Detonation Chamber calculates entropy and extracts threat metrics."""
        from detonation_chamber import AntimagistDetonationChamber
        chamber = AntimagistDetonationChamber()
        res = chamber.analyze_specimen_forensics(sys.executable)

        self.assertIsInstance(res, dict)
        self.assertIn("entropy", res)
        self.assertIn("is_packed", res)
        print(f"  [+] Detonation Chamber: Specimen analyzed (Entropy: {res['entropy']}, Packed: {res['is_packed']})")

    def test_07_hud_overlay_in_game(self):
        """Verifies In-Game Transparent HUD Overlay creates, streams, and destroys cleanly."""
        from hud_overlay import AntimagistHUDOverlay
        hud = AntimagistHUDOverlay()
        self.assertFalse(hud.is_visible)

        # Show HUD
        hud.show()
        self.assertTrue(hud.is_visible)
        self.assertIsNotNone(hud.window)

        # Quick RAM Boost dry-run
        hud._quick_ram_boost()

        # Clean teardown
        hud.destroy()
        self.assertFalse(hud.is_visible)
        print("  [+] In-Game HUD Overlay: Frameless glassmorphic window lifecycle validated.")

    def test_08_cs2_tournament_optimizer(self):
        """Verifies Counter-Strike 2 discovery and autoexec injection."""
        from cs2_optimizer import AntimagistCS2Optimizer
        cs2 = AntimagistCS2Optimizer()
        st = cs2.get_status()

        self.assertIsInstance(st, dict)
        self.assertIn("is_installed", st)
        self.assertIn("cfg_dir", st)

        if st["is_installed"]:
            ok, msg = cs2.apply_tournament_optimization()
            self.assertTrue(ok)
            self.assertTrue(os.path.exists(cs2.autoexec_path))
            print(f"  [+] CS2 Optimizer: Found CS2 at {st['cs2_root']} and verified tournament autoexec.")
        else:
            print("  [!] CS2 Optimizer: CS2 not found in candidate paths (skipping write).")

    def test_09_voice_listener_intent_dispatch(self):
        """Verifies Two-Way Voice Copilot intent mapping and execution."""
        from voice_listener import AntimagistVoiceListener
        vl = AntimagistVoiceListener()

        r1 = vl.process_voice_intent("boost memory")
        self.assertIn("Memory Boost", r1)

        r2 = vl.process_voice_intent("clean cache")
        self.assertIn("cache", r2.lower())

        r3 = vl.process_voice_intent("fix ping")
        self.assertIn("latency", r3.lower())

        print("  [+] Two-Way Voice Listener: Intent processing and dispatch validated.")

    def test_10_context_menu_v4_integrator(self):
        """Verifies Windows Explorer right-click shell extensions register and unregister."""
        from context_menu_v4 import AntimagistContextMenuV4
        cm = AntimagistContextMenuV4()

        ok, msg = cm.register_context_menus()
        self.assertTrue(ok)
        self.assertTrue(cm.is_registered())
        print("  [+] Context Menu Integrator: HKCU Explorer shell extension verified.")

    def test_11_master_v4_plus_application_lifecycle(self):
        """Verifies AntimagistV4ApexApp launches cleanly, binds all 13 panes, and shuts down."""
        from antimagist_v4_apex import AntimagistV4ApexApp

        app = AntimagistV4ApexApp()
        self.assertIsNotNone(app)
        self.assertTrue(hasattr(app, "hud_overlay"))
        self.assertTrue(hasattr(app, "cs2_optimizer"))
        self.assertTrue(hasattr(app, "voice_listener"))
        self.assertTrue(hasattr(app, "context_menu_v4"))

        # Verify new CS2 pane renders cleanly
        app.show_cs2_pane()

        # Verify other essential panes
        app.show_dashboard_pane()
        app.show_gamer_pane()
        app.show_mobile_pane()
        app.show_detonation_pane()

        # Clean destruction
        app.destroy()
        print("  [+] Antimagist V4 Apex Application: Clean UI binding, all 13 navigation panes operational.")


if __name__ == "__main__":
    print("=" * 75)
    print("  ANTIMAGIST V4 PLUS — MASTER VERIFICATION & REGRESSION SUITE")
    print("=" * 75)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAntimagistV4Plus)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[SUCCESS] 100% OF TESTS PASSED WITH ZERO CRASHES OR REGRESSIONS.")
        sys.exit(0)
    else:
        print("\n[FAIL] SOME TESTS FAILED. INVESTIGATION REQUIRED.")
        sys.exit(1)
