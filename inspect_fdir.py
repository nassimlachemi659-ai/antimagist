with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(16)
    chunk_name = f.read(4)
    # let's read 12 bytes
    h = f.read(12)
    print("chunk_name:", chunk_name, "h:", h)
    # unpack as uint32 or uint64
    import struct
    print("h uint32:", struct.unpack(">3I", h))
    print("h uint32 LE:", struct.unpack("<3I", h))
    # Let's inspect next 200 bytes
    sample = f.read(250)
    print("sample:", repr(sample))
