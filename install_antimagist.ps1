# Antimagist V7+ Ultra - Windows 1-Click Installer
$ErrorActionPreference = "Stop"
$appData = [System.Environment]::GetFolderPath("LocalApplicationData")
$targetDir = Join-Path $appData "Antimagist"
$srcDir = Join-Path $PSScriptRoot "dist\Antimagist_V4_Apex"
$desktop = [System.Environment]::GetFolderPath("Desktop")
$programs = [System.Environment]::GetFolderPath("Programs")

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "          ANTIMAGIST V7+ ULTRA - SETUP WIZARD" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Create Target Directory
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# Terminate existing instance if running
Get-Process -Name "Antimagist_V4_Apex" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 600

# 2. Copy Binaries
Write-Host "[*] Installing application files to $targetDir..." -ForegroundColor Yellow
Copy-Item -Path (Join-Path $srcDir "*") -Destination $targetDir -Recurse -Force

# 3. Create Desktop Shortcut
$wsh = New-Object -ComObject WScript.Shell
$scPath = Join-Path $desktop "Antimagist V7+ Ultra.lnk"
$sc = $wsh.CreateShortcut($scPath)
$sc.TargetPath = Join-Path $targetDir "Antimagist_V4_Apex.exe"
$sc.WorkingDirectory = $targetDir
$sc.Description = "Antimagist Enterprise Security V7+ Ultra Edition"
$sc.IconLocation = Join-Path $targetDir "antimagist.ico"
$sc.Save()

# 4. Create Start Menu Shortcut
$smPath = Join-Path $programs "Antimagist V7+ Ultra.lnk"
$sm = $wsh.CreateShortcut($smPath)
$sm.TargetPath = Join-Path $targetDir "Antimagist_V4_Apex.exe"
$sm.WorkingDirectory = $targetDir
$sm.Description = "Antimagist Enterprise Security V7+ Ultra Edition"
$sm.IconLocation = Join-Path $targetDir "antimagist.ico"
$sm.Save()

Write-Host "[+] Installation Complete!" -ForegroundColor Green
Write-Host "[+] Desktop Shortcut created: $scPath" -ForegroundColor Cyan
Write-Host "[+] Start Menu Shortcut created: $smPath" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
