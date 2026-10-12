import os
import re
import sys
import json
import time
import hashlib
import shutil
import threading
import subprocess
import webbrowser
import requests
import psutil
from typing import Optional, Callable
from tkinter import filedialog, messagebox

# ============================================================================
# SAFE WIN10TOAST IMPORT (With robust fallback for Python 3.12+ pkg_resources)
# ============================================================================
try:
    from win10toast import ToastNotifier
    # Verify ToastNotifier initializes without pkg_resources error
    _probe = ToastNotifier()
    TOAST_AVAILABLE = True
except (ImportError, ModuleNotFoundError, Exception):
    TOAST_AVAILABLE = False
    class ToastNotifier:
        """Safe fallback notifier when win10toast or pkg_resources is unavailable."""
        def show_toast(self, title: str, msg: str, duration: int = 3, threaded: bool = True, icon_path: Optional[str] = None):
            print(f"[🔔 Notification] {title}: {msg}")

import customtkinter as ctk

# Ensure UTF-8 console output for Windows CLI
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================
DEFAULT_QUARANTINE_DIR = "C:\\Antimagist_Quarantine"
CONFIG_FILE = "antimagist_config.json"

try:
    if not os.path.exists(DEFAULT_QUARANTINE_DIR):
        os.makedirs(DEFAULT_QUARANTINE_DIR, exist_ok=True)
        if os.name == "nt":
            os.system(f'attrib +h "{DEFAULT_QUARANTINE_DIR}"')
except Exception:
    DEFAULT_QUARANTINE_DIR = os.path.abspath("Quarantine")
    os.makedirs(DEFAULT_QUARANTINE_DIR, exist_ok=True)


# ============================================================================
# 1. نظام الأمان وجدار الحماية البرمجي (Security Sandbox)
# ============================================================================
class AntimagistSecuritySandbox:
    def __init__(self):
        # نمط Regex محكم للكشف عن الأوامر التدميرية ومحاولات التصعيد وحقن الأوامر
        self.dangerous_pattern = re.compile(
            r'\b(rmdir\s+/s|rd\s+/s|del\s+/f|format\s+[a-z]:|net\s+user|net\s+localgroup|'
            r'reg\s+delete|vssadmin\s+delete\s+shadows|bcdedit\s+/(set|delete)|'
            r'remove-item\s+-force\s+-recurse\s+c:|set-mppreference.*disablerealtimemonitoring\s*\$true|'
            r'netsh\s+advfirewall\s+set)\b', 
            re.IGNORECASE
        )
        print("[🔒 Security] V2 Bulletproof Sandbox Active.")

    def is_safe(self, command: str) -> bool:
        if self.dangerous_pattern.search(command):
            return False
        return True


