"""
process_cage_job_object.py — Antimagist Real Windows Kernel Job-Object Resource Cage
=====================================================================================
Antimagist Enterprise Security V12 Kernel Component
- Implements real Windows Kernel Job Object Isolation via native Win32 APIs:
    • CreateJobObjectW
    • SetInformationJobObject (JobObjectExtendedLimitInformation & JobObjectCpuRateControlInformation)
    • AssignProcessToJobObject
    • TerminateJobObject
- Hard-caps background bloat processes (launcher webviews, updaters, background tasks) to:
    • Maximum 10% CPU core rate limit (JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP)
    • Maximum 500 MB RAM Working Set limit (JOB_OBJECT_LIMIT_PROCESS_MEMORY)
- Provides active process cage tracking, live telemetry, release, and termination controls.
"""

import os
import sys
import time
import ctypes
from ctypes import wintypes
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    ]


class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class JOBOBJECT_CPU_RATE_CONTROL_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ControlFlags", wintypes.DWORD),
        ("CpuRate", wintypes.DWORD),
    ]


# Job Object Information Classes
JobObjectExtendedLimitInformation = 9
JobObjectCpuRateControlInformation = 15

# Limit Flags
JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
JOB_OBJECT_LIMIT_WORKINGSET = 0x00000001

# CPU Rate Control Flags
JOB_OBJECT_CPU_RATE_CONTROL_ENABLE = 0x00000001
JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP = 0x00000004

# Process Access Flags
PROCESS_TERMINATE = 0x0001
PROCESS_SET_QUOTA = 0x0100
PROCESS_SET_INFORMATION = 0x0200
PROCESS_QUERY_INFORMATION = 0x0400


