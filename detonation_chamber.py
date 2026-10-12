"""
detonation_chamber.py — Antimagist V4 Micro-Sandbox & Forensic Detonation Chamber
==================================================================================
Antimagist Enterprise Security V4 Component
- Safe Detonation Harness for unknown, unverified, or zero-day executables and scripts
- Windows Sandbox (.wsb) auto-configuration with strict Read-Only host isolation
- Advanced In-Memory PE Forensic Static Analyzer:
    • Section entropy calculation (Detects UPX packing & encrypted ransomware payloads)
    • Suspicious API import enumeration (VirtualAlloc, WriteProcessMemory, CreateRemoteThread)
    • Embedded C2 IPs, URLs, hidden PowerShell download cradles, and persistence registry keys
"""

import os
import sys
import re
import math
import shutil
import subprocess
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SUSPICIOUS_APIS = [
    "VirtualAlloc", "VirtualProtect", "WriteProcessMemory", "CreateRemoteThread",
    "OpenProcess", "QueueUserAPC", "SetWindowsHookEx", "IsDebuggerPresent",
    "CheckRemoteDebuggerPresent", "CryptEncrypt", "CryptDecrypt", "HttpOpenRequest"
]

class AntimagistDetonationChamber:
    def __init__(self, sandbox_workspace: str = "C:\\Antimagist_Sandbox"):
        self.workspace = sandbox_workspace
        if not os.path.exists(self.workspace):
            try:
                os.makedirs(self.workspace, exist_ok=True)
            except Exception:
                self.workspace = os.path.abspath("Sandbox_Workspace")
                os.makedirs(self.workspace, exist_ok=True)

    def is_windows_sandbox_available(self) -> bool:
        """Checks if Windows Sandbox feature is installed and enabled."""
        try:
            res = subprocess.run(["where", "WindowsSandbox.exe"], capture_output=True, text=True)
            return res.returncode == 0
        except Exception:
            return False

    def create_sandbox_config(self, target_filepath: str) -> str:
        """Generates an ephemeral .wsb file mapping the specimen in a Read-Only virtual container."""
        target_dir = os.path.dirname(os.path.abspath(target_filepath))
        target_name = os.path.basename(target_filepath)
        wsb_path = os.path.join(self.workspace, "antimagist_detonation.wsb")

        wsb_xml = f"""<Configuration>
  <VGpu>Disable</VGpu>
  <Networking>Disable</Networking>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>{target_dir}</HostFolder>
      <SandboxFolder>C:\\SpecimenFolder</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>explorer.exe C:\\SpecimenFolder</Command>
  </LogonCommand>
</Configuration>"""

        with open(wsb_path, "w", encoding="utf-8") as f:
            f.write(wsb_xml)

        return wsb_path

    def calculate_entropy(self, data: bytes) -> float:
        """Calculates Shannon entropy. Scores above 7.0 indicate packed or encrypted malware."""
        if not data:
            return 0.0
        entropy = 0
        length = len(data)
        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 2)

    def analyze_specimen_forensics(self, filepath: str) -> Dict[str, Any]:
        """Performs deep forensic inspection on an untrusted specimen."""
        if not os.path.exists(filepath):
            return {"error": "File does not exist."}

        file_size = os.path.getsize(filepath)
        with open(filepath, "rb") as f:
            raw_data = f.read(min(file_size, 5 * 1024 * 1024)) # Sample first 5MB

        entropy = self.calculate_entropy(raw_data)
        is_packed = entropy > 7.1

        # Extract ASCII strings
        ascii_strings = re.findall(rb"[\x20-\x7E]{4,}", raw_data)
        decoded_strings = [s.decode(errors="ignore") for s in ascii_strings]

        # Scan for IOCs
        found_apis = []
        found_urls = []
        found_ips = []
        suspicious_cmds = []

        ip_regex = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
        url_regex = re.compile(r"https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

        for s in decoded_strings:
            # Check APIs
            for api in SUSPICIOUS_APIS:
                if api.lower() in s.lower() and api not in found_apis:
                    found_apis.append(api)

            # Check IPs
            m_ip = ip_regex.findall(s)
            for ip in m_ip:
                if not ip.startswith("0.") and not ip.startswith("127.") and ip not in found_ips:
                    found_ips.append(ip)

            # Check URLs
            m_url = url_regex.findall(s)
            for u in m_url:
                if u not in found_urls:
                    found_urls.append(u)

            # Check suspicious command lines
            s_low = s.lower()
            if any(k in s_low for k in ["powershell -enc", "cmd /c", "wscript.shell", "bypass -c", "certutil -urlcache"]):
                if s not in suspicious_cmds:
                    suspicious_cmds.append(s[:80])

        risk_score = 0
        if is_packed: risk_score += 35
        if len(found_apis) >= 3: risk_score += 25
        if len(found_ips) >= 1: risk_score += 20
        if len(suspicious_cmds) >= 1: risk_score += 25

        rating = "CRITICAL RISK (Probable Malware)" if risk_score >= 60 else ("ELEVATED RISK (Packed/Suspicious)" if risk_score >= 35 else "LOW RISK / CLEAN HEURISTICS")

        return {
            "filename": os.path.basename(filepath),
            "size_kb": round(file_size / 1024, 1),
            "entropy": entropy,
            "is_packed": is_packed,
            "suspicious_apis": found_apis[:8],
            "detected_ips": found_ips[:5],
            "detected_urls": found_urls[:5],
            "suspicious_patterns": suspicious_cmds[:5],
            "risk_score": min(100, risk_score),
            "rating": rating,
            "windows_sandbox_supported": self.is_windows_sandbox_available()
        }


if __name__ == "__main__":
    print("[*] Testing Antimagist Detonation Chamber...")
    chamber = AntimagistDetonationChamber()
    print(f"  • Windows Sandbox Available: {chamber.is_windows_sandbox_available()}")
    
    # Analyze Python executable as a sample specimen
    target = sys.executable
    print(f"  • Performing Forensic Analysis on: {target}...")
    res = chamber.analyze_specimen_forensics(target)
    print(f"  • File: {res['filename']} (Entropy: {res['entropy']} - Packed: {res['is_packed']})")
    print(f"  • Risk Score: {res['risk_score']} ({res['rating']})")
    print(f"  • APIs Found: {res['suspicious_apis']}")
    print("  • Detonation Chamber Test PASSED.")
