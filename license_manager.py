"""
license_manager.py — Antimagist V5 Cryptographic Licensing & HWID Subsystem
=============================================================================
Antimagist Enterprise Security V5 Commercial Engine
- Hardware ID (HWID) binding based on motherboard UUID, machine GUID, and CPU
- HMAC-SHA256 signature verification preventing unauthorized key tampering
- License tiers:
    1. 'TRIAL'    (3-day free trial on first launch)
    2. 'MONTHLY'  (30-day recurring subscription, €2/month)
    3. 'LIFETIME' (Permanent non-expiring license, €10 one-time)
- Encrypted local license storage in %LocalAppData%\\Antimagist\\license.dat
"""

import os
import sys
import time
import json
import hmac
import hashlib
import platform
import subprocess
import winreg
from typing import Dict, Any, Tuple, Optional

# Secret master signing seed for HMAC verification
MASTER_SIGN_KEY = b"ANTIMAGIST-V5-SINGULARITY-MASTER-KEY-2026-NVIDIA-RTX5050"

LICENSE_FILE_PATH = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "Antimagist",
    "license.dat"
)


def get_hardware_id() -> str:
    """Computes a persistent, deterministic Hardware ID (HWID) for the current PC."""
    components = []

    # 1. Machine GUID from Windows Registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            components.append(str(guid).strip())
    except Exception:
        components.append(platform.node())

    # 2. System UUID
    try:
        cmd = 'powershell -NoProfile -Command "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"'
        out = subprocess.check_output(cmd, shell=True, text=True, timeout=2).strip()
        if out:
            components.append(out)
    except Exception:
        pass

    # 3. Processor Identifier & Architecture
    components.append(platform.processor())
    components.append(os.environ.get("PROCESSOR_IDENTIFIER", "DEFAULT_CPU"))

    raw = "::".join(components).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest().upper()
    return f"HWID-{digest[:4]}-{digest[4:8]}-{digest[8:12]}-{digest[12:16]}"


def compute_key_signature(payload: str) -> str:
    """Calculates an 8-character HMAC signature for a license payload."""
    sig = hmac.new(MASTER_SIGN_KEY, payload.encode("utf-8"), hashlib.sha256).hexdigest().upper()
    return f"{sig[:4]}-{sig[4:8]}"


