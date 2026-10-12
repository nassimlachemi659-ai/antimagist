"""
network_monitor.py — Real-Time Network & Port Sniffer / Connection Firewall
=============================================================================
Antimagist Enterprise Security V3 Component
- Maps all live TCP/UDP sockets with process attribution
- Detects untrusted connections and non-standard remote ports
- Provides safe process termination for suspicious communication
"""

import os
import psutil
from typing import List, Dict, Any, Optional, Tuple

SUSPICIOUS_PORTS = {
    4444: "Metasploit Default Listener",
    1337: "Common Hacker/Backdoor Port",
    6667: "IRC Botnet C2 Channel",
    8888: "Suspicious HTTP Proxy / Reverse Shell",
    31337: "Back Orifice Trojan Classic",
    5555: "Android ADB Remote Exploit",
    9001: "Tor / Custom C2 Tunnel",
    7777: "Unusual Inbound / RAT Listener",
}

class AntimagistNetworkMonitor:
    def __init__(self):
        pass

    def get_active_connections(self, filter_status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves all active TCP/UDP sockets mapped to process names.
        """
        connections = []
        try:
            raw_conns = psutil.net_connections(kind='inet')
        except Exception as ex:
            print(f"[-] net_connections error: {ex}")
            return []

        for c in raw_conns:
            if filter_status and c.status != filter_status:
                continue

            laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "LISTENING"
            r_port = c.raddr.port if c.raddr else 0

            pname = "System / Kernel"
            p_path = ""
            if c.pid and c.pid > 0:
                try:
                    p = psutil.Process(c.pid)
                    pname = p.name()
                    try:
                        p_path = p.exe()
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        p_path = ""
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pname = "Terminated Process"

            is_suspicious = False
            flag_reason = ""
            if r_port in SUSPICIOUS_PORTS:
                is_suspicious = True
                flag_reason = f"⚠️ Alert: Known C2 Port ({SUSPICIOUS_PORTS[r_port]})"
            elif c.status == "ESTABLISHED" and pname.lower() in ["powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe"]:
                is_suspicious = True
                flag_reason = "⚠️ Alert: Shell process communicating over network"

            connections.append({
                "pid": c.pid or 0,
                "process_name": pname,
                "process_path": p_path,
                "local_address": laddr,
                "remote_address": raddr,
                "remote_port": r_port,
                "status": c.status,
                "protocol": "TCP" if c.type == 1 else "UDP",
                "is_suspicious": is_suspicious,
                "flag_reason": flag_reason
            })

        # Sort: suspicious first, then established, then listening
        connections.sort(key=lambda x: (not x["is_suspicious"], x["status"] != "ESTABLISHED"))
        return connections

    def get_summary_metrics(self) -> Dict[str, int]:
        conns = self.get_active_connections()
        established = sum(1 for c in conns if c["status"] == "ESTABLISHED")
        listening = sum(1 for c in conns if c["status"] == "LISTEN" or c["remote_address"] == "LISTENING")
        suspicious = sum(1 for c in conns if c["is_suspicious"])
        return {
            "total_sockets": len(conns),
            "established": established,
            "listening": listening,
            "suspicious": suspicious
        }

    def terminate_process_by_pid(self, pid: int) -> Tuple[bool, str]:
        """Safely terminates a process associated with a network socket."""
        if pid <= 4:
            return False, "Cannot terminate Windows System core processes."
        try:
            p = psutil.Process(pid)
            name = p.name()
            p.terminate()
            p.wait(timeout=3)
            return True, f"Successfully terminated {name} (PID: {pid})."
        except (psutil.NoSuchProcess, psutil.AccessDenied) as ex:
            return False, f"Permission Denied or Process already stopped: {ex}"
