# 🛡️ Antimagist Enterprise Security V5 (Singularity Edition)

[![Platform: Windows 10 & 11](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue?style=for-the-badge&logo=windows)](https://microsoft.com/windows)
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Anti-Cheat: 100% Safe](https://img.shields.io/badge/Anti--Cheat-100%25%20Safe%20(Zero%20Hooks)-success?style=for-the-badge)](https://github.com)
[![Architecture: Universal GPU & CPU](https://img.shields.io/badge/Hardware-Universal%20(NVIDIA%2FAMD%2FIntel)-purple?style=for-the-badge)](https://github.com)
[![Status: Production Ready](https://img.shields.io/badge/Status-Commercial%20V5-brightgreen?style=for-the-badge)](https://github.com)

> **Transparent, honest, and high-performance esports latency stripper and zero-trust cybersecurity suite for competitive PC gamers.**

---

## 🌟 The 6 Verifiable System Mechanics

Antimagist is built with **100% technical honesty**. We do not use fake marketing numbers or unverified claims. Here is exactly what the engine adjusts on your Windows system:

1. **📶 Zero Packet Grouping (`TcpNoDelay` & `TcpAckFrequency = 1`):**
   - Disables Windows' default Nagle algorithm to prevent packet queue buffering, sending gameplay inputs immediately without network jitter.
2. **⚡ Clean Standby Memory Reclamation (`EmptyWorkingSet`):**
   - Calls the official Windows memory API to release inactive cached standby pages before matches, preventing in-game memory thrashing and stutter.
3. **🎯 CPU Affinity P-Core Pinning:**
   - Maps physical CPU core topology and pins gaming execution to dedicated physical Performance Cores, eliminating thread switching across slower Efficiency cores.
4. **🖱️ 1:1 Linear Raw Mouse Input & GameDVR Stripping:**
   - Resets Windows mouse registry thresholds to 0 for true linear 1:1 muscle memory, and disables background Xbox GameDVR recording overhead.
5. **🖥️ 100% Anti-Cheat Safe Transparent HUD (<kbd>Ctrl+Shift+O</kbd>):**
   - Renders as an external borderless layered transparent window using native Windows API (`WS_EX_TOPMOST`). Zero DLL injection, zero DirectX/Vulkan hooking. Fully compliant with VAC, Vanguard, BattlEye, and Easy Anti-Cheat.
6. **🛡️ 1-Click Registry Backup & Instant Rollback:**
   - Automatically preserves timestamped JSON backups of your original system configuration before applying any adjustments, allowing 1-click restoration to Windows defaults anytime.

---

## 🕹️ Competitive Gaming Subsystems

- **🤖 Auto-Pilot Game Sentinel (`game_watchdog.py`):** Automatically detects when your games launch (`cs2.exe`, `sotgame.exe`, `gmod.exe`, `valorant.exe`, etc.), engages full Apex boost, locks P-cores, and logs post-match analytics.
- **🎯 Counter-Strike 2 Tournament Auto-Tuner (`cs2_optimizer.py`):** Auto-configures sub-tick netcode rates, optimal interp ratios, and low latency sleep settings into CS2's official configuration.
- **📱 Mobile Companion HUD (`mobile_companion.py`):** Local Wi-Fi HTTP telemetry server with instant QR code pairing to check GPU temps and RAM from your smartphone.
- **🎮 Discord Rich Presence (`discord_rpc.py`):** Pure-Python native Named Pipe IPC (`\\.\pipe\discord-ipc-0`) streaming live gaming metrics to your Discord profile without heavy background bloat.
- **🧪 Forensic Detonation Chamber (`detonation_chamber.py`):** Inspects unknown community game files using Shannon entropy calculation and PE header parsing before running them.
- **🎙️ Two-Way Voice Copilot (`voice_listener.py`):** Push-to-Talk voice commands (<kbd>Ctrl+Space</kbd>) allowing spoken system commands during intense matches.

---

## 🔐 Commercial Licensing & Anti-Piracy Architecture

Antimagist V5 includes an **enterprise cryptographic licensing engine**:

- **Hardware ID (HWID) Binding:** Hashes Motherboard UUID, Windows Machine GUID, and CPU identifier into a deterministic SHA-256 fingerprint. Keys are cryptographically bound to the buyer's PC.
- **Cryptographic Key Signing:** Signed using HMAC-SHA256 (`AM5-LIFE-...` or `AM5-SUB-...`).
- **3-Day Free Trial:** Every new installation includes an unthrottled 72-hour trial.
- **Admin Key Generator (`keygen_admin.py`):** Owner GUI and CLI tool to generate Lifetime (€10) or Monthly (€2) keys for buyers.

---

## 🚀 Quick Start & Installation

### Option 1: 1-Click Setup (Recommended)
1. Run `Install_Antimagist_V5.bat` or double-click the PowerShell installer.
2. Automatically deploys to `%LocalAppData%\Antimagist` (no UAC / Administrator prompt needed).
3. Places high-resolution shortcuts on your **Desktop** and **Start Menu**.

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/antimagist.git
cd antimagist

# Install dependencies
pip install customtkinter psutil requests qrcode win32com pystray pillow keyboard

# Launch Master Application
python antimagist_v4_apex.py
```

---

## 🧪 Verification & Regression Testing

Antimagist includes a master automated test suite verifying all 17 subsystems:

```bash
python test_master_v5_suite.py
```
```
Ran 17 tests in 8.281s — [SUCCESS] 100% OF TESTS PASSED WITH ZERO CRASHES.
```

---

## 📁 Repository Structure

```
├── antimagist_v4_apex.py      # Master V5 Singularity Application
├── game_watchdog.py           # Auto-Pilot Game Sentinel & Session Logger
├── windows_stripper.py        # Esports Latency Stripper & Registry Optimizer
├── license_manager.py         # HWID Lock & HMAC-SHA256 Licensing Engine
├── keygen_admin.py            # Private Admin License Key Generator
├── cs2_optimizer.py           # Counter-Strike 2 Tournament Auto-Tuner
├── hud_overlay.py             # Transparent In-Game HUD (Anti-Cheat Safe)
├── discord_rpc.py             # Pure-Python Named-Pipe Discord Presence
├── sound_fx.py                # Cyber Sci-Fi Sound FX Engine
├── mobile_companion.py        # Smartphone Telemetry Server & QR Pairing
├── detonation_chamber.py      # Forensic Shannon Entropy Threat Scanner
├── test_master_v5_suite.py    # 17-Point Automated Verification Suite
├── installer_builder.py       # Turnkey Installer Generator
├── website/                   # Commercial Marketing Website
│   ├── index.html             # Landing Page
│   ├── styles.css             # Glassmorphic Stylesheet
│   └── app.js                 # Interactive Terminal Simulation
└── README.md                  # Project Documentation
```

---

## 📄 License & Commercial Distribution

- **Software Edition:** Antimagist V5 Singularity Commercial
- **Pricing:** €2 / Month Subscription | €10 Lifetime License
- **Support:** Discord VIP Support & 1-Click HWID Migration
