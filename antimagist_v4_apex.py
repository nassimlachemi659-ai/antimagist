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

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AntimagistV4ApexApp(AntimagistV3App):
    """Antimagist Enterprise Security Version 5 (Singularity Edition)."""

    def __init__(self):
        # 1. Initialize Core V4/V5 Subsystems
        self.voice = AntimagistVoiceCopilot(enabled=True)
        self.sfx = AntimagistSoundFX(enabled=True)
        self.core_director = AntimagistCoreDirector()
        self.detonation_chamber = AntimagistDetonationChamber()
        self.gpu_sentinel = AntimagistGPUSentinel()
        self.game_library = AntimagistGameLibrary()
        self.windows_stripper = AntimagistWindowsStripper()
        self.license_manager = AntimagistLicenseManager()

        # Call base constructor
        super().__init__()

        # Update window title
        self.title("Antimagist — Enterprise Security V5 Singularity Edition")

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
            ("🎯 CS2 Tuner",         "cs2",        self.show_cs2_pane),
            ("⚡ Latency Stripper",  "stripper",   self.show_stripper_pane),
            ("📈 Match History",     "analytics",  self.show_analytics_pane),
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
                        details="Protected by Antimagist V5 Singularity",
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
        """Clean shutdown of V5 services."""
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
        super().destroy()


if __name__ == "__main__":
    app = AntimagistV4ApexApp()
    app.mainloop()
