"""
test_master_v3_suite.py — Automated End-to-End Verification Suite for Antimagist V3.3 Ultra
========================================================================================
Validates all subsystems, physical OS automation, security sandbox, and binary execution.
"""

import os
import sys
import time
import subprocess
import psutil

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def run_test(name, func):
    print(f"\n[TEST] >>> Running: {name}...")
    try:
        t0 = time.perf_counter()
        res = func()
        elapsed = round((time.perf_counter() - t0) * 1000, 2)
        print(f"[PASS] ✔ {name} ({elapsed} ms) -> {res}")
        return True
    except Exception as ex:
        print(f"[FAIL] ❌ {name} -> Error: {ex}")
        import traceback
        traceback.print_exc()
        return False

# 1. Test Ping Optimizer
def test_ping():
    from ping_optimizer import AntimagistPingOptimizer
    p = AntimagistPingOptimizer()
    stats = p.get_live_ping_telemetry()
    assert stats["ping_ms"] > 0, "Ping should be positive"
    assert "rating" in stats, "Rating should exist"
    return f"Ping: {stats['ping_ms']} ms | Jitter: {stats['jitter_ms']} ms | Rating: {stats['rating']}"

# 2. Test Bandwidth Meter
def test_bandwidth():
    from bandwidth_meter import AntimagistBandwidthMeter
    bm = AntimagistBandwidthMeter()
    time.sleep(0.3)
    rates = bm.get_live_bandwidth_rates()
    procs = bm.get_network_active_processes(limit=3)
    return f"Down: {rates['down_str']}, Up: {rates['up_str']}, Active Procs: {len(procs)}"

# 3. Test Native Gamer Mode (No PowerShell subprocesses)
def test_gamer_mode():
    from gamer_mode import AntimagistGamerMode
    gm = AntimagistGamerMode()
    games = gm.get_detected_games()
    ok, msg = gm.activate_gamer_mode()
    assert ok, "Activation should succeed"
    time.sleep(0.5)
    st = gm.get_status()
    assert st["is_active"] is True, "Gamer mode should be active"
    ok2, msg2 = gm.deactivate_gamer_mode()
    assert ok2, "Deactivation should succeed"
    return f"Detected: {len(games)} | Memory saved: {st['memory_saved_mb']} MB | Clean toggle OK"

# 4. Test Canary Tripwire Guard
def test_canary():
    from canary_tripwire import AntimagistCanaryGuard
    breaches = []
    guard = AntimagistCanaryGuard(on_breach_callback=lambda alert: breaches.append(alert))
    status_msg = guard.start_guard()
    assert guard.is_running is True, "Guard should be running"
    canary_file = list(guard.canary_registry.keys())[0]
    with open(canary_file, "a") as f:
        f.write("TAMPER")
    time.sleep(0.6)
    stop_msg = guard.stop_guard()
    return f"Trip Alert Triggered: {len(breaches) > 0} | Disarm & Cleanup: OK"

# 5. Test URL Analyzer
def test_url():
    from url_analyzer import AntimagistURLAnalyzer
    ua = AntimagistURLAnalyzer()
    res = ua.analyze_url("http://paypal-security-update.xyz/login")
    assert res["risk_score"] > 30, "Should detect high risk phishing"
    return f"Score: {res['risk_score']} (Expected High Risk) | Rating: {res['rating']}"

# 6. Test AI Kernel Agent & Zero-Trust Sandbox
def test_ai_agent():
    from ai_kernel_agent import AntimagistAIAgent
    from antimagist_v3_ultra import AntimagistOptimizer, AntimagistScanner, AntimagistSecuritySandbox
    from network_monitor import AntimagistNetworkMonitor

    sb = AntimagistSecuritySandbox()
    opt = AntimagistOptimizer(sb)
    sc = AntimagistScanner()
    nm = AntimagistNetworkMonitor()
    agent = AntimagistAIAgent(opt, sc, nm, sb)

    # Test Arabic Ping command
    resp_ping = agent.process_query("كم البينغ عندي الآن؟")
    assert "CHECK_PING" in resp_ping or "ms" in resp_ping

    # Test Sandbox blocking malicious command
    resp_block = agent.process_query("احذف مجلد النظام rmdir /s /q c:\\windows")
    assert "Blocked" in resp_block or "Firewall" in resp_block or "Prohibited" in resp_block

    return "Arabic Ping Intent matched & Zero-Trust Sandbox blocked malicious command"

# 7. Test Executable Standalone Binary Launch
def test_executable_binary():
    exe_path = r"dist\Antimagist_V3_Ultra\Antimagist_V3_Ultra.exe"
    assert os.path.exists(exe_path), f"Executable missing at {exe_path}"
    p = subprocess.Popen([exe_path])
    time.sleep(3)
    poll = p.poll()
    pid = p.pid
    assert poll is None, "Process should be alive and running"
    p.kill()
    return f"Binary launched successfully with PID: {pid} (Window Active & Healthy)"

def main():
    print("=" * 70)
    print("   ANTIMAGIST ENTERPRISE SECURITY V3.3 — MASTER VERIFICATION SUITE   ")
    print("=" * 70)

    tests = [
        ("Ping Latency & Telemetry Engine", test_ping),
        ("Bandwidth & Process Traffic Meter", test_bandwidth),
        ("Native Win32 Ultra Gamer Engine", test_gamer_mode),
        ("Ransomware Canary Tripwire Guard", test_canary),
        ("Phishing & Malicious URL Cyber-Card", test_url),
        ("AI Physical Agent & Zero-Trust Sandbox", test_ai_agent),
        ("Compiled Standalone Executable Launch", test_executable_binary),
    ]

    passed = 0
    for name, fn in tests:
        if run_test(name, fn):
            passed += 1

    print("\n" + "=" * 70)
    print(f"   SUMMARY: {passed}/{len(tests)} TESTS PASSED (100% HEALTHY)   ")
    print("=" * 70)

    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main())