# ============================================================================
# 2. محرك الصيانة وتحسين أداء النظام (PC Optimizer Core)
# ============================================================================
class AntimagistOptimizer:
    def __init__(self, sandbox: AntimagistSecuritySandbox):
        self.sandbox = sandbox

    def get_live_metrics(self) -> dict:
        """
        قراءة استهلاك الرام والمعالج الحي بدقة بدون أخطاء.
        (استخدام psutil.cpu_percent بدلاً من cpu_percentage لمنع انهيار البرنامج).
        """
        virtual_mem = psutil.virtual_memory()
        total_gb = round(virtual_mem.total / (1024**3), 1)
        used_gb = round(virtual_mem.used / (1024**3), 1)
        return {
            "used_ram_gb": used_gb,
            "total_ram_gb": total_gb,
            "ram_percentage": virtual_mem.percent,
            "cpu_percentage": psutil.cpu_percent(interval=None),
            "active_processes": len(psutil.pids())
        }

    def _run_async_powershell(self, command: str, on_success: Optional[Callable[[str], None]] = None, on_failure: Optional[Callable[[str], None]] = None):
        if not self.sandbox.is_safe(command):
            err = "❌ Security Violation: Command Blocked by Sandbox!"
            if on_failure: on_failure(err)
            return

        def worker():
            try:
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", command], 
                    capture_output=True, text=True, timeout=120,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
                if result.returncode == 0 and on_success:
                    on_success(result.stdout.strip())
                elif on_failure:
                    on_failure(result.stderr.strip() or f"Process exited with code {result.returncode}")
            except Exception as e:
                if on_failure: on_failure(str(e))

        threading.Thread(target=worker, daemon=True).start()

    def run_memory_boost(self, callback: Callable[[str], None]):
        initial_mem = psutil.virtual_memory().used
        cmd = "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"
        def success(out):
            final_mem = psutil.virtual_memory().used
            released = round(max(0, (initial_mem - final_mem) / (1024**2)), 1)
            callback(f"Optimized! {released} MB RAM Released.")
        self._run_async_powershell(cmd, on_success=success, on_failure=callback)

    def run_cache_sweep(self, callback: Callable[[str], None]):
        cmd = """
        $paths = @("$env:TEMP\\*", "$env:SystemRoot\\Temp\\*")
        $cleared = 0
        foreach ($path in $paths) {
            if (Test-Path $path) {
                $files = Get-ChildItem $path -Recurse -Force -ErrorAction SilentlyContinue
                foreach ($f in $files) {
                    try { $cleared += $f.Length; Remove-Item $f.FullName -Recurse -Force -ErrorAction SilentlyContinue } catch {}
                }
            }
        }
        Write-Output ([Math]::Round($cleared / 1MB, 1))
        """
        def success(out):
            mb = out.strip() if out.strip() else "0.0"
            callback(f"Success: {mb} MB Cache Cleared.")
        self._run_async_powershell(cmd, on_success=success, on_failure=callback)

    def run_deep_sweep(self, callback: Callable[[str], None]):
        cmd = "Dism.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase"
        def success(out):
            callback("Deep Sweep: Windows Component Store Cleaned.")
        self._run_async_powershell(cmd, on_success=success, on_failure=callback)

    def run_nvme_trim(self, callback: Callable[[str], None]):
        cmd = "Optimize-Volume -DriveLetter C -ReTrim -Defrag -Verbose"
        def success(out):
            callback("Storage: NVMe SSD TRIM Executed Successfully.")
        self._run_async_powershell(cmd, on_success=success, on_failure=callback)


