import base64
import gzip
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSWORD = b"dt7Qf2m_Kx9vR4pZs6Lw0Ej3Ub8Ay1Nc5Hg-TzP"
ITERATIONS = 100000

save_path = r"C:\Users\nst\Documents\Devices Tycoon\Save.dt"

with open(save_path, "r", encoding="utf-8") as f:
    envelope = f.read().strip()

parts = envelope.split("|")
print(f"Parts count: {len(parts)}, magic: {parts[0]}, comp: {parts[1]}")

salt = base64.b64decode(parts[2])
iv = base64.b64decode(parts[3])
ciphertext = base64.b64decode(parts[4])

print(f"Salt len: {len(salt)}, IV len: {len(iv)}, Ciphertext len: {len(ciphertext)}")

# Derive key
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=ITERATIONS,
)
key = kdf.derive(PASSWORD)

aesgcm = AESGCM(key)
decrypted = aesgcm.decrypt(iv, ciphertext, None)

if parts[1] == "gz":
    data = gzip.decompress(decrypted)
else:
    data = decrypted

text = data.decode("utf-8")
print(f"Successfully decrypted! Uncompressed length: {len(text)}")
print("Sample:\n", text[:1000])

with open(r"C:\Users\nst\.gemini\antigravity\scratch\save_decrypted.json", "w", encoding="utf-8") as f:
    f.write(text)
