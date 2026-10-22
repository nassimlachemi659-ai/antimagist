import json

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys:", data.keys())
for k, v in data.items():
    if k != "arrays":
        print(f"Key {k}: {type(v)} = {v}")
