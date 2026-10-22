with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

idx = 15562704
# Look 5000 bytes before 15562704
start = max(0, idx - 5000)
snippet = content[start:idx]
pos = snippet.rfind(b"F5")
print("Found F5 in snippet at:", pos)
if pos != -1:
    f5_chunk = snippet[pos-100:pos+300]
    safe = f5_chunk.decode("ascii", "backslashreplace")
    print("F5 snippet:\n", safe)
