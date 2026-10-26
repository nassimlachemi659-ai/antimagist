"""
statistical_decision_engine.py — Antimagist Statistical & Reinforcement Intelligence
=====================================================================================
Pillar 4: Lightweight, Zero-Overhead Statistical Anomaly Detection & Causal Attribution
Replaces static single-tick thresholds with online statistics and behavioral memory:
  1. StatisticalAnomalyEngine: 5-tick warmup grace, rolling 30-sample Welford/EMA variance,
     Z-score > 2.8 with 3-tick confirmation & hysteresis damping.
  2. BlackBoxFlightRecorder: Ring buffer (maxlen=60, <64KB RAM) for instant (<1ms) causal
     stutter attribution (GPU Thermal Drop, CPU Interrupt, Route Jitter).
  3. InterventionEvaluator: Reinforcement self-tuning ("Verify Impact or Roll Back"),
     persisting weights to antimagist_brain_weights.json and applying 30-min suppression cooldowns.
  4. ProcessVelocityTracker: RAM growth velocity (dRAM/dt MB/min) and Windows GetForegroundWindow()
     protection preventing trimming of active user applications.
"""

import os
import sys
import time
import math
import json
import ctypes
from collections import deque
from typing import Dict, Any, List, Optional, Tuple

WEIGHTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "antimagist_brain_weights.json")


# ============================================================================
# 1. STATISTICAL ANOMALY ENGINE (Welford's Variance + 3-Tick Hysteresis)
# ============================================================================
class StatisticalAnomalyEngine:
    """
    Pure-Python statistical filter for telemetry streams (math + collections.deque).
    Completely eliminates cold-start and transient false-alarm spikes.
    """

    METRIC_FLOORS = {
        "ping_ms": 25.0,        # Don't trigger if ping is in nominal 5-20ms range
        "jitter_ms": 15.0,      # Don't trigger if jitter is below 15ms
        "cpu_pct": 40.0,        # Don't trigger if CPU is below 40%
        "ram_pct": 80.0,        # Don't trigger if RAM is below 80%
        "gpu_temp": 80.0        # Don't trigger if GPU temp is below 80°C
    }

    def __init__(self, window_size: int = 30, warmup_ticks: int = 5, z_threshold: float = 2.8):
        self.window_size = window_size
        self.warmup_ticks = warmup_ticks
        self.z_threshold = z_threshold
        self.sample_count = 0

        # Rolling 30-sample window for each metric
        self.windows: Dict[str, deque] = {
            "ping_ms": deque(maxlen=window_size),
            "jitter_ms": deque(maxlen=window_size),
            "cpu_pct": deque(maxlen=window_size),
            "ram_pct": deque(maxlen=window_size),
            "gpu_temp": deque(maxlen=window_size)
        }

        # Consecutive anomaly counter for 3-tick confirmation
        self.consecutive_anomalies: Dict[str, int] = {k: 0 for k in self.windows}
        # Hysteresis suppression cooldown per metric (timestamp)
        self.hysteresis_until: Dict[str, float] = {k: 0.0 for k in self.windows}

    def feed_sample(self, metric: str, value: float) -> Tuple[bool, float, float, float]:
        """
        Feeds a live sample.
        Returns (is_confirmed_anomaly, z_score, rolling_mean, rolling_std).
        """
        if metric not in self.windows:
            self.windows[metric] = deque(maxlen=self.window_size)
            self.consecutive_anomalies[metric] = 0
            self.hysteresis_until[metric] = 0.0

        val = float(value)
        win = self.windows[metric]

        # 1. Check Cold-Start Grace Period (First 5 ticks are silent warmup)
        is_warmed_up = len(win) >= self.warmup_ticks
        win.append(val)
        self.sample_count += 1

        if not is_warmed_up or len(win) < 3:
            return False, 0.0, val, 1.0

        # 2. Compute Online Rolling Mean and Sample Standard Deviation
        n = len(win)
        mean = sum(win) / n
        variance = sum((x - mean) ** 2 for x in win) / max(1, n - 1)
        # Prevent division by zero with a minimum standard deviation floor
        std = max(1.0, math.sqrt(variance))

        # 3. Z-Score Calculation
        z_score = (val - mean) / std

        # 4. Hysteresis Check (Don't trigger if currently damped)
        now = time.time()
        if now < self.hysteresis_until.get(metric, 0.0):
            self.consecutive_anomalies[metric] = 0
            return False, z_score, mean, std

        # 5. Dual Validation: Z-Score > 2.8 AND Absolute Floor Exceeded
        floor_val = self.METRIC_FLOORS.get(metric, 0.0)
        is_candidate = (z_score >= self.z_threshold) and (val >= floor_val)

        if is_candidate:
            self.consecutive_anomalies[metric] += 1
        else:
            self.consecutive_anomalies[metric] = 0

        # 6. 3-Tick Confirmation
        if self.consecutive_anomalies[metric] >= 3:
            # Anomaly confirmed over 3 consecutive ticks!
            # Reset counter and apply 15s hysteresis damping to prevent oscillation
            self.consecutive_anomalies[metric] = 0
            self.hysteresis_until[metric] = now + 15.0
            return True, z_score, mean, std

        return False, z_score, mean, std

    def is_warmed_up(self) -> bool:
        return self.sample_count >= self.warmup_ticks

    def reset_metric(self, metric: str):
        if metric in self.consecutive_anomalies:
            self.consecutive_anomalies[metric] = 0


