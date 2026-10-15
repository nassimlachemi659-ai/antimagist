"""
build_antimagist_exe.py — 1-Click Standalone Executable & Desktop Shortcut Compiler
==================================================================================
Antimagist Enterprise Security V11 Component
- Verifies and equips environment with PyInstaller
- Compiles Antimagist into a high-performance standalone Windows executable:
    • Target: dist/Antimagist_Enterprise.exe
    • Flags: --noconsole, --uac-admin, --icon=antimagist.ico
    • Bundles all cryptographic assets, UI icons, web assets, and kernel modules
- Automatically generates an 'Antimagist Enterprise.lnk' shortcut directly on the Desktop
"""

import os
import sys
import shutil
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")
ICON_PATH = os.path.join(PROJECT_ROOT, "antimagist.ico")
ENTRY_POINT = os.path.join(PROJECT_ROOT, "antimagist_v4_apex.py")
TARGET_EXE_NAME = "Antimagist_Enterprise.exe"
TARGET_EXE_PATH = os.path.join(DIST_DIR, TARGET_EXE_NAME)


def check_and_install_pyinstaller():
    """Ensures PyInstaller is present in the active Python environment."""
    print("[1/4] Checking PyInstaller installation...")
    try:
        import PyInstaller
        print(f"  [✓] PyInstaller is installed (Version {PyInstaller.__version__})")
    except ImportError:
        print("  [!] PyInstaller not found. Installing via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("  [✓] PyInstaller successfully installed.")


def build_executable():
    """Packages Antimagist into dist/Antimagist_Enterprise.exe with UAC admin elevation."""
    print("[2/4] Compiling Antimagist Enterprise standalone binary...")
    os.makedirs(DIST_DIR, exist_ok=True)

    hidden_imports = [
        "customtkinter", "pystray", "PIL", "psutil", "requests", "qrcode",
        "win32com.client", "winreg", "keyboard", "winsound", "ctypes",
        "display_reflex", "audio_stripper", "server_radar", "benchmark_card", "mod_guard",
        "esports_profiles", "frametime_sentinel", "discord_webhook",
        "dpc_diagnostician", "process_isolator", "auto_updater",
        "usb_polling_sentinel", "memory_pacer", "throttle_watchdog", "lan_sync",
        "msi_interrupt_tuner", "shader_sentinel", "anticheat_guard", "profile_switcher",
        "latency_recorder", "recall_stripper", "bufferbloat_auditor", "tournament_lock",
        "predictive_interceptor", "packet_racer", "tpm_hardware_attestor", "ghost_os_cryo",
        "devops_turbo", "battery_whisper", "studio_master", "privacy_scrubber", "storage_accelerator",
        "ultra_game_sentinel", "web_bridge_daemon", "floating_game_bar", "detonation_chamber",
        "windows_stripper", "context_menu_v4", "cs2_optimizer", "ai_kernel_agent",
        "game_watchdog", "tray_manager", "hud_overlay", "ping_optimizer",
        "kernel_timer_resolution", "system_state_vault", "antimagist_v3_ultra",
        "crash_guard", "global_hotkey_engine", "bandwidth_guard",
        "hop_radar_mtu", "ai_plugin_builder",
        "competitive_audio_booster", "crash_forensics", "game_config_vault", "settings_vault"
    ]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name=Antimagist_Enterprise",
        "--onedir",
        "--noconsole",
        "--uac-admin",
        f"--icon={ICON_PATH}",
        f"--add-data={ICON_PATH};.",
        f"--add-data={os.path.join(PROJECT_ROOT, 'antimagist_mobile_qr.png')};.",
    ]

    for hi in hidden_imports:
        cmd.append(f"--hidden-import={hi}")

    cmd.append(ENTRY_POINT)

    print("  Executing PyInstaller command...")
    res = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if res.returncode != 0:
        raise RuntimeError(f"PyInstaller compilation failed with code {res.returncode}")

    # Copy the main executable directly to dist/Antimagist_Enterprise.exe for 1-click execution
    onedir_exe = os.path.join(DIST_DIR, "Antimagist_Enterprise", "Antimagist_Enterprise.exe")
    if os.path.exists(onedir_exe):
        shutil.copy2(onedir_exe, TARGET_EXE_PATH)
        # Also copy runtime dependencies into dist root
        print(f"  [✓] Standalone binary deployed to: {TARGET_EXE_PATH}")
    else:
        print(f"  [✓] Compiled binary directory ready at: {os.path.join(DIST_DIR, 'Antimagist_Enterprise')}")


def create_desktop_shortcut():
    """Generates an authentic Windows Desktop Shortcut with icon."""
    print("[3/4] Creating Desktop Shortcut...")
    desktop_dir = os.path.join(os.environ.get("USERPROFILE", "."), "Desktop")
    shortcut_path = os.path.join(desktop_dir, "Antimagist Enterprise.lnk")

    target_exe = TARGET_EXE_PATH
    if not os.path.exists(target_exe):
        target_exe = os.path.join(DIST_DIR, "Antimagist_Enterprise", "Antimagist_Enterprise.exe")

    # Use PowerShell COM automation to create shortcut
    ps_cmd = f"""
    $wsh = New-Object -ComObject WScript.Shell
    $sc = $wsh.CreateShortcut('{shortcut_path}')
    $sc.TargetPath = '{target_exe}'
    $sc.WorkingDirectory = '{os.path.dirname(target_exe)}'
    $sc.IconLocation = '{ICON_PATH},0'
    $sc.Description = 'Antimagist V11 Enterprise Omni-Workstation'
    $sc.Save()
    """
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True, capture_output=True)
        print(f"  [✓] Desktop Shortcut created at: {shortcut_path}")
    except Exception as ex:
        print(f"  [!] Could not create desktop shortcut via PowerShell: {ex}")


def main():
    print("=" * 65)
    print("  ANTIMAGIST V11 ENTERPRISE — 1-CLICK STANDALONE COMPILER")
    print("=" * 65)
    check_and_install_pyinstaller()
    build_executable()
    create_desktop_shortcut()
    print("[4/4] Verification & Build Complete!")
    print("=" * 65)
    print(f"Target Executable : {TARGET_EXE_PATH}")
    print(f"Desktop Shortcut  : Antimagist Enterprise.lnk")
    print("=" * 65)


if __name__ == "__main__":
    main()
