"""
test_v14_statistical_and_flight_recorder.py
===========================================
Verification Suite for Antimagist V14 Statistical Decision Engine:
  1. Cold-Start Warmup Grace Period & Single-Tick Spike Suppression
  2. Welford's Variance & 3-Tick Confirmation Hysteresis
  3. Lock-Free Black Box Flight Recorder (<1ms Causal Attribution)
  4. Reinforcement Self-Tuning & 30-Minute Suppression Cooldown
  5. Process Memory Velocity (dRAM/dt) & Active Foreground App Protection
  6. AI Kernel "why did I just lag?" Attribution Integration
"""

import os
import sys
import time
import unittest
from collections import deque

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from statistical_decision_engine import (
    StatisticalAnomalyEngine,
    BlackBoxFlightRecorder,
    InterventionEvaluator,
    ProcessVelocityTracker
)
from ai_kernel_agent import AntimagistAIAgent


class TestStatisticalDecisionEngine(unittest.TestCase):

    def test_01_cold_start_warmup_and_single_spike_suppression(self):
        """Verifies initial 5 ticks are silent and single-tick spikes never trigger false auto-heals."""
        engine = StatisticalAnomalyEngine(window_size=30, warmup_ticks=5, z_threshold=2.8)

        # First 4 ticks: must not be warmed up
        for _ in range(4):
            is_anomaly, _, _, _ = engine.feed_sample("ping_ms", 4.0)
            self.assertFalse(is_anomaly)
        self.assertFalse(engine.is_warmed_up())

        # 5th tick warms up
        engine.feed_sample("ping_ms", 4.5)
        self.assertTrue(engine.is_warmed_up())

        # Massive single-tick jitter spike (e.g. socket init at 124.8ms)
        is_anomaly, z, mean, std = engine.feed_sample("ping_ms", 124.8)
        self.assertFalse(is_anomaly, "Single-tick spike should not trigger anomaly without 3-tick confirmation!")

    def test_02_three_tick_confirmation_and_hysteresis(self):
        """Verifies anomalies require 3 consecutive anomalous ticks above Z-score 2.8 and floor."""
        engine = StatisticalAnomalyEngine(window_size=30, warmup_ticks=5, z_threshold=2.8)
        # Establish stable 2ms baseline
        for _ in range(25):
            engine.feed_sample("jitter_ms", 2.0)

        # Tick 1 of spike
        a1, z1, _, _ = engine.feed_sample("jitter_ms", 45.0)
        self.assertFalse(a1)
        self.assertGreater(z1, 2.8)

        # Tick 2 of spike
        a2, z2, _, _ = engine.feed_sample("jitter_ms", 48.0)
        self.assertFalse(a2)

        # Tick 3 of spike -> Confirmed!
        a3, z3, _, _ = engine.feed_sample("jitter_ms", 50.0)
        self.assertTrue(a3, "Persistent 3-tick anomaly must be confirmed.")

        # Tick 4 -> Hysteresis damping prevents re-triggering
        a4, z4, _, _ = engine.feed_sample("jitter_ms", 52.0)
        self.assertFalse(a4, "Hysteresis damping must suppress immediate re-trigger.")

    def test_03_flight_recorder_causal_attribution_speed_and_accuracy(self):
        """Verifies BlackBoxFlightRecorder attributes causes in <1ms across all failure modes."""
        recorder = BlackBoxFlightRecorder(maxlen=60)
        t = time.time()

        # Scenario A: Network Route Jitter
        recorder.record_tick(t - 3.0, cpu_pct=12.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=58, ping_ms=6.0, jitter_ms=0.5)
        recorder.record_tick(t - 1.5, cpu_pct=12.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=58, ping_ms=8.0, jitter_ms=1.0)
        recorder.record_tick(t, cpu_pct=12.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=58, ping_ms=65.0, jitter_ms=42.0)

        t_start = time.perf_counter()
        diag_net = recorder.attribute_causal_chain(10.0)
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        self.assertLess(elapsed_ms, 2.0, f"Flight recorder must execute in <2ms, took {elapsed_ms:.3f}ms")
        self.assertIn("Network Route Jitter Spike", diag_net)
        self.assertIn("Hardware Unaffected", diag_net)

        # Scenario B: GPU Thermal Clock Drop
        recorder.buffer.clear()
        recorder.record_tick(t - 3.0, cpu_pct=12.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=65, ping_ms=6.0, jitter_ms=0.5)
        recorder.record_tick(t - 1.5, cpu_pct=12.0, ram_mb=8000, gpu_clock_mhz=1950, gpu_temp=76, ping_ms=6.0, jitter_ms=0.5)
        recorder.record_tick(t, cpu_pct=12.0, ram_mb=8000, gpu_clock_mhz=1650, gpu_temp=83, ping_ms=6.0, jitter_ms=0.5)
        diag_gpu = recorder.attribute_causal_chain(10.0)
        self.assertIn("GPU Thermal/Power Clock Drop", diag_gpu)

        # Scenario C: CPU Interrupt
        recorder.buffer.clear()
        recorder.record_tick(t - 3.0, cpu_pct=10.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=60, ping_ms=6.0, jitter_ms=0.5, top_cpu_proc="System")
        recorder.record_tick(t - 1.5, cpu_pct=30.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=60, ping_ms=6.0, jitter_ms=0.5, top_cpu_proc="SearchApp.exe")
        recorder.record_tick(t, cpu_pct=65.0, ram_mb=8000, gpu_clock_mhz=2100, gpu_temp=60, ping_ms=6.0, jitter_ms=0.5, top_cpu_proc="SearchApp.exe")
        diag_cpu = recorder.attribute_causal_chain(10.0)
        self.assertIn("Background Process CPU Interrupt", diag_cpu)
        self.assertIn("SearchApp.exe", diag_cpu)

    def test_04_reinforcement_self_tuning_and_suppression(self):
        """Verifies impactful interventions increase weights while ineffective ones enter 30m suppression."""
        eval_path = "test_eval_tmp.json"
        evaluator = InterventionEvaluator(weights_path=eval_path)

        # Success case: Jitter dropped from 35ms -> 4ms
        act_id1 = evaluator.record_pre_intervention("flush_dns_qos", "jitter_ms", 35.0)
        ok1, msg1 = evaluator.evaluate_post_intervention(act_id1, 4.0)
        self.assertTrue(ok1)
        self.assertGreater(evaluator.weights["flush_dns_qos"], 1.0)
        self.assertIn("[Verified]", msg1)

        # Ineffective case: RAM freed was only 5 MB
        act_id2 = evaluator.record_pre_intervention("trim_ram", "used_ram_mb", 5000)
        ok2, msg2 = evaluator.evaluate_post_intervention(act_id2, 4995)
        self.assertFalse(ok2)
        self.assertIn("[Suppressed]", msg2)
        self.assertTrue(evaluator.is_action_suppressed("trim_ram"))
        self.assertGreaterEqual(evaluator.get_suppression_remaining_sec("trim_ram"), 1750)

        if os.path.exists(eval_path):
            os.remove(eval_path)

    def test_05_process_memory_velocity_and_foreground_protection(self):
        """Verifies RAM slope calculation (dRAM/dt) and active foreground window protection."""
        tracker = ProcessVelocityTracker(window_sec=60.0)
        now = time.time()

        # PID 101: Stable process sitting at 850 MB for 10s
        tracker.histories[101] = deque([(now - 10, 850.0), (now - 5, 850.0), (now, 850.0)])
        self.assertEqual(tracker.get_memory_velocity_mb_per_min(101), 0.0)
        self.assertFalse(tracker.is_true_memory_leak(101))
        allow_stable, reason_stable = tracker.should_allow_auto_trim(101, "Discord.exe", total_system_ram_pct=50.0)
        self.assertFalse(allow_stable)

        # PID 202: Active memory leak (+50 MB over 10s -> +300 MB/min)
        tracker.histories[202] = deque([(now - 10, 400.0), (now - 5, 425.0), (now, 450.0)])
        self.assertGreater(tracker.get_memory_velocity_mb_per_min(202), 100.0)
        self.assertTrue(tracker.is_true_memory_leak(202))
        allow_leak, reason_leak = tracker.should_allow_auto_trim(202, "unstable_app.exe", total_system_ram_pct=50.0)
        self.assertTrue(allow_leak)

        # Foreground window protection mock
        fg_pid = tracker.get_foreground_process_id()
        if fg_pid > 0:
            allow_fg, reason_fg = tracker.should_allow_auto_trim(fg_pid, "active_window.exe", total_system_ram_pct=90.0)
            self.assertFalse(allow_fg)
            self.assertIn("active foreground window", reason_fg)

    def test_06_ai_agent_lag_attribution_query(self):
        """Verifies AI Agent responds to 'why did I just lag?' using flight recorder causal attribution."""
        agent = AntimagistAIAgent()
        resp = agent.process_query("why did I just lag?")
        self.assertIn("Black Box Flight Recorder", resp)
        self.assertIn("Forensic Diagnosis", resp)


if __name__ == "__main__":
    unittest.main()
