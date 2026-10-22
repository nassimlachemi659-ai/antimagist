import struct
import json

with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(16)
    chunk_name = f.read(4) # b'fdir'
    chunk_len = struct.unpack(">Q", f.read(8))[0]
    entry_count = struct.unpack(">I", f.read(4))[0]
    
    entries = {}
    for i in range(entry_count):
        raw = f.read(36)
        offset, flags, comp_size, uncomp_size, name_len = struct.unpack(">QQQQI", raw)
        name = f.read(name_len).decode('utf-8')
        entries[name] = (offset, comp_size, uncomp_size)

print("Total entries:", len(entries))
for target in ["data.json", "c3runtime.js", "scripts/main.js", "scripts/c3runtime.js"]:
    if target in entries:
        print(f"Found {target}: {entries[target]}")
        # Let's extract target!
        # Where does data start? data chunk follows fdir chunk!
        # header = 16 + 4 + 8 + chunk_len
        # Let's check chunk after fdir
