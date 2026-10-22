import os
import shutil
import zipfile

GAME_MODS = r'S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods'
DOCS_MODS = r'C:\Users\nst\Documents\Teardown\mods'
DESKTOP_PACK = r'C:\Users\nst\Desktop\Teardown_Mods_Pack_For_Friend'
DESKTOP_ZIP = r'C:\Users\nst\Desktop\Teardown_Mods_Pack.zip'
BASE_DIR = r'S:\Teardown\Teardown.Build.12032026-OFME\Teardown'

SOUND_SOURCES = {
    'laser': os.path.join(BASE_DIR, r'mods\lasergun\snd\laser.ogg'),
    'laser_hit': os.path.join(BASE_DIR, r'mods\lasergun\snd\hit.ogg'),
    'rocket': os.path.join(BASE_DIR, r'mods\vehiclebooster\rocket.ogg'),
    'shot': os.path.join(BASE_DIR, r'mods\tillaggaryd\script\paperlauncher\papergun0.ogg'),
    'shot_heavy': os.path.join(BASE_DIR, r'mods\tillaggaryd\script\paperlauncher\papergun3.ogg'),
    'spark': os.path.join(BASE_DIR, r'mods\quilezsecurity\assets\script\spark-3.ogg'),
    'gas': os.path.join(BASE_DIR, r'mods\smokegun\snd\gas.ogg'),
    'spin': os.path.join(BASE_DIR, r'mods\minigun\snd\spin.ogg')
}

def copy_snd(mod_name, snd_keys):
    snd_dir = os.path.join(GAME_MODS, mod_name, 'snd')
    os.makedirs(snd_dir, exist_ok=True)
    for k in snd_keys:
        src = SOUND_SOURCES.get(k)
        if src and os.path.exists(src):
            dst = os.path.join(snd_dir, f'{k}.ogg')
            shutil.copy2(src, dst)

# --- 1. Orbital Laser Strike ---
def update_orbital_laser():
    mod_name = 'Orbital_Laser_Strike'
    copy_snd(mod_name, ['laser', 'laser_hit'])
    lua = '''#version 2
#include "script/include/player.lua"

local laserSnd, hitSnd

function server.init()
\tRegisterTool("orbitallaser", "Orbital Laser Strike", "MOD/vox/weapon.vox", 1)
\tSetToolAmmoPickupAmount("orbitallaser", 50)
\tSetBool("game.tool.orbitallaser.enabled", true)
end

function client.init()
\tlaserSnd = LoadLoop("MOD/snd/laser.ogg")
\thitSnd = LoadSound("MOD/snd/laser_hit.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("orbitallaser", true, p)
\t\tSetToolAmmo("orbitallaser", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "orbitallaser" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("orbitallaser", p) < 50 then SetToolAmmo("orbitallaser", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputDown("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tMakeHole(hitPos, 3.5, 3.0, 2.0)
\t\t\t\tExplosion(hitPos, 2.5)
\t\t\t\tPointLight(hitPos, 0.2, 0.8, 1.0, 10.0)

\t\t\t\t-- Particle sparks at impact
\t\t\t\tParticleReset()
\t\t\t\tParticleType("spark")
\t\t\t\tParticleColor(0.2, 0.8, 1.0, 1.0, 1.0, 1.0)
\t\t\t\tParticleRadius(0.1, 0.02)
\t\t\t\tParticleEmissive(10, 0)
\t\t\t\tfor i = 1, 8 do
\t\t\t\t\tlocal vel = Vec(math.random(-6,6), math.random(2,10), math.random(-6,6))
\t\t\t\t\tSpawnParticle(hitPos, vel, 0.5)
\t\t\t\tend
\t\t\tend

\t\t\tif InputPressed("grab", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tfor y = 60, 0, -5 do
\t\t\t\t\tlocal skyP = VecAdd(hitPos, Vec(0, y, 0))
\t\t\t\t\tPointLight(skyP, 0.2, 0.9, 1.0, 15.0)
\t\t\t\t\tMakeHole(skyP, 4.0, 3.0, 2.0)
\t\t\t\tend
\t\t\t\tExplosion(hitPos, 12.0)
\t\t\t\tfor i = 1, 10 do
\t\t\t\t\tlocal off = Vec(math.random(-5, 5), math.random(0, 4), math.random(-5, 5))
\t\t\t\t\tExplosion(VecAdd(hitPos, off), 6.0)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "orbitallaser" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputDown("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.6))
\t\t\t\tDrawLine(muzzle, hitPos, 0.2, 0.8, 1.0, 1.0)
\t\t\t\tlocal skyPos = VecAdd(hitPos, Vec(0, 80, 0))
\t\t\t\tDrawLine(skyPos, hitPos, 0.4, 0.9, 1.0, 1.0)
\t\t\t\tif laserSnd then PlayLoop(laserSnd, hitPos, 1.0) end
\t\t\tend

\t\t\tif InputPressed("grab", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tif hitSnd then PlaySound(hitSnd, hitPos, 2.0) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 2. Plasma Disintegrator Rifle ---
def update_plasma_rifle():
    mod_name = 'Plasma_Disintegrator_Rifle'
    copy_snd(mod_name, ['shot', 'laser_hit'])
    lua = '''#version 2
