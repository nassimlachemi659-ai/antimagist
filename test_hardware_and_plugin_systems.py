"""
test_hardware_and_plugin_systems.py — Automated Verification Test Suite
=======================================================================
Verifies the 5 deep hardware, network hop, game-config, and self-expanding AI systems:
1. Live Hardware Profile Switcher (Esports Ultra, Daily Balanced, Eco/UPS Guard, cycle)
2. 1:1 Raw Mouse Input Enforcer (Registry & SystemParametersInfo)
3. CS2 & Steam Workshop Connection Doctor + Pro Config
4. Dual-Hop Latency Diagnostics (Local Gateway vs External Edge)
5. Zero-Fragmentation Auto-MTU Discovery (Binary Search)
6. Live GPU Clocks, Power Draw, Thermal Headroom & Reset Driver Stack
7. Self-Expanding AI Plugin Builder (AST Validation, dynamic file creation, execution)
"""

import os
import sys
import time
import unittest

# Ensure UTF-8 console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class TestAntimagistHardwareAndPluginSystems(unittest.TestCase):

    def test_01_hardware_profile_switcher(self):
        """Test Live Hardware Profile Switcher real OS transitions."""
        from profile_switcher import AntimagistProfileSwitcher, HARDWARE_PROFILES
        switcher = AntimagistProfileSwitcher()

        # Check existing profile
        init_p = switcher.get_active_profile()
        self.assertIn(init_p["key"], HARDWARE_PROFILES)

        # Switch to daily balanced
        ok1, msg1, p1 = switcher.switch_profile("daily_balanced")
        self.assertTrue(ok1)
        self.assertEqual(p1["key"], "daily_balanced")
        self.assertEqual(p1["name"], "⚡ DAILY BALANCED")

        # Switch to eco ups guard
        ok2, msg2, p2 = switcher.switch_profile("eco_ups_guard")
        self.assertTrue(ok2)
        self.assertEqual(p2["key"], "eco_ups_guard")
        self.assertEqual(p2["cpu_max_pct"], 65)

        # Switch to esports ultra
        ok3, msg3, p3 = switcher.switch_profile("esports_ultra")
        self.assertTrue(ok3)
        self.assertEqual(p3["key"], "esports_ultra")
        self.assertEqual(p3["timer_ms"], 0.5)

        # Cycle profile
        ok4, msg4, p4 = switcher.cycle_profile()
        self.assertTrue(ok4)
        self.assertEqual(p4["key"], "daily_balanced")

        # Return to esports ultra
        switcher.switch_profile("esports_ultra")

    def test_02_raw_mouse_input_enforcer(self):
        """Test 1:1 Raw Mouse Input inspection and enforcement."""
        from cs2_optimizer import AntimagistCS2Optimizer
        optimizer = AntimagistCS2Optimizer()

        status = optimizer.get_raw_mouse_status()
        self.assertIn("is_raw_1to1", status)
        self.assertIn("mouse_speed", status)

        ok, msg = optimizer.enforce_raw_mouse_input()
        self.assertTrue(ok)
        self.assertIn("Raw Mouse", msg)

        # Verify registry and live state after enforcement
        status_after = optimizer.get_raw_mouse_status()
        self.assertEqual(status_after["mouse_speed"], "0")
        self.assertEqual(status_after["threshold1"], "0")
        self.assertEqual(status_after["threshold2"], "0")

    def test_03_cs2_steam_workshop_doctor(self):
        """Test Steam UDP socket & workshop repair and pro config injection."""
        from cs2_optimizer import AntimagistCS2Optimizer
        optimizer = AntimagistCS2Optimizer()

        ok, msg, details = optimizer.repair_steam_workshop_connection()
        self.assertTrue(ok)
        self.assertIn("port_scan", details)
        self.assertTrue(len(details["port_scan"]) > 0)

        ok_cfg, msg_cfg = optimizer.apply_pro_low_latency_config()
        self.assertTrue(ok_cfg)
        self.assertIn("CS2 Pro Low-Latency Config", msg_cfg)

    def test_04_dual_hop_latency_radar(self):
        """Test Dual-Hop Diagnostics for Gateway Router vs External ISP Edge."""
        from hop_radar_mtu import AntimagistHopRadarMTU
        radar = AntimagistHopRadarMTU()

        gw = radar.get_default_gateway()
        self.assertTrue(bool(gw and len(gw.split(".")) == 4))

        iface = radar.get_active_interface()
        self.assertTrue(bool(iface))

        diag = radar.run_dual_hop_diagnostic()
        self.assertIn("router_latency_ms", diag)
        self.assertIn("external_latency_ms", diag)
        self.assertIn("bottleneck", diag)
        self.assertTrue(diag["router_latency_ms"] >= 0)
        self.assertTrue(diag["external_latency_ms"] >= 0)

    def test_05_zero_fragmentation_mtu_discovery(self):
        """Test Binary Search Ping Sweep for Zero-Fragmentation MTU."""
        from hop_radar_mtu import AntimagistHopRadarMTU
        radar = AntimagistHopRadarMTU()

        payload, mtu, msg = radar.discover_optimal_mtu()
        self.assertTrue(1300 <= payload <= 1472)
        self.assertEqual(mtu, payload + 28)
        self.assertTrue(1328 <= mtu <= 1500)
        self.assertIn("Zero-fragmentation", msg)

    def test_06_gpu_sentinel_clocks_headroom_reset(self):
        """Test GPU Core/VRAM clocks, power draw, thermal headroom, and reset driver stack."""
        from gpu_sentinel import AntimagistGPUSentinel
        sentinel = AntimagistGPUSentinel()

        metrics = sentinel.get_live_gpu_metrics()
        self.assertIn("core_clock_mhz", metrics)
        self.assertIn("memory_clock_mhz", metrics)
        self.assertIn("power_draw_w", metrics)
        self.assertIn("thermal_headroom_c", metrics)
        self.assertTrue(metrics["thermal_headroom_c"] >= 0)

        # Test Reset GPU Driver Stack (Win + Ctrl + Shift + B)
        ok_reset, msg_reset = sentinel.reset_gpu_driver_stack()
        self.assertTrue(ok_reset)
        self.assertIn("Win + Ctrl + Shift + B", msg_reset)

    def test_07_self_expanding_ai_plugin_builder(self):
        """Test dynamic AI tool creation, AST syntax validation, and immediate execution."""
        from ai_plugin_builder import AntimagistPluginBuilder
        builder = AntimagistPluginBuilder()

        prompt = "create a new tool to audit ram memory"
        ok, summary, meta = builder.build_tool_from_prompt(prompt)
        self.assertTrue(ok)
        self.assertIn("audit_ram_memory", meta["id"])
        self.assertTrue(os.path.exists(meta["file_path"]))
        self.assertIn("initial_execution", meta)

        # Direct execution of newly created plugin
        ok_exec, msg_exec = builder.execute_plugin(meta["id"])
        self.assertTrue(ok_exec)
        self.assertIn("Memory Posture", msg_exec)

        # Discovery test
        plugins = builder.discover_plugins()
        self.assertTrue(any(p["id"] == meta["id"] for p in plugins))


if __name__ == "__main__":
    unittest.main()
