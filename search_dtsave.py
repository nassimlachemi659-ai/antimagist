import os

needle = b"DTSAVE1"
game_dir = r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon"

for root, dirs, files in os.walk(game_dir):
    for fn in files:
        fp = os.path.join(root, fn)
        try:
            with open(fp, "rb") as f:
                content = f.read()
                if needle in content:
                    print("Found DTSAVE1 in:", fp)
                    idx = content.find(needle)
                    print("Context:", content[max(0, idx-100):min(len(content), idx+200)])
        except Exception as e:
            print("Error reading", fp, e)
