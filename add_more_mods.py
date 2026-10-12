import os

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")

def create_more_mods():
    print("Creating additional Teardown weapon and map mods...")

    # ==========================================
    # MOD 1: Black Hole Singularity Cannon (Tool)
    # ==========================================
    bh_dir = os.path.join(mods_dir, "Black_Hole_Cannon")
    os.makedirs(bh_dir, exist_ok=True)
    
    with open(os.path.join(bh_dir, "info.txt"), "w") as f:
        f.write("name = Black Hole Singularity Cannon\nauthor = Antigravity\ndescription = Fires a gravitational singularity that sucks in and vaporizes buildings!\ntags = Tool\n")
        
    bh_lua = """-- Black Hole Singularity Cannon
function init()
	RegisterTool("blackhole", "Black Hole Cannon", "tools/shotgun.vox")
	SetBool("game.tool.blackhole.enabled", true)
end

function tick(dt)
	if GetString("game.player.tool") == "blackhole" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputPressed("attack") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				-- Singularity implosion phase
				for r = 2, 10, 2 do
					MakeHole(hitPos, r, r - 0.5, r - 1.0)
					PointLight(hitPos, 0.1, 0.0, 0.3, 15.0)
				end
				-- Final explosive shockwave
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
    with open(os.path.join(bh_dir, "main.lua"), "w") as f:
        f.write(bh_lua)

    # ==========================================
    # MOD 2: Airstrike Radio Beacon (Tool)
    # ==========================================
    air_dir = os.path.join(mods_dir, "Airstrike_Radio_Beacon")
    os.makedirs(air_dir, exist_ok=True)
    
    with open(os.path.join(air_dir, "info.txt"), "w") as f:
        f.write("name = Tactical Airstrike Beacon\nauthor = Antigravity\ndescription = Call in heavy artillery missile salvoes onto target coordinates!\ntags = Tool\n")
        
    air_lua = """-- Tactical Airstrike Beacon
function init()
	RegisterTool("airstrike", "Airstrike Beacon", "tools/spraycan.vox")
	SetBool("game.tool.airstrike.enabled", true)
end

function tick(dt)
	if GetString("game.player.tool") == "airstrike" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputPressed("attack") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				-- Rain 8 missiles over 2 seconds
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
    with open(os.path.join(air_dir, "main.lua"), "w") as f:
        f.write(air_lua)

    # ==========================================
    # MOD 3: Thor's Mjolnir Lightning Hammer (Tool)
    # ==========================================
    thor_dir = os.path.join(mods_dir, "Thor_Mjolnir_Lightning")
    os.makedirs(thor_dir, exist_ok=True)
    
    with open(os.path.join(thor_dir, "info.txt"), "w") as f:
        f.write("name = Thor Mjolnir Lightning Strike\nauthor = Antigravity\ndescription = Summon godly lightning bolts to smash through building supports and light fires!\ntags = Tool\n")
        
    thor_lua = """-- Thor's Mjolnir Lightning Strike
function init()
	RegisterTool("thorhammer", "Thor Lightning Hammer", "tools/sledge.vox")
	SetBool("game.tool.thorhammer.enabled", true)
end

function tick(dt)
	if GetString("game.player.tool") == "thorhammer" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputPressed("attack") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				-- Lightning pillar effect
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
    with open(os.path.join(thor_dir, "main.lua"), "w") as f:
        f.write(thor_lua)

    # ==========================================
    # MOD 4: Megacity Downtown Towers (Map)
    # ==========================================
    city_dir = os.path.join(mods_dir, "Megacity_Downtown_Towers")
    os.makedirs(city_dir, exist_ok=True)
    
    with open(os.path.join(city_dir, "info.txt"), "w") as f:
        f.write("name = Megacity Downtown Towers\nauthor = Antigravity\ndescription = Massive urban center featuring twin towers, gas station, and high rise bridges.\ntags = Map\n")
        
    city_xml = """<scene version="1.4.0">
	<environment name="Environment" template="night" pos="0.0 0.0 0.0"/>
	<spawnpoint name="Player spawn" pos="0.0 1.5 25.0" rot="0.0 0.0 0.0"/>
	
	<!-- Ground Plate / Asphalt -->
	<body pos="0.0 0.0 0.0" type="static">
		<box size="300.0 0.5 300.0" material="asphalt" color="0.2 0.2 0.2"/>
	</body>

	<!-- Twin Tower 1 -->
	<body pos="-25.0 0.5 -40.0" type="static">
		<box size="22.0 70.0 22.0" material="glass" color="0.2 0.5 0.8"/>
	</body>

	<!-- Twin Tower 2 -->
	<body pos="25.0 0.5 -40.0" type="static">
		<box size="22.0 70.0 22.0" material="glass" color="0.2 0.5 0.8"/>
	</body>

	<!-- Skybridge connecting Twin Towers -->
	<body pos="0.0 45.0 -40.0" type="static">
		<box size="30.0 4.0 8.0" material="steel" color="0.7 0.7 0.7"/>
	</body>

	<!-- Main Office Building -->
	<body pos="0.0 0.5 -100.0" type="static">
		<box size="35.0 85.0 35.0" material="concrete" color="0.85 0.85 0.85"/>
	</body>

	<!-- Gas Station Structure -->
	<body pos="-40.0 0.5 0.0" type="static">
		<box size="20.0 6.0 15.0" material="metal" color="0.9 0.9 0.9"/>
	</body>

	<!-- Fuel Tanks Under Gas Station -->
	<group pos="-40.0 1.0 0.0">
		<body pos="-5.0 0.5 0.0" dynamic="true">
			<cylinder size="1.2 2.5" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="0.0 0.5 0.0" dynamic="true">
			<cylinder size="1.2 2.5" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="5.0 0.5 0.0" dynamic="true">
			<cylinder size="1.2 2.5" material="metal" color="0.9 0.1 0.1"/>
		</body>
	</group>
