import struct

with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    header = f.read(16)
    print("Header:", header)
    # Let's inspect next 64 bytes
    data = f.read(128)
    print("Next bytes:", data)
