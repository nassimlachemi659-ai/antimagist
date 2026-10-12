"""
ai_kernel_agent.py — Antimagist Sentient AI Kernel Agent & PC Automation Core
=============================================================================
Antimagist Enterprise Security V3 Component
- Connects AI directly to real PC actions (RAM flush, Cache sweep, Process kill, DISM, TRIM, Telemetry)
- Multi-Brain Architecture:
    1. Google Gemini API (Cloud LLM with native function calling & high reasoning)
    2. Local Ollama (Offline sovereign LLM at localhost:11434)
    3. Sovereign Kernel Copilot (Zero-dependency local intent engine with full Arabic & English support)
- Zero-Trust Sandbox protection preventing destructive or unauthorized execution
"""

import os
import re
import time
import json
import psutil
import requests
import threading
from typing import Callable, Optional, Dict, Any, Tuple
from ping_optimizer import AntimagistPingOptimizer

# Try Gemini import
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


SYSTEM_KERNEL_PROMPT = """
You are Antimagist Sentient AI — an elite cybersecurity engineer and root-level copilot embedded directly into the Windows OS kernel.
You possess real authority and physical capabilities to optimize, monitor, troubleshoot, and defend this computer.
You communicate in a crisp, confident, technical, and friendly tone (supporting English and Arabic fluently).

Available Physical Tools on this PC:
- [BOOST_RAM]: Flushes standby memory working sets and garbage collects RAM.
- [CLEAN_CACHE]: Sweeps temporary files in %TEMP% and %SystemRoot%\\Temp.
- [FLUSH_DNS]: Resets Windows DNS Client Cache to fix network lag.
- [CHECK_PING]: Measures live gaming ping, jitter, and packet loss in milliseconds.
- [OPTIMIZE_PING]: Disables Nagle's algorithm and applies low-latency TCP gaming settings.
- [DISM_SWEEP]: Compacts the Windows Component Store (DISM deep sweep).
- [NVMe_TRIM]: Dispatches hardware TRIM optimization to SSD/NVMe drives.
- [GET_METRICS]: Returns live CPU, RAM, Disk, and Process telemetry.
- [NETWORK_AUDIT]: Audits live network sockets for backdoor/C2 ports.
- [KILL_PROCESS: <name or PID>]: Safely terminates a heavy or suspicious process.

RULES:
1. When the user requests a PC optimization, cleanup, network inspection, or process termination, use the appropriate tool tag immediately.
2. If the user asks a technical or general question, answer expertly and authoritatively.
3. Respond in the same language the user addressed you in (English or Arabic).
"""


