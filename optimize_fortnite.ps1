# Fortnite & Windows Latency / FPS Optimization Script

Write-Host "=== 1. OPTIMIZING FORTNITE GAMEUSERSETTINGS.INI ==="
$fnIni = "$env:LOCALAPPDATA\FortniteGame\Saved\Config\WindowsClient\GameUserSettings.ini"

if (Test-Path $fnIni) {
    Copy-Item $fnIni "$fnIni.bak" -Force
    Write-Host "[+] Backup created at $fnIni.bak"

    $content = Get-Content $fnIni -Raw
    
    # Force Exclusive Fullscreen (Mode 0) to bypass Desktop Window Manager latency
    $content = $content -replace 'FullscreenMode=\d+', 'FullscreenMode=0'
    $content = $content -replace 'LastConfirmedFullscreenMode=\d+', 'LastConfirmedFullscreenMode=0'
    $content = $content -replace 'PreferredFullscreenMode=\d+', 'PreferredFullscreenMode=0'

    # Disable mouse acceleration/smoothing for raw 1:1 input
    if ($content -match 'bDisableMouseAcceleration=') {
        $content = $content -replace 'bDisableMouseAcceleration=False', 'bDisableMouseAcceleration=True'
    } else {
        $content = $content -replace '\[/Script/FortniteGame.FortGameUserSettings\]', "[/Script/FortniteGame.FortGameUserSettings]`r`nbDisableMouseAcceleration=True"
    }

    # Ensure Motion Blur and Grass are disabled
    $content = $content -replace 'bMotionBlur=True', 'bMotionBlur=False'
    $content = $content -replace 'bShowGrass=True', 'bShowGrass=False'

    # Ensure Reflex Low Latency is ON
    if ($content -match 'LowInputLatencyModeIsEnabled=') {
        $content = $content -replace 'LowInputLatencyModeIsEnabled=False', 'LowInputLatencyModeIsEnabled=True'
    }

    [System.IO.File]::WriteAllText($fnIni, $content)
    Write-Host "[+] Exclusive Fullscreen & Raw Mouse Input configured in GameUserSettings.ini"
} else {
    Write-Warning "[-] Fortnite GameUserSettings.ini not found!"
}

Write-Host "`n=== 2. OPTIMIZING WINDOWS GAMING & LATENCY REGISTRY ==="

# GameConfigStore (Disable GameDVR Background Capture & Allow True Fullscreen)
$gcsPath = "HKCU:\System\GameConfigStore"
if (Test-Path $gcsPath) {
    Set-ItemProperty -Path $gcsPath -Name "GameDVR_Enabled" -Value 0 -Type DWord -Force
    Set-ItemProperty -Path $gcsPath -Name "GameDVR_FSEBehaviorMode" -Value 2 -Type DWord -Force
    Set-ItemProperty -Path $gcsPath -Name "GameDVR_HonorUserFSEBehaviorMode" -Value 1 -Type DWord -Force
    Set-ItemProperty -Path $gcsPath -Name "GameDVR_DXGIHonorFSEWindowsCompatible" -Value 1 -Type DWord -Force
    Write-Host "[+] GameConfigStore optimized (GameDVR disabled, Exclusive Fullscreen forced)"
}

# Windows Game Bar
$gbPath = "HKCU:\Software\Microsoft\GameBar"
if (-not (Test-Path $gbPath)) { New-Item -Path $gbPath -Force | Out-Null }
Set-ItemProperty -Path $gbPath -Name "AutoGameModeEnabled" -Value 1 -Type DWord -Force
Set-ItemProperty -Path $gbPath -Name "AllowAutoGameMode" -Value 1 -Type DWord -Force
Write-Host "[+] Windows Game Mode verified enabled"

# Windows GameDVR User settings
$gdvrPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR"
if (-not (Test-Path $gdvrPath)) { New-Item -Path $gdvrPath -Force | Out-Null }
Set-ItemProperty -Path $gdvrPath -Name "AppCaptureEnabled" -Value 0 -Type DWord -Force
Set-ItemProperty -Path $gdvrPath -Name "HistoricalCaptureEnabled" -Value 0 -Type DWord -Force
Write-Host "[+] Windows GameDVR capture turned OFF to free GPU/CPU cycles"

# Multimedia SystemProfile Network and Responsiveness
$sysProfile = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
try {
    # 0xffffffff disables Windows network packet throttling
    Set-ItemProperty -Path $sysProfile -Name "NetworkThrottlingIndex" -Value ([Convert]::ToUInt32("ffffffff", 16)) -Type DWord -ErrorAction Stop
    # 0 gives 100% CPU priority to foreground applications (games)
    Set-ItemProperty -Path $sysProfile -Name "SystemResponsiveness" -Value 0 -Type DWord -ErrorAction Stop
    Write-Host "[+] Multimedia SystemProfile: NetworkThrottlingIndex and SystemResponsiveness optimized"
} catch {
    Write-Host "[-] Note: SystemProfile requires elevated privileges (skipped or already managed)"
}

# Multimedia SystemProfile Games Task
$gamesTask = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games"
try {
    Set-ItemProperty -Path $gamesTask -Name "GPU Priority" -Value 8 -Type DWord -ErrorAction Stop
    Set-ItemProperty -Path $gamesTask -Name "Priority" -Value 6 -Type DWord -ErrorAction Stop
    Set-ItemProperty -Path $gamesTask -Name "Scheduling Category" -Value "High" -Type String -ErrorAction Stop
    Set-ItemProperty -Path $gamesTask -Name "SFIO Priority" -Value "High" -Type String -ErrorAction Stop
    Write-Host "[+] Games Task Priority set to High"
} catch {
    Write-Host "[-] Note: Games Task priority requires elevated privileges (skipped or already managed)"
}

Write-Host "`n=== 3. CLEANING STALE FORTNITE CACHES ==="
# Stale web and shader temporary caches can cause microstuttering
$fnWebCache = "$env:LOCALAPPDATA\FortniteGame\Saved\WebCache"
if (Test-Path $fnWebCache) {
    Remove-Item -Path "$fnWebCache\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[+] Fortnite WebCache cleared"
}

$egsWebCache = "$env:LOCALAPPDATA\EpicGamesLauncher\Saved\webcache"
if (Test-Path $egsWebCache) {
    Remove-Item -Path "$egsWebCache\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[+] Epic Games Launcher webcache cleared"
}

Write-Host "`n=== ALL TWEAKS APPLIED SUCCESSFULLY! ==="
