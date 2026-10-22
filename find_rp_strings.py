with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

# Russian: Очки исследований
needle = "Очки исследований".encode("utf-8")
idx = content.find(needle)
print("Found Russian term:", idx)
if idx != -1:
    snippet = content[idx-200:idx+300]
    print(snippet.decode("ascii", "backslashreplace"))

# English: "Research points" or "Research Points"
for eng in [b"Research points", b"Research Points"]:
    p = 0
    while True:
        pos = content.find(eng, p)
        if pos == -1:
            break
        print(f"Found '{eng.decode()}' at {pos}:")
        print(content[pos-100:pos+200].decode("ascii", "backslashreplace"))
        p = pos + len(eng)
        break
