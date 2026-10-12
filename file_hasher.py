import hashlib
import os

def calculate_file_hashes(file_path):
    """
    تحسب هذه الدالة بصمات SHA-256 و MD5 لأي ملف لتحديد هويته الرقمية.
    """
    sha256_hash = hashlib.sha256()
    md5_hash = hashlib.md5()
    
    try:
        # قراءة الملف على أجزاء صغيرة (Blocks) لتجنب استهلاك الذاكرة مع الملفات الكبيرة
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
                md5_hash.update(byte_block)
                
        return {
            "sha256": sha256_hash.hexdigest(),
            "md5": md5_hash.hexdigest(),
            "status": "Success"
        }
    except FileNotFoundError:
        return {"status": "Error", "message": "الملف غير موجود."}
    except PermissionError:
        return {"status": "Error", "message": "صلاحيات غير كافية لقراءة الملف."}

# اختبار الدالة (يمكنك استبدال المسار بملف حقيقي على جهازك للتجربة)
if __name__ == "__main__":
    test_file = "test.txt"
    
    # إنشاء ملف نصي مؤقت للتجربة إذا لم يكن موجوداً
    if not os.path.exists(test_file):
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("This is a safe test file for our AI Super Agent.")
            
    result = calculate_file_hashes(test_file)
    print("نتائج فحص الملف البدئي:")
    print(f"SHA-256: {result.get('sha256')}")
    print(f"MD5: {result.get('md5')}")