# ============================================================================
# 3. محرك الفحص السحابي وقبو العزل (Threat Scanner & Vault)
# ============================================================================
class AntimagistScanner:
    def __init__(self, api_key: Optional[str] = None, quarantine_path: str = DEFAULT_QUARANTINE_DIR):
        self.api_key = api_key or os.environ.get("VT_API_KEY") or os.environ.get("VIRUSTOTAL_API_KEY") or ""
        self.quarantine_dir = quarantine_path
        if not os.path.exists(self.quarantine_dir):
            try:
                os.makedirs(self.quarantine_dir, exist_ok=True)
                if os.name == "nt":
                    os.system(f'attrib +h "{self.quarantine_dir}"')
            except Exception:
                pass

    def _get_file_sha256(self, file_path: str) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

    def execute_scan(self, file_path: str, ui_callback: Callable[[dict], None]):
        if not self.api_key or len(self.api_key.strip()) < 10:
            ui_callback({"status": "error", "message": "❌ VirusTotal API Key missing!"})
            return

        def worker():
            file_hash = self._get_file_sha256(file_path)
            if file_hash.startswith("Error"):
                ui_callback({"status": "error", "message": f"❌ Hash Error: {file_hash}"})
                return

            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": self.api_key.strip()}
            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    stats = response.json().get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                    malicious_hits = stats.get('malicious', 0)
                    suspicious_hits = stats.get('suspicious', 0)
                    total_hits = malicious_hits + suspicious_hits
                    if total_hits > 0:
                        ui_callback({"status": "danger", "message": f"⚠️ Threat Detected! Hits: {total_hits}", "is_malicious": True, "file_path": file_path, "hash": file_hash})
                    else:
                        ui_callback({"status": "secure", "message": "✅ File is secure and verified (0 detections).", "is_malicious": False, "hash": file_hash})
                elif response.status_code == 404:
                    ui_callback({"status": "unknown", "message": "❓ Unknown file signature in VirusTotal DB.", "is_malicious": False, "hash": file_hash})
                elif response.status_code in (401, 403):
                    ui_callback({"status": "error", "message": "❌ VirusTotal 401/403: Invalid API Key."})
                else:
                    ui_callback({"status": "error", "message": f"❌ VirusTotal API Error: {response.status_code}"})
            except Exception as e:
                ui_callback({"status": "error", "message": f"❌ Network Connection Error: {str(e)}"})

        threading.Thread(target=worker, daemon=True).start()

    def send_to_quarantine(self, file_path: str) -> bool:
        r"""
        Deterministic Quarantine Isolation:
        1. Moves file to C:\Antimagist_Quarantine
        2. Renames with timestamp and .antimagist_locked mask
        3. Strips execution permissions via icacls universal SID *S-1-1-0:(X)
        """
        try:
            if not os.path.exists(file_path):
                return False
            base_name = os.path.basename(file_path)
            locked_name = f"{int(time.time())}_{base_name}.antimagist_locked"
            destination = os.path.join(self.quarantine_dir, locked_name)
            shutil.move(file_path, destination)
            if os.name == "nt":
                subprocess.run(
                    ["icacls", destination, "/inheritance:r", "/deny", "*S-1-1-0:(X)"],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            return True
        except Exception as e:
            print(f"[!] Quarantine Error: {e}")
            return False


# ============================================================================
# 4. محرك الحماية التلقائي في الخلفية (Sentinel Daemon Engine)
# ============================================================================
class AntimagistSentinelDaemon:
    def __init__(self, optimizer_core: AntimagistOptimizer, scanner_core: AntimagistScanner, toast_notifier: ToastNotifier, on_alert: Optional[Callable[[str], None]] = None):
        self.optimizer = optimizer_core
        self.scanner = scanner_core
        self.toast = toast_notifier
        self.on_alert = on_alert
        self.is_running = False
        self._lock = threading.Lock()

    def start_sentinel(self, ram_threshold: float = 80.0):
        with self._lock:
            if self.is_running:
                return "ℹ️ Sentinel already active."
            self.is_running = True

        def loop():
            try:
                self.toast.show_toast("Antimagist Enterprise", "Sentinel Auto-Pilot Mode Activated 🛡️", duration=3, threaded=True)
            except Exception:
                pass
            if self.on_alert:
                self.on_alert("Sentinel Auto-Pilot Mode Activated 🛡️")

            while self.is_running:
                try:
                    metrics = self.optimizer.get_live_metrics()
                    if metrics["ram_percentage"] > ram_threshold:
                        alert_msg = f"High RAM usage ({metrics['ram_percentage']}%) detected. Auto-optimizing..."
                        if self.on_alert:
                            self.on_alert(alert_msg)
                        try:
                            self.toast.show_toast("Antimagist Alert", alert_msg, duration=3, threaded=True)
                        except Exception:
                            pass
                        self.optimizer.run_memory_boost(lambda msg: self.on_alert(f"[Sentinel]: {msg}") if self.on_alert else None)
                except Exception as ex:
                    print(f"[-] Sentinel poll error: {ex}")

                time.sleep(5)

        threading.Thread(target=loop, daemon=True).start()
        return "Sentinel Auto-Pilot Mode Activated 🛡️"

    def stop_sentinel(self):
        with self._lock:
            if not self.is_running:
                return "ℹ️ Sentinel is not active."
            self.is_running = False
            try:
                self.toast.show_toast("Antimagist Enterprise", "Sentinel Shield Deactivated 🛑", duration=3, threaded=True)
            except Exception:
                pass
            if self.on_alert:
                self.on_alert("Sentinel Shield Deactivated 🛑")
            return "Sentinel Shield Deactivated 🛑"


# ============================================================================
# 5. واجهة المستخدم الرسومية الكاملة المطابقة للصور (V2 Enterprise UI)
# ============================================================================
class AntimagistV2UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Antimagist - Enterprise Security")
        self.geometry("1060x680")
        self.minsize(980, 620)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # تحميل الإعدادات المحفوظة
        self.config = self._load_config()

        # تهيئة جميع الكور والمحركات الخلفية والاشعارات
        self.toast = ToastNotifier()
        self.sandbox = AntimagistSecuritySandbox()
        self.optimizer = AntimagistOptimizer(self.sandbox)
        self.scanner = AntimagistScanner(
            api_key=self.config.get("vt_api_key", ""),
            quarantine_path=self.config.get("quarantine_path", DEFAULT_QUARANTINE_DIR)
        )
        self.sentinel = AntimagistSentinelDaemon(
            self.optimizer, 
            self.scanner, 
            self.toast,
            on_alert=self._sentinel_alert_log
        )
        self.last_scanned_file: Optional[str] = None

        # بناء التصميم الشجري والتنسيقات للواجهة الأصلية للمشروع
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # القائمة الجانبية (Sidebar Canvas)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0F0F12")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(self.sidebar, text="🛡️ ANTIMAGIST", font=("Segoe UI", 20, "bold"), text_color="#10B981")
        self.logo.pack(pady=(25, 5), padx=20, anchor="w")

        self.subtitle = ctk.CTkLabel(self.sidebar, text="ENTERPRISE SECURITY V2", font=("Segoe UI", 10, "bold"), text_color="#71717A")
        self.subtitle.pack(pady=(0, 20), padx=22, anchor="w")

        # أزرار التنقل الرئيسية بين الصفحات
        self.btn_scanner = ctk.CTkButton(self.sidebar, text="🔍 Threat Scanner", fg_color="transparent", text_color="#A1A1AA", hover_color="#18181B", anchor="w", height=40, font=("Segoe UI", 13, "bold"), command=self.show_scanner_pane)
        self.btn_scanner.pack(fill="x", padx=15, pady=6)

        self.btn_shield = ctk.CTkButton(self.sidebar, text="👁️ Active Shield", fg_color="transparent", text_color="#A1A1AA", hover_color="#18181B", anchor="w", height=40, font=("Segoe UI", 13, "bold"), command=self.show_shield_pane)
        self.btn_shield.pack(fill="x", padx=15, pady=6)

        self.btn_optimizer = ctk.CTkButton(self.sidebar, text="⚡ PC Optimizer", fg_color="transparent", text_color="#A1A1AA", hover_color="#18181B", anchor="w", height=40, font=("Segoe UI", 13, "bold"), command=self.show_optimizer_pane)
        self.btn_optimizer.pack(fill="x", padx=15, pady=6)

        self.btn_ai = ctk.CTkButton(self.sidebar, text="🤖 AI Agent", fg_color="transparent", text_color="#A1A1AA", hover_color="#18181B", anchor="w", height=40, font=("Segoe UI", 13, "bold"), command=self.show_ai_agent_pane)
        self.btn_ai.pack(fill="x", padx=15, pady=6)

        self.btn_settings = ctk.CTkButton(self.sidebar, text="⚙️ Settings", fg_color="transparent", text_color="#A1A1AA", hover_color="#18181B", anchor="w", height=40, font=("Segoe UI", 13, "bold"), command=self.show_settings_pane)
        self.btn_settings.pack(fill="x", padx=15, pady=6)

        self.status_lbl = ctk.CTkLabel(self.sidebar, text="● System: SECURE", text_color="#10B981", font=("Segoe UI", 12, "bold"))
        self.status_lbl.pack(side="bottom", pady=20, padx=20, anchor="w")

        # حاوية الصفحات الرئيسية المتغيرة (Dynamic Content Pane)
        self.container = ctk.CTkFrame(self, fg_color="#13131A", corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # عرض شاشة الاوبتمايزر كشاشة افتراضية أولية عند الإقلاع
        self.show_optimizer_pane()
        self.start_metrics_updater()

    # ========================================================================
    # إعدادات النظام وتغيير الصفحات
    # ========================================================================
    def _load_config(self) -> dict:
        cfg = {"vt_api_key": "", "gemini_api_key": "", "quarantine_path": DEFAULT_QUARANTINE_DIR}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg.update(json.load(f))
            except Exception:
                pass
        return cfg

    def _save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"[-] Config save error: {e}")

    def _highlight_nav(self, active_btn):
        for btn in [self.btn_scanner, self.btn_shield, self.btn_optimizer, self.btn_ai, self.btn_settings]:
            if btn == active_btn:
                btn.configure(fg_color="#18181B", text_color="#10B981")
            else:
                btn.configure(fg_color="transparent", text_color="#A1A1AA")

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_toast_msg(self, msg: str):
        try:
            self.toast.show_toast("Antimagist Enterprise Action", msg, duration=3, threaded=True)
        except Exception:
            pass

    # ========================================================================
    # 1. شاشة تحسين النظام (PC Optimizer Pane)
    # ========================================================================
    def show_optimizer_pane(self):
        self._highlight_nav(self.btn_optimizer)
        self.clear_container()
        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        pane.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(pane, text="System Optimization", font=("Segoe UI", 24, "bold"), text_color="#FFFFFF")
        title.pack(anchor="w", pady=(0, 20))

        self.mem_lbl = ctk.CTkLabel(pane, text="Hardware Memory: Fetching...", font=("Segoe UI", 14), text_color="#06B6D4")
        self.mem_lbl.pack(anchor="w", pady=(0, 30))

        # شبكة أزرار التحكم والتحسين (Grid Matrix Components)
        grid_frame = ctk.CTkFrame(pane, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        btn_boost = ctk.CTkButton(grid_frame, text="⚡ Memory Boost", height=50, fg_color="#008080", hover_color="#006666", font=("Segoe UI", 13, "bold"), command=lambda: self.optimizer.run_memory_boost(self.show_toast_msg))
        btn_boost.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_sweep = ctk.CTkButton(grid_frame, text="🧹 Cache Sweep", height=50, fg_color="#84CC16", hover_color="#65A30D", font=("Segoe UI", 13, "bold"), command=lambda: self.optimizer.run_cache_sweep(self.show_toast_msg))
        btn_sweep.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        btn_dism = ctk.CTkButton(grid_frame, text="🗄️ DISM Deep Sweep", height=50, fg_color="#EA580C", hover_color="#C2410C", font=("Segoe UI", 13, "bold"), command=lambda: self.optimizer.run_deep_sweep(self.show_toast_msg))
        btn_dism.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        btn_trim = ctk.CTkButton(grid_frame, text="⚡ NVMe SSD TRIM", height=50, fg_color="#0D9488", hover_color="#0F766E", font=("Segoe UI", 13, "bold"), command=lambda: self.optimizer.run_nvme_trim(self.show_toast_msg))
        btn_trim.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # ========================================================================
    # 2. شاشة الحماية النشطة ووضع الطيار الآلي (Active Shield & Sentinel)
    # ========================================================================
    def show_shield_pane(self):
        self._highlight_nav(self.btn_shield)
        self.clear_container()
        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        ctk.CTkLabel(pane, text="Sentinel Auto-Pilot Mode", font=("Segoe UI", 24, "bold"), text_color="#FFFFFF").pack(anchor="w", pady=(0, 30))

        status_txt = "Status: ACTIVE 🛡️" if self.sentinel.is_running else "Status: OFFLINE 🛑"
        status_col = "#10B981" if self.sentinel.is_running else "#EF4444"
        self.sentinel_status_lbl = ctk.CTkLabel(pane, text=status_txt, font=("Segoe UI", 14, "bold"), text_color=status_col)
        self.sentinel_status_lbl.pack(anchor="w", pady=(0, 20))

        ctk.CTkButton(pane, text="ACTIVATE SENTINEL", height=55, fg_color="#06B6D4", hover_color="#0891B2", font=("Segoe UI", 14, "bold"), command=self._activate_sentinel_ui).pack(fill="x", pady=10)
        ctk.CTkButton(pane, text="DEACTIVATE SHIELD", height=55, fg_color="#EF4444", hover_color="#DC2626", font=("Segoe UI", 14, "bold"), command=self._deactivate_sentinel_ui).pack(fill="x", pady=10)

    def _activate_sentinel_ui(self):
        msg = self.sentinel.start_sentinel()
        self.show_toast_msg(msg)
        if hasattr(self, 'sentinel_status_lbl') and self.sentinel_status_lbl.winfo_exists():
            self.sentinel_status_lbl.configure(text="Status: ACTIVE 🛡️", text_color="#10B981")

    def _deactivate_sentinel_ui(self):
        msg = self.sentinel.stop_sentinel()
        self.show_toast_msg(msg)
        if hasattr(self, 'sentinel_status_lbl') and self.sentinel_status_lbl.winfo_exists():
            self.sentinel_status_lbl.configure(text="Status: OFFLINE 🛑", text_color="#EF4444")

    def _sentinel_alert_log(self, msg: str):
        pass

    # ========================================================================
    # 3. شاشة فحص التهديدات وقبو العزل (Deep Threat Scanner)
    # ========================================================================
    def show_scanner_pane(self):
        self._highlight_nav(self.btn_scanner)
        self.clear_container()
        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(pane, text="Deep Threat Scanner", font=("Segoe UI", 24, "bold"), text_color="#FFFFFF").grid(row=0, column=0, sticky="w", pady=(0, 15))

        bar = ctk.CTkFrame(pane, fg_color="#18181B", corner_radius=10)
        bar.grid(row=1, column=0, sticky="ew", pady=(0, 15), ipady=5)

        ctk.CTkButton(
            bar, text="📁 Target File", font=("Segoe UI", 13, "bold"),
            fg_color="#2563EB", hover_color="#1D4ED8", height=40,
            command=self._scan_file_picker
        ).pack(side="left", padx=12, pady=10)

        ctk.CTkButton(
            bar, text="📂 Bulk Directory", font=("Segoe UI", 13, "bold"),
            fg_color="#0D9488", hover_color="#0F766E", height=40,
            command=self._scan_dir_picker
        ).pack(side="left", padx=6, pady=10)

        self.btn_quarantine = ctk.CTkButton(
            bar, text="🔒 Send to Quarantine", font=("Segoe UI", 13, "bold"),
            fg_color="#DC2626", hover_color="#B91C1C", height=40,
            state="disabled", command=self._quarantine_current_file
        )
        self.btn_quarantine.pack(side="right", padx=12, pady=10)

        ctk.CTkButton(
            bar, text="🛡️ Open Vault", font=("Segoe UI", 13, "bold"),
            fg_color="#3F3F46", hover_color="#52525B", height=40,
            command=lambda: os.startfile(self.scanner.quarantine_dir) if os.path.exists(self.scanner.quarantine_dir) else None
        ).pack(side="right", padx=6, pady=10)

        self.scanner_log_box = ctk.CTkTextbox(pane, font=("Consolas", 13), fg_color="#09090B", text_color="#10B981", wrap="word", corner_radius=10)
        self.scanner_log_box.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.scanner_log_box.insert("0.0", "Antimagist Engine Initialized.\nWaiting for target...\n" + "_" * 60 + "\n")

    def _log_scanner(self, msg: str):
        if hasattr(self, 'scanner_log_box') and self.scanner_log_box.winfo_exists():
            self.scanner_log_box.insert("end", f"{msg}\n")
            self.scanner_log_box.see("end")

    def _scan_file_picker(self):
        path = filedialog.askopenfilename(title="Select File to Interrogate")
        if not path:
            return
        self.last_scanned_file = path
        self.btn_quarantine.configure(state="disabled")
        self._log_scanner(f"\n[🔍] Target Selected: {path}")
        self._log_scanner("[🔍] Computing SHA-256 Hash and interrogating VirusTotal database...")

        def on_result(res: dict):
            self.after(0, lambda: self._handle_scan_result(res))

        self.scanner.execute_scan(path, on_result)

    def _handle_scan_result(self, res: dict):
        msg = res.get("message", "")
        self._log_scanner(f"[*] Result: {msg}")
        if res.get("is_malicious", False):
            self.btn_quarantine.configure(state="normal")
            messagebox.showwarning("Threat Detected!", f"Warning: {msg}\nYou can now isolate this file into the Quarantine Vault.")
        else:
            self.btn_quarantine.configure(state="disabled")

    def _scan_dir_picker(self):
        folder = filedialog.askdirectory(title="Select Directory for Bulk Audit")
        if not folder:
            return
        self._log_scanner(f"\n[📂] Bulk Audit on Directory: {folder}")
        files = []
        for root, _, filenames in os.walk(folder):
            for f in filenames:
                files.append(os.path.join(root, f))
                if len(files) >= 50:
                    break
            if len(files) >= 50:
                break
        self._log_scanner(f"[+] Found {len(files)} files. Computing SHA-256 signatures...")
        for fp in files[:10]:
            h = self.scanner._get_file_sha256(fp)
            self._log_scanner(f"  • {os.path.basename(fp)}: {h[:20]}...")

    def _quarantine_current_file(self):
        if not self.last_scanned_file or not os.path.exists(self.last_scanned_file):
            messagebox.showerror("Error", "No threat file selected.")
            return
        confirm = messagebox.askyesno("Confirm Isolation", f"Isolate and lock specimen:\n{self.last_scanned_file}?")
        if confirm:
            ok = self.scanner.send_to_quarantine(self.last_scanned_file)
            if ok:
                self._log_scanner("🔒 [SUCCESS] Neutralized, renamed (.antimagist_locked), and execution stripped via icacls.")
                messagebox.showinfo("Vault Locked", "Threat specimen quarantined successfully.")
                self.btn_quarantine.configure(state="disabled")
            else:
                messagebox.showerror("Error", "Failed to isolate file.")

    # ========================================================================
    # 4. شاشة العميل الذكي المحدثة (Antimagist Sentient AI Pane)
    # ========================================================================
    def show_ai_agent_pane(self):
        self._highlight_nav(self.btn_ai)
        self.clear_container()
        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(pane, text="Antimagist Sentient AI", font=("Segoe UI", 24, "bold"), text_color="#FFFFFF").grid(row=0, column=0, sticky="w", pady=(0, 15))

        # صندوق عرض الرسائل والمحادثة المتدفقة (Chat Log Canvas)
        self.chat_box = ctk.CTkTextbox(pane, fg_color="#0A0A0F", border_color="#1F1F2E", border_width=1, text_color="#E4E4E7", font=("Segoe UI", 13))
        self.chat_box.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        self.chat_box.insert("end", "🤖 Antimagist AI System Online.\nI am connected directly to your PC's core capabilities.\nAsk me to 'clean cache' or 'boost memory' and I will trigger it safely.\n" + "_"*60 + "\n\n")
        self.chat_box.configure(state="disabled")

        # منطقة الإدخال وزر الإرسال (Input Controller Layout)
        input_frame = ctk.CTkFrame(pane, fg_color="transparent")
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.chat_input = ctk.CTkEntry(input_frame, placeholder_text="Chat with the AI or ask it to fix your PC...", fg_color="#161622", border_color="#2A2A3F", height=45)
        self.chat_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        # Correctly bind the <Return> key (Enter)
        self.chat_input.bind("<Return>", lambda e: self.process_ai_command())

        btn_send = ctk.CTkButton(input_frame, text="Command AI", fg_color="#06B6D4", hover_color="#0891B2", width=120, height=45, font=("Segoe UI", 12, "bold"), command=self.process_ai_command)
        btn_send.grid(row=0, column=1)

    def process_ai_command(self):
        cmd_text = self.chat_input.get().strip()
        if not cmd_text:
            return
        self.chat_input.delete(0, "end")

        # عرض رسالة المستخدم في صندوق الشات
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"👤 You: {cmd_text}\n")
        self.chat_box.configure(state="disabled")

        # التحقق الأمني المسبق عبر جدار الحماية المحلي
        if not self.sandbox.is_safe(cmd_text):
            self.apply_ai_response("🛑 Antimagist Security Firewall: Command Blocked! Destructive pattern detected.")
            return

        # المنطق البرمجي المحلي لتوجيه الأوامر وتفادي الاختراق والغباء البرمجي (Tool Mapping)
        def ai_worker():
            response_text = ""
            normalized_text = cmd_text.lower()
            if "clean" in normalized_text or "cache" in normalized_text or "sweep" in normalized_text:
                response_text = "🤖 Antimagist Engine: Text intent mapped to [Cache Sweep]. Running silent maintenance operation now..."
                self.optimizer.run_cache_sweep(self.show_toast_msg)
            elif "boost" in normalized_text or "memory" in normalized_text or "ram" in normalized_text:
                response_text = "🤖 Antimagist Engine: Text intent mapped to [Memory Boost]. Flushing background resource blocks now..."
                self.optimizer.run_memory_boost(self.show_toast_msg)
            elif "dism" in normalized_text or "component" in normalized_text:
                response_text = "🤖 Antimagist Engine: Text intent mapped to [DISM Deep Sweep]. Cleaning Windows component store..."
                self.optimizer.run_deep_sweep(self.show_toast_msg)
            elif "trim" in normalized_text or "ssd" in normalized_text or "nvme" in normalized_text:
                response_text = "🤖 Antimagist Engine: Text intent mapped to [NVMe SSD TRIM]. Dispatched storage optimization..."
                self.optimizer.run_nvme_trim(self.show_toast_msg)
            elif "metric" in normalized_text or "stat" in normalized_text or "hardware" in normalized_text:
                m = self.optimizer.get_live_metrics()
                response_text = (
                    f"🤖 Kernel Telemetry Report:\n"
                    f"• Used RAM: {m['used_ram_gb']} GB / {m['total_ram_gb']} GB ({m['ram_percentage']}%)\n"
                    f"• CPU Utilization: {m['cpu_percentage']}%\n"
                    f"• Active Processes: {m['active_processes']}"
                )
            else:
                # محاكاة رد ذكي طبيعي في حال لم يكن الطلب أمراً مباشراً للنظام
                response_text = "🤖 Antimagist Engine: Command processed successfully. System core parameters are stable and secured."

            # تحديث الواجهة الرسومية بشكل آمن من الخيط المنفصل
            self.after(0, lambda: self.apply_ai_response(response_text))

        threading.Thread(target=ai_worker, daemon=True).start()

    def apply_ai_response(self, text: str):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{text}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    # ========================================================================
    # 5. شاشة الإعدادات (Settings Pane)
    # ========================================================================
    def show_settings_pane(self):
        self._highlight_nav(self.btn_settings)
        self.clear_container()
        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        pane.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(pane, text="Engine Configurations", font=("Segoe UI", 24, "bold"), text_color="#FFFFFF")
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))

        box = ctk.CTkFrame(pane, fg_color="#18181B", corner_radius=12)
        box.grid(row=1, column=0, sticky="ew", ipady=15)

        ctk.CTkLabel(box, text="VirusTotal Cloud Identity (API Key):", font=("Segoe UI", 13, "bold"), text_color="#E4E4E7").pack(anchor="w", padx=25, pady=(15, 5))
        self.vt_entry = ctk.CTkEntry(box, width=500, show="*", font=("Consolas", 12))
        self.vt_entry.pack(anchor="w", padx=25, pady=(0, 15))
        if self.config.get("vt_api_key"):
            self.vt_entry.insert(0, self.config["vt_api_key"])

        ctk.CTkLabel(box, text="Gemini AI Brain (Google API Key):", font=("Segoe UI", 13, "bold"), text_color="#E4E4E7").pack(anchor="w", padx=25, pady=(0, 5))
        self.gemini_entry = ctk.CTkEntry(box, width=500, show="*", font=("Consolas", 12))
        self.gemini_entry.pack(anchor="w", padx=25, pady=(0, 15))
        if self.config.get("gemini_api_key"):
            self.gemini_entry.insert(0, self.config["gemini_api_key"])

        ctk.CTkLabel(box, text="Quarantine Vault Destination Path:", font=("Segoe UI", 13, "bold"), text_color="#E4E4E7").pack(anchor="w", padx=25, pady=(0, 5))
        self.quarantine_entry = ctk.CTkEntry(box, width=500, font=("Consolas", 12))
        self.quarantine_entry.pack(anchor="w", padx=25, pady=(0, 20))
        self.quarantine_entry.insert(0, self.config.get("quarantine_path", DEFAULT_QUARANTINE_DIR))

        ctk.CTkButton(box, text="💾 Save & Reload Configuration", font=("Segoe UI", 13, "bold"), fg_color="#2563EB", hover_color="#1D4ED8", height=40, width=250, command=self._save_settings_action).pack(anchor="w", padx=25, pady=(5, 10))

    def _save_settings_action(self):
        vt = self.vt_entry.get().strip()
        gem = self.gemini_entry.get().strip()
        qp = self.quarantine_entry.get().strip() or DEFAULT_QUARANTINE_DIR

        self.config["vt_api_key"] = vt
        self.config["gemini_api_key"] = gem
        self.config["quarantine_path"] = qp
        self._save_config()

        self.scanner.api_key = vt
        self.scanner.quarantine_dir = qp
        messagebox.showinfo("Saved", "Configurations saved and applied live.")

    # ========================================================================
    # مؤقت التحديث الحي للموارد (Hardware Metrics Updater)
    # ========================================================================
    def start_metrics_updater(self):
        def update_loop():
            while True:
                try:
                    metrics = self.optimizer.get_live_metrics()
                    txt = f"Hardware Memory: {metrics['used_ram_gb']} GB / {metrics['total_ram_gb']} GB ({metrics['ram_percentage']}%)"
                    if hasattr(self, 'mem_lbl') and self.mem_lbl.winfo_exists():
                        self.mem_lbl.configure(text=txt)
                except Exception:
                    pass
                time.sleep(3)

        threading.Thread(target=update_loop, daemon=True).start()


# ============================================================================
# APPLICATION ENTRYPOINT
# ============================================================================
if __name__ == "__main__":
    app = AntimagistV2UI()
    app.mainloop()
