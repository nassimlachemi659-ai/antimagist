import os
import xml.etree.ElementTree as ET
import re

s_mods = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods"

def check_map_assets(mod_name):
    print(f"\n--- Checking Map Assets for: {mod_name} ---")
    mod_dir = os.path.join(s_mods, mod_name)
    main_xml = os.path.join(mod_dir, "main.xml")
    
    if not os.path.exists(main_xml):
        print(f"ERROR: {main_xml} does not exist!")
        return False
        
    try:
        tree = ET.parse(main_xml)
        root = tree.getroot()
        print(" - XML Syntax: VALID")
    except Exception as e:
        print(f" - XML Syntax: ERROR: {e}")
        return False
        
    # Check spawnpoint
    spawn = root.find(".//spawnpoint")
    if spawn is not None:
        print(f" - Spawnpoint: FOUND at pos={spawn.attrib.get('pos')}")
    else:
        print(" - Spawnpoint: WARNING: No <spawnpoint> element found directly, checking text...")

    # Check referenced files
    with open(main_xml, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    file_refs = re.findall(r'file="([^"]+)"', content)
    brush_refs = re.findall(r'brush="([^"]+)"', content)
    all_refs = set(file_refs + brush_refs)
    
    missing = []
    found = 0
    for ref in all_refs:
        if ref.startswith("MOD/"):
            rel_path = ref[4:]
            full_path = os.path.join(mod_dir, rel_path)
            # Normalize path
            full_path = os.path.normpath(full_path)
            if not os.path.exists(full_path):
                missing.append(ref)
            else:
                found += 1
        elif ref in ["main.lua", "sandbox.lua"]:
            found += 1 # standard game scripts

    print(f" - Asset References: {found} OK, {len(missing)} missing.")
    if missing:
        print(f" - First 5 missing references: {missing[:5]}")
    return len(missing) == 0

def check_weapons():
    print("\n--- Checking Weapon Scripts & 3D Voxel Assets ---")
    weapons = [
        "Orbital_Laser_Strike",
        "Black_Hole_Singularity",
        "Mjolnir_Thunder_Hammer",
        "Hyper_Precision_Railgun"
    ]
    for w in weapons:
        w_dir = os.path.join(s_mods, w)
        info = os.path.join(w_dir, "info.txt")
        lua = os.path.join(w_dir, "main.lua")
        vox = os.path.join(w_dir, "vox", "weapon.vox")
        
        info_ok = os.path.exists(info)
        lua_ok = os.path.exists(lua)
        vox_size = os.path.getsize(vox) if os.path.exists(vox) else 0
        
        # Check lua for #version 2 and server hooks
        with open(lua, "r", encoding="utf-8") as f:
            lua_code = f.read()
        has_v2 = "#version 2" in lua_code
        has_server_init = "function server.init()" in lua_code
        has_server_tick = "function server.tick" in lua_code
        has_usetool = 'InputDown("usetool"' in lua_code or 'InputPressed("usetool"' in lua_code
        
        print(f"Weapon: {w}")
        print(f"  - 3D Model: {'EXISTS (' + str(vox_size) + ' bytes)' if vox_size > 0 else 'MISSING'}")
        print(f"  - Script v2: {has_v2} | Server Init: {has_server_init} | Server Tick: {has_server_tick} | Shoot Trigger: {has_usetool}")

if __name__ == "__main__":
    check_map_assets("Boeing_737_Burning_Edition")
    check_map_assets("Gwels_High_Skyscraper")
    check_map_assets("Mega_Destruction_Metropolis")
    check_weapons()
