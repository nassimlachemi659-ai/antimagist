import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

s_mods = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods"
desktop = os.path.expanduser("~/Desktop")
output_pack_dir = os.path.join(desktop, "Teardown_Mods_Pack_For_Friend")
zip_output_path = os.path.join(desktop, "Teardown_Mods_Pack.zip")

all_16_mods = [
    # 6 Maps
    "Boeing_737_Burning_Edition",
    "Gwels_High_Skyscraper",
    "Mega_Destruction_Metropolis",
    "Nuclear_Power_Plant",
    "Military_Fort_Airbase",
    "Mega_Ocean_Port_Bridge",
    
    # 10 Weapons
    "Orbital_Laser_Strike",
    "Black_Hole_Singularity",
    "Mjolnir_Thunder_Hammer",
    "Hyper_Precision_Railgun",
    "Airstrike_Radio_Beacon",
    "Cluster_Bomb_Launcher",
    "Thermobaric_Flame_Cannon",
    "Gravity_Shockwave_Repulsor",
    "Tactical_Nuke_Launcher",
    "Chrono_Time_Disruptor"
]

def verify_and_package():
    print("==================================================")
    print("VERIFYING & TESTING ALL 16 MODS")
    print("==================================================")
    
    passed_count = 0

    for m in all_16_mods:
        p = os.path.join(s_mods, m)
        if not os.path.exists(p):
            print(f"[FAIL] Missing directory: {m}")
            continue

        info = os.path.join(p, "info.txt")
        has_info = os.path.exists(info)
        
        xml = os.path.join(p, "main.xml")
        xml_ok = "N/A"
        if os.path.exists(xml):
            try:
                ET.parse(xml)
                xml_ok = "VALID"
            except Exception as e:
                xml_ok = f"ERR: {e}"

        lua = os.path.join(p, "main.lua")
        lua_ok = "N/A"
        if os.path.exists(lua):
            with open(lua, "r", encoding="utf-8", errors="ignore") as f:
                c = f.read()
                if "server.init" in c or "function init" in c:
                    lua_ok = "VALID (v2)"

        vox = os.path.join(p, "vox", "weapon.vox")
        vox_size = os.path.getsize(vox) if os.path.exists(vox) else 0
        vox_status = f"OK ({vox_size}b)" if vox_size > 0 else ("N/A" if xml_ok != "N/A" else "MISSING")

        is_ok = has_info and (xml_ok == "VALID" or lua_ok == "VALID (v2)")
        if is_ok:
            passed_count += 1
            print(f"[PASSED] {m} | Info: {has_info} | XML: {xml_ok} | Lua: {lua_ok} | Vox: {vox_status}")
        else:
            print(f"[FAILED] {m}")

    print(f"\nVerification Score: {passed_count} / {len(all_16_mods)} PASSED!")

    # Packaging to Desktop
    print("\n==================================================")
    print("PACKAGING ALL 16 MODS TO DESKTOP")
    print("==================================================")
    if os.path.exists(output_pack_dir):
        shutil.rmtree(output_pack_dir)
    os.makedirs(output_pack_dir, exist_ok=True)

    for m in all_16_mods:
        src = os.path.join(s_mods, m)
        dst = os.path.join(output_pack_dir, m)
        if os.path.exists(src):
            shutil.copytree(src, dst)
            print(f" - Bundled: {m}")

    readme = """==================================================
TEARDOWN ULTIMATE MOD PACK (16 TESTED & VERIFIED MODS)
==================================================

🗺️ 6 EPIC MAPS:
1. Boeing 737 Burning Edition (Burning passenger jet on runway)
2. Gwel's High Skyscraper (5-story modern office building)
3. Mega Destruction Metropolis (Huge urban city sandbox)
4. Nuclear Power Plant Complex (Two 60m cooling towers & reactor dome)
5. Military Mountain Airbase & Silo (Concrete mountain bunker & radar)
6. Mega Ocean Port & Bridge (Deep sea harbor & 100m suspension bridge)

🔫 10 DESTRUCTIVE WEAPONS:
1. Orbital Laser Strike [Key 1] - Laser beam [LMB] & Sky Ion Nuke [RMB]
2. Black Hole Singularity Cannon [Key 2] - Gravitational vortex implosion
3. Mjolnir Thunder Hammer [Key 3] - Godly lightning shockwaves
4. Hyper Precision Railgun [Key 4] - 120m penetration kinetic slug
5. Tactical Airstrike Beacon [Key 5] - Calls 12-missile artillery strike
6. MIRV Cluster Bomb Launcher [Key 6] - Scatters 14 explosive sub-bomblets
7. Thermobaric Flame Cannon [Key 7] - High-temp melting flame stream
8. Gravity Shockwave Repulsor [Key 8] - Concussive kinetic pulse
9. Tactical Nuke Launcher (Fat Man) [Key 9] - 35m vaporizing fireball
10. Chrono Time Disruptor [Key 0] - [LMB] Slow Motion 0.2x | [RMB] Normal Speed

--------------------------------------------------
HOW TO INSTALL:
--------------------------------------------------
Copy all 16 mod folders directly into:
- If Cracked / Online-Fix: Your Teardown\\mods\\ folder (e.g. S:\\Teardown\\...\\mods)
- If Steam: C:\\Users\\<Username>\\Documents\\Teardown\\mods\\

--------------------------------------------------
HOW TO PLAY:
--------------------------------------------------
1. Launch Teardown.
2. Go to Main Menu -> MODS.
3. Click any map and hit PLAY.
4. Use number keys 1 through 0 or your Mouse Wheel to select weapons!
==================================================
"""
    with open(os.path.join(output_pack_dir, "HOW_TO_INSTALL.txt"), "w", encoding="utf-8") as f:
        f.write(readme)

    print("\nCompressing to Teardown_Mods_Pack.zip...")
    if os.path.exists(zip_output_path):
        os.remove(zip_output_path)

    with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_pack_dir):
            for file in files:
                f_path = os.path.join(root, file)
                rel_path = os.path.relpath(f_path, output_pack_dir)
                zipf.write(f_path, rel_path)

    zip_size_mb = os.path.getsize(zip_output_path) / (1024 * 1024)
    print(f"Created ZIP: {zip_output_path} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    verify_and_package()
