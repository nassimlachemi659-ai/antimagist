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
import socket
import urllib.parse
import requests
from typing import Dict, Any, Optional

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
