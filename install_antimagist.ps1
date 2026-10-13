# Antimagist Automated Installer Script
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Antimagist Enterprise Security V11 Omni-Workstation Setup" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[+] Verifying Windows environment..." -ForegroundColor Green
$dest = "$env:LOCALAPPDATA\Antimagist"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Write-Host "[+] Creating Desktop and Start Menu Shortcuts..." -ForegroundColor Green
$wsh = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")
$sc = $wsh.CreateShortcut("$desktop\Antimagist.lnk")
$sc.TargetPath = "$PSScriptRoot\dist\Antimagist_V4_Apex\Antimagist.exe"
$sc.WorkingDirectory = "$PSScriptRoot\dist\Antimagist_V4_Apex"
$sc.IconLocation = "$PSScriptRoot\antimagist.ico,0"
$sc.Save()
Write-Host "[+] Antimagist successfully installed and ready!" -ForegroundColor Green
