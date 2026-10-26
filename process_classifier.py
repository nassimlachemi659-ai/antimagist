"""
process_classifier.py — Antimagist 4-Tier Process Intelligence Classifier
=========================================================================
Strict Zero-Trust Classification Engine:
  - TIER 0 (PROTECTED OS & KERNEL):
      explorer.exe, dwm.exe, csrss.exe, svchost.exe, MsMpEng.exe, System,
      Registry, audiodg.exe, smss.exe, wininit.exe, services.exe, lsass.exe,
      sihost.exe, fontdrvhost.exe, taskhostw.exe, memory compression
      Rule: NEVER allow killing or suspending. Hide [Kill] button in UI.
  - TIER 1 (PROTECTED USER & HARDWARE DRIVERS):
      Drivers/Peripherals: NGENUITY.exe, lghub.exe, lghub_agent.exe, RazerCentralService.exe,
      Razer Synapse 3.exe, steelseriesgg.exe, corsair.service.exe, icue.exe.
      Active Apps/Tools: Discord.exe, Antigravity.exe, Code.exe, language_server*,
      python.exe, devenv.exe, rider64.exe, slack.exe, obs64.exe.
      Games & Anti-Cheats: cs2.exe, Fortnite*, EasyAntiCheat*, BEService.exe,
      vgc.exe, RiotClientServices.exe, VALORANT.exe.
      Rule: Allow safe [Trim RAM] (EmptyWorkingSet), but NEVER let "Suspend Bloat",
      "Turbo Boost", or background cleaners kill or freeze them! Hide [Kill] in UI.
  - TIER 2 (TRIM & THROTTLE TARGETS):
      Heavy background browsers and updaters:
      chrome.exe, msedge.exe, steamwebhelper.exe, EpicWebHelper.exe,
      brave.exe, firefox.exe, opera.exe, battle.net.exe, origin.exe.
      Rule: Safe [Trim RAM] and throttle CPU priority during game.
  - TIER 3 (TRUE BLOATWARE):
      Background telemetry, unused store apps:
      OneDrive.exe, SearchApp.exe, WidgetService.exe, CompatTelRunner.exe,
      GameBar.exe, GameBarFTServer.exe, Cortana.exe, YourPhone.exe, PhoneExperienceHost.exe,
      CrossDeviceService.exe, MSTeams.exe, msedgewebview2.exe.
      Rule: Prioritize for bloat hunting and background suspension.
"""

import fnmatch
from typing import Dict, Any, Tuple

# Tier 0: Critical OS & Kernel
TIER_0_PROCESSES = {
    "system", "system idle process", "registry", "smss.exe", "csrss.exe",
    "wininit.exe", "services.exe", "lsass.exe", "svchost.exe", "explorer.exe",
    "dwm.exe", "msmpeng.exe", "audiodg.exe", "sihost.exe", "fontdrvhost.exe",
    "taskhostw.exe", "memory compression", "securityhealthservice.exe",
    "spoolsv.exe", "conhost.exe"
}

# Tier 1 Drivers: Hardware & Peripherals
TIER_1_DRIVERS = {
    "ngenuity.exe", "lghub.exe", "lghub_agent.exe", "lghub_updater.exe",
    "razercentralservice.exe", "razer synapse 3.exe", "rzsynapse.exe",
    "steelseriesgg.exe", "steelseriesengine3.exe", "corsair.service.exe",
    "icue.exe", "rtkngui64.exe", "ravbg64.exe", "nvcontainer.exe",
    "nvidia web helper.exe", "amdrsserv.exe"
}

# Tier 1 Apps: User Tools & Anti-Cheats
TIER_1_APPS = {
    "discord.exe", "antigravity.exe", "code.exe", "python.exe", "pythonw.exe",
    "devenv.exe", "rider64.exe", "slack.exe", "obs64.exe", "steam.exe",
    "epicgameslauncher.exe", "cs2.exe", "beservice.exe", "vgc.exe",
    "riotclientservices.exe", "valorant.exe", "easyanticheat.exe",
    "easyanticheat_eos.exe"
}

TIER_1_PATTERNS = [
    "language_server*", "fortnite*", "easyanticheat*", "beservice*"
]

