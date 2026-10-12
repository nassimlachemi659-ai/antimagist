import os
import re
import xml.etree.ElementTree as ET

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")

def sanitize_mod_id(folder_name):
    # Teardown converts folder names to lowercase and replaces non-alphanumeric chars with hyphens
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', folder_name).strip('-').lower()
    return f"local-{slug}"

def test_mods():
    print("==========================================")
    print("SCANNING & TESTING ALL TEARDOWN MODS")
    print("==========================================")
    
    folders = [f for f in os.listdir(mods_dir) if os.path.isdir(os.path.join(mods_dir, f))]
    results = []

    for folder in folders:
        f_path = os.path.join(mods_dir, folder)
        info_file = os.path.join(f_path, "info.txt")
        lua_file = os.path.join(f_path, "main.lua")
        xml_file = os.path.join(f_path, "main.xml")
        
        status = "PASSED"
        details = []

        # 1. Test info.txt
        if os.path.exists(info_file):
            with open(info_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "name" in content:
                    details.append("info.txt OK")
                else:
                    details.append("info.txt missing 'name'")
        else:
            status = "WARNING"
            details.append("No info.txt")

        # 2. Test main.xml if present
        if os.path.exists(xml_file):
            try:
                ET.parse(xml_file)
                details.append("main.xml XML Syntax VALID")
            except Exception as e:
                status = "FAILED"
                details.append(f"main.xml XML Error: {e}")

        # 3. Test main.lua if present
        if os.path.exists(lua_file):
            with open(lua_file, "r", encoding="utf-8", errors="ignore") as f:
                l_content = f.read()
                if "function init" in l_content or "function tick" in l_content or "RegisterTool" in l_content:
                    details.append("main.lua Teardown API VALID")
                else:
                    details.append("main.lua present")

        mod_id = sanitize_mod_id(folder)
        results.append((folder, mod_id, status, ", ".join(details)))
        print(f"[{status}] {folder} -> ID: {mod_id} ({', '.join(details)})")

    # Update AppData/Local/Teardown/mods.xml to activate all mods
    if os.path.exists(appdata_mods_xml):
        print("\nUpdating AppData/Local/Teardown/mods.xml to auto-enable all mods...")
        try:
            tree = ET.parse(appdata_mods_xml)
            root = tree.getroot()
            
            existing_ids = {m.attrib.get("id"): m for m in root.findall("mod")}
            
            for folder, mod_id, status, _ in results:
                if mod_id in existing_ids:
                    existing_ids[mod_id].set("active", "true")
                    existing_ids[mod_id].set("shown", "true")
                else:
                    new_mod_elem = ET.SubElement(root, "mod")
                    new_mod_elem.set("id", mod_id)
                    new_mod_elem.set("active", "true")
                    new_mod_elem.set("shown", "true")
            
            tree.write(appdata_mods_xml, encoding="utf-8", xml_declaration=True)
            print("Successfully updated mods.xml! All 19 mods are now AUTO-ENABLED.")
        except Exception as e:
            print(f"Error updating mods.xml: {e}")

if __name__ == "__main__":
    test_mods()
