import json

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

slot0 = data["arrays"]["ArraySaves"]["cells"][0]
for idx, val in enumerate(slot0[:25]):
    print(f"Index {idx}: {val}")
