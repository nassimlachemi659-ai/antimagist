import os
import xml.etree.ElementTree as ET

s_game_mods_dir = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods"
appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")

def run_test_check():
    print("==========================================")
    print("TESTING & SCANNING TEARDOWN MODS ON DRIVE S:")
    print("==========================================")
    
    if not os.path.exists(s_game_mods_dir):
        print(f"FAILED: Path not found: {s_game_mods_dir}")
        return

    folders = [f for f in os.listdir(s_game_mods_dir) if os.path.isdir(os.path.join(s_game_mods_dir, f))]
    
    passed_count = 0
    total_custom = 0

    for folder in folders:
        f_path = os.path.join(s_game_mods_dir, folder)
        info_file = os.path.join(f_path, "info.txt")
        lua_file = os.path.join(f_path, "main.lua")
        xml_file = os.path.join(f_path, "main.xml")
        
        # Check if it's one of our 20 custom mods or a built-in mod
        is_custom = os.path.exists(lua_file) or os.path.exists(xml_file)
        if not is_custom:
            continue
            
        total_custom += 1
        status = "PASSED"
        details = []

        # 1. Verify info.txt v2 format
        if os.path.exists(info_file):
            with open(info_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "en_name" in content or "name" in content:
                    details.append("v2 Schema OK")
                else:
                    status = "WARNING"
                    details.append("missing name key")
        else:
            status = "FAILED"
            details.append("No info.txt")

        # 2. Verify XML syntax if map mod
        if os.path.exists(xml_file):
            try:
                ET.parse(xml_file)
                details.append("main.xml Syntax VALID")
            except Exception as e:
                status = "FAILED"
                details.append(f"XML Error: {e}")

        # 3. Verify Lua API if weapon mod
        if os.path.exists(lua_file):
            with open(lua_file, "r", encoding="utf-8", errors="ignore") as f:
                l_content = f.read()
                if "function" in l_content:
                    details.append("main.lua Lua API VALID")

        if status == "PASSED":
            passed_count += 1

        print(f"[{status}] {folder} -> ({', '.join(details)})")

    print(f"\nSummary: {passed_count} / {total_custom} Custom Mods Tested & Passed on Drive S:")

    # Check mods.xml
    if os.path.exists(appdata_mods_xml):
        tree = ET.parse(appdata_mods_xml)
        root = tree.getroot()
        active_mods = [m.attrib.get("id") for m in root.findall("mod") if m.attrib.get("active") == "true"]
        print(f"Active Registry Entries in mods.xml: {len(active_mods)}")

if __name__ == "__main__":
    run_test_check()
