with open("antimalware_app.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('f"Command failed with exit code {e.returncode}:\n{e.output}"', 'f"Command failed with exit code {e.returncode}:\\n{e.output}"')
c = c.replace('f"\n\n🌐 [NATIVE TOOL]: Opened \'{t}\'\n"', 'f"\\n\\n🌐 [NATIVE TOOL]: Opened \'{t}\'\\n"')
c = c.replace('output += "\n\n❌ FATAL', 'output += "\\n\\n❌ FATAL')
c = c.replace('self.after(0, lambda: self.log_ai_chunk("\n\n🛑 HALTING:', 'self.after(0, lambda: self.log_ai_chunk("\\n\\n🛑 HALTING:')

with open("antimalware_app.py", "w", encoding="utf-8") as f:
    f.write(c)
