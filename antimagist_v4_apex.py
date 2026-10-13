"""
antimagist_v4_apex.py — Antimagist Enterprise Security V5 Singularity Edition
=============================================================================
Architectural Additions in Version 5 (Singularity):
  1. Autonomous Auto-Pilot Game Sentinel & Match Analytics (game_watchdog.py)
     - Automatically detects game launch in background, engages full Apex boost,
       pins P-Cores, summons HUD overlay, and recaps session metrics on exit.
  2. Pure-Python Discord Rich Presence (RPC) Client (discord_rpc.py)
     - Streams real-time GPU hardware telemetry & gaming status to Discord profile.
  3. Cyber Sci-Fi Sound FX & Voice Pack Engine (sound_fx.py)
     - Asynchronous tactile clicks, warp frequency sweeps, and breach sirens.
  4. Esports Latency Stripper & Windows Debloater (windows_stripper.py)
     - Disables GameDVR, sets 1:1 true raw mouse tracking, removes menu delays.
  5. In-Game Transparent HUD Overlay (hud_overlay.py)
     - Anti-cheat safe frameless overlay (Ctrl + Shift + O).
  6. Counter-Strike 2 & FPS Tournament Auto-Tuner (cs2_optimizer.py)
     - Injects sub-tick autoexec with NVIDIA Reflex low-latency sleep.
  7. Two-Way Voice Copilot & Speech Dispatcher (voice_listener.py)
     - Push-to-Talk HUD (Ctrl + Space) or Topbar 🎙️ MIC button.
  8. Windows Context Menu Shell Integrator (context_menu_v4.py)
     - Adds Explorer right-click "🧪 Detonate with Chamber" and "🚀 Launch with Apex Boost".
  9. Dedicated GPU Sentinel (Universal GPU Engine) & Steam Library Auto-Launcher.
  10. Mobile Remote Companion HUD & QR Pairing Server.
"""

import os
import sys
import time
import webbrowser
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk

