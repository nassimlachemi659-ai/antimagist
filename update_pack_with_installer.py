import os
import shutil
import zipfile

pack_dir = r'C:\Users\nst\Desktop\Teardown_Mods_Pack_For_Friend'
zip_path = r'C:\Users\nst\Desktop\Teardown_Mods_Pack.zip'

bat_content = """@echo off
title Teardown Mod Pack Auto-Installer
color 0b
echo =======================================================
echo     TEARDOWN ULTIMATE MOD PACK AUTO-INSTALLER
echo =======================================================
echo.
echo Installing all 22 verified and tested mods...
echo This replaces old files to prevent any MOD SYNC MISMATCH!
echo.

set "DOCS_MODS=%USERPROFILE%\\Documents\\Teardown\\mods"
if not exist "%DOCS_MODS%" mkdir "%DOCS_MODS%"

echo [*] Copying to %DOCS_MODS%...
for /d %%D in (*) do (
    if exist "%%D\\main.lua" (
        echo   - Updating %%D...
        if exist "%DOCS_MODS%\\%%D" rmdir /s /q "%DOCS_MODS%\\%%D"
        xcopy "%%D" "%DOCS_MODS%\\%%D\\" /E /I /Q /Y >nul
    )
    if exist "%%D\\main.xml" (
        echo   - Updating %%D...
        if exist "%DOCS_MODS%\\%%D" rmdir /s /q "%DOCS_MODS%\\%%D"
        xcopy "%%D" "%DOCS_MODS%\\%%D\\" /E /I /Q /Y >nul
    )
)

echo.
echo =======================================================
echo [IMPORTANT FOR ONLINE-FIX / CRACKED PLAYERS]:
echo If your Teardown game has its own 'mods' folder:
echo (Example: [Game Folder]\\Teardown\\mods\\)
echo.
echo 1. Delete the old mod folders from [Game Folder]\\Teardown\\mods\\
echo 2. Copy the 22 mod folders from here into [Game Folder]\\Teardown\\mods\\
echo =======================================================
echo.
echo [DONE] Installation complete! Launch Teardown and enjoy!
echo.
pause
"""

bat_path = os.path.join(pack_dir, 'AUTO_INSTALL_FOR_FRIEND.bat')
with open(bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_content)

how_to_path = os.path.join(pack_dir, 'HOW_TO_INSTALL.txt')
how_to_content = """==================================================
TEARDOWN ULTIMATE MOD PACK (22 VERIFIED & TESTED MODS)
==================================================

8 EPIC MAPS:
1. Boeing 737 Burning Edition (Burning passenger jet on runway)
2. Gwel's High Skyscraper (5-story modern office skyscraper)
3. Mega Destruction Metropolis (Huge urban city sandbox)
4. Nuclear Power Plant Complex (Two 60m cooling towers & reactor dome)
5. Military Mountain Airbase & Silo (Concrete mountain bunker & radar)
6. Mega Ocean Port & Bridge (Deep sea harbor & 100m suspension bridge)
7. Skyscraper Construction Site & Cranes (70m steel frame & two 80m cranes)
8. Suburban Town & Gas Station Chaos (6 residential homes & explosive gas station)

14 DESTRUCTIVE WEAPONS (ALL FIXED VIEWMODEL POSITIONING):
1. Orbital Laser Strike [Key 1] - Continuous laser [LMB] & sky ion nuke [RMB]
2. Plasma Disintegrator Rifle [Key 1] - Rapid blue plasma bolts that melt voxels
3. Black Hole Singularity Cannon [Key 2] - Gravitational vortex implosion
4. Mjolnir Thunder Hammer [Key 3] - Godly lightning shockwave hammer
5. Hyper Precision Railgun [Key 4] - 120m penetration kinetic slug
6. C4 Remote Sticky Explosives [Key 4] - [LMB] Plant sticky C4 | [RMB] Detonate
7. Tactical Airstrike Beacon [Key 5] - Calls 12-missile artillery strike
8. Meteor Shower Celestial Strike [Key 5] - Summons falling flaming meteors
9. MIRV Cluster Bomb Launcher [Key 6] - Scatters 14 explosive sub-bomblets
10. Thermobaric Flame Cannon [Key 7] - High-temp melting flame stream
11. Gravity Shockwave Repulsor [Key 8] - Concussive kinetic physics pulse
12. Voxel Vacuum Dissolver [Key 8] - Vaporizes and dissolves walls into thin air
13. Tactical Nuke Launcher (Fat Man) [Key 9] - 35m vaporizing nuclear fireball
14. Chrono Time Disruptor [Key 0] - [LMB] Slow Motion 0.2x | [RMB] Normal Speed

--------------------------------------------------
HOW TO INSTALL:
--------------------------------------------------
OPTION A (Automatic):
- Double click AUTO_INSTALL_FOR_FRIEND.bat

OPTION B (Manual):
- Copy all 22 mod folders directly into:
  * If Cracked / Online-Fix: Your Teardown\\mods\\ folder (e.g. S:\\Teardown\\...\\mods)
  * If Steam: C:\\Users\\<Username>\\Documents\\Teardown\\mods\\

--------------------------------------------------
HOW TO FIX "MOD SYNC ERROR / NOT IDENTICAL":
--------------------------------------------------
If your friend gets "Mod sync mismatch / not identical" (e.g. Tactical Airstrike Beacon):
1. Why this happens:
   The friend has an OLDER or duplicate version of the mod in their folder!
2. How to fix:
   a) In the friend's computer, open their Teardown\\mods\\ folder AND Documents\\Teardown\\mods\\.
   b) Delete the old 'Airstrike_Radio_Beacon' (or delete all old mod folders).
   c) Copy the FRESH folder from this pack into Teardown\\mods\\.
   d) Both players will now have the exact same file hash and connect instantly!

--------------------------------------------------
HOW TO PLAY:
--------------------------------------------------
1. Launch Teardown.
2. Go to Main Menu -> MODS.
3. Click any map and hit PLAY.
4. All default weapons and mod weapons have unlimited ammo and are ready!
==================================================
"""

with open(how_to_path, 'w', encoding='utf-8') as f:
    f.write(how_to_content)

print('[UPDATED] AUTO_INSTALL_FOR_FRIEND.bat and HOW_TO_INSTALL.txt')

# Re-create ZIP
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(pack_dir):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, pack_dir)
            zf.write(full, rel)

stat = os.stat(zip_path)
print(f'[CREATED NEW ZIP] {zip_path} ({stat.st_size / (1024*1024):.2f} MB)')
