with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(15555000)
    data = f.read(7000)

text = data.decode("utf-8", errors="replace")
safe = text.encode("ascii", "backslashreplace").decode("ascii")

# Find F5.DAYS or F5
pos = safe.find("DAYS")
if pos != -1:
    print(safe[max(0, pos - 500):pos + 500])
else:
    print("DAYS not found in this chunk")