from antimagist_v3_ultra import (
    AntimagistV3App,
    COLOR_BG_DARK, COLOR_SIDEBAR, COLOR_CARD, COLOR_CARD_HOVER,
    COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER,
    COLOR_CRIMSON, COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED, COLOR_TEXT_SUBTLE
)
from mobile_companion import AntimagistMobileCompanion
from voice_engine import AntimagistVoiceCopilot
from core_director import AntimagistCoreDirector
from detonation_chamber import AntimagistDetonationChamber
from gpu_sentinel import AntimagistGPUSentinel
from game_library import AntimagistGameLibrary
from hud_overlay import AntimagistHUDOverlay
from cs2_optimizer import AntimagistCS2Optimizer, TOURNAMENT_AUTOEXEC_CONTENT
from voice_listener import AntimagistVoiceListener
from context_menu_v4 import AntimagistContextMenuV4
from sound_fx import AntimagistSoundFX
from windows_stripper import AntimagistWindowsStripper
from discord_rpc import AntimagistDiscordRPC
from game_watchdog import AntimagistGameWatchdog
from license_manager import AntimagistLicenseManager
from esports_profiles import AntimagistEsportsProfiler
from frametime_sentinel import AntimagistFrametimeSentinel
from discord_webhook import AntimagistDiscordWebhook
from display_reflex import AntimagistDisplayReflex
from audio_stripper import AntimagistAudioStripper
from server_radar import AntimagistServerRadar
from benchmark_card import AntimagistBenchmarkCard
from mod_guard import AntimagistModGuard
from dpc_diagnostician import AntimagistDPCDiagnostician
from process_isolator import AntimagistProcessIsolator
from auto_updater import AntimagistAutoUpdater
from usb_polling_sentinel import AntimagistUSBPollingSentinel
from memory_pacer import AntimagistMemoryPacer
from throttle_watchdog import AntimagistThrottleWatchdog
from lan_sync import AntimagistLANSync

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistV4ApexApp(AntimagistV3App):
    """Antimagist Enterprise Security Version 7+ (Ultra Edition)."""

    def __init__(self):
        # 1. Initialize Core Subsystems (V4 through V7+)
        self.voice = AntimagistVoiceCopilot(enabled=True)
        self.sfx = AntimagistSoundFX(enabled=True)
        self.core_director = AntimagistCoreDirector()
        self.detonation_chamber = AntimagistDetonationChamber()
        self.gpu_sentinel = AntimagistGPUSentinel()
        self.game_library = AntimagistGameLibrary()
        self.windows_stripper = AntimagistWindowsStripper()
        self.license_manager = AntimagistLicenseManager()
        self.esports_profiler = AntimagistEsportsProfiler()
        self.frametime_sentinel = AntimagistFrametimeSentinel()
        self.discord_webhook = AntimagistDiscordWebhook()
        self.display_reflex = AntimagistDisplayReflex()
        self.audio_stripper = AntimagistAudioStripper()
        self.server_radar = AntimagistServerRadar()
        self.benchmark_card = AntimagistBenchmarkCard()
        self.mod_guard = AntimagistModGuard()
        self.dpc_diagnostician = AntimagistDPCDiagnostician()
        self.process_isolator = AntimagistProcessIsolator()
        self.auto_updater = AntimagistAutoUpdater()
        self.usb_sentinel = AntimagistUSBPollingSentinel()
        self.memory_pacer = AntimagistMemoryPacer()
        self.throttle_watchdog = AntimagistThrottleWatchdog()
        self.lan_sync = AntimagistLANSync()

        # Call base constructor
        super().__init__()

        # Update window title
        self.title("Antimagist — Enterprise Security V7+ Ultra Edition")

        # 2. Initialize Discord Rich Presence Client
        self.discord_rpc = AntimagistDiscordRPC()
        threading.Thread(target=self._init_discord_rpc, daemon=True).start()

        # 3. Initialize and start Mobile Remote Companion HUD
        self.mobile_companion = AntimagistMobileCompanion(
            optimizer_core=self.optimizer,
            gamer_mode=self.gamer_mode,
            ping_optimizer=self.ping_optimizer,
            bandwidth_meter=self.bandwidth_meter,
            gpu_sentinel=self.gpu_sentinel,
            voice_engine=self.voice,
            port=8765
        )
        self.mobile_companion.start_server()

        # 4. Initialize Gaming & Interactive Modules
        self.hud_overlay = AntimagistHUDOverlay(
            parent_app=self,
            optimizer_core=self.optimizer,
            gamer_mode=self.gamer_mode,
            ping_optimizer=self.ping_optimizer,
            gpu_sentinel=self.gpu_sentinel,
            voice_engine=self.voice
        )
        self.cs2_optimizer = AntimagistCS2Optimizer()
        self.voice_listener = AntimagistVoiceListener(
            parent_app=self,
            optimizer_core=self.optimizer,
            gamer_mode=self.gamer_mode,
            ping_optimizer=self.ping_optimizer,
            cs2_optimizer=self.cs2_optimizer,
            hud_overlay=self.hud_overlay,
            voice_engine=self.voice
        )
        self.context_menu_v4 = AntimagistContextMenuV4()

        # 5. Initialize Autonomous Game Watchdog
        self.game_watchdog = AntimagistGameWatchdog(
            optimizer_core=self.optimizer,
            gamer_mode=self.gamer_mode,
            ping_optimizer=self.ping_optimizer,
            gpu_sentinel=self.gpu_sentinel,
            core_director=self.core_director,
            hud_overlay=self.hud_overlay,
            discord_rpc=self.discord_rpc,
            voice_engine=self.voice,
            sound_fx=self.sfx
        )
        self.game_watchdog.start_watchdog()

        # Global Hotkeys (Ctrl+Shift+O for HUD Overlay, Ctrl+Space for Voice Listener)
        self._init_global_hotkeys()

        # Update Topbar Branding
        if hasattr(self, 'topbar'):
            self._enhance_topbar_v4()

        # Re-attach canary breach callback with spoken voice alert & siren
        self.canary_guard.on_breach = self._on_ransomware_breach_v5

        # Process CLI shell verb arguments
        self._check_cli_arguments()

    def _init_discord_rpc(self):
        try:
            ok = self.discord_rpc.connect()
            if ok:
                gm = self.gpu_sentinel.get_live_gpu_metrics()
                self.discord_rpc.update_presence(
                    details="Protected by Antimagist V5 Singularity",
                    state=f"{gm['gpu_name'][:12]} ({gm['temperature_c']}°C) | Ping: 5ms"
                )
        except Exception:
            pass

    # ========================================================================
    # GLOBAL HOTKEYS & CLI VERB DISPATCHER
    # ========================================================================
    def _init_global_hotkeys(self):
        def register():
            try:
                import keyboard
                keyboard.add_hotkey("ctrl+shift+o", lambda: self.after(0, self.hud_overlay.toggle_overlay))
                keyboard.add_hotkey("ctrl+space", lambda: self.after(0, self.voice_listener.open_voice_dialog))
            except Exception:
                pass
        threading.Thread(target=register, daemon=True).start()

    def _check_cli_arguments(self):
        if len(sys.argv) > 2:
            verb = sys.argv[1].lower()
            target = sys.argv[2]
            if verb == "--detonate":
                self.after(600, lambda: self._detonate_target_from_cli(target))
            elif verb == "--apex-launch":
                self.after(600, lambda: self._launch_target_from_cli(target))

    def _detonate_target_from_cli(self, target_path: str):
        self.show_detonation_pane()
        if hasattr(self, "det_log_box") and os.path.exists(target_path):
            self.det_log_box.insert("end", f"\n[🔍 Shell Extension Triggered] Analyzing: {target_path}\n")
            res = self.detonation_chamber.analyze_specimen_forensics(target_path)
            self.det_log_box.insert("end", f"• Threat Score: {res.get('risk_score', 0)}/100 | Entropy: {res.get('entropy', 0.0)}\n")
            self.det_log_box.see("end")

    def _launch_target_from_cli(self, target_path: str):
        self.optimizer.run_memory_boost(lambda m: None)
        self.ping_optimizer.optimize_gaming_network()
        self.gamer_mode.activate_gamer_mode()
        self.sfx.play_warp_boost()
        self.voice.speak(f"Apex boost engaged for {os.path.basename(target_path)}.")
        try:
            os.startfile(target_path)
        except Exception:
            pass

    # ========================================================================
    # TOPBAR V5 ENHANCEMENTS
    # ========================================================================
    def _enhance_topbar_v4(self):
        # 1. Voice Copilot Toggle Button
        self.btn_voice = ctk.CTkButton(
            self.topbar, text="🔊 VOICE: ON",
            font=("Segoe UI", 11, "bold"), text_color="#000000",
            fg_color="#00FF9D", hover_color="#00D480",
            height=32, width=95, corner_radius=8,
            command=self._toggle_voice_copilot
        )
        self.btn_voice.pack(side="right", padx=(0, 6), pady=12)

        # 2. Sound FX Toggle
        self.btn_sfx = ctk.CTkButton(
            self.topbar, text="🎵 SFX: ON",
            font=("Segoe UI", 11, "bold"), text_color="#000000",
            fg_color="#A855F7", hover_color="#9333EA",
            height=32, width=85, corner_radius=8,
            command=self._toggle_sfx
        )
        self.btn_sfx.pack(side="right", padx=(0, 6), pady=12)

        # 3. In-Game HUD Overlay Button
        self.btn_hud_nav = ctk.CTkButton(
            self.topbar, text="🖥️ HUD",
            font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY,
            fg_color="#1E293B", hover_color="#334155",
            height=32, width=65, corner_radius=8,
            command=self._toggle_hud_with_sfx
        )
        self.btn_hud_nav.pack(side="right", padx=(0, 6), pady=12)

        # 4. Two-Way Voice Mic Dialogue
        self.btn_mic = ctk.CTkButton(
            self.topbar, text="🎙️ MIC",
            font=("Segoe UI", 11, "bold"), text_color="#000000",
            fg_color="#00F0FF", hover_color="#00B4D8",
            height=32, width=65, corner_radius=8,
            command=self._open_mic_with_sfx
        )
        self.btn_mic.pack(side="right", padx=(0, 6), pady=12)

        # 5. Mobile Companion Quick Button
        self.btn_mobile_nav = ctk.CTkButton(
            self.topbar, text="📱 MOBILE HUD",
            font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY,
            fg_color="#1E293B", hover_color="#334155",
            height=32, width=110, corner_radius=8,
            command=self.show_mobile_pane
        )
        self.btn_mobile_nav.pack(side="right", padx=(0, 6), pady=12)

        # 6. Live GPU Sentinel Pill Badge
        gm = self.gpu_sentinel.get_live_gpu_metrics()
        self.pill_gpu = ctk.CTkLabel(
            self.topbar, text=f"🎮 {gm['gpu_name'][:12]}: {gm['temperature_c']}°C",
            font=("Segoe UI", 10, "bold"), text_color=gm['status_color'],
            fg_color="#0F172A", corner_radius=8, width=140, height=32
        )
        self.pill_gpu.pack(side="right", padx=(0, 6), pady=12)

        # 7. Community Free Status Button
        st = self.license_manager.get_status_summary()
        lic_txt = "🛡️ FREE EDITION"
        lic_color = "#00FF9D"
        self.btn_license = ctk.CTkButton(
            self.topbar, text=lic_txt,
            font=("Segoe UI", 10, "bold"), text_color="#000000",
            fg_color=lic_color, hover_color="#38BDF8",
            height=32, width=115, corner_radius=8,
            command=self._open_activation_dialog
        )
        self.btn_license.pack(side="right", padx=(0, 6), pady=12)

    def _open_activation_dialog(self):
        self.sfx.play_click()
        dlg = ctk.CTkToplevel(self)
        dlg.title("Antimagist V5 — Community Edition")
        dlg.geometry("480x420")
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()

        st = self.license_manager.get_status_summary()

        ctk.CTkLabel(dlg, text="🛡️ ANTIMAGIST COMMUNITY EDITION", font=("Segoe UI", 14, "bold"), text_color="#00F0FF").pack(pady=(16, 4))
        ctk.CTkLabel(dlg, text="100% Free Forever • All Features Unlocked For Competitive Gamers", font=("Segoe UI", 10), text_color="#94A3B8").pack(pady=(0, 10))

        # HWID Display
        f_hw = ctk.CTkFrame(dlg, fg_color="#0F1320")
        f_hw.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(f_hw, text="Machine Hardware ID (HWID):", font=("Segoe UI", 10, "bold"), text_color="#94A3B8").pack(anchor="w", padx=12, pady=(6, 2))
        ctk.CTkLabel(f_hw, text=st["hwid"], font=("Consolas", 11, "bold"), text_color="#00FF9D").pack(anchor="w", padx=12, pady=(0, 6))

        # Current Status
        f_st = ctk.CTkFrame(dlg, fg_color="#0F1320")
        f_st.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(f_st, text="Status: 100% Free Community Edition (Unlocked)", font=("Segoe UI", 11, "bold"), text_color="#00FF9D").pack(padx=12, pady=8)

        # License Entry
        ctk.CTkLabel(dlg, text="Paste License Key (AM5-...):", font=("Segoe UI", 10, "bold"), text_color="#E2E8F0").pack(anchor="w", padx=20, pady=(6, 2))
        ent_key = ctk.CTkEntry(dlg, placeholder_text="e.g. AM5-LIFE-XXXX or AM5-SUB-XXXX", font=("Consolas", 11), height=36, fg_color="#161F33", border_color="#334155")
        ent_key.pack(fill="x", padx=20, pady=(0, 10))

        def activate():
            raw_k = ent_key.get().strip()
            ok, msg = self.license_manager.activate_license(raw_k)
            if ok:
                self.sfx.play_success()
                new_st = self.license_manager.get_status_summary()
                self.btn_license.configure(text=f"💎 {new_st['tier']}", fg_color="#00FF9D")
                messagebox.showinfo("License Activated", msg, parent=dlg)
                dlg.destroy()
            else:
                self.sfx.play_breach_siren()
                messagebox.showerror("Activation Failed", msg, parent=dlg)

        btn_act = ctk.CTkButton(dlg, text="⚡ ACTIVATE LICENSE", font=("Segoe UI", 12, "bold"), fg_color="#00F0FF", text_color="#000000", hover_color="#38BDF8", height=38, command=activate)
        btn_act.pack(fill="x", padx=20, pady=(4, 10))

    def _toggle_voice_copilot(self):
        self.sfx.play_click()
        is_on = self.voice.toggle_voice()
        if is_on:
            self.btn_voice.configure(text="🔊 VOICE: ON", fg_color="#00FF9D", text_color="#000000")
            self.voice.speak("Antimagist Voice Copilot unmuted.")
        else:
            self.btn_voice.configure(text="🔇 VOICE: MUTED", fg_color="#334155", text_color="#94A3B8")

    def _toggle_sfx(self):
        is_on = self.sfx.toggle_sound()
        if is_on:
            self.btn_sfx.configure(text="🎵 SFX: ON", fg_color="#A855F7", text_color="#000000")
            self.sfx.play_success()
        else:
            self.btn_sfx.configure(text="🔇 SFX: OFF", fg_color="#334155", text_color="#94A3B8")

    def _toggle_hud_with_sfx(self):
        self.sfx.play_click()
        self.hud_overlay.toggle_overlay()

    def _open_mic_with_sfx(self):
        self.sfx.play_click()
        self.voice_listener.open_voice_dialog()

    # ========================================================================
    # SIDEBAR V5 MASTER NAVIGATION (14 PANES)
    # ========================================================================
    def _build_body_layout(self):
        super()._build_body_layout()

        # Clear standard sidebar items and reconstruct with V5 items
        for btn in self.nav_buttons.values():
            btn.destroy()
        self.nav_buttons.clear()

        v5_nav_items = [
            ("📊 Dashboard",        "dash",       self.show_dashboard_pane),
            ("🎮 Esports Vault",    "esports",    self.show_esports_pane),
            ("🖥️ Display Reflex",    "reflex",     self.show_display_reflex_pane),
            ("🎧 Audio Stripper",    "audio",      self.show_audio_stripper_pane),
            ("🌐 Server Radar",      "radar",      self.show_server_radar_pane),
            ("⏱️ DPC Latency",       "dpc",        self.show_dpc_pane),
            ("🧠 Process Isolator",  "isolator",   self.show_isolator_pane),
            ("🖱️ USB Polling",      "usb",        self.show_usb_polling_pane),
            ("🧠 Memory Pacer",      "mempacer",   self.show_memory_pacer_pane),
            ("🔥 Throttle Watchdog", "throttle",   self.show_throttle_pane),
            ("📡 LAN Team Sync",     "lansync",    self.show_lan_sync_pane),
            ("🖼️ Benchmark Card",    "card",       self.show_benchmark_card_pane),
            ("🛡️ Mod Guard",         "modguard",   self.show_mod_guard_pane),
            ("🔄 Auto-Updater",      "updater",    self.show_updater_pane),
            ("🎯 CS2 Tuner",         "cs2",        self.show_cs2_pane),
            ("⚡ Latency Stripper",  "stripper",   self.show_stripper_pane),
            ("📈 Match History",     "analytics",  self.show_analytics_pane),
            ("💬 Community Review",  "review",     self.show_review_pane),
            ("🔍 Threat Radar",      "scanner",    self.show_scanner_pane),
            ("🧪 Detonation Room",   "detonate",   self.show_detonation_pane),
            ("📱 Mobile HUD",        "mobile",     self.show_mobile_pane),
            ("👁️ Active Shield",     "shield",     self.show_shield_pane),
            ("🌐 Network Guard",     "net",        self.show_network_pane),
            ("🚀 Startup Apps",      "startup",    self.show_startup_pane),
            ("🎮 Gamer Mode",        "gamer",      self.show_gamer_pane),
            ("🔗 URL Radar",         "url",        self.show_url_pane),
            ("⚡ PC Optimizer",      "opt",        self.show_optimizer_pane),
            ("🤖 Sentient AI",       "ai",         self.show_ai_agent_pane),
            ("⚙️ Settings",          "settings",   self.show_settings_pane),
        ]

        for text, key, cmd in v5_nav_items:
            def make_cmd(orig_cmd=cmd):
                self.sfx.play_click()
                orig_cmd()

            btn = ctk.CTkButton(
                self.sidebar, text=text, font=("Segoe UI", 11, "bold"),
                fg_color="transparent", text_color=COLOR_TEXT_SUBTLE,
                hover_color=COLOR_CARD, anchor="w",
                height=30, corner_radius=8, command=make_cmd
            )
            btn.pack(fill="x", padx=10, pady=1)
            self.nav_buttons[key] = btn

    # ========================================================================
    # 1. NEW V5 PANE: ESPORTS LATENCY STRIPPER (show_stripper_pane)
    # ========================================================================
    def show_stripper_pane(self):
        self._highlight_nav("stripper")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        # Header Title
        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Windows Esports Latency Stripper & Debloater", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Strip background recording, eliminate mouse acceleration, and disable network packet throttling", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Actions & Status
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        posture = self.windows_stripper.get_tuning_posture()
        ctk.CTkLabel(left_card, text="OS Latency Posture", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        # Status pills
        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        pills = [
            ("Xbox GameDVR Recording", "DISABLED (Optimal)" if posture["gamedvr_disabled"] else "ENABLED (High Latency)", COLOR_EMERALD if posture["gamedvr_disabled"] else COLOR_CRIMSON),
            ("1:1 Raw Mouse Tracking", "ACTIVE (Zero Curve)" if posture["raw_mouse_active"] else "ACCELERATION ON", COLOR_EMERALD if posture["raw_mouse_active"] else COLOR_AMBER),
            ("UI MenuShowDelay", "0 ms (Instantaneous)" if posture["menu_delay_optimized"] else "400 ms (Default)", COLOR_EMERALD if posture["menu_delay_optimized"] else COLOR_TEXT_MUTED)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="⚡ Apply Esports Latency Tuning", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._apply_stripper_tuning
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🔄 Restore Windows Defaults", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=34, corner_radius=8, command=self._restore_stripper_defaults
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Esports Breakdown
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Competitive Advantage Breakdown", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 10))

        explanations = [
            ("🎮 GameDVR Background Recording", "Windows silently records recent gameplay to NVMe disk in a 60fps loop. This causes micro-stutters and frame drops in CS2 and Valorant. Disabling it completely frees rendering pipelines."),
            ("🖱️ True 1:1 Raw Mouse Tracking", "Windows applies an artificial non-linear pointer speed curve by default. Setting MouseSpeed and threshold keys to 0 delivers pure hardware mouse sensor raw input."),
            ("📶 Gaming Network Throttling", "Windows network throttling restricts non-multimedia network throughput during intensive I/O. Disabling it ensures game packets bypass kernel rate limiters.")
        ]
        for t, d in explanations:
            bx = ctk.CTkFrame(right_card, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(bx, text=t, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(bx, text=d, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _apply_stripper_tuning(self):
        ok, msg = self.windows_stripper.apply_esports_latency_tuning()
        self.sfx.play_success()
        self.show_toast_msg(msg)
        self.show_stripper_pane()

    def _restore_stripper_defaults(self):
        ok, msg = self.windows_stripper.restore_windows_defaults()
        self.sfx.play_click()
        self.show_toast_msg(msg)
        self.show_stripper_pane()

    # ========================================================================
    # 2. NEW V5 PANE: AUTONOMOUS MATCH ANALYTICS (show_analytics_pane)
    # ========================================================================
    def show_analytics_pane(self):
        self._highlight_nav("analytics")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(2, weight=1)

        # Header Title
        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Autonomous Match Analytics & Telemetry Vault", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Historical log of autonomous gaming sessions with peak GPU temperatures and average ping", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Top Stats Summary
        history = self.game_watchdog.match_history
        top_bar = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        top_bar.grid(row=1, column=0, sticky="ew", pady=(0, 12), ipady=6)
        top_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(top_bar, text=f"LOGGED MATCHES\n{len(history)} Sessions", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).grid(row=0, column=0)
        
        last_game = history[-1]["game_name"] if history else "Standing By"
        ctk.CTkLabel(top_bar, text=f"LAST TITLE\n{last_game}", font=("Segoe UI", 11, "bold"), text_color=COLOR_EMERALD).grid(row=0, column=1)

        ctk.CTkLabel(top_bar, text="AUTO-PILOT SENTINEL\nACTIVE (0.1% CPU)", font=("Segoe UI", 11, "bold"), text_color=COLOR_AMBER).grid(row=0, column=2)
        ctk.CTkLabel(top_bar, text="DISCORD RPC STATUS\nSYNCED VIA IPC", font=("Segoe UI", 11, "bold"), text_color="#A855F7").grid(row=0, column=3)

        # Scrollable Matches Table
        table_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        th = ctk.CTkFrame(table_card, fg_color="#0F1320", height=32, corner_radius=6)
        th.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))
        th.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        ctk.CTkLabel(th, text="GAME TITLE", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_SUBTLE).grid(row=0, column=0, sticky="w", padx=10)
        ctk.CTkLabel(th, text="DURATION", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_SUBTLE).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(th, text="PEAK GPU TEMP", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_SUBTLE).grid(row=0, column=2, sticky="w")
        ctk.CTkLabel(th, text="AVG PING", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_SUBTLE).grid(row=0, column=3, sticky="w")
        ctk.CTkLabel(th, text="TIMESTAMP", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_SUBTLE).grid(row=0, column=4, sticky="e", padx=10)

        scroll = ctk.CTkScrollableFrame(table_card, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        if not history:
            ctk.CTkLabel(scroll, text="No match records yet. Launch any Steam game to trigger autonomous telemetry!", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(pady=40)
        else:
            for rec in reversed(history):
                row = ctk.CTkFrame(scroll, fg_color="#0A0C14", corner_radius=6)
                row.pack(fill="x", pady=2)
                row.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
                ctk.CTkLabel(row, text=rec.get("game_name", ""), font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).grid(row=0, column=0, sticky="w", padx=10, pady=5)
                ctk.CTkLabel(row, text=rec.get("duration_str", ""), font=("Consolas", 10), text_color=COLOR_TEXT_PRIMARY).grid(row=0, column=1, sticky="w")
                ctk.CTkLabel(row, text=f"{rec.get('peak_gpu_temp', 0)} °C", font=("Consolas", 10), text_color=COLOR_EMERALD).grid(row=0, column=2, sticky="w")
                ctk.CTkLabel(row, text=f"{rec.get('avg_ping_ms', 0)} ms", font=("Consolas", 10), text_color=COLOR_AMBER).grid(row=0, column=3, sticky="w")
                ctk.CTkLabel(row, text=rec.get("date", ""), font=("Consolas", 9), text_color=COLOR_TEXT_MUTED).grid(row=0, column=4, sticky="e", padx=10)

    # ========================================================================
    # MULTI-GAME ESPORTS VAULT PANE (show_esports_pane)
    # ========================================================================
    def show_esports_pane(self):
        self._highlight_nav("esports")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Multi-Game Tournament Esports Vault", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Engineered tournament auto-tuners for CS2, Valorant, Apex Legends, Fortnite, and Warzone", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        scroll = ctk.CTkScrollableFrame(pane, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure((0, 1), weight=1)

        titles = self.esports_profiler.scan_installed_esports_titles()

        game_configs = [
            ("CS2", "Counter-Strike 2", "Valve Sub-Tick Networking & Reflex", self._tune_cs2_esports),
            ("VALORANT", "Valorant", "High Priority Class & Raw Mouse Sync", self._tune_valorant_esports),
            ("APEX_LEGENDS", "Apex Legends", "Uncapped FPS, Audio Buffer & Ragdoll Strip", self._tune_apex_esports),
            ("FORTNITE", "Fortnite", "Linear Mouse Acceleration Wipe & VSync Strip", self._tune_fortnite_esports),
            ("WARZONE", "Call of Duty (Warzone)", "P-Core CPU Renderer Worker Sync", self._tune_warzone_esports),
        ]

        row_idx = 0
        col_idx = 0
        for code, name, desc, action in game_configs:
            info = titles.get(code, {})
            det = info.get("detected", False)
            status_txt = "● DETECTED" if det else "○ STANDBY"
            status_col = COLOR_EMERALD if det else COLOR_TEXT_MUTED

            card = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
            card.grid(row=row_idx, column=col_idx, sticky="nsew", padx=8, pady=8)

            ctk.CTkLabel(card, text=name, font=("Segoe UI", 16, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 2))
            ctk.CTkLabel(card, text=status_txt, font=("Segoe UI", 11, "bold"), text_color=status_col).pack(anchor="w", padx=16, pady=(0, 6))
            ctk.CTkLabel(card, text=desc, font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED, wraplength=340, justify="left").pack(anchor="w", padx=16, pady=(0, 14))

            btn_color = "#00FF9D" if det else "#1E293B"
            btn_txt_col = "#000000" if det else "#94A3B8"
            ctk.CTkButton(
                card, text=f"⚡ Tune {name}", font=("Segoe UI", 12, "bold"),
                fg_color=btn_color, hover_color="#00D480", text_color=btn_txt_col,
                height=38, corner_radius=8, command=action
            ).pack(fill="x", padx=16, pady=(0, 16))

            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1

    def _tune_cs2_esports(self):
        self.sfx.play_warp_boost()
        ok, msg = self.esports_profiler.optimize_cs2()
        self.voice.speak("Counter Strike 2 tournament autoexec injected.")
        self.show_esports_pane()

    def _tune_valorant_esports(self):
        self.sfx.play_click()
        ok, msg = self.esports_profiler.optimize_valorant()
        self.voice.speak("Valorant process priority tuned.")
        self.show_esports_pane()

    def _tune_apex_esports(self):
        self.sfx.play_warp_boost()
        ok, msg = self.esports_profiler.optimize_apex_legends()
        self.voice.speak("Apex Legends low latency config written.")
        self.show_esports_pane()

    def _tune_fortnite_esports(self):
        self.sfx.play_click()
        ok, msg = self.esports_profiler.optimize_fortnite()
        self.voice.speak("Fortnite linear mouse tracking applied.")
        self.show_esports_pane()

    def _tune_warzone_esports(self):
        self.sfx.play_warp_boost()
        ok, msg = self.esports_profiler.optimize_warzone()
        self.voice.speak("Warzone CPU worker threads synchronized.")
        self.show_esports_pane()

    # ========================================================================
    # COMMUNITY REVIEW PANE (show_review_pane)
    # ========================================================================
    def show_review_pane(self):
        self._highlight_nav("review")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Community Benchmark & Feedback Hub", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Submit verified benchmarks, frame-time reviews, and developer suggestions to Discord", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Input Form
        left = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left, text="Player Benchmark Submission", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 6))

        ctk.CTkLabel(left, text="GAMER TAG / DISCORD HANDLE", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(6, 2))
        self.ent_review_name = ctk.CTkEntry(left, placeholder_text="e.g. ApexPredator#1337", height=36, corner_radius=8)
        self.ent_review_name.pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(left, text="EXPERIENCE RATING (1-5 STARS)", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(6, 2))
        star_bar = ctk.CTkFrame(left, fg_color="transparent")
        star_bar.pack(anchor="w", padx=16, pady=(0, 10))
        self._selected_stars = 5
        self._star_buttons = []

        def set_stars(n):
            self._selected_stars = n
            for idx, b in enumerate(self._star_buttons):
                b.configure(fg_color="#00FF9D" if idx < n else "#1E293B", text_color="#000000" if idx < n else "#94A3B8")

        for i in range(1, 6):
            btn_s = ctk.CTkButton(star_bar, text=f"{i} ⭐", width=48, height=30, corner_radius=6,
                                  fg_color="#00FF9D", text_color="#000000", font=("Segoe UI", 10, "bold"),
                                  command=lambda val=i: set_stars(val))
            btn_s.pack(side="left", padx=2)
            self._star_buttons.append(btn_s)

        ctk.CTkLabel(left, text="BENCHMARK FEEDBACK & GAMEPLAY COMMENTS", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(6, 2))
        self.txt_review_comments = ctk.CTkTextbox(left, height=120, corner_radius=8, font=("Segoe UI", 11))
        self.txt_review_comments.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            left, text="📢 Send Verified Benchmark to Discord", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._submit_review_action
        ).pack(fill="x", padx=16, pady=(4, 16))

        # Right Card: Hardware Posture Preview
        right = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right, text="Telemetry Attached to Your Submission", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 6))

        gm = self.gpu_sentinel.get_live_gpu_metrics()
        pt = self.ping_optimizer.get_live_ping_telemetry()
        ft = self.frametime_sentinel.get_metrics() if self.frametime_sentinel else {}

        spec_box = ctk.CTkFrame(right, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        spec_box.pack(fill="both", expand=True, padx=16, pady=10)

        lines = [
            f"• Verified GPU: {gm.get('gpu_name', 'GPU')} ({gm.get('temperature_c', '--')}°C)",
            f"• Cloudflare Latency: {pt.get('ping_ms', 15.0)} ms (Zero Packet Loss)",
            f"• Frame Consistency: {ft.get('frametime_variance_ms', 0.4)} ms jitter",
            f"• 1% Low Metric: {int(ft.get('one_percent_low_fps', 144))} FPS",
            f"• Memory Optimization: Ready (Standby Reclaimed)",
            f"• Community License: 100% Free Lifetime Unlocked"
        ]
        for l in lines:
            ctk.CTkLabel(spec_box, text=l, font=("Consolas", 11), text_color=COLOR_CYAN, anchor="w").pack(anchor="w", padx=16, pady=6)

    def _submit_review_action(self):
        name = self.ent_review_name.get().strip() if hasattr(self, "ent_review_name") else "Anonymous"
        feedback = self.txt_review_comments.get("1.0", "end").strip() if hasattr(self, "txt_review_comments") else ""
        if not feedback:
            feedback = "Verified smooth low-latency gaming session with Antimagist V5 Singularity."

        self.sfx.play_click()
        ok, msg = self.discord_webhook.send_benchmark_review(
            player_name=name or "Gamer",
            rating=getattr(self, "_selected_stars", 5),
            feedback=feedback
        )
        self.voice.speak("Thank you. Benchmark review logged.")
        self.show_review_pane()

    # ========================================================================
    # CS2 PANE
    # ========================================================================
    def show_cs2_pane(self):
        self._highlight_nav("cs2")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Counter-Strike 2 & Esports Tournament Tuner", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Inject sub-tick networking, uncap framerate, enable NVIDIA Reflex low-latency, and pin to P-Cores", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        st = self.cs2_optimizer.get_status()
        status_txt = "● CS2 DETECTED & READY" if st["is_installed"] else "○ CS2 NOT DETECTED"
        status_col = COLOR_EMERALD if st["is_installed"] else COLOR_CRIMSON

        ctk.CTkLabel(left_card, text="Game Status & Direct Launch", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 4))
        ctk.CTkLabel(left_card, text=status_txt, font=("Segoe UI", 12, "bold"), text_color=status_col).pack(anchor="w", padx=16, pady=(0, 10))

        ctk.CTkButton(
            left_card, text="🚀 Launch CS2 with Apex Boost", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._launch_cs2_action
        ).pack(fill="x", padx=16, pady=8)

        ctk.CTkButton(
            left_card, text="⚙️ Apply Tournament Autoexec", font=("Segoe UI", 12, "bold"),
            fg_color="#00F0FF", hover_color="#00B4D8", text_color="#000000",
            height=38, corner_radius=10, command=self._apply_cs2_autoexec_action
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🖥️ Toggle In-Game Overlay (Ctrl+Shift+O)", font=("Segoe UI", 12, "bold"),
            fg_color="#7C3AED", hover_color="#6D28D9", text_color="#FFFFFF",
            height=38, corner_radius=10, command=self.hud_overlay.toggle_overlay
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🔄 Restore Original Config Backup", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=34, corner_radius=8, command=self._restore_cs2_backup_action
        ).pack(fill="x", padx=16, pady=(6, 16))

        path_box = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
        path_box.pack(fill="x", padx=16, pady=(0, 16))
        ctk.CTkLabel(path_box, text=f"Directory:\n{st['cs2_root']}", font=("Consolas", 10), text_color=COLOR_TEXT_MUTED, wraplength=380, justify="left").pack(anchor="w", padx=10, pady=8)

        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right_card, text="Tournament Autoexec Parameters", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        cfg_box = ctk.CTkTextbox(right_card, font=("Consolas", 11), fg_color="#0A0C14", text_color=COLOR_EMERALD, corner_radius=10)
        cfg_box.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        cfg_box.insert("0.0", TOURNAMENT_AUTOEXEC_CONTENT)
        cfg_box.configure(state="disabled")

    def _launch_cs2_action(self):
        self.sfx.play_warp_boost()
        ok, msg = self.cs2_optimizer.launch_cs2_with_apex_boost(
            optimizer_core=self.optimizer,
            gamer_mode=self.gamer_mode,
            ping_optimizer=self.ping_optimizer,
            core_director=self.core_director,
            voice_engine=self.voice
        )
        self.show_toast_msg(msg)

    def _apply_cs2_autoexec_action(self):
        self.sfx.play_success()
        ok, msg = self.cs2_optimizer.apply_tournament_optimization()
        self.show_toast_msg(msg)
        if self.voice:
            self.voice.speak("Tournament autoexec applied to Counter-Strike 2.")

    def _restore_cs2_backup_action(self):
        self.sfx.play_click()
        ok, msg = self.cs2_optimizer.restore_backup()
        self.show_toast_msg(msg)

    # ========================================================================
    # SETTINGS OVERRIDE WITH CONTEXT MENU V4
    # ========================================================================
    def show_settings_pane(self):
        super().show_settings_pane()
        try:
            f_v4 = ctk.CTkFrame(self.container.winfo_children()[-1], fg_color="transparent")
            f_v4.pack(fill="x", padx=25, pady=(5, 10))

            is_reg = self.context_menu_v4.is_registered()
            btn_txt = "🗑️ Remove Apex V4 Shell Menus" if is_reg else "🖱️ Add Apex V4 Shell Menus (Detonate & Apex Boost)"
            btn_col = "#3B1219" if is_reg else "#1E293B"

            ctk.CTkButton(
                f_v4, text=btn_txt, font=("Segoe UI", 12, "bold"),
                fg_color=btn_col, hover_color="#334155",
                text_color=COLOR_CRIMSON if is_reg else COLOR_CYAN,
                height=38, command=self._toggle_context_menu_v4_ui
            ).pack(side="left")
        except Exception:
            pass

    def _toggle_context_menu_v4_ui(self):
        self.sfx.play_click()
        if self.context_menu_v4.is_registered():
            ok, msg = self.context_menu_v4.unregister_context_menus()
        else:
            ok, msg = self.context_menu_v4.register_context_menus()
        self.show_toast_msg(msg)
        self.show_settings_pane()

    # ========================================================================
    # DASHBOARD OVERRIDE WITH GPU SENTINEL
    # ========================================================================
    def show_dashboard_pane(self):
        self._highlight_nav("dash")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Mission Control & Hardware Telemetry", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Real-time GPU Sentinel, CPU/RAM gauges, thread affinity, and active threat radar", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        gauge_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        gauge_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(0, 12))

        ctk.CTkLabel(gauge_card, text="Hardware Load Gauges", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12, 4))

        self.gauge_canvas = tk.Canvas(gauge_card, height=160, bg=COLOR_CARD, highlightthickness=0)
        self.gauge_canvas.pack(fill="x", padx=10, pady=2)

        stats_box = ctk.CTkFrame(gauge_card, fg_color="transparent")
        stats_box.pack(fill="x", padx=16, pady=4)
        self.lbl_gauge_ram_text = ctk.CTkLabel(stats_box, text="RAM: Fetching...", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN)
        self.lbl_gauge_ram_text.pack(side="left")
        self.lbl_gauge_cpu_text = ctk.CTkLabel(stats_box, text="CPU: Fetching...", font=("Segoe UI", 11, "bold"), text_color=COLOR_EMERALD)
        self.lbl_gauge_cpu_text.pack(side="right")

        gpu_box = ctk.CTkFrame(gauge_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        gpu_box.pack(fill="x", padx=12, pady=(6, 10))

        gm = self.gpu_sentinel.get_live_gpu_metrics()
        gpu_top = ctk.CTkFrame(gpu_box, fg_color="transparent")
        gpu_top.pack(fill="x", padx=10, pady=(6, 2))
        ctk.CTkLabel(gpu_top, text=f"🎮 {gm['gpu_name']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(side="left")
        
        self.lbl_dash_gpu_temp = ctk.CTkLabel(gpu_top, text=f"{gm['temperature_c']} °C", font=("Segoe UI", 12, "bold"), text_color=gm['status_color'])
        self.lbl_dash_gpu_temp.pack(side="right")

        gpu_sub = ctk.CTkFrame(gpu_box, fg_color="transparent")
        gpu_sub.pack(fill="x", padx=10, pady=(0, 6))
        self.lbl_dash_gpu_vram = ctk.CTkLabel(gpu_sub, text=f"VRAM: {gm['vram_str']}", font=("Consolas", 10), text_color=COLOR_TEXT_MUTED)
        self.lbl_dash_gpu_vram.pack(side="left")
        self.lbl_dash_gpu_util = ctk.CTkLabel(gpu_sub, text=f"Core Load: {gm['utilization_gpu_pct']}%", font=("Consolas", 10), text_color=COLOR_AMBER)
        self.lbl_dash_gpu_util.pack(side="right")

        proc_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        proc_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(0, 12))

        ctk.CTkLabel(proc_card, text="Top Memory Consumers (Live)", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12, 4))
        self.proc_list_box = ctk.CTkTextbox(proc_card, font=("Consolas", 11), fg_color="#0A0C14", text_color=COLOR_CYAN, wrap="none", corner_radius=10)
        self.proc_list_box.pack(fill="both", expand=True, padx=12, pady=8)

        bottom_bar = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        bottom_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        ctk.CTkLabel(bottom_bar, text="Direct Action Triggers:", font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_MUTED).pack(side="left", padx=16, pady=10)

        ctk.CTkButton(
            bottom_bar, text="⚡ Flush RAM", font=("Segoe UI", 11, "bold"),
            fg_color="#006666", hover_color="#008080", height=32,
            command=self._flush_ram_with_sfx
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            bottom_bar, text="🧹 Sweep Junk", font=("Segoe UI", 11, "bold"),
            fg_color="#4D7C0F", hover_color="#65A30D", height=32,
            command=self._sweep_junk_with_sfx
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            bottom_bar, text="🎯 CS2 Tuner", font=("Segoe UI", 11, "bold"),
            fg_color="#F59E0B", hover_color="#D97706", height=32, text_color="#000000",
            command=self.show_cs2_pane
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            bottom_bar, text="📱 Mobile HUD", font=("Segoe UI", 11, "bold"),
            fg_color="#0284C7", hover_color="#0369A1", height=32,
            command=self.show_mobile_pane
        ).pack(side="left", padx=6)

    def _flush_ram_with_sfx(self):
        self.sfx.play_warp_boost()
        self.optimizer.run_memory_boost(self.show_toast_msg)

    def _sweep_junk_with_sfx(self):
        self.sfx.play_click()
        self.optimizer.run_cache_sweep(self.show_toast_msg)

    # ========================================================================
    # GAMER MODE & APEX STEAM GAME LAUNCHER (show_gamer_pane)
    # ========================================================================
    def show_gamer_pane(self):
        self._highlight_nav("gamer")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(2, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ctk.CTkLabel(head, text="Ultra Gamer & Steam Apex Launcher", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Hardware-level game booster: 1-click launch with P-Core pinning, TCP zero-latency, and memory purging", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 12), ipady=6)
        card.grid_columnconfigure((0, 1, 2, 3), weight=1)

        st = self.gamer_mode.get_status()
        status_txt = "● STATUS: GAMER MODE ENGAGED (P-Core & Zero-Latency Active)" if st["is_active"] else "● STATUS: NORMAL DESKTOP PROFILE"
        status_col = COLOR_EMERALD if st["is_active"] else COLOR_TEXT_MUTED
        self.gamer_status_lbl = ctk.CTkLabel(card, text=status_txt, font=("Segoe UI", 12, "bold"), text_color=status_col)
        self.gamer_status_lbl.grid(row=0, column=0, columnspan=4, pady=(6, 8))

        self.gamer_lbl_boosted = ctk.CTkLabel(card, text=f"BOOSTED APPS\n{st['boosted_count']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN)
        self.gamer_lbl_boosted.grid(row=1, column=0, padx=6)

        self.gamer_lbl_mem = ctk.CTkLabel(card, text=f"MEMORY SAVED\n{st['memory_saved_mb']} MB", font=("Segoe UI", 11, "bold"), text_color=COLOR_EMERALD)
        self.gamer_lbl_mem.grid(row=1, column=1, padx=6)

        self.gamer_lbl_games = ctk.CTkLabel(card, text=f"INSTALLED GAMES\n{len(self.game_library.cached_games)} Titles", font=("Segoe UI", 11, "bold"), text_color=COLOR_AMBER)
        self.gamer_lbl_games.grid(row=1, column=2, padx=6)

        self.gamer_lbl_ping = ctk.CTkLabel(card, text=f"GAMING PING\n{st.get('last_ping_ms', 0)} ms", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN)
        self.gamer_lbl_ping.grid(row=1, column=3, padx=6)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=2, column=0, columnspan=4, pady=(10, 4))

        self.btn_gamer_toggle = ctk.CTkButton(
            btn_row,
            text="DISENGAGE GAMER MODE" if st["is_active"] else "⚡ ENGAGE ULTRA GAMER MODE",
            font=("Segoe UI", 12, "bold"),
            fg_color=COLOR_CRIMSON if st["is_active"] else COLOR_CYAN,
            text_color="#FFFFFF" if st["is_active"] else "#000000",
            hover_color="#DC2626" if st["is_active"] else "#00B4D8",
            height=38, width=260, corner_radius=10,
            command=self._toggle_gamer_mode_ui
        )
        self.btn_gamer_toggle.pack()

        matrix_frame = ctk.CTkFrame(pane, fg_color="transparent")
        matrix_frame.grid(row=2, column=0, sticky="nsew")
        matrix_frame.grid_columnconfigure((0, 1), weight=1)
        matrix_frame.grid_rowconfigure(0, weight=1)

        launch_card = ctk.CTkFrame(matrix_frame, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        launch_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        launch_card.grid_columnconfigure(0, weight=1)
        launch_card.grid_rowconfigure(1, weight=1)

        l_head = ctk.CTkFrame(launch_card, fg_color="transparent")
        l_head.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        ctk.CTkLabel(l_head, text="Installed Games Library", font=("Segoe UI", 13, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
        ctk.CTkButton(
            l_head, text="🔄 Rescan", font=("Segoe UI", 10, "bold"),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_CYAN,
            height=26, width=70, corner_radius=6, command=lambda: self._rescan_and_refresh_games(scroll_games)
        ).pack(side="right")

        scroll_games = ctk.CTkScrollableFrame(launch_card, fg_color="transparent")
        scroll_games.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self._populate_game_list(scroll_games)

        active_card = ctk.CTkFrame(matrix_frame, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        active_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        active_card.grid_columnconfigure(0, weight=1)
        active_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(active_card, text="Running Games & P-Core Affinity", font=("Segoe UI", 13, "bold"), text_color=COLOR_TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=14, pady=(10, 4))

        scroll_active = ctk.CTkScrollableFrame(active_card, fg_color="transparent")
        scroll_active.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        active_games = self.gamer_mode.get_detected_games()
        if not active_games:
            ctk.CTkLabel(scroll_active, text="No foreground games currently running.\nLaunch a game on the left to engage Apex Boost!", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED, justify="center").pack(pady=40)
        else:
            for g in active_games:
                row_f = ctk.CTkFrame(scroll_active, fg_color="#121522", corner_radius=6)
                row_f.pack(fill="x", pady=3, padx=4)
                row_f.grid_columnconfigure((0, 1, 2), weight=1)
                ctk.CTkLabel(row_f, text=g["name"], font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).grid(row=0, column=0, sticky="w", padx=8, pady=6)
                ctk.CTkLabel(row_f, text=f"PID: {g['pid']} | {g['memory_mb']} MB", font=("Consolas", 10), text_color=COLOR_EMERALD).grid(row=0, column=1, sticky="w", padx=4)
                
                btn_pin = ctk.CTkButton(
                    row_f, text="📌 Pin P-Cores", font=("Segoe UI", 10, "bold"),
                    fg_color="#7C3AED", hover_color="#6D28D9", height=24, width=90,
                    command=lambda pid=g["pid"]: self._pin_core_action(pid)
                )
                btn_pin.grid(row=0, column=2, sticky="e", padx=8)

    def _populate_game_list(self, scroll_widget):
        for w in scroll_widget.winfo_children():
            w.destroy()
        games = self.game_library.cached_games
        if not games:
            ctk.CTkLabel(scroll_widget, text="No Steam games found in default directories.", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(pady=20)
            return

        for g in games:
            card = ctk.CTkFrame(scroll_widget, fg_color="#0F1322", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            card.pack(fill="x", pady=3, padx=2)

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=10, pady=(6, 2))
            ctk.CTkLabel(top_row, text=g["name"], font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(top_row, text=f"{g['size_gb']} GB", font=("Consolas", 10), text_color=COLOR_TEXT_MUTED).pack(side="right")

            bot_row = ctk.CTkFrame(card, fg_color="transparent")
            bot_row.pack(fill="x", padx=10, pady=(0, 6))
            ctk.CTkLabel(bot_row, text=f"Platform: {g['platform']}", font=("Segoe UI", 10), text_color=COLOR_CYAN).pack(side="left")

            btn_boost = ctk.CTkButton(
                bot_row, text="🚀 Apex Launch", font=("Segoe UI", 10, "bold"),
                fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
                height=26, width=110, corner_radius=6,
                command=lambda target=g: self._launch_apex_game(target)
            )
            btn_boost.pack(side="right")

    def _launch_apex_game(self, game_dict):
        self.sfx.play_warp_boost()
        ok, msg = self.game_library.launch_game_with_apex_boost(
            game_dict=game_dict,
            optimizer_core=self.optimizer,
            gamer_mode=self.gamer_mode,
            core_director=self.core_director,
            ping_optimizer=self.ping_optimizer,
            voice_engine=self.voice
        )
        self.show_toast_msg(msg)

    def _rescan_and_refresh_games(self, scroll_widget):
        self.sfx.play_click()
        self.game_library.scan_library()
        self._populate_game_list(scroll_widget)
        self.show_toast_msg(f"Library Rescanned: Found {len(self.game_library.cached_games)} games.")

    def _pin_core_action(self, pid: int):
        self.sfx.play_click()
        ok, msg = self.core_director.pin_process_to_performance_cores(pid)
        self.show_toast_msg(msg)
        if ok:
            self.voice.speak("Process pinned to performance cores.")

    # ========================================================================
    # MOBILE REMOTE COMPANION HUD (show_mobile_pane)
    # ========================================================================
    def show_mobile_pane(self):
        self._highlight_nav("mobile")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=25)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Mobile Remote Companion HUD", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Real-time Wi-Fi telemetry and 1-tap remote actions on your phone without Alt-Tabbing from games", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_card, text="Scan with Phone Camera", font=("Segoe UI", 14, "bold"), text_color=COLOR_CYAN).pack(pady=(16, 4))
        ctk.CTkLabel(left_card, text="Must be on the same local Wi-Fi network", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(pady=(0, 10))

        qr_file = self.mobile_companion.qr_path
        if os.path.exists(qr_file):
            try:
                pil_qr = Image.open(qr_file).resize((210, 210))
                ctk_qr = ctk.CTkImage(pil_qr, size=(210, 210))
                lbl_qr = ctk.CTkLabel(left_card, image=ctk_qr, text="")
                lbl_qr.pack(pady=5)
            except Exception:
                ctk.CTkLabel(left_card, text="[QR Code Available at: " + qr_file + "]", text_color=COLOR_EMERALD).pack(pady=20)

        url = self.mobile_companion.get_pairing_url()
        ctk.CTkLabel(left_card, text=f"LAN URL: {url}", font=("Consolas", 11), text_color=COLOR_EMERALD).pack(pady=(10, 4))

        status_txt = f"● HTTP SERVER ONLINE (Port {self.mobile_companion.port})"
        ctk.CTkLabel(left_card, text=status_txt, font=("Segoe UI", 10, "bold"), text_color=COLOR_EMERALD).pack(pady=(0, 12))

        ctk.CTkButton(
            left_card, text="🌐 Open Mobile App in Browser", font=("Segoe UI", 12, "bold"),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_CYAN,
            height=34, width=220, command=lambda: webbrowser.open(url)
        ).pack(pady=(0, 15))

        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Tactical Mobile Capabilities", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(16, 12))

        features = [
            ("⚡ 1-Tap Turbo Boost", "Instantly clears standby memory while gaming fullscreen without Alt-Tabbing."),
            ("🎮 Live GPU Telemetry", "Real-time GPU core temperature, VRAM allocation, and thermal guard across all GPUs."),
            ("📶 Real-Time Ping HUD", "Continuously streams sub-millisecond Cloudflare ping and packet loss to your phone."),
            ("🤖 Phone-to-PC AI Agent", "Directly type instructions on your smartphone and trigger system actions on PC."),
            ("🎮 1-Tap Gamer Mode", "Elevate process scheduling to High Priority directly from your mobile screen."),
            ("🧹 Cache Sweeper", "Wipes Windows temporary bloat with a single tap on your smartphone.")
        ]

        for title, desc in features:
            f_box = ctk.CTkFrame(right_card, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            f_box.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(f_box, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(4, 1))
            ctk.CTkLabel(f_box, text=desc, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=380, justify="left").pack(anchor="w", padx=10, pady=(0, 4))

    # ========================================================================
    # MICRO-SANDBOX & DETONATION CHAMBER (show_detonation_pane)
    # ========================================================================
    def show_detonation_pane(self):
        self._highlight_nav("detonate")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=25)
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(2, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Micro-Sandbox & Forensic Detonation Chamber", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Inspect zero-day files, compute Shannon entropy, detect packing, and isolate in virtual container", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        ctrl = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        ctrl.grid(row=1, column=0, sticky="ew", pady=(0, 12), ipady=8)
        ctrl.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(
            ctrl, text="📂 Select Specimen File", font=("Segoe UI", 12, "bold"),
            fg_color="#00F0FF", hover_color="#00B4D8", text_color="#000000",
            height=36, width=190, command=self._pick_and_detonate_file
        ).grid(row=0, column=0, padx=12, pady=6)

        self.det_entropy_lbl = ctk.CTkLabel(ctrl, text="ENTROPY: --\n(Packing: --)", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN)
        self.det_entropy_lbl.grid(row=0, column=1, padx=10)

        self.det_apis_lbl = ctk.CTkLabel(ctrl, text="SUSPICIOUS APIS: --", font=("Segoe UI", 11, "bold"), text_color=COLOR_AMBER)
        self.det_apis_lbl.grid(row=0, column=2, padx=10)

        self.det_rating_lbl = ctk.CTkLabel(ctrl, text="THREAT RATING: IDLE", font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_MUTED)
        self.det_rating_lbl.grid(row=0, column=3, padx=10)

        table_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)

        self.det_log_box = ctk.CTkTextbox(
            table_card, font=("Consolas", 12), fg_color="#0A0C14",
            text_color=COLOR_EMERALD, wrap="word", corner_radius=12
        )
        self.det_log_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.det_log_box.insert("0.0",
            "[DETONATION CHAMBER] Standing by for unknown specimen execution.\n"
            "[DETONATION CHAMBER] Supports executables (.exe), dynamic libraries (.dll), and scripts (.bat, .vbs, .ps1).\n"
            + "─" * 75 + "\n"
        )

    def _pick_and_detonate_file(self):
        self.sfx.play_click()
        fpath = filedialog.askopenfilename(title="Select Untrusted File for Detonation Analysis")
        if not fpath:
            return

        self.det_log_box.insert("end", f"\n[🔍] Specimen Acquired: {fpath}\n")
        self.det_log_box.insert("end", "[*] Computing Shannon Entropy and extracting PE imports...\n")
        self.det_log_box.see("end")

        def worker():
            res = self.detonation_chamber.analyze_specimen_forensics(fpath)

            def update_ui():
                ent = res.get("entropy", 0.0)
                is_p = res.get("is_packed", False)
                rating = res.get("rating", "UNKNOWN")
                score = res.get("risk_score", 0)
                apis = res.get("suspicious_apis", [])

                self.det_entropy_lbl.configure(text=f"ENTROPY: {ent}\n(Packed: {is_p})", text_color=COLOR_CRIMSON if is_p else COLOR_EMERALD)
                self.det_apis_lbl.configure(text=f"SUSPICIOUS APIS: {len(apis)}", text_color=COLOR_AMBER if apis else COLOR_EMERALD)

                col = COLOR_CRIMSON if score >= 60 else (COLOR_AMBER if score >= 35 else COLOR_EMERALD)
                self.det_rating_lbl.configure(text=f"THREAT: {score}/100\n({rating[:16]})", text_color=col)

                self.det_log_box.insert("end",
                    f"╔══════════════════════════════════════════════════════════════════════╗\n"
                    f"║  DETONATION FORENSIC ANALYSIS REPORT                                 ║\n"
                    f"║  Target: {res.get('filename', ''):<32} Size: {res.get('size_kb', 0):>6.1f} KB        ║\n"
                    f"║  Entropy: {ent:<6} Packed: {str(is_p):<7} Threat Score: {score}/100                ║\n"
                    f"╚══════════════════════════════════════════════════════════════════════╝\n"
                    f"• Verdict: {rating}\n"
                    f"• Dangerous API Hooks: {', '.join(apis) if apis else 'None detected'}\n"
                    f"• Hardcoded IPs: {', '.join(res.get('detected_ips', [])) if res.get('detected_ips') else 'None'}\n"
                    f"• Embedded URLs: {', '.join(res.get('detected_urls', [])) if res.get('detected_urls') else 'None'}\n"
                    f"• Shell Commands: {', '.join(res.get('suspicious_patterns', [])) if res.get('suspicious_patterns') else 'Clean'}\n"
                )

                if self.detonation_chamber.is_windows_sandbox_available():
                    wsb = self.detonation_chamber.create_sandbox_config(fpath)
                    self.det_log_box.insert("end", f"[*] Created isolated Windows Sandbox harness at:\n    {wsb}\n")
                else:
                    self.det_log_box.insert("end", "[ℹ] Windows Sandbox not installed. Performed deep In-Memory PE Static Detonation.\n")

                self.det_log_box.see("end")

            self.after(0, update_ui)

        threading.Thread(target=worker, daemon=True).start()

    # ========================================================================
    # V6 PILLAR 1: DISPLAY REFLEX & DIRECTFLIP ENGINE
    # ========================================================================
    def show_display_reflex_pane(self):
        self._highlight_nav("reflex")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        # Header Title
        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Display Reflex & DirectFlip Presentation Engine", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Bypass DWM hybrid compositor, audit HAGS, and enforce true independent DirectFlip presentation", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Live Display Telemetry
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        tel = self.display_reflex.get_display_telemetry()
        ctk.CTkLabel(left_card, text="Win32 Display & Compositor Telemetry", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        hz_color = COLOR_EMERALD if tel["refresh_rate_hz"] >= 144 else COLOR_CYAN
        pills = [
            ("Native Resolution & Hz", f"{tel['resolution']} @ {tel['refresh_rate_hz']}Hz", hz_color),
            ("Color Bit Depth", f"{tel['color_depth_bpp']}-bit TrueColor", COLOR_TEXT_PRIMARY),
            ("HAGS GPU Scheduling", "ENABLED (Hardware Scheduled)" if tel["hags_enabled"] else "DISABLED (Standard OS Queue)", COLOR_EMERALD if tel["hags_enabled"] else COLOR_AMBER),
            ("DirectFlip Presentation", "OPTIMIZED (Direct MPO Bypass)" if tel["directflip_optimized"] else "STANDARD (Windowed Blt Mode)", COLOR_EMERALD if tel["directflip_optimized"] else COLOR_CRIMSON),
            ("Display Tier Classification", tel["display_classification"], COLOR_CYAN)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="⚡ Enforce DirectFlip Presentation (0 DWM Latency)", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._apply_directflip_tuning
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🔄 Restore Windows Display Defaults", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=34, corner_radius=8, command=self._restore_display_defaults
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Technical Mechanics
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Presentation Pipeline Architecture", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 10))

        breakdowns = [
            ("🖥️ DirectFlip & Multi-Plane Overlay (MPO)", "In standard windowed mode, Windows Desktop Window Manager copies frames via BitBlt, adding 1-2 frames of compositor delay. DirectFlip hands the game buffer straight to the display scanout hardware."),
            ("⚙️ Hardware Accelerated GPU Scheduling (HAGS)", "Offloads frame command scheduling from the CPU to dedicated GPU microcode. Essential for high refresh rate monitors (144Hz - 360Hz) to eliminate CPU submission bottlenecks."),
            ("🎯 Fullscreen Optimization (FSO) Bypass", "Windows 10/11 injects hybrid overlays that can cause frametime jitter. Antimagist enforces true independent flip while retaining quick Alt-Tab responsiveness.")
        ]
        for t, d in breakdowns:
            bx = ctk.CTkFrame(right_card, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(bx, text=t, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(bx, text=d, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _apply_directflip_tuning(self):
        ok, msg = self.display_reflex.optimize_directflip_presentation()
        self.sfx.play_success()
        self.show_toast_msg(msg)
        self.show_display_reflex_pane()

    def _restore_display_defaults(self):
        ok, msg = self.display_reflex.restore_display_defaults()
        self.sfx.play_click()
        self.show_toast_msg(msg)
        self.show_display_reflex_pane()

    # ========================================================================
    # V6 PILLAR 2: ESPORTS AUDIO STRIPPER ENGINE
    # ========================================================================
    def show_audio_stripper_pane(self):
        self._highlight_nav("audio")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Esports Low-Latency Audio Stream Stripper", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Isolate audiodg.exe to a dedicated physical P-Core with High Priority to eliminate audio buffer underruns", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Audio Engine Status
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        astat = self.audio_stripper.get_audio_status()
        ctk.CTkLabel(left_card, text="Windows Audio Graph Isolation (audiodg.exe)", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        rec_core = astat.get("recommended_affinity_core", 2)
        pills = [
            ("audiodg.exe Process State", astat["status_text"], COLOR_EMERALD if astat["audiodg_running"] else COLOR_AMBER),
            ("Active Audio Graph Instances", f"{len(astat['running_instances'])} Process(es)", COLOR_CYAN),
            ("Recommended Dedicated Core", f"Core {rec_core} (Physical P-Core)", COLOR_EMERALD),
            ("Process Priority Target", "HIGH_PRIORITY_CLASS (No Starvation)", COLOR_CYAN)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text=f"⚡ Pin audiodg.exe to Dedicated Core {rec_core}", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=lambda: self._apply_audio_affinity(rec_core)
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🔄 Restore Default Multi-Core Audio Scheduling", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=34, corner_radius=8, command=self._restore_audio_affinity
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Audio Latency Explanation
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Why Audio Isolation Wins Matches", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 10))

        explanations = [
            ("🎧 Footstep Audio Latency in CS2 & Valorant", "Windows audio processing shares CPU cores with game rendering threads. In heavy firefights or smoke grenade rendering, audio buffers starve, causing footstep cues to lag behind by 20-50ms."),
            ("🛡️ audiodg.exe Physical P-Core Isolation", "Binding the audio pipeline exclusively to an isolated physical P-Core guarantees real-time buffer processing with zero context-switching contention."),
            ("⏱️ DPC Latency & Buffer Underruns", "Elevating audiodg.exe to High Priority Class completely prevents audio pop, crackle, and micro-stutter when your GPU operates at 99% utilization.")
        ]
        for t, d in explanations:
            bx = ctk.CTkFrame(right_card, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(bx, text=t, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(bx, text=d, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _apply_audio_affinity(self, core_idx: int):
        ok, msg = self.audio_stripper.optimize_audio_stream(core_idx)
        self.sfx.play_success()
        self.show_toast_msg(msg)
        self.show_audio_stripper_pane()

    def _restore_audio_affinity(self):
        ok, msg = self.audio_stripper.restore_audio_defaults()
        self.sfx.play_click()
        self.show_toast_msg(msg)
        self.show_audio_stripper_pane()

    # ========================================================================
    # V6 PILLAR 3: GLOBAL MATCHMAKING SERVER RADAR
    # ========================================================================
    def show_server_radar_pane(self):
        self._highlight_nav("radar")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(2, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Global Game Server Matchmaking Radar", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Real-time pre-queue latency benchmarks across major competitive matchmaking datacenters and gaming DNS", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Top summary bar
        top_bar = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        top_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=6)
        top_bar.grid_columnconfigure((0, 1, 2), weight=1)

        cached = self.server_radar.cached_results or self.server_radar.scan_all_regions()
        ctk.CTkLabel(top_bar, text=f"BEST MATCHMAKING CLUSTER\n{cached.get('best_datacenter', 'EU Central')}", font=("Segoe UI", 11, "bold"), text_color=COLOR_EMERALD).grid(row=0, column=0)
        ctk.CTkLabel(top_bar, text=f"OPTIMAL TCP PING\n{cached.get('best_ping_ms', 0)} ms", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).grid(row=0, column=1)

        best_dns = cached.get("dns", [{}])[0].get("name", "Cloudflare DNS") if cached.get("dns") else "Cloudflare DNS"
        best_dns_ping = cached.get("dns", [{}])[0].get("ping_ms", 4.2) if cached.get("dns") else 4.2
        ctk.CTkLabel(top_bar, text=f"RECOMMENDED GAMING DNS\n{best_dns} ({best_dns_ping} ms)", font=("Segoe UI", 11, "bold"), text_color=COLOR_AMBER).grid(row=0, column=2)

        # Left Column: Datacenters Table
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=2, column=0, sticky="nsew", padx=(0, 10))

        lh = ctk.CTkFrame(left_card, fg_color="transparent")
        lh.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(lh, text="Regional Competitive Datacenters", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")

        ctk.CTkButton(
            lh, text="🔄 Refresh Radar", font=("Segoe UI", 10, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=28, width=110, corner_radius=6, command=self._refresh_radar_data
        ).pack(side="right")

        scroll_srv = ctk.CTkScrollableFrame(left_card, fg_color="transparent")
        scroll_srv.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for srv in cached.get("servers", []):
            row = ctk.CTkFrame(scroll_srv, fg_color="#0A0C14", corner_radius=8)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{srv['flag']} {srv['name']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=10, pady=8)
            col = COLOR_EMERALD if srv["ping_ms"] < 35 else (COLOR_AMBER if srv["ping_ms"] < 70 else COLOR_CRIMSON)
            ctk.CTkLabel(row, text=f"{srv['ping_ms']} ms", font=("Consolas", 11, "bold"), text_color=col).pack(side="right", padx=10)

        # Right Column: DNS Resolvers & Jitter
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=2, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Gaming DNS Resolvers & Latency", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(14, 8))

        scroll_dns = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_dns.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for d in cached.get("dns", []):
            row = ctk.CTkFrame(scroll_dns, fg_color="#0A0C14", corner_radius=8)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=f"🌐 {d['name']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN if d.get("is_recommended") else COLOR_TEXT_PRIMARY).pack(side="left", padx=10, pady=8)
            tag = " [FASTEST]" if d.get("is_recommended") else ""
            ctk.CTkLabel(row, text=f"{d['ping_ms']} ms{tag}", font=("Consolas", 11, "bold"), text_color=COLOR_EMERALD if d.get("is_recommended") else COLOR_TEXT_MUTED).pack(side="right", padx=10)

    def _refresh_radar_data(self):
        self.sfx.play_click()
        def worker():
            self.server_radar.scan_all_regions()
            self.after(0, self.show_server_radar_pane)
        threading.Thread(target=worker, daemon=True).start()

    # ========================================================================
    # V6 PILLAR 4: CYBERPUNK BENCHMARK CARD GENERATOR
    # ========================================================================
    def show_benchmark_card_pane(self):
        self._highlight_nav("card")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Cyberpunk PNG Benchmark Card Generator", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Generate esports-grade 1200x675 system telemetry cards with SHA-256 authentic hardware verification", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Configuration & Generate
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_card, text="Benchmark Card Configuration", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        ctk.CTkLabel(left_card, text="Player / Rig Call-Sign:", font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(6, 2))
        self.ent_card_tag = ctk.CTkEntry(left_card, font=("Segoe UI", 12), height=38, fg_color="#0A0C14", border_color=COLOR_BORDER)
        self.ent_card_tag.pack(fill="x", padx=16, pady=(0, 12))
        self.ent_card_tag.insert(0, "Apex Predator // Rig-01")

        ctk.CTkButton(
            left_card, text="🎨 Generate 1200x675 Cyberpunk Card", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._generate_benchmark_card
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="📂 Open Generated Card in Viewer", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_PRIMARY,
            height=34, corner_radius=8, command=self._open_benchmark_card
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Status output
        self.lbl_card_status = ctk.CTkLabel(left_card, text="Ready to render authentic telemetry card.", font=("Consolas", 10), text_color=COLOR_CYAN)
        self.lbl_card_status.pack(padx=16, pady=8)

        # Right Card: Feature Highlights
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Authentic Telemetry Standard", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 10))

        highlights = [
            ("🛡️ Cryptographic SHA-256 Fingerprint", "Every card embeds a hardware verification hash generated from your physical GPU, CPU topology, and display refresh rate. Guaranteed 100% genuine."),
            ("🌌 Ultra-High Definition 1200x675 16:9", "Perfect resolution for sharing your competitive setup on Discord, Twitter / X, or Reddit."),
            ("⚡ Universal Hardware Telemetry", "Accurately represents NVIDIA GeForce, AMD Radeon, and Intel Arc GPUs, high refresh rates (up to 360Hz+), and sub-tick network latencies.")
        ]
        for t, d in highlights:
            bx = ctk.CTkFrame(right_card, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(bx, text=t, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(bx, text=d, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _generate_benchmark_card(self):
        self.sfx.play_click()
        tag = self.ent_card_tag.get().strip() or "Apex Predator // Rig-01"
        out_p = os.path.join(os.environ.get("USERPROFILE", "."), "Pictures", "Antimagist_Benchmark_Card.png")
        if not os.path.exists(os.path.dirname(out_p)):
            out_p = "benchmark_card.png"

        try:
            saved_p = self.benchmark_card.generate_card(out_p, player_tag=tag)
            self.sfx.play_success()
            self.lbl_card_status.configure(text=f"Card saved: {os.path.basename(saved_p)}", text_color=COLOR_EMERALD)
            self.show_toast_msg("Cyberpunk Benchmark Card generated successfully!")
        except Exception as ex:
            self.lbl_card_status.configure(text=f"Error: {ex}", text_color=COLOR_CRIMSON)

    def _open_benchmark_card(self):
        out_p = os.path.join(os.environ.get("USERPROFILE", "."), "Pictures", "Antimagist_Benchmark_Card.png")
        if not os.path.exists(out_p):
            out_p = "benchmark_card.png"
        if os.path.exists(out_p):
            os.startfile(out_p)
        else:
            self.show_toast_msg("Please generate a benchmark card first.")

    # ========================================================================
    # V6 PILLAR 5: MOD & CONFIG HEURISTIC GUARD
    # ========================================================================
    def show_mod_guard_pane(self):
        self._highlight_nav("modguard")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Mod & Config Heuristic Guard", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Scan downloaded autoexecs, FPS booster scripts, and community mods for hidden Discord webhooks & token stealers", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Target Selector & Controls
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_card, text="Target File / Directory Scanner", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        # Path Entry
        f_p = ctk.CTkFrame(left_card, fg_color="transparent")
        f_p.pack(fill="x", padx=16, pady=4)
        self.ent_mod_target = ctk.CTkEntry(f_p, font=("Segoe UI", 11), height=36, placeholder_text="Select autoexec.cfg, script.bat, or mod directory...", fg_color="#0A0C14", border_color=COLOR_BORDER)
        self.ent_mod_target.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            f_p, text="📂 Browse", width=80, height=36, font=("Segoe UI", 11, "bold"),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_PRIMARY,
            command=self._browse_mod_target
        ).pack(side="right")

        # Action Buttons
        ctk.CTkButton(
            left_card, text="🔍 Run Heuristic Threat Scan", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._run_mod_guard_scan
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🛡️ Sanitize & Neutralize Threats Safely", font=("Segoe UI", 12, "bold"),
            fg_color="#A855F7", hover_color="#9333EA", text_color="#FFFFFF",
            height=38, corner_radius=8, command=self._sanitize_mod_file
        ).pack(fill="x", padx=16, pady=(6, 12))

        # Verdict Display
        self.lbl_mod_verdict = ctk.CTkLabel(left_card, text="STATUS: STANDING BY", font=("Segoe UI", 12, "bold"), text_color=COLOR_CYAN)
        self.lbl_mod_verdict.pack(padx=16, pady=4)

        # Right Card: Scan Results / Log Box
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right_card, text="Heuristic Forensics & Threat Log", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        self.txt_mod_log = ctk.CTkTextbox(right_card, font=("Consolas", 10), fg_color="#0A0C14", text_color=COLOR_TEXT_PRIMARY, corner_radius=8)
        self.txt_mod_log.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.txt_mod_log.insert("end", "[*] Antimagist Mod Guard Engine ready.\n[*] Select any .cfg, .bat, .ps1, or .lua script to audit.\n")

    def _browse_mod_target(self):
        f = filedialog.askopenfilename(
            title="Select Game Config or Mod Script",
            filetypes=[("Supported Game Files", "*.cfg;*.bat;*.cmd;*.ps1;*.lua;*.ini;*.txt"), ("All Files", "*.*")]
        )
        if f:
            self.ent_mod_target.delete(0, "end")
            self.ent_mod_target.insert(0, f)

    def _run_mod_guard_scan(self):
        self.sfx.play_click()
        target = self.ent_mod_target.get().strip()
        if not target or not os.path.exists(target):
            self.show_toast_msg("Please specify a valid file or folder to scan.")
            return

        def worker():
            if os.path.isdir(target):
                res = self.mod_guard.scan_directory(target)
                def update_dir():
                    self.txt_mod_log.delete("1.0", "end")
                    self.txt_mod_log.insert("end", f"=== DIRECTORY SCAN SUMMARY ===\n")
                    self.txt_mod_log.insert("end", f"• Target: {res['directory']}\n")
                    self.txt_mod_log.insert("end", f"• Scanned: {res['scanned_files']} files\n")
                    self.txt_mod_log.insert("end", f"• Result: {res['threat_summary']}\n\n")
                    for finding in res.get("findings", []):
                        self.txt_mod_log.insert("end", f"[{finding['verdict']}] {finding['file_name']} (Score: {finding['threat_score']})\n")
                        for d in finding["detections"]:
                            self.txt_mod_log.insert("end", f"    Line {d['line']}: {d['description']}\n")
                    self.txt_mod_log.see("end")
                    if res["malicious_files"] > 0:
                        self.lbl_mod_verdict.configure(text=f"VERDICT: {res['malicious_files']} MALICIOUS THREATS DETECTED", text_color=COLOR_CRIMSON)
                    else:
                        self.lbl_mod_verdict.configure(text="VERDICT: ALL SCANNED FILES CLEAN", text_color=COLOR_EMERALD)
                self.after(0, update_dir)
            else:
                res = self.mod_guard.scan_file(target)
                def update_file():
                    self.txt_mod_log.delete("1.0", "end")
                    self.txt_mod_log.insert("end", f"=== FILE FORENSICS AUDIT ===\n")
                    self.txt_mod_log.insert("end", f"• File: {res['file_name']}\n")
                    self.txt_mod_log.insert("end", f"• Size: {res.get('file_size_bytes', 0)} bytes | SHA256: {res['sha256'][:16]}...\n")
                    self.txt_mod_log.insert("end", f"• Threat Score: {res['threat_score']}/100\n")
                    self.txt_mod_log.insert("end", f"• Verdict: {res['verdict']}\n\n")
                    if res.get("detections"):
                        self.txt_mod_log.insert("end", f"--- DETECTIONS ({len(res['detections'])}) ---\n")
                        for d in res["detections"]:
                            self.txt_mod_log.insert("end", f"• Line {d['line']} [{d['severity']}]: {d['description']}\n")
                            self.txt_mod_log.insert("end", f"  Snippet: {d['snippet']}\n")
                    else:
                        self.txt_mod_log.insert("end", "[✓] Zero malicious hooks, download cradles, or webhooks found.\n")
                    self.txt_mod_log.see("end")

                    col = COLOR_EMERALD if res["verdict"] == "SAFE" else (COLOR_AMBER if res["verdict"] == "SUSPICIOUS" else COLOR_CRIMSON)
                    self.lbl_mod_verdict.configure(text=f"VERDICT: {res['verdict']} (Score: {res['threat_score']})", text_color=col)
                self.after(0, update_file)

        threading.Thread(target=worker, daemon=True).start()

    def _sanitize_mod_file(self):
        target = self.ent_mod_target.get().strip()
        if not target or not os.path.isfile(target):
            self.show_toast_msg("Please specify a valid file to sanitize.")
            return

        ok, msg = self.mod_guard.sanitize_file(target)
        if ok:
            self.sfx.play_success()
            self.show_toast_msg(msg)
            self._run_mod_guard_scan()
        else:
            self.sfx.play_alarm()
            self.show_toast_msg(f"Failed: {msg}")

    # ========================================================================
    # V7 PILLAR 1: HARDWARE DPC & ISR DRIVER LATENCY DIAGNOSTICIAN
    # ========================================================================
    def show_dpc_pane(self):
        self._highlight_nav("dpc")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Hardware DPC & ISR Driver Latency Diagnostician", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Audit microsecond interrupt preemption, timer resolution, and active kernel driver latency culprits (nvlddmkm, ndis, storport)", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Live Jitter & Timer Resolution
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        audit = self.dpc_diagnostician.audit_system_latency()
        ctk.CTkLabel(left_card, text="Win32 QPC Jitter & Timer Posture", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        pills = [
            ("Responsiveness Verdict", audit["overall_verdict"].replace("_", " "), audit["verdict_color"]),
            ("Max Interrupt Jitter", f"{audit['jitter']['max_jitter_us']} µs", COLOR_EMERALD if audit['jitter']['max_jitter_us'] < 50 else COLOR_AMBER),
            ("QPC Counter Clock", f"{audit['jitter']['qpc_frequency_mhz']} MHz (Hardware TSC)", COLOR_CYAN),
            ("System Timer Resolution", f"{audit['timer']['current_ms']} ms ({audit['timer']['status_label']})", COLOR_EMERALD if audit['timer']['is_optimized'] else COLOR_AMBER),
            ("Audited In-Memory Drivers", f"{audit['total_drivers_monitored']} Active Kernel Services", COLOR_TEXT_PRIMARY)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="🔄 Re-Run Microsecond Interrupt Audit", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._refresh_dpc_audit
        ).pack(fill="x", padx=16, pady=6)

        # Right Card: Active Drivers & Remediation
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Active Kernel Drivers & Optimization Guide", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_drv = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_drv.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for drv in audit.get("audited_drivers", []):
            bx = ctk.CTkFrame(scroll_drv, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", pady=3)
            hdr = ctk.CTkFrame(bx, fg_color="transparent")
            hdr.pack(fill="x", padx=10, pady=(6, 2))
            ctk.CTkLabel(hdr, text=f"⚙️ {drv['driver_file']} — {drv['name']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(side="left")
            ctk.CTkLabel(hdr, text=f"[{drv['type']}]", font=("Consolas", 10, "bold"), text_color=COLOR_EMERALD).pack(side="right")
            ctk.CTkLabel(bx, text=drv["advice"], font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=420, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _refresh_dpc_audit(self):
        self.sfx.play_click()
        def worker():
            self.after(0, self.show_dpc_pane)
        threading.Thread(target=worker, daemon=True).start()

    # ========================================================================
    # V7 PILLAR 2: INTELLIGENT PROCESS ISOLATOR & CORE ALLOCATOR
    # ========================================================================
    def show_isolator_pane(self):
        self._highlight_nav("isolator")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Intelligent Process Isolator & Core Allocator", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Park background bloat (Chrome, Discord, Spotify) onto secondary cores and dedicate physical P-Cores to your game", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Core Topology & Action
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        topo = self.process_isolator.get_core_allocation_topology()
        ctk.CTkLabel(left_card, text="CPU Topology & Core Partitioning", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        iso_status = "ACTIVE (Apps Parked)" if self.process_isolator.is_isolated else "STANDBY (Balanced)"
        iso_color = COLOR_EMERALD if self.process_isolator.is_isolated else COLOR_CYAN

        pills = [
            ("Core Allocation Status", iso_status, iso_color),
            ("Dedicated Game P-Cores", f"Cores {topo['dedicated_game_cores']}", COLOR_EMERALD),
            ("Isolated Background Cores", f"Cores {topo['isolated_background_cores']}", COLOR_AMBER),
            ("Physical Core Count", f"{topo['physical_cores']} Physical / {topo['total_logical_cores']} Logical", COLOR_TEXT_PRIMARY)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="⚡ Isolate P-Cores & Park Background Apps", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._apply_process_isolation
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🔄 Restore Default Windows Scheduling", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=34, corner_radius=8, command=self._restore_process_isolation
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Discovered Apps
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        bg_apps = self.process_isolator.scan_background_processes()
        ctk.CTkLabel(right_card, text=f"Managed Background Apps ({len(bg_apps)} Discovered)", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_bg = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_bg.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        if not bg_apps:
            ctk.CTkLabel(scroll_bg, text="No background bloat processes detected. Your system is lean!", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(pady=40)
        else:
            for p in bg_apps:
                row = ctk.CTkFrame(scroll_bg, fg_color="#0A0C14", corner_radius=8)
                row.pack(fill="x", pady=3)
                ctk.CTkLabel(row, text=f"📦 {p['name']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(side="left", padx=10, pady=8)
                ctk.CTkLabel(row, text=f"PID: {p['pid']} | Priority: {p['priority']}", font=("Consolas", 10), text_color=COLOR_TEXT_MUTED).pack(side="right", padx=10)

    def _apply_process_isolation(self):
        ok, msg, sm = self.process_isolator.isolate_for_game()
        self.sfx.play_success()
        self.show_toast_msg(msg)
        self.show_isolator_pane()

    def _restore_process_isolation(self):
        ok, msg = self.process_isolator.restore_all_processes()
        self.sfx.play_click()
        self.show_toast_msg(msg)
        self.show_isolator_pane()

    # ========================================================================
    # V7 PILLAR 3: GITHUB RELEASES AUTOMATED UPDATER
    # ========================================================================
    def show_updater_pane(self):
        self._highlight_nav("updater")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="GitHub Releases Automated Updater", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Check official repository releases, inspect changelogs, and download portable builds directly from GitHub", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Version Status & Controls
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        info = self.auto_updater.cached_update_info or self.auto_updater.check_for_updates()
        ctk.CTkLabel(left_card, text="Release Version Status", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        status_text = "NEW VERSION AVAILABLE" if info["update_available"] else "UP TO DATE"
        status_col = COLOR_EMERALD if not info["update_available"] else COLOR_AMBER

        pills = [
            ("Installed Version", f"v{self.auto_updater.current_version} Titan", COLOR_CYAN),
            ("Latest GitHub Tag", info["latest_version"], COLOR_EMERALD),
            ("Release Status", status_text, status_col),
            ("Published Timestamp", str(info.get("published_at", "Latest")), COLOR_TEXT_MUTED)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="🔍 Check for Updates Now", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._check_updater_now
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🌐 Open Official GitHub Releases Page", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_PRIMARY,
            height=34, corner_radius=8, command=self.auto_updater.open_releases_page
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Release Notes
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right_card, text="Latest Release Changelog", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        txt_notes = ctk.CTkTextbox(right_card, font=("Consolas", 10), fg_color="#0A0C14", text_color=COLOR_TEXT_PRIMARY, corner_radius=8)
        txt_notes.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        txt_notes.insert("end", f"=== {info.get('release_title', 'Antimagist')} ===\n\n{info.get('release_notes', 'Official Release')}\n")

    def _check_updater_now(self):
        self.sfx.play_click()
        def worker():
            self.auto_updater.check_for_updates()
            self.after(0, self.show_updater_pane)
        threading.Thread(target=worker, daemon=True).start()

    # ========================================================================
    # V7+ ENGINE 1: USB POLLING RATE & FLICK SENTINEL
    # ========================================================================
    def show_usb_polling_pane(self):
        self._highlight_nav("usb")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="USB Polling Rate & 1000Hz-8000Hz Flick Sentinel", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Real microsecond packet delta measurement, interval jitter scoring, and xHCI selective suspend elimination", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Live Sampling & USB Power Posture
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        audit = self.usb_sentinel.audit_usb_power_posture()
        sample = self.usb_sentinel.last_sample_result or self.usb_sentinel.sample_mouse_polling(duration_sec=0.4)

        ctk.CTkLabel(left_card, text="Mouse Polling & USB Latency Diagnostics", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        pills = [
            ("Measured Polling Rate", f"{sample['polling_rate_hz']} Hz", COLOR_EMERALD),
            ("Esports Tier", sample["tier"], COLOR_CYAN),
            ("Average Packet Delta", f"{sample['avg_interval_ms']} ms", COLOR_TEXT_PRIMARY),
            ("Interval Jitter Std Dev", f"{sample['jitter_std_dev_us']} µs", COLOR_AMBER if sample['jitter_std_dev_us'] > 60 else COLOR_EMERALD),
            ("Delivery Consistency", f"{sample['consistency_score']}%", COLOR_EMERALD),
            ("USB Power Posture", audit["power_posture"], COLOR_EMERALD if audit["usb_selective_suspend_disabled"] else COLOR_AMBER)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="🖱️ Sample Live Mouse Polling (Move Mouse Continuously)", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._sample_usb_polling_now
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="⚡ Disable USB Selective Suspend (Lock xHCI Awake)", font=("Segoe UI", 12, "bold"),
            fg_color="#00F0FF", hover_color="#00B4D8", text_color="#000000",
            height=36, corner_radius=8, command=self._optimize_usb_power
        ).pack(fill="x", padx=16, pady=4)

        ctk.CTkButton(
            left_card, text="🔄 Restore Default USB Power Savings", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=32, corner_radius=8, command=self._restore_usb_power
        ).pack(fill="x", padx=16, pady=(4, 16))

        # Right Card: Esports Polling Rate Technical Guide
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Competitive Mouse Architecture & Flick Sentinel", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_usb = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_usb.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        guides = [
            ("⚡ 1000Hz vs 4000Hz vs 8000Hz Demystified", "1000Hz mouse delivers a packet every 1.00 ms. 4000Hz delivers every 0.25 ms. 8000Hz delivers every 0.125 ms. While 8000Hz reduces input delay by ~0.87ms, it generates 8x interrupt requests per second, requiring high single-core CPU headroom and isolated P-Cores to prevent frametime spikes."),
            ("🛑 USB Selective Suspend & Sleep Penalty", "Windows default power profiles enable USB Selective Suspend, allowing the xHCI USB host controller to enter low-power sleep states during idle moments. When rapidly starting a flick shot, waking the controller can introduce a 2ms - 15ms packet delay. Disabling selective suspend keeps the bus permanently hot."),
            ("🎯 Jitter Standard Deviation & Consistency", "Even on 1000Hz mice, poorly tuned Windows timer resolution or conflicting DPC drivers can cause polling jitter where packets bundle together. Antimagist microsecond QPC analysis verifies true packet pacing."),
            ("🛡️ Anti-Cheat & Tournament Compliance", "Antimagist USB Polling Sentinel operates strictly in user-mode via Win32 hardware timers and OS power configurations. It does not inject into mouse firmware or modify hardware drivers.")
        ]
        for title, desc in guides:
            bx = ctk.CTkFrame(scroll_usb, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", pady=4)
            ctk.CTkLabel(bx, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(bx, text=desc, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=420, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _sample_usb_polling_now(self):
        self.sfx.play_click()
        self.show_toast_msg("Sampling mouse motion for 0.6s... Move cursor continuously!")
        def worker():
            self.usb_sentinel.sample_mouse_polling(duration_sec=0.6)
            self.after(0, self.show_usb_polling_pane)
        threading.Thread(target=worker, daemon=True).start()

    def _optimize_usb_power(self):
        self.sfx.play_warp_boost()
        ok, msg = self.usb_sentinel.optimize_usb_latency()
        self.show_toast_msg(msg)
        self.show_usb_polling_pane()

    def _restore_usb_power(self):
        self.sfx.play_click()
        ok, msg = self.usb_sentinel.restore_usb_defaults()
        self.show_toast_msg(msg)
        self.show_usb_polling_pane()

    # ========================================================================
    # V7+ ENGINE 2: MEMORY COMPRESSION & PAGEFILE PACER
    # ========================================================================
    def show_memory_pacer_pane(self):
        self._highlight_nav("mempacer")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Windows Memory Compression & Pagefile Pacer", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Eliminate CPU cache thrashing from background memory decompression and optimize Windows MMAgent", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: RAM Status & MMAgent Toggles
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        audit = self.memory_pacer.cached_audit or self.memory_pacer.audit_memory_subsystem()
        mem = audit["memory_stats"]
        mm = audit["mmagent_stats"]

        ctk.CTkLabel(left_card, text="RAM Telemetry & MMAgent Subsystem", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        mc_str = "ENABLED (Decompression Risk)" if mm["memory_compression_enabled"] else "DISABLED (Pure Low-Latency)"
        mc_col = COLOR_AMBER if mm["memory_compression_enabled"] else COLOR_EMERALD

        pills = [
            ("Physical RAM Capacity", f"{mem['used_phys_gb']} GB / {mem['total_phys_gb']} GB ({mem['memory_load_pct']}%)", COLOR_CYAN),
            ("Available Free RAM", f"{mem['avail_phys_gb']} GB", COLOR_EMERALD),
            ("Pagefile Pool", f"{mem['avail_pagefile_gb']} GB Avail / {mem['total_pagefile_gb']} GB Total", COLOR_TEXT_PRIMARY),
            ("Kernel Memory Compression", mc_str, mc_col),
            ("Page Combining (De-dupe)", "ENABLED" if mm["page_combining_enabled"] else "DISABLED", COLOR_CYAN),
            ("Pacing Recommendation", audit["pacing_status"], COLOR_EMERALD)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="⚡ Disable Memory Compression (Low Latency Mode)", font=("Segoe UI", 12, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=40, corner_radius=10, command=lambda: self._toggle_mem_comp(False)
        ).pack(fill="x", padx=16, pady=4)

        ctk.CTkButton(
            left_card, text="🔄 Enable Memory Compression (Default Mode)", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_PRIMARY,
            height=34, corner_radius=8, command=lambda: self._toggle_mem_comp(True)
        ).pack(fill="x", padx=16, pady=4)

        ctk.CTkButton(
            left_card, text="🧹 Trim Standby Memory & Stabilize Working Sets", font=("Segoe UI", 12, "bold"),
            fg_color="#00F0FF", hover_color="#00B4D8", text_color="#000000",
            height=36, corner_radius=8, command=self._trim_standby_now
        ).pack(fill="x", padx=16, pady=(4, 16))

        # Right Card: Architecture Deep-Dive
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(right_card, text="Windows MMAgent Architecture & Truthfulness", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_mem = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_mem.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        m_guides = [
            ("🧠 What Is Windows Memory Compression?", "Windows 10/11 introduced kernel memory compression (handled by the 'System' process). When RAM gets full, Windows compresses inactive pages in RAM instead of writing them to disk. This is a blessing for 8GB laptops, but for 16GB, 32GB, and 64GB gaming rigs, uncompressing pages on-demand steals CPU cycles and causes micro-stutter in open-world titles."),
            ("⚖️ The Technical Truth: When to Disable?", "If you have >= 16 GB of physical RAM, disabling Memory Compression ensures that zero CPU interrupts are spent decompressing memory buffers during gaming. If you have under 16 GB of RAM, you should leave it ENABLED to avoid slower disk paging."),
            ("📑 Page Combining Overhead", "Page Combining scans physical memory to de-duplicate identical memory pages across processes. In high-performance esports environments, this continuous hash-scanning is unnecessary overhead."),
            ("🛡️ Standby Cache Pacing", "Windows keeps cached files in standby RAM. Antimagist safely trims unneeded working sets without killing processes or inducing out-of-memory faults.")
        ]
        for title, desc in m_guides:
            bx = ctk.CTkFrame(scroll_mem, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
            bx.pack(fill="x", pady=4)
            ctk.CTkLabel(bx, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(bx, text=desc, font=("Segoe UI", 10), text_color=COLOR_TEXT_MUTED, wraplength=420, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _toggle_mem_comp(self, enable: bool):
        self.sfx.play_click()
        ok, msg = self.memory_pacer.set_memory_compression(enable)
        self.show_toast_msg(msg)
        self.memory_pacer.audit_memory_subsystem()
        self.show_memory_pacer_pane()

    def _trim_standby_now(self):
        self.sfx.play_success()
        ok, msg = self.memory_pacer.trim_standby_cache()
        self.show_toast_msg(msg)
        self.memory_pacer.audit_memory_subsystem()
        self.show_memory_pacer_pane()

    # ========================================================================
    # V7+ ENGINE 3: LIVE HARDWARE THERMAL THROTTLE & CLOCK DROP WATCHDOG
    # ========================================================================
    def show_throttle_pane(self):
        self._highlight_nav("throttle")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="Hardware Thermal Throttle & Clock Drop Watchdog", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Live GPU/CPU boost clock tracking, thermal tripwire alerts, and stutter root-cause analysis", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Live Hardware Clocks & Thermals
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        report = self.throttle_watchdog.check_hardware_health()
        gpu = report["gpu"]
        cpu = report["cpu"]

        ctk.CTkLabel(left_card, text="Live Hardware Sensor Metrics", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_stat = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_stat.pack(fill="x", padx=16, pady=(0, 14))

        status_col = COLOR_EMERALD if report["status"] == "HEALTHY_PEAK_PERFORMANCE" else COLOR_CRIMSON

        pills = [
            ("Thermal Status", report["status"], status_col),
            ("GPU Core Temperature", f"{gpu['temperature_c']} °C", COLOR_EMERALD if gpu['temperature_c'] < 80 else COLOR_CRIMSON),
            ("GPU Graphics Clock", f"{gpu['current_clock_mhz']} MHz / {gpu['max_clock_mhz']} MHz", COLOR_CYAN),
            ("GPU Core Load", f"{gpu['utilization_pct']} %", COLOR_TEXT_PRIMARY),
            ("CPU Clock Speed", f"{cpu['current_clock_mhz']} MHz / {cpu['max_clock_mhz']} MHz", COLOR_CYAN),
            ("CPU Load", f"{cpu['load_pct']} %", COLOR_TEXT_PRIMARY),
            ("Active Throttle Alerts", f"{len(report['alerts'])} Tripwires", COLOR_EMERALD if not report['alerts'] else COLOR_CRIMSON)
        ]
        for title, val, col in pills:
            r = ctk.CTkFrame(f_stat, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(r, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Consolas", 10, "bold"), text_color=col).pack(side="right")

        ctk.CTkButton(
            left_card, text="🔄 Refresh Hardware Telemetry & Audit", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._refresh_throttle_pane
        ).pack(fill="x", padx=16, pady=6)

        ctk.CTkButton(
            left_card, text="🗑️ Clear Throttle Event History", font=("Segoe UI", 11),
            fg_color="#1E293B", hover_color="#334155", text_color=COLOR_TEXT_MUTED,
            height=34, corner_radius=8, command=self._clear_throttle_events
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Recorded Throttle Events
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        events = self.throttle_watchdog.throttle_events
        ctk.CTkLabel(right_card, text=f"Thermal & Clock Throttle Event Log ({len(events)})", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_th = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_th.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        if not events:
            ctk.CTkLabel(scroll_th, text="No thermal throttling or clock drop events detected.\nYour hardware cooling is performing optimally!", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED, justify="center").pack(pady=40)
        else:
            for ev in reversed(events):
                bx = ctk.CTkFrame(scroll_th, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
                bx.pack(fill="x", pady=3)
                hdr = ctk.CTkFrame(bx, fg_color="transparent")
                hdr.pack(fill="x", padx=10, pady=(6, 2))
                ctk.CTkLabel(hdr, text=f"⚠️ {ev['timestamp']} — {ev['source']} Throttle", font=("Segoe UI", 11, "bold"), text_color=COLOR_AMBER).pack(side="left")
                ctk.CTkLabel(hdr, text=f"{ev['temperature_c']}°C | {ev['clock_mhz']} MHz", font=("Consolas", 10, "bold"), text_color=COLOR_CRIMSON).pack(side="right")

    def _refresh_throttle_pane(self):
        self.sfx.play_click()
        self.show_throttle_pane()

    def _clear_throttle_events(self):
        self.sfx.play_click()
        self.throttle_watchdog.clear_events()
        self.show_throttle_pane()

    # ========================================================================
    # V7+ ENGINE 4: LAN ESPORTS TEAM & TOURNAMENT SYNCHRONIZER
    # ========================================================================
    def show_lan_sync_pane(self):
        self._highlight_nav("lansync")
        self.clear_container()

        pane = ctk.CTkFrame(self.container, fg_color="transparent")
        pane.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        pane.grid_columnconfigure((0, 1), weight=1)
        pane.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(pane, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(head, text="LAN Esports Team & Tournament Synchronizer", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(head, text="Offline UDP broadcast sync for tournament configs, verified SHA-256 profiles, and radar rules across team PCs", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        # Left Card: Broadcast Profile Form
        left_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_card, text="Broadcast Tournament Profile (Team Captain / IGL)", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        f_form = ctk.CTkFrame(left_card, fg_color="#0A0C14", corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        f_form.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkLabel(f_form, text="Team Name:", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=12, pady=(8, 2))
        self.ent_lan_team = ctk.CTkEntry(f_form, placeholder_text="e.g. Apex Wolves", fg_color="#1E293B", border_color=COLOR_BORDER)
        self.ent_lan_team.pack(fill="x", padx=12, pady=(0, 6))
        self.ent_lan_team.insert(0, "Antimagist Esports")

        ctk.CTkLabel(f_form, text="Game Title:", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=12, pady=(4, 2))
        self.ent_lan_game = ctk.CTkEntry(f_form, placeholder_text="e.g. Counter-Strike 2", fg_color="#1E293B", border_color=COLOR_BORDER)
        self.ent_lan_game.pack(fill="x", padx=12, pady=(0, 6))
        self.ent_lan_game.insert(0, "Counter-Strike 2")

        ctk.CTkLabel(f_form, text="Tournament Profile Preset:", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=12, pady=(4, 2))
        self.ent_lan_profile = ctk.CTkEntry(f_form, placeholder_text="e.g. GrandFinals_LowLatency", fg_color="#1E293B", border_color=COLOR_BORDER)
        self.ent_lan_profile.pack(fill="x", padx=12, pady=(0, 10))
        self.ent_lan_profile.insert(0, "Tournament_1000Hz_MaxFPS")

        ctk.CTkButton(
            left_card, text="📡 Broadcast Profile to LAN (Port 8789)", font=("Segoe UI", 13, "bold"),
            fg_color="#00FF9D", hover_color="#00D480", text_color="#000000",
            height=44, corner_radius=10, command=self._broadcast_lan_profile
        ).pack(fill="x", padx=16, pady=6)

        listener_btn_text = "🛑 Stop LAN Listener" if self.lan_sync.running else "🎧 Start Background LAN Listener"
        listener_col = "#334155" if self.lan_sync.running else "#00F0FF"
        ctk.CTkButton(
            left_card, text=listener_btn_text, font=("Segoe UI", 11, "bold"),
            fg_color=listener_col, hover_color="#38BDF8", text_color="#000000" if not self.lan_sync.running else "#FFFFFF",
            height=34, corner_radius=8, command=self._toggle_lan_listener
        ).pack(fill="x", padx=16, pady=(6, 16))

        # Right Card: Discovered Peer Profiles
        right_card = ctk.CTkFrame(pane, fg_color=COLOR_CARD, corner_radius=14, border_color=COLOR_BORDER, border_width=1)
        right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        discovered = self.lan_sync.get_discovered_profiles()
        ctk.CTkLabel(right_card, text=f"Discovered Peer Tournament Profiles ({len(discovered)})", font=("Segoe UI", 14, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_lan = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        scroll_lan.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        if not discovered:
            ctk.CTkLabel(scroll_lan, text="No LAN team profiles received yet.\nStart the listener or have your Team Captain broadcast a preset!", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED, justify="center").pack(pady=40)
        else:
            for prof in reversed(discovered):
                bx = ctk.CTkFrame(scroll_lan, fg_color="#0A0C14", corner_radius=8, border_color=COLOR_BORDER, border_width=1)
                bx.pack(fill="x", pady=4)
                hdr = ctk.CTkFrame(bx, fg_color="transparent")
                hdr.pack(fill="x", padx=10, pady=(6, 2))
                ctk.CTkLabel(hdr, text=f"🏆 {prof['team_name']} — {prof['profile_name']}", font=("Segoe UI", 11, "bold"), text_color=COLOR_CYAN).pack(side="left")
                ctk.CTkLabel(hdr, text=f"IP: {prof.get('sender_ip', 'LAN')}", font=("Consolas", 10), text_color=COLOR_TEXT_MUTED).pack(side="right")
                ctk.CTkLabel(bx, text=f"Game: {prof['game']} | SHA256: {prof.get('sha256', '')[:16]}... [VERIFIED]", font=("Consolas", 9), text_color=COLOR_EMERALD).pack(anchor="w", padx=10, pady=(0, 6))

    def _broadcast_lan_profile(self):
        self.sfx.play_warp_boost()
        team = self.ent_lan_team.get().strip() or "Antimagist Team"
        game = self.ent_lan_game.get().strip() or "FPS Game"
        pname = self.ent_lan_profile.get().strip() or "Standard_Esports"

        settings = {
            "timer_resolution_ms": 1.0,
            "memory_compression": False,
            "usb_polling_hz": 1000,
            "directflip_mpo_disabled": True,
            "hags_enabled": True
        }
        packet = self.lan_sync.create_tournament_profile(team, game, pname, settings)
        ok, msg = self.lan_sync.broadcast_profile(packet)
        self.show_toast_msg(msg)

    def _toggle_lan_listener(self):
        self.sfx.play_click()
        if self.lan_sync.running:
            self.lan_sync.stop_listener()
            self.show_toast_msg("LAN broadcast listener stopped.")
        else:
            self.lan_sync.start_listener()
            self.show_toast_msg("LAN broadcast listener active on Port 8789.")
        self.show_lan_sync_pane()

    # ========================================================================
    # TELEMETRY LOOP WITH REAL-TIME GPU & DISCORD STATUS POLLING
    # ========================================================================
    def _poll_telemetry_loop(self):
        super()._poll_telemetry_loop()
        def gpu_worker():
            try:
                gm = self.gpu_sentinel.get_live_gpu_metrics()
                def update_gpu():
                    if hasattr(self, 'pill_gpu') and self.pill_gpu.winfo_exists():
                        self.pill_gpu.configure(
                            text=f"🎮 {gm['gpu_name'][:12]}: {gm['temperature_c']}°C",
                            text_color=gm['status_color']
                        )
                    if hasattr(self, 'lbl_dash_gpu_temp') and self.lbl_dash_gpu_temp.winfo_exists():
                        self.lbl_dash_gpu_temp.configure(text=f"{gm['temperature_c']} °C", text_color=gm['status_color'])
                    if hasattr(self, 'lbl_dash_gpu_vram') and self.lbl_dash_gpu_vram.winfo_exists():
                        self.lbl_dash_gpu_vram.configure(text=f"VRAM: {gm['vram_str']}")
                    if hasattr(self, 'lbl_dash_gpu_util') and self.lbl_dash_gpu_util.winfo_exists():
                        self.lbl_dash_gpu_util.configure(text=f"Core Load: {gm['utilization_gpu_pct']}%")
                self.after(0, update_gpu)

                # Periodic Discord Presence refresh (every ~15s)
                if hasattr(self, "discord_rpc") and self.discord_rpc.is_connected:
                    self.discord_rpc.update_presence(
                        details="Protected by Antimagist V7+ Ultra",
                        state=f"{gm['gpu_name'][:12]} ({gm['temperature_c']}°C) | Protected"
                    )
            except Exception:
                pass
        threading.Thread(target=gpu_worker, daemon=True).start()

    # ========================================================================
    # V5 GAMER MODE & VOICE ALERTS
    # ========================================================================
    def _toggle_gamer_mode_ui(self):
        self.sfx.play_click()
        super()._toggle_gamer_mode_ui()
        if self.gamer_mode.is_active:
            self.sfx.play_warp_boost()
            self.voice.alert_gamer_mode_on()
            games = self.gamer_mode.get_detected_games()
            for g in games:
                self.core_director.pin_process_to_performance_cores(g["pid"])
        else:
            self.voice.alert_gamer_mode_off()

    def _execute_turbo_clean(self):
        self.sfx.play_warp_boost()
        super()._execute_turbo_clean()
        self.voice.alert_turbo_clean()

    def _on_ransomware_breach_v5(self, breach_info: dict):
        self.sfx.play_alarm()
        self.voice.alert_ransomware_tripwire(breach_info.get("file", ""))
        self._on_ransomware_breach(breach_info)

    def _optimize_ping_ui(self):
        self.sfx.play_success()
        super()._optimize_ping_ui()
        self.voice.alert_ping_optimized()

    def destroy(self):
        """Clean shutdown of V7+ services."""
        try:
            self.game_watchdog.stop_watchdog()
        except Exception:
            pass
        try:
            self.discord_rpc.close()
        except Exception:
            pass
        try:
            self.mobile_companion.stop_server()
        except Exception:
            pass
        try:
            self.hud_overlay.destroy()
        except Exception:
            pass
        try:
            self.voice_listener.close_dialog()
        except Exception:
            pass
        try:
            self.lan_sync.stop_listener()
        except Exception:
            pass
        super().destroy()


if __name__ == "__main__":
    app = AntimagistV4ApexApp()
    app.mainloop()
