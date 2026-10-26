$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "Antimagist.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_Enterprise_Live\Antimagist_Enterprise_Live.exe"
$Shortcut.WorkingDirectory = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_Enterprise_Live"
$Shortcut.IconLocation = "C:\Users\nst\.gemini\antigravity\scratch\dist\Antimagist_Enterprise_Live\Antimagist_Enterprise_Live.exe,0"
$Shortcut.Description = "Antimagist Enterprise Gaming & Security Engine (V13 Closed-Loop Intelligence)"
$Shortcut.Save()

Write-Output "Clean desktop shortcut successfully created: $ShortcutPath"
