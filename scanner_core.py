import os
import sys
import hashlib
import shutil
import requests
import threading

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class AntimagistScannerCore:
    def __init__(self, api_key: str = None, quarantine_dir: str = None):
        # جلب المفتاح تلقائياً من الإعدادات أو البيئة المحلية (دعم VIRUSTOTAL_API_KEY و VT_API_KEY)
        self.api_key = api_key or os.environ.get("VIRUSTOTAL_API_KEY") or os.environ.get("VT_API_KEY")
        
        # قبو العزل: إذا تعذر الوصول للجذر، استخدم المجلد المحلي الآمن
        if not quarantine_dir:
            default_root = "C:\\Antimagist_Quarantine"
            try:
                if not os.path.exists(default_root):
                    os.makedirs(default_root)
                self.quarantine_dir = default_root
            except Exception:
                self.quarantine_dir = os.path.abspath("Quarantine")
        else:
            self.quarantine_dir = quarantine_dir
        
        # إنشاء قبو العزل فوراً إذا لم يكن موجوداً
        if not os.path.exists(self.quarantine_dir):
            try:
                os.makedirs(self.quarantine_dir, exist_ok=True)
                # إخفاء المجلد في الويندوز كإجراء حماية إضافي
                if os.name == 'nt':
                    os.system(f'attrib +h "{self.quarantine_dir}"')
            except Exception as e:
                print(f"[-] فشل إنشاء قبو العزل: {str(e)}")

    # 1. حساب الـ SHA-256 للملف قبل الفحص (لحفظ استهلاك الـ API والسرعة)
    def calculate_sha256(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

    # 2. فحص الملف عبر قاعدة بيانات VirusTotal v3 (Hash Check)
    def scan_file(self, file_path: str, on_complete):
        """
        يقوم بفحص الملف دون تجميد الواجهة الرسومية (Asynchronous).
        """
        if not self.api_key or "أدخل" in self.api_key or "YOUR_" in self.api_key:
            on_complete({"status": "error", "message": "❌ لم يتم إدخال مفتاح VirusTotal API في الإعدادات!"})
            return

        if not os.path.exists(file_path):
            on_complete({"status": "error", "message": "❌ الملف المحدد غير موجود!"})
            return

        def worker():
            file_hash = self.calculate_sha256(file_path)
            if file_hash.startswith("Error"):
                on_complete({"status": "error", "message": f"❌ تعذر قراءة وحساب هاش الملف: {file_hash}"})
                return

            # الرابط القياسي المعتمد لـ VirusTotal API v3
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": self.api_key}

            try:
                response = requests.get(url, headers=headers, timeout=15)
                
                # حالة 1: الملف معروف مسبقاً في قاعدة البيانات
                if response.status_code == 200:
                    data = response.json()
                    stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                    malicious_count = stats.get('malicious', 0)
                    suspicious_count = stats.get('suspicious', 0)
                    
                    if malicious_count > 0:
                        on_complete({
                            "status": "danger", 
                            "message": f"⚠️ تهديد مؤكد! تم رصده بواسطة {malicious_count} محرك فيروسات.",
                            "hash": file_hash,
                            "malicious_count": malicious_count,
                            "is_malicious": True
                        })
                    elif suspicious_count > 0:
                        on_complete({
                            "status": "warning", 
                            "message": f"⚠️ ملف مشبوه! صُنّف كمريب بواسطة {suspicious_count} محركات.",
                            "hash": file_hash,
                            "is_malicious": False
                        })
                    else:
                        on_complete({
                            "status": "secure", 
                            "message": "✅ الملف سليم تماماً ولم يتم العثور على تهديدات في VirusTotal.",
                            "hash": file_hash,
                            "is_malicious": False
                        })
                
                # حالة 2: الملف جديد تماماً ولم يفحص من قبل عالمياً
                elif response.status_code == 404:
                    on_complete({
                        "status": "unknown", 
                        "message": "❓ ملف مجهول الهوية (غير مدرج في VirusTotal)، ينصح بالحذر.",
                        "hash": file_hash,
                        "is_malicious": False
                    })
                elif response.status_code == 401:
                    on_complete({"status": "error", "message": "❌ مفتاح VirusTotal API غير صالح (401 Unauthorized)."})
                elif response.status_code == 429:
                    on_complete({"status": "error", "message": "⏳ تم تجاوز حد طلبات الـ API المسموح بها في VirusTotal (429 Rate Limit)."})
                else:
                    on_complete({"status": "error", "message": f"❌ خطأ في الاتصال بالخادم: رمز {response.status_code}"})

            except Exception as e:
                on_complete({"status": "error", "message": f"❌ تعذر الاتصال بالشبكة: {str(e)}"})

        threading.Thread(target=worker, daemon=True).start()

    # 3. محرك العزل التام للملف المصاب (Quarantine Engine)
    def quarantine_file(self, file_path: str, threat_name: str = "Detected Malware") -> bool:
        """
        ينقل الملف المصاب صامتاً إلى القبو، يعطله عبر تشفير XOR وتغيير امتداده وسحب صلاحيات التشغيل.
        """
        try:
            if not os.path.exists(file_path):
                return False
                
            file_name = os.path.basename(file_path)
            quarantine_path = os.path.join(self.quarantine_dir, f"{file_name}.antimagist_locked")
            
            # قراءة وتجريد الملف من قدرته التنفيذية (Disarm via XOR payload scrambling)
            try:
                with open(file_path, "rb") as f_in:
                    raw_bytes = f_in.read()
                disarmed = bytearray(b ^ 0x5A for b in raw_bytes)
                with open(quarantine_path, "wb") as f_out:
                    f_out.write(disarmed)
                os.remove(file_path)
            except Exception:
                # محاولة النقل العادي إذا فشل التشفير
                shutil.move(file_path, quarantine_path)

            # سحب صلاحيات التنفيذ تماماً من الملف المعزول باستخدام المعرف العالمي *S-1-1-0 (Everyone)
            if os.name == 'nt':
                try:
                    subprocess.run(
                        f'icacls "{quarantine_path}" /deny *S-1-1-0:(X)',
                        shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW
                    )
                except Exception:
                    pass

            return True
        except Exception as e:
            print(f"[-] خطأ أثناء عزل الملف: {str(e)}")
            return False

# --- اختبار تشغيل تجريبي ---
if __name__ == "__main__":
    scanner = AntimagistScannerCore()
    print(f"[✅] تم تهيئة AntimagistScannerCore بنجاح.")
    print(f"[📂] قبو العزل النشط: {scanner.quarantine_dir}")
    
    # اختبار حساب الهاش لملف بايثون الحالي
    this_file = os.path.abspath(__file__)
    h = scanner.calculate_sha256(this_file)
    print(f"[🔒] SHA-256 للملف الحالي: {h}")
    assert len(h) == 64, "فشل حساب الهاش!"
    
    # اختبار عزل تجريبي آمن لملف اختبار
    dummy_test = os.path.abspath("dummy_malware_test.tmp")
    with open(dummy_test, "w") as f:
        f.write("DUMMY_EICAR_TEST_PAYLOAD")
    ok = scanner.quarantine_file(dummy_test, "Test Threat")
    print(f"[🔒] تم عزل الملف التجريبي بنجاح؟ {ok}")
    assert ok, "فشل العزل التجريبي!"
    
    # تنظيف الملف المعزول التجريبي
    locked_path = os.path.join(scanner.quarantine_dir, "dummy_malware_test.tmp.antimagist_locked")
    if os.path.exists(locked_path):
        try: os.remove(locked_path)
        except Exception: pass
        
    print("[✅] اكتملت جميع اختبارات وحدة AntimagistScannerCore بنجاح تام!")