# Tier 2: Heavy Web Browsers & Updaters
TIER_2_BROWSERS_UPDATERS = {
    "chrome.exe", "msedge.exe", "steamwebhelper.exe", "epicwebhelper.exe",
    "brave.exe", "firefox.exe", "opera.exe", "operagx.exe", "battle.net.exe",
    "origin.exe", "ea.exe", "galaxyclient.exe"
}

# Tier 3: True Background Bloatware & Telemetry
TIER_3_BLOATWARE = {
    "onedrive.exe", "searchapp.exe", "widgetservice.exe", "compattelrunner.exe",
    "gamebar.exe", "gamebarftserver.exe", "cortana.exe", "yourphone.exe",
    "phoneexperiencehost.exe", "crossdeviceservice.exe", "msteams.exe",
    "msedgewebview2.exe", "skype.exe", "wermgr.exe", "devicecensus.exe"
}


class ProcessIntelligenceClassifier:
    """Classifies processes into 4 strict zero-trust safety tiers."""

    @staticmethod
    def classify(proc_name: str, pid: int = -1) -> Dict[str, Any]:
        p_lower = proc_name.lower().strip() if proc_name else ""

        # Low PIDs (0, 4) are strictly OS Kernel
        if (pid in (0, 4) and pid != -1) or p_lower in TIER_0_PROCESSES:
            return {
                "tier": 0,
                "badge": "OS",
                "badge_bg": "#3B1219",
                "badge_fg": "#F87171",  # Red
                "can_kill": False,
                "can_suspend": False,
                "can_trim": False if (pid in (0, 4) and pid != -1) or p_lower in ("system", "system idle process", "registry", "audiodg.exe") else True,
                "description": "Protected Windows OS Kernel / Critical Subsystem"
            }

        # Check Tier 1 Drivers
        if p_lower in TIER_1_DRIVERS:
            return {
                "tier": 1,
                "badge": "DRIVER",
                "badge_bg": "#2E1065",
                "badge_fg": "#C084FC",  # Purple
                "can_kill": False,
                "can_suspend": False,
                "can_trim": True,
                "description": "Protected Hardware Peripheral Driver"
            }

        # Check Tier 1 Apps & Games
        if p_lower in TIER_1_APPS or any(fnmatch.fnmatch(p_lower, pat) for pat in TIER_1_PATTERNS):
            return {
                "tier": 1,
                "badge": "APP",
                "badge_bg": "#083344",
                "badge_fg": "#38BDF8",  # Cyan
                "can_kill": False,
                "can_suspend": False,
                "can_trim": True,
                "description": "Protected User Application / Voice / Game"
            }

        # Check Tier 3 Bloatware
        if p_lower in TIER_3_BLOATWARE:
            return {
                "tier": 3,
                "badge": "BLOAT",
                "badge_bg": "#451A03",
                "badge_fg": "#FBBF24",  # Amber
                "can_kill": True,
                "can_suspend": True,
                "can_trim": True,
                "description": "Identified Background Bloatware / Telemetry"
            }

        # Check Tier 2 Browsers & Updaters
        if p_lower in TIER_2_BROWSERS_UPDATERS:
            return {
                "tier": 2,
                "badge": "APP",
                "badge_bg": "#1E293B",
                "badge_fg": "#94A3B8",  # Slate
                "can_kill": True,
                "can_suspend": True,
                "can_trim": True,
                "description": "Background Browser / Helper Subprocess"
            }

        # Default fallback for unlisted user applications
        return {
            "tier": 2,
            "badge": "APP",
            "badge_bg": "#132338",
            "badge_fg": "#60A5FA",  # Light Blue
            "can_kill": True,
            "can_suspend": False,
            "can_trim": True,
            "description": "Active User Process"
        }

    @classmethod
    def is_kill_allowed(cls, proc_name: str, pid: int = -1) -> bool:
        return cls.classify(proc_name, pid)["can_kill"]

    @classmethod
    def is_suspend_allowed(cls, proc_name: str, pid: int = -1) -> bool:
        return cls.classify(proc_name, pid)["can_suspend"]

    @classmethod
    def is_trim_allowed(cls, proc_name: str, pid: int = -1) -> bool:
        return cls.classify(proc_name, pid)["can_trim"]