</scene>
"""
    with open(os.path.join(city_dir, "main.xml"), "w") as f:
        f.write(city_xml)

    # ==========================================
    # MOD 5: Mega Suspension Bridge Collapse (Map)
    # ==========================================
    bridge_dir = os.path.join(mods_dir, "Mega_Suspension_Bridge")
    os.makedirs(bridge_dir, exist_ok=True)
    
    with open(os.path.join(bridge_dir, "info.txt"), "w") as f:
        f.write("name = Mega Suspension Bridge Collapse\nauthor = Antigravity\ndescription = Huge suspension bridge spanning water, designed for explosive structural collapse.\ntags = Map\n")
        
    bridge_xml = """<scene version="1.4.0">
	<environment name="Environment" template="sunset" pos="0.0 0.0 0.0"/>
	<spawnpoint name="Player spawn" pos="-80.0 12.0 0.0" rot="0.0 -90.0 0.0"/>
	
	<!-- Water / Chasm -->
	<body pos="0.0 -5.0 0.0" type="static">
		<box size="300.0 1.0 150.0" material="water" color="0.1 0.3 0.6"/>
	</body>

	<!-- Bridge Support Pillar Left -->
	<body pos="-40.0 0.0 0.0" type="static">
		<box size="8.0 40.0 12.0" material="concrete" color="0.6 0.6 0.6"/>
	</body>

	<!-- Bridge Support Pillar Right -->
	<body pos="40.0 0.0 0.0" type="static">
		<box size="8.0 40.0 12.0" material="concrete" color="0.6 0.6 0.6"/>
	</body>

	<!-- Bridge Deck Roadway -->
	<body pos="0.0 10.0 0.0" type="static">
		<box size="180.0 1.5 10.0" material="asphalt" color="0.25 0.25 0.25"/>
	</body>

	<!-- Bridge Steel Cables / Supports -->
	<body pos="-40.0 25.0 4.0" type="static">
		<box size="2.0 20.0 2.0" material="steel" color="0.8 0.1 0.1"/>
	</body>
	<body pos="-40.0 25.0 -4.0" type="static">
		<box size="2.0 20.0 2.0" material="steel" color="0.8 0.1 0.1"/>
	</body>
	<body pos="40.0 25.0 4.0" type="static">
		<box size="2.0 20.0 2.0" material="steel" color="0.8 0.1 0.1"/>
	</body>
	<body pos="40.0 25.0 -4.0" type="static">
		<box size="2.0 20.0 2.0" material="steel" color="0.8 0.1 0.1"/>
	</body>
</scene>
"""
    with open(os.path.join(bridge_dir, "main.xml"), "w") as f:
        f.write(bridge_xml)

    print("Added 5 new custom mods successfully!")

if __name__ == "__main__":
    create_more_mods()
