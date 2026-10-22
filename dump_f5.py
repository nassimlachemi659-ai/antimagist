with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

idx = 15562704
snippet = content[idx - 1500:idx + 500]

with open(r"C:\Users\nst\.gemini\antigravity\scratch\f5_snippet.js", "wb") as out:
    out.write(snippet)

print("Saved f5 snippet!")
