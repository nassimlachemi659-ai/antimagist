# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/nst/.gemini/antigravity/scratch/antimagist_v4_apex.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/nst/.gemini/antigravity/scratch/antimagist.ico', '.'), ('C:/Users/nst/.gemini/antigravity/scratch/antimagist_mobile_qr.png', '.')],
    hiddenimports=['customtkinter', 'pystray', 'PIL', 'psutil', 'requests', 'qrcode', 'win32com.client', 'winreg', 'keyboard', 'winsound', 'ctypes', 'display_reflex', 'audio_stripper', 'server_radar', 'benchmark_card', 'mod_guard', 'esports_profiles', 'frametime_sentinel', 'discord_webhook', 'dpc_diagnostician', 'process_isolator', 'auto_updater', 'usb_polling_sentinel', 'memory_pacer', 'throttle_watchdog', 'lan_sync', 'msi_interrupt_tuner', 'shader_sentinel', 'anticheat_guard', 'profile_switcher', 'latency_recorder', 'recall_stripper', 'bufferbloat_auditor', 'tournament_lock', 'predictive_interceptor', 'packet_racer', 'tpm_hardware_attestor', 'ghost_os_cryo', 'devops_turbo', 'battery_whisper', 'studio_master', 'privacy_scrubber', 'storage_accelerator', 'ultra_game_sentinel', 'web_bridge_daemon', 'floating_game_bar', 'detonation_chamber', 'windows_stripper', 'context_menu_v4', 'cs2_optimizer', 'ai_kernel_agent', 'game_watchdog', 'tray_manager', 'hud_overlay', 'ping_optimizer', 'kernel_timer_resolution', 'system_state_vault', 'antimagist_v3_ultra', 'crash_guard', 'global_hotkey_engine', 'bandwidth_guard'],
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
    name='Antimagist_Enterprise',
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
    uac_admin=True,
    icon=['C:/Users/nst/.gemini/antigravity/scratch/antimagist.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Antimagist_Enterprise',
)
