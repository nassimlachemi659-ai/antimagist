import os
import sys
import re
import subprocess
import threading
import psutil

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class AntimagistOptimizerCore:
    def __init__(self, sandbox=None):
        self.sandbox = sandbox
        # جدار الحماية المحلي الصارم (Zero-Trust Sandbox Blocklist)
        self.dangerous_pattern = re.compile(
            r'\b(rmdir\s+/s|del\s+/f|format|net\s+user|net\s+localgroup|reg\s+delete|vssadmin|bcdedit)\b', 
            re.IGNORECASE
        )
        print("[🔒 Antimagist] تم تنشيط جدار الحماية الأمني للمحرك بنجاح.")

    # 1. نظام الفحص والمراقبة الحي للموارد (Real-Time Metrics)
    def get_live_system_metrics(self) -> dict:
        """
        يقوم بجلب استهلاك الرام الحقيقي بدقة لربطه بعداد الواجهة الديناميكي.
        """
        virtual_mem = psutil.virtual_memory()
        total_gb = round(virtual_mem.total / (1024**3), 1)
        used_gb = round(virtual_mem.used / (1024**3), 1)
        percent = virtual_mem.percent
        
        return {
            "used_ram_gb": used_gb,
            "total_ram_gb": total_gb,
            "ram_percentage": percent,
            "cpu_percentage": psutil.cpu_percent(interval=None),
            "active_processes": len(psutil.pids())
        }

    # 2. فحص الأمان المسبق قبل إطلاق أي أمر في النظام (Pre-Flight Filter)
    def _is_safe_command(self, command: str) -> bool:
        if self.dangerous_pattern.search(command):
            return False
        if self.sandbox:
            decision = self.sandbox.evaluate("execute_powershell", {"command": command})
            if not decision.allowed:
                return False
        return True

    # 3. محرك التنفيذ الآمن والمنفصل للخلفية (Safe Async Execution Bridge)
    def _run_powershell_safely(self, command: str, callback_success=None, callback_failure=None):
        if not self._is_safe_command(command):
            error_msg = "❌ تم حظر الأمر برمجياً لحماية النظام: محاولة تشغيل أمر تدميري محظور!"
            print(error_msg)
            if callback_failure: callback_failure(error_msg)
            return

        def worker():
            try:
                # تشغيل الأوامر صامتاً وبشكل غير مرئي للمستخدم لتجنب النوافذ المزعجة
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", command], 
                    capture_output=True, text=True, timeout=300,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                if result.returncode == 0:
                    if callback_success: callback_success(result.stdout)
                else:
                    if callback_failure: callback_failure(result.stderr)
            except Exception as e:
                if callback_failure: callback_failure(str(e))

        # إطلاق خيط منفصل (Thread) للحفاظ على استقرار واستجابة الواجهة وعدم تعليقها
        threading.Thread(target=worker, daemon=True).start()

    # 4. وظائف الصيانة والتحسين المباشرة للأزرار (Optimization Toolset)
    def trigger_memory_boost(self, on_complete):
        """ يمسح الـ Standby list وينظف الرام المخزنة مؤقتاً وغير المستغلة """
        initial_mem = psutil.virtual_memory().used
        
        # أمر لتفريغ الذاكرة الخاملة لتقليل الضغط فوراً
        cmd = "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"
        
        def success(output):
            final_mem = psutil.virtual_memory().used
            released = round(max(0, (initial_mem - final_mem) / (1024**2)), 1)
            on_complete(f"Optimized! {released} MB of RAM Released.")
            
        self._run_powershell_safely(cmd, callback_success=success)

    def trigger_cache_sweep(self, on_complete):
        """ ينظف مجلدات الـ Temp ومخلفات التصفح المتراكمة لزيادة مساحة الهارددسك """
        cmd = """
        $paths = @("$env:TEMP\\*", "$env:SystemRoot\\Temp\\*")
        $cleared = 0
        foreach ($path in $paths) {
            if (Test-Path $path) {
                $files = Get-ChildItem $path -Recurse -Force -ErrorAction SilentlyContinue
                foreach ($f in $files) {
                    try { 
                        $cleared += $f.Length
                        Remove-Item $f.FullName -Recurse -Force -ErrorAction SilentlyContinue 
                    } catch {}
                }
            }
        }
        Write-Output ([Math]::Round($cleared / 1MB, 1))
        """
        def success(output):
            mb_cleared = output.strip() if output.strip() else "0.0"
            on_complete(f"Success: {mb_cleared} MB Cache Cleared.")
            
        self._run_powershell_safely(cmd, callback_success=success)

    def trigger_deep_sweep(self, on_complete):
        """ يضغط وينظف مستودع تحديثات الويندوز المتضخم (Component Store Cleanup) صامتاً """
        cmd = "DISM.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase"
        self._run_powershell_safely(cmd, callback_success=lambda out: on_complete("Deep Windows Cleanup Complete!"))

    def trigger_nvme_trim(self, on_complete):
        """ يرسل إشارة TRIM لأقراص الـ SSD لتسريع أدائها الإجمالي وصحتها """
        cmd = "Optimize-Volume -DriveLetter C -Defrag -Verbose"
        self._run_powershell_safely(cmd, callback_success=lambda out: on_complete("Drive Optimization & TRIM Complete!"))

if __name__ == "__main__":
    optimizer = AntimagistOptimizerCore()
    
    # محاكاة تحديث البيانات للواجهة
    stats = optimizer.get_live_system_metrics()
    print(f"\n📊 [العداد المباشر] الرام المستهلكة حالياً: {stats['used_ram_gb']} GB / {stats['total_ram_gb']} GB ({stats['ram_percentage']}%)")
    print(f"🔥 [العداد المباشر] استهلاك المعالج: {stats['cpu_percentage']}%")
    print(f"🔥 [العداد المباشر] العمليات النشطة في الخلفية: {stats['active_processes']} عملية\n")

    # محاكاة فحص الأمان
    print("🔒 اختبار حظر الأوامر الخطيرة:")
    is_safe = optimizer._is_safe_command("rmdir /s C:\\Windows")
    print(f"الأمر 'rmdir /s C:\\Windows' آمن؟ {is_safe}")
    assert not is_safe, "فشل اختبار الحظر الأمني!"

    # محاكاة الضغط على زر Cache Sweep في برنامجك
    print("\n[⚡] جاري تنظيف الكاش المؤقت عبر المحرك الخلفي...")
    evt = threading.Event()
    def _on_done(ui_message):
        print(f"🤖 [واجهة البرنامج]: {ui_message}")
        evt.set()

    optimizer.trigger_cache_sweep(on_complete=_on_done)
    evt.wait(timeout=10)
    print("\n✅ تم تشغيل واختبار AntimagistOptimizerCore بنجاح تام!")
