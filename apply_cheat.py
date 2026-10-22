import base64
import gzip
import json
import os
import shutil
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSWORD = b"dt7Qf2m_Kx9vR4pZs6Lw0Ej3Ub8Ay1Nc5Hg-TzP"
ITERATIONS = 100000

save_path = r"C:\Users\nst\Documents\Devices Tycoon\Save.dt"
backup_path = r"C:\Users\nst\Documents\Devices Tycoon\Save.dt.orig_bak"

# 1. Backup original save if not already backed up
if not os.path.exists(backup_path):
    shutil.copy2(save_path, backup_path)
    print("Created original backup:", backup_path)

# 2. Read and decrypt save
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

if parts[1] == "gz":
    data_bytes = gzip.decompress(decrypted)
else:
    data_bytes = decrypted

data = json.loads(data_bytes.decode("utf-8"))

# 3. Check current money
old_money = data["arrays"]["ArraySaves"]["cells"][0][10][0]
print(f"Current money: ${old_money:,}")

# 4. Modify money to 2 Billion
target_money = 2000000000
data["arrays"]["ArraySaves"]["cells"][0][10][0] = target_money

# Also check other arrays if money is duplicated anywhere
new_json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

# 5. Compress and Encrypt
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

# 6. Verify decryption of our new envelope before saving
test_parts = new_envelope.split("|")
test_kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.b64decode(test_parts[2]), iterations=ITERATIONS)
test_key = test_kdf.derive(PASSWORD)
test_dec = AESGCM(test_key).decrypt(base64.b64decode(test_parts[3]), base64.b64decode(test_parts[4]), None)
test_decomp = gzip.decompress(test_dec).decode("utf-8")
test_obj = json.loads(test_decomp)
verified_money = test_obj["arrays"]["ArraySaves"]["cells"][0][10][0]
print(f"Verification successful! Verified money in new package: ${verified_money:,}")

# 7. Write to Save.dt and Save_Backup.dt
with open(save_path, "w", encoding="utf-8") as f:
    f.write(new_envelope)

save_dt_backup = r"C:\Users\nst\Documents\Devices Tycoon\Save_Backup.dt"
with open(save_dt_backup, "w", encoding="utf-8") as f:
    f.write(new_envelope)

print("SUCCESSFULLY SAVED TO DISK!")
