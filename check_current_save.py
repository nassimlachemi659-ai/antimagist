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
salt = base64.b64decode(parts[2])
iv = base64.b64decode(parts[3])
ciphertext = base64.b64decode(parts[4])

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
key = kdf.derive(PASSWORD)
aesgcm = AESGCM(key)
decrypted = aesgcm.decrypt(iv, ciphertext, None)

data_bytes = gzip.decompress(decrypted) if parts[1] == "gz" else decrypted
data = json.loads(data_bytes.decode("utf-8"))

slot0 = data["arrays"]["ArraySaves"]["cells"][0]
print(f"Current Money: ${slot0[10][0]:,}")
print(f"Current RP: {slot0[11][0]}")