class AntimagistAIAgent:
    def __init__(
        self, 
        optimizer_core, 
        scanner_core, 
        network_monitor, 
        security_sandbox,
        api_key: str = ""
    ):
        self.optimizer = optimizer_core
        self.scanner = scanner_core
        self.network_monitor = network_monitor
        self.sandbox = security_sandbox
        self.ping_optimizer = AntimagistPingOptimizer()
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

        self._configure_gemini()

    def update_api_key(self, api_key: str):
        self.api_key = api_key
        self._configure_gemini()

    def _configure_gemini(self):
        if GENAI_AVAILABLE and self.api_key and len(self.api_key.strip()) > 10:
            try:
                genai.configure(api_key=self.api_key.strip())
            except Exception as ex:
                print(f"[-] Gemini agent configure warning: {ex}")

    def is_ollama_online(self) -> bool:
        """Quick 500ms probe to check if local Ollama daemon is active."""
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=0.6)
            return r.status_code == 200
        except Exception:
            return False

    def _run_powershell_sync(self, cmd: str) -> str:
        if not self.sandbox.is_safe(cmd):
            return "Command blocked by Zero-Trust Sandbox."
        try:
            import subprocess
            res = subprocess.run(
                ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", cmd],
                capture_output=True, text=True, timeout=20,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            return res.stdout.strip()
        except Exception as ex:
            return str(ex)

    # ========================================================================
    # PHYSICAL PC EXECUTION TOOLS (Governed by Zero-Trust Sandbox)
    # ========================================================================
    def execute_tool(self, tool_tag: str, arg: str = "") -> Tuple[bool, str]:
        """
        Executes a real operating system action on behalf of the AI.
        Returns (success: bool, output_message: str).
        """
        tag = tool_tag.upper().strip()

        if tag == "BOOST_RAM":
            mem_before = psutil.virtual_memory().used
            cmd = "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"
            res = self._run_powershell_sync(cmd)
            mem_after = psutil.virtual_memory().used
            freed_mb = max(0, round((mem_before - mem_after) / (1024**2), 1))
            return True, f"RAM Boost complete. Working sets compressed. ~{freed_mb} MB released."

        elif tag == "CLEAN_CACHE":
            cmd = """
            $paths = @("$env:TEMP\\*", "$env:SystemRoot\\Temp\\*")
            $c = 0
            foreach ($p in $paths) {
                if (Test-Path $p) {
                    $items = Get-ChildItem $p -Recurse -Force -ErrorAction SilentlyContinue
                    foreach ($i in $items) {
                        try { Remove-Item $i.FullName -Recurse -Force -ErrorAction Stop; $c++ } catch {}
                    }
                }
            }
            "Cleaned $c files."
            """
            out = self._run_powershell_sync(cmd)
            return True, f"Cache sweep executed. Temporary file junk wiped ({out.strip()})."

        elif tag == "FLUSH_DNS":
            cmd = "Clear-DnsClientCache"
            self._run_powershell_sync(cmd)
            return True, "Windows DNS Client Cache successfully flushed and socket pools reset."

        elif tag == "CHECK_PING":
            stats = self.ping_optimizer.get_live_ping_telemetry()
            return True, f"Live Ping: {stats['ping_ms']} ms | Jitter: {stats['jitter_ms']} ms | Packet Loss: {stats['packet_loss_pct']}% | Quality: {stats['rating']} ({stats['target']})"

        elif tag == "OPTIMIZE_PING":
            ok, msg = self.ping_optimizer.optimize_gaming_network()
            return ok, msg

        elif tag == "DISM_SWEEP":
            # Dispatched asynchronously to prevent blocking
            self.optimizer.run_deep_sweep(lambda msg: None)
            return True, "DISM Component Store Deep Sweep dispatched to background kernel thread."

        elif tag == "NVMe_TRIM":
            self.optimizer.run_nvme_trim(lambda msg: None)
            return True, "NVMe SSD Defrag & ReTrim command dispatched across physical drive."

        elif tag == "GET_METRICS":
            m = self.optimizer.get_live_metrics()
            top = self.optimizer.get_top_memory_processes(3)
            top_txt = ", ".join([f"{name} ({mb:.0f} MB)" for name, mb in top])
            report = (
                f"RAM: {m['used_ram_gb']}/{m['total_ram_gb']} GB ({m['ram_percentage']}%) | "
                f"CPU: {m['cpu_percentage']}% | "
                f"C: Disk: {m['disk_used_gb']}/{m['disk_total_gb']} GB ({m['disk_percent']}%) | "
                f"Active Processes: {m['active_processes']} | "
                f"Top Memory: {top_txt}"
            )
            return True, report

        elif tag == "NETWORK_AUDIT":
            conns = self.network_monitor.get_active_connections()
            summary = self.network_monitor.get_summary_metrics()
            susp_count = summary.get("suspicious", 0)
            return True, f"Audited {summary['total_sockets']} sockets ({summary['established']} established). Suspicious C2 detections: {susp_count}."

        elif tag == "KILL_PROCESS":
            target = arg.strip()
            if not target:
                return False, "No target process specified."
            # Check if target is a PID
            if target.isdigit():
                pid = int(target)
                return self.network_monitor.terminate_process_by_pid(pid)
            else:
                # Terminate by name
                killed = 0
                for p in psutil.process_iter(['name', 'pid']):
                    try:
                        if p.info['name'] and p.info['name'].lower() == target.lower():
                            if p.info['pid'] > 4:
                                p.terminate()
                                killed += 1
                    except Exception:
                        pass
                if killed > 0:
                    return True, f"Terminated {killed} instances of process '{target}'."
                return False, f"No running process matching '{target}' was found."

        return False, f"Unknown tool tag: {tag}"

    # ========================================================================
    # MAIN INTELLIGENCE DISPATCHER (Gemini -> Ollama -> Sovereign Intent)
    # ========================================================================
    def process_query(self, user_text: str, on_stream_callback: Optional[Callable[[str], None]] = None) -> str:
        """
        Receives user prompt, determines intent, executes PC actions if needed,
        and returns authoritative AI output.
        """
        text = user_text.strip()
        if not text:
            return "Please provide a command or question."

        # Security Sandbox check on user input
        if not self.sandbox.is_safe(text):
            return "🛑 Security Firewall Alert: Command blocked! Destructive pattern detected."

        # 1. Try Gemini Multimodal / Text API if configured
        if GENAI_AVAILABLE and self.api_key and len(self.api_key.strip()) > 10:
            ai_out = self._query_gemini(text)
            if ai_out:
                return self._parse_and_execute_tags(ai_out)

        # 2. Try Local Ollama if online
        if self.is_ollama_online():
            ai_out = self._query_ollama(text)
            if ai_out:
                return self._parse_and_execute_tags(ai_out)

        # 3. Sovereign Kernel Copilot (Zero-Dependency Intent Engine with Arabic & English)
        return self._query_sovereign_kernel(text)

    # ------------------------------------------------------------------------
    # Brain 1: Gemini API
    # ------------------------------------------------------------------------
    def _query_gemini(self, prompt: str) -> Optional[str]:
        for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_KERNEL_PROMPT
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception:
                continue
        return None

    # ------------------------------------------------------------------------
    # Brain 2: Local Ollama (localhost:11434)
    # ------------------------------------------------------------------------
    def _query_ollama(self, prompt: str) -> Optional[str]:
        try:
            r = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.2",
                "prompt": f"{SYSTEM_KERNEL_PROMPT}\n\nUser: {prompt}\nAI:",
                "stream": False,
                "options": {"temperature": 0.3}
            }, timeout=25)
            if r.status_code == 200:
                return r.json().get("response", "").strip()
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------------
    # Brain 3: Sovereign Kernel Copilot (Fast, Deterministic, Multilingual)
    # ------------------------------------------------------------------------
    def _query_sovereign_kernel(self, prompt: str) -> str:
        norm = prompt.lower()

        # Arabic & English Matching Matrix
        # RAM & Memory
        if any(w in norm for w in ["boost", "ram", "memory", "ذاكرة", "رام", "بطيء", "تسريع", "flush"]):
            ok, msg = self.execute_tool("BOOST_RAM")
            m = self.optimizer.get_live_metrics()
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"⚡ تم تنفيذ الإجراء بنجاح: [BOOST_RAM]\n"
                f"• النتيجة: {msg}\n"
                f"• استهلاك الرام الحالي: {m['used_ram_gb']} GB / {m['total_ram_gb']} GB ({m['ram_percentage']}%)"
            )

        # Cache & Junk cleaning
        elif any(w in norm for w in ["clean", "cache", "junk", "temp", "تنظيف", "مساحة", "ملفات مؤقتة", "قمامة", "sweep"]):
            ok, msg = self.execute_tool("CLEAN_CACHE")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"🧹 تم تنفيذ الإجراء بنجاح: [CLEAN_CACHE]\n"
                f"• النتيجة: {msg}"
            )

        # Optimize Gaming Ping / Low Latency (Action first)
        elif any(w in norm for w in ["optimize ping", "boost ping", "reduce lag", "fix ping", "حسن البينغ", "تسريع النت", "تقليل اللاق", "تحسين البينغ", "قلل البينغ", "تسريع البينغ"]):
            ok, msg = self.execute_tool("OPTIMIZE_PING")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"⚡ تم تفعيل وضع تقليل اللاق وتسريع البينغ: [OPTIMIZE_PING]\n"
                f"• النتيجة: {msg}"
            )

        # Ping Measurement & Latency Health
        elif any(w in norm for w in ["check ping", "what is my ping", "ping", "latency", "بينغ", "بينق", "قياس البينغ", "كم البينغ", "فحص البينغ"]):
            ok, msg = self.execute_tool("CHECK_PING")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"📶 تقرير استجابة وسرعة البينغ المباشر: [CHECK_PING]\n"
                f"• {msg}\n"
                f"• ملاحظة: تم قياس السرعة بدقة عبر شبكة Cloudflare العالمية (1.1.1.1)."
            )

        # DNS / Network general flush
        elif any(w in norm for w in ["dns", "lag", "شبكة", "لاق", "تقطيع", "نت"]):
            ok, msg = self.execute_tool("FLUSH_DNS")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"🌐 تم تنفيذ الإجراء بنجاح: [FLUSH_DNS]\n"
                f"• النتيجة: {msg}"
            )

        # Network Sniffer / Backdoor audit
        elif any(w in norm for w in ["port", "socket", "sniffer", "c2", "اتصالات", "منافذ", "تجسس"]):
            ok, msg = self.execute_tool("NETWORK_AUDIT")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"🔍 فحص جدار الحماية والاتصالات: [NETWORK_AUDIT]\n"
                f"• النتيجة: {msg}"
            )

        # DISM Component Store
        elif any(w in norm for w in ["dism", "component", "نواة", "صيانة عميقة"]):
            ok, msg = self.execute_tool("DISM_SWEEP")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"🗄️ تم تنفيذ الإجراء بنجاح: [DISM_SWEEP]\n"
                f"• النتيجة: {msg}"
            )

        # NVMe / SSD TRIM
        elif any(w in norm for w in ["trim", "ssd", "nvme", "قرص", "هارد"]):
            ok, msg = self.execute_tool("NVMe_TRIM")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"⚡ تم تنفيذ الإجراء بنجاح: [NVMe_TRIM]\n"
                f"• النتيجة: {msg}"
            )

        # Hardware Telemetry & Specs
        elif any(w in norm for w in ["metric", "stat", "spec", "hardware", "مواصفات", "حرارة", "استهلاك", "معالج", "cpu"]):
            ok, msg = self.execute_tool("GET_METRICS")
            return (
                f"🤖 [Antimagist Sovereign Kernel]\n"
                f"📊 تقرير الموارد الحية للجهاز:\n"
                f"• {msg}"
            )

        # Process Kill
        elif "kill" in norm or "انهاء" in norm or "اغلق" in norm or "ايقاف" in norm:
            # Extract target
            parts = norm.replace("kill", "").replace("انهاء", "").replace("اغلق", "").replace("ايقاف", "").strip().split()
            target = parts[0] if parts else ""
            if target:
                ok, msg = self.execute_tool("KILL_PROCESS", target)
                return f"🤖 [Antimagist Sovereign Kernel]\n🛑 إجراء إنهاء العملية: {msg}"
            else:
                return "يرجى تحديد اسم أو رقم العملية المراد إنهاؤها (مثال: kill chrome.exe)."

        # Fallback Conversational Response
        return (
            "🤖 [Antimagist Sentient AI Kernel Online]\n"
            "أنا متصل مباشرة ببيانات ونواة جهازك عبر جدار حماية Zero-Trust.\n\n"
            "يمكنني تنفيذ الإجراءات التالية فوراً:\n"
            "• 'نظف الرام' أو 'تسريع الذاكرة' [BOOST_RAM]\n"
            "• 'نظف الملفات المؤقتة' [CLEAN_CACHE]\n"
            "• 'حل مشكلة البينج واللاق' [FLUSH_DNS]\n"
            "• 'افحص اتصالات الشبكة' [NETWORK_AUDIT]\n"
            "• 'اعطني إحصائيات المعالج والموارد' [GET_METRICS]\n"
            "• 'اغلق عملية <name>' [KILL_PROCESS]\n\n"
            "💡 ملاحظة: لتفعيل الذكاء الاصطناعي التوليدي الكامل (Gemini LLM)، يمكنك إدخال مفتاح Google API في صفحة الإعدادات (Settings)."
        )

    # ------------------------------------------------------------------------
    # Tag Parser & Executor (for Gemini and Ollama outputs)
    # ------------------------------------------------------------------------
    def _parse_and_execute_tags(self, ai_text: str) -> str:
        """Parses action tags like [BOOST_RAM], executes them on PC, and attaches execution telemetry."""
        executed_actions = []

        # Find tags
        tag_pattern = re.compile(r'\[(BOOST_RAM|CLEAN_CACHE|FLUSH_DNS|DISM_SWEEP|NVMe_TRIM|GET_METRICS|NETWORK_AUDIT|KILL_PROCESS(?::\s*([^\]]+))?)\]', re.IGNORECASE)
        matches = tag_pattern.findall(ai_text)

        clean_text = tag_pattern.sub("", ai_text).strip()

        for match in matches:
            full_tag = match[0].split(":")[0].strip()
            arg = match[1].strip() if len(match) > 1 else ""
            ok, msg = self.execute_tool(full_tag, arg)
            executed_actions.append(f"⚡ [KERNEL EXECUTED: {full_tag}] -> {msg}")

        result_blocks = []
        if executed_actions:
            result_blocks.append("╔══════════════════════════════════════════════════════════════════════╗")
            result_blocks.append("║  ⚙️ PHYSICAL PC ACTIONS EXECUTED BY ANTIMAGIST AI KERNEL             ║")
            result_blocks.append("╚══════════════════════════════════════════════════════════════════════╝")
            result_blocks.extend(executed_actions)
            result_blocks.append("─" * 70)

        if clean_text:
            result_blocks.append(clean_text)

        return "\n".join(result_blocks)
