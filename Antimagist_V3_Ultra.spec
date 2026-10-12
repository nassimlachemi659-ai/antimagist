# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['antimagist_v3_ultra.py'],
    pathex=[],
    binaries=[],
    datas=[('antimagist.ico', '.')],
    hiddenimports=['customtkinter', 'pystray', 'PIL', 'psutil', 'requests'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Antimagist_V3_Ultra',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['antimagist.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Antimagist_V3_Ultra',
)
