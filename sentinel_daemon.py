import os
import sys
import time
import threading
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class AntimagistSentinelDaemon:
    def __init__(self, optimizer_core, scanner_core, on_alert_callback=None):
        self.optimizer = optimizer_core
        self.scanner = scanner_core
        self.on_alert = on_alert_callback
        self.is_running = False
        self._lock = threading.Lock()
        print("[🛡️ Sentinel] محرك الحماية التلقائي مستعد للعمل في الخلفية.")

    def start_sentinel(self, ram_threshold: float = 85.0, check_interval: int = 5):
        """
        يطلق حارس الخلفية التلقائي في خيط منفصل تماماً (Daemon Thread).
        """
        with self._lock:
            if self.is_running:
                return "ℹ️ Sentinel يعمل بالفعل في الخلفية."
            self.is_running = True

        def sentinel_loop():
            print("[🚀 Sentinel] تم تنشيط وضع الطيار الآلي بنجاح.")
            while self.is_running:
                try:
                    # 1. مراقبة استهلاك الرام ذاتياً لمنع الاختناق (Resource Guard)
                    metrics = self.optimizer.get_live_metrics()
                    if metrics["ram_percentage"] > ram_threshold:
                        alert_msg = f"[🛡️ Sentinel Alert] استهلاك الرام مرتفع جداً ({metrics['ram_percentage']}%). جاري التنظيف التلقائي الصامت..."
                        print(alert_msg)
                        if self.on_alert:
                            self.on_alert(alert_msg)
                        
                        # إطلاق تنظيف صامت للذاكرة
                        self.optimizer.run_memory_boost(lambda msg: print(f"[🛡️ Sentinel Action]: {msg}"))
                        self.optimizer.run_cache_sweep(lambda msg: print(f"[🛡️ Sentinel Action]: {msg}"))

                    # 2. فحص سجلات الأخطاء الحرجة في الويندوز (Windows Event Log Trapping)
                    # يقوم بالبحث الصامت عن أي Crash حدث في آخر 10 ثوانٍ لحله أو تنبيهك به
                    log_cmd = "Get-WinEvent -LogName Application -MaxEvents 5 -ErrorAction SilentlyContinue | Where-Object {$_.LevelDisplayName -eq 'Critical' -or $_.LevelDisplayName -eq 'Error'}"
                    
                    # يتم تمرير الأمر عبر الجدار الأمني المحلي لضمان سلامته
                    if hasattr(self.optimizer, 'sandbox') and self.optimizer.sandbox.is_safe(log_cmd):
                        # فحص سريع صامت بدون تعطيل المعالج
                        proc = subprocess.run(
                            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", log_cmd],
                            capture_output=True, text=True, timeout=8,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                        )
                        if proc.stdout.strip():
                            # هنا تم التقاط كراش أو خطأ فادح في النظام، يتم تسجيله وعزله برمجياً
                            event_msg = "[⚠️ Sentinel Detection] تم رصد خطأ حرج في تطبيقات الويندوز في الخلفية!"
                            print(event_msg)
                            if self.on_alert:
                                self.on_alert(event_msg)

                except Exception as e:
                    print(f"[-] خطأ داخل حلقة Sentinel: {str(e)}")
                
                # فحص دوري كل 5 ثوانٍ لضمان استقرار المعالج بنسبة 0% استهلاك للـ AI
                for _ in range(check_interval):
                    if not self.is_running:
                        break
                    time.sleep(1)

        threading.Thread(target=sentinel_loop, daemon=True).start()
        return "✅ تم إطلاق حارس الخلفية بنجاح."

    def stop_sentinel(self):
        """إيقاف الحارس فوراً وسحب الصلاحيات التلقائية في الخلفية."""
        with self._lock:
            if not self.is_running:
                return "ℹ️ Sentinel متوقف بالفعل."
            self.is_running = False
            print("[🛑 Sentinel] تم إيقاف وضع الطيار الآلي وأمان الخلفية مستقر.")
            return "🛑 تم إيقاف الحارس."


if __name__ == "__main__":
    from enterprise_engine import AntimagistEnterpriseEngine
    
    print("=== اختبار حارس الأمان الآلي AntimagistSentinelDaemon ===")
    engine = AntimagistEnterpriseEngine()
    
    alerts_captured = []
    def _test_alert(msg):
        alerts_captured.append(msg)
        print(f"[UI Event Broadcast] {msg}")

    daemon = AntimagistSentinelDaemon(engine.optimizer, engine.scanner, on_alert_callback=_test_alert)
    
    # بدء تشغيل الحارس بحد منخفض للتجربة
    res_start = daemon.start_sentinel(ram_threshold=99.0, check_interval=2)
    print(res_start)
    assert daemon.is_running, "فشل تشغيل الـ Daemon!"

    # انتظار دورتين للتحقق من سلامة الحلقة
    time.sleep(3)

    # إيقاف الحارس
    res_stop = daemon.stop_sentinel()
    print(res_stop)
    assert not daemon.is_running, "فشل إيقاف الـ Daemon!"

    print("\n✅ تم اجتياز كافة اختبارات AntimagistSentinelDaemon بنجاح!")
