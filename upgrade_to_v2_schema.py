import os
import xml.etree.ElementTree as ET

game_mods_dir = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods"
doc_mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")

custom_mod_folders = [
    "Airstrike_Radio_Beacon",
    "BBQ Blowtorch New Model-65-New-1604795432",
    "BIG_MAP_Mega_Airport_Terminal",
    "BIG_MAP_Military_Bunker_Base",
    "BIG_MAP_Suburban_Shopping_Mall",
    "Black_Hole_Cannon",
    "Boeing 737 Burning Edition 486 1 2026-08-30T15-28Z KRYbzsnBW",
    "Cluster_Bomb_Launcher",
    "Gwel's High Building-382-1-1727573253",
    "Hyper_Precision_Railgun",
    "Megacity_Downtown_Towers",
    "Mega_Gun On Steroids-427-0-1-0-1758827703",
    "Mega_Suspension_Bridge",
    "Mossberg 590 Vox-14-1-0-1604432126",
    "Orbital_Laser_Cannon",
    "Plasma_Disintegrator_Cannon",
    "Sandbox_Destruction_Arena",
    "Screen Recorder Copy",
    "Thor_Mjolnir_Lightning",
    "WWII German Weapons Mod for Teardown-4-V1-0-1604195964"
]

def upgrade_schema(target_dir):
    print(f"Upgrading info.txt to Teardown v2 schema in {target_dir}...")
    for folder in custom_mod_folders:
        f_path = os.path.join(target_dir, folder)
        if not os.path.exists(f_path):
            continue
            
        info_file = os.path.join(f_path, "info.txt")
        is_map = "main.xml" in os.listdir(f_path)
        clean_name = folder.replace("_", " ").replace("-", " ").title()
        
        info_content = f"""en_name = {clean_name}
author = Antigravity & Modder
en_description = Custom {'Map' if is_map else 'Weapon'} Mod for Teardown.
tags = {'Map, Sandbox, Multiplayer' if is_map else 'Tool, Global, Multiplayer'}
version = 2
"""
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(info_content)
        print(f"Upgraded info.txt for {folder}")

def update_mods_xml():
    if os.path.exists(appdata_mods_xml):
        print("Updating mods.xml with builtin and local mod IDs...")
        tree = ET.parse(appdata_mods_xml)
        root = tree.getroot()
        
        existing_ids = {m.attrib.get("id"): m for m in root.findall("mod")}
        
        for folder in custom_mod_folders:
            slug = folder.lower().replace("_", "-").replace(" ", "-").replace("'", "")
            ids_to_add = [f"local-{slug}", f"builtin-{slug}", f"local-{folder}", f"builtin-{folder}"]
            
            for mod_id in ids_to_add:
                if mod_id in existing_ids:
                    existing_ids[mod_id].set("active", "true")
                    existing_ids[mod_id].set("shown", "true")
                else:
                    elem = ET.SubElement(root, "mod")
                    elem.set("id", mod_id)
                    elem.set("active", "true")
                    elem.set("shown", "true")
                    
        tree.write(appdata_mods_xml, encoding="utf-8", xml_declaration=True)
        print("Updated mods.xml successfully!")

if __name__ == "__main__":
    upgrade_schema(game_mods_dir)
    upgrade_schema(doc_mods_dir)
    update_mods_xml()
