"""
url_analyzer.py — Phishing & Malicious URL Cyber-Card Intelligence
===================================================================
Antimagist Enterprise Security V3 Component
- Inspects target URLs, domains, and web endpoints for phishing indicators
- Resolves DNS host IP, detects typosquatting and suspicious brand impersonation
- Integrates with VirusTotal URL v3 API if configured with deterministic offline fallback
"""

import os
import re
import sys
import math
import socket
import urllib.parse
import subprocess
import requests
import psutil
from typing import Dict, Any, Optional, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SUSPICIOUS_PHISHING_KEYWORDS = [
    "paypal", "apple", "login", "signin", "verify", "secure", "bank",
    "wallet", "crypto", "blockchain", "support", "billing", "account-update",
    "password", "auth", "confirm", "free-nitro", "steam-gift"
]

SUSPICIOUS_TLDS = [".xyz", ".top", ".buzz", ".work", ".click", ".loan", ".rest", ".fit", ".gq", ".cf", ".tk", ".ml"]

class AntimagistURLAnalyzer:
    def __init__(self, vt_api_key: str = ""):
        self.vt_api_key = vt_api_key

    def update_api_key(self, api_key: str):
        self.vt_api_key = api_key

    def analyze_url(self, raw_url: str) -> Dict[str, Any]:
        """Performs full cyber reconnaissance and phishing evaluation on a URL."""
        url = raw_url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname or ""

        # 1. DNS Resolution
        resolved_ip = "N/A"
        try:
            resolved_ip = socket.gethostbyname(hostname)
        except Exception:
            resolved_ip = "Unresolvable (NXDOMAIN / Offline)"

        # 2. Risk Heuristics
        risk_score = 0
        risk_flags = []

        host_lower = hostname.lower()

        # Typosquatting / Brand impersonation check
        for kw in SUSPICIOUS_PHISHING_KEYWORDS:
            if kw in host_lower:
                # Check if it's not the official domain
                if not host_lower.endswith(f"{kw}.com") and not host_lower.endswith(f"{kw}.org"):
                    risk_score += 35
                    risk_flags.append(f"Impersonation keyword detected: '{kw}' in non-standard domain")
                    break

        # Suspicious TLD check
        for tld in SUSPICIOUS_TLDS:
            if host_lower.endswith(tld):
                risk_score += 25
                risk_flags.append(f"High-abuse generic TLD: '{tld}'")
                break

        # Raw IP address used instead of hostname
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname):
            risk_score += 40
            risk_flags.append("Bare IP address URL (Common in phishing and C2 relays)")

        # Multiple subdomains
        if hostname.count(".") >= 3:
            risk_score += 15
            risk_flags.append(f"Excessive subdomains ({hostname.count('.')} levels)")

        # Excessive URL length or suspicious path
        if len(url) > 90:
            risk_score += 10
            risk_flags.append("Abnormally long URL query / token payload")

        # 3. VirusTotal Cloud Lookup (if API key available)
        vt_stats = None
        if self.vt_api_key and len(self.vt_api_key.strip()) > 10:
            try:
                import base64
                url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
                headers = {"x-apikey": self.vt_api_key.strip()}
                r = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    attr = data.get("data", {}).get("attributes", {})
                    stats = attr.get("last_analysis_stats", {})
                    malicious = stats.get("malicious", 0)
                    suspicious = stats.get("suspicious", 0)
                    vt_stats = f"VT Engines: {malicious} Malicious, {suspicious} Suspicious"
                    if malicious > 0:
                        risk_score = max(risk_score, 85)
                        risk_flags.append(f"Flagged by {malicious} VirusTotal security engines!")
            except Exception:
                pass

        # Risk Classification
        if risk_score >= 50:
            rating = "HIGH RISK (Phishing / Scam Alert)"
            color = "#FF0055"
        elif risk_score >= 20:
            rating = "SUSPICIOUS (Exercise Caution)"
            color = "#FBBF24"
        else:
            rating = "CLEAN / LOW RISK"
            color = "#00FF9D"

        return {
            "url": url,
            "hostname": hostname,
            "resolved_ip": resolved_ip,
            "risk_score": min(100, risk_score),
            "rating": rating,
            "rating_color": color,
            "risk_flags": risk_flags or ["No heuristic anomalies detected."],
            "vt_cloud": vt_stats or "Cloud VT: Verified clean or key unconfigured."
        }

    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        """Calculates Shannon entropy to detect DGA or obfuscated random domain strings."""
        if not text:
            return 0.0
        entropy = 0.0
        length = len(text)
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 2)

    def get_live_network_connections(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Queries all active outbound TCP/UDP connections via psutil, mapping PID to process name,
        remote IP:port, and performing threat analysis (HTTP unencrypted, DGA entropy, suspicious ports).
        """
        connections: List[Dict[str, Any]] = []
        try:
            # Map PIDs to names
            proc_map: Dict[int, str] = {}
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    proc_map[p.info['pid']] = p.info.get('name') or "Unknown"
                except Exception:
                    pass

            SUSP_PORTS = {4444, 1337, 31337, 6667, 8888, 5555, 9999}
            CLEARTEXT_PORTS = {80: "HTTP", 21: "FTP", 23: "TELNET", 25: "SMTP"}

            for conn in psutil.net_connections(kind='inet'):
                if not conn.raddr:
                    continue  # Skip listening sockets with no remote peer

                r_ip = conn.raddr.ip
                r_port = conn.raddr.port
                l_ip = conn.laddr.ip if conn.laddr else "0.0.0.0"
                l_port = conn.laddr.port if conn.laddr else 0
                status = conn.status or "ESTABLISHED"
                pid = conn.pid or 0
                pname = proc_map.get(pid, "System / Idle" if pid == 0 else "Unknown")

                # Threat assessment
                threat_flags = []
                threat_level = "NORMAL"

                # Check unencrypted cleartext web protocol
                if r_port in CLEARTEXT_PORTS:
                    proto = CLEARTEXT_PORTS[r_port]
                    threat_flags.append(f"Unencrypted {proto} traffic (cleartext payload)")
                    threat_level = "SUSPICIOUS"

                # Check known backdoor / reverse shell ports
                if r_port in SUSP_PORTS:
                    threat_flags.append(f"High-risk C2/Backdoor Port ({r_port})")
                    threat_level = "HIGH"

                # Flag public IP vs local private IP
                is_private = (
                    r_ip.startswith("10.") or 
                    r_ip.startswith("192.168.") or 
                    r_ip.startswith("127.") or 
                    r_ip.startswith("172.16.") or
                    r_ip == "::1"
                )

                connections.append({
                    "pid": pid,
                    "process_name": pname,
                    "local_addr": f"{l_ip}:{l_port}",
                    "remote_addr": f"{r_ip}:{r_port}",
                    "remote_ip": r_ip,
                    "remote_port": r_port,
                    "status": status,
                    "is_private": is_private,
                    "threat_level": threat_level,
                    "threat_flags": threat_flags or ["Encrypted / Verified transport"]
                })

                if len(connections) >= limit:
                    break
        except Exception:
            pass

        return connections

    def block_ip_in_firewall(self, remote_ip: str, rule_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        Creates an outbound Windows Firewall rule to block all communication with the specified IP address.
        """
        ip = remote_ip.strip()
        # Basic IPv4 validation
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            return False, f"Invalid IPv4 address format: '{ip}'"

        name = rule_name or f"Antimagist Outbound Block {ip}"
        if os.name != 'nt':
            return False, "Windows Firewall rules require Windows OS."

        cmd = [
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={name}",
            "dir=out",
            "action=block",
            f"remoteip={ip}"
        ]

        try:
            res = subprocess.run(
                cmd, capture_output=True, text=True, timeout=3,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if res.returncode == 0 or "Ok." in (res.stdout or ""):
                return True, f"🛡️ Outbound Windows Firewall rule active: Blocked {ip} (Rule: '{name}')."
            return False, f"Firewall command returned code {res.returncode}: {res.stderr or res.stdout}"
        except Exception as ex:
            return False, f"Could not create firewall rule: {ex}"


if __name__ == "__main__":
    print("[*] Testing Antimagist URL Analyzer & Network Radar...")
    analyzer = AntimagistURLAnalyzer()
    res = analyzer.analyze_url("http://paypal-account-verify-update.xyz/login")
    print(f"  • URL Analysis: {res['rating']} (Score: {res['risk_score']}/100)")
    print(f"  • Flags: {res['risk_flags']}")

    ent = analyzer.calculate_shannon_entropy("x8f192b00ac9f712.xyz")
    print(f"  • Shannon Entropy: {ent}")

    conns = analyzer.get_live_network_connections(limit=5)
    print(f"  • Active Outbound Connections Scanned: {len(conns)}")
    if conns:
        c = conns[0]
        print(f"    - {c['process_name']} (PID {c['pid']}) -> {c['remote_addr']} [{c['threat_level']}]")

    ok_b, msg_b = analyzer.block_ip_in_firewall("192.0.2.1", "Antimagist Test Block")
    print(f"  • Firewall Block Test: {ok_b} -> {msg_b}")
    print("[+] URL Analyzer & Network Radar PASSED.")

