import os
import xml.etree.ElementTree as ET

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
savegame_xml_path = os.path.expanduser("~/AppData/Local/Teardown/savegame.xml")

tool_mods_data = [
    {
        "folder": "Orbital_Laser_Cannon",
        "id": "orbitallaser",
        "name": "Orbital Laser Cannon",
        "vox": "tools/shotgun.vox",
        "group": 1,
        "lua_code": """-- Orbital Laser Cannon & Tactical Nuke
function init()
	RegisterTool("orbitallaser", "Orbital Laser Cannon", "tools/shotgun.vox", 1)
	SetBool("game.tool.orbitallaser.enabled", true)
	SetBool("game.tool.orbitallaser.unlocked", true)
	SetInt("game.tool.orbitallaser.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.orbitallaser.enabled", true)
	SetBool("game.tool.orbitallaser.unlocked", true)
	SetInt("game.tool.orbitallaser.ammo", 999)

	if GetString("game.player.tool") == "orbitallaser" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputDown("usetool") or InputPressed("usetool") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				MakeHole(hitPos, 5.0, 4.0, 3.0)
				Explosion(hitPos, 5.0)
				PointLight(hitPos, 1.0, 0.5, 0.1, 15.0)
			end
		end

		if InputPressed("grab") or InputPressed("camerazoom") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				MakeHole(hitPos, 12.0, 10.0, 8.0)
				Explosion(hitPos, 10.0)
				for i = 1, 6 do
					local offset = Vec(math.random(-3, 3), math.random(0, 4), math.random(-3, 3))
					Explosion(VecAdd(hitPos, offset), 6.0)
				end
			end
		end
	end
end

function draw()
	if GetString("game.player.tool") == "orbitallaser" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Orbital Laser Cannon | [LMB] Laser Beam | [RMB / E] Tactical Nuke")
		UiPop()
	end
end
"""
    },
    {
        "folder": "Black_Hole_Cannon",
        "id": "blackhole",
        "name": "Black Hole Cannon",
        "vox": "tools/shotgun.vox",
        "group": 2,
        "lua_code": """-- Black Hole Singularity Cannon
function init()
	RegisterTool("blackhole", "Black Hole Cannon", "tools/shotgun.vox", 2)
	SetBool("game.tool.blackhole.enabled", true)
	SetBool("game.tool.blackhole.unlocked", true)
	SetInt("game.tool.blackhole.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.blackhole.enabled", true)
	SetBool("game.tool.blackhole.unlocked", true)
	SetInt("game.tool.blackhole.ammo", 999)

	if GetString("game.player.tool") == "blackhole" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputDown("usetool") or InputPressed("usetool") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				for r = 2, 10, 2 do
					MakeHole(hitPos, r, r - 0.5, r - 1.0)
					PointLight(hitPos, 0.1, 0.0, 0.4, 15.0)
				end
				Explosion(hitPos, 8.0)
			end
		end
	end
end

function draw()
	if GetString("game.player.tool") == "blackhole" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Black Hole Cannon | [LMB] Fire Singularity Vortex")
		UiPop()
	end
end
"""
    },
    {
        "folder": "Airstrike_Radio_Beacon",
        "id": "airstrike",
        "name": "Airstrike Beacon",
        "vox": "tools/spraycan.vox",
        "group": 3,
        "lua_code": """-- Tactical Airstrike Beacon
function init()
	RegisterTool("airstrike", "Airstrike Beacon", "tools/spraycan.vox", 3)
	SetBool("game.tool.airstrike.enabled", true)
	SetBool("game.tool.airstrike.unlocked", true)
	SetInt("game.tool.airstrike.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.airstrike.enabled", true)
	SetBool("game.tool.airstrike.unlocked", true)
	SetInt("game.tool.airstrike.ammo", 999)

	if GetString("game.player.tool") == "airstrike" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputDown("usetool") or InputPressed("usetool") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				for i = 1, 8 do
					local offsetX = math.random(-10, 10)
					local offsetZ = math.random(-10, 10)
					local target = VecAdd(hitPos, Vec(offsetX, 0, offsetZ))
					MakeHole(target, 6.0, 5.0, 4.0)
					Explosion(target, 6.0)
					SpawnFire(target)
				end
			end
		end
	end
end

function draw()
	if GetString("game.player.tool") == "airstrike" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Airstrike Beacon | [LMB] Call Heavy Missile Salvo")
		UiPop()
	end
end
"""
    },
    {
        "folder": "Thor_Mjolnir_Lightning",
        "id": "thorhammer",
        "name": "Thor Lightning Hammer",
        "vox": "tools/sledge.vox",
        "group": 4,
        "lua_code": """-- Thor Mjolnir Lightning Strike
function init()
	RegisterTool("thorhammer", "Thor Lightning Hammer", "tools/sledge.vox", 4)
	SetBool("game.tool.thorhammer.enabled", true)
	SetBool("game.tool.thorhammer.unlocked", true)
	SetInt("game.tool.thorhammer.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.thorhammer.enabled", true)
	SetBool("game.tool.thorhammer.unlocked", true)
	SetInt("game.tool.thorhammer.ammo", 999)

	if GetString("game.player.tool") == "thorhammer" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputDown("usetool") or InputPressed("usetool") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				for y = 0, 40, 5 do
					local p = VecAdd(hitPos, Vec(0, y, 0))
					PointLight(p, 0.4, 0.8, 1.0, 10.0)
					MakeHole(p, 3.0, 2.0, 1.0)
				end
				Explosion(hitPos, 7.0)
				SpawnFire(hitPos)
			end
		end
	end
end

function draw()
	if GetString("game.player.tool") == "thorhammer" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Thor Mjolnir | [LMB] Summon Lightning Blast")
		UiPop()
	end
end
"""
    },
    {
        "folder": "Plasma_Disintegrator_Cannon",
        "id": "plasmacannon",
        "name": "Plasma Disintegrator",
        "vox": "tools/shotgun.vox",
        "group": 5,
        "lua_code": """-- Plasma Disintegrator Cannon
function init()
	RegisterTool("plasmacannon", "Plasma Disintegrator", "tools/shotgun.vox", 5)
	SetBool("game.tool.plasmacannon.enabled", true)
	SetBool("game.tool.plasmacannon.unlocked", true)
	SetInt("game.tool.plasmacannon.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.plasmacannon.enabled", true)
	SetBool("game.tool.plasmacannon.unlocked", true)
	SetInt("game.tool.plasmacannon.ammo", 999)

	if GetString("game.player.tool") == "plasmacannon" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputDown("usetool") or InputPressed("usetool") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				MakeHole(hitPos, 6.0, 5.0, 4.0)
				Explosion(hitPos, 4.0)
				PointLight(hitPos, 0.0, 0.9, 1.0, 15.0)
			end
		end
	end
end

function draw()
	if GetString("game.player.tool") == "plasmacannon" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Plasma Disintegrator | [LMB] Fire Plasma Sphere")
		UiPop()
	end
end
"""
    },
    {
        "folder": "Cluster_Bomb_Launcher",
        "id": "clusterbomb",
        "name": "Cluster Bomb Launcher",
        "vox": "tools/rocket.vox",
        "group": 6,
        "lua_code": """-- Cluster Bomb Launcher
function init()
	RegisterTool("clusterbomb", "Cluster Bomb Launcher", "tools/rocket.vox", 6)
	SetBool("game.tool.clusterbomb.enabled", true)
	SetBool("game.tool.clusterbomb.unlocked", true)
	SetInt("game.tool.clusterbomb.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.clusterbomb.enabled", true)
	SetBool("game.tool.clusterbomb.unlocked", true)
	SetInt("game.tool.clusterbomb.ammo", 999)

	if GetString("game.player.tool") == "clusterbomb" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputDown("usetool") or InputPressed("usetool") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				Explosion(hitPos, 6.0)
				for i = 1, 12 do
					local rx = math.random(-8, 8)
					local ry = math.random(0, 4)
					local rz = math.random(-8, 8)
					local subPos = VecAdd(hitPos, Vec(rx, ry, rz))
					MakeHole(subPos, 4.0, 3.0, 2.0)
					Explosion(subPos, 4.0)
				end
			end
		end
	end
end

function draw()
	if GetString("game.player.tool") == "clusterbomb" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Cluster Bomb Launcher | [LMB] Launch MIRV Salvo")
		UiPop()
	end
end
"""
    },
    {
        "folder": "Hyper_Precision_Railgun",
        "id": "railgun",
        "name": "Hyper Precision Railgun",
        "vox": "tools/shotgun.vox",
        "group": 1,
        "lua_code": """-- Hyper Precision Railgun
function init()
	RegisterTool("railgun", "Hyper Precision Railgun", "tools/shotgun.vox", 1)
	SetBool("game.tool.railgun.enabled", true)
	SetBool("game.tool.railgun.unlocked", true)
	SetInt("game.tool.railgun.ammo", 999)
end

function tick(dt)
	SetBool("game.tool.railgun.enabled", true)
	SetBool("game.tool.railgun.unlocked", true)
	SetInt("game.tool.railgun.ammo", 999)

	if GetString("game.player.tool") == "railgun" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		if InputDown("usetool") or InputPressed("usetool") then
			for step = 1, 100, 2 do
				local p = VecAdd(t.pos, VecScale(dir, step))
				MakeHole(p, 2.5, 2.0, 1.5)
				PointLight(p, 1.0, 0.8, 0.2, 5.0)
			end
			Explosion(VecAdd(t.pos, VecScale(dir, 50)), 5.0)
		end
	end
end

function draw()
	if GetString("game.player.tool") == "railgun" then
		UiPush()
			UiAlign("center middle")
			UiTranslate(UiCenter(), UiHeight() - 50)
			UiFont("bold.otf", 24)
			UiText("Hyper Precision Railgun | [LMB] Fire Armor-Piercing Slug")
		UiPop()
	end
end
"""
    }
]

