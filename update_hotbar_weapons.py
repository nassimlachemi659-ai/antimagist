import os

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")

weapon_configs = [
    ("Orbital_Laser_Cannon", "orbitallaser", "Orbital Laser Cannon", "tools/shotgun.vox", 1),
    ("Black_Hole_Cannon", "blackhole", "Black Hole Cannon", "tools/shotgun.vox", 2),
    ("Airstrike_Radio_Beacon", "airstrike", "Airstrike Beacon", "tools/spraycan.vox", 3),
    ("Thor_Mjolnir_Lightning", "thorhammer", "Thor Lightning Hammer", "tools/sledge.vox", 4),
    ("Plasma_Disintegrator_Cannon", "plasmacannon", "Plasma Disintegrator", "tools/shotgun.vox", 5),
    ("Cluster_Bomb_Launcher", "clusterbomb", "Cluster Bomb Launcher", "tools/rocket.vox", 6),
    ("Hyper_Precision_Railgun", "railgun", "Hyper Precision Railgun", "tools/shotgun.vox", 1)
]

def update_lua_weapons():
    print("Updating weapon mods to bind directly to hotbar keys 1, 2, 3, 4, 5, 6...")
    for folder, tool_id, name, vox, group in weapon_configs:
        lua_path = os.path.join(mods_dir, folder, "main.lua")
        if os.path.exists(lua_path):
            with open(lua_path, "r") as f:
                content = f.read()
            
            # Update RegisterTool call with group integer
            old_reg = f'RegisterTool("{tool_id}", "{name}", "{vox}")'
            new_reg = f'RegisterTool("{tool_id}", "{name}", "{vox}", {group})\n\tSetBool("game.tool.{tool_id}.enabled", true)\n\tSetInt("game.tool.{tool_id}.ammo", 999)'
            
            if old_reg in content:
                content = content.replace(old_reg, new_reg)
                with open(lua_path, "w") as f:
                    f.write(content)
                print(f"Updated {tool_id} -> Group {group} (Hotbar key {group})")

if __name__ == "__main__":
    update_lua_weapons()
