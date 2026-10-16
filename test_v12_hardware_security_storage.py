"""
test_v12_hardware_security_storage.py — Antimagist V12 Enterprise Kernel, Storage & Security Test Suite
======================================================================================================
Automated verification suite testing:
1. GPU VRAM Purger, Hardware Acceleration Guard & Competitive Display Vibrance / HDR Switcher
2. CPU Core Unparking Engine & Physical RAM Speed / XMP Auditor
3. Live Network Connection Radar ("URL Radar") & Anti-Cheat TPM / Hardware Attestation Matrix
4. Real Windows Kernel Job-Object Resource Cage (10% CPU / 500MB RAM hard limit)
5. NVMe SSD S.M.A.R.T. Health, Native TRIM & Component Store DISM Compaction Engine
6. AI Sovereign Workflow Macros (Study Mode, Cinema Mode, Competitive Esports Mode)
"""

import os
import sys
import time
import subprocess
import unittest

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class TestAntimagistV12HardwareSecurityStorage(unittest.TestCase):

    def setUp(self):
        self.start_time = time.time()

    # ========================================================================
    # MODULE 1: GPU VRAM PURGER, HARDWARE ACCEL & VIBRANCE / HDR
    # ========================================================================
    def test_01_gpu_vram_scan_and_purge(self):
        from gpu_sentinel import AntimagistGPUSentinel
        gpu = AntimagistGPUSentinel()

        # 1. Scan background VRAM hogs
        hogs = gpu.scan_background_vram_hogs()
        self.assertIsInstance(hogs, list)
        for h in hogs:
            self.assertIn("name", h)
            self.assertIn("pid", h)
            self.assertIn("vram_mb", h)

        # 2. Free background VRAM and flush DWM
        ok, msg, stats = gpu.free_background_vram()
        self.assertTrue(ok)
        self.assertIn("trimmed_processes", stats)
        self.assertIn("freed_mb", stats)
        self.assertIn("dwm_flushed", stats)
        self.assertTrue(stats["dwm_flushed"])

    def test_02_display_vibrance_and_hdr(self):
        from display_reflex import AntimagistDisplayReflex
        disp = AntimagistDisplayReflex()

        # 1. Set competitive vibrance gamma ramp (1.35x boost)
        ok, msg = disp.set_competitive_vibrance(boost=1.35)
        self.assertTrue(ok)
        self.assertTrue("Competitive Display Vibrance applied" in msg or "135%" in msg)

        # 2. Reset display gamma ramp to standard 1.0 linear curve
        ok_reset, msg_reset = disp.reset_display_vibrance()
        self.assertTrue(ok_reset)
        self.assertIn("standard", msg_reset.lower())

        # 3. Query HDR status
        hdr_stat = disp.get_hdr_status()
        self.assertIn("hdr_capable_pipeline", hdr_stat)
        self.assertIn("hotkey", hdr_stat)
        self.assertIsInstance(hdr_stat["hdr_capable_pipeline"], bool)

    # ========================================================================
    # MODULE 2: CPU CORE UNPARKING & RAM SPEED / XMP INSPECTOR
    # ========================================================================
    def test_03_cpu_core_unparking(self):
        from core_director import AntimagistCoreDirector
        cd = AntimagistCoreDirector()

        # 1. Audit core parking state
        audit = cd.audit_cpu_core_parking()
        self.assertIn("min_unparked_pct", audit)
        self.assertIn("is_fully_unparked", audit)
        self.assertIn("status_label", audit)

        # 2. Apply 100% core unparking
        ok, msg = cd.unpark_all_cpu_cores(True)
        self.assertTrue(ok)
        self.assertIn("100%", msg)

        # 3. Verify unparked
        audit_after = cd.audit_cpu_core_parking()
        self.assertEqual(audit_after["min_unparked_pct"], 100)
        self.assertTrue(audit_after["is_fully_unparked"])

    def test_04_ram_speed_and_xmp(self):
        from core_director import AntimagistCoreDirector
        cd = AntimagistCoreDirector()

        ram = cd.audit_physical_ram_speed_and_xmp()
        self.assertIn("configured_speed_mhz", ram)
        self.assertIn("slots_populated", ram)
        self.assertIn("total_ram_gb", ram)
        self.assertIn("channel_mode", ram)
        self.assertIn("xmp_active", ram)
        self.assertIn("status_label", ram)

        # Real machine verification
        self.assertGreater(ram["configured_speed_mhz"], 0)
        self.assertGreaterEqual(ram["slots_populated"], 1)
        self.assertGreater(ram["total_ram_gb"], 0)

    # ========================================================================
    # MODULE 3: LIVE NETWORK CONNECTION RADAR & ANTI-CHEAT TPM ATTESTATION
    # ========================================================================
    def test_05_url_radar_and_entropy(self):
        from url_analyzer import AntimagistURLAnalyzer
        analyzer = AntimagistURLAnalyzer()

        # 1. Test Shannon entropy calculations
        e_normal = analyzer.calculate_shannon_entropy("google.com")
        e_dga = analyzer.calculate_shannon_entropy("xk89qzz1b4p902laq33.biz")
        self.assertGreater(e_dga, e_normal)
        self.assertGreaterEqual(e_normal, 0.0)

        # 2. Query live socket connections
        conns = analyzer.get_live_network_connections(limit=30)
        self.assertIsInstance(conns, list)
        if conns:
            c = conns[0]
            self.assertIn("pid", c)
            self.assertIn("process_name", c)
            self.assertIn("remote_ip", c)
            self.assertIn("status", c)
            self.assertIn("threat_level", c)

        # 3. Test firewall blocking dry-run / command generation
        ok_fw, msg_fw = analyzer.block_ip_in_firewall("192.0.2.1", rule_name="Antimagist_Test_Block")
        self.assertIsInstance(ok_fw, bool)
        self.assertIsInstance(msg_fw, str)
        self.assertGreater(len(msg_fw), 0)

    def test_06_anticheat_tpm_attestation(self):
        from tpm_hardware_attestor import AntimagistTPMAttestor
        attestor = AntimagistTPMAttestor()

        rep = attestor.audit_anticheat_hardware_readiness()
        self.assertIn("tpm_2_0", rep)
        self.assertIn("secure_boot", rep)
        self.assertIn("hvci_memory_integrity", rep)
        self.assertIn("hardware_dep", rep)
        self.assertIn("anti_cheat_compatibility", rep)
        self.assertIn("tier_rating", rep)
        self.assertIn("remediations", rep)

        # Check required anti-cheat targets in matrix
        ac = rep["anti_cheat_compatibility"]
        self.assertIn("riot_vanguard", ac)
        self.assertIn("faceit_ac", ac)
        self.assertIn("easy_anti_cheat", ac)
        self.assertIn("battleye", ac)

        for name, entry in ac.items():
            self.assertIn("name", entry)
            self.assertIn("status", entry)
            self.assertIn("supported", entry)

    # ========================================================================
    # MODULE 4: REAL WINDOWS KERNEL JOB-OBJECT RESOURCE CAGE
    # ========================================================================
    def test_07_job_object_process_cage(self):
        from process_cage_job_object import AntimagistJobObjectCage
        cage = AntimagistJobObjectCage()

        # Spawn a disposable background process to cage
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        pid = proc.pid
        try:
            # 1. Cage process to 10% CPU and 500 MB RAM
            ok, msg = cage.cage_process(pid, cpu_rate_pct=10, memory_limit_mb=500)
            self.assertTrue(ok)
            self.assertIn("caged", msg.lower())

            # 2. Verify in caged inventory
            caged_list = cage.list_caged_processes()
            pids = [item["pid"] for item in caged_list]
            self.assertIn(pid, pids)

            # 3. Terminate caged process via Job Object
            ok_term, msg_term = cage.terminate_caged_process(pid)
            self.assertTrue(ok_term)

            # Verify process exited
            try:
                proc.wait(timeout=3)
            except Exception:
                pass
            self.assertIsNotNone(proc.poll())
        finally:
            if proc.poll() is None:
                proc.kill()
            cage.close_all_cages()

    # ========================================================================
    # MODULE 5: NVMe SSD S.M.A.R.T. HEALTH, TRIM & DISM ENGINE
    # ========================================================================
    def test_08_nvme_health_trim_and_dism(self):
        from storage_accelerator import StorageAcceleratorEngine
        engine = StorageAcceleratorEngine()

        # 1. Audit NVMe physical disk health
        nvme = engine.audit_nvme_health()
        self.assertIn("status_label", nvme)
        self.assertIn("disks", nvme)
        self.assertIsInstance(nvme["disks"], list)

        # 2. Execute NVMe TRIM (handled cleanly with elevation fallback)
        ok_trim, msg_trim = engine.execute_nvme_trim("C")
        self.assertIsInstance(ok_trim, bool)
        self.assertIsInstance(msg_trim, str)
        self.assertGreater(len(msg_trim), 0)

        # 3. Execute DISM Component Store Analyze (non-destructive)
        progress_events = []
        def _on_prog(line, pct):
            progress_events.append((line, pct))

        ok_dism, msg_dism = engine.execute_dism_cleanup(analyze_only=True, progress_callback=_on_prog)
        self.assertIsInstance(ok_dism, bool)
        self.assertIsInstance(msg_dism, str)
        self.assertGreater(len(msg_dism), 0)

    # ========================================================================
    # MODULE 6: AI SOVEREIGN WORKFLOW MACROS & INTENT PARSING
    # ========================================================================
    def test_09_ai_custom_workflow_macros_and_intents(self):
        from ai_kernel_agent import AntimagistAIAgent
        from antimagist_v3_ultra import AntimagistOptimizer, AntimagistScanner, AntimagistSecuritySandbox
        from network_monitor import AntimagistNetworkMonitor

        sandbox = AntimagistSecuritySandbox()
        optimizer = AntimagistOptimizer(sandbox)
        scanner = AntimagistScanner()
        net_mon = AntimagistNetworkMonitor()

        agent = AntimagistAIAgent(
            optimizer_core=optimizer,
            scanner_core=scanner,
            network_monitor=net_mon,
            security_sandbox=sandbox
        )

        # 1. Direct macro executions
        ok_s, msg_s = agent.action_macro_study_mode()
        self.assertTrue(ok_s)
        self.assertIn("Study Mode Active", msg_s)

        ok_c, msg_c = agent.action_macro_cinema_mode()
        self.assertTrue(ok_c)
        self.assertIn("Cinema Mode Active", msg_c)

        ok_e, msg_e = agent.action_macro_competitive_mode()
        self.assertTrue(ok_e)
        self.assertIn("Competitive Mode Active", msg_e)

        # 2. Copilot Natural Language Intent Routing
        res_study = agent.process_query("activate study mode")
        self.assertIn("Study Mode", res_study)

        res_cinema = agent.process_query("cinema mode")
        self.assertIn("Cinema Mode", res_cinema)

        res_esports = agent.process_query("esports mode")
        self.assertTrue("Competitive Mode Active" in res_esports or "esports" in res_esports.lower())

        res_vram = agent.process_query("purge vram")
        self.assertIn("VRAM Purger", res_vram)

        res_unpark = agent.process_query("unpark cores")
        self.assertIn("Core Unparking", res_unpark)

        res_ram = agent.process_query("check ram speed")
        self.assertIn("RAM", res_ram)

        res_anticheat = agent.process_query("tpm attestation")
        self.assertIn("Anti-Cheat", res_anticheat)


if __name__ == "__main__":
    unittest.main()
