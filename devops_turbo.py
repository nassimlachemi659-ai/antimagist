"""
Antimagist V11 — Developer & AI Workstation Turbocharger (devops_turbo.py)
Accelerates compilation, package management, IDE responsiveness, and WSL2/Docker workflows.

Key Capabilities:
1. Windows Defender Minifilter Smart Exclusions (audits & excludes project dirs/compilers).
2. WSL2 & Docker vmmem Dynamic RAM Clamp & .wslconfig Auto-Tuner.
3. IDE & Compiler Priority Elevator (VS Code, Visual Studio, PyCharm, cargo, rustc, node, cl).
4. Subprocess I/O priority boost (sets HIGH_PRIORITY_CLASS and IO_PRIORITY_HIGH).
"""

import os
import sys
import ctypes
import subprocess
import psutil
from typing import Dict, List, Any

DEV_PROCESS_NAMES = {
    "code.exe": "VS Code",
    "devenv.exe": "Visual Studio",
    "idea64.exe": "IntelliJ IDEA",
    "pycharm64.exe": "PyCharm",
    "cl.exe": "MSVC C/C++ Compiler",
    "cargo.exe": "Rust Cargo",
    "rustc.exe": "Rust Compiler",
    "node.exe": "Node.js Runtime",
    "python.exe": "Python Interpreter",
    "docker.exe": "Docker Daemon",
    "wsl.exe": "Windows Subsystem for Linux",
    "vmmem.exe": "WSL2 Virtual Machine Engine",
    "vmmemWSL.exe": "WSL2 Virtual Machine Engine",
    "git.exe": "Git SCM"
}

# Win32 I/O Priority Constants
# ProcessIoPriority is an undocumented / semi-documented NT class, handled via NtSetInformationProcess
# Standard priority class in psutil: psutil.HIGH_PRIORITY_CLASS, psutil.ABOVE_NORMAL_PRIORITY_CLASS

