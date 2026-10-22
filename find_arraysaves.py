with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

# Let's find occurrences of ArraySaves or ResearchPoints
needle = b"ArraySaves"
pos = 0
found = []
while True:
    idx = content.find(needle, pos)
    if idx == -1:
        break
    found.append(idx)
    pos = idx + len(needle)

print(f"Found {len(found)} occurrences of ArraySaves")
for idx in found[:10]:
    snippet = content[max(0, idx - 100):min(len(content), idx + 200)]
    print(f"--- at {idx} ---")
    print(snippet)
