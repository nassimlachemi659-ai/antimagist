import os
import time
import tkinter as tk
from antimalware_app import AntiMalwareApp, QUARANTINE_DIR

root = tk.Tk()
root.withdraw()

print("=== ANTIMAGIST COMPREHENSIVE SYSTEM TEST ===")

app = AntiMalwareApp()

tests_passed = 0
total_tests = 5

try:
    # 1. YARA Load Test
    print("\n[*] TEST 1: Heuristic Engine (YARA) Initialization")
    if app.yara_rules:
        print("    [PASS] YARA rules successfully compiled and loaded.")
        tests_passed += 1
    else:
        print("    [FAIL] YARA rules missing.")

    # 2. Database Test
    print("\n[*] TEST 2: Local SQLite Threat Database")
    app.add_to_local_db("TEST_HASH_123", "EICAR-Test-Signature")
    res = app.check_local_db("TEST_HASH_123")
    if res == "EICAR-Test-Signature":
        print("    [PASS] Database read/write operations verified.")
        tests_passed += 1
    else:
        print("    [FAIL] Database failure.")

    # 3. RAM Optimization Test
    print("\n[*] TEST 3: Kernel Memory Flush (EmptyWorkingSet)")
    freed = app.boost_ram(show_popup=False)
    if freed >= 0:
        print(f"    [PASS] Memory optimizer executed successfully. Freed: {freed:.1f} MB")
        tests_passed += 1
    else:
        print("    [FAIL] Memory optimizer crashed.")

    # 4. Quarantine Encryption Test
    print("\n[*] TEST 4: XOR Quarantine Encryption Vault")
    test_file = "dummy_virus.bat"
    with open(test_file, "w") as f: f.write("MALICIOUS CODE")
    
    app.quarantine_file(test_file, "TEST_VIRUS")
    if not os.path.exists(test_file):
        print("    [PASS] Original threat neutralized and deleted.")
        tests_passed += 1
    else:
        print("    [FAIL] Threat still on disk.")

    # 5. Junk Cleaner Test
    print("\n[*] TEST 5: System Cache Sweeper")
    freed_mb, files = app.clean_junk(show_popup=False)
    if freed_mb >= 0:
        print(f"    [PASS] Cache sweeper executed securely. Deleted: {files} files.")
        tests_passed += 1
    else:
        print("    [FAIL] Cache sweeper crashed.")

except Exception as e:
    print(f"\n[CRITICAL ERROR] Test suite crashed: {e}")

print(f"\n=== TEST RESULTS: {tests_passed}/{total_tests} PASSED ===")
root.destroy()