# ============================================================================
# 2. LOCK-FREE "BLACK BOX" FLIGHT RECORDER (Causal Stutter Attribution)
# ============================================================================
class BlackBoxFlightRecorder:
    """
    Lock-free circular telemetry flight recorder (<64 KB RAM).
    Analyzes pre-spike flight telemetry to mathematically isolate the root cause.
    """

    def __init__(self, maxlen: int = 60):
        # Rolling 60-sample flight recorder (covers ~90 seconds at 1.5s/tick)
        self.buffer = deque(maxlen=maxlen)
        self.latest_attribution = "System Nominally Balanced. Zero causal hardware/network bottlenecks detected."
        self.last_spike_ts = 0.0

    def record_tick(
        self,
        timestamp: float,
        cpu_pct: float,
        ram_mb: float,
        gpu_clock_mhz: int,
        gpu_temp: int,
        ping_ms: float,
        jitter_ms: float,
        top_cpu_proc: str = "System",
        top_ram_proc: str = "System"
    ):
        """Appends a lightweight compact tuple on every 1.5s tick."""
        sample = (
            float(timestamp),
            float(cpu_pct),
            float(ram_mb),
            int(gpu_clock_mhz),
            int(gpu_temp),
            float(ping_ms),
            float(jitter_ms),
            str(top_cpu_proc or "System"),
            str(top_ram_proc or "System")
        )
        self.buffer.append(sample)

    def attribute_causal_chain(self, window_seconds: float = 10.0) -> str:
        """
        Analyzes the past window_seconds inside the ring buffer leading up to a spike.
        Returns a concise 1-line forensic attribution in <1ms execution time.
        """
        if len(self.buffer) < 3:
            return "Flight Recorder initializing — insufficient historical telemetry."

        now = self.buffer[-1][0]
        recent_samples = [s for s in self.buffer if (now - s[0]) <= window_seconds]
        if len(recent_samples) < 2:
            recent_samples = list(self.buffer)[-4:]

        curr = recent_samples[-1]
        baseline = recent_samples[0]

        curr_ts, curr_cpu, curr_ram, curr_gclk, curr_gtemp, curr_ping, curr_jit, curr_cpu_proc, curr_ram_proc = curr
        base_ts, base_cpu, base_ram, base_gclk, base_gtemp, base_ping, base_jit, base_cpu_proc, base_ram_proc = baseline

        attribution = ""

        # Causality 1: GPU Thermal or Power Throttling (Clock dropped while temperature rose or remained high)
        if base_gclk > 500 and (base_gclk - curr_gclk) >= 150 and curr_gtemp >= 74:
            drop_mhz = base_gclk - curr_gclk
            attribution = (
                f"GPU Thermal/Power Clock Drop (Clocks throttled -{drop_mhz} MHz from {base_gclk} to {curr_gclk} MHz @ {curr_gtemp}°C)"
            )

        # Causality 2: Background Process CPU Interrupt
        elif (curr_cpu - base_cpu) >= 20.0 or (curr_cpu > 45.0 and curr_cpu_proc not in ("System", "cs2.exe")):
            attribution = (
                f"Background Process CPU Interrupt ({curr_cpu_proc} spiked CPU to {curr_cpu:.0f}%)"
            )

        # Causality 3: Network Route Jitter Spike (Network spiked while Hardware stayed completely flat)
        elif (curr_jit - base_jit) >= 8.0 or curr_jit > 15.0 or (curr_ping - base_ping) >= 20.0:
            attribution = (
                f"Network Route Jitter Spike (Network ±{curr_jit:.1f}ms jitter / {curr_ping:.0f}ms ping, Hardware Unaffected)"
            )

        # Causality 4: Standby RAM / Working Set Pressure
        elif (curr_ram - base_ram) >= 250.0:
            attribution = (
                f"Memory Leak Growth Spike ({curr_ram_proc} allocated +{curr_ram - base_ram:.0f} MB RAM)"
            )

        else:
            attribution = (
                f"Transient Micro-Jitter (Ping: {curr_ping:.0f}ms, CPU: {curr_cpu:.0f}%, GPU: {curr_gtemp}°C nominal)"
            )

        self.latest_attribution = attribution
        self.last_spike_ts = now
        return attribution

    def get_latest_attribution(self) -> str:
        return self.latest_attribution


