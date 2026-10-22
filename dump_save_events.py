with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

idx = 16310972
snippet = content[idx - 6000:idx + 1000]

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_events.js", "wb") as out:
    out.write(snippet)

print("Saved save_events.js!")
