with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(15562000)
    data = f.read(1000)

with open(r"C:\Users\nst\.gemini\antigravity\scratch\readslot.txt", "wb") as out:
    out.write(data)

print("Saved readslot.txt!")
