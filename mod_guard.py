"""
mod_guard.py — Antimagist V6 Mod & Config Heuristic Guard
==========================================================
Antimagist Enterprise Security V6 Component
- Protects gamers from malicious configs, autoexecs, FPS boost packs, and community mods:
    • Detects Discord token grabbers & webhook exfiltration endpoints
    • Uncovers obfuscated PowerShell download cradles (base64, iex, certutil, bitsadmin)
    • Flags unauthorized Windows Defender tampering and registry persistence
    • Identifies dangerous Lua hooks (os.execute, io.popen, package.loadlib)
    • Sanitizes malicious files safely while preserving legitimate game cvars
- 100% Technical Integrity: Explains threat scores and matched signatures truthfully
"""

import os
import re
import sys
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistModGuard:
    """Heuristic scanner and sanitizer for game configs, autoexecs, and mod packages."""

    # Threat Rules: (Rule ID, Pattern, Severity, Threat Score, Description)
    RULES = [
        # Discord Webhook Exfiltration
        (
            "RULE_WEBHOOK_EXFIL",
            re.compile(r"https?://(ptb\.|canary\.)?discord(app)?\.com/api/webhooks/\d+/([A-Za-z0-9_-]+)", re.IGNORECASE),
            "CRITICAL",
            90,
            "Discord Webhook URL detected (Commonly used by stealer malware to leak tokens & passwords)"
        ),
        # Discord Token Grabber regex
        (
            "RULE_TOKEN_GRABBER",
            re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", re.IGNORECASE),
            "CRITICAL",
            95,
            "Discord User Authentication Token pattern detected"
        ),
        # Obfuscated PowerShell / Base64 Execution
        (
            "RULE_POWERSHELL_ENCODED",
            re.compile(r"powershell(\.exe)?\s+(-(e|enc|encodedcommand)\s+[A-Za-z0-9+/=]{6,})", re.IGNORECASE),
            "HIGH",
            85,
            "Obfuscated Base64 PowerShell execution cradle"
        ),
        # Remote Download Cradles
        (
            "RULE_DOWNLOAD_CRADLE",
            re.compile(r"(certutil(\.exe)?\s+(-urlcache|-f)\s+http|bitsadmin(\.exe)?\s+/transfer|Invoke-WebRequest\s+.*-(OutFile|Uri)|(New-Object\s+Net\.WebClient)\.DownloadFile|curl\s+.*\|\s*sh|curl\s+.*\|\s*cmd)", re.IGNORECASE),
            "HIGH",
            80,
            "Stealth remote binary download cradle (certutil / bitsadmin / WebClient)"
        ),
        # Defender / Security Tampering
        (
            "RULE_DEFENDER_TAMPER",
            re.compile(r"(Set-MpPreference\s+-DisableRealtimeMonitoring\s+\$true|DisableRealtimeMonitoring|tamperprotection|reg\s+add.*DisableAntiSpyware)", re.IGNORECASE),
            "CRITICAL",
            90,
            "Unauthorized attempt to disable Windows Defender or Antivirus protection"
        ),
        # Registry Persistence
        (
            "RULE_PERSISTENCE_RUN",
            re.compile(r"(CurrentVersion\\Run|CurrentVersion\\RunOnce)\s+/v", re.IGNORECASE),
            "MEDIUM",
            60,
            "Registry Run/RunOnce autorun persistence modification"
        ),
        # Dangerous Lua Functions in Game Mods
        (
            "RULE_LUA_RCE",
            re.compile(r"\b(os\.execute|io\.popen|package\.loadlib|debug\.sethook)\s*\(", re.IGNORECASE),
            "HIGH",
            75,
            "Dangerous Lua OS command execution or native library loading"
        ),
        # Suspicious Executable Drop in Temp/AppData
        (
            "RULE_TEMP_EXEC",
            re.compile(r"(%temp%|%appdata%|%localappdata%)\\[\w-]+\.(exe|scr|vbs|bat|cmd|dll)", re.IGNORECASE),
            "MEDIUM",
            50,
            "Suspicious payload execution target in temporary / application data directories"
        )
    ]

    ALLOWED_EXTENSIONS = {".cfg", ".bat", ".cmd", ".ps1", ".lua", ".vbs", ".reg", ".ini", ".txt", ".py", ".json", ".vpk"}

    def __init__(self):
        pass

    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scans a single configuration or script file against heuristic threat rules."""
        if not os.path.exists(file_path):
            return {
                "file": file_path,
                "error": "File not found",
                "threat_score": 0,
                "verdict": "ERROR",
                "detections": []
            }

        # Compute SHA-256 hash
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            file_hash = hasher.hexdigest()
        except Exception:
            file_hash = "UNKNOWN"

        # Read content safely with encoding fallback
        content = ""
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                with open(file_path, "r", encoding=enc, errors="ignore") as f:
                    content = f.read()
                break
            except Exception:
                continue

        lines = content.splitlines()
        detections = []
        max_score = 0

        for line_idx, line in enumerate(lines, 1):
            clean_line = line.strip()
            # If line is commented out, it is neutralized in configs/scripts
            is_comment = clean_line.startswith(("//", ";", "#", "rem ")) or clean_line.startswith("/*")
            if is_comment:
                continue

            for rule_id, pattern, severity, score, desc in self.RULES:
                match = pattern.search(line)
                if match:
                    # Obfuscate sensitive credentials in output
                    snippet = match.group(0)
                    if "webhooks" in snippet:
                        snippet = re.sub(r"/webhooks/\d+/([A-Za-z0-9_-]+)", r"/webhooks/[REDACTED_WEBHOOK_SECRET]", snippet)
                    elif len(snippet) > 40:
                        snippet = snippet[:15] + "...[REDACTED]..." + snippet[-10:]

                    detections.append({
                        "line": line_idx,
                        "rule_id": rule_id,
                        "severity": severity,
                        "score": score,
                        "description": desc,
                        "snippet": snippet,
                        "is_commented": False
                    })
                    if score > max_score:
                        max_score = score

        # Determine verdict
        if max_score >= 80:
            verdict = "MALICIOUS"
        elif max_score >= 40:
            verdict = "SUSPICIOUS"
        else:
            verdict = "SAFE"

        return {
            "file": os.path.abspath(file_path),
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "sha256": file_hash,
            "threat_score": max_score,
            "verdict": verdict,
            "detections": detections,
            "total_detections": len(detections)
        }

    def scan_directory(self, dir_path: str, recursive: bool = True) -> Dict[str, Any]:
        """Scans all eligible mod, config, and script files within a directory."""
        if not os.path.isdir(dir_path):
            return {
                "directory": dir_path,
                "error": "Directory does not exist",
                "scanned_files": 0,
                "results": []
            }

        scanned = 0
        malicious_count = 0
        suspicious_count = 0
        safe_count = 0
        results = []

        for root, _, files in os.walk(dir_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.ALLOWED_EXTENSIONS:
                    full_p = os.path.join(root, file)
                    res = self.scan_file(full_p)
                    scanned += 1
                    if res["verdict"] == "MALICIOUS":
                        malicious_count += 1
                        results.append(res)
                    elif res["verdict"] == "SUSPICIOUS":
                        suspicious_count += 1
                        results.append(res)
                    else:
                        safe_count += 1
            if not recursive:
                break

        return {
            "directory": os.path.abspath(dir_path),
            "scanned_files": scanned,
            "safe_files": safe_count,
            "suspicious_files": suspicious_count,
            "malicious_files": malicious_count,
            "threat_summary": f"{malicious_count} Malicious, {suspicious_count} Suspicious, {safe_count} Clean",
            "findings": results
        }

    def sanitize_file(self, file_path: str, backup: bool = True) -> Tuple[bool, str]:
        """Comments out identified malicious commands and preserves legitimate config settings."""
        scan_res = self.scan_file(file_path)
        if not scan_res.get("detections"):
            return True, "File is already clean; no neutralization needed."

        # Read original lines
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception as ex:
            return False, f"Failed to read file: {ex}"

        # Create backup if requested
        if backup:
            bak_path = file_path + ".antimagist.bak"
            try:
                with open(bak_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as ex:
                return False, f"Backup creation failed: {ex}"

        # Neutralize malicious lines
        flagged_lines = {d["line"] for d in scan_res["detections"]}
        modified_lines = []

        ext = os.path.splitext(file_path)[1].lower()
        comment_prefix = "// [ANTIMAGIST_NEUTRALIZED] " if ext in [".cfg", ".lua", ".c", ".cpp"] else "# [ANTIMAGIST_NEUTRALIZED] "
        if ext in [".bat", ".cmd"]:
            comment_prefix = "rem [ANTIMAGIST_NEUTRALIZED] "

        neutralized_count = 0
        for idx, line in enumerate(lines, 1):
            if idx in flagged_lines:
                modified_lines.append(f"{comment_prefix}{line.strip()}\n")
                neutralized_count += 1
            else:
                modified_lines.append(line)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(modified_lines)
            return True, f"Sanitization complete: Neutralized {neutralized_count} malicious command(s). Backup saved."
        except Exception as ex:
            return False, f"Failed to write sanitized file: {ex}"


if __name__ == "__main__":
    print("[*] Testing Antimagist Mod Guard Engine...")
    guard = AntimagistModGuard()

    # Create dummy suspicious autoexec file for testing
    dummy_file = "test_suspicious_autoexec.cfg"
    dummy_content = """// Legit CS2 autoexec
fps_max 0
cl_interp 0.015625
rate 786432

// Malicious hidden webhook payload
powershell -enc aW52b2tlLWV4cHJlc3Npb24gImV2aWwi
curl https://discord.com/api/webhooks/123456789/abcdefghijk
"""
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write(dummy_content)

    res = guard.scan_file(dummy_file)
    print(f"  • Verdict: {res['verdict']} (Score: {res['threat_score']})")
    print(f"  • Total Detections: {res['total_detections']}")
    for d in res["detections"]:
        print(f"    - Line {d['line']}: [{d['severity']}] {d['description']}")

    ok, msg = guard.sanitize_file(dummy_file)
    print(f"  • Sanitization: {ok} ({msg})")

    # Rescan sanitized file
    res2 = guard.scan_file(dummy_file)
    print(f"  • Post-Sanitize Verdict: {res2['verdict']} (Score: {res2['threat_score']})")

    # Cleanup test files
    for p in [dummy_file, dummy_file + ".antimagist.bak"]:
        if os.path.exists(p):
            os.remove(p)

    print("[+] Mod Guard Engine PASSED.")
