import struct

with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(16 + 4 + 8 + 4)
    for i in range(5):
        raw36 = f.read(36)
        print(f"Entry {i} raw36:", [hex(x) for x in struct.unpack(">QQQQI", raw36)])
        name_len = struct.unpack(">QQQQI", raw36)[4]
        raw_name = f.read(name_len)
        print(f"Entry {i} raw_name ({name_len}):", raw_name)
