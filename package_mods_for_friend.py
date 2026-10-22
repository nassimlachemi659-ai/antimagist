import os
import shutil
import zipfile

s_mods = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods"
desktop = os.path.expanduser("~/Desktop")
output_pack_dir = os.path.join(desktop, "Teardown_Mods_Pack_For_Friend")
zip_output_path = os.path.join(desktop, "Teardown_Mods_Pack.zip")

mods_to_package = [
    "Boeing_737_Burning_Edition",
    "Gwels_High_Skyscraper",
    "Mega_Destruction_Metropolis",
    "Orbital_Laser_Strike",
    "Black_Hole_Singularity",
    "Mjolnir_Thunder_Hammer",
    "Hyper_Precision_Railgun"
]

def package_mods():
    print("Creating mods pack folder on Desktop...")
    if os.path.exists(output_pack_dir):
        shutil.rmtree(output_pack_dir)
    os.makedirs(output_pack_dir, exist_ok=True)

    # Copy all 7 mods
    for mod_name in mods_to_package:
        src = os.path.join(s_mods, mod_name)
        dst = os.path.join(output_pack_dir, mod_name)
        if os.path.exists(src):
            shutil.copytree(src, dst)
            print(f" - Copied {mod_name}")
        else:
            print(f" - Warning: missing {mod_name}")

    # Create README instructions for friend
    readme_content = """==============================================
TEARDOWN WORKING MODS PACK (WEAPONS & MAPS)
==============================================

INCLUDED MODS:
1. Boeing 737 Burning Edition (Map - Burning Airplane)
2. Gwel's High Skyscraper (Map - 5-Story Glass Office Building)
3. Mega Destruction Metropolis (Map - Huge Urban City Sandbox)
4. Orbital Laser Strike (Weapon - Laser Beam [LMB] & Ion Nuke [RMB])
5. Black Hole Singularity Cannon (Weapon - Gravitational Implosion)
6. Mjolnir Thunder Hammer (Weapon - Lightning Shockwave Hammer)
7. Hyper Precision Railgun (Weapon - 120m Armor Piercing Kinetic Slug)

----------------------------------------------
HOW TO INSTALL FOR YOUR FRIEND:
----------------------------------------------
METHOD 1 (Recommended):
Copy all 7 folders into your Teardown game mods directory:
Example:
- If cracked / Online-Fix: YourTeardownFolder\\mods\\
- If standard Steam: C:\\Users\\<YourName>\\Documents\\Teardown\\mods\\

METHOD 2:
Go to Documents -> Teardown -> mods, and paste all 7 folders there.

----------------------------------------------
HOW TO PLAY IN-GAME:
----------------------------------------------
1. Launch Teardown.
2. Go to Main Menu -> MODS.
3. Maps: Click on any map (Boeing 737, Skyscraper, Metropolis) and click PLAY!
4. Weapons: In any map or multiplayer match, press keys 1, 2, 3, 4 or scroll your Mouse Wheel to equip and destroy!
==============================================
"""
    readme_path = os.path.join(output_pack_dir, "HOW_TO_INSTALL.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Created HOW_TO_INSTALL.txt")

    # Create ZIP archive
    print("\nCreating ZIP file for easy sharing...")
    if os.path.exists(zip_output_path):
        os.remove(zip_output_path)

    with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_pack_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, output_pack_dir)
                zipf.write(file_path, rel_path)

    zip_size_mb = os.path.getsize(zip_output_path) / (1024 * 1024)
    print(f"Successfully generated ZIP: {zip_output_path} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    package_mods()
