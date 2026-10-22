import json

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

slot0 = data["arrays"]["ArraySaves"]["cells"][0]
print("Row 88:")
print(slot0[88])

# Let's inspect rows around 88 or any other interesting rows
for r in [9, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 71, 75, 80, 81, 88, 101, 104, 105, 109, 112]:
    print(f"Row {r:3d}: {slot0[r]}")
