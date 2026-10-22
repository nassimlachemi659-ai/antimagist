with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(rb"F5\s*=", content)]
print("Matches for F5 = :", matches)
for m in matches:
    print(content[m-20:m+200].decode("ascii", "backslashreplace"))
