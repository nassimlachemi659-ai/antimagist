import subprocess
import re

def clear_xbl_credentials():
    print("Scanning Windows Credential Manager for stale Xbox Live tokens...")
    try:
        output = subprocess.check_output("cmdkey /list", shell=True, text=True)
        targets = []
        for line in output.splitlines():
            if "Target:" in line:
                target = line.split("Target:", 1)[1].strip()
                target = target.replace("LegacyGeneric:target=", "").replace("WindowsLive:target=", "")
                if "Xbl" in target or "Xbox" in target:
                    targets.append(target)
        
        print(f"Found {len(targets)} Xbox credential targets to clear:")
        for t in targets:
            print(f" - Deleting credential target: {t}")
            cmd = f'cmdkey /delete:"{t}"'
            subprocess.run(cmd, shell=True)
            
        print("Successfully cleared stale Xbox Live credentials!")
    except Exception as e:
        print(f"Error clearing credentials: {e}")

if __name__ == "__main__":
    clear_xbl_credentials()
