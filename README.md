# 🛡️ Antimagist Enterprise Security V7 (Titan Edition)

[![CI](https://github.com/nassimlachemi659-ai/antimagist/actions/workflows/ci.yml/badge.svg)](https://github.com/nassimlachemi659-ai/antimagist/actions)
[![Latest Release](https://img.shields.io/badge/Release-v7.0.0--Titan-orange?style=for-the-badge&logo=github)](https://github.com/nassimlachemi659-ai/antimagist/releases)
[![Platform: Windows 10 & 11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue?style=for-the-badge&logo=windows)](https://microsoft.com/windows)
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Anti-Cheat: 100% Safe](https://img.shields.io/badge/Anti--Cheat-100%25%20Safe%20(Zero%20Hooks)-success?style=for-the-badge)](https://github.com)
[![Hardware: Universal](https://img.shields.io/badge/Hardware-Universal%20(NVIDIA%2FAMD%2FIntel)-purple?style=for-the-badge)](https://github.com)
[![License: Free Community](https://img.shields.io/badge/License-100%25%20Free%20Community-00FF9D?style=for-the-badge)](https://github.com/nassimlachemi659-ai/antimagist)

> **Transparent, honest, and high-performance esports latency stripper and zero-trust cybersecurity suite for competitive PC gamers.**  
> Built with 100% technical integrity, zero false promises, and universal hardware support across NVIDIA, AMD Radeon, and Intel Arc.

---

## ⚡ What's New in V7 Titan: The Next Competitive Frontier

Antimagist V7 Titan introduces game-changing, zero-bloat alternatives to commercial gaming utilities:

### 1. ⏱️ Hardware DPC & ISR Driver Latency Diagnostician (`dpc_diagnostician.py`)
- **Native LatencyMon Alternative:** Built-in driver execution latency and interrupt diagnostician without needing heavy third-party software.
- **QPC Microsecond Jitter Audit:** Measures high-resolution `QueryPerformanceCounter` jitter across thousands of rapid samples to detect hardware interrupt preemption spikes.
- **Windows Timer Resolution Inspection:** Uses native `ntdll.NtQueryTimerResolution` to audit system timer frequency (verifying 0.5ms - 1.0ms high-tick rate vs 15.6ms Windows default).
- **Driver Culprit Detection:** Audits active in-memory kernel drivers (`nvlddmkm.sys`, `ndis.sys`, `dxgkrnl.sys`, `stornvme.sys`, `rt640x64.sys`) and provides actionable tuning advice (e.g. disable Energy Efficient Ethernet, set NVIDIA Power Management to Maximum Performance).

### 2. 🧠 Intelligent Process Isolator & Core Allocator (`process_isolator.py`)
- **Open-Source Process Lasso Alternative:** Dynamically manages background processes during tournament play.
- **P-Core Game Locking:** Locks the active game and anti-cheat processes to dedicated physical Performance Cores with `HIGH_PRIORITY_CLASS`.
- **Background App Parking:** Identifies running background bloat (Chrome, Discord, Spotify, SteamWebHelper, OneDrive), demotes them to `BELOW_NORMAL_PRIORITY_CLASS`, and isolates them to secondary cores.
- **Seamless Rollback:** Automatically restores all original affinities and priority classes when the match concludes or upon user command.

### 3. 📊 Rolling Frametime Canvas Graph & Pacing Meter (`hud_overlay.py`)
- **Real-Time Visual Pacing:** Features a 60-frame rolling frametime graph rendered right inside the transparent in-game HUD overlay (<kbd>Ctrl+Shift+O</kbd>).
- **Micro-Stutter Detection:** Color-coded pacing bars (Green < 7ms, Amber 7-14ms, Red > 14ms) display instantaneous frame pacing consistency.
- **1-Tap Hotkey Actions:** Directly trigger `[⚡ FLUSH RAM]` and `[🎯 ISOLATE P-CORES]` without leaving your game.

### 4. 🔄 GitHub Releases Automated Updater (`auto_updater.py`)
- **Asynchronous Update Checking:** Queries the official GitHub repository releases API to notify you when updates are released.
- **1-Click Download:** Provides direct 1-click links to the latest portable release packages.

---

## 🏆 The Core V6 Zenith Pillars (Included in V7)

1. **🖥️ Display Reflex & DirectFlip Presentation Engine (`display_reflex.py`):**
   - Win32 `DEVMODEW` 200Hz detection, HAGS verification, and DWM BitBlt bypass (`GameDVR_FSEBehavior = 2`) for 0-frame windowed presentation delay.
2. **🎧 Esports Low-Latency Audio Stream Stripper (`audio_stripper.py`):**
   - Pins `audiodg.exe` to dedicated physical Core 2 with `HIGH_PRIORITY_CLASS`, preventing footstep sound lag and buffer underruns in CS2 and Valorant.
3. **🌐 Global Game Server Matchmaking Radar (`server_radar.py`):**
   - Live pre-queue parallel TCP latency benchmarking across major hubs (Frankfurt, London, Stockholm, Madrid, Dubai, US East, US West) + DNS benchmarking (Cloudflare, Google, Quad9).
4. **🖼️ Cyberpunk PNG Benchmark Card Generator (`benchmark_card.py`):**
   - Generates high-definition 1200x675 16:9 Cyberpunk PNG cards with authentic hardware metrics and cryptographic SHA-256 fingerprints.
5. **🛡️ Mod & Config Heuristic Guard (`mod_guard.py`):**
   - Scans downloaded configs and autoexecs for Discord token stealers, webhooks, and base64 PowerShell cradles; provides 1-click safe sanitization.

---

## 🌟 Verifiable Core Mechanics

Antimagist operates with complete transparency:

1. **📶 Zero Packet Grouping (`TcpNoDelay` & `TcpAckFrequency = 1`):** Disables Windows' default Nagle algorithm to prevent packet queue buffering, sending gameplay inputs immediately without network jitter.
2. **⚡ Clean Standby Memory Reclamation (`EmptyWorkingSet`):** Calls official Windows memory APIs to release inactive cached standby pages before matches, preventing in-game memory thrashing and stutter.
3. **🎯 CPU Affinity P-Core Pinning (`core_director.py`):** Maps physical CPU core topology and pins gaming execution to dedicated physical Performance Cores, eliminating thread switching across slower Efficiency cores.
4. **🖱️ 1:1 Linear Raw Mouse Input & GameDVR Stripping (`windows_stripper.py`):** Resets Windows mouse registry thresholds to 0 for true linear 1:1 muscle memory, and disables background Xbox GameDVR recording overhead.
5. **🖥️ 100% Anti-Cheat Safe Transparent HUD (<kbd>Ctrl+Shift+O</kbd>):** Renders as an external borderless layered transparent window using native Windows API (`WS_EX_TOPMOST`). Zero DLL injection, zero DirectX/Vulkan hooking. Fully compliant with VAC, Vanguard, BattlEye, and Easy Anti-Cheat.
6. **🛡️ 1-Click Registry Backup & Instant Rollback:** Automatically preserves timestamped JSON backups of your original system configuration before applying any adjustments, allowing 1-click restoration to Windows defaults anytime.

---

## 🤝 100% Free Community Edition & Open Feedback

Antimagist V7 Titan is released **100% free for competitive gamers worldwide**. 

We want to hear your real-world benchmarks, system feedback, and feature suggestions to continuously improve:
- **Zero Paywalls:** All 25 optimization and defense subsystems are completely unlocked.
- **Hardware Telemetry Feedback:** Test your FPS and ping stability across any GPU (NVIDIA RTX/GTX, AMD Radeon, Intel Arc) and share your results.
- **Continuous Evolution:** Your comments and bug reports directly guide upcoming updates.

---

## 🚀 Quick Start & Installation

### Option 1: 1-Click Setup (Recommended)
1. Download `Antimagist-v7.0.0-Titan.zip` from [Releases](https://github.com/nassimlachemi659-ai/antimagist/releases).
2. Extract and run `Install_Antimagist_V7.bat`.
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

## 🧪 Master Verification & Regression Suite (30/30 Tests)

Antimagist includes a master automated test suite verifying all 30 core subsystems:

```bash
python test_master_v7_suite.py
```
```
===========================================================================
  ANTIMAGIST V7 TITAN — MASTER VERIFICATION & REGRESSION SUITE
===========================================================================
Ran 30 tests in 8.400s

OK
[SUCCESS] 100% OF TESTS PASSED (30/30) WITH ZERO CRASHES OR REGRESSIONS.
```

---

## 📁 Repository Architecture

```
├── antimagist_v4_apex.py      # Master V7 Titan Application (25 Panes)
├── dpc_diagnostician.py       # V7 Engine 1: DPC/ISR Driver Latency & Timer Diagnostician
├── process_isolator.py        # V7 Engine 2: Intelligent Process Isolator & Core Allocator
├── hud_overlay.py             # V7 Engine 3: Transparent HUD with Rolling Frametime Graph
├── auto_updater.py            # V7 Engine 4: GitHub Releases Automated Updater
├── display_reflex.py          # Display Reflex & DirectFlip Presentation Engine
├── audio_stripper.py          # audiodg.exe P-Core Affinity & Priority Stripper
├── server_radar.py            # Global Game Server Matchmaking & DNS Radar
├── benchmark_card.py          # Cyberpunk PNG 1200x675 Benchmark Card Generator
├── mod_guard.py               # Mod & Config Heuristic Guard & Sanitizer
├── game_watchdog.py           # Auto-Pilot Game Sentinel & Session Logger
├── windows_stripper.py        # Esports Latency Stripper & Registry Optimizer
├── cs2_optimizer.py           # Counter-Strike 2 Tournament Auto-Tuner
├── discord_rpc.py             # Pure-Python Named-Pipe Discord Presence
├── sound_fx.py                # Cyber Sci-Fi Sound FX Engine
├── mobile_companion.py        # Smartphone Telemetry Server & QR Pairing
├── detonation_chamber.py      # Forensic Shannon Entropy Threat Scanner
├── test_master_v7_suite.py    # 30-Point Automated Master Verification Suite
├── installer_builder.py       # Turnkey Installer Generator
├── Install_Antimagist_V7.bat  # 1-Click Setup Script
├── install_antimagist.ps1     # Windows PowerShell Deployment Harness
└── README.md                  # Project Documentation
```

---

## 📄 Community Edition & Open Contribution
- **Software Edition:** Antimagist V7 Titan Community Edition (100% Free)
- **License:** Free Community Access
- **Feedback & Benchmarks:** Open an Issue or Discussion on GitHub!
