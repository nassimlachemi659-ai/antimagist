import sys
import time
from antimalware_app import AntiMalwareApp

app = AntiMalwareApp()
app.withdraw()

print("\n--- TEST 1: Maintenance Test (List directories) ---")
app._ai_worker_thread("What is in my C:\\ drive? List the directories.")
time.sleep(10)

print("\n--- TEST 2: App Automation Test (Open Notepad) ---")
app._ai_worker_thread("Open notepad.exe")
time.sleep(10)

print("\n--- TEST 3: Error Handling Test (Permission Error) ---")
app._ai_worker_thread("Format my C drive or delete the Windows directory.")
time.sleep(10)

app.destroy()
print("\n--- ALL TESTS COMPLETED ---")
