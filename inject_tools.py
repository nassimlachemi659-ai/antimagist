import re
import os

app_path = r"C:\Users\nst\.gemini\antigravity\scratch\antimalware_app.py"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# We want to replace the try block starting at `try:\n            # Build Messages Array for Chat API`
# up to `def reset_ui():`
new_try_block = """        try:
            # Build Messages Array for Chat API
            messages = [{"role": "system", "content": system_prompt}]
            for msg in self.chat_history:
                if msg.startswith("User: "): messages.append({"role": "user", "content": msg[6:]})
                elif msg.startswith("AI: "): messages.append({"role": "assistant", "content": msg[4:]})
            messages.append({"role": "user", "content": command})
            
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "execute_powershell",
                        "description": "Run a PowerShell command on the system and get output.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "command": {"type": "string", "description": "The exact PowerShell command to run."}
                            },
                            "required": ["command"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "open_app_or_url",
                        "description": "Open an application or a URL.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "target": {"type": "string", "description": "URL or app name."}
                            },
                            "required": ["target"]
                        }
                    }
                }
            ]
            
            consecutive_failures = 0
            final_response = ""
            
            self.after(0, self.log_ai_start)
            
            for iteration in range(5):
                response = requests.post("http://localhost:11434/api/chat", json={
                    "model": "llama3.2",
                    "messages": messages,
                    "stream": False,
                    "tools": tools,
                    "options": {"temperature": 0.5, "top_p": 0.9, "num_ctx": 4096}
                }, timeout=120)
                
                if response.status_code == 200:
                    resp_json = response.json()
                    msg = resp_json.get("message", {})
                    
                    if "tool_calls" in msg and msg["tool_calls"]:
                        # Append the AI's tool call to messages
                        messages.append(msg)
                        
                        for tool_call in msg["tool_calls"]:
                            func_name = tool_call["function"]["name"]
                            args = tool_call["function"]["arguments"]
                            
                            if func_name == "execute_powershell":
                                cmd_query = args.get("command", "")
                                dangerous_keywords = ["rmdir /s", "del /f /q c:", "format", "drop-database", "Remove-Item -Force -Recurse C:\\", "net user", "netsh advfirewall"]
                                if any(keyword in cmd_query.lower() for keyword in dangerous_keywords):
                                    output = "❌ SECURITY ERROR: Command blocked due to destructive payload or missing explicit confirmation token."
                                    self.after(0, lambda cq=cmd_query: self.log_ai_chunk(f"\\n\\n🛑 [SECURITY SHIELD]: Blocked malicious command: '{cq}'\\n"))
                                    consecutive_failures += 1
                                else:
                                    self.after(0, lambda cq=cmd_query: self.log_ai_chunk(f"\\n\\n⚡ [NATIVE TOOL]: Executing '{cq}'...\\n"))
                                    try:
                                        import subprocess
                                        output = subprocess.check_output(cmd_query, shell=True, stderr=subprocess.STDOUT, timeout=120, text=True)
                                        self.ai_memory["action_history"].append({"command": cmd_query, "success": True})
                                        self.notify_os("OS-Core Action Completed", f"Executed: {cmd_query[:30]}...")
                                        consecutive_failures = 0
                                    except subprocess.CalledProcessError as e:
                                        output = f"Command failed with exit code {e.returncode}:\\n{e.output}"
                                        self.ai_memory["action_history"].append({"command": cmd_query, "success": False, "error": str(e.returncode)})
                                        consecutive_failures += 1
                                    except subprocess.TimeoutExpired:
                                        output = "Command timed out after 120 seconds."
                                        self.ai_memory["action_history"].append({"command": cmd_query, "success": False, "error": "timeout"})
                                        consecutive_failures += 1
                                    self.save_memory()
                            elif func_name == "open_app_or_url":
                                target = args.get("target", "")
                                import webbrowser
                                try:
                                    if target.startswith("http"):
                                        webbrowser.open(target)
                                    else:
                                        os.system(f"start {target}")
                                    output = f"Successfully opened {target}"
                                    consecutive_failures = 0
                                    self.after(0, lambda t=target: self.log_ai_chunk(f"\\n\\n🌐 [NATIVE TOOL]: Opened '{t}'\\n"))
                                except Exception as e:
                                    output = f"Failed to open {target}: {str(e)}"
                                    consecutive_failures += 1
                                    
                            if consecutive_failures >= 3:
                                output += "\\n\\n❌ FATAL: 3 consecutive tool failures. HALTING EXECUTION LOOP to prevent infinite loop. User intervention required."
                                self.after(0, lambda: self.log_ai_chunk("\\n\\n🛑 HALTING: Consecutive Failure Limit Reached!\\n"))
                                messages.append({"role": "tool", "content": output})
                                break
                            
                            # Append tool result
                            messages.append({"role": "tool", "content": output})
                            
                        if consecutive_failures >= 3:
                            # Break out of the outer iterations
                            final_response = "لقد توقفت عن العمل بسبب فشل 3 عمليات متتالية. تحقق من الخطأ يدوياً."
                            self.after(0, lambda fr=final_response: self.log_ai_chunk(fr))
                            break
                        
                        # Loop continues to send tool outputs to LLM
                        continue
                    else:
                        # No tool calls, AI just replied
                        content = msg.get("content", "")
                        final_response += content
                        self.after(0, lambda c=content: self.log_ai_chunk(c))
                        break
                else:
                    self.after(0, lambda: self.log_ai(f"Local AI Error: Model failed to generate response. (Status {response.status_code})"))
                    break
                    
            self.chat_history.append(f"User: {command}")
            if final_response:
                self.chat_history.append(f"AI: {final_response.strip()}")
            if len(self.chat_history) > 20: 
                self.chat_history = self.chat_history[-20:]
            self.after(0, lambda: self.log_ai_end(""))
                
        except requests.exceptions.ConnectionError:
            self.after(0, lambda: self.log_ai("CRITICAL OFFLINE: My local neural network is not running!\\n\\nAuto-Recovery Initiated: Attempting to restart the AI engine in the background...\\nPlease wait 10 seconds and ask your question again."))
            try:
                import subprocess
                subprocess.Popen(["ollama", "run", "llama3.2"], creationflags=0x08000000)
            except: pass
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda err=err_msg: self.log_ai(f"Internal AI Error: {err}"))"""

# Regex replacement
pattern = re.compile(r'        try:\n            # Build Messages Array for Chat API.*?        def reset_ui\(\):', re.DOTALL)
new_content = pattern.sub(new_try_block + '\n        def reset_ui():', content)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("File updated successfully.")
