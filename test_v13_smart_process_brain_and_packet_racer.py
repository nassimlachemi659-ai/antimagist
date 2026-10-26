"""
test_v13_smart_process_brain_and_packet_racer.py — Antimagist V13 Closed-Loop Intelligence Test Suite
====================================================================================================
Verifies:
  1. 4-Tier Process Intelligence Classifier & Whitelist (Zero-Trust Protection)
  2. Packet Racer Single-NIC Dual-Route UDP Pacing & QoS Mode
  3. Memory Pacer Bloat Suspension Safe Rejection on Tier 0/1 Processes
  4. Autonomous Guardian & Startup Diagnostic Telemetry Integrity
"""

import os
import sys
import time
import unittest

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from process_classifier import ProcessIntelligenceClassifier
from packet_racer import AntimagistPacketRacer
from memory_pacer import AntimagistMemoryPacer


class TestSmartProcessBrainAndPacketRacer(unittest.TestCase):

    def test_tier_0_kernel_protection(self):
        """Tier 0 processes (OS & Kernel) must NEVER be killable or suspendable."""
        t0_samples = [
            "explorer.exe", "dwm.exe", "csrss.exe", "svchost.exe",
            "MsMpEng.exe", "System", "Registry", "audiodg.exe"
        ]
        for name in t0_samples:
            info = ProcessIntelligenceClassifier.classify(name)
            self.assertEqual(info["tier"], 0, f"Expected {name} to be Tier 0")
            self.assertEqual(info["badge"], "OS", f"Expected {name} badge to be OS")
            self.assertFalse(info["can_kill"], f"Tier 0 process {name} must NOT be killable")
            self.assertFalse(info["can_suspend"], f"Tier 0 process {name} must NOT be suspendable")
            self.assertFalse(ProcessIntelligenceClassifier.is_kill_allowed(name))
            self.assertFalse(ProcessIntelligenceClassifier.is_suspend_allowed(name))

    def test_tier_1_driver_protection(self):
        """Tier 1 Peripheral & Hardware Drivers must NEVER be killable or suspendable."""
        driver_samples = ["NGENUITY.exe", "lghub.exe", "RazerCentralService.exe", "steelseriesgg.exe"]
        for name in driver_samples:
            info = ProcessIntelligenceClassifier.classify(name)
            self.assertEqual(info["tier"], 1, f"Expected {name} to be Tier 1")
            self.assertEqual(info["badge"], "DRIVER", f"Expected {name} badge to be DRIVER")
            self.assertFalse(info["can_kill"], f"Hardware driver {name} must NOT be killable")
            self.assertFalse(info["can_suspend"], f"Hardware driver {name} must NOT be suspendable")
            self.assertTrue(info["can_trim"], f"Driver {name} should allow safe working set trimming")

    def test_tier_1_user_apps_and_games_protection(self):
        """Tier 1 Voice, IDE tools, Games, and Anti-cheats must NEVER be killed or suspended by cleaners."""
        app_samples = [
            "Discord.exe", "Antigravity.exe", "Code.exe", "python.exe",
            "cs2.exe", "vgc.exe", "EasyAntiCheat.exe", "BEService.exe"
        ]
        for name in app_samples:
            info = ProcessIntelligenceClassifier.classify(name)
            self.assertEqual(info["tier"], 1, f"Expected {name} to be Tier 1")
            self.assertEqual(info["badge"], "APP", f"Expected {name} badge to be APP")
            self.assertFalse(info["can_kill"], f"Protected app {name} must NOT be killable")
            self.assertFalse(info["can_suspend"], f"Protected app {name} must NOT be suspendable")
            self.assertTrue(info["can_trim"], f"Protected app {name} allows safe RAM trimming")

    def test_tier_2_and_3_bloatware_classification(self):
        """Tier 2 (Browsers/helpers) and Tier 3 (Bloatware) must be actionable for trimming and suspending."""
        tier_2_samples = ["chrome.exe", "msedge.exe", "steamwebhelper.exe", "EpicWebHelper.exe"]
        for name in tier_2_samples:
            info = ProcessIntelligenceClassifier.classify(name)
            self.assertEqual(info["tier"], 2)
            self.assertTrue(info["can_kill"])
            self.assertTrue(info["can_suspend"])
            self.assertTrue(info["can_trim"])

        tier_3_samples = ["OneDrive.exe", "SearchApp.exe", "WidgetService.exe", "CompatTelRunner.exe", "GameBar.exe"]
        for name in tier_3_samples:
            info = ProcessIntelligenceClassifier.classify(name)
            self.assertEqual(info["tier"], 3)
            self.assertEqual(info["badge"], "BLOAT")
            self.assertTrue(info["can_kill"])
            self.assertTrue(info["can_suspend"])

    def test_memory_pacer_rejects_protected_processes(self):
        """Memory Pacer must refuse to suspend any Tier 0 or Tier 1 process."""
        pacer = AntimagistMemoryPacer()
        
        # Test rejection of Tier 1 app
        ok_d, msg_d, _ = pacer.suspend_bloat_process("Discord.exe")
        self.assertFalse(ok_d)
        self.assertIn("whitelisted", msg_d)

        # Test rejection of Tier 1 driver
        ok_n, msg_n, _ = pacer.suspend_bloat_process("NGENUITY.exe")
        self.assertFalse(ok_n)
        self.assertIn("whitelisted", msg_n)

        # Test rejection of Tier 0 system component
        ok_e, msg_e, _ = pacer.suspend_bloat_process("explorer.exe")
        self.assertFalse(ok_e)
        self.assertIn("whitelisted", msg_e)

    def test_packet_racer_single_nic_mode(self):
        """Packet Racer must detect single adapter and engage Single-NIC Dual-Route Mode with live telemetry."""
        racer = AntimagistPacketRacer()
        adapters = racer.audit_network_adapters()
        self.assertGreaterEqual(len(adapters), 1, "Must discover at least 1 network adapter")

        # Initial standby telemetry must not have 0.0 ms placeholders
        tel_init = racer.get_racing_telemetry()
        self.assertGreater(tel_init["effective_rtt_ms"], 0.0)
        self.assertGreater(tel_init["path_a_rtt_ms"], 0.0)
        self.assertGreater(tel_init["path_b_rtt_ms"], 0.0)
        self.assertEqual(tel_init["active_socket_pairs"], 2)
        self.assertEqual(tel_init["packet_loss_pct"], 0.00)

        # Start racing
        ok, msg = racer.start_packet_racing()
        self.assertTrue(ok)
        self.assertTrue(racer.is_racing)
        self.assertIn("online", msg)

        # Allow 3 ticks of parallel UDP racing
        time.sleep(0.35)

        tel = racer.get_racing_telemetry()
        self.assertTrue(tel["is_racing"])
        self.assertGreater(tel["raced_packets_count"], 0)
        self.assertGreater(tel["effective_rtt_ms"], 0.0)
        self.assertGreaterEqual(tel["jitter_reduction_pct"], 20.0)
        self.assertEqual(tel["packet_loss_pct"], 0.00)

        if len(adapters) == 1:
            self.assertEqual(tel["mode"], "Single-NIC Dual-Route UDP Pacing & QoS Mode")
            self.assertIn("Route A", tel["path_a_name"])
            self.assertIn("Route B", tel["path_b_name"])

        # Stop racing cleanly
        ok_stop, msg_stop = racer.stop_packet_racing()
        self.assertTrue(ok_stop)
        self.assertFalse(racer.is_racing)


if __name__ == "__main__":
    unittest.main()
