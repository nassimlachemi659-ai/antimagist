with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

needle = b"ArraySaves"
pos = 0
i = 0
while True:
    idx = content.find(needle, pos)
    if idx == -1:
        break
    pos = idx + len(needle)
    i += 1
    snippet = content[max(0, idx - 150):min(len(content), idx + 250)]
    print(f"=== Match {i} at {idx} ===")
    try:
        print(snippet.decode("utf-8", errors="replace"))
    except:
        print(snippet)