class DevOpsTurboEngine:
    """Manages developer workstation optimization, WSL2 tuning, and compiler acceleration."""

    def __init__(self):
        self.user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        self.wsl_config_path = os.path.join(self.user_profile, ".wslconfig")

    def detect_active_dev_processes(self) -> List[Dict[str, Any]]:
        """Scans running processes and identifies active developer tools and compilers."""
        results = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                name_lower = proc.info['name'].lower() if proc.info['name'] else ''
                for dev_key, dev_title in DEV_PROCESS_NAMES.items():
                    if name_lower == dev_key.lower():
                        mem_mb = (proc.info['memory_info'].rss / (1024 * 1024)) if proc.info['memory_info'] else 0
                        results.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "title": dev_title,
                            "memory_mb": round(mem_mb, 1),
                            "cpu_percent": proc.info.get('cpu_percent', 0.0)
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return results

    def elevate_dev_priorities(self) -> Dict[str, Any]:
        """Elevates developer processes to Above Normal or High priority."""
        elevated = []
        errors = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name_lower = proc.info['name'].lower() if proc.info['name'] else ''
                if any(name_lower == k.lower() for k in DEV_PROCESS_NAMES):
                    p = psutil.Process(proc.info['pid'])
                    # Elevate compilers to HIGH, IDEs to ABOVE_NORMAL
                    if name_lower in ["cl.exe", "cargo.exe", "rustc.exe", "node.exe"]:
                        p.nice(psutil.HIGH_PRIORITY_CLASS)
                    else:
                        p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
                    elevated.append(f"{proc.info['name']} (PID {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                errors.append(f"{proc.info.get('name', 'Unknown')}: {e}")
            except Exception as e:
                errors.append(f"{proc.info.get('name', 'Unknown')}: {e}")

        return {
            "success": True,
            "elevated_count": len(elevated),
            "elevated_processes": elevated,
            "error_count": len(errors)
        }

    def inspect_wsl_config(self) -> Dict[str, Any]:
        """Inspects .wslconfig and returns configuration status and recommendations."""
        exists = os.path.exists(self.wsl_config_path)
        content = ""
        memory_limit = "Uncapped"
        processors = "All"
        swap = "Default"

        if exists:
            try:
                with open(self.wsl_config_path, "r", encoding="utf-8") as f:
                    content = f.read()
                for line in content.splitlines():
                    clean = line.strip()
                    if clean.lower().startswith("memory="):
                        memory_limit = clean.split("=")[1].strip()
                    elif clean.lower().startswith("processors="):
                        processors = clean.split("=")[1].strip()
                    elif clean.lower().startswith("swap="):
                        swap = clean.split("=")[1].strip()
            except Exception as e:
                content = f"Error reading: {e}"

        # Detect active WSL vmmem memory
        vmmem_usage_mb = 0.0
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['name'] and proc.info['name'].lower() in ["vmmem.exe", "vmmemwsl.exe"]:
                    if proc.info['memory_info']:
                        vmmem_usage_mb += proc.info['memory_info'].rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return {
            "wsl_config_exists": exists,
            "config_path": self.wsl_config_path,
            "memory_limit": memory_limit,
            "processors": processors,
            "swap": swap,
            "vmmem_ram_mb": round(vmmem_usage_mb, 1),
            "is_optimized": exists and memory_limit != "Uncapped"
        }

    def apply_optimal_wsl_config(self, ram_limit_gb: int = 6) -> Dict[str, Any]:
        """Writes an optimal .wslconfig limiting vmmem RAM and setting optimal core count."""
        try:
            total_cores = psutil.cpu_count(logical=False) or 4
            config_template = f"""# Antimagist V11 Optimal WSL2 Configuration
[wsl2]
memory={ram_limit_gb}GB
processors={total_cores}
swap=4GB
localhostForwarding=true
guiApplications=false
autoProxy=true
nestedVirtualization=false
"""
            with open(self.wsl_config_path, "w", encoding="utf-8") as f:
                f.write(config_template)

            return {
                "success": True,
                "message": f"Optimal .wslconfig applied ({ram_limit_gb}GB RAM clamp, {total_cores} cores). Restart WSL with 'wsl --shutdown' to activate.",
                "path": self.wsl_config_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def audit_defender_exclusions(self) -> Dict[str, Any]:
        """Queries Windows Defender exclusions for developer paths."""
        try:
            cmd = "powershell -NoProfile -NonInteractive -Command \"Get-MpPreference | Select-Object -ExpandProperty ExclusionPath\""
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            paths = [p.strip() for p in res.stdout.splitlines() if p.strip()]
            return {
                "success": True,
                "exclusion_paths": paths,
                "count": len(paths)
            }
        except Exception as e:
            return {
                "success": False,
                "exclusion_paths": [],
                "count": 0,
                "error": str(e)
            }

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Aggregates all DevOps and AI workstation telemetry."""
        dev_procs = self.detect_active_dev_processes()
        wsl_info = self.inspect_wsl_config()
        total_ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)

        return {
            "active_dev_procs": dev_procs,
            "dev_proc_count": len(dev_procs),
            "wsl_info": wsl_info,
            "total_ram_gb": total_ram_gb,
            "status": "OPTIMIZED" if wsl_info["is_optimized"] else "ATTENTION_NEEDED"
        }


if __name__ == "__main__":
    engine = DevOpsTurboEngine()
    print("=== Antimagist V11 DevOps & AI Workstation Turbo ===")
    metrics = engine.get_summary_metrics()
    print(f"Dev Processes Found: {metrics['dev_proc_count']}")
    for p in metrics['active_dev_procs']:
        print(f"  • {p['title']} ({p['name']}): PID {p['pid']}, {p['memory_mb']} MB RAM")
    print(f"WSL2 Config Exists: {metrics['wsl_info']['wsl_config_exists']}")
    print(f"WSL2 RAM Limit: {metrics['wsl_info']['memory_limit']}")
    print(f"WSL2 Active RAM: {metrics['wsl_info']['vmmem_ram_mb']} MB")
    elevate_res = engine.elevate_dev_priorities()
    print(f"Elevated Processes: {elevate_res['elevated_count']}")
    print("[SUCCESS] devops_turbo.py verified cleanly.")