# ============================================================================
# 3. REINFORCEMENT SELF-TUNING ("Verify Impact or Roll Back")
# ============================================================================
class InterventionEvaluator:
    """
    Evaluates every automated action 15 seconds after execution.
    - If successful: Increases action confidence score.
    - If ineffective: Suppresses action for 30 minutes and rolls back state.
    """

    def __init__(self, weights_path: str = WEIGHTS_FILE):
        self.weights_path = weights_path
        self.weights: Dict[str, float] = self._load_weights()
        # Action suppression cooldowns: action_name -> cooldown_expiration_timestamp
        self.suppression_cooldowns: Dict[str, float] = {}
        # Pending verifications: action_id -> dict
        self.pending_verifications: Dict[str, Dict[str, Any]] = {}

    def _load_weights(self) -> Dict[str, float]:
        defaults = {
            "trim_ram": 1.0,
            "flush_dns_qos": 1.0,
            "throttle_cpu": 1.0,
            "reset_display_hz": 1.0
        }
        if os.path.exists(self.weights_path):
            try:
                with open(self.weights_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        defaults.update(data)
            except Exception:
                pass
        return defaults

    def _save_weights_atomic(self):
        tmp_path = self.weights_path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.weights, f, indent=2)
            os.replace(tmp_path, self.weights_path)
        except Exception:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass

    def is_action_suppressed(self, action_name: str) -> bool:
        """Checks if an action is currently suppressed under 30-min penalty."""
        until = self.suppression_cooldowns.get(action_name, 0.0)
        return time.time() < until

    def get_suppression_remaining_sec(self, action_name: str) -> int:
        until = self.suppression_cooldowns.get(action_name, 0.0)
        return max(0, int(until - time.time()))

    def record_pre_intervention(self, action_name: str, metric_name: str, pre_metric_val: float) -> str:
        """Registers a scheduled verification window for an automated action."""
        action_id = f"{action_name}_{int(time.time() * 1000)}"
        self.pending_verifications[action_id] = {
            "action_name": action_name,
            "metric_name": metric_name,
            "pre_val": float(pre_metric_val),
            "timestamp": time.time()
        }
        return action_id

    def evaluate_post_intervention(
        self,
        action_id: str,
        post_metric_val: float,
        on_rollback_callback: Optional[callable] = None
    ) -> Tuple[bool, str]:
        """
        Validates net improvement.
        Returns (is_success, log_message).
        """
        record = self.pending_verifications.pop(action_id, None)
        if not record:
            return True, "No pending verification found."

        action_name = record["action_name"]
        metric_name = record["metric_name"]
        pre_val = record["pre_val"]
        post_val = float(post_metric_val)

        is_improved = False
        delta_str = ""

        if action_name == "trim_ram":
            # Target: RAM MB freed or percent reduced
            freed_mb = pre_val - post_val
            if freed_mb >= 75.0:
                is_improved = True
                delta_str = f"Freed ~{freed_mb:.1f} MB working set RAM that stayed free"
            else:
                delta_str = f"RAM change nominal ({freed_mb:+.1f} MB)"

        elif action_name == "flush_dns_qos":
            # Target: Jitter ms reduced by at least 25% or down by > 3ms
            jitter_drop = pre_val - post_val
            pct_drop = (jitter_drop / max(0.1, pre_val)) * 100.0
            if (pct_drop >= 25.0) or (jitter_drop >= 3.0):
                is_improved = True
                delta_str = f"Jitter reduced from {pre_val:.1f}ms -> {post_val:.1f}ms (+{pct_drop:.0f}% stability)"
            else:
                delta_str = f"Jitter delta nominal ({pre_val:.1f}ms -> {post_val:.1f}ms)"

        elif action_name == "throttle_cpu":
            # Target: CPU % dropped
            cpu_drop = pre_val - post_val
            if cpu_drop >= 15.0:
                is_improved = True
                delta_str = f"Background process CPU dropped by {cpu_drop:.0f}%"
            else:
                delta_str = f"CPU delta negligible ({cpu_drop:+.0f}%)"

        else:
            is_improved = post_val < pre_val
            delta_str = f"Delta: {pre_val:.1f} -> {post_val:.1f}"

        # Reinforcement Weight Update
        if is_improved:
            cur_weight = self.weights.get(action_name, 1.0)
            self.weights[action_name] = min(2.5, round(cur_weight + 0.1, 2))
            self._save_weights_atomic()
            msg = f"[Verified] Action '{action_name}': {delta_str}. Confidence score: {self.weights[action_name]}."
            return True, msg
        else:
            # Action had negligible or negative effect — penalize and suppress for 30 minutes (1800s)
            cur_weight = self.weights.get(action_name, 1.0)
            self.weights[action_name] = max(0.2, round(cur_weight - 0.2, 2))
            self.suppression_cooldowns[action_name] = time.time() + 1800.0
            self._save_weights_atomic()

            if on_rollback_callback:
                try:
                    on_rollback_callback()
                except Exception:
                    pass

            msg = (
                f"[Suppressed] Action '{action_name}' had zero effect ({delta_str}). "
                f"Suppressed for 30 minutes to prevent CPU waste."
            )
            return False, msg