#include "script/include/player.lua"

local fireSnd

function server.init()
\tRegisterTool("plasmarifle", "Plasma Disintegrator Rifle", "MOD/vox/weapon.vox", 1)
\tSetToolAmmoPickupAmount("plasmarifle", 50)
\tSetBool("game.tool.plasmarifle.enabled", true)
end

function client.init()
\tfireSnd = LoadSound("MOD/snd/shot.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("plasmarifle", true, p)
\t\tSetToolAmmo("plasmarifle", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "plasmarifle" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("plasmarifle", p) < 50 then SetToolAmmo("plasmarifle", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputDown("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tShoot(t.pos, fwd, "bullet", 4.0)
\t\t\t\tMakeHole(hitPos, 3.0, 2.5, 1.5)
\t\t\t\tPointLight(hitPos, 0.2, 0.6, 1.0, 12.0)
\t\t\t\tSpawnFire(hitPos)

\t\t\t\tParticleReset()
\t\t\t\tParticleType("spark")
\t\t\t\tParticleColor(0.1, 0.6, 1.0, 1.0, 1.0, 1.0)
\t\t\t\tParticleRadius(0.08, 0.02)
\t\t\t\tParticleEmissive(8, 0)
\t\t\t\tfor i = 1, 6 do
\t\t\t\t\tlocal vel = Vec(math.random(-5,5), math.random(1,6), math.random(-5,5))
\t\t\t\t\tSpawnParticle(hitPos, vel, 0.4)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "plasmarifle" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.6))
\t\t\t\tDrawLine(muzzle, hitPos, 0.1, 0.6, 1.0, 1.0)
\t\t\t\tif fireSnd then PlaySound(fireSnd, muzzle, 1.0) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 3. Hyper Precision Railgun ---
def update_railgun():
    mod_name = 'Hyper_Precision_Railgun'
    copy_snd(mod_name, ['shot_heavy', 'rocket'])
    lua = '''#version 2
#include "script/include/player.lua"

local blastSnd

function server.init()
\tRegisterTool("railgun", "Hyper Precision Railgun", "MOD/vox/weapon.vox", 4)
\tSetToolAmmoPickupAmount("railgun", 50)
\tSetBool("game.tool.railgun.enabled", true)
end

function client.init()
\tblastSnd = LoadSound("MOD/snd/shot_heavy.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("railgun", true, p)
\t\tSetToolAmmo("railgun", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "railgun" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("railgun", p) < 50 then SetToolAmmo("railgun", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) then
\t\t\t\tShoot(t.pos, fwd, "bullet", 15.0)
\t\t\t\tlocal maxP = hit and dist or 120
\t\t\t\tfor step = 1, maxP, 2 do
\t\t\t\t\tlocal pPos = VecAdd(t.pos, VecScale(fwd, step))
\t\t\t\t\tMakeHole(pPos, 3.5, 2.8, 2.0)
\t\t\t\t\tPointLight(pPos, 1.0, 0.9, 0.3, 8.0)
\t\t\t\tend
\t\t\t\tif hit then
\t\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\t\tExplosion(hitPos, 6.0)
\t\t\t\t\tParticleReset()
\t\t\t\t\tParticleType("spark")
\t\t\t\t\tParticleColor(1.0, 0.9, 0.2, 1.0, 1.0, 1.0)
\t\t\t\t\tParticleRadius(0.15, 0.03)
\t\t\t\t\tParticleEmissive(12, 0)
\t\t\t\t\tfor i = 1, 25 do
\t\t\t\t\t\tlocal vel = Vec(math.random(-10,10), math.random(2,12), math.random(-10,10))
\t\t\t\t\t\tSpawnParticle(hitPos, vel, 0.8)
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "railgun" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) then
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.6))
\t\t\t\tlocal target = hit and VecAdd(t.pos, VecScale(fwd, dist)) or VecAdd(t.pos, VecScale(fwd, 150))
\t\t\t\tDrawLine(muzzle, target, 1.0, 0.9, 0.4, 1.0)
\t\t\t\tif blastSnd then PlaySound(blastSnd, muzzle, 2.0) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 4. Mjolnir Thunder Hammer ---
def update_mjolnir():
    mod_name = 'Mjolnir_Thunder_Hammer'
    copy_snd(mod_name, ['spark', 'shot_heavy'])
    lua = '''#version 2
#include "script/include/player.lua"

local thunderSnd

function server.init()
\tRegisterTool("mjolnir", "Mjolnir Thunder Hammer", "MOD/vox/weapon.vox", 3)
\tSetToolAmmoPickupAmount("mjolnir", 50)
\tSetBool("game.tool.mjolnir.enabled", true)
end

function client.init()
\tthunderSnd = LoadSound("MOD/snd/spark.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("mjolnir", true, p)
\t\tSetToolAmmo("mjolnir", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "mjolnir" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("mjolnir", p) < 50 then SetToolAmmo("mjolnir", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tfor y = 0, 50, 4 do
\t\t\t\t\tlocal pPos = VecAdd(hitPos, Vec(0, y, 0))
\t\t\t\t\tPointLight(pPos, 0.4, 0.8, 1.0, 15.0)
\t\t\t\t\tMakeHole(pPos, 4.5, 3.5, 2.5)
\t\t\t\tend
\t\t\t\tExplosion(hitPos, 9.0)
\t\t\t\tSpawnFire(hitPos)

\t\t\t\tParticleReset()
\t\t\t\tParticleType("spark")
\t\t\t\tParticleColor(0.3, 0.7, 1.0, 1.0, 1.0, 1.0)
\t\t\t\tParticleRadius(0.15, 0.02)
\t\t\t\tParticleEmissive(15, 0)
\t\t\t\tfor i = 1, 35 do
\t\t\t\t\tlocal vel = Vec(math.random(-12,12), math.random(2,14), math.random(-12,12))
\t\t\t\t\tSpawnParticle(hitPos, vel, 0.8)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "mjolnir" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.28, -0.48, -0.42))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tlocal skyPos = VecAdd(hitPos, Vec(0, 80, 0))
\t\t\t\tDrawLine(skyPos, hitPos, 0.4, 0.8, 1.0, 1.0)
\t\t\t\tfor b = 1, 3 do
\t\t\t\t\tlocal offSky = VecAdd(skyPos, Vec(math.random(-15,15), 0, math.random(-15,15)))
\t\t\t\t\tDrawLine(offSky, hitPos, 0.6, 0.9, 1.0, 1.0)
\t\t\t\tend
\t\t\t\tif thunderSnd then PlaySound(thunderSnd, hitPos, 2.5) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 5. Tactical Nuke Launcher (Fat Man) ---
def update_nuke():
    mod_name = 'Tactical_Nuke_Launcher'
    copy_snd(mod_name, ['rocket', 'shot_heavy'])
    lua = '''#version 2
#include "script/include/player.lua"

local launchSnd

function server.init()
\tRegisterTool("fatman", "Tactical Nuke Launcher (Fat Man)", "MOD/vox/weapon.vox", 9)
\tSetToolAmmoPickupAmount("fatman", 50)
\tSetBool("game.tool.fatman.enabled", true)
end

function client.init()
\tlaunchSnd = LoadSound("MOD/snd/rocket.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("fatman", true, p)
\t\tSetToolAmmo("fatman", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "fatman" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("fatman", p) < 50 then SetToolAmmo("fatman", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tShoot(t.pos, fwd, "rocket", 2.0)
\t\t\t\tMakeHole(hitPos, 20.0, 15.0, 10.0)
\t\t\t\tExplosion(hitPos, 25.0)
\t\t\t\tfor i = 1, 15 do
\t\t\t\t\tlocal off = Vec(math.random(-12, 12), math.random(1, 8), math.random(-12, 12))
\t\t\t\t\tExplosion(VecAdd(hitPos, off), 10.0)
\t\t\t\t\tSpawnFire(VecAdd(hitPos, off))
\t\t\t\tend

\t\t\t\t-- Mushroom cloud column
\t\t\t\tParticleReset()
\t\t\t\tParticleType("smoke")
\t\t\t\tParticleColor(0.8, 0.4, 0.1, 0.2, 0.2, 0.2)
\t\t\t\tParticleRadius(1.5, 4.0)
\t\t\t\tParticleAlpha(0.8, 0.0)
\t\t\t\tfor y = 0, 40, 3 do
\t\t\t\t\tlocal colP = VecAdd(hitPos, Vec(math.random(-4,4), y, math.random(-4,4)))
\t\t\t\t\tSpawnParticle(colP, Vec(0, 5, 0), 2.5)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "fatman" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tif InputPressed("usetool", p) then
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.8))
\t\t\t\tif launchSnd then PlaySound(launchSnd, muzzle, 2.5) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 6. Thermobaric Flame Cannon ---
def update_flame_cannon():
    mod_name = 'Thermobaric_Flame_Cannon'
    copy_snd(mod_name, ['gas'])
    lua = '''#version 2
#include "script/include/player.lua"

local flameSnd

function server.init()
\tRegisterTool("flamecannon", "Thermobaric Flame Cannon", "MOD/vox/weapon.vox", 7)
\tSetToolAmmoPickupAmount("flamecannon", 50)
\tSetBool("game.tool.flamecannon.enabled", true)
end

function client.init()
\tflameSnd = LoadLoop("MOD/snd/gas.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("flamecannon", true, p)
\t\tSetToolAmmo("flamecannon", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "flamecannon" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("flamecannon", p) < 50 then SetToolAmmo("flamecannon", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputDown("usetool", p) then
\t\t\t\tlocal range = math.min(dist or 25, 25)
\t\t\t\tfor step = 1, range, 2 do
\t\t\t\t\tlocal pPos = VecAdd(t.pos, VecScale(fwd, step))
\t\t\t\t\tPointLight(pPos, 1.0, 0.4, 0.1, 8.0)
\t\t\t\t\tParticleReset()
\t\t\t\t\tParticleType("smoke")
\t\t\t\t\tParticleColor(1.0, 0.5, 0.1, 0.8, 0.1, 0.0)
\t\t\t\t\tParticleRadius(0.3, 1.2)
\t\t\t\t\tParticleAlpha(0.9, 0.0)
\t\t\t\t\tlocal spread = Vec(math.random(-1,1)*0.2, math.random(-1,1)*0.2, math.random(-1,1)*0.2)
\t\t\t\t\tSpawnParticle(pPos, VecAdd(VecScale(fwd, 15), spread), 0.6)
\t\t\t\tend

\t\t\t\tif hit and dist <= 25 then
\t\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\t\tMakeHole(hitPos, 2.5, 2.0, 1.5)
\t\t\t\t\tSpawnFire(hitPos)
\t\t\t\t\tExplosion(hitPos, 1.5)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "flamecannon" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tif InputDown("usetool", p) and flameSnd then
\t\t\t\tPlayLoop(flameSnd, t.pos, 1.0)
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 7. Black Hole Singularity ---
def update_black_hole():
    mod_name = 'Black_Hole_Singularity'
    copy_snd(mod_name, ['gas', 'laser'])
    lua = '''#version 2
#include "script/include/player.lua"

local singSnd

function server.init()
\tRegisterTool("blackhole", "Black Hole Singularity Cannon", "MOD/vox/weapon.vox", 2)
\tSetToolAmmoPickupAmount("blackhole", 50)
\tSetBool("game.tool.blackhole.enabled", true)
end

function client.init()
\tsingSnd = LoadLoop("MOD/snd/gas.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("blackhole", true, p)
\t\tSetToolAmmo("blackhole", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "blackhole" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("blackhole", p) < 50 then SetToolAmmo("blackhole", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tfor i = 1, 30 do
\t\t\t\t\tMakeHole(hitPos, 8.0, 7.0, 6.0)
\t\t\t\tend
\t\t\t\tPointLight(hitPos, 0.7, 0.1, 1.0, 15.0)
\t\t\t\tExplosion(hitPos, 8.0)

\t\t\t\tParticleReset()
\t\t\t\tParticleType("plain")
\t\t\t\tParticleColor(0.6, 0.1, 0.9, 0.1, 0.0, 0.2)
\t\t\t\tParticleRadius(0.3, 0.05)
\t\t\t\tParticleEmissive(10, 0)
\t\t\t\tfor i = 1, 30 do
\t\t\t\t\tlocal off = Vec(math.random(-8,8), math.random(1,8), math.random(-8,8))
\t\t\t\t\tlocal startP = VecAdd(hitPos, off)
\t\t\t\t\tlocal inward = VecScale(VecNormalize(VecSub(hitPos, startP)), 12)
\t\t\t\t\tSpawnParticle(startP, inward, 0.6)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "blackhole" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.6))
\t\t\t\tDrawLine(muzzle, hitPos, 0.7, 0.2, 1.0, 1.0)
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 8. Meteor Shower Celestial Strike ---
def update_meteor():
    mod_name = 'Meteor_Shower_Strike'
    copy_snd(mod_name, ['rocket', 'shot_heavy'])
    lua = '''#version 2
#include "script/include/player.lua"

local roarSnd

function server.init()
\tRegisterTool("meteorshower", "Meteor Shower Celestial Strike", "MOD/vox/weapon.vox", 5)
\tSetToolAmmoPickupAmount("meteorshower", 50)
\tSetBool("game.tool.meteorshower.enabled", true)
end

function client.init()
\troarSnd = LoadSound("MOD/snd/rocket.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("meteorshower", true, p)
\t\tSetToolAmmo("meteorshower", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "meteorshower" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("meteorshower", p) < 50 then SetToolAmmo("meteorshower", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal center = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tfor i = 1, 10 do
\t\t\t\t\tlocal off = Vec(math.random(-15, 15), 0, math.random(-15, 15))
\t\t\t\t\tlocal target = VecAdd(center, off)
\t\t\t\t\tlocal skyPos = VecAdd(target, Vec(math.random(-10, 10), 70 + i*3, math.random(-10, 10)))
\t\t\t\t\tMakeHole(target, 6.0, 5.0, 4.0)
\t\t\t\t\tExplosion(target, 7.0)
\t\t\t\t\tSpawnFire(target)

\t\t\t\t\tParticleReset()
\t\t\t\t\tParticleType("smoke")
\t\t\t\t\tParticleColor(1.0, 0.4, 0.1, 0.2, 0.2, 0.2)
\t\t\t\t\tParticleRadius(0.8, 2.5)
\t\t\t\t\tParticleAlpha(0.9, 0.0)
\t\t\t\t\tfor y = 0, 30, 5 do
\t\t\t\t\t\tlocal sp = VecLerp(skyPos, target, y/30)
\t\t\t\t\t\tSpawnParticle(sp, Vec(0, 2, 0), 1.5)
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "meteorshower" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.35))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal center = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tfor i = 1, 8 do
\t\t\t\t\tlocal off = Vec(math.random(-15, 15), 0, math.random(-15, 15))
\t\t\t\t\tlocal target = VecAdd(center, off)
\t\t\t\t\tlocal skyPos = VecAdd(target, Vec(math.random(-8, 8), 70, math.random(-8, 8)))
\t\t\t\t\tDrawLine(skyPos, target, 1.0, 0.4, 0.1, 1.0)
\t\t\t\tend
\t\t\t\tif roarSnd then PlaySound(roarSnd, center, 2.5) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 9. MIRV Cluster Bomb Launcher ---
def update_cluster_bomb():
    mod_name = 'Cluster_Bomb_Launcher'
    copy_snd(mod_name, ['rocket', 'shot'])
    lua = '''#version 2
#include "script/include/player.lua"

local popSnd

function server.init()
\tRegisterTool("clusterbomb", "MIRV Cluster Bomb Launcher", "MOD/vox/weapon.vox", 6)
\tSetToolAmmoPickupAmount("clusterbomb", 50)
\tSetBool("game.tool.clusterbomb.enabled", true)
end

function client.init()
\tpopSnd = LoadSound("MOD/snd/rocket.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("clusterbomb", true, p)
\t\tSetToolAmmo("clusterbomb", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "clusterbomb" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("clusterbomb", p) < 50 then SetToolAmmo("clusterbomb", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tShoot(t.pos, fwd, "rocket", 1.8)
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tExplosion(hitPos, 7.0)
\t\t\t\tfor i = 1, 14 do
\t\t\t\t\tlocal off = Vec(math.random(-8, 8), math.random(1, 5), math.random(-8, 8))
\t\t\t\t\tlocal subPos = VecAdd(hitPos, off)
\t\t\t\t\tExplosion(subPos, 4.0)
\t\t\t\t\tParticleReset()
\t\t\t\t\tParticleType("spark")
\t\t\t\t\tParticleColor(1.0, 0.7, 0.2, 1.0, 0.1, 0.0)
\t\t\t\t\tParticleRadius(0.1, 0.02)
\t\t\t\t\tfor s = 1, 8 do
\t\t\t\t\t\tSpawnParticle(subPos, Vec(math.random(-8,8), math.random(2,8), math.random(-8,8)), 0.6)
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "clusterbomb" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tif InputPressed("usetool", p) and popSnd then
\t\t\t\tPlaySound(popSnd, t.pos, 1.8)
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 10. Gravity Shockwave Repulsor ---
def update_repulsor():
    mod_name = 'Gravity_Shockwave_Repulsor'
    copy_snd(mod_name, ['shot_heavy'])
    lua = '''#version 2
#include "script/include/player.lua"

local shockSnd

function server.init()
\tRegisterTool("repulsor", "Gravity Shockwave Repulsor", "MOD/vox/weapon.vox", 8)
\tSetToolAmmoPickupAmount("repulsor", 50)
\tSetBool("game.tool.repulsor.enabled", true)
end

function client.init()
\tshockSnd = LoadSound("MOD/snd/shot_heavy.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("repulsor", true, p)
\t\tSetToolAmmo("repulsor", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "repulsor" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("repulsor", p) < 50 then SetToolAmmo("repulsor", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))

\t\t\tif InputPressed("usetool", p) then
\t\t\t\tfor dist = 2, 35, 3 do
\t\t\t\t\tlocal pPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\t\tExplosion(pPos, 3.5)
\t\t\t\t\tPointLight(pPos, 0.4, 0.7, 1.0, 10.0)

\t\t\t\t\tParticleReset()
\t\t\t\t\tParticleType("smoke")
\t\t\t\t\tParticleColor(0.6, 0.8, 1.0, 0.2, 0.2, 0.2)
\t\t\t\t\tParticleRadius(0.5, 2.0)
\t\t\t\t\tParticleAlpha(0.7, 0.0)
\t\t\t\t\tfor i = 1, 5 do
\t\t\t\t\t\tlocal vel = Vec(math.random(-8,8), math.random(1,6), math.random(-8,8))
\t\t\t\t\t\tSpawnParticle(pPos, vel, 0.8)
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "repulsor" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.26, -0.44, -0.4))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tif InputPressed("usetool", p) then
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.6))
\t\t\t\tlocal target = VecAdd(t.pos, VecScale(fwd, 35))
\t\t\t\tDrawLine(muzzle, target, 0.4, 0.8, 1.0, 1.0)
\t\t\t\tif shockSnd then PlaySound(shockSnd, muzzle, 2.0) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 11. Voxel Vacuum Gun ---
def update_vacuum_gun():
    mod_name = 'Voxel_Vacuum_Gun'
    copy_snd(mod_name, ['gas'])
    lua = '''#version 2
#include "script/include/player.lua"

local vacSnd

function server.init()
\tRegisterTool("vacuumgun", "Voxel Vacuum Dissolver", "MOD/vox/weapon.vox", 8)
\tSetToolAmmoPickupAmount("vacuumgun", 50)
\tSetBool("game.tool.vacuumgun.enabled", true)
end

function client.init()
\tvacSnd = LoadLoop("MOD/snd/gas.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("vacuumgun", true, p)
\t\tSetToolAmmo("vacuumgun", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "vacuumgun" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("vacuumgun", p) < 50 then SetToolAmmo("vacuumgun", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputDown("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tMakeHole(hitPos, 4.0, 3.5, 2.5)
\t\t\t\tPointLight(hitPos, 0.3, 0.9, 0.7, 8.0)

\t\t\t\tParticleReset()
\t\t\t\tParticleType("plain")
\t\t\t\tParticleColor(0.2, 0.9, 0.8, 0.1, 0.1, 0.1)
\t\t\t\tParticleRadius(0.12, 0.02)
\t\t\t\tParticleEmissive(8, 0)
\t\t\t\tfor i = 1, 8 do
\t\t\t\t\tlocal vel = VecScale(VecNormalize(VecSub(t.pos, hitPos)), 10)
\t\t\t\t\tSpawnParticle(hitPos, vel, 0.5)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "vacuumgun" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.44, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputDown("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tlocal muzzle = VecAdd(t.pos, VecScale(fwd, 0.6))
\t\t\t\tDrawLine(muzzle, hitPos, 0.2, 0.9, 0.8, 1.0)
\t\t\t\tif vacSnd then PlayLoop(vacSnd, t.pos, 1.0) end
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 12. C4 Remote Explosive ---
def update_c4():
    mod_name = 'C4_Remote_Explosive'
    copy_snd(mod_name, ['spark', 'shot_heavy'])
    lua = '''#version 2
#include "script/include/player.lua"

local beepSnd

function server.init()
\tRegisterTool("c4bomb", "C4 Remote Sticky Explosives", "MOD/vox/weapon.vox", 4)
\tSetToolAmmoPickupAmount("c4bomb", 50)
\tSetBool("game.tool.c4bomb.enabled", true)
end

function client.init()
\tbeepSnd = LoadSound("MOD/snd/spark.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("c4bomb", true, p)
\t\tSetToolAmmo("c4bomb", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "c4bomb" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("c4bomb", p) < 50 then SetToolAmmo("c4bomb", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\t-- Left Click: Plant C4
\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tPointLight(hitPos, 1.0, 0.1, 0.1, 8.0)
\t\t\t\tMakeHole(hitPos, 1.5, 1.5, 1.0)
\t\t\tend

\t\t\t-- Right Click: Detonate
\t\t\tif InputPressed("grab", p) and hit then
\t\t\t\tlocal hitPos = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tExplosion(hitPos, 10.0)
\t\t\t\tfor i = 1, 6 do
\t\t\t\t\tlocal off = Vec(math.random(-4, 4), math.random(0, 3), math.random(-4, 4))
\t\t\t\t\tExplosion(VecAdd(hitPos, off), 5.0)
\t\t\t\tend
\t\t\t\tParticleReset()
\t\t\t\tParticleType("smoke")
\t\t\t\tParticleColor(0.3, 0.3, 0.3, 0.1, 0.1, 0.1)
\t\t\t\tParticleRadius(1.0, 3.5)
\t\t\t\tParticleAlpha(0.8, 0.0)
\t\t\t\tfor i = 1, 10 do
\t\t\t\t\tSpawnParticle(hitPos, Vec(math.random(-5,5), math.random(2,8), math.random(-5,5)), 1.5)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "c4bomb" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tif InputPressed("usetool", p) and beepSnd then
\t\t\t\tPlaySound(beepSnd, t.pos, 1.5)
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 13. Airstrike Radio Beacon ---
def update_airstrike():
    mod_name = 'Airstrike_Radio_Beacon'
    copy_snd(mod_name, ['spark', 'rocket'])
    lua = '''#version 2
#include "script/include/player.lua"

local radioSnd

function server.init()
\tRegisterTool("airstrike", "Tactical Airstrike Beacon", "MOD/vox/weapon.vox", 5)
\tSetToolAmmoPickupAmount("airstrike", 50)
\tSetBool("game.tool.airstrike.enabled", true)
end

function client.init()
\tradioSnd = LoadSound("MOD/snd/spark.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("airstrike", true, p)
\t\tSetToolAmmo("airstrike", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "airstrike" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("airstrike", p) < 50 then SetToolAmmo("airstrike", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tlocal fwd = TransformToParentVec(t, Vec(0, 0, -1))
\t\t\tlocal hit, dist = QueryRaycast(t.pos, fwd, 500)

\t\t\tif InputPressed("usetool", p) and hit then
\t\t\t\tlocal target = VecAdd(t.pos, VecScale(fwd, dist))
\t\t\t\tPointLight(target, 1.0, 0.1, 0.1, 15.0)
\t\t\t\tfor i = 1, 12 do
\t\t\t\t\tlocal off = Vec(math.random(-10, 10), 0, math.random(-10, 10))
\t\t\t\t\tlocal hitPos = VecAdd(target, off)
\t\t\t\t\tExplosion(hitPos, 7.0)
\t\t\t\t\tSpawnFire(hitPos)
\t\t\t\t\tParticleReset()
\t\t\t\t\tParticleType("smoke")
\t\t\t\t\tParticleColor(0.7, 0.3, 0.1, 0.2, 0.2, 0.2)
\t\t\t\t\tParticleRadius(0.8, 2.5)
\t\t\t\t\tParticleAlpha(0.8, 0.0)
\t\t\t\t\tSpawnParticle(hitPos, Vec(0, 6, 0), 2.0)
\t\t\t\tend
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "airstrike" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tif InputPressed("usetool", p) and radioSnd then
\t\t\t\tPlaySound(radioSnd, t.pos, 2.0)
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

# --- 14. Chrono Time Disruptor ---
def update_chrono():
    mod_name = 'Chrono_Time_Disruptor'
    copy_snd(mod_name, ['spin'])
    lua = '''#version 2
#include "script/include/player.lua"

local spinSnd

function server.init()
\tRegisterTool("chronogun", "Chrono Time Disruptor (Slow-Mo)", "MOD/vox/weapon.vox", 0)
\tSetToolAmmoPickupAmount("chronogun", 50)
\tSetBool("game.tool.chronogun.enabled", true)
end

function client.init()
\tspinSnd = LoadSound("MOD/snd/spin.ogg")
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tSetToolEnabled("chronogun", true, p)
\t\tSetToolAmmo("chronogun", 999, p)
\tend

\tfor p in Players() do
\t\tif GetPlayerTool(p) == "chronogun" and GetPlayerVehicle(p) == 0 then
\t\t\tif GetToolAmmo("chronogun", p) < 50 then SetToolAmmo("chronogun", 999, p) end

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tif InputPressed("usetool", p) then
\t\t\t\tif not IsMultiplayer() then SetTimeScale(0.2) end
\t\t\t\tPointLight(t.pos, 0.1, 1.0, 0.4, 10.0)
\t\t\tend
\t\t\tif InputPressed("grab", p) then
\t\t\t\tif not IsMultiplayer() then SetTimeScale(1.0) end
\t\t\t\tPointLight(t.pos, 1.0, 1.0, 1.0, 10.0)
\t\t\tend
\t\tend
\tend
end

function client.tick(dt)
\tfor p in Players() do
\t\tif GetPlayerTool(p) == "chronogun" and GetPlayerVehicle(p) == 0 then
\t\t\tlocal toolTransform = Transform(Vec(0.25, -0.42, -0.38))
\t\t\tSetToolTransform(toolTransform, 1.0, p)

\t\t\tlocal t = GetPlayerCameraTransform(p)
\t\t\tif (InputPressed("usetool", p) or InputPressed("grab", p)) and spinSnd then
\t\t\t\tPlaySound(spinSnd, t.pos, 1.5)
\t\t\tend
\t\tend
\tend
end
'''
    with open(os.path.join(GAME_MODS, mod_name, 'main.lua'), 'w', encoding='utf-8') as f:
        f.write(lua)
    print(f'[EFFECTS ADDED] {mod_name}')

def main():
    print("=== ADDING AUDIO, VISUAL, AND PARTICLE EFFECTS TO ALL 14 WEAPONS ===")
    update_orbital_laser()
    update_plasma_rifle()
    update_railgun()
    update_mjolnir()
    update_nuke()
    update_flame_cannon()
    update_black_hole()
    update_meteor()
    update_cluster_bomb()
    update_repulsor()
    update_vacuum_gun()
    update_c4()
    update_airstrike()
    update_chrono()

    print("\n=== SYNCING TO DOCUMENTS/TEARDOWN/MODS ===")
    weapons = [
        'Airstrike_Radio_Beacon', 'Black_Hole_Singularity', 'C4_Remote_Explosive',
        'Chrono_Time_Disruptor', 'Cluster_Bomb_Launcher', 'Gravity_Shockwave_Repulsor',
        'Hyper_Precision_Railgun', 'Meteor_Shower_Strike', 'Mjolnir_Thunder_Hammer',
        'Orbital_Laser_Strike', 'Plasma_Disintegrator_Rifle', 'Tactical_Nuke_Launcher',
        'Thermobaric_Flame_Cannon', 'Voxel_Vacuum_Gun'
    ]
    for w in weapons:
        src = os.path.join(GAME_MODS, w)
        dst = os.path.join(DOCS_MODS, w)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print("\n=== SYNCING TO DESKTOP PACK FOR FRIEND ===")
    for w in weapons:
        src = os.path.join(GAME_MODS, w)
        dst = os.path.join(DESKTOP_PACK, w)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print("\n=== RE-PACKAGING DESKTOP ZIP ARCHIVE ===")
    if os.path.exists(DESKTOP_ZIP):
        os.remove(DESKTOP_ZIP)

    with zipfile.ZipFile(DESKTOP_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(DESKTOP_PACK):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, DESKTOP_PACK)
                zf.write(full, rel)

    stat = os.stat(DESKTOP_ZIP)
    print(f'[CREATED NEW ZIP WITH ALL SOUNDS & EFFECTS] {DESKTOP_ZIP} ({stat.st_size / (1024*1024):.2f} MB)')
    print("\nALL WEAPON EFFECTS UPGRADES COMPLETED!")

if __name__ == '__main__':
    main()
