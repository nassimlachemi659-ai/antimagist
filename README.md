# 🛡️ Antimagist Enterprise Security V6 (Zenith Edition)

[![CI](https://github.com/nassimlachemi659-ai/antimagist/actions/workflows/ci.yml/badge.svg)](https://github.com/nassimlachemi659-ai/antimagist/actions)
[![Latest Release](https://img.shields.io/badge/Release-v6.0.0--Zenith-orange?style=for-the-badge&logo=github)](https://github.com/nassimlachemi659-ai/antimagist/releases)
[![Platform: Windows 10 & 11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue?style=for-the-badge&logo=windows)](https://microsoft.com/windows)
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Anti-Cheat: 100% Safe](https://img.shields.io/badge/Anti--Cheat-100%25%20Safe%20(Zero%20Hooks)-success?style=for-the-badge)](https://github.com)
[![Hardware: Universal](https://img.shields.io/badge/Hardware-Universal%20(NVIDIA%2FAMD%2FIntel)-purple?style=for-the-badge)](https://github.com)
[![License: Free Community](https://img.shields.io/badge/License-100%25%20Free%20Community-00FF9D?style=for-the-badge)](https://github.com/nassimlachemi659-ai/antimagist)

> **Transparent, honest, and high-performance esports latency stripper and zero-trust cybersecurity suite for competitive PC gamers.**  
> Built with 100% technical integrity, zero false promises, and universal hardware support across NVIDIA, AMD Radeon, and Intel Arc.

---

## ⚡ What's New in V6 Zenith: The 5 Competitive Pillars

Antimagist V6 Zenith introduces five high-impact, verifiable competitive subsystems engineered for tournament-tier play:

### 1. 🖥️ Display Reflex & DirectFlip Presentation Engine (`display_reflex.py`)
- **Native Win32 Display Telemetry:** Uses native `DEVMODEW` / `EnumDisplaySettingsW` to query actual display resolution, refresh rate (up to 360Hz+), and color depth without third-party bloat.
- **Hardware-Accelerated GPU Scheduling (HAGS) Audit:** Verifies Windows HAGS status (`HwSchMode = 2`) to ensure frame scheduling commands execute on dedicated GPU microcode rather than bottlenecking the CPU queue.
- **DirectFlip / Independent Flip (MPO) Enforcement:** Bypasses Desktop Window Manager (DWM) BitBlt compositor latency via `HKCU\System\GameConfigStore` (`GameDVR_FSEBehavior = 2`), handing game buffers straight to display scanout hardware with zero compositor lag.

### 2. 🎧 Esports Low-Latency Audio Stream Stripper (`audio_stripper.py`)
- **Audio Process Isolation (`audiodg.exe`):** Windows audio processing by default shares CPU cores with game rendering threads, causing footstep cues to lag behind during intense firefights.
- **Physical P-Core Pinning:** Isolates `audiodg.exe` exclusively to a dedicated physical Performance Core (Core 2).
- **High Priority Class Scheduling:** Elevates the audio engine to `HIGH_PRIORITY_CLASS`, completely eliminating audio buffer underruns, sound popping, and DPC latency spikes when your GPU operates at 99% load.

### 3. 🌐 Global Game Server Matchmaking Radar (`server_radar.py`)
- **Pre-Queue Regional Radar:** Measures non-blocking TCP handshake latency across premier competitive hubs:
  - 🇩🇪 **EU Central (Frankfurt)**
  - 🇬🇧 **EU West (London)**
  - 🇸🇪 **EU North (Stockholm)**
  - 🇪🇸 **EU South (Madrid)**
  - 🇦🇪 **Middle East (Dubai)**
  - 🇺🇸 **US East (Virginia)**
  - 🇺🇸 **US West (California)**
- **Gaming DNS Benchmarking:** Analyzes and compares ultra-fast gaming DNS resolvers (Cloudflare `1.1.1.1`, Google `8.8.8.8`, Quad9 `9.9.9.9`) to recommend optimal matchmaking routing.

### 4. 🖼️ Cyberpunk PNG Benchmark Card Generator (`benchmark_card.py`)
- **High-Definition 1200x675 16:9 Export:** Renders an esports-grade Cyberpunk benchmark card featuring deep obsidian (`#0A0E17`), neon emerald (`#00FF9D`), and cyan accents.
- **Audited Rig Telemetry:** Embeds authentic hardware specs: GPU model, CPU P-core topology, native refresh rate, 1% Lows, and matchmaking ping.
- **Cryptographic SHA-256 Fingerprint:** Generates an authentic hash from your physical hardware and timestamp, guaranteeing 100% genuine benchmark metrics with zero fake FPS claims.

### 5. 🛡️ Mod & Config Heuristic Guard (`mod_guard.py`)
- **Malicious Config & Autoexec Detection:** Static heuristic analysis flags Discord token stealers, hidden Discord webhook exfiltration endpoints (`discord.com/api/webhooks/`), obfuscated PowerShell download cradles (`powershell -enc`), and Defender tampering in downloaded FPS boost packs.
- **Safe 1-Click Sanitization:** Neutralizes malicious lines and download cradles while preserving legitimate game console variables (`cl_interp`, `fps_max`, `rate`). Creates automatic `.bak` backups before modifying files.

---

## 🌟 Verifiable Core Mechanics

Antimagist operates with complete transparency:

1. **📶 Zero Packet Grouping (`TcpNoDelay` & `TcpAckFrequency = 1`):**
   - Disables Windows' default Nagle algorithm to prevent packet queue buffering, sending gameplay inputs immediately without network jitter.
2. **⚡ Clean Standby Memory Reclamation (`EmptyWorkingSet`):**
   - Calls the official Windows memory API to release inactive cached standby pages before matches, preventing in-game memory thrashing and stutter.
3. **🎯 CPU Affinity P-Core Pinning (`core_director.py`):**
   - Maps physical CPU core topology and pins gaming execution to dedicated physical Performance Cores, eliminating thread switching across slower Efficiency cores.
4. **🖱️ 1:1 Linear Raw Mouse Input & GameDVR Stripping (`windows_stripper.py`):**
   - Resets Windows mouse registry thresholds to 0 for true linear 1:1 muscle memory, and disables background Xbox GameDVR recording overhead.
5. **🖥️ 100% Anti-Cheat Safe Transparent HUD (<kbd>Ctrl+Shift+O</kbd>):**
   - Renders as an external borderless layered transparent window using native Windows API (`WS_EX_TOPMOST`). Zero DLL injection, zero DirectX/Vulkan hooking. Fully compliant with VAC, Vanguard, BattlEye, and Easy Anti-Cheat.
6. **🛡️ 1-Click Registry Backup & Instant Rollback:**
   - Automatically preserves timestamped JSON backups of your original system configuration before applying any adjustments, allowing 1-click restoration to Windows defaults anytime.

---

## 🤝 100% Free Community Edition & Open Feedback

Antimagist V6 Zenith is released **100% free for competitive gamers worldwide**. 

We want to hear your real-world benchmarks, system feedback, and feature suggestions to continuously improve:
- **Zero Paywalls:** All 22 optimization and defense subsystems are completely unlocked.
- **Hardware Telemetry Feedback:** Test your FPS and ping stability across any GPU (NVIDIA RTX/GTX, AMD Radeon, Intel Arc) and share your results.
- **Continuous Evolution:** Your comments and bug reports directly guide upcoming updates.

---

## 🚀 Quick Start & Installation

### Option 1: 1-Click Setup (Recommended)
1. Download `Antimagist-v6.0.0-Zenith.zip` from [Releases](https://github.com/nassimlachemi659-ai/antimagist/releases).
2. Extract and run `Install_Antimagist_V6.bat`.
3. Automatically installs to `%LocalAppData%\Antimagist` (no UAC / Administrator prompt needed).
4. Launches from your **Desktop** or **Start Menu** shortcut.

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/nassimlachemi659-ai/antimagist.git
cd antimagist

# Install dependencies
pip install customtkinter psutil requests qrcode win32com pystray pillow keyboard

# Launch Master Application
python antimagist_v4_apex.py
```

---

## 🧪 Master Verification & Regression Suite (25/25 Tests)

Antimagist includes a master automated test suite verifying all 25 core subsystems:

```bash
python test_master_v6_suite.py
```
```
===========================================================================
  ANTIMAGIST V6 ZENITH — MASTER VERIFICATION & REGRESSION SUITE
===========================================================================
Ran 25 tests in 10.302s

OK
[SUCCESS] 100% OF TESTS PASSED (25/25) WITH ZERO CRASHES OR REGRESSIONS.
```

---

## 📁 Repository Architecture

```
├── antimagist_v4_apex.py      # Master V6 Zenith Application (22 Panes)
├── display_reflex.py          # Pillar 1: Display Reflex & DirectFlip Presentation Engine
├── audio_stripper.py          # Pillar 2: audiodg.exe P-Core Affinity & Priority Stripper
├── server_radar.py            # Pillar 3: Global Game Server Matchmaking & DNS Radar
├── benchmark_card.py          # Pillar 4: Cyberpunk PNG 1200x675 Benchmark Card Generator
├── mod_guard.py               # Pillar 5: Mod & Config Heuristic Guard & Sanitizer
├── game_watchdog.py           # Auto-Pilot Game Sentinel & Session Logger
├── windows_stripper.py        # Esports Latency Stripper & Registry Optimizer
├── cs2_optimizer.py           # Counter-Strike 2 Tournament Auto-Tuner
├── hud_overlay.py             # Transparent In-Game HUD (Anti-Cheat Safe)
├── discord_rpc.py             # Pure-Python Named-Pipe Discord Presence
├── sound_fx.py                # Cyber Sci-Fi Sound FX Engine
├── mobile_companion.py        # Smartphone Telemetry Server & QR Pairing
├── detonation_chamber.py      # Forensic Shannon Entropy Threat Scanner
├── test_master_v6_suite.py    # 25-Point Automated Master Verification Suite
├── installer_builder.py       # Turnkey Installer Generator
├── Install_Antimagist_V6.bat  # 1-Click Setup Script
├── install_antimagist.ps1     # Windows PowerShell Deployment Harness
└── README.md                  # Project Documentation
```

---

## 📄 Community Edition & Open Contribution
- **Software Edition:** Antimagist V6 Zenith Community Edition (100% Free)
- **License:** Free Community Access
- **Feedback & Benchmarks:** Open an Issue or Discussion on GitHub!
