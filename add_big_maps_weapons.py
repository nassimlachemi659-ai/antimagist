import os

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")

def create_more_weapons_and_big_maps():
    print("Creating additional weapons and BIG maps...")

    # ==========================================
    # WEAPON 1: Plasma Disintegrator Cannon
    # ==========================================
    p_dir = os.path.join(mods_dir, "Plasma_Disintegrator_Cannon")
    os.makedirs(p_dir, exist_ok=True)
    with open(os.path.join(p_dir, "info.txt"), "w") as f:
        f.write("name = Plasma Disintegrator Cannon\nauthor = Antigravity\ndescription = Fires turquoise plasma spheres that melt through solid concrete and steel!\ntags = Tool\n")
    p_lua = """function init()
	RegisterTool("plasmacannon", "Plasma Disintegrator", "tools/shotgun.vox")
	SetBool("game.tool.plasmacannon.enabled", true)
end
function tick(dt)
	if GetString("game.player.tool") == "plasmacannon" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		if InputPressed("attack") then
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
    with open(os.path.join(p_dir, "main.lua"), "w") as f:
        f.write(p_lua)

    # ==========================================
    # WEAPON 2: Cluster Bomb Launcher (MIRV)
    # ==========================================
    c_dir = os.path.join(mods_dir, "Cluster_Bomb_Launcher")
    os.makedirs(c_dir, exist_ok=True)
    with open(os.path.join(c_dir, "info.txt"), "w") as f:
        f.write("name = Cluster Bomb Launcher (MIRV)\nauthor = Antigravity\ndescription = Fires a warhead that splits into 12 explosive cluster bomblets!\ntags = Tool\n")
    c_lua = """function init()
	RegisterTool("clusterbomb", "Cluster Bomb Launcher", "tools/rocket.vox")
	SetBool("game.tool.clusterbomb.enabled", true)
end
function tick(dt)
	if GetString("game.player.tool") == "clusterbomb" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		if InputPressed("attack") then
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
    with open(os.path.join(c_dir, "main.lua"), "w") as f:
        f.write(c_lua)

    # ==========================================
    # WEAPON 3: Kinetic Hyper Railgun
    # ==========================================
    r_dir = os.path.join(mods_dir, "Hyper_Precision_Railgun")
    os.makedirs(r_dir, exist_ok=True)
    with open(os.path.join(r_dir, "info.txt"), "w") as f:
        f.write("name = Hyper Precision Railgun\nauthor = Antigravity\ndescription = Hyper-velocity kinetic slug that pierces directly through 100m of solid structures!\ntags = Tool\n")
    r_lua = """function init()
	RegisterTool("railgun", "Hyper Precision Railgun", "tools/shotgun.vox")
	SetBool("game.tool.railgun.enabled", true)
end
function tick(dt)
	if GetString("game.player.tool") == "railgun" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		if InputPressed("attack") then
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
    with open(os.path.join(r_dir, "main.lua"), "w") as f:
        f.write(r_lua)

    # ==========================================
    # BIG MAP 1: Mega Airport & Runway Terminal (400x400)
    # ==========================================
    air_dir = os.path.join(mods_dir, "BIG_MAP_Mega_Airport_Terminal")
    os.makedirs(air_dir, exist_ok=True)
    with open(os.path.join(air_dir, "info.txt"), "w") as f:
        f.write("name = BIG MAP: International Airport Terminal\nauthor = Antigravity\ndescription = Massive 400m airport with control tower, passenger terminal, jetways, and airplanes.\ntags = Map\n")
    air_xml = """<scene version="1.4.0">
	<environment name="Environment" template="sunny" pos="0.0 0.0 0.0"/>
	<spawnpoint name="Player spawn" pos="-50.0 1.5 80.0" rot="0.0 0.0 0.0"/>
	
	<!-- Airport Asphalt Field & Runway -->
	<body pos="0.0 0.0 0.0" type="static">
		<box size="400.0 0.5 400.0" material="asphalt" color="0.25 0.25 0.25"/>
	</body>

	<!-- Main Passenger Terminal Building -->
	<body pos="0.0 0.5 0.0" type="static">
		<box size="120.0 18.0 40.0" material="glass" color="0.3 0.6 0.9"/>
	</body>

	<!-- Airport Control Tower -->
	<body pos="-80.0 0.5 -50.0" type="static">
		<box size="14.0 65.0 14.0" material="concrete" color="0.8 0.8 0.8"/>
	</body>
	<body pos="-80.0 65.5 -50.0" type="static">
		<box size="22.0 12.0 22.0" material="glass" color="0.2 0.7 0.9"/>
	</body>

	<!-- Hangar 1 -->
	<body pos="90.0 0.5 -60.0" type="static">
		<box size="60.0 25.0 50.0" material="metal" color="0.6 0.6 0.65"/>
	</body>

	<!-- Airplane 1 (Fuselage) -->
	<body pos="-40.0 6.0 -60.0" type="static">
		<box size="65.0 8.0 8.0" material="metal" color="0.95 0.95 0.95"/>
	</body>
	<!-- Airplane 1 (Wings) -->
	<body pos="-40.0 6.0 -60.0" type="static">
		<box size="16.0 1.5 55.0" material="metal" color="0.9 0.9 0.9"/>
	</body>

	<!-- Fuel Tanks Ramp -->
	<group pos="70.0 1.0 40.0">
		<body pos="-8.0 1.5 0.0" dynamic="true">
			<cylinder size="2.5 5.0" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="0.0 1.5 0.0" dynamic="true">
			<cylinder size="2.5 5.0" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="8.0 1.5 0.0" dynamic="true">
			<cylinder size="2.5 5.0" material="metal" color="0.9 0.1 0.1"/>
		</body>
	</group>
