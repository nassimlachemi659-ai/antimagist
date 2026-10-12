$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "Antimagist Enterprise V3.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_V3_Ultra\Antimagist_V3_Ultra.exe"
$Shortcut.WorkingDirectory = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_V3_Ultra"
$Shortcut.IconLocation = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_V3_Ultra\antimagist.ico,0"
$Shortcut.Description = "Antimagist Enterprise Security V3 Ultra-Modern Edition"
$Shortcut.Save()
Write-Output "Shortcut successfully created at: $ShortcutPath"
