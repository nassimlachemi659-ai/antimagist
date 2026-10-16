"""
self_healing_supervisor.py — Antimagist Self-Healing Runtime Supervisor
=======================================================================
Pillar 2: Autonomous Fault Quarantine, Thread Watchdog & Self-Repairing State
Features:
  1. Thread & Module Watchdog with heartbeat monitoring and auto-respawn
  2. Atomic, Self-Repairing JSON Config / Vault / Database persistence
  3. Dynamic API Fallback & Self-Patching method caching
"""

import os
import sys
import time
import json
import shutil
import threading
import traceback
from typing import Dict, Any, Optional, Callable, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class SelfHealingSupervisor:
    """
    Autonomous Watchdog and Self-Healing Supervisor.
    Keeps background threads alive, quarantines exceptions, and auto-repairs corrupted files.
    """

    _instance = None
    _lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SelfHealingSupervisor, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.workers: Dict[str, Dict[str, Any]] = {}
        self.fault_quarantine_log: list = []
        self.api_fallback_cache: Dict[str, Callable] = {}
        self._running = True

        # Start background watchdog daemon
        self._watchdog_thread = threading.Thread(
            target=self._watchdog_loop,
            name="AntimagistSupervisorWatchdog",
            daemon=True
        )
        self._watchdog_thread.start()

    # ========================================================================
    # 1. THREAD WATCHDOG & HEARTBEAT ENGINE
    # ========================================================================
    def register_worker(
        self,
        name: str,
        target_func: Callable,
        args: tuple = (),
        kwargs: Optional[dict] = None,
        timeout_sec: float = 6.0,
        auto_restart: bool = True
    ) -> threading.Thread:
        """
        Registers a worker thread with active heartbeat tracking.
        If the thread dies or freezes beyond timeout_sec, supervisor respawns it.
        """
        kwargs = kwargs or {}
        with self._lock:
            worker_meta = {
                "name": name,
                "target": target_func,
                "args": args,
                "kwargs": kwargs,
                "timeout_sec": timeout_sec,
                "auto_restart": auto_restart,
                "last_heartbeat": time.time(),
                "restart_count": 0,
                "thread": None,
                "status": "STARTING"
            }
            self.workers[name] = worker_meta

        return self._spawn_worker_thread(name)

    def heartbeat(self, name: str):
        """Pulsed by running workers to indicate health."""
        with self._lock:
            if name in self.workers:
                self.workers[name]["last_heartbeat"] = time.time()
                self.workers[name]["status"] = "HEALTHY"

    def _spawn_worker_thread(self, name: str) -> threading.Thread:
        """Internal helper to safely instantiate and start the worker thread."""
        meta = self.workers[name]

        def _safe_runner():
            try:
                meta["last_heartbeat"] = time.time()
                meta["status"] = "RUNNING"
                meta["target"](*meta["args"], **meta["kwargs"])
            except Exception as ex:
                tb = traceback.format_exc()
                self.quarantine_fault(name, ex, tb)
                meta["status"] = "CRASHED"

        t = threading.Thread(target=_safe_runner, name=f"AntimagistWorker_{name}", daemon=True)
        meta["thread"] = t
        t.start()
        return t

    def _watchdog_loop(self):
        """Monitors registered threads every 2 seconds for hangs or crashes."""
        while self._running:
            time.sleep(2.0)
            now = time.time()
            with self._lock:
                for name, meta in list(self.workers.items()):
                    if not meta.get("auto_restart"):
                        continue

                    thread = meta.get("thread")
                    time_since_hb = now - meta.get("last_heartbeat", now)
                    timeout = meta.get("timeout_sec", 6.0)

                    # Condition 1: Thread dead
                    thread_died = thread is not None and not thread.is_alive()
                    # Condition 2: Thread frozen past timeout
                    thread_frozen = time_since_hb > timeout and meta.get("status") == "RUNNING"

                    if thread_died or thread_frozen:
                        reason = "Thread terminated unexpectedly" if thread_died else f"Thread heartbeat timed out ({time_since_hb:.1f}s > {timeout}s)"
                        self.quarantine_fault(name, RuntimeError(reason), f"Watchdog detected: {reason}")
                        meta["restart_count"] += 1
                        meta["status"] = "RESTARTING"
                        # Respawn thread cleanly
                        self._spawn_worker_thread(name)

    def quarantine_fault(self, source: str, error: Exception, trace_info: str):
        """Logs and quarantines faults to protect the UI from crashing."""
        entry = {
            "source": source,
            "error_type": type(error).__name__,
            "message": str(error),
            "traceback": trace_info[:400],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with self._lock:
            self.fault_quarantine_log.append(entry)
            if len(self.fault_quarantine_log) > 50:
                self.fault_quarantine_log.pop(0)

    # ========================================================================
    # 2. ATOMIC & SELF-REPAIRING STATE VAULT (CONFIG / JSON)
    # ========================================================================
    @staticmethod
    def atomic_write_json(filepath: str, data: Any) -> bool:
        """
        Writes data to filepath atomically:
        Writes to .tmp file -> flushes/syncs -> replaces target file.
        Also maintains a shadow backup .bak copy for disaster recovery.
        """
        tmp_path = f"{filepath}.tmp"
        bak_path = f"{filepath}.bak"
        try:
            dname = os.path.dirname(filepath)
            if dname and not os.path.exists(dname):
                os.makedirs(dname, exist_ok=True)

            # Write to temporary file
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Create shadow backup of existing valid file
            if os.path.exists(filepath):
                try:
                    shutil.copy2(filepath, bak_path)
                except Exception:
                    pass

            # Atomic rename / replace
            os.replace(tmp_path, filepath)
            return True
        except Exception as ex:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            return False

    @classmethod
    def safe_read_json(
        cls,
        filepath: str,
        default_fallback: Any,
        validator: Optional[Callable[[Any], bool]] = None
    ) -> Any:
        """
        Reads JSON file safely. If missing, corrupt, 0-byte, or fails validation:
        1. Tries to restore from .bak shadow copy
        2. If .bak is also corrupted, reconstructs from default_fallback
        3. Atomically writes back valid state so subsequent reads succeed.
        """
        bak_path = f"{filepath}.bak"

        # Try reading primary file
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        if validator is None or validator(data):
                            return data
            except Exception:
                pass  # Corrupted primary, fall through to .bak

        # Try reading shadow backup
        if os.path.exists(bak_path):
            try:
                with open(bak_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        if validator is None or validator(data):
                            # Restore primary from backup
                            cls.atomic_write_json(filepath, data)
                            return data
            except Exception:
                pass

        # Complete reconstruction from default
        reconstructed = default_fallback() if callable(default_fallback) else default_fallback
        cls.atomic_write_json(filepath, reconstructed)
        return reconstructed

    # ========================================================================
    # 3. DYNAMIC API FALLBACK & SELF-PATCHING EXECUTION
    # ========================================================================
    def execute_with_fallback(
        self,
        api_key: str,
        primary_callable: Callable,
        fallback_callable: Callable,
        *args, **kwargs
    ) -> Any:
        """
        Executes primary_callable. If it raises an exception or is known to fail
        on this system, routes directly to fallback_callable and caches the working method.
        """
        if api_key in self.api_fallback_cache:
            return self.api_fallback_cache[api_key](*args, **kwargs)

        try:
            res = primary_callable(*args, **kwargs)
            return res
        except Exception as ex:
            self.quarantine_fault(f"API_{api_key}", ex, f"Falling back to native handler: {ex}")
            # Cache fallback so future calls don't incur failure penalty
            self.api_fallback_cache[api_key] = fallback_callable
            return fallback_callable(*args, **kwargs)

    def shutdown(self):
        """Stops the watchdog loop cleanly."""
        self._running = False


# Global singleton instance
supervisor = SelfHealingSupervisor()


if __name__ == "__main__":
    print("[*] Testing Antimagist Self-Healing Supervisor...")

    # 1. Test Atomic Config Read/Write & Self-Repair
    test_cfg = "test_healer_config.json"
    data = {"mode": "ESPORTS", "version": "12.3", "active": True}
    supervisor.atomic_write_json(test_cfg, data)
    print(f"  • Atomic Write JSON: Created {test_cfg}")

    # Corrupt the file intentionally
    with open(test_cfg, "w") as f:
        f.write("{ INVALID JSON CORRUPTED DATA !!! ")
    print("  • Simulated Disaster: Corrupted config file with malformed JSON")

    # Safe Read should self-heal from .bak or defaults
    repaired = supervisor.safe_read_json(test_cfg, {"mode": "DEFAULT", "recovered": True})
    print(f"  • Self-Healing Recovery: Successfully read repaired state -> mode: {repaired.get('mode')}")
    assert repaired.get("mode") in ("ESPORTS", "DEFAULT")

    # 2. Test Thread Watchdog & Auto-Respawn
    counter = {"ticks": 0}
    def flaky_worker():
        while True:
            counter["ticks"] += 1
            supervisor.heartbeat("flaky")
            time.sleep(0.3)
            if counter["ticks"] == 3:
                # Deliberate intentional crash to test watchdog
                raise ValueError("Simulated worker exception")

    t = supervisor.register_worker("flaky", flaky_worker, timeout_sec=1.5)
    print("  • Registered fragile worker with 1.5s watchdog timeout")
    time.sleep(2.5)

    meta = supervisor.workers.get("flaky")
    print(f"  • Watchdog Restart Count: {meta.get('restart_count')} (Recovered after simulated crash)")
    assert meta.get("restart_count") >= 1

    # Clean up test artifacts
    supervisor.shutdown()
    for p in [test_cfg, f"{test_cfg}.bak", f"{test_cfg}.tmp"]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    print("[+] Self-Healing Supervisor verified successfully.")
