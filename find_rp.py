import re

with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    content = f.read()

# Let's search for words like Research, ResearchPoints, SciencePoints, Points, etc.
patterns = [b"ResearchPoints", b"Research_Points", b"ResearchPoint", b"Research", b"Points"]
for p in patterns:
    matches = [m.start() for m in re.finditer(re.escape(p), content, re.IGNORECASE)]
    print(f"Pattern {p}: {len(matches)} matches")
    for idx in matches[:5]:
        snippet = content[max(0, idx - 50):min(len(content), idx + 80)]
        print(f"  [{idx}] {snippet}")
