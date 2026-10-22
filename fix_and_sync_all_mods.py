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

# 1. FIX WEAPONS: Remove SetToolTransform from server.tick, ensure client.tick has it, ensure server.init sets game.tool.<id>.enabled
def fix_weapon(w_name):
    main_path = os.path.join(GAME_MODS, w_name, 'main.lua')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into lines
    lines = content.splitlines()
    new_lines = []
    in_server_tick = False
    in_client_tick = False

    tool_id = None
    for l in lines:
        m = re.search(r'RegisterTool\s*\(\s*"([^"]+)"', l)
        if m:
            tool_id = m.group(1)
            break

    for l in lines:
        if 'function server.tick' in l:
            in_server_tick = True
            in_client_tick = False
        elif 'function client.tick' in l:
            in_server_tick = False
            in_client_tick = True
        elif 'function server.init' in l:
            in_server_tick = False
            in_client_tick = False

        # In server.tick, filter out SetToolTransform and toolTransform declaration
        if in_server_tick:
            if 'SetToolTransform' in l:
                continue
            if 'local toolTransform = Transform' in l:
                continue
            if '-- Position tool in bottom right' in l:
                continue
            # Replace PlayersAdded() with Players() so tools are constantly active and replenished
            if 'for p in PlayersAdded() do' in l:
                l = l.replace('for p in PlayersAdded() do', 'for p in Players() do')

        # In server.init, ensure SetBool("game.tool.<id>.enabled", true) is present
        if 'SetToolAmmoPickupAmount' in l and tool_id:
            new_lines.append(l)
            new_lines.append(f'\tSetBool("game.tool.{tool_id}.enabled", true)')
            continue

        new_lines.append(l)

    fixed_code = '\n'.join(new_lines) + '\n'
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    print(f'[FIXED WEAPON] {w_name}')

# 2. FIX MAPS: Provide sandbox.lua and main.lua
SANDBOX_LUA_CONTENT = """#version 2
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
\tlocal tools = ListKeys("game.tool")
\tfor i = 1, #tools do
\t\tfor p in Players() do
\t\t\tSetToolEnabled(tools[i], true, p)
\t\t\tSetToolAmmo(tools[i], 9999, p)
\t\tend
\tend
end
"""

MAIN_LUA_DEFAULT = """#version 2

function server.init()
end

function client.init()
end
"""

def fix_map(m_name):
    m_dir = os.path.join(GAME_MODS, m_name)
    sb_path = os.path.join(m_dir, 'sandbox.lua')
    with open(sb_path, 'w', encoding='utf-8') as f:
        f.write(SANDBOX_LUA_CONTENT)

    main_path = os.path.join(m_dir, 'main.lua')
    if not os.path.exists(main_path):
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(MAIN_LUA_DEFAULT)
    else:
        # Check if #version 2 is in main.lua
        with open(main_path, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
        if '#version 2' not in c:
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write('#version 2\n' + c)

    print(f'[FIXED MAP] {m_name}')

# Fix Gwels doors and elevator scripts for multiplayer
def fix_gwels_scripts():
    doors_path = os.path.join(GAME_MODS, 'Gwels_High_Skyscraper', 'scripts', 'doors.lua')
    if os.path.exists(doors_path):
        with open(doors_path, 'r', encoding='utf-8') as f:
            dc = f.read()
        if '#version 2' not in dc:
            wrap_doors = "#version 2\n" + dc + "\n\nfunction server.init()\n\tinit()\nend\n\nfunction server.tick(dt)\n\tupdate(dt)\nend\n"
            with open(doors_path, 'w', encoding='utf-8') as f:
                f.write(wrap_doors)
            print('[FIXED GWELS DOORS]')

    elev_path = os.path.join(GAME_MODS, 'Gwels_High_Skyscraper', 'scripts', 'elevator.lua')
    if os.path.exists(elev_path):
        with open(elev_path, 'r', encoding='utf-8') as f:
            ec = f.read()
        if '#version 2' not in ec:
            wrap_elev = "#version 2\n" + ec + "\n\nfunction server.init()\n\tinit()\nend\n\nfunction server.tick(dt)\n\ttick(dt)\nend\n"
            with open(elev_path, 'w', encoding='utf-8') as f:
                f.write(wrap_elev)
            print('[FIXED GWELS ELEVATOR]')

def main():
    print("=== APPLYING MOD FIXES ===")
    for w in WEAPONS:
        fix_weapon(w)
    for m in MAPS:
        fix_map(m)
    fix_gwels_scripts()

    print("\n=== SYNCING TO DOCUMENTS/TEARDOWN/MODS ===")
    os.makedirs(DOCS_MODS, exist_ok=True)
    all_22 = MAPS + WEAPONS
    for item in all_22:
        src = os.path.join(GAME_MODS, item)
        dst = os.path.join(DOCS_MODS, item)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f'[SYNCED DOCS] {item}')

    print("\n=== SYNCING TO DESKTOP PACK FOR FRIEND ===")
    os.makedirs(DESKTOP_PACK, exist_ok=True)
    for item in all_22:
        src = os.path.join(GAME_MODS, item)
        dst = os.path.join(DESKTOP_PACK, item)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f'[SYNCED DESKTOP PACK] {item}')

    print("\n=== CREATING CLEAN DESKTOP ZIP ARCHIVE ===")
    if os.path.exists(DESKTOP_ZIP):
        os.remove(DESKTOP_ZIP)

    with zipfile.ZipFile(DESKTOP_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add HOW_TO_INSTALL.txt at zip root
        how_to = os.path.join(DESKTOP_PACK, 'HOW_TO_INSTALL.txt')
        if os.path.exists(how_to):
            zf.write(how_to, 'HOW_TO_INSTALL.txt')
        for item in all_22:
            base_dir = os.path.join(DESKTOP_PACK, item)
            for root, dirs, files in os.walk(base_dir):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, DESKTOP_PACK)
                    zf.write(full, rel)

    stat = os.stat(DESKTOP_ZIP)
    print(f'[CREATED ZIP] {DESKTOP_ZIP} ({stat.st_size / (1024*1024):.2f} MB)')
    print("\nALL OPERATIONS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
