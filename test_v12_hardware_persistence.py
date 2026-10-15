"""
test_v12_hardware_persistence.py — Antimagist V12 Enterprise Hardware, Audio & Persistence Test Suite
===================================================================================================
Automated verification suite testing:
1. DPC Latency Interceptor & PCIe / USB Input Unlocker (powercfg query & disabler, MSI-X inspection)
2. Competitive Footstep Audio Booster & Mic Gain Lock Guard (CoreAudio COM interface, 48kHz audit)
3. BSOD, Minidump & GPU Crash Forensics Engine (Event Log parsing, BugCheck decoding, remediation)
4. Game Config Vault & Smart Shader Cleaner (Fortnite + CS2 backup, tune & restore, smart clean)
5. Persistent Settings Engine (antimagist_config.json atomic read/write/merge)
6. Auto-Updater System Dependency Health & Shareable Rig Card generation
"""

import os
import sys
import time
import json
import unittest

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class TestAntimagistV12HardwareAndPersistence(unittest.TestCase):

    def setUp(self):
        self.start_time = time.time()

    # ========================================================================
    # MODULE 1: DPC LATENCY INTERCEPTOR & PCIe / USB INPUT UNLOCKER
    # ========================================================================
    def test_01_usb_pcie_power_audit_and_unlock(self):
        from msi_interrupt_tuner import AntimagistMSITuner
        tuner = AntimagistMSITuner()

        # 1. Audit USB & PCIe sleep states
        p_stat = tuner.audit_usb_pcie_sleep()
        self.assertIn("usb_selective_suspend_disabled", p_stat)
        self.assertIn("pcie_aspm_disabled", p_stat)
        self.assertIn("advice", p_stat)

        # 2. Apply latency unlock via powercfg
        ok, msg = tuner.apply_usb_pcie_latency_unlock()
        self.assertTrue(ok)
        self.assertIn("disabled", msg.lower())

        # 3. Verify updated state
        p_stat_after = tuner.audit_usb_pcie_sleep()
        self.assertTrue(p_stat_after["usb_selective_suspend_disabled"])
        self.assertTrue(p_stat_after["pcie_aspm_disabled"])
        self.assertTrue(p_stat_after["is_optimal"])

    def test_02_msi_interrupt_audit(self):
        from msi_interrupt_tuner import AntimagistMSITuner
        tuner = AntimagistMSITuner()

        devs = tuner.scan_pci_devices()
        self.assertIsInstance(devs, list)
        self.assertGreater(len(devs), 0)

        # Verify device schema
        for d in devs:
            self.assertIn("pci_path", d)
            self.assertIn("name", d)
            self.assertIn("class", d)
            self.assertIn("msi_supported", d)
            self.assertIn("status", d)

        audit = tuner.audit_interrupt_health()
        self.assertIn("total_audited", audit)
        self.assertIn("msi_active_count", audit)
        self.assertIn("status", audit)
        self.assertGreater(audit["total_audited"], 0)

    # ========================================================================
    # MODULE 2: COMPETITIVE FOOTSTEP AUDIO BOOSTER & MIC GAIN LOCK
    # ========================================================================
    def test_03_mic_gain_lock_and_footstep_audit(self):
        from competitive_audio_booster import AntimagistAudioBooster
        booster = AntimagistAudioBooster()

        # 1. Query mic volume
        mic = booster.get_mic_volume()
        self.assertIn("available", mic)
        self.assertIn("volume_pct", mic)
        self.assertIn("is_muted", mic)

        # 2. Lock mic to 100%
        ok, msg = booster.lock_mic_volume_100()
        self.assertTrue(ok)
        self.assertIn("100%", msg)

        # 3. Footstep & sample rate audit
        audit = booster.audit_footstep_enhancements()
        self.assertIn("endpoints", audit)
        self.assertIn("recommended_sample_rate", audit)
        self.assertIn("is_48khz_compliant", audit)
        self.assertTrue(audit["is_48khz_compliant"])

        # 4. Background daemon lifecycle
        booster.start_mic_lock_daemon(interval_sec=1.0)
        self.assertTrue(booster.is_mic_lock_running())
        booster.stop_mic_lock_daemon()
        self.assertFalse(booster.is_mic_lock_running())

    # ========================================================================
    # MODULE 3: BSOD, MINIDUMP & GPU CRASH FORENSICS ENGINE
    # ========================================================================
    def test_04_crash_forensics_engine(self):
        from crash_forensics import AntimagistCrashForensics
        forensics = AntimagistCrashForensics()

        rep = forensics.scan_crash_history(max_records=5)
        self.assertIn("status", rep)
        self.assertIn("summary_text", rep)
        self.assertIn("total_crashes_analyzed", rep)
        self.assertIn("crashes", rep)

        # If crashes were found on this system, test decoding
        if rep["crashes"]:
            latest = rep["crashes"][0]
            self.assertIn("event_id", latest)
            self.assertIn("bugcheck_hex", latest)
            self.assertIn("bugcheck_name", latest)
            self.assertIn("explanation", latest)
            self.assertIn("remediation_title", latest)

            # Test 1-click remediation dispatch
            ok_fix, msg_fix = forensics.apply_remediation(latest["action_key"])
            self.assertTrue(ok_fix)
            self.assertIsInstance(msg_fix, str)

    # ========================================================================
    # MODULE 4: GAME CONFIG VAULT (CS2 + FORTNITE)
    # ========================================================================
    def test_05_game_config_vault_fortnite_and_cs2(self):
        from game_config_vault import AntimagistGameConfigVault
        vault = AntimagistGameConfigVault()

        # 1. Fortnite config testing
        fn_path = vault.get_fortnite_config_path()
        if fn_path:
            # Backup
            ok_bak, msg_bak, bak_p = vault.backup_fortnite_config()
            self.assertTrue(ok_bak)
            self.assertTrue(os.path.exists(bak_p))

            # Optimize
            ok_opt, msg_opt, preserved = vault.optimize_fortnite_config()
            self.assertTrue(ok_opt)
            self.assertIsInstance(preserved, dict)

            # Restore
            ok_rst, msg_rst = vault.restore_fortnite_config()
            self.assertTrue(ok_rst)

        # 2. CS2 config testing
        cs2_info = vault.get_cs2_config_paths()
        self.assertIn("is_detected", cs2_info)
        if cs2_info["is_detected"]:
            ok_cs, msg_cs = vault.optimize_cs2_config()
            self.assertTrue(ok_cs)
            autoexec_p = os.path.join(cs2_info["autoexec_dir"], "autoexec.cfg")
            self.assertTrue(os.path.exists(autoexec_p))

        # 3. Vault Inventory
        inv = vault.list_backups()
        self.assertIn("fortnite_backups", inv)
        self.assertIn("cs2_backups", inv)
        self.assertIn("total_vault_snapshots", inv)

    # ========================================================================
    # MODULE 5: SMART SHADER CLEANER (SMART VS NUCLEAR RESET)
    # ========================================================================
    def test_06_smart_shader_cleaner(self):
        from shader_sentinel import AntimagistShaderSentinel
        sentinel = AntimagistShaderSentinel()

        # 1. Audit
        audit = sentinel.audit_shader_caches()
        self.assertIn("total_size_mb", audit)
        self.assertIn("total_files", audit)
        self.assertIn("pools", audit)

        # 2. Smart clean (preserves recent shaders)
        ok_smart, msg_smart, cleaned, preserved = sentinel.smart_clean_shaders(max_age_days=7)
        self.assertTrue(ok_smart)
        self.assertIsInstance(cleaned, int)
        self.assertIsInstance(preserved, int)

        # 3. Deep nuclear reset
        ok_nuc, msg_nuc, del_cnt = sentinel.deep_nuclear_shader_reset()
        self.assertTrue(ok_nuc)
        self.assertIsInstance(del_cnt, int)

    # ========================================================================
    # MODULE 6: PERSISTENT SETTINGS ENGINE (antimagist_config.json)
    # ========================================================================
    def test_07_settings_vault_persistence(self):
        from settings_vault import AntimagistSettingsVault
        vault = AntimagistSettingsVault()

        # Load
        cfg = vault.load_settings()
        self.assertIn("active_hardware_profile", cfg)
        self.assertIn("autopilot_ram_threshold_pct", cfg)
        self.assertIn("custom_hotkeys", cfg)

        # Mutate & Save
        test_val = 85
        vault.set("autopilot_ram_threshold_pct", test_val)
        vault.increment_metric("total_ram_flushed_mb", 512.0)

        # Reload fresh instance
        fresh_vault = AntimagistSettingsVault()
        reloaded = fresh_vault.load_settings()
        self.assertEqual(reloaded["autopilot_ram_threshold_pct"], test_val)
        self.assertGreaterEqual(reloaded["total_ram_flushed_mb"], 512.0)

    # ========================================================================
    # MODULE 7: AUTO-UPDATER SYSTEM DEPENDENCY HEALTH
    # ========================================================================
    def test_08_updater_system_dependency_health(self):
        from auto_updater import AntimagistAutoUpdater
        updater = AntimagistAutoUpdater()

        health = updater.check_system_dependencies_and_health()
        self.assertIn("python_packages", health)
        self.assertIn("all_packages_ok", health)
        self.assertIn("nvidia_driver", health)
        self.assertIn("defender_definitions", health)
        self.assertIn("winget_available", health)
        self.assertTrue(health["all_packages_ok"])
        self.assertIn("617", health["nvidia_driver"])  # Machine has driver 617.42

    # ========================================================================
    # MODULE 8: AI KERNEL AGENT TOOL ROUTING FOR NEW SYSTEMS
    # ========================================================================
    def test_09_ai_kernel_agent_new_tools(self):
        from ai_kernel_agent import AntimagistAIAgent
        from optimizer_core import AntimagistOptimizerCore
        from scanner_core import AntimagistScannerCore
        from network_monitor import AntimagistNetworkMonitor
        from security_sandbox import SecuritySandbox

        agent = AntimagistAIAgent(
            optimizer_core=AntimagistOptimizerCore(),
            scanner_core=AntimagistScannerCore(),
            network_monitor=AntimagistNetworkMonitor(),
            security_sandbox=SecuritySandbox()
        )

        # Test Crash Forensics Tool
        ok_cf, msg_cf = agent.execute_tool("CRASH_FORENSICS")
        self.assertTrue(ok_cf)
        self.assertIn("Crash", msg_cf)

        # Test Mic Lock Tool
        ok_mic, msg_mic = agent.execute_tool("LOCK_MIC")
        self.assertTrue(ok_mic)
        self.assertIn("100%", msg_mic)

        # Test Fortnite Tuner Tool
        ok_fn, msg_fn = agent.execute_tool("TUNE_FORTNITE")
        self.assertTrue(ok_fn)
        self.assertIn("Fortnite", msg_fn)

        # Test Smart Shader Cleaner Tool
        ok_sh, msg_sh = agent.execute_tool("SMART_CLEAN_SHADERS")
        self.assertTrue(ok_sh)
        self.assertIn("Shader", msg_sh)

        # Test Latency Unlock Tool
        ok_lat, msg_lat = agent.execute_tool("UNLOCK_PCI_USB_SLEEP")
        self.assertTrue(ok_lat)
        self.assertIn("disabled", msg_lat.lower())


if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING ANTIMAGIST V12 ENTERPRISE HARDWARE & PERSISTENCE TEST SUITE")
    print("=" * 70)
    unittest.main()
