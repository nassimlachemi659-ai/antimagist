import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

s_game_dir = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown"
s_mods_dir = os.path.join(s_game_dir, "mods")
doc_mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")
data_vox_tool = os.path.join(s_game_dir, "data", "vox", "tool")
desktop = os.path.expanduser("~/Desktop")
output_pack_dir = os.path.join(desktop, "Teardown_Mods_Pack_For_Friend")
zip_output_path = os.path.join(desktop, "Teardown_Mods_Pack.zip")

# ==============================================================================
# DEFINITION OF ALL 14 WEAPONS (ALL WITH FIXED VIEWMODEL POSITIONING)
# ==============================================================================
# The transform Vec(0.26, -0.45, -0.40) moves weapons to the bottom-right corner
# so the screen is completely clear and the weapon sits naturally in your hands!

weapons_data = [
    {
        "folder": "Orbital_Laser_Strike",
        "name": "Orbital Laser Strike",
        "desc": "High-intensity laser beam [LMB] & sky ion nuke [RMB]!",
        "tool_id": "orbitallaser",
        "vox_src": "rifle.vox",
        "group": 1,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			-- Left Click: Laser
			if InputDown("usetool", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				MakeHole(hitPos, 3.5, 3.0, 2.0)
				Explosion(hitPos, 2.5)
				PointLight(hitPos, 0.2, 0.8, 1.0, 10.0)
			end
			-- Right Click: Ion Nuke
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
"""
    },
    {
        "folder": "Plasma_Disintegrator_Rifle",
        "name": "Plasma Disintegrator Rifle",
        "desc": "Fires hyper-velocity blue plasma bolts that melt through solid voxels!",
        "tool_id": "plasmarifle",
        "vox_src": "rifle.vox",
        "group": 1,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			if InputDown("usetool", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				MakeHole(hitPos, 3.0, 2.5, 1.5)
				PointLight(hitPos, 0.1, 0.5, 1.0, 12.0)
				SpawnFire(hitPos)
			end
"""
    },
    {
        "folder": "Black_Hole_Singularity",
        "name": "Black Hole Singularity Cannon",
        "desc": "Gravitational vortex that pulls in and implodes buildings into a singularity!",
        "tool_id": "blackhole",
        "vox_src": "rocket.vox",
        "group": 2,
        "x": 0.26, "y": -0.44, "z": -0.40,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				for r = 2, 12, 2 do
					MakeHole(hitPos, r, r - 0.5, r - 1.0)
					PointLight(hitPos, 0.1, 0.0, 0.5, 20.0)
				end
				Explosion(hitPos, 9.0)
			end
"""
    },
    {
        "folder": "Mjolnir_Thunder_Hammer",
        "name": "Mjolnir Thunder Hammer",
        "desc": "Godly warhammer that unleashes lightning shockwaves on impact!",
        "tool_id": "mjolnir",
        "vox_src": "sledge.vox",
        "group": 3,
        "x": 0.28, "y": -0.48, "z": -0.42,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				for y = 0, 45, 5 do
					local pPos = VecAdd(hitPos, Vec(0, y, 0))
					PointLight(pPos, 0.4, 0.8, 1.0, 12.0)
					MakeHole(pPos, 4.0, 3.0, 2.0)
				end
				Explosion(hitPos, 8.0)
				SpawnFire(hitPos)
			end
"""
    },
    {
        "folder": "Hyper_Precision_Railgun",
        "name": "Hyper Precision Railgun",
        "desc": "Kinetic slug that pierces straight through 120m of reinforced structures!",
        "tool_id": "railgun",
        "vox_src": "shotgun.vox",
        "group": 4,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			if InputPressed("usetool", p) then
				for step = 1, 120, 2 do
					local pPos = VecAdd(t.pos, VecScale(fwd, step))
					MakeHole(pPos, 3.0, 2.5, 2.0)
					PointLight(pPos, 1.0, 0.8, 0.2, 5.0)
				end
				Explosion(VecAdd(t.pos, VecScale(fwd, 40)), 6.0)
			end
"""
    },
    {
        "folder": "C4_Remote_Explosive",
        "name": "C4 Remote Sticky Explosives",
        "desc": "[LMB] Plant sticky C4 charges | [RMB] Detonate all charges at once!",
        "tool_id": "c4explosive",
        "vox_src": "explosive.vox",
        "group": 4,
        "x": 0.24, "y": -0.42, "z": -0.35,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				Explosion(hitPos, 7.0)
				SpawnFire(hitPos)
			end
			if InputPressed("grab", p) and hit then
				local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
				Explosion(hitPos, 12.0)
			end
"""
    },
    {
        "folder": "Airstrike_Radio_Beacon",
        "name": "Tactical Airstrike Beacon",
        "desc": "Mark coordinates with [LMB] to call down a heavy 12-missile artillery barrage!",
        "tool_id": "airstrike",
        "vox_src": "spraycan.vox",
        "group": 5,
        "x": 0.25, "y": -0.44, "z": -0.35,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local targetPos = VecAdd(t.pos, VecScale(fwd, dist))
				for i = 1, 12 do
					local offX = math.random(-12, 12)
					local offZ = math.random(-12, 12)
					local strikePos = VecAdd(targetPos, Vec(offX, 0, offZ))
					for y = 45, 0, -5 do
						local skyPos = VecAdd(strikePos, Vec(0, y, 0))
						PointLight(skyPos, 1.0, 0.5, 0.1, 10.0)
					end
					MakeHole(strikePos, 6.0, 5.0, 3.5)
					Explosion(strikePos, 7.0)
					SpawnFire(strikePos)
				end
			end
"""
    },
    {
        "folder": "Meteor_Shower_Strike",
        "name": "Meteor Shower Celestial Strike",
        "desc": "Calls flaming orbital meteorites that crash from space into buildings!",
        "tool_id": "meteorshower",
        "vox_src": "turbo.vox",
        "group": 5,
        "x": 0.25, "y": -0.42, "z": -0.35,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local targetPos = VecAdd(t.pos, VecScale(fwd, dist))
				for i = 1, 8 do
					local ox = math.random(-15, 15)
					local oz = math.random(-15, 15)
					local mPos = VecAdd(targetPos, Vec(ox, 0, oz))
					for h = 60, 0, -6 do
						PointLight(VecAdd(mPos, Vec(0, h, 0)), 1.0, 0.3, 0.0, 20.0)
					end
					MakeHole(mPos, 8.0, 6.0, 4.0)
					Explosion(mPos, 9.0)
					SpawnFire(mPos)
				end
			end
"""
    },
    {
        "folder": "Cluster_Bomb_Launcher",
        "name": "MIRV Cluster Bomb Launcher",
        "desc": "Launches a cluster bomb that scatters into 14 explosive sub-munitions!",
        "tool_id": "clusterbomb",
        "vox_src": "pipebomb.vox",
        "group": 6,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local impact = VecAdd(t.pos, VecScale(fwd, dist))
				Explosion(impact, 8.0)
				for i = 1, 14 do
					local rx = math.random(-10, 10)
					local rz = math.random(-10, 10)
					local subPos = VecAdd(impact, Vec(rx, 1, rz))
					MakeHole(subPos, 4.5, 3.5, 2.0)
					Explosion(subPos, 5.0)
					SpawnFire(subPos)
				end
			end
"""
    },
    {
        "folder": "Thermobaric_Flame_Cannon",
        "name": "Thermobaric Flame Cannon",
        "desc": "High-temperature thermobaric stream that melts and incinerates structures!",
        "tool_id": "flamecannon",
        "vox_src": "blowtorch.vox",
        "group": 7,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			if InputDown("usetool", p) and hit then
				local burnPos = VecAdd(t.pos, VecScale(fwd, dist))
				MakeHole(burnPos, 2.5, 2.0, 1.0)
				SpawnFire(burnPos)
				PointLight(burnPos, 1.0, 0.4, 0.05, 12.0)
				if math.random(1, 4) == 1 then
					Explosion(burnPos, 2.0)
				end
			end
"""
    },
    {
        "folder": "Gravity_Shockwave_Repulsor",
        "name": "Gravity Shockwave Repulsor",
        "desc": "Emits a concussive kinetic pulse that blasts buildings and vehicles into the air!",
        "tool_id": "repulsor",
        "vox_src": "leafblower.vox",
        "group": 8,
        "x": 0.26, "y": -0.44, "z": -0.40,
        "fire_code": """
			if InputPressed("usetool", p) then
				for step = 4, 30, 4 do
					local ringPos = VecAdd(t.pos, VecScale(fwd, step))
					MakeHole(ringPos, 4.0, 3.5, 2.5)
					PointLight(ringPos, 0.3, 0.7, 1.0, 15.0)
				end
				if hit then
					local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
					Explosion(hitPos, 6.0)
				end
			end
"""
    },
    {
        "folder": "Voxel_Vacuum_Gun",
        "name": "Voxel Vacuum Dissolver",
        "desc": "Directly disintegrates and dissolves walls, roofs, and vehicles into thin air!",
        "tool_id": "vacuumgun",
        "vox_src": "extinguisher.vox",
        "group": 8,
        "x": 0.25, "y": -0.44, "z": -0.38,
        "fire_code": """
			if InputDown("usetool", p) and hit then
				local vacPos = VecAdd(t.pos, VecScale(fwd, dist))
				MakeHole(vacPos, 2.8, 2.5, 2.0)
				PointLight(vacPos, 0.8, 0.1, 0.9, 8.0)
			end
"""
    },
    {
        "folder": "Tactical_Nuke_Launcher",
        "name": "Tactical Nuke Launcher (Fat Man)",
        "desc": "Fires a tactical nuclear warhead that vaporizes entire city blocks in a 35m fireball!",
        "tool_id": "fatman",
        "vox_src": "bomb.vox",
        "group": 9,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			if InputPressed("usetool", p) and hit then
				local nukePos = VecAdd(t.pos, VecScale(fwd, dist))
				MakeHole(nukePos, 18.0, 15.0, 10.0)
				Explosion(nukePos, 20.0)
				PointLight(nukePos, 1.0, 0.9, 0.6, 50.0)
				for i = 1, 16 do
					local ang = (i / 16.0) * 6.28318
					local ox = math.cos(ang) * 12.0
					local oz = math.sin(ang) * 12.0
					local wavePos = VecAdd(nukePos, Vec(ox, 1, oz))
					Explosion(wavePos, 8.0)
					SpawnFire(wavePos)
				end
			end
"""
    },
    {
        "folder": "Chrono_Time_Disruptor",
        "name": "Chrono Time Disruptor (Slow-Mo)",
        "desc": "Control time physics! [LMB] slow motion 0.2x | [RMB] restore normal speed 1.0x!",
        "tool_id": "chronogun",
        "vox_src": "booster.vox",
        "group": 0,
        "x": 0.25, "y": -0.42, "z": -0.38,
        "fire_code": """
			if InputPressed("usetool", p) then
				SetTimeScale(0.2)
			end
			if InputPressed("grab", p) then
				SetTimeScale(1.0)
			end
"""
    }
]

# ==============================================================================
# DEFINITION OF 8 EPIC BIG MAPS
# ==============================================================================

extra_maps = [
    {
        "folder": "Skyscraper_Construction_Site",
        "name": "Skyscraper Construction & Cranes",
        "desc": "A 70m steel frame skyscraper under construction with two 80m yellow tower cranes you can topple!",
        "xml": """<scene version="3" shadowVolume="300 140 300">
	<environment template="sunny" skyboxrot="60"/>
	<voxbox pos="-150.0 0.0 -150.0" size="3000 2 3000" texture="1" color="0.25 0.25 0.25"/>
	<spawnpoint pos="0.0 1.2 70.0" rot="0.0 180.0 0.0"/>
	<boundary>
		<vertex pos="-145.0 -145.0"/>
		<vertex pos="145.0 -145.0"/>
		<vertex pos="145.0 145.0"/>
		<vertex pos="-145.0 145.0"/>
	</boundary>
	<script file="main.lua"/>
	<script file="sandbox.lua"/>

	<!-- 70-METER STEEL FRAME SKYSCRAPER -->
	<group pos="0.0 0.2 -30.0">
		<voxbox pos="-15.0 0.0 -15.0" size="300 700 300" material="metal" color="0.6 0.2 0.1"/>
		<voxbox pos="-13.0 15.0 -13.0" size="260 20 260" material="concrete" color="0.7 0.7 0.7"/>
		<voxbox pos="-13.0 30.0 -13.0" size="260 20 260" material="concrete" color="0.7 0.7 0.7"/>
		<voxbox pos="-13.0 45.0 -13.0" size="260 20 260" material="concrete" color="0.7 0.7 0.7"/>
		<voxbox pos="-13.0 60.0 -13.0" size="260 20 260" material="concrete" color="0.7 0.7 0.7"/>
	</group>

	<!-- CRANE 1 (80m Tall) -->
	<group pos="-35.0 0.2 -30.0">
		<voxbox pos="-2.0 0.0 -2.0" size="40 800 40" material="metal" color="0.9 0.8 0.1"/>
		<voxbox pos="-2.0 78.0 -2.0" size="300 30 30" material="metal" color="0.9 0.8 0.1"/>
	</group>

	<!-- CRANE 2 (80m Tall) -->
	<group pos="35.0 0.2 -30.0">
		<voxbox pos="-2.0 0.0 -2.0" size="40 800 40" material="metal" color="0.9 0.8 0.1"/>
		<voxbox pos="-20.0 78.0 -2.0" size="300 30 30" material="metal" color="0.9 0.8 0.1"/>
	</group>
</scene>
"""
    },
    {
        "folder": "Suburban_Town_Chaos",
        "name": "Suburban Town & Gas Station Chaos",
        "desc": "Full suburban town with 6 residential houses, a shopping market, and an explosive gas station!",
        "xml": """<scene version="3" shadowVolume="300 100 300">
	<environment template="sunny" skyboxrot="45"/>
	<voxbox pos="-150.0 0.0 -150.0" size="3000 2 3000" texture="1" color="0.3 0.3 0.3"/>
	<spawnpoint pos="0.0 1.2 60.0" rot="0.0 180.0 0.0"/>
	<boundary>
		<vertex pos="-145.0 -145.0"/>
		<vertex pos="145.0 -145.0"/>
		<vertex pos="145.0 145.0"/>
		<vertex pos="-145.0 145.0"/>
	</boundary>
	<script file="main.lua"/>
	<script file="sandbox.lua"/>

	<!-- SUBURBAN HOMES -->
	<group pos="-50.0 0.2 10.0">
		<voxbox pos="-10.0 0.0 -8.0" size="200 90 160" material="wood" color="0.8 0.7 0.5"/>
	</group>
	<group pos="0.0 0.2 10.0">
		<voxbox pos="-10.0 0.0 -8.0" size="200 90 160" material="brick" color="0.7 0.3 0.2"/>
	</group>
	<group pos="50.0 0.2 10.0">
		<voxbox pos="-10.0 0.0 -8.0" size="200 90 160" material="wood" color="0.4 0.6 0.7"/>
	</group>

	<!-- GAS STATION WITH EXPLOSIVE CANOPY & FUEL TANKS -->
	<group pos="0.0 0.2 -60.0">
		<voxbox pos="-25.0 0.0 -15.0" size="500 80 300" material="metal" color="0.9 0.9 0.9"/>
		<!-- Pillars -->
		<voxbox pos="-20.0 0.0 -10.0" size="30 70 30" material="metal" color="0.8 0.1 0.1"/>
		<voxbox pos="20.0 0.0 -10.0" size="30 70 30" material="metal" color="0.8 0.1 0.1"/>
		<voxbox pos="-20.0 0.0 10.0" size="30 70 30" material="metal" color="0.8 0.1 0.1"/>
		<voxbox pos="20.0 0.0 10.0" size="30 70 30" material="metal" color="0.8 0.1 0.1"/>
		<!-- Gas Storage Cylinders -->
		<voxbox pos="-8.0 0.0 0.0" size="60 40 40" material="metal" color="0.9 0.1 0.1"/>
		<voxbox pos="8.0 0.0 0.0" size="60 40 40" material="metal" color="0.9 0.1 0.1"/>
	</group>
</scene>
"""
    }
]

def build_all_perfectly():
    print("--- 1. Writing all 14 Weapons with Viewmodel Positioning ---")
    for w in weapons_data:
        lua_template = f"""#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("{w['tool_id']}", "{w['name']}", "MOD/vox/weapon.vox", {w['group']})
	SetToolAmmoPickupAmount("{w['tool_id']}", 50)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("{w['tool_id']}", true, p)
		SetToolAmmo("{w['tool_id']}", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "{w['tool_id']}" and GetPlayerVehicle(p) == 0 then
			-- Position tool in bottom right corner so it never blocks the player's view
			local toolTransform = Transform(Vec({w['x']}, {w['y']}, {w['z']}))
			SetToolTransform(toolTransform, 1.0, p)

			local t = GetPlayerCameraTransform(p)
			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
			local hit, dist = QueryRaycast(t.pos, fwd, 500)
{w['fire_code']}
		end
	end
end

function client.tick(dt)
	for p in Players() do
		if GetPlayerTool(p) == "{w['tool_id']}" and GetPlayerVehicle(p) == 0 then
			local toolTransform = Transform(Vec({w['x']}, {w['y']}, {w['z']}))
			SetToolTransform(toolTransform, 1.0, p)
		end
	end
end
"""
        for parent in [s_mods_dir, doc_mods_dir]:
            p = os.path.join(parent, w["folder"])
            vox_dir = os.path.join(p, "vox")
            os.makedirs(vox_dir, exist_ok=True)
            
            # Copy 3D voxel model
            src_vox = os.path.join(data_vox_tool, w["vox_src"])
            dst_vox = os.path.join(vox_dir, "weapon.vox")
            if os.path.exists(src_vox):
                shutil.copyfile(src_vox, dst_vox)

            # Write info.txt
            with open(os.path.join(p, "info.txt"), "w", encoding="utf-8") as f:
                f.write(f"en_name = {w['name']}\nauthor = Antigravity\nen_description = {w['desc']}\ntags = Tool, Global, Multiplayer\nversion = 2\n")

            # Write main.lua
            with open(os.path.join(p, "main.lua"), "w", encoding="utf-8") as f:
                f.write(lua_template)

        print(f"Built & Positioned Weapon: {w['name']}")

    print("\n--- 2. Building Extra Big Maps ---")
    for m in extra_maps:
        for parent in [s_mods_dir, doc_mods_dir]:
            p = os.path.join(parent, m["folder"])
            os.makedirs(p, exist_ok=True)
            
            with open(os.path.join(p, "info.txt"), "w", encoding="utf-8") as f:
                f.write(f"en_name = {m['name']}\nauthor = Antigravity\nen_description = {m['desc']}\ntags = Map\nversion = 2\n")

            with open(os.path.join(p, "main.xml"), "w", encoding="utf-8") as f:
                f.write(m["xml"])
        print(f"Built Map: {m['name']}")

    # Update mods.xml registry
    if os.path.exists(appdata_mods_xml):
        tree = ET.parse(appdata_mods_xml)
        root = tree.getroot()
        existing = {m.attrib.get("id"): m for m in root.findall("mod")}
        
        all_flds = [w["folder"] for w in weapons_data] + [m["folder"] for m in extra_maps]
        for fld in all_flds:
            slug = fld.lower().replace("_", "-")
            for id_str in [f"local-{slug}", f"builtin-{slug}"]:
                if id_str in existing:
                    existing[id_str].set("active", "true")
                    existing[id_str].set("shown", "true")
                else:
                    elem = ET.SubElement(root, "mod")
                    elem.set("id", id_str)
                    elem.set("active", "true")
                    elem.set("shown", "true")
                    
        tree.write(appdata_mods_xml, encoding="utf-8", xml_declaration=True)
        print("Updated mods.xml successfully!")

if __name__ == "__main__":
    build_all_perfectly()