# ============================================================================
# 4. PER-PROCESS BEHAVIORAL MEMORY & FOREGROUND WINDOW PROTECTION
# ============================================================================
class ProcessVelocityTracker:
    """
    Tracks memory growth slope (MB per minute) of each PID over 60-second windows.
    Protects steady applications and the currently focused foreground window.
    """

    def __init__(self, window_sec: float = 60.0):
        self.window_sec = window_sec
        # pid -> deque of (timestamp, memory_mb)
        self.histories: Dict[int, deque] = {}

    def get_foreground_process_id(self) -> int:
        """Returns the PID of the currently active/focused foreground window via Win32."""
        if os.name != 'nt':
            return 0
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return 0
            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            return int(pid.value)
        except Exception:
            return 0

    def record_process_sample(self, pid: int, memory_mb: float):
        """Records a timestamped memory observation for a PID."""
        now = time.time()
        if pid not in self.histories:
            self.histories[pid] = deque(maxlen=40)

        dq = self.histories[pid]
        dq.append((now, float(memory_mb)))

        # Evict old points beyond window_sec
        while dq and (now - dq[0][0]) > self.window_sec:
            dq.popleft()

    def get_memory_velocity_mb_per_min(self, pid: int) -> float:
        """
        Calculates dRAM / dt in MB per minute over the rolling 60s window.
        Returns 0.0 if insufficient historical data.
        """
        dq = self.histories.get(pid)
        if not dq or len(dq) < 2:
            return 0.0

        t_first, m_first = dq[0]
        t_last, m_last = dq[-1]
        dt = t_last - t_first

        if dt < 5.0:  # Require at least 5s of sampling
            return 0.0

        dm = m_last - m_first
        # (MB / seconds) * 60 = MB / minute
        velocity = (dm / dt) * 60.0
        return round(velocity, 2)

    def is_true_memory_leak(self, pid: int, threshold_mb_per_min: float = 15.0) -> bool:
        """
        Returns True only if the process's working set is actively climbing
        consistently at >15 MB/min, avoiding trimming static apps.
        """
        velocity = self.get_memory_velocity_mb_per_min(pid)
        if velocity <= threshold_mb_per_min:
            return False

        dq = self.histories.get(pid)
        if not dq or len(dq) < 3:
            return False

        # Require total growth of at least 30 MB in this window
        total_growth = dq[-1][1] - dq[0][1]
        return total_growth >= 30.0

    def should_allow_auto_trim(self, pid: int, name: str, total_system_ram_pct: float) -> Tuple[bool, str]:
        """
        Enforces strict zero-stutter trimming rules:
        1. NEVER trim the focused foreground window (causes instant stutter!).
        2. DO NOT trim processes with flat or negative velocity (normal working state).
        3. Only trim if memory velocity is actively leaking (>15 MB/min) OR total RAM > 80%.
        """
        fg_pid = self.get_foreground_process_id()
        if fg_pid > 0 and pid == fg_pid:
            return False, f"Protected: {name} (PID {pid}) is the active foreground window."

        # Check memory growth slope
        velocity = self.get_memory_velocity_mb_per_min(pid)
        is_leaking = self.is_true_memory_leak(pid)

        if is_leaking:
            return True, f"Active memory leak detected (+{velocity:.1f} MB/min velocity)"

        if total_system_ram_pct >= 80.0:
            return True, f"High system RAM pressure ({total_system_ram_pct:.0f}%)"

        return False, f"Memory state stable ({velocity:+.1f} MB/min velocity) — trimming avoided to prevent paging stutters."

    def cleanup_dead_pids(self, active_pids: List[int]):
        """Evicts terminated processes to keep memory consumption under 20KB."""
        active_set = set(active_pids)
        dead = [pid for pid in self.histories if pid not in active_set]
        for pid in dead:
            del self.histories[pid]


# Global Singletons
statistical_anomaly_engine = StatisticalAnomalyEngine()
flight_recorder = BlackBoxFlightRecorder()
intervention_evaluator = InterventionEvaluator()
process_velocity_tracker = ProcessVelocityTracker()
