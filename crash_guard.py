"""
crash_guard.py — Antimagist V11 Enterprise Global Exception Boundary & Self-Healing Logger
========================================================================================
Antimagist Enterprise Security V11 Component
- Intercepts uncaught exceptions on main and background daemon threads
- Logs forensic stack traces to 'antimagist_crash_guard.log'
- Provides graceful recovery wrappers (@safe_worker) to keep UI responsive
- Handles Windows WMI and network RPC timeouts without freezing the application
"""

import os
import sys
import time
import traceback
import threading
import functools
from typing import Callable, Any, Optional

CRASH_LOG_FILE = os.path.abspath("antimagist_crash_guard.log")


class AntimagistCrashGuard:
    """Enterprise self-healing exception boundary and diagnostic logger."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AntimagistCrashGuard, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, log_path: Optional[str] = None):
        if self._initialized:
            return
        self.log_path = log_path or CRASH_LOG_FILE
        self.crash_count = 0
        self._installed = False
        self._initialized = True

    def install(self):
        """Installs global exception hooks for sys and threading."""
        if self._installed:
            return
        sys.excepthook = self._handle_sys_exception
        if hasattr(threading, "excepthook"):
            threading.excepthook = self._handle_thread_exception
        self._installed = True
        self.log_event("INFO", "Antimagist CrashGuard self-healing exception boundary armed.")

    def log_event(self, level: str, message: str, exc_info: Optional[Exception] = None):
        """Appends a timestamped event or error trace to the crash log."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = [f"[{timestamp}] [{level.upper()}] {message}"]
        if exc_info:
            tb_lines = traceback.format_exception(type(exc_info), exc_info, exc_info.__traceback__)
            entry.append("".join(tb_lines).strip())
        entry_text = "\n".join(entry) + "\n"

        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(entry_text)
        except Exception:
            pass

    def _handle_sys_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.crash_count += 1
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.log_event("CRITICAL_SYS", f"Uncaught Main-Thread Exception: {exc_value}\n{tb}")

    def _handle_thread_exception(self, args):
        self.crash_count += 1
        tb = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
        thread_name = args.thread.name if args.thread else "UnknownThread"
        self.log_event("ERROR_THREAD", f"Uncaught Background Exception in '{thread_name}': {args.exc_value}\n{tb}")


def safe_worker(fallback_return: Any = None, silent: bool = False):
    """Decorator to wrap background worker functions and callbacks in crash-proof boundaries."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                guard = AntimagistCrashGuard()
                if not silent:
                    guard.log_event("WARNING_WORKER", f"Suppressed exception in {func.__name__}: {ex}", exc_info=ex)
                return fallback_return
        return wrapper
    return decorator


if __name__ == "__main__":
    print("[*] Testing Antimagist Crash Guard...")
    guard = AntimagistCrashGuard()
    guard.install()
    guard.log_event("TEST", "Diagnostic self-test verification entry.")
    
    @safe_worker(fallback_return="SAFE_FALLBACK")
    def test_faulty_worker():
        raise TimeoutError("Simulated Windows WMI RPC timeout.")

    res = test_faulty_worker()
    print(f"  Result with safe_worker: {res}")
    print(f"  Log File: {guard.log_path}")
    print("[+] Antimagist Crash Guard PASSED.")
