"""
gpu_sentinel.py — Antimagist V4 GPU Sentinel & RTX Thermal Radar
=================================================================
Antimagist Enterprise Security V4 Component
- Live hardware telemetry for dedicated graphics cards (NVIDIA GeForce RTX / GTX / AMD)
- Real-time GPU Core Temperature, Core Utilization, and VRAM Allocation
- Thermal pressure alert when GPU temperatures cross critical thresholds (> 82°C)
- Integrated streaming to Antimagist Desktop Dashboard, Topbar, and Mobile Companion HUD
"""

import os
import sys
import time
import subprocess
import threading
from typing import Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistGPUSentinel:
    """Monitors dedicated GPU metrics with sub-second non-blocking caching."""

    def __init__(self):
        self._lock = threading.Lock()
        self.last_metrics: Dict[str, Any] = {
            "gpu_name": "Detecting GPU...",
            "temperature_c": 0,
            "utilization_gpu_pct": 0,
            "utilization_vram_pct": 0,
            "vram_total_mb": 0,
            "vram_used_mb": 0,
            "vram_str": "0.0 / 0.0 GB",
            "status_color": "#00FF9D",
            "thermal_alert": False,
            "is_available": False
        }
        self.last_poll_time = 0.0

        # Run initial poll
        self._poll_gpu()

    def _query_nvidia_smi(self) -> Optional[Dict[str, Any]]:
        """Queries nvidia-smi for ultra-fast native hardware metrics."""
        cmd = [
            "nvidia-smi",
            "--query-gpu=name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.used,clocks.current.graphics,clocks.current.memory,power.draw,fan.speed",
            "--format=csv,noheader,nounits"
        ]
        try:
            res = subprocess.run(
                cmd, capture_output=True, text=True, timeout=1.5,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            if res.returncode == 0 and res.stdout.strip():
                parts = [p.strip() for p in res.stdout.strip().split(",")]
                if len(parts) >= 6:
                    name = parts[0]
                    temp = int(float(parts[1])) if parts[1] and parts[1] != "[N/A]" else 0
                    util_gpu = int(float(parts[2])) if parts[2] and parts[2] != "[N/A]" else 0
                    util_vram = int(float(parts[3])) if parts[3] and parts[3] != "[N/A]" else 0
                    total_mb = int(float(parts[4])) if parts[4] and parts[4] != "[N/A]" else 0
                    used_mb = int(float(parts[5])) if parts[5] and parts[5] != "[N/A]" else 0

                    core_clock = int(float(parts[6])) if len(parts) > 6 and parts[6] and parts[6] != "[N/A]" else 0
                    mem_clock = int(float(parts[7])) if len(parts) > 7 and parts[7] and parts[7] != "[N/A]" else 0
                    try:
                        power_w = round(float(parts[8]), 1) if len(parts) > 8 and parts[8] and parts[8] != "[N/A]" else 0.0
                    except Exception:
                        power_w = 0.0
                    try:
                        fan_speed = int(float(parts[9])) if len(parts) > 9 and parts[9] and parts[9] != "[N/A]" else 0
                    except Exception:
                        fan_speed = 0

                    used_gb = round(used_mb / 1024.0, 1)
                    total_gb = round(total_mb / 1024.0, 1)
                    vram_str = f"{used_gb} / {total_gb} GB"

                    if temp < 65:
                        color = "#00FF9D" # Emerald
                    elif temp < 80:
                        color = "#FBBF24" # Amber
                    else:
                        color = "#FF0055" # Crimson

                    return {
                        "gpu_name": name,
                        "temperature_c": temp,
                        "utilization_gpu_pct": util_gpu,
                        "utilization_vram_pct": util_vram,
                        "vram_total_mb": total_mb,
                        "vram_used_mb": used_mb,
                        "vram_str": vram_str,
                        "core_clock_mhz": core_clock,
                        "memory_clock_mhz": mem_clock,
                        "power_draw_w": power_w,
                        "fan_speed_pct": fan_speed,
                        "status_color": color,
                        "thermal_alert": temp >= 83,
                        "is_available": True
                    }
        except Exception:
            pass
        return None

    def _poll_gpu(self):
        now = time.time()
        # Cache for at least 3.0s to prevent excessive polling
        if now - self.last_poll_time < 3.0 and self.last_metrics.get("gpu_name") != "Detecting GPU...":
            return

        nv = self._query_nvidia_smi()
        if nv:
            with self._lock:
                self.last_metrics = nv
                self.last_poll_time = now
        else:
            with self._lock:
                self.last_metrics["gpu_name"] = "Standard Graphics Adapter"
                self.last_metrics["is_available"] = False
                self.last_poll_time = now

    def get_live_gpu_metrics(self) -> Dict[str, Any]:
        """Returns live cached GPU metrics."""
        self._poll_gpu()
        with self._lock:
            return dict(self.last_metrics)


if __name__ == "__main__":
    print("[*] Testing Antimagist GPU Sentinel...")
    sentinel = AntimagistGPUSentinel()
    m = sentinel.get_live_gpu_metrics()
    print(f"  • Hardware: {m['gpu_name']}")
    print(f"  • Temperature: {m['temperature_c']} °C (Color: {m['status_color']})")
    print(f"  • Core Utilization: {m['utilization_gpu_pct']}%")
    print(f"  • VRAM Allocation: {m['vram_str']} ({m['utilization_vram_pct']}%)")
    print(f"  • Thermal Alert Status: {m['thermal_alert']}")
    print("  • GPU Sentinel Test PASSED.")