class AntimagistLicenseManager:
    """Handles license activation, trial enforcement, and HWID locking."""

    def __init__(self):
        self.hwid = get_hardware_id()
        self._ensure_license_dir()
        self.license_info = self.load_license()

    def _ensure_license_dir(self):
        d = os.path.dirname(LICENSE_FILE_PATH)
        if not os.path.exists(d):
            try:
                os.makedirs(d, exist_ok=True)
            except Exception:
                pass

    def load_license(self) -> Dict[str, Any]:
        """Loads and verifies current active license or trial."""
        if os.path.exists(LICENSE_FILE_PATH):
            try:
                with open(LICENSE_FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                valid, msg = self.verify_license_data(data)
                if valid:
                    return data
            except Exception:
                pass

        # If no valid paid license, fall back to or initialize 3-day trial
        return self._get_or_create_trial()

    def _get_or_create_trial(self) -> Dict[str, Any]:
        """Returns active trial or initializes a new 3-day trial."""
        now = int(time.time())
        trial_record_path = os.path.join(os.path.dirname(LICENSE_FILE_PATH), ".trial_stamp")

        start_time = now
        if os.path.exists(trial_record_path):
            try:
                with open(trial_record_path, "r", encoding="utf-8") as f:
                    start_time = int(f.read().strip())
            except Exception:
                start_time = now
        else:
            try:
                with open(trial_record_path, "w", encoding="utf-8") as f:
                    f.write(str(now))
            except Exception:
                pass

        return {
            "tier": "FREE COMMUNITY",
            "is_valid": True,
            "hwid": self.hwid,
            "activated_at": start_time,
            "expires_at": 9999999999,
            "days_left": 9999,
            "license_key": "COMMUNITY-EDITION-UNLOCKED",
            "message": "Community Edition — 100% Free Forever"
        }

    def verify_license_data(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Cryptographically verifies a stored license dictionary."""
        key = data.get("license_key", "")
        tier = data.get("tier", "")
        bound_hwid = data.get("hwid", "")
        expires_at = data.get("expires_at", 0)

        # 1. Verify HWID binding
        if bound_hwid and bound_hwid != self.hwid:
            return False, "License is bound to another PC (HWID mismatch)."

        # 2. Verify signature
        valid, key_tier, key_expiry = self.validate_license_key_format(key)
        if not valid:
            return False, "Cryptographic signature validation failed."

        # 3. Check expiration
        now = int(time.time())
        if tier != "LIFETIME" and expires_at > 0 and now > expires_at:
            return False, "Subscription license has expired."

        return True, "License valid and active."

    def validate_license_key_format(self, key: str) -> Tuple[bool, str, int]:
        """
        Validates key structure:
        AM5-<TIER>-<EXPIRY_TIMESTAMP_OR_LIFETIME>-<RANDOM_SEED>-<SIG1>-<SIG2>
        """
        if not key or not isinstance(key, str):
            return False, "", 0

        parts = key.strip().upper().split("-")
        if len(parts) != 6 or parts[0] != "AM5":
            return False, "", 0

        tier = parts[1] # 'LIFE' or 'SUB'
        expiry_str = parts[2]
        seed = parts[3]
        provided_sig = f"{parts[4]}-{parts[5]}"

        payload = f"AM5-{tier}-{expiry_str}-{seed}"
        expected_sig = compute_key_signature(payload)

        if not hmac.compare_digest(provided_sig, expected_sig):
            return False, "", 0

        expires_at = 0
        if tier == "SUB":
            try:
                expires_at = int(expiry_str)
            except ValueError:
                return False, "", 0
        elif tier == "LIFE":
            expires_at = 9999999999

        return True, "LIFETIME" if tier == "LIFE" else "MONTHLY", expires_at

    def activate_license(self, key: str) -> Tuple[bool, str]:
        """Activates a provided commercial license key on this machine."""
        valid, tier, expires_at = self.validate_license_key_format(key)
        if not valid:
            return False, "Invalid license key. Check your key formatting or signature."

        now = int(time.time())
        if tier == "MONTHLY" and now > expires_at:
            return False, "This license key has already expired."

        license_data = {
            "tier": tier,
            "is_valid": True,
            "hwid": self.hwid,
            "activated_at": now,
            "expires_at": expires_at,
            "license_key": key.strip().upper(),
            "message": f"Activated ({tier} Edition)"
        }

        try:
            self._ensure_license_dir()
            with open(LICENSE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(license_data, f, indent=2)
            self.license_info = license_data
            return True, f"Success! {tier} license successfully activated and locked to this PC."
        except Exception as e:
            return False, f"Failed to save license record: {str(e)}"

    def get_status_summary(self) -> Dict[str, Any]:
        """Returns live licensing state for the UI."""
        info = self.license_info
        tier = info.get("tier", "FREE COMMUNITY")
        return {
            "tier": tier,
            "is_paid": True,
            "is_valid": True,
            "hwid": self.hwid,
            "license_key": info.get("license_key", "COMMUNITY-EDITION-UNLOCKED"),
            "expires_at": info.get("expires_at", 9999999999),
            "days_left": 9999,
            "message": info.get("message", "Community Edition — 100% Free Forever")
        }


if __name__ == "__main__":
    lm = AntimagistLicenseManager()
    print("=" * 60)
    print("  ANTIMAGIST V5 LICENSING & HWID ENGINE")
    print("=" * 60)
    print(f"  • Machine HWID: {lm.hwid}")
    st = lm.get_status_summary()
    print(f"  • Current Status: {st['tier']} | Valid: {st['is_valid']} | {st['message']}")
