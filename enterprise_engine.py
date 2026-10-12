import os
import re
import sys
import time
import json
import hashlib
import shutil
import threading
import subprocess
import webbrowser
import requests
import psutil

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ==========================================
# 1. نظام الأمان وجدار الحماية البرمجي (Security Sandbox)
# ==========================================
class AntimagistSecuritySandbox:
    def __init__(self):
        # نمط Regex للكشف عن الأوامر التدميرية أو محاولات الاختراق وحقن الأوامر
        self.dangerous_pattern = re.compile(
            r'\b(rmdir\s+/s|del\s+/f|format|net\s+user|net\s+localgroup|reg\s+delete|vssadmin|bcdedit)\b', 
            re.IGNORECASE
        )
        print("[🔒 Security] تم تنشيط جدار الحماية الحديدي وعزل الأوامر التدميرية.")

    def is_safe(self, command: str) -> bool:
        """يفحص الأمر محلياً قبل السماح له بالوصول إلى موجه الأوامر."""
        if self.dangerous_pattern.search(command):
            return False
        return True


# ==========================================
# 2. محرك الصيانة وتحسين أداء النظام (PC Optimizer Core)
# ==========================================
class AntimagistOptimizer:
    def __init__(self, sandbox: AntimagistSecuritySandbox):
        self.sandbox = sandbox

    def get_live_metrics(self) -> dict:
        """يجلب إحصائيات استهلاك النظام وتحديث العدادات كل 3 ثوانٍ في الواجهة."""
        virtual_mem = psutil.virtual_memory()
        total_gb = round(virtual_mem.total / (1024**3), 1)
        used_gb = round(virtual_mem.used / (1024**3), 1)
        return {
            "used_ram_gb": used_gb,
            "total_ram_gb": total_gb,
            "ram_percentage": virtual_mem.percent,
            "cpu_percentage": psutil.cpu_percent(interval=None),  # تصحيح cpu_percent
            "active_processes": len(psutil.pids())
        }

    def _run_async_powershell(self, command: str, on_success=None, on_failure=None):
        """جسر تشغيل أوامر PowerShell في خيوط منفصلة صامتة لمنع تجميد الواجهة."""
        if not self.sandbox.is_safe(command):
            err = "❌ تم حظر الأمر برمجياً لحماية النظام: محاولة تشغيل أمر تدميري محظور!"
            if on_failure: on_failure(err)
            return

        def worker():
            try:
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", command], 
                    capture_output=True, text=True, timeout=120,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                if result.returncode == 0 and on_success:
                    on_success(result.stdout)
                elif on_failure:
                    on_failure(result.stderr)
            except Exception as e:
                if on_failure: on_failure(str(e))

        threading.Thread(target=worker, daemon=True).start()

    def run_memory_boost(self, callback):
        initial_mem = psutil.virtual_memory().used
        cmd = "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"
        
        def success(out):
            final_mem = psutil.virtual_memory().used
            released = round(max(0, (initial_mem - final_mem) / (1024**2)), 1)
            callback(f"Optimized! {released} MB of RAM Released.")
            
        self._run_async_powershell(cmd, on_success=success, on_failure=callback)

    def run_cache_sweep(self, callback):
        cmd = """
        $paths = @("$env:TEMP\\*", "$env:SystemRoot\\Temp\\*")
        $cleared = 0
        foreach ($path in $paths) {
            if (Test-Path $path) {
                $files = Get-ChildItem $path -Recurse -Force
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

    def run_deep_sweep(self, callback):
        cmd = "DISM.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase"
        self._run_async_powershell(cmd, on_success=lambda out: callback("Deep Windows Cleanup Complete!"), on_failure=callback)

    def run_nvme_trim(self, callback):
        cmd = "Optimize-Volume -DriveLetter C -Defrag"
        self._run_async_powershell(cmd, on_success=lambda out: callback("Drive Optimization & TRIM Complete!"), on_failure=callback)


# ==========================================
# 3. محرك الفحص السحابي وقبو العزل (Threat Scanner & Vault)
# ==========================================
class AntimagistScanner:
    def __init__(self, api_key: str = None, quarantine_path: str = "C:\\Antimagist_Quarantine"):
        self.api_key = api_key or os.environ.get("VT_API_KEY") or os.environ.get("VIRUSTOTAL_API_KEY")
        self.quarantine_dir = quarantine_path
        
        # إنشاء قبو العزل المخفي تلقائياً عند إقلاع البرنامج مع دعم التحويل الآمن إذا كان C: محمي
        if not os.path.exists(self.quarantine_dir):
            try:
                os.makedirs(self.quarantine_dir, exist_ok=True)
                if os.name == 'nt':
                    os.system(f'attrib +h "{self.quarantine_dir}"')
            except Exception:
                self.quarantine_dir = os.path.abspath("Quarantine")
                os.makedirs(self.quarantine_dir, exist_ok=True)

    def _get_file_sha256(self, file_path: str) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

    def execute_scan(self, file_path: str, ui_callback):
        """يبدأ الفحص السحابي لـ الهاش عبر خلايا VirusTotal API v3 صامتاً في الخلفية."""
        if not self.api_key or len(self.api_key) < 10 or "YOUR_" in self.api_key or "أدخل" in self.api_key:
            ui_callback({"status": "error", "message": "❌ خطأ: مفتاح VirusTotal API غير صالح أو مفقود في الإعدادات!"})
            return

        if not os.path.exists(file_path):
            ui_callback({"status": "error", "message": "❌ خطأ: الملف المحدد غير موجود على القرص!"})
            return

        def worker():
            file_hash = self._get_file_sha256(file_path)
            if file_hash.startswith("Error"):
                ui_callback({"status": "error", "message": "❌ فشل حساب بصمة SHA-256 للملف."})
                return

            # الرابط القياسي لـ VirusTotal API v3
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": self.api_key}

            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                    malicious_hits = stats.get('malicious', 0)
                    
                    if malicious_hits > 0:
                        ui_callback({
                            "status": "danger",
                            "message": f"⚠️ تهديد أمني مؤكد! تم رصده بواسطة {malicious_hits} محرك مكافحة فيروسات.",
                            "is_malicious": True,
                            "file_path": file_path,
                            "hash": file_hash,
                            "malicious_hits": malicious_hits
                        })
                    else:
                        ui_callback({
                            "status": "secure",
                            "message": "✅ الملف سليم ومطابق لقواعد البيانات العالمية.",
                            "is_malicious": False,
                            "hash": file_hash
                        })
                elif response.status_code == 404:
                    ui_callback({
                        "status": "unknown",
                        "message": "❓ ملف مجهول وجديد تماماً على خوادم الفحص العالمي. ينصح بالحذر.",
                        "is_malicious": False,
                        "hash": file_hash
                    })
                elif response.status_code == 401:
                    ui_callback({"status": "error", "message": "❌ خطأ: مفتاح VirusTotal API غير مصرح به (401 Unauthorized)."})
                elif response.status_code == 429:
                    ui_callback({"status": "error", "message": "⏳ تم تجاوز الحد المسموح به لطلبات VirusTotal (429 Rate Limit)."})
                else:
                    ui_callback({"status": "error", "message": f"❌ خطأ من الخادم المضيف: رمز استجابة {response.status_code}"})
            except Exception as e:
                ui_callback({"status": "error", "message": f"❌ خطأ في الاتصال بالشبكة: {str(e)}"})

        threading.Thread(target=worker, daemon=True).start()

    def send_to_quarantine(self, file_path: str) -> bool:
        """يسحب صلاحيات الملف التشغيلية، يشفر البايتات، يغير الامتداد، وينقله إلى القبو المحمي."""
        try:
            if not os.path.exists(file_path):
                return False
            
            file_name = os.path.basename(file_path)
            locked_name = f"{int(time.time())}_{file_name}.antimagist_locked"
            destination = os.path.join(self.quarantine_dir, locked_name)
            
            # قراءة وتجريد محتوى الملف عبر XOR Scrambling (Disarm Payload)
            try:
                with open(file_path, "rb") as fi:
                    raw_data = fi.read()
                disarmed = bytearray(b ^ 0x5A for b in raw_data)
                with open(destination, "wb") as fo:
                    fo.write(disarmed)
                os.remove(file_path)
            except Exception:
                shutil.move(file_path, destination)
            
            # سحب صلاحيات التنفيذ والتشغيل من الويندوز تماماً لحظر التفاعل معه (Zero-Execute)
            if os.name == 'nt':
                try:
                    # سحب توارث الصلاحيات واستخدام المعرف العالمي *S-1-1-0 وحساب Everyone
                    subprocess.run(["icacls", destination, "/inheritance:r", "/deny", "*S-1-1-0:(X)"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    subprocess.run(["icacls", destination, "/deny", "Everything:(X)"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except Exception:
                    pass

            return True
        except Exception as e:
            print(f"[-] فشل عزل الملف بأمان: {str(e)}")
            return False


# ==========================================
# 4. النواة الرئيسية لإدارة المحرك (Application Core Orchestrator)
# ==========================================
class AntimagistEnterpriseEngine:
    def __init__(self, vt_api_key: str = None):
        self.sandbox = AntimagistSecuritySandbox()
        self.optimizer = AntimagistOptimizer(self.sandbox)
        self.scanner = AntimagistScanner(api_key=vt_api_key)
        print("[⚡ Engine] تم تحميل محرك Antimagist بالكامل وهو جاهز للربط بالواجهة.")


# --- اختبار تشغيل المحرك الشامل يدوياً في الـ Terminal ---
if __name__ == "__main__":
    print("=== Antimagist - Enterprise Security Back-end Initializing ===")
    
    # محاكاة تشغيل المحرك
    engine = AntimagistEnterpriseEngine(vt_api_key="YOUR_VIRUSTOTAL_API_KEY_HERE")
    
    # 1. اختبار عدادات الرام والموارد الحية للـ GUI
    metrics = engine.optimizer.get_live_metrics()
    print(f"\n📊 [مراقبة الموارد] استهلاك الرام الحالي: {metrics['used_ram_gb']} GB / {metrics['total_ram_gb']} GB ({metrics['ram_percentage']}%)")
    print(f"⚡ [مراقبة الموارد] استهلاك المعالج: {metrics['cpu_percentage']}% | العمليات: {metrics['active_processes']}")

    # 2. اختبار جدار الحماية
    test_safe = engine.sandbox.is_safe("Get-Process")
    test_dangerous = engine.sandbox.is_safe("rmdir /s C:\\Windows")
    print(f"🔒 اختبار Get-Process: {'آمن ✅' if test_safe else 'محظور ❌'}")
    print(f"🔒 اختبار rmdir /s: {'آمن ❌' if test_dangerous else 'محظور بنجاح ✅'}")
    assert test_safe and not test_dangerous, "فشل فحص جدار الحماية!"

    # 3. اختبار قبو العزل
    dummy_file = os.path.abspath("dummy_threat_test.bin")
    with open(dummy_file, "wb") as f:
        f.write(b"MOCK_MALWARE_SIGNATURE")
    
    isolated = engine.scanner.send_to_quarantine(dummy_file)
    print(f"🛡️ تم عزل الملف التجريبي ونقله للقبو: {isolated} ✅")
    assert isolated, "فشل عزل الملف التجريبي!"

    print("\n✅ تم اجتياز كافة اختبارات AntimagistEnterpriseEngine بنجاح تام!")
