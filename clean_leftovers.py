import os
import shutil

dirs = [
    r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods\Boeing 737 Burning Edition 486 1 2026-08-30T15-28Z KRYbzsnBW",
    r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods\Gwel's High Building-382-1-1727573253",
    os.path.expanduser(r"~/Documents/Teardown/mods/Boeing 737 Burning Edition 486 1 2026-08-30T15-28Z KRYbzsnBW"),
    os.path.expanduser(r"~/Documents/Teardown/mods/Gwel's High Building-382-1-1727573253")
]

for d in dirs:
    if os.path.exists(d):
        shutil.rmtree(d, ignore_errors=True)
        print("Removed: ", d)
