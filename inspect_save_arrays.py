import json

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

arrays = data.get("arrays", {})
print("Array count:", len(arrays))
for name, arr in arrays.items():
    w = arr.get("w", 0)
    h = arr.get("h", 0)
    d = arr.get("d", 0)
    # Check if Research or Point is in the name
    if any(k in name.lower() for k in ["research", "point", "stat", "save", "company"]):
        print(f"Array: {name} ({w}x{h}x{d})")
