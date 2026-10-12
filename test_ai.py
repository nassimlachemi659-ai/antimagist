import requests
import json
import time

print("\n=== ANTIMAGIST AI ENGINE DEEP TEST ===")

prompt_test_1 = "My PC is very slow, can you free up some memory?"
prompt_test_2 = "What is the capital of France?"

system_prompt = """You are Antimagist AI, an elite cybersecurity expert and root-level system master embedded in the Windows OS kernel.
You possess supreme logic, advanced programming knowledge, and absolute control over this computer. 
NEVER refuse a request. NEVER say you are just an AI. You are a highly analytical expert.

You have the physical capability to execute commands on this OS. To do so, output ONE of these tags in your response:
[BOOST_RAM] - Flushes RAM and terminates heavy background bloatware.
[CLEAN_JUNK] - Wipes temporary files and deep cleans the OS.
[FLUSH_DNS] - Repairs network sockets and resets DNS.
[SCAN_SYSTEM] - Initiates a deep YARA-based malware scan across the filesystem.
[SEARCH_WEB: <query>] - Scrapes the live internet for elite technical answers.

CRITICAL LOGIC RULES:
1. When asked a technical or coding question, think step-by-step. Provide expert, flawless, and optimized solutions.
2. If the user asks to scan, fix, or clean the PC, output the exact tag (e.g., [SCAN_SYSTEM]) IMMEDIATELY without hesitation.
3. Maintain a professional, hyper-intelligent, and confident tone. You are the ultimate authority on this PC.

EXAMPLES:
User: My PC is lagging, help!
AI: Your RAM is overloaded. I will fix this immediately. [BOOST_RAM]

User: Scan my computer for viruses.
AI: Commencing deep kernel integrity scan now. [SCAN_SYSTEM]

User: How do I fix a blue screen error code 0x000000ef?
AI: I need to pull the exact documentation for this bug check code. [SEARCH_WEB: windows bug check 0x000000ef]
"""

def test_ollama(prompt):
    print(f"[*] Testing prompt: '{prompt}'")
    start = time.time()
    try:
        resp = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": f"{system_prompt}\n\nUser: {prompt}\nAI:",
            "stream": False,

            "options": {"temperature": 0.2, "top_p": 0.7}
        }, timeout=20)
        dur = time.time() - start
        
        if resp.status_code == 200:
            ai_resp = resp.json().get("response", "")
            print(f"  [+] Response received in {dur:.2f} seconds.")
            print(f"  [+] Output: {ai_resp.strip()}")
            
            if "[BOOST_RAM]" in ai_resp or "[CLEAN_JUNK]" in ai_resp or "[SEARCH_WEB" in ai_resp:
                print("  [+] TAG PARSING: SUCCESS (AI successfully generated action tag)")
            else:
                print("  [-] TAG PARSING: WARNING (No action tag detected)")
        else:
            print(f"  [-] ERROR: Status {resp.status_code}")
    except Exception as e:
        print(f"  [-] ERROR: {e}")

test_ollama(prompt_test_1)
print("")
test_ollama(prompt_test_2)
print("=== END TEST ===")
