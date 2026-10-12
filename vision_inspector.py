"""
vision_inspector.py — Gemini Multimodal AI Vision Threat Inspector
===================================================================
Antimagist Enterprise Security V3 Component
- Analyzes screenshots of suspicious websites, phishing emails, or ransom notes
- Dissects visual indicators of compromise (IOCs) using Google Gemini Multimodal Vision
- Provides deterministic heuristic fallback if API key is not configured
"""

import os
import hashlib
from typing import Optional, Dict, Any
from PIL import Image

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

SECURITY_ANALYSIS_PROMPT = """
You are Antimagist Enterprise AI Kernel Security Inspector.
Analyze this user-submitted screenshot or image carefully for security threats.

Provide a structured, authoritative assessment with these exact sections:
1. 🛡️ THREAT CLASSIFICATION: (e.g. Phishing / Fake Antivirus Scam / Ransomware Note / Deceptive Website / Legitimate System Dialog / Clean)
2. 🔍 VISUAL INDICATORS OF COMPROMISE: (Describe deceptive UI patterns, fake logos, suspicious URLs, urgent social engineering language, or fake error codes)
3. 🛑 RECOMMENDED MITIGATION: (Step-by-step actions for the user: e.g. Do not click links, terminate browser, isolate network, safe to proceed)

Keep your response concise, professional, and clear.
"""

class AntimagistVisionInspector:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self._configure_client()

    def update_api_key(self, api_key: str):
        self.api_key = api_key
        self._configure_client()

    def _configure_client(self):
        if GENAI_AVAILABLE and self.api_key and len(self.api_key.strip()) > 10:
            try:
                genai.configure(api_key=self.api_key.strip())
            except Exception as ex:
                print(f"[-] Gemini configure error: {ex}")

    def analyze_image_file(self, image_path: str) -> Dict[str, Any]:
        """Analyzes an image file for visual threats."""
        if not os.path.exists(image_path):
            return {"success": False, "message": "Image file not found on disk."}

        # Basic metadata & hash
        sha256 = hashlib.sha256()
        try:
            with open(image_path, "rb") as f:
                sha256.update(f.read())
            img_hash = sha256.hexdigest()
            with Image.open(image_path) as img_handle:
                pil_img = img_handle.copy()
            width, height = pil_img.size
        except Exception as ex:
            return {"success": False, "message": f"Failed to load image: {ex}"}

        # Check if Gemini Multimodal Vision is available
        if GENAI_AVAILABLE and self.api_key and len(self.api_key.strip()) > 10:
            for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro-vision"]:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content([SECURITY_ANALYSIS_PROMPT, pil_img])
                    ai_text = response.text.strip() if response.text else "No analysis returned from Gemini."
                    return {
                        "success": True,
                        "engine": f"Gemini Vision ({model_name})",
                        "hash": img_hash,
                        "resolution": f"{width}x{height}",
                        "analysis": ai_text
                    }
                except Exception:
                    continue

        # Heuristic fallback
        fallback_analysis = (
            f"ℹ️ Local Image Audit:\n"
            f"• Dimensions: {width}x{height} px\n"
            f"• SHA-256 Signature: {img_hash[:20]}...\n\n"
            f"⚠️ Notice: To unlock real-time Gemini AI Vision Threat Analysis (phishing detection & scam dissection), "
            f"ensure a valid Google Gemini API Key is entered in the 'Settings' pane."
        )
        return {
            "success": True,
            "engine": "Local Image Telemetry",
            "hash": img_hash,
            "resolution": f"{width}x{height}",
            "analysis": fallback_analysis
        }
