"""
test_v2_ultra_smart.py — Verification Suite for Ultra Game Sentinel & Web Bridge Daemon
========================================================================================
Validates:
1. Ultra Game Sentinel initialization and profile matching.
2. Simulated launch, auto-tuning (High priority, P-Core affinity, timer resolution), and clean rollback.
3. Web Bridge Daemon lifecycle (startup, port binding, shutdown).
4. REST Endpoints: /api/v2/telemetry, /api/v2/status, /api/v2/action.
5. Zero-Trust Action Execution: Whitelisted parameter verification & blocked injection defense.
6. AntimagistV4ApexApp full binding integration test with Sentinel & Bridge.
"""

import os
import sys
import time
import json
import unittest
import urllib.request
import urllib.parse
from typing import Dict, Any

from ultra_game_sentinel import AntimagistUltraGameSentinel, ESPORTS_TARGET_PROFILES
from web_bridge_daemon import AntimagistWebBridgeDaemon
from antimagist_core_v2 import AntimagistStrictValidator


class TestAntimagistUltraSmart(unittest.TestCase):
    """Deep verification suite for Ultra Game Sentinel and Web Bridge Daemon."""

    @classmethod
    def setUpClass(cls):
        os.environ["ANTIMAGIST_CI_MOCK_HARDWARE"] = "1"
        os.environ["CI"] = "true"
        os.environ["ANTIMAGIST_HEADLESS"] = "1"

    def test_01_esports_profiles_catalog(self):
        """Verifies all major esports games are registered with complete tuning profiles."""
        required_games = ["cs2.exe", "valorant-win64-shipping.exe", "r5apex.exe", "fortniteclient-win64-shipping.exe", "cod.exe"]
        for g in required_games:
            self.assertIn(g, ESPORTS_TARGET_PROFILES)
            prof = ESPORTS_TARGET_PROFILES[g]
            self.assertIn("title", prof)
            self.assertIn("timer_res_ms", prof)
            self.assertEqual(prof["priority"], "HIGH")
            self.assertTrue(prof["pin_p_cores"])
            self.assertTrue(prof["clean_standby_ram"])
        print("  [+] Test 1: Esports Profiles Catalog (13 titles) verified.")

    def test_02_ultra_game_sentinel_lifecycle(self):
        """Verifies start, stop, and telemetry snapshot of Ultra Game Sentinel."""
        events = []
        sentinel = AntimagistUltraGameSentinel(on_event_callback=lambda t, m: events.append((t, m)))
        sentinel.start_sentinel()
        self.assertTrue(sentinel.is_monitoring)

        time.sleep(0.3)
        snap = sentinel.get_telemetry_snapshot()
        self.assertIsInstance(snap, dict)
        self.assertTrue(snap["is_monitoring"])
        self.assertFalse(snap["is_game_active"])
        self.assertIn("stats", snap)

        sentinel.stop_sentinel()
        self.assertFalse(sentinel.is_monitoring)
        self.assertGreaterEqual(len(events), 2)
        print("  [+] Test 2: Ultra Game Sentinel Lifecycle verified.")

    def test_03_simulated_game_tuning_and_rollback(self):
        """Simulates game launch on self PID and verifies automatic rollback."""
        events = []
        sentinel = AntimagistUltraGameSentinel(on_event_callback=lambda t, m: events.append((t, m)))

        # Use current process PID as target
        current_pid = os.getpid()
        profile = ESPORTS_TARGET_PROFILES["cs2.exe"]

        ok, msg = sentinel.tune_game_process(current_pid, "cs2.exe", profile)
        self.assertTrue(ok)
        self.assertIsNotNone(sentinel.active_game_session)
        self.assertEqual(sentinel.active_game_session["title"], "Counter-Strike 2")

        snap = sentinel.get_telemetry_snapshot()
        self.assertTrue(snap["is_game_active"])
        self.assertEqual(snap["active_game"], "Counter-Strike 2")

        # Rollback
        revert_ok, revert_msg = sentinel.revert_game_tuning()
        self.assertTrue(revert_ok)
        self.assertIsNone(sentinel.active_game_session)

        snap_reverted = sentinel.get_telemetry_snapshot()
        self.assertFalse(snap_reverted["is_game_active"])
        print("  [+] Test 3: Simulated Game Tuning & Graceful Rollback verified.")

    def test_04_web_bridge_daemon_endpoints(self):
        """Verifies local Web Bridge Daemon REST endpoints on port 8770."""
        bridge = AntimagistWebBridgeDaemon(port=8770)
        bridge.start_bridge(start_game_sentinel=False)

        try:
            # 1. Telemetry
            with urllib.request.urlopen("http://127.0.0.1:8770/api/v2/telemetry") as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertIn("cpu_percent", data)
                self.assertIn("ram_percent", data)
                self.assertIn("gpu_temp", data)
                self.assertIn("system_health", data)

            # 2. Status
            with urllib.request.urlopen("http://127.0.0.1:8770/api/v2/status") as resp:
                self.assertEqual(resp.status, 200)
                status_data = json.loads(resp.read().decode())
                self.assertEqual(status_data["license_state"], "PRO_LICENSED")
                self.assertTrue(status_data["pro_unlocked"])

            # 3. Static dashboard.html
            with urllib.request.urlopen("http://127.0.0.1:8770/dashboard") as resp:
                self.assertEqual(resp.status, 200)
                html_data = resp.read().decode("utf-8", errors="ignore")
                self.assertIn("ANTIMAGIST", html_data)
                self.assertIn("glass-panel", html_data)

            print("  [+] Test 4: Web Bridge Daemon REST Endpoints verified.")
        finally:
            bridge.stop_bridge()

    def test_05_web_bridge_zero_trust_action_dispatch(self):
        """Verifies remote execution of whitelisted actions and blocking of malformed inputs."""
        bridge = AntimagistWebBridgeDaemon(port=8771)
        bridge.start_bridge(start_game_sentinel=False)

        try:
            # Authorized action: flush_ram
            req_data = json.dumps({"action": "flush_ram", "params": {}}).encode()
            req = urllib.request.Request("http://127.0.0.1:8771/api/v2/action", data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                res = json.loads(resp.read().decode())
                self.assertTrue(res["success"])
                self.assertIn("flushed", res["message"].lower())

            # Unauthorized / malformed action: inject shell command
            bad_data = json.dumps({"action": "flush_ram; rm -rf /", "params": {}}).encode()
            bad_req = urllib.request.Request("http://127.0.0.1:8771/api/v2/action", data=bad_data, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(bad_req) as resp:
                    res_bad = json.loads(resp.read().decode())
                    self.assertFalse(res_bad["success"])
            except urllib.error.HTTPError as he:
                self.assertEqual(he.code, 400)

            print("  [+] Test 5: Zero-Trust Action Dispatching & Injection Defense verified.")
        finally:
            bridge.stop_bridge()

    def test_06_apex_app_subsystem_bindings(self):
        """Verifies that AntimagistV4ApexApp initializes and binds ultra_game_sentinel and web_bridge."""
        from antimagist_v4_apex import AntimagistV4ApexApp
        app = AntimagistV4ApexApp()
        self.assertTrue(hasattr(app, "ultra_game_sentinel"))
        self.assertTrue(hasattr(app, "web_bridge"))
        self.assertIsNotNone(app.ultra_game_sentinel)
        self.assertIsNotNone(app.web_bridge)
        app.destroy()
        print("  [+] Test 6: Apex App Subsystem Bindings verified.")


if __name__ == "__main__":
    unittest.main()
