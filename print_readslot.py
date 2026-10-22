with open(r"C:\Users\nst\.gemini\antigravity\scratch\readslot.txt", "rb") as f:
    data = f.read()

text = data.decode("utf-8", errors="replace")
safe = text.encode("ascii", "backslashreplace").decode("ascii")
print(safe)
