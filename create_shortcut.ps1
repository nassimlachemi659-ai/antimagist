$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "Antimagist.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_Enterprise\Antimagist_Enterprise.exe"
$Shortcut.WorkingDirectory = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_Enterprise"
$Shortcut.IconLocation = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_Enterprise\Antimagist_Enterprise.exe,0"
$Shortcut.Description = "Antimagist Enterprise Gaming & Security Engine"
$Shortcut.Save()

Write-Output "Clean desktop shortcut successfully created: $ShortcutPath"