</scene>
"""
    with open(os.path.join(air_dir, "main.xml"), "w") as f:
        f.write(air_xml)

    # ==========================================
    # BIG MAP 2: Military Base & Missile Silo (350x350)
    # ==========================================
    mil_dir = os.path.join(mods_dir, "BIG_MAP_Military_Bunker_Base")
    os.makedirs(mil_dir, exist_ok=True)
    with open(os.path.join(mil_dir, "info.txt"), "w") as f:
        f.write("name = BIG MAP: Military Bunker & Missile Silo\nauthor = Antigravity\ndescription = Reinforced military compound with radar tower, thick concrete bunkers, and missile silo.\ntags = Map\n")
    mil_xml = """<scene version="1.4.0">
	<environment name="Environment" template="sunset" pos="0.0 0.0 0.0"/>
	<spawnpoint name="Player spawn" pos="-60.0 1.5 70.0" rot="0.0 0.0 0.0"/>
	
	<!-- Desert Ground Base -->
	<body pos="0.0 0.0 0.0" type="static">
		<box size="350.0 0.5 350.0" material="dirt" color="0.5 0.4 0.3"/>
	</body>

	<!-- Heavy Concrete Command Bunker -->
	<body pos="0.0 0.5 0.0" type="static">
		<box size="75.0 22.0 55.0" material="concrete" color="0.45 0.45 0.45"/>
	</body>

	<!-- Radar & Communications Tower -->
	<body pos="60.0 0.5 -40.0" type="static">
		<box size="10.0 75.0 10.0" material="steel" color="0.3 0.3 0.35"/>
	</body>

	<!-- Missile Silo Vault -->
	<body pos="-60.0 0.5 -50.0" type="static">
		<box size="35.0 15.0 35.0" material="steel" color="0.25 0.25 0.25"/>
	</body>

	<!-- Perimeter Guard Wall -->
	<body pos="0.0 0.5 100.0" type="static">
		<box size="240.0 8.0 4.0" material="concrete" color="0.5 0.5 0.5"/>
	</body>
</scene>
"""
    with open(os.path.join(mil_dir, "main.xml"), "w") as f:
        f.write(mil_xml)

    # ==========================================
    # BIG MAP 3: Suburban Neighborhood & Shopping Mall
    # ==========================================
    mall_dir = os.path.join(mods_dir, "BIG_MAP_Suburban_Shopping_Mall")
    os.makedirs(mall_dir, exist_ok=True)
    with open(os.path.join(mall_dir, "info.txt"), "w") as f:
        f.write("name = BIG MAP: Suburban Neighborhood & Mall\nauthor = Antigravity\ndescription = Huge suburban map with 6 destructible houses, streets, and a 2-story shopping mall.\ntags = Map\n")
    mall_xml = """<scene version="1.4.0">
	<environment name="Environment" template="sunny" pos="0.0 0.0 0.0"/>
	<spawnpoint name="Player spawn" pos="0.0 1.5 90.0" rot="0.0 0.0 0.0"/>
	
	<!-- City Ground -->
	<body pos="0.0 0.0 0.0" type="static">
		<box size="350.0 0.5 350.0" material="asphalt" color="0.3 0.3 0.3"/>
	</body>

	<!-- Suburban House 1 -->
	<body pos="-70.0 0.5 50.0" type="static">
		<box size="22.0 10.0 18.0" material="wood" color="0.8 0.7 0.5"/>
	</body>
	<!-- Suburban House 2 -->
	<body pos="-30.0 0.5 50.0" type="static">
		<box size="22.0 10.0 18.0" material="brick" color="0.7 0.3 0.2"/>
	</body>
	<!-- Suburban House 3 -->
	<body pos="30.0 0.5 50.0" type="static">
		<box size="22.0 10.0 18.0" material="wood" color="0.4 0.6 0.5"/>
	</body>
	<!-- Suburban House 4 -->
	<body pos="70.0 0.5 50.0" type="static">
		<box size="22.0 10.0 18.0" material="brick" color="0.8 0.4 0.3"/>
	</body>

	<!-- 2-Story Shopping Mall Complex -->
	<body pos="0.0 0.5 -50.0" type="static">
		<box size="140.0 25.0 70.0" material="glass" color="0.3 0.7 0.9"/>
	</body>
</scene>
"""
    with open(os.path.join(mall_dir, "main.xml"), "w") as f:
        f.write(mall_xml)

    print("Added additional 3 weapons and 3 BIG maps!")

if __name__ == "__main__":
    create_more_weapons_and_big_maps()
