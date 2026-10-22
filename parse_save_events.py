with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_events.js", "rb") as f:
    data = f.read()

import re
matches = [m.start() for m in re.finditer(rb"ArraySaves", data)]
print("ArraySaves in save_events:", len(matches))
for m in matches:
    print(data[max(0, m - 50):min(len(data), m + 150)].decode("ascii", "backslashreplace"))
