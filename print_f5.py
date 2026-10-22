with open(r"C:\Users\nst\.gemini\antigravity\scratch\f5_snippet.js", "rb") as f:
    data = f.read()

# Let's decode or print as ascii-safe
text = data.decode("utf-8", errors="replace")
# Filter out cyrillic to pure ascii representations so it doesn't crash cp1252
safe_text = text.encode("ascii", "backslashreplace").decode("ascii")
print(safe_text[:3000])
