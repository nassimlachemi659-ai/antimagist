import json

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

slot0 = data["arrays"]["ArraySaves"]["cells"][0]
for idx, val in enumerate(slot0):
    val_str = str(val)
    if len(val_str) > 60:
        val_str = val_str[:60] + "..."
    # only print non-zero / non-empty or interesting
    if val != [0] and val != ["0"] and val != [""]:
        print(f"Row {idx:3d}: {val_str}")
