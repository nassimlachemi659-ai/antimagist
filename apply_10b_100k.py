import base64
import gzip
import json
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSWORD = b"dt7Qf2m_Kx9vR4pZs6Lw0Ej3Ub8Ay1Nc5Hg-TzP"
ITERATIONS = 100000

save_path = r"C:\Users\nst\Documents\Devices Tycoon\Save.dt"
save_backup_path = r"C:\Users\nst\Documents\Devices Tycoon\Save_Backup.dt"

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
print(f"Old Money: ${slot0[10][0]:,}")
print(f"Old RP: {slot0[11][0]:,}")

# Update to 10 Billion Money and 100k RP
slot0[10][0] = 10000000000
slot0[11][0] = 100000

new_json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
compressed = gzip.compress(new_json_str.encode("utf-8"))
new_salt = os.urandom(16)
new_iv = os.urandom(12)

new_kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=new_salt, iterations=ITERATIONS)
new_key = new_kdf.derive(PASSWORD)
new_aesgcm = AESGCM(new_key)
new_ciphertext = new_aesgcm.encrypt(new_iv, compressed, None)

new_envelope = (
    f"DTSAVE1|gz|"
    f"{base64.b64encode(new_salt).decode()}|"
    f"{base64.b64encode(new_iv).decode()}|"
    f"{base64.b64encode(new_ciphertext).decode()}"
)

# Verify
test_parts = new_envelope.split("|")
test_kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.b64decode(test_parts[2]), iterations=ITERATIONS)
test_key = test_kdf.derive(PASSWORD)
test_dec = AESGCM(test_key).decrypt(base64.b64decode(test_parts[3]), base64.b64decode(test_parts[4]), None)
test_decomp = gzip.decompress(test_dec).decode("utf-8")
test_obj = json.loads(test_decomp)
v_money = test_obj["arrays"]["ArraySaves"]["cells"][0][10][0]
v_rp = test_obj["arrays"]["ArraySaves"]["cells"][0][11][0]

print(f"Verified! Money: ${v_money:,}, RP: {v_rp:,}")

with open(save_path, "w", encoding="utf-8") as f:
    f.write(new_envelope)

with open(save_backup_path, "w", encoding="utf-8") as f:
    f.write(new_envelope)

print("SUCCESSFULLY APPLIED 10B AND 100K RP!")
