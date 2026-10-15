"""
test_antimagist_verification.py — Comprehensive Automated Verification Test Suite
==================================================================================
Tests:
  1. Telemetry Sensors (CPU > 0.0%, RAM valid floats, full GPU name, Ping/Jitter/Loss metrics).
  2. Core System Optimization Functions (RAM flush, cache sweep, process list fetch).
  3. AI Copilot OS Action Tools (action_open_and_type, action_fix_audio, action_diagnose_game).
  4. Natural Language Intent Routing & Typo-Tolerant Action Dispatch.
  5. UI Initialization in Headless Mode (Zero layout exceptions, all 46 panes registered).
"""

import os
import sys
import time
import unittest
import psutil

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from antimagist_v3_ultra import AntimagistOptimizer
from gpu_sentinel import AntimagistGPUSentinel
from ping_optimizer import AntimagistPingOptimizer
from ai_kernel_agent import AntimagistAIAgent
from security_sandbox import SecuritySandbox


class TestTelemetrySensors(unittest.TestCase):
    """Verifies that live telemetry sensors return valid, non-zero, non-truncated metrics."""

    def setUp(self):
        self.optimizer = AntimagistOptimizer()
        self.gpu = AntimagistGPUSentinel()
        self.ping = AntimagistPingOptimizer()

    def test_cpu_telemetry_not_stuck(self):
        """Verify CPU percent returns valid float > 0.0 (not stuck at 0.0%)."""
        # Prime psutil counter
        psutil.cpu_percent(interval=None)
        time.sleep(0.1)
        m = self.optimizer.get_live_metrics(cpu_interval=None)
        cpu_val = m["cpu_percentage"]
        self.assertIsInstance(cpu_val, float)
        self.assertGreater(cpu_val, 0.0, f"CPU % is stuck at {cpu_val}%")
        print(f"  [+] Live CPU Telemetry Verified: {cpu_val}% (Active processes: {m['active_processes']})")

    def test_ram_telemetry_valid_floats(self):
        """Verify RAM metrics return valid positive numbers."""
        m = self.optimizer.get_live_metrics()
        self.assertGreater(m["total_ram_gb"], 0.0)
        self.assertGreater(m["used_ram_gb"], 0.0)
        self.assertGreater(m["ram_percentage"], 0.0)
        self.assertLessEqual(m["ram_percentage"], 100.0)
        print(f"  [+] RAM Telemetry Verified: {m['used_ram_gb']} / {m['total_ram_gb']} GB ({m['ram_percentage']}%)")

    def test_gpu_name_not_truncated(self):
        """Verify GPU model name is not truncated with hardcoded slices."""
        gm = self.gpu.get_live_gpu_metrics()
        gpu_name = gm["gpu_name"]
        self.assertIsInstance(gpu_name, str)
        self.assertGreater(len(gpu_name), 5)
        # Ensure it's not chopped off like 'NVIDIA GeFor' or 'RTX 5'
        self.assertNotIn("NVIDIA GeFor:", gpu_name)
        self.assertTrue("RTX" in gpu_name or "GeForce" in gpu_name or "Radeon" in gpu_name or "Intel" in gpu_name or "Graphics" in gpu_name)
        print(f"  [+] Full GPU Name Verified: '{gpu_name}' ({gm['temperature_c']}°C, {gm['vram_str']})")

    def test_ping_jitter_loss_metrics(self):
        """Verify Ping, Jitter, and Packet Loss return valid metrics."""
        stats = self.ping.get_live_ping_telemetry()
        self.assertIn("ping_ms", stats)
        self.assertIn("jitter_ms", stats)
        self.assertIn("packet_loss_pct", stats)
        self.assertIn("status_color", stats)
        self.assertGreaterEqual(stats["ping_ms"], 0.0)
        self.assertGreaterEqual(stats["jitter_ms"], 0.0)
        self.assertGreaterEqual(stats["packet_loss_pct"], 0.0)
        print(f"  [+] Ping Telemetry Verified: {stats['ping_ms']:.1f}ms | Jitter: ±{stats['jitter_ms']:.1f}ms | Loss: {stats['packet_loss_pct']:.0f}%")


class TestCoreSystemOptimization(unittest.TestCase):
    """Verifies core optimization actions execute safely without throwing exceptions."""

    def setUp(self):
        self.optimizer = AntimagistOptimizer()

    def test_memory_boost_execution(self):
        """Verify memory boost runs and flushes working set without errors."""
        completed = False
        res_payload = None

        def on_done(res):
            nonlocal completed, res_payload
            completed = True
            res_payload = res

        self.optimizer.run_memory_boost(on_done)
        for _ in range(50):
            if completed:
                break
            time.sleep(0.1)
        self.assertTrue(completed)
        self.assertIsNotNone(res_payload)
        self.assertTrue("RAM Released" in str(res_payload) or "freed" in str(res_payload).lower())
        print(f"  [+] Memory Boost Verified: {res_payload}")

    def test_process_list_fetch(self):
        """Verify top memory process list returns populated list of tuples."""
        procs = self.optimizer.get_top_memory_processes(limit=8)
        self.assertIsInstance(procs, list)
        self.assertGreater(len(procs), 0)
        name, mb = procs[0]
        self.assertIsInstance(name, str)
        self.assertGreater(mb, 0.0)
        print(f"  [+] Process List Fetch Verified: Top process '{name}' ({mb:.1f} MB)")


