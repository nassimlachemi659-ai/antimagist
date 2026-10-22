import os
import shutil
import zipfile
import re

GAME_MODS = r'S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods'
DOCS_MODS = r'C:\Users\nst\Documents\Teardown\mods'
DESKTOP_PACK = r'C:\Users\nst\Desktop\Teardown_Mods_Pack_For_Friend'
DESKTOP_ZIP = r'C:\Users\nst\Desktop\Teardown_Mods_Pack.zip'

MAPS = [
    'Boeing_737_Burning_Edition',
    'Gwels_High_Skyscraper',
    'Mega_Destruction_Metropolis',
    'Nuclear_Power_Plant',
    'Military_Fort_Airbase',
    'Mega_Ocean_Port_Bridge',
    'Skyscraper_Construction_Site',
    'Suburban_Town_Chaos'
]

WEAPONS = [
    'Airstrike_Radio_Beacon',
    'Black_Hole_Singularity',
    'C4_Remote_Explosive',
    'Chrono_Time_Disruptor',
    'Cluster_Bomb_Launcher',
    'Gravity_Shockwave_Repulsor',
    'Hyper_Precision_Railgun',
    'Meteor_Shower_Strike',
    'Mjolnir_Thunder_Hammer',
    'Orbital_Laser_Strike',
    'Plasma_Disintegrator_Rifle',
    'Tactical_Nuke_Launcher',
    'Thermobaric_Flame_Cannon',
    'Voxel_Vacuum_Gun'
]

# Optimize Weapons: ONLY call SetToolEnabled/SetToolAmmo in PlayersAdded() or on low ammo. NEVER spam per frame!
def optimize_weapon(w_name):
    main_path = os.path.join(GAME_MODS, w_name, 'main.lua')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []
    in_server_tick = False

    tool_id = None
    for l in lines:
        m = re.search(r'RegisterTool\s*\(\s*"([^"]+)"', l)
        if m:
            tool_id = m.group(1)
            break

    i = 0
    while i < len(lines):
        l = lines[i]
        if 'function server.tick' in l:
            in_server_tick = True
            new_lines.append(l)
            # Add network-optimized player registration
            new_lines.append('\tfor p in PlayersAdded() do')
            new_lines.append(f'\t\tSetToolEnabled("{tool_id}", true, p)')
            new_lines.append(f'\t\tSetToolAmmo("{tool_id}", 999, p)')
            new_lines.append('\tend')
            i += 1
            # Skip old for p in Players() / PlayersAdded() tool enabling block
            if i < len(lines) and ('for p in Players()' in lines[i] or 'for p in PlayersAdded()' in lines[i]):
                i += 1
                while i < len(lines) and 'end' not in lines[i]:
                    i += 1
                if i < len(lines) and 'end' in lines[i]:
                    i += 1
            continue

        if in_server_tick and f'GetPlayerTool(p) == "{tool_id}"' in l:
            new_lines.append(l)
            # Refill ammo only if low, to save network packets
            new_lines.append(f'\t\t\tif GetToolAmmo("{tool_id}", p) < 50 then SetToolAmmo("{tool_id}", 999, p) end')
            i += 1
            continue

        if 'function client.tick' in l:
            in_server_tick = False

        new_lines.append(l)
        i += 1

    # Special handling for Chrono_Time_Disruptor: avoid breaking lockstep in MP
    if w_name == 'Chrono_Time_Disruptor':
        fixed_text = '\n'.join(new_lines)
        fixed_text = fixed_text.replace('SetTimeScale(0.2)', 'if not IsMultiplayer() then SetTimeScale(0.2) end')
        fixed_text = fixed_text.replace('SetTimeScale(1.0)', 'if not IsMultiplayer() then SetTimeScale(1.0) end')
        new_lines = fixed_text.splitlines()

    fixed_code = '\n'.join(new_lines) + '\n'
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    print(f'[OPTIMIZED WEAPON NETCODE] {w_name}')

# Optimize Map sandbox.lua: Do NOT spam 80 RPCs every frame!
SANDBOX_LUA_OPTIMIZED = """#version 2
#include "script/sandbox.lua"

local _base_server_init = server.init
function server.init()
\tif _base_server_init then _base_server_init() end
\tif setupToolsUpgradedFully then
\t\tsetupToolsUpgradedFully()
\tend
\tlocal tools = ListKeys("game.tool")
\tfor i = 1, #tools do
\t\tSetBool("game.tool." .. tools[i] .. ".enabled", true, true)
\t\tSetInt("game.tool." .. tools[i] .. ".ammo", 9999, true)
\tend
end

local _base_server_tick = server.tick
function server.tick(dt)
\tif _base_server_tick then _base_server_tick(dt) end
\tfor p in PlayersAdded() do
\t\tlocal tools = ListKeys("game.tool")
\t\tfor i = 1, #tools do
\t\t\tSetToolEnabled(tools[i], true, p)
\t\t\tSetToolAmmo(tools[i], 9999, p)
\t\tend
\tend
end
"""

def optimize_map(m_name):
    sb_path = os.path.join(GAME_MODS, m_name, 'sandbox.lua')
    with open(sb_path, 'w', encoding='utf-8') as f:
        f.write(SANDBOX_LUA_OPTIMIZED)
    print(f'[OPTIMIZED MAP NETCODE] {m_name}')

def main():
    print("=== OPTIMIZING NETWORK TRAFFIC ACROSS ALL MODS ===")
    for w in WEAPONS:
        optimize_weapon(w)
    for m in MAPS:
        optimize_map(m)

    print("\n=== SYNCING TO DOCUMENTS/TEARDOWN/MODS ===")
    all_22 = MAPS + WEAPONS
    for item in all_22:
        src = os.path.join(GAME_MODS, item)
        dst = os.path.join(DOCS_MODS, item)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print("\n=== SYNCING TO DESKTOP PACK FOR FRIEND ===")
    for item in all_22:
        src = os.path.join(GAME_MODS, item)
        dst = os.path.join(DESKTOP_PACK, item)
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
    print(f'[CREATED OPTIMIZED ZIP] {DESKTOP_ZIP} ({stat.st_size / (1024*1024):.2f} MB)')
    print("\nALL NETCODE OPTIMIZATIONS COMPLETED!")

if __name__ == '__main__':
    main()
