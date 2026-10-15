"""
test_copilot_intelligence.py — Verification Suite for Upgraded Sovereign AI Copilot
===================================================================================
Tests:
1. Conversational Banter & Repetition Critique Handling (English & Arabic)
2. Project Status & Finalization Queries
3. Real-Time Diagnostics (Lag, Stutter, Frametime Pacing)
4. Memory Investigation & Top Working-Set Inspection
5. CPU Load & Thermal Throttling Insights
6. Storage Telemetry & NVMe TRIM
7. Network Ping, Packet Loss & Gaming QoS
8. DPC Latency & Driver Interrupt Diagnosis
9. Esports Profiling (CS2, Valorant, Fortnite, Apex)
10. Windows 11 Bloatware & Telemetry Auditing
11. Security Sandbox & Port Auditing
12. Direct Action Execution (Boost RAM, Clean Cache, Flush DNS)
13. Zero-Trust Safety Firewall Interception of Destructive Commands
14. Response Uniqueness & Absolute Elimination of Canned Fallback
"""

import os
import sys
import time
import unittest
from typing import Dict, Any

from ai_kernel_agent import AntimagistAIAgent
from antimagist_v3_ultra import AntimagistOptimizer, AntimagistScanner, AntimagistSecuritySandbox
from network_monitor import AntimagistNetworkMonitor