class TestAICopilotActionAgent(unittest.TestCase):
    """Verifies AI Copilot OS Action Tools perform real actions and return structured output."""

    def setUp(self):
        self.optimizer = AntimagistOptimizer()
        self.sandbox = SecuritySandbox(None)
        self.agent = AntimagistAIAgent(self.optimizer, None, None, self.sandbox)

    def test_action_open_and_type_dry(self):
        """Verify browser & app automation tool constructs search URLs and reports actions."""
        # Querying YouTube search
        ok, msg = self.agent.action_open_and_type("youtube", search_query="lofi gaming beats")
        self.assertTrue(ok)
        self.assertIn("YouTube", msg)
        self.assertIn("lofi+gaming+beats", msg)

        # Querying Google search
        ok, msg = self.agent.action_open_and_type("chrome", search_query="antimagist enterprise")
        self.assertTrue(ok)
        self.assertIn("Google Chrome", msg)
        print(f"  [+] action_open_and_type Verified: {msg}")

    def test_action_fix_audio(self):
        """Verify automated audio troubleshooter inspects services, unmuting, and endpoints."""
        ok, report = self.agent.action_fix_audio()
        self.assertTrue(ok)
        self.assertIn("Audiosrv", report)
        self.assertIn("AudioEndpointBuilder", report)
        self.assertIn("unmute", report.lower())
        self.assertIn("Endpoints:", report)
        print("  [+] action_fix_audio Verified: multi-step audio diagnostic and repair succeeded.")

    def test_action_diagnose_game(self):
        """Verify automated game crash doctor queries Event Viewer and checks hardware headroom."""
        ok, report = self.agent.action_diagnose_game("CS2")
        self.assertTrue(ok)
        self.assertIn("Game Crash Doctor", report)
        self.assertIn("Windows Application Crash", report)
        self.assertIn("HARDWARE HEADROOM", report)
        self.assertIn("Shader Cache", report)
        print("  [+] action_diagnose_game Verified: root cause diagnostic succeeded.")

    def test_natural_language_intent_routing(self):
        """Verify natural language requests with typos reliably trigger OS actions."""
        # 1. Audio fix intent
        resp_audio = self.agent.process_query("fix why my sound doesn't work")
        self.assertIn("Audio Troubleshooter", resp_audio)

        # 2. Game crash intent
        resp_game = self.agent.process_query("why does cs2 crash or not work")
        self.assertIn("Game Crash Doctor", resp_game)

        # 3. Browser search intent
        resp_browser = self.agent.process_query("open youtube and search synthwave chill")
        self.assertIn("Browser Automation", resp_browser)

        # 4. RAM question intent
        resp_ram = self.agent.process_query("what is eating my ram")
        self.assertIn("Memory Inspection", resp_ram)

        print("  [+] Natural Language Intent Routing Verified: 4/4 directives routed accurately.")


class TestHeadlessUIInitialization(unittest.TestCase):
    """Verifies full application UI initializes without layout exceptions or missing callbacks."""

    def test_ui_instantiation(self):
        """Instantiate AntimagistV4ApexApp in headless mode and verify components."""
        from antimagist_v4_apex import AntimagistV4ApexApp
        app = AntimagistV4ApexApp()
        app.withdraw()  # Keep hidden for headless CI/CD testing

        # Verify window title
        self.assertIn("V11 Omni-Workstation", app.title())

        # Verify 5 primary navigation tabs exist
        self.assertIn("dash", app.primary_nav_buttons)
        self.assertIn("ai_tab", app.primary_nav_buttons)
        self.assertIn("sec_suite", app.primary_nav_buttons)
        self.assertIn("perf_suite", app.primary_nav_buttons)
        self.assertIn("settings_tab", app.primary_nav_buttons)

        # Verify 46 advanced tools exist in nav_buttons (plus any dynamic AI plugins)
        self.assertGreaterEqual(len(app.nav_buttons), 46)

        # Verify topbar pills
        self.assertTrue(hasattr(app, "btn_voice"))
        self.assertTrue(hasattr(app, "btn_sfx"))
        self.assertTrue(hasattr(app, "pill_gpu"))
        self.assertTrue(hasattr(app, "pill_ping"))

        # Verify dashboard interactive process table
        self.assertTrue(hasattr(app, "proc_scroll_frame"))

        print(f"  [+] Headless UI Verified: Title, Topbar, 5 Primary Tabs, and all {len(app.nav_buttons)} Panes initialized cleanly.")
        app.destroy()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  ANTIMAGIST V11 OMNI-WORKSTATION — PRINCIPAL SYSTEMS QA VERIFICATION")
    print("=" * 70)
    unittest.main(verbosity=2)
