"""
bandwidth_meter.py — Real-Time Per-Process Network Bandwidth & Data Hog Detector
================================================================================
Antimagist Enterprise Security V3 Component
- Monitors live system Upload/Download throughput in KB/s and MB/s
- Attributes active network sockets to running processes
- Flags background bandwidth hogs that spike gaming ping or induce packet loss
"""

import os
import sys
import time
import psutil
from typing import Dict, Any, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistBandwidthMeter:
    def __init__(self):
        self.last_time = time.time()
        self.last_io = psutil.net_io_counters()
        self.last_down_kbs: float = 0.0
        self.last_up_kbs: float = 0.0

    def get_live_bandwidth_rates(self) -> Dict[str, Any]:
        """Calculates current system-wide download and upload speeds in KB/s."""
        now = time.time()
        curr_io = psutil.net_io_counters()
        dt = max(0.2, now - self.last_time)

        down_bytes = curr_io.bytes_recv - self.last_io.bytes_recv
        up_bytes = curr_io.bytes_sent - self.last_io.bytes_sent

        down_kbs = round((down_bytes / dt) / 1024.0, 1)
        up_kbs = round((up_bytes / dt) / 1024.0, 1)

        self.last_time = now
        self.last_io = curr_io
        self.last_down_kbs = down_kbs
        self.last_up_kbs = up_kbs

        return {
            "down_kbs": down_kbs,
            "up_kbs": up_kbs,
            "down_str": f"{down_kbs / 1024.0:.2f} MB/s" if down_kbs > 1024 else f"{down_kbs:.1f} KB/s",
            "up_str": f"{up_kbs / 1024.0:.2f} MB/s" if up_kbs > 1024 else f"{up_kbs:.1f} KB/s",
            "total_bytes_sent_mb": round(curr_io.bytes_sent / (1024**2), 1),
            "total_bytes_recv_mb": round(curr_io.bytes_recv / (1024**2), 1)
        }

    def get_network_active_processes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Scans all established network sockets and identifies processes with active connections.
        Flags processes that could cause background latency spikes.
        """
        proc_conn_counts: Dict[int, int] = {}
        try:
            conns = psutil.net_connections(kind='inet')
            for c in conns:
                if c.status == "ESTABLISHED" and c.pid and c.pid > 0:
                    proc_conn_counts[c.pid] = proc_conn_counts.get(c.pid, 0) + 1
        except Exception:
            pass

        results = []
        for pid, count in sorted(proc_conn_counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
            try:
                p = psutil.Process(pid)
                pname = p.name()
                mem_mb = round(p.memory_info().rss / (1024**2), 1)
                
                # Flag known heavy background downloaders
                pname_lower = pname.lower()
                is_heavy = any(h in pname_lower for h in ["steam", "epic", "torrent", "qbittorrent", "discord", "chrome", "edge", "onedrive"])
                
                results.append({
                    "pid": pid,
                    "name": pname,
                    "connections": count,
                    "memory_mb": mem_mb,
                    "is_potential_hog": is_heavy,
                    "tag": "⚠️ Background Traffic" if is_heavy else "Active Connection"
                })
            except Exception:
                pass

        return results


if __name__ == "__main__":
    bm = AntimagistBandwidthMeter()
    time.sleep(1.0)
    rates = bm.get_live_bandwidth_rates()
    print(f"[*] Bandwidth: Down {rates['down_str']} | Up {rates['up_str']}")
    procs = bm.get_network_active_processes()
    print(f"[*] Active Network Processes: {len(procs)}")
    for p in procs:
        print(f"  • {p['name']} (PID: {p['pid']}) - {p['connections']} sockets [{p['tag']}]")
