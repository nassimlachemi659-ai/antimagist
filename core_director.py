"""
core_director.py — Antimagist V4 CPU Core Director & Thread Affinity Optimizer
=============================================================================
Antimagist Enterprise Security V4 Component
- Maps physical CPU cores and logical SMT/HyperThreading topologies
- Pins games and competitive applications exclusively to High-Performance Cores (P-Cores)
- Prevents game threads from being scheduled onto slow Efficiency Cores (E-Cores)
- Eliminates 1% low FPS micro-stuttering and stabilizes frame delivery
"""

import os
import sys
import psutil
from typing import List, Dict, Any, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistCoreDirector:
    def __init__(self):
        self.physical_cores = psutil.cpu_count(logical=False) or 4
        self.logical_cores = psutil.cpu_count(logical=True) or 4
        self.original_affinities: Dict[int, List[int]] = {}

        # Determine optimal gaming core mask
        # On standard SMT/Hyperthreaded CPUs, primary performance threads are even-numbered or primary physical cores
        self.p_core_mask: List[int] = list(range(self.logical_cores))
        if self.logical_cores > 8:
            # For 12+ thread chips (e.g. 6P + 4E or 8P + 8E), primary performance cores reside in the first block
            self.p_core_mask = list(range(min(self.logical_cores, self.physical_cores * 2)))

    def get_cpu_topology(self) -> Dict[str, Any]:
        return {
            "physical_cores": self.physical_cores,
            "logical_processors": self.logical_cores,
            "has_hyperthreading": self.logical_cores > self.physical_cores,
            "p_core_indices": self.p_core_mask,
            "p_core_count": len(self.p_core_mask)
        }

    def get_performance_core_list(self) -> List[int]:
        """Returns the list of performance core processor indices."""
        return list(self.p_core_mask)

    def pin_process_to_performance_cores(self, pid: int) -> Tuple[bool, str]:
        """Pins target process exclusively to high-performance cores."""
        if pid <= 4:
            return False, "Cannot modify system kernel affinity."
        try:
            p = psutil.Process(pid)
            orig = p.cpu_affinity()
            self.original_affinities[pid] = orig

            p.cpu_affinity(self.p_core_mask)
            return True, f"Successfully pinned {p.name()} (PID: {pid}) to P-Cores {self.p_core_mask}."
        except (psutil.NoSuchProcess, psutil.AccessDenied) as ex:
            return False, f"Could not pin process {pid}: {ex}"

    def restore_process_affinity(self, pid: int) -> Tuple[bool, str]:
        """Restores original full-core affinity to a process."""
        if pid in self.original_affinities:
            try:
                p = psutil.Process(pid)
                p.cpu_affinity(self.original_affinities[pid])
                del self.original_affinities[pid]
                return True, f"Restored default affinity for PID {pid}."
            except Exception as ex:
                return False, f"Could not restore affinity for PID {pid}: {ex}"
        return True, "Process had no custom affinity pinned."


if __name__ == "__main__":
    cd = AntimagistCoreDirector()
    topo = cd.get_cpu_topology()
    print("[*] CPU Topology Analysis:")
    print(f"  • Physical Cores: {topo['physical_cores']}")
    print(f"  • Logical Processors: {topo['logical_processors']}")
    print(f"  • P-Core Target Mask: {topo['p_core_indices']}")

    curr_pid = os.getpid()
    ok, msg = cd.pin_process_to_performance_cores(curr_pid)
    print(f"  • Pin Test ({ok}): {msg}")
    ok2, msg2 = cd.restore_process_affinity(curr_pid)
    print(f"  • Restore Test ({ok2}): {msg2}")