def fix_all():
    print("1. Updating Lua weapon code for usetool input and unlock flags...")
    for item in tool_mods_data:
        lua_path = os.path.join(mods_dir, item["folder"], "main.lua")
        os.makedirs(os.path.dirname(lua_path), exist_ok=True)
        with open(lua_path, "w") as f:
            f.write(item["lua_code"])
        print(f"Fixed weapon script: {item['id']}")

    print("\n2. Updating savegame.xml to enable and unlock all tools...")
    if os.path.exists(savegame_xml_path):
        tree = ET.parse(savegame_xml_path)
        root = tree.getroot()
        savegame = root.find("savegame")
        if savegame is not None:
            tool_elem = savegame.find("tool")
            if tool_elem is None:
                tool_elem = ET.SubElement(savegame, "tool")
            
            tool_ids = [t["id"] for t in tool_mods_data] + ["megagun", "sledge", "spraycan", "extinguisher", "shotgun", "rocket", "pipebomb", "blowtorch"]
            for tid in tool_ids:
                t_sub = tool_elem.find(tid)
                if t_sub is None:
                    t_sub = ET.SubElement(tool_elem, tid)
                
                en = t_sub.find("enabled")
                if en is None:
                    en = ET.SubElement(t_sub, "enabled")
                en.set("value", "1")
                
                am = t_sub.find("ammo")
                if am is None:
                    am = ET.SubElement(t_sub, "ammo")
                am.set("value", "999")

            tree.write(savegame_xml_path, encoding="utf-8", xml_declaration=True)
            print("Successfully updated savegame.xml! All tools enabled & unlocked.")

if __name__ == "__main__":
    fix_all()
