import os
import shutil
import xml.etree.ElementTree as ET

s_game_dir = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown"
s_mods_dir = os.path.join(s_game_dir, "mods")
doc_mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")
data_vox_tool = os.path.join(s_game_dir, "data", "vox", "tool")

# ==============================================================================
# 1. CREATE 6 NEW WEAPONS (Teardown v2 Standard)
# ==============================================================================

new_weapons = [
    {
        "folder": "Airstrike_Radio_Beacon",
        "name": "Tactical Airstrike Beacon",
        "desc": "Mark coordinates with [LMB] to call down a heavy 12-missile artillery barrage!",
        "tool_id": "airstrike",
        "vox_src": "spraycan.vox",
        "group": 5,
        "code": """#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("airstrike", "Tactical Airstrike Beacon", "MOD/vox/weapon.vox", 5)
	SetToolAmmoPickupAmount("airstrike", 10)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("airstrike", true, p)
		SetToolAmmo("airstrike", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "airstrike" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				local hit, dist = QueryRaycast(t.pos, fwd, 500)
				if hit then
					local targetPos = VecAdd(t.pos, VecScale(fwd, dist))
					-- Spawn a barrage of 12 cascading strikes
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
			end
		end
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
        "code": """#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("clusterbomb", "MIRV Cluster Bomb Launcher", "MOD/vox/weapon.vox", 6)
	SetToolAmmoPickupAmount("clusterbomb", 20)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("clusterbomb", true, p)
		SetToolAmmo("clusterbomb", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "clusterbomb" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				local hit, dist = QueryRaycast(t.pos, fwd, 500)
				if hit then
					local impact = VecAdd(t.pos, VecScale(fwd, dist))
					Explosion(impact, 8.0)
					-- Disperse 14 sub-bombs
					for i = 1, 14 do
						local rx = math.random(-10, 10)
						local rz = math.random(-10, 10)
						local subPos = VecAdd(impact, Vec(rx, 1, rz))
						MakeHole(subPos, 4.5, 3.5, 2.0)
						Explosion(subPos, 5.0)
						SpawnFire(subPos)
					end
				end
			end
		end
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
        "code": """#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("flamecannon", "Thermobaric Flame Cannon", "MOD/vox/weapon.vox", 7)
	SetToolAmmoPickupAmount("flamecannon", 100)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("flamecannon", true, p)
		SetToolAmmo("flamecannon", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "flamecannon" and GetPlayerVehicle(p) == 0 then
			if InputDown("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				local hit, dist = QueryRaycast(t.pos, fwd, 35)
				if hit then
					local burnPos = VecAdd(t.pos, VecScale(fwd, dist))
					MakeHole(burnPos, 2.5, 2.0, 1.0)
					SpawnFire(burnPos)
					PointLight(burnPos, 1.0, 0.4, 0.05, 12.0)
					if math.random(1, 4) == 1 then
						Explosion(burnPos, 2.0)
					end
				end
			end
		end
	end
end
"""
    },
    {
        "folder": "Gravity_Shockwave_Repulsor",
        "name": "Gravity Shockwave Repulsor",
        "desc": "Emits a massive concussive kinetic pulse that blasts buildings and vehicles into the air!",
        "tool_id": "repulsor",
        "vox_src": "leafblower.vox",
        "group": 8,
        "code": """#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("repulsor", "Gravity Shockwave Repulsor", "MOD/vox/weapon.vox", 8)
	SetToolAmmoPickupAmount("repulsor", 50)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("repulsor", true, p)
		SetToolAmmo("repulsor", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "repulsor" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				-- Emit 5 forward penetrating kinetic rings
				for step = 4, 30, 4 do
					local ringPos = VecAdd(t.pos, VecScale(fwd, step))
					MakeHole(ringPos, 4.0, 3.5, 2.5)
					PointLight(ringPos, 0.3, 0.7, 1.0, 15.0)
				end
				local hit, dist = QueryRaycast(t.pos, fwd, 40)
				if hit then
					local hitPos = VecAdd(t.pos, VecScale(fwd, dist))
					Explosion(hitPos, 6.0)
				end
			end
		end
	end
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
        "code": """#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("fatman", "Tactical Nuke Launcher", "MOD/vox/weapon.vox", 9)
	SetToolAmmoPickupAmount("fatman", 5)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("fatman", true, p)
		SetToolAmmo("fatman", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "fatman" and GetPlayerVehicle(p) == 0 then
			if InputPressed("usetool", p) then
				local t = GetPlayerCameraTransform(p)
				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
				local hit, dist = QueryRaycast(t.pos, fwd, 500)
				if hit then
					local nukePos = VecAdd(t.pos, VecScale(fwd, dist))
					-- Core thermal vaporization sphere
					MakeHole(nukePos, 18.0, 15.0, 10.0)
					Explosion(nukePos, 20.0)
					PointLight(nukePos, 1.0, 0.9, 0.6, 50.0)
					-- Outer shockwave detonations
					for i = 1, 16 do
						local ang = (i / 16.0) * 6.28318
						local ox = math.cos(ang) * 12.0
						local oz = math.sin(ang) * 12.0
						local wavePos = VecAdd(nukePos, Vec(ox, 1, oz))
						Explosion(wavePos, 8.0)
						SpawnFire(wavePos)
					end
				end
			end
		end
	end
end
"""
    },
    {
        "folder": "Chrono_Time_Disruptor",
        "name": "Chrono Time Disruptor (Slow-Mo)",
        "desc": "Control time physics! [LMB] slow motion (0.2x speed) | [RMB] restore normal speed!",
        "tool_id": "chronogun",
        "vox_src": "booster.vox",
        "group": 0,
        "code": """#version 2
#include "script/include/player.lua"

function server.init()
	RegisterTool("chronogun", "Chrono Time Disruptor", "MOD/vox/weapon.vox", 0)
	SetToolAmmoPickupAmount("chronogun", 100)
end

function server.tick(dt)
	for p in PlayersAdded() do
		SetToolEnabled("chronogun", true, p)
		SetToolAmmo("chronogun", 999, p)
	end

	for p in Players() do
		if GetPlayerTool(p) == "chronogun" and GetPlayerVehicle(p) == 0 then
			-- Left click: slow motion
			if InputPressed("usetool", p) then
				SetTimeScale(0.2)
			end
			-- Right click: normal speed
			if InputPressed("grab", p) then
				SetTimeScale(1.0)
			end
		end
	end
end
"""
    }
]

# ==============================================================================
# 2. CREATE 3 NEW BIG MAPS (Teardown v3 Standard)
# ==============================================================================

new_maps = [
    {
        "folder": "Nuclear_Power_Plant",
        "name": "Nuclear Power Plant Complex",
        "desc": "Massive 300m industrial facility with two 60m cooling towers, reactor containment dome, and turbine hall!",
        "xml": """<scene version="3" shadowVolume="300 120 300">
	<environment template="sunset" skyboxrot="90"/>
	<voxbox pos="-150.0 0.0 -150.0" size="3000 2 3000" texture="1" color="0.25 0.25 0.25"/>
	<spawnpoint pos="0.0 1.2 80.0" rot="0.0 180.0 0.0"/>
	<boundary>
		<vertex pos="-145.0 -145.0"/>
		<vertex pos="145.0 -145.0"/>
		<vertex pos="145.0 145.0"/>
		<vertex pos="-145.0 145.0"/>
	</boundary>
	<script file="main.lua"/>
	<script file="sandbox.lua"/>

	<!-- COOLING TOWER 1 (60m Tall) -->
	<group pos="-50.0 0.2 -40.0">
		<voxbox pos="-18.0 0.0 -18.0" size="360 600 360" material="concrete" color="0.75 0.75 0.75"/>
		<voxbox pos="-14.0 1.0 -14.0" size="280 590 280" material="masonry" color="0.1 0.1 0.1"/>
	</group>

	<!-- COOLING TOWER 2 (60m Tall) -->
	<group pos="50.0 0.2 -40.0">
		<voxbox pos="-18.0 0.0 -18.0" size="360 600 360" material="concrete" color="0.75 0.75 0.75"/>
		<voxbox pos="-14.0 1.0 -14.0" size="280 590 280" material="masonry" color="0.1 0.1 0.1"/>
	</group>

	<!-- REACTOR CONTAINMENT DOME (Explosive Core) -->
	<group pos="0.0 0.2 -100.0">
		<voxbox pos="-20.0 0.0 -20.0" size="400 300 400" material="concrete" color="0.85 0.85 0.85"/>
		<voxbox pos="-8.0 4.0 -8.0" size="160 160 160" material="metal" color="0.9 0.8 0.1"/>
	</group>

	<!-- TURBINE GENERATOR HALL -->
	<group pos="0.0 0.2 0.0">
		<voxbox pos="-40.0 0.0 -15.0" size="800 160 300" material="brick" color="0.65 0.35 0.25"/>
		<voxbox pos="-35.0 8.0 -10.0" size="700 80 200" material="glass" color="0.2 0.6 0.9"/>
	</group>
</scene>
"""
    },
    {
        "folder": "Military_Fort_Airbase",
        "name": "Military Mountain Airbase & Silo",
        "desc": "Reinforced mountain fortress with 70m radar mast, heavy bunker, fighter jet hangars, and missile vaults!",
        "xml": """<scene version="3" shadowVolume="300 120 300">
	<environment template="night" skyboxrot="180"/>
	<voxbox pos="-150.0 0.0 -150.0" size="3000 2 3000" texture="1" color="0.3 0.3 0.25"/>
	<spawnpoint pos="0.0 1.2 70.0" rot="0.0 180.0 0.0"/>
	<boundary>
		<vertex pos="-145.0 -145.0"/>
		<vertex pos="145.0 -145.0"/>
		<vertex pos="145.0 145.0"/>
		<vertex pos="-145.0 145.0"/>
	</boundary>
	<script file="main.lua"/>
	<script file="sandbox.lua"/>

	<!-- COMMAND BUNKER -->
	<group pos="0.0 0.2 -50.0">
		<voxbox pos="-35.0 0.0 -25.0" size="700 220 500" material="concrete" color="0.45 0.45 0.45"/>
	</group>

	<!-- RADAR & COMMUNICATIONS MAST (70m tall) -->
	<group pos="60.0 0.2 -60.0">
		<voxbox pos="-4.0 0.0 -4.0" size="80 700 80" material="metal" color="0.3 0.3 0.35"/>
		<voxbox pos="-10.0 65.0 -10.0" size="200 40 200" material="metal" color="0.8 0.1 0.1"/>
	</group>

	<!-- JET HANGAR 1 -->
	<group pos="-70.0 0.2 0.0">
		<voxbox pos="-25.0 0.0 -30.0" size="500 200 600" material="metal" color="0.55 0.55 0.6"/>
	</group>

	<!-- MISSILE SILO VAULT -->
	<group pos="60.0 0.2 10.0">
		<voxbox pos="-15.0 0.0 -15.0" size="300 140 300" material="metal" color="0.2 0.2 0.2"/>
	</group>
</scene>
"""
    },
    {
        "folder": "Mega_Ocean_Port_Bridge",
        "name": "Mega Ocean Port & Bridge",
        "desc": "Deep water harbor featuring a 100m suspension bridge, cargo cranes, and container stacks!",
        "xml": """<scene version="3" shadowVolume="350 120 350">
	<environment template="sunny" skyboxrot="30"/>
	<voxbox pos="-175.0 -10.0 -175.0" size="3500 20 3500" texture="1" color="0.2 0.2 0.2"/>
	<water pos="0.0 0.0 0.0"/>
	<spawnpoint pos="-60.0 12.0 40.0" rot="0.0 -90.0 0.0"/>
	<boundary>
		<vertex pos="-160.0 -160.0"/>
		<vertex pos="160.0 -160.0"/>
		<vertex pos="160.0 160.0"/>
		<vertex pos="-160.0 160.0"/>
	</boundary>
	<script file="main.lua"/>
	<script file="sandbox.lua"/>

	<!-- HARBOR CONCRETE DOCKS -->
	<group pos="-60.0 0.0 40.0">
		<voxbox pos="-40.0 0.0 -60.0" size="800 100 1200" material="concrete" color="0.5 0.5 0.5"/>
	</group>

	<!-- CONTAINER STACKS -->
	<group pos="-70.0 10.2 20.0">
		<voxbox pos="-10.0 0.0 0.0" size="120 80 300" material="metal" color="0.8 0.2 0.2"/>
		<voxbox pos="5.0 0.0 0.0" size="120 80 300" material="metal" color="0.2 0.4 0.8"/>
		<voxbox pos="-3.0 8.0 0.0" size="120 80 300" material="metal" color="0.2 0.8 0.3"/>
	</group>

	<!-- SUSPENSION BRIDGE ROADWAY (Over Water) -->
	<group pos="0.0 10.0 -60.0">
		<!-- Deck -->
		<voxbox pos="-120.0 0.0 -6.0" size="2400 15 120" material="asphalt" color="0.25 0.25 0.25"/>
		<!-- Left Pillar -->
		<voxbox pos="-50.0 -10.0 -5.0" size="60 500 100" material="concrete" color="0.75 0.75 0.75"/>
		<!-- Right Pillar -->
		<voxbox pos="50.0 -10.0 -5.0" size="60 500 100" material="concrete" color="0.75 0.75 0.75"/>
	</group>
</scene>
"""
    }
]

def build_all():
    print("--- 1. Building 6 New Weapons ---")
    for w in new_weapons:
        for parent in [s_mods_dir, doc_mods_dir]:
            p = os.path.join(parent, w["folder"])
            vox_dir = os.path.join(p, "vox")
            os.makedirs(vox_dir, exist_ok=True)
            
            # Copy real 3D model
            src_vox = os.path.join(data_vox_tool, w["vox_src"])
            dst_vox = os.path.join(vox_dir, "weapon.vox")
            if os.path.exists(src_vox):
                shutil.copyfile(src_vox, dst_vox)

            # Write info.txt
            with open(os.path.join(p, "info.txt"), "w", encoding="utf-8") as f:
                f.write(f"en_name = {w['name']}\nauthor = Antigravity\nen_description = {w['desc']}\ntags = Tool, Global, Multiplayer\nversion = 2\n")

            # Write main.lua
            with open(os.path.join(p, "main.lua"), "w", encoding="utf-8") as f:
                f.write(w["code"])
        print(f"Created weapon: {w['name']}")

    print("\n--- 2. Building 3 New Big Maps ---")
    for m in new_maps:
        for parent in [s_mods_dir, doc_mods_dir]:
            p = os.path.join(parent, m["folder"])
            os.makedirs(p, exist_ok=True)
            
            # Write info.txt
            with open(os.path.join(p, "info.txt"), "w", encoding="utf-8") as f:
                f.write(f"en_name = {m['name']}\nauthor = Antigravity\nen_description = {m['desc']}\ntags = Map\nversion = 2\n")

            # Write main.xml
            with open(os.path.join(p, "main.xml"), "w", encoding="utf-8") as f:
                f.write(m["xml"])
        print(f"Created map: {m['name']}")

    # ==============================================================================
    # 3. UPDATE REGISTRY (mods.xml)
    # ==============================================================================
    print("\n--- 3. Updating mods.xml Registry ---")
    if os.path.exists(appdata_mods_xml):
        tree = ET.parse(appdata_mods_xml)
        root = tree.getroot()
        existing = {m.attrib.get("id"): m for m in root.findall("mod")}
        
        all_new_folders = [w["folder"] for w in new_weapons] + [m["folder"] for m in new_maps]
        for fld in all_new_folders:
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
    build_all()
