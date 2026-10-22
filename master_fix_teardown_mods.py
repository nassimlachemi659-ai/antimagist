import os
import shutil
import xml.etree.ElementTree as ET

s_game_dir = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown"
s_mods_dir = os.path.join(s_game_dir, "mods")
doc_mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")
data_vox_tool = os.path.join(s_game_dir, "data", "vox", "tool")

# 1. Clean up old dummy / broken mod folders from both directories
dummy_folders_to_remove = [
    "Airstrike_Radio_Beacon",
    "BIG_MAP_Mega_Airport_Terminal",
    "BIG_MAP_Military_Bunker_Base",
    "BIG_MAP_Suburban_Shopping_Mall",
    "Black_Hole_Cannon",
    "Cluster_Bomb_Launcher",
    "Hyper_Precision_Railgun",
    "Megacity_Downtown_Towers",
    "Mega_Suspension_Bridge",
    "Orbital_Laser_Cannon",
    "Plasma_Disintegrator_Cannon",
    "Sandbox_Destruction_Arena",
    "Screen Recorder Copy",
    "Thor_Mjolnir_Lightning",
    "BBQ Blowtorch New Model-65-New-1604795432",
    "Mossberg 590 Vox-14-1-0-1604432126",
    "WWII German Weapons Mod for Teardown-4-V1-0-1604195964",
    "Mega_Gun On Steroids-427-0-1-0-1758827703"
]

def clean_old():
    print("--- 1. Cleaning up broken / dummy mod folders ---")
    for f in dummy_folders_to_remove:
        p1 = os.path.join(s_mods_dir, f)
        p2 = os.path.join(doc_mods_dir, f)
        if os.path.exists(p1):
            shutil.rmtree(p1, ignore_errors=True)
            print(f"Removed from S: {f}")
        if os.path.exists(p2):
            shutil.rmtree(p2, ignore_errors=True)
            print(f"Removed from Documents: {f}")

