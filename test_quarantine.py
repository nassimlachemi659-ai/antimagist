import os
import time
import tkinter as tk
from antimalware_app import AntiMalwareApp, QUARANTINE_DIR

# Suppress GUI
root = tk.Tk()
root.withdraw()

print("=== INITIATING FINAL SYSTEM STRESS TEST ===")

app = AntiMalwareApp()

# 1. Create a dummy malicious file
test_file = "dummy_virus.bat"
print("\n[*] Step 1: Simulating Malware Attack...")
with open(test_file, "w") as f:
    f.write("powershell -enc MALICIOUS_CODE_SIMULATION\ncmd.exe /c start")
print(f"    -> Created malicious file: {test_file}")

# 2. Verify file exists
if os.path.exists(test_file):
    print("    -> Malware is ACTIVE on disk.")
    
# 3. Trigger Engine Scan
print("\n[*] Step 2: Engine Interception...")
app._scan_logic(test_file, "ACTIVE SHIELD")

# 4. Verify Quarantine Results
print("\n[*] Step 3: Verifying Quarantine Protocol...")
time.sleep(1) # Give OS a moment to update file system

if not os.path.exists(test_file):
    print("    ✅ SUCCESS: Original malware was completely DELETED from disk.")
else:
    print("    ❌ FAILED: Malware is still on disk!")

# Check Quarantine Vault
quarantine_files = os.listdir(QUARANTINE_DIR) if os.path.exists(QUARANTINE_DIR) else []
if any("dummy_virus.bat.quarantine" in f for f in quarantine_files):
    print("    ✅ SUCCESS: Malware was encrypted and locked in the Quarantine Vault.")
else:
    print("    ❌ FAILED: Malware not found in Vault.")

print("\n=== SYSTEM TEST COMPLETE ===")
root.destroy()
