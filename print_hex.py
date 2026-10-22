with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(16 + 4 + 8 + 4)
    data = f.read(150)
    for i, b in enumerate(data):
        c = chr(b) if 32 <= b <= 126 else '.'
        print(f"{i:3d}: 0x{b:02x} ({c})")
