with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(rb"\bDAYS\s*:", content)]
print("Matches for DAYS:", matches)
for m in matches:
    snippet = content[m-50:m+250]
    print(snippet.decode("ascii", "backslashreplace"))
