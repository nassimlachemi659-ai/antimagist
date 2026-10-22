with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

idx = content.find(b'_MAGIC="DTSAVE1"')
start = max(0, idx - 2000)
end = min(len(content), idx + 8000)

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_logic.js", "wb") as out:
    out.write(content[start:end])

print("Dumped save logic! Size:", end - start)