class TestCopilotIntelligence(unittest.TestCase):
    """Deep verification suite for Antimagist AI Copilot conversational & systems intelligence."""

    @classmethod
    def setUpClass(cls):
        os.environ["ANTIMAGIST_CI_MOCK_HARDWARE"] = "1"
        os.environ["CI"] = "true"

        cls.sandbox = AntimagistSecuritySandbox()
        cls.optimizer = AntimagistOptimizer(cls.sandbox)
        cls.scanner = AntimagistScanner()
        cls.net_mon = AntimagistNetworkMonitor()
        cls.agent = AntimagistAIAgent(
            optimizer_core=cls.optimizer,
            scanner_core=cls.scanner,
            network_monitor=cls.net_mon,
            security_sandbox=cls.sandbox,
            api_key=""  # Test offline sovereign kernel
        )
        cls.agent.api_key = ""
        cls.agent._gemini_rate_limited_until = time.time() + 99999

    def test_01_user_complaint_and_banter(self):
        """Verifies AI handles 'stupid / repeating / xDDD / bro' with self-awareness and expert upgrade notice."""
        queries = [
            "the copilot AI is stupid bro ??? he just repeat one thing xDDD fixxx mann",
            "why do you repeat the same thing",
            "are you dumb lol",
            "انت غبي بتكرر نفس الكلام xDDD"
        ]
        for q in queries:
            resp = self.agent.process_query(q)
            self.assertNotIn("Ready for directives. Here is your live system posture", resp)
            self.assertTrue(any(k in resp.lower() for k in ["sovereign", "kernel", "offline", "upgraded", "السيادي", "ترقية"]))
        print("  [+] Test 1: User complaint & banter handled with wit, self-awareness, and technical clarity.")

    def test_02_project_status_and_finalization(self):
        """Verifies AI answers 'what next / end the project' with complete project architecture report."""
        queries = [
            "what next man , the end we need to end the project , sooo give me the last things u want to add or fix or optimize",
            "شو بعدين خلصنا المشروع؟"
        ]
        for q in queries:
            resp = self.agent.process_query(q)
            self.assertTrue(any(k in resp for k in ["Antimagist", "Gold Master", "المشروع", "Malwarebytes"]))
            self.assertTrue(any(k in resp for k in ["46", "67", "Sandbox", "الأمان"]))
        print("  [+] Test 2: Project status & finalization report verified.")

    def test_03_micro_stutter_and_lag_diagnostics(self):
        """Verifies deep frametime and lag analysis with live hardware inspection."""
        resp_en = self.agent.process_query("why is my game lagging and stuttering?")
        self.assertIn("Micro-Stutter & Frametime Analysis", resp_en)
        self.assertIn("CPU", resp_en)
        self.assertIn("RAM", resp_en)
        self.assertIn("DPC", resp_en)

        resp_ar = self.agent.process_query("ليش الالعاب تقطع وتعلق عندي؟")
        self.assertIn("تشخيص اللاق والتقطيع", resp_ar)
        self.assertIn("المعالج", resp_ar)
        self.assertIn("الذاكرة", resp_ar)
        print("  [+] Test 3: Micro-stutter & lag diagnostics verified (bilingual).")

    def test_04_memory_hog_inspection(self):
        """Verifies live inspection of top working-set memory consumers."""
        resp_en = self.agent.process_query("what is eating my ram?")
        self.assertIn("Live Memory Inspection", resp_en)
        self.assertIn("BOOST_RAM", resp_en)
        self.assertIn("Top 5 Working-Set Memory Consumers", resp_en)

        resp_ar = self.agent.process_query("شو ماكل الرام عندي ومخليه ممتلئ؟")
        self.assertIn("فحص مستهلكي الذاكرة", resp_ar)
        self.assertIn("أكثر 5 عمليات", resp_ar)
        print("  [+] Test 4: Memory hog inspection and process analysis verified.")

    def test_05_cpu_load_and_thermals(self):
        """Verifies thermal throttling and high CPU load diagnostics."""
        resp_en = self.agent.process_query("why is my pc so hot and fans are loud?")
        self.assertIn("Thermal & CPU Load Analysis", resp_en)
        self.assertIn("TJMax Threshold", resp_en)

        resp_ar = self.agent.process_query("حرارة المعالج عالية جدا والمراوح صوتها مزعج")
        self.assertIn("تقرير حرارة وحمل المعالج", resp_ar)
        self.assertIn("TJMax", resp_ar)
        print("  [+] Test 5: CPU load and thermal throttling diagnostics verified.")

    def test_06_storage_telemetry_and_nvme_trim(self):
        """Verifies NVMe TRIM and storage health telemetry."""
        resp_en = self.agent.process_query("check my nvme ssd storage space and trim it")
        self.assertIn("Storage Telemetry & NVMe Optimization", resp_en)
        self.assertIn("System Drive (C:)", resp_en)

        resp_ar = self.agent.process_query("افحص مساحة قرص C وسوي trim للهارديسك")
        self.assertIn("تقرير التخزين و SSD TRIM", resp_ar)
        self.assertIn("قرص النظام", resp_ar)
        print("  [+] Test 6: Storage telemetry & NVMe TRIM verified.")

    def test_07_network_latency_and_ping(self):
        """Verifies ping probe and low-latency gaming optimization."""
        resp_en = self.agent.process_query("check ping and reduce packet lag")
        self.assertIn("Gaming Network & Ping Telemetry", resp_en)
        self.assertIn("Cloudflare", resp_en)

        resp_ar = self.agent.process_query("افحص البينغ والنت عندي وسرعه")
        self.assertIn("تحليل شبكة الألعاب والبينغ", resp_ar)
        self.assertIn("OPTIMIZE_PING", resp_ar)
        print("  [+] Test 7: Network latency and ping probe verified.")

    def test_08_dpc_latency_and_driver_interrupts(self):
        """Verifies DPC audit and audio crackle explanation."""
        resp_en = self.agent.process_query("audit dpc latency why do I get audio crackling")
        self.assertIn("DPC Latency & Hardware Driver Interrupt Audit", resp_en)
        self.assertIn("Deferred Procedure Calls", resp_en)
        print("  [+] Test 8: DPC latency and driver interrupts audit verified.")

    def test_09_cs2_and_esports_profiles(self):
        """Verifies CS2 tournament optimizations and other esports engine guidelines."""
        resp_cs2 = self.agent.process_query("optimize pc for counter strike 2 tournament")
        self.assertIn("CS2 Tournament Tuning Deployed", resp_cs2)
        self.assertIn("P-Core Affinity Pinning", resp_cs2)

        resp_val = self.agent.process_query("how should I tune for valorant and apex?")
        self.assertIn("Competitive Esports Game Profile", resp_val)
        self.assertIn("Valorant", resp_val)
        print("  [+] Test 9: CS2 & esports profiles verified.")

    def test_10_win11_bloatware_and_recall(self):
        """Verifies Windows 11 Recall and telemetry stripping recommendations."""
        resp = self.agent.process_query("is windows 11 recall slowing down my pc?")
        self.assertIn("Windows 11 Bloatware & Telemetry Audit", resp)
        self.assertIn("Windows Recall", resp)
        print("  [+] Test 10: Windows 11 bloatware and Recall audit verified.")

    def test_11_security_audit_and_ports(self):
        """Verifies Zero-Trust socket audit and pre-flight checklist."""
        resp = self.agent.process_query("is my pc safe or are there open trojan ports?")
        self.assertIn("Zero-Trust Security Audit", resp)
        self.assertIn("Socket & Network Audit", resp)
        print("  [+] Test 11: Security audit and port monitoring verified.")

    def test_12_direct_action_execution(self):
        """Verifies physical PC optimization actions execute and report metrics."""
        resp_ram = self.agent.process_query("flush ram")
        self.assertIn("BOOST_RAM Executed", resp_ram)

        resp_clean = self.agent.process_query("clean cache junk")
        self.assertIn("CLEAN_CACHE Executed", resp_clean)

        resp_dns = self.agent.process_query("flush dns")
        self.assertIn("FLUSH_DNS Executed", resp_dns)
        print("  [+] Test 12: Direct action executions (RAM, Cache, DNS) verified.")

    def test_13_zero_trust_sandbox_blocks_injection(self):
        """Verifies sandbox blocks destructive system commands."""
        bad_commands = [
            "rmdir /s /q C:\\Windows",
            "format C: /fs:NTFS",
            "rd /s /q C:\\"
        ]
        for cmd in bad_commands:
            resp = self.agent.process_query(cmd)
            self.assertIn("Security Firewall Alert: Command blocked", resp)
        print("  [+] Test 13: Zero-Trust sandbox defense verified against destructive commands.")

    def test_14_response_diversity_and_no_canned_template(self):
        """
        CRITICAL TEST: Verifies that across 15 completely different questions,
        NONE of them return identical outputs and NONE return the obsolete canned template.
        """
        prompts = [
            "the copilot AI is stupid bro ??? he just repeat one thing xDDD",
            "what next man we need to end the project",
            "why is my game lagging?",
            "what is eating my ram?",
            "why is my pc so hot?",
            "check my ssd storage space",
            "check ping and optimize network",
            "audit dpc latency",
            "optimize for cs2",
            "tune for valorant",
            "how to debloat windows 11",
            "is my pc infected with malware?",
            "who are you and what can you do?",
            "what is the meaning of quantum computing in gaming?",
            "شو بتعمل يا صديقي؟"
        ]
        responses = [self.agent.process_query(p) for p in prompts]
        
        # Verify no responses are empty
        for r in responses:
            self.assertGreater(len(r), 40)
            self.assertNotIn("Ready for directives. Here is your live system posture:\n• RAM:", r)

        # Verify uniqueness (all 15 responses are distinct)
        unique_responses = set(responses)
        self.assertEqual(len(unique_responses), len(prompts), "Detected duplicate responses across diverse prompts!")
        print(f"  [+] Test 14: Response diversity verified (15/15 unique, intelligent outputs; 0 canned fallbacks).")


if __name__ == "__main__":
    unittest.main()
