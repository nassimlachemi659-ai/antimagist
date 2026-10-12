$ExePath = "$env:LOCALAPPDATA\OS-Core\Antimagist.exe"
$SourceExe = "$PSScriptRoot\dist\Antimagist.exe"

If (!(Test-Path "$env:LOCALAPPDATA\OS-Core")) {
    New-Item -ItemType Directory -Force -Path "$env:LOCALAPPDATA\OS-Core"
}

Copy-Item -Path $SourceExe -Destination $ExePath -Force

$Action = New-ScheduledTaskAction -Execute $ExePath -Argument "--daemon"
$Trigger = New-ScheduledTaskTrigger -AtLogon
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Days 9999)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -TaskName "OS-Core-Agent" -Description "Runs OS-Core AI Agent in the background" -Force
Write-Host "OS-Core Agent successfully registered as a background daemon!"
