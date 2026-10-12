import os
import shutil

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")

def fix_existing_mods():
    print("Fixing existing mods...")
    
    # 1. Boeing 737
    b737_parent = os.path.join(mods_dir, "Boeing 737 Burning Edition 486 1 2026-08-30T15-28Z KRYbzsnBW")
    b737_sub = os.path.join(b737_parent, "Boeing 737 burning edition")
    if os.path.exists(b737_sub):
        for item in os.listdir(b737_sub):
            s = os.path.join(b737_sub, item)
            d = os.path.join(b737_parent, item)
            if not os.path.exists(d):
                shutil.move(s, d)
        print("Flattened Boeing 737 mod structure.")
        
    info_b737 = os.path.join(b737_parent, "info.txt")
    if not os.path.exists(info_b737):
        with open(info_b737, "w") as f:
            f.write("name = Boeing 737 Burning Edition\nauthor = Community\ndescription = Burning passenger airplane map.\ntags = Map\n")

    # 2. Mossberg 590
    moss_parent = os.path.join(mods_dir, "Mossberg 590 Vox-14-1-0-1604432126")
    moss_sub = os.path.join(moss_parent, "Mossberg 590 Teardown")
    if os.path.exists(moss_sub):
        for item in os.listdir(moss_sub):
            s = os.path.join(moss_sub, item)
            d = os.path.join(moss_parent, item)
            if not os.path.exists(d):
                shutil.move(s, d)
        print("Flattened Mossberg 590 mod structure.")
        
    info_moss = os.path.join(moss_parent, "info.txt")
    if not os.path.exists(info_moss):
        with open(info_moss, "w") as f:
            f.write("name = Mossberg 590 Shotgun\nauthor = Modder\ndescription = Mossberg 590 Voxel Shotgun Model.\ntags = Tool\n")

    # 3. WWII German Weapons
    ww2_parent = os.path.join(mods_dir, "WWII German Weapons Mod for Teardown-4-V1-0-1604195964")
    ww2_sub = os.path.join(ww2_parent, "Teardown WWII German Weapons Mod V1.0")
    if os.path.exists(ww2_sub):
        for item in os.listdir(ww2_sub):
            s = os.path.join(ww2_sub, item)
            d = os.path.join(ww2_parent, item)
            if not os.path.exists(d):
                shutil.move(s, d)
        print("Flattened WWII German Weapons mod structure.")
        
    info_ww2 = os.path.join(ww2_parent, "info.txt")
    if not os.path.exists(info_ww2):
        with open(info_ww2, "w") as f:
            f.write("name = WWII German Weapons\nauthor = WWII Modder\ndescription = German weapons pack for Teardown.\ntags = Tool\n")

    # 4. BBQ Blowtorch
    bbq_parent = os.path.join(mods_dir, "BBQ Blowtorch New Model-65-New-1604795432")
    info_bbq = os.path.join(bbq_parent, "info.txt")
    if not os.path.exists(info_bbq):
        with open(info_bbq, "w") as f:
            f.write("name = BBQ Blowtorch\nauthor = Modder\ndescription = High heat BBQ blowtorch model.\ntags = Tool\n")


def create_new_mods():
    print("Creating new custom weapon and map mods...")
    
    # New Mod 1: Orbital Laser Cannon & Tactical Nuke
    orbital_dir = os.path.join(mods_dir, "Orbital_Laser_Cannon")
    os.makedirs(orbital_dir, exist_ok=True)
    
    with open(os.path.join(orbital_dir, "info.txt"), "w") as f:
        f.write("name = Orbital Laser Cannon & Nuke\nauthor = Antigravity\ndescription = Fire orbital lasers with Left Click, launch Tactical Nukes with Right Click!\ntags = Tool\n")
        
    main_lua_content = """-- Orbital Laser Cannon & Tactical Nuke Mod
function init()
	RegisterTool("orbitallaser", "Orbital Laser Cannon", "tools/shotgun.vox")
	SetBool("game.tool.orbitallaser.enabled", true)
end

function tick(dt)
	if GetString("game.player.tool") == "orbitallaser" then
		local t = GetPlayerCameraTransform()
		local dir = TransformToParentVec(t, Vec(0, 0, -1))
		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 500)
		
		if InputPressed("attack") then
			if hit then
				local hitPos = VecAdd(t.pos, VecScale(dir, dist))
				MakeHole(hitPos, 5.0, 4.0, 3.0)
				Explosion(hitPos, 5.0)
				PointLight(hitPos, 1.0, 0.6, 0.2, 12.0)
			end
		end

		if InputPressed("rmb") or InputPressed("grab") or InputPressed("secondary") then
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
			UiText("Orbital Laser Cannon | [LMB] Laser Beam | [RMB] Tactical Nuke")
		UiPop()
	end
end
"""
    with open(os.path.join(orbital_dir, "main.lua"), "w") as f:
        f.write(main_lua_content)

    # New Mod 2: Custom Destruction Testing Arena Map
    sandbox_dir = os.path.join(mods_dir, "Sandbox_Destruction_Arena")
    os.makedirs(sandbox_dir, exist_ok=True)
    
    with open(os.path.join(sandbox_dir, "info.txt"), "w") as f:
        f.write("name = Destruction Testing Arena\nauthor = Antigravity\ndescription = Destructible towers, concrete pillars, and explosive gas barrels sandbox map.\ntags = Map\n")
        
    main_xml_content = """<scene version="1.4.0">
	<environment name="Environment" template="sunny" pos="0.0 0.0 0.0"/>
	<spawnpoint name="Player spawn" pos="0.0 1.5 15.0" rot="0.0 0.0 0.0"/>
	
	<!-- Ground Plate -->
	<body pos="0.0 0.0 0.0" type="static">
		<box size="250.0 0.5 250.0" material="concrete" color="0.35 0.35 0.35"/>
	</body>

	<!-- Brick Tower 1 -->
	<body pos="-12.0 0.5 -25.0" type="static">
		<box size="14.0 45.0 14.0" material="brick" color="0.75 0.3 0.2"/>
	</body>

	<!-- Concrete Skyscraper 2 -->
	<body pos="15.0 0.5 -30.0" type="static">
		<box size="16.0 55.0 16.0" material="concrete" color="0.8 0.8 0.8"/>
	</body>

	<!-- Glass Tower 3 -->
	<body pos="0.0 0.5 -60.0" type="static">
		<box size="12.0 60.0 12.0" material="glass" color="0.3 0.6 0.95"/>
	</body>

	<!-- Explosive Barrels Target Area -->
	<group pos="0.0 1.0 -10.0">
		<body pos="-3.0 0.5 0.0" dynamic="true">
			<cylinder size="0.8 1.4" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="0.0 0.5 0.0" dynamic="true">
			<cylinder size="0.8 1.4" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="3.0 0.5 0.0" dynamic="true">
			<cylinder size="0.8 1.4" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="-1.5 1.9 0.0" dynamic="true">
			<cylinder size="0.8 1.4" material="metal" color="0.9 0.1 0.1"/>
		</body>
		<body pos="1.5 1.9 0.0" dynamic="true">
			<cylinder size="0.8 1.4" material="metal" color="0.9 0.1 0.1"/>
		</body>
	</group>
</scene>
"""
    with open(os.path.join(sandbox_dir, "main.xml"), "w") as f:
        f.write(main_xml_content)

    print("Mods setup completed!")

if __name__ == "__main__":
    fix_existing_mods()
    create_new_mods()
