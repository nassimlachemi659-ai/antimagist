import os
import sys
import tkinter as tk
root = tk.Tk()
root.withdraw()

from antimalware_app import AntiMalwareApp

print("=== STARTING ENGINE DIAGNOSTICS ===")
app = AntiMalwareApp()

files_to_test = ["eicar.txt", "bad_script.bat"]

for test_file in files_to_test:
    print(f"\n[*] Target: {test_file}")
    
    print("    [Layer 1: Local DB]")
    result = app.calculate_file_hashes(test_file)
    if result["status"] == "Success":
        sha256 = result["sha256"]
        local_hit = app.check_local_db(sha256)
        print(f"    -> Match: {'DETECTED (' + local_hit + ')' if local_hit else 'Clean'}")
    
    print("    [Layer 3: YARA]")
    if app.yara_rules:
        yara_hits = app.scan_with_yara(test_file)
        if yara_hits:
            print(f"    -> Match: DETECTED {yara_hits}")
        else:
            print("    -> Match: Clean")

print("\n=== DIAGNOSTICS COMPLETE ===")
root.destroy()
