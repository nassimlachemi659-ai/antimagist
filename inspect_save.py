import base64
import os
import zlib
import gzip

save_path = r"C:\Users\nst\Documents\Devices Tycoon\Save.dt"
settings_path = r"C:\Users\nst\Documents\Devices Tycoon\Settings.dt"

def check_file(path):
    print(f"=== Checking {path} ===")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()
    print("Length:", len(content))
    print("Prefix:", content[:100])
    try:
        raw = base64.b64decode(content)
        print("Decoded length:", len(raw))
        print("First 32 bytes:", raw[:32])
        # Try zlib
        try:
            decomp = zlib.decompress(raw)
            print("Zlib decompressed successfully! Length:", len(decomp))
            print("Decomp prefix:", decomp[:200])
            return
        except Exception as e:
            print("Zlib failed:", e)
        # Try gzip
        try:
            decomp = gzip.decompress(raw)
            print("Gzip decompressed successfully! Length:", len(decomp))
            print("Decomp prefix:", decomp[:200])
            return
        except Exception as e:
            print("Gzip failed:", e)
        # Try raw utf-8
        try:
            txt = raw.decode("utf-8")
            print("UTF-8 decoded successfully! Prefix:", txt[:200])
            return
        except Exception as e:
            print("UTF-8 failed:", e)
    except Exception as e:
        print("Base64 decode failed:", e)

check_file(settings_path)
check_file(save_path)