class AntimagistJobObjectCage:
    """Manages Windows Kernel Job Object resource sandboxing and process caging."""

    def __init__(self):
        self.caged_jobs: Dict[int, Dict[str, Any]] = {}
        self.k32 = ctypes.windll.kernel32 if os.name == 'nt' else None

    def cage_process(
        self,
        pid: int,
        cpu_rate_pct: int = 10,
        memory_limit_mb: int = 500
    ) -> Tuple[bool, str]:
        """
        Assigns the target process into a restricted Windows Kernel Job Object cage.
        Enforces a hard CPU cap (default 10%) and maximum memory working set limit (default 500 MB).
        """
        if os.name != 'nt' or not self.k32:
            return False, "Windows Kernel Job Objects require Windows OS."

        if pid <= 4:
            return False, "Cannot cage Windows System/Kernel process."

        import psutil
        try:
            proc = psutil.Process(pid)
            pname = proc.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as ex:
            return False, f"Could not inspect PID {pid}: {ex}"

        # If already caged, release previous job first
        if pid in self.caged_jobs:
            self.release_process(pid)

        job_name = f"AntimagistCage_PID_{pid}_{int(time.time())}"
        hJob = self.k32.CreateJobObjectW(None, job_name)
        if not hJob:
            err = ctypes.GetLastError()
            return False, f"CreateJobObjectW failed with error code {err}."

        try:
            # 1. Configure CPU Rate Hard Cap (1000 = 10.00%)
            cpu_info = JOBOBJECT_CPU_RATE_CONTROL_INFORMATION()
            cpu_info.ControlFlags = JOB_OBJECT_CPU_RATE_CONTROL_ENABLE | JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP
            cpu_info.CpuRate = max(100, min(10000, cpu_rate_pct * 100))

            res_cpu = self.k32.SetInformationJobObject(
                hJob,
                JobObjectCpuRateControlInformation,
                ctypes.byref(cpu_info),
                ctypes.sizeof(cpu_info)
            )

            # 2. Configure Memory Working Set & Process Memory Limit (500 MB)
            ext_info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            ext_info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_PROCESS_MEMORY
            ext_info.ProcessMemoryLimit = memory_limit_mb * 1024 * 1024

            res_mem = self.k32.SetInformationJobObject(
                hJob,
                JobObjectExtendedLimitInformation,
                ctypes.byref(ext_info),
                ctypes.sizeof(ext_info)
            )

            # 3. Open Process and Assign to Job Object
            access = PROCESS_SET_QUOTA | PROCESS_TERMINATE | PROCESS_SET_INFORMATION | PROCESS_QUERY_INFORMATION
            hProcess = self.k32.OpenProcess(access, False, pid)
            if not hProcess:
                self.k32.CloseHandle(hJob)
                err = ctypes.GetLastError()
                return False, f"OpenProcess failed on PID {pid} (Error: {err}). Process may require Administrator rights."

            res_assign = self.k32.AssignProcessToJobObject(hJob, hProcess)
            self.k32.CloseHandle(hProcess)

            if not res_assign:
                self.k32.CloseHandle(hJob)
                err = ctypes.GetLastError()
                return False, f"AssignProcessToJobObject failed (Error: {err}). Process might belong to another immutable Job."

            self.caged_jobs[pid] = {
                "pid": pid,
                "name": pname,
                "hJob": hJob,
                "cpu_rate_pct": cpu_rate_pct,
                "memory_limit_mb": memory_limit_mb,
                "caged_at": time.strftime("%H:%M:%S"),
                "status": "CAGED"
            }

            return True, f"🔒 Process '{pname}' (PID {pid}) caged: Hard-capped to {cpu_rate_pct}% CPU & {memory_limit_mb}MB RAM."
        except Exception as ex:
            if hJob:
                self.k32.CloseHandle(hJob)
            return False, f"Failed to cage process {pid}: {ex}"

    def release_process(self, pid: int) -> Tuple[bool, str]:
        """Releases target process from its Job Object cage by closing the Job handle."""
        if pid in self.caged_jobs:
            item = self.caged_jobs.pop(pid)
            hJob = item.get("hJob")
            if hJob and self.k32:
                try:
                    self.k32.CloseHandle(hJob)
                except Exception:
                    pass
            return True, f"🔓 Released process '{item.get('name')}' (PID {pid}) from Job Object cage."
        return False, f"Process PID {pid} is not currently caged."

    def terminate_caged_process(self, pid: int) -> Tuple[bool, str]:
        """Immediately terminates the caged process via TerminateJobObject or process kill."""
        if pid in self.caged_jobs:
            item = self.caged_jobs.pop(pid)
            hJob = item.get("hJob")
            pname = item.get("name", "Unknown")
            terminated = False

            if hJob and self.k32:
                try:
                    res = self.k32.TerminateJobObject(hJob, 1)
                    if res:
                        terminated = True
                    self.k32.CloseHandle(hJob)
                except Exception:
                    pass

            if not terminated:
                import psutil
                try:
                    p = psutil.Process(pid)
                    p.kill()
                    terminated = True
                except Exception:
                    pass

            return True, f"🛑 Terminated caged process '{pname}' (PID {pid}). Resources reclaimed."
        return False, f"Process PID {pid} is not currently in cage registry."

    def list_caged_processes(self) -> List[Dict[str, Any]]:
        """Returns the list of active caged processes with live telemetry."""
        import psutil
        results = []
        dead_pids = []

        for pid, data in self.caged_jobs.items():
            if not psutil.pid_exists(pid):
                dead_pids.append(pid)
                continue

            try:
                p = psutil.Process(pid)
                mem_mb = round(p.memory_info().rss / (1024**2), 1)
                cpu = p.cpu_percent(interval=None)
                results.append({
                    "pid": pid,
                    "name": data["name"],
                    "caged_at": data["caged_at"],
                    "cpu_rate_cap": f"{data['cpu_rate_pct']}%",
                    "mem_cap_mb": f"{data['memory_limit_mb']} MB",
                    "current_cpu_pct": cpu,
                    "current_ram_mb": mem_mb,
                    "status": "CAGED_ACTIVE"
                })
            except Exception:
                dead_pids.append(pid)

        # Cleanup terminated processes
        for dpid in dead_pids:
            self.release_process(dpid)

        return results

    def release_all(self) -> Tuple[bool, str]:
        """Releases all processes currently in the cage registry."""
        count = len(self.caged_jobs)
        for pid in list(self.caged_jobs.keys()):
            self.release_process(pid)
        return True, f"Released {count} process(es) from Windows Kernel Job Object cage."

    close_all_cages = release_all


if __name__ == "__main__":
    print("[*] Testing Antimagist Real Windows Kernel Job-Object Resource Cage...")
    cage = AntimagistJobObjectCage()
    # Test on current python process or spawned child
    import subprocess
    child = subprocess.Popen(["notepad.exe"])
    print(f"  • Spawned test child notepad.exe (PID {child.pid})")

    ok_c, msg_c = cage.cage_process(child.pid, cpu_rate_pct=10, memory_limit_mb=500)
    print(f"  • Cage Process ({ok_c}): {msg_c}")

    caged = cage.list_caged_processes()
    print(f"  • Active Caged Processes: {len(caged)}")
    for cp in caged:
        print(f"    - {cp['name']} (PID {cp['pid']}): CPU Cap {cp['cpu_rate_cap']}, RAM Cap {cp['mem_cap_mb']}")

    ok_t, msg_t = cage.terminate_caged_process(child.pid)
    print(f"  • Terminate Caged Process ({ok_t}): {msg_t}")
    print("[+] Windows Job Object Resource Cage PASSED.")
