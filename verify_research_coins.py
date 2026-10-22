with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(rb"ResearchCoins", content)]
print("ResearchCoins occurrences:", len(matches))
for m in matches[:5]:
    snippet = content[max(0, m - 50):min(len(content), m + 100)]
    print(snippet.decode("ascii", "backslashreplace"))
