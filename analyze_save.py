import json

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys in root:", data.keys())
print("Arrays in save:", data.get("arrays", {}).keys())

arr_saves = data["arrays"]["ArraySaves"]
print(f"ArraySaves dimensions: w={arr_saves['w']}, h={arr_saves['h']}, d={arr_saves['d']}")

# Let's inspect the cells of slot 0 (or whatever slots exist)
cells = arr_saves["cells"]
print(f"Number of primary slots: {len(cells)}")
for slot_idx, slot in enumerate(cells):
    print(f"--- Slot {slot_idx} (len {len(slot)}) ---")
    for row_idx in range(min(30, len(slot))):
        print(f"  row {row_idx}: {slot[row_idx]}")
