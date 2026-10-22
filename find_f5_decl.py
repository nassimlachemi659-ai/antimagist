with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(rb"(?:const|var|let)\s+F5\s*=", content)]
print("Matches for F5=", matches)
for m in matches:
    print(content[m:m+300].decode("ascii", "backslashreplace"))