def fix_boeing_737(target_parent):
    print("--- 2. Fixing Boeing 737 Burning Edition ---")
    b_dir = os.path.join(target_parent, "Boeing_737_Burning_Edition")
    old_b = os.path.join(target_parent, "Boeing 737 Burning Edition 486 1 2026-08-30T15-28Z KRYbzsnBW")
    if os.path.exists(old_b) and not os.path.exists(b_dir):
        os.rename(old_b, b_dir)
    elif not os.path.exists(b_dir) and os.path.exists(old_b):
        b_dir = old_b

    if os.path.exists(b_dir):
        # 1. Update info.txt
        info_path = os.path.join(b_dir, "info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write("""en_name = Boeing 737 Burning Edition
author = Serenity & AlexVeeBee
en_description = High-detail burning and destroyed passenger Boeing 737 airplane map.
tags = Map
version = 2
""")
        # 2. Make map.xml the main playable level
        map_xml = os.path.join(b_dir, "map.xml")
        main_xml = os.path.join(b_dir, "main.xml")
        menu_scene = os.path.join(b_dir, "menu_scene.xml")
        if os.path.exists(map_xml):
            if not os.path.exists(menu_scene) and os.path.exists(main_xml):
                shutil.copyfile(main_xml, menu_scene)
            shutil.copyfile(map_xml, main_xml)
            print("Set map.xml as main.xml in Boeing 737 for direct spawning!")

        # 3. Neutralize version check in main.lua so it never kicks player out
        main_lua = os.path.join(b_dir, "main.lua")
        with open(main_lua, "w", encoding="utf-8") as f:
            f.write("""function init()
    SetBool('map.version.outdated', false)
end

function tick()
    SetBool('map.version.outdated', false)
end
""")
        print("Fixed Boeing 737 scripts!")

def fix_gwel_skyscraper(target_parent):
    print("--- 3. Fixing Gwel High Skyscraper ---")
    g_dir = os.path.join(target_parent, "Gwels_High_Skyscraper")
    old_g = os.path.join(target_parent, "Gwel's High Building-382-1-1727573253")
    if os.path.exists(old_g) and not os.path.exists(g_dir):
        os.rename(old_g, g_dir)
    elif not os.path.exists(g_dir) and os.path.exists(old_g):
        g_dir = old_g

    if os.path.exists(g_dir):
        # 1. Update info.txt
        info_path = os.path.join(g_dir, "info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write("""en_name = Gwel's High Skyscraper
author = Gwel
en_description = Massive 5-story modern office skyscraper with glass facade, furniture, and destructible pillars.
tags = Map
version = 2
""")
        # 2. Replace empty main.xml with the real Normal.xml (4100-line building)
        normal_xml = os.path.join(g_dir, "Normal.xml")
        main_xml = os.path.join(g_dir, "main.xml")
        if os.path.exists(normal_xml):
            shutil.copyfile(normal_xml, main_xml)
            print("Set Normal.xml as main.xml in Gwel Skyscraper for direct spawning!")

def create_mega_destruction_map(target_parent):
    print("--- 4. Creating Mega Destruction City Map ---")
    map_dir = os.path.join(target_parent, "Mega_Destruction_Metropolis")
    os.makedirs(map_dir, exist_ok=True)
    
    with open(os.path.join(map_dir, "info.txt"), "w", encoding="utf-8") as f:
        f.write("""en_name = Mega Destruction Metropolis
author = Antigravity
en_description = Huge destructible urban sandbox with skyscrapers, warehouses, and fuel tanks!
tags = Map
version = 2
""")

    # Valid Teardown XML Scene syntax (voxbox size in decimeters / voxels: 10 = 1m)
    scene_xml = """<scene version="3" shadowVolume="300 120 300">
	<environment template="sunny" skyboxrot="45"/>
	
	<!-- Ground Plate (300m x 300m) -->
	<voxbox pos="-150.0 0.0 -150.0" size="3000 2 3000" texture="1" color="0.25 0.25 0.25"/>

	<!-- Player Spawn -->
	<spawnpoint pos="0.0 1.2 50.0" rot="0.0 180.0 0.0"/>

	<!-- Boundary -->
	<boundary>
		<vertex pos="-145.0 -145.0"/>
		<vertex pos="145.0 -145.0"/>
		<vertex pos="145.0 145.0"/>
		<vertex pos="-145.0 145.0"/>
	</boundary>

	<!-- Standard sandbox scripts -->
	<script file="main.lua"/>
	<script file="sandbox.lua"/>

	<!-- SKYSCRAPER 1: Concrete & Glass Tower (60m tall) -->
	<group pos="-40.0 0.2 -30.0">
		<voxbox pos="-12.0 0.0 -12.0" size="240 600 240" material="concrete" color="0.8 0.8 0.8"/>
		<voxbox pos="-10.0 20.0 -10.0" size="200 550 200" material="glass" color="0.2 0.6 0.9"/>
	</group>

	<!-- SKYSCRAPER 2: Brick Office Tower (50m tall) -->
	<group pos="40.0 0.2 -30.0">
		<voxbox pos="-12.0 0.0 -12.0" size="240 500 240" material="brick" color="0.7 0.3 0.2"/>
	</group>

	<!-- WAREHOUSE: Metal & Wood Building (15m tall) -->
	<group pos="0.0 0.2 -80.0">
		<voxbox pos="-30.0 0.0 -20.0" size="600 150 400" material="metal" color="0.6 0.65 0.7"/>
	</group>

	<!-- SUSPENSION BRIDGE HIGHWAY -->
	<group pos="0.0 0.2 0.0">
		<!-- Road deck -->
		<voxbox pos="-100.0 8.0 -5.0" size="2000 15 100" material="concrete" color="0.3 0.3 0.3"/>
		<!-- Pillars -->
		<voxbox pos="-40.0 0.0 -4.0" size="40 300 80" material="concrete" color="0.7 0.7 0.7"/>
		<voxbox pos="40.0 0.0 -4.0" size="40 300 80" material="concrete" color="0.7 0.7 0.7"/>
	</group>
</scene>
"""
    with open(os.path.join(map_dir, "main.xml"), "w", encoding="utf-8") as f:
        f.write(scene_xml)
    print("Created Mega Destruction Metropolis map!")

def create_custom_weapons(target_parent):
    print("--- 5. Creating 4 Real Teardown v2 Weapons ---")

    # WEAPON 1: Orbital Laser Strike
    w1_dir = os.path.join(target_parent, "Orbital_Laser_Strike")
    os.makedirs(os.path.join(w1_dir, "vox"), exist_ok=True)
    if os.path.exists(os.path.join(data_vox_tool, "rifle.vox")):
        shutil.copyfile(os.path.join(data_vox_tool, "rifle.vox"), os.path.join(w1_dir, "vox", "weapon.vox"))

    with open(os.path.join(w1_dir, "info.txt"), "w", encoding="utf-8") as f:
        f.write("""en_name = Orbital Laser Strike
author = Antigravity
en_description = High-intensity laser beam [LMB] and Orbital Ion Nuke from the sky [RMB]!
tags = Tool, Global, Multiplayer
version = 2
""")

    with open(os.path.join(w1_dir, "main.lua"), "w", encoding="utf-8") as f:
        f.write("""#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("orbitallaser", "Orbital Laser Strike", "MOD/vox/weapon.vox", 1)
	SetToolAmmoPickupAmount("orbitallaser", 100)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("orbitallaser", true, p)
		SetToolAmmo("orbitallaser", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "orbitallaser" and GetPlayerVehicle(p) == 0 then
			local t = GetPlayerCameraTransform(p)
			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
			local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, 500)

			-- Left Click: Continuous Laser Beam
			if InputDown("usetool", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				MakeHole(hitPos, 3.5, 3.0, 2.0)
				Explosion(hitPos, 2.5)
				PointLight(hitPos, 0.2, 0.8, 1.0, 10.0)
			end

			-- Right Click: Orbital Ion Nuke
			if InputPressed("grab", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				for y = 50, 0, -5 do
					local skyP = VecAdd(hitPos, Vec(0, y, 0))
					PointLight(skyP, 1.0, 0.4, 0.1, 15.0)
					MakeHole(skyP, 4.0, 3.0, 2.0)
				end
				Explosion(hitPos, 12.0)
				for i = 1, 8 do
					local off = Vec(math.random(-4, 4), math.random(0, 3), math.random(-4, 4))
					Explosion(VecAdd(hitPos, off), 6.0)
				end
			end
		end
	end
end
""")
    print("Created Orbital Laser Strike!")

    # WEAPON 2: Black Hole Singularity Cannon
    w2_dir = os.path.join(target_parent, "Black_Hole_Singularity")
    os.makedirs(os.path.join(w2_dir, "vox"), exist_ok=True)
    if os.path.exists(os.path.join(data_vox_tool, "rocket.vox")):
        shutil.copyfile(os.path.join(data_vox_tool, "rocket.vox"), os.path.join(w2_dir, "vox", "weapon.vox"))

    with open(os.path.join(w2_dir, "info.txt"), "w", encoding="utf-8") as f:
        f.write("""en_name = Black Hole Singularity Cannon
author = Antigravity
en_description = Gravitational vortex that pulls in and implodes buildings into a singularity!
tags = Tool, Global, Multiplayer
version = 2
""")

    with open(os.path.join(w2_dir, "main.lua"), "w", encoding="utf-8") as f:
        f.write("""#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("blackhole", "Black Hole Cannon", "MOD/vox/weapon.vox", 2)
	SetToolAmmoPickupAmount("blackhole", 50)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("blackhole", true, p)
		SetToolAmmo("blackhole", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "blackhole" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				local hit, dist = QueryRaycast(t.pos, fwd, 500)
				if hit then
					local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
					for r = 2, 12, 2 do
						MakeHole(hitPos, r, r - 0.5, r - 1.0)
						PointLight(hitPos, 0.1, 0.0, 0.5, 20.0)
					end
					Explosion(hitPos, 9.0)
				end
			end
		end
	end
end
""")
    print("Created Black Hole Singularity Cannon!")

    # WEAPON 3: Mjolnir Thunder Hammer
    w3_dir = os.path.join(target_parent, "Mjolnir_Thunder_Hammer")
    os.makedirs(os.path.join(w3_dir, "vox"), exist_ok=True)
    if os.path.exists(os.path.join(data_vox_tool, "sledge.vox")):
        shutil.copyfile(os.path.join(data_vox_tool, "sledge.vox"), os.path.join(w3_dir, "vox", "weapon.vox"))

    with open(os.path.join(w3_dir, "info.txt"), "w", encoding="utf-8") as f:
        f.write("""en_name = Mjolnir Thunder Hammer
author = Antigravity
en_description = Godly warhammer that unleashes lightning shockwaves on impact!
tags = Tool, Global, Multiplayer
version = 2
""")

    with open(os.path.join(w3_dir, "main.lua"), "w", encoding="utf-8") as f:
        f.write("""#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("mjolnir", "Mjolnir Thunder Hammer", "MOD/vox/weapon.vox", 3)
	SetToolAmmoPickupAmount("mjolnir", 50)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("mjolnir", true, p)
		SetToolAmmo("mjolnir", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "mjolnir" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				local hit, dist = QueryRaycast(t.pos, fwd, 500)
				if hit then
					local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
					for y = 0, 45, 5 do
						local pPos = VecAdd(hitPos, Vec(0, y, 0))
						PointLight(pPos, 0.4, 0.8, 1.0, 12.0)
						MakeHole(pPos, 4.0, 3.0, 2.0)
					end
					Explosion(hitPos, 8.0)
					SpawnFire(hitPos)
				end
			end
		end
	end
end
""")
    print("Created Mjolnir Thunder Hammer!")

    # WEAPON 4: Hyper Precision Railgun
    w4_dir = os.path.join(target_parent, "Hyper_Precision_Railgun")
    os.makedirs(os.path.join(w4_dir, "vox"), exist_ok=True)
    if os.path.exists(os.path.join(data_vox_tool, "shotgun.vox")):
        shutil.copyfile(os.path.join(data_vox_tool, "shotgun.vox"), os.path.join(w4_dir, "vox", "weapon.vox"))

    with open(os.path.join(w4_dir, "info.txt"), "w", encoding="utf-8") as f:
        f.write("""en_name = Hyper Precision Railgun
author = Antigravity
en_description = High-velocity kinetic slug that pierces straight through 120m of reinforced structures!
tags = Tool, Global, Multiplayer
version = 2
""")

    with open(os.path.join(w4_dir, "main.lua"), "w", encoding="utf-8") as f:
        f.write("""#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("railgun", "Hyper Precision Railgun", "MOD/vox/weapon.vox", 4)
	SetToolAmmoPickupAmount("railgun", 50)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("railgun", true, p)
		SetToolAmmo("railgun", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "railgun" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				for step = 1, 120, 2 do
					local pPos = VecAdd(t.pos, VecScale(fwd, step))
					MakeHole(pPos, 3.0, 2.5, 2.0)
					PointLight(pPos, 1.0, 0.8, 0.2, 5.0)
				end
				Explosion(VecAdd(t.pos, VecScale(fwd, 40)), 6.0)
			end
		end
	end
end
""")
    print("Created Hyper Precision Railgun!")

def update_registry():
    print("--- 6. Updating mods.xml Registry ---")
    if os.path.exists(appdata_mods_xml):
        tree = ET.parse(appdata_mods_xml)
        root = tree.getroot()
        
        # Keep builtins
        active_ids = [
            "local-boeing-737-burning-edition",
            "local-gwels-high-skyscraper",
            "local-mega-destruction-metropolis",
            "local-orbital-laser-strike",
            "local-black-hole-singularity",
            "local-mjolnir-thunder-hammer",
            "local-hyper-precision-railgun"
        ]
        
        existing = {m.attrib.get("id"): m for m in root.findall("mod")}
        for aid in active_ids:
            if aid in existing:
                existing[aid].set("active", "true")
                existing[aid].set("shown", "true")
            else:
                elem = ET.SubElement(root, "mod")
                elem.set("id", aid)
                elem.set("active", "true")
                elem.set("shown", "true")
                
        tree.write(appdata_mods_xml, encoding="utf-8", xml_declaration=True)
        print("Updated mods.xml successfully!")

def sync_to_game():
    print("--- 7. Syncing verified mods from Documents to Game Folder ---")
    valid_folders = [
        "Boeing_737_Burning_Edition",
        "Gwels_High_Skyscraper",
        "Mega_Destruction_Metropolis",
        "Orbital_Laser_Strike",
        "Black_Hole_Singularity",
        "Mjolnir_Thunder_Hammer",
        "Hyper_Precision_Railgun"
    ]
    for vf in valid_folders:
        src = os.path.join(doc_mods_dir, vf)
        dst = os.path.join(s_mods_dir, vf)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Synced to Game Directory: {vf}")

if __name__ == "__main__":
    clean_old()
    fix_boeing_737(doc_mods_dir)
    fix_gwel_skyscraper(doc_mods_dir)
    create_mega_destruction_map(doc_mods_dir)
    create_custom_weapons(doc_mods_dir)
    update_registry()
    sync_to_game()
    print("\nALL TASKS COMPLETED SUCCESSFULLY!")
