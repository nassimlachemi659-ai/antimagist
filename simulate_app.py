import os, time
import threading
from antimalware_app import AntiMalwareApp

app = AntiMalwareApp()
def start_app():
    app.mainloop()

threading.Thread(target=start_app, daemon=True).start()
time.sleep(2) # wait for ui to load

app.ai_entry.insert(0, "hey")
app.handle_ai_input()

time.sleep(10) # wait for ai to reply
app.destroy()
