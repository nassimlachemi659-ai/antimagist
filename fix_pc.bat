@echo off
:: Self-elevating batch file - will auto-request UAC admin prompt
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    PowerShell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

PowerShell -ExecutionPolicy Bypass -Command ^
"& { ^
$ErrorActionPreference = 'SilentlyContinue'; ^
Write-Host '========================================' -ForegroundColor Cyan; ^
Write-Host '  Fixing your PC network settings...' -ForegroundColor Cyan; ^
Write-Host '========================================'; ^
^
Write-Host '[1/6] TCP Min RTO 300ms -> 100ms...' -ForegroundColor Yellow; ^
netsh int tcp set supplemental template=internet MinRto=100 | Out-Null; ^
Write-Host '      Done.' -ForegroundColor Green; ^
^
Write-Host '[2/6] Enabling ECN...' -ForegroundColor Yellow; ^
netsh int tcp set global ecncapability=enabled | Out-Null; ^
Write-Host '      Done.' -ForegroundColor Green; ^
^
Write-Host '[3/6] Setting TCP auto-tuning to highlyrestricted (less jitter)...' -ForegroundColor Yellow; ^
netsh int tcp set global autotuninglevel=highlyrestricted | Out-Null; ^
Write-Host '      Done.' -ForegroundColor Green; ^
^
Write-Host '[4/6] Disabling Nagle algorithm (better for gaming)...' -ForegroundColor Yellow; ^
$ifacePath = ''HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces''; ^
Get-ChildItem $ifacePath | ForEach-Object { ^
    $ip = Get-ItemProperty -Path $_.PSPath -Name DhcpIPAddress -EA SilentlyContinue; ^
    if ($ip -and $ip.DhcpIPAddress -ne ''0.0.0.0'') { ^
        Set-ItemProperty -Path $_.PSPath -Name TcpAckFrequency -Value 1 -Type DWord -Force; ^
        Set-ItemProperty -Path $_.PSPath -Name TCPNoDelay -Value 1 -Type DWord -Force; ^
        Write-Host ('      Fixed: ' + $ip.DhcpIPAddress) -ForegroundColor Green; ^
    } ^
}; ^
^
Write-Host '[5/6] Disabling Delivery Optimization P2P (stop seeding Windows updates)...' -ForegroundColor Yellow; ^
$doPath = ''HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization''; ^
if (!(Test-Path $doPath)) { New-Item -Path $doPath -Force | Out-Null }; ^
Set-ItemProperty -Path $doPath -Name DODownloadMode -Value 0 -Type DWord -Force; ^
Write-Host '      Done.' -ForegroundColor Green; ^
^
Write-Host '[6/6] Flushing DNS cache...' -ForegroundColor Yellow; ^
ipconfig /flushdns | Out-Null; ^
Write-Host '      Done.' -ForegroundColor Green; ^
^
Write-Host ''; ^
Write-Host '========================================' -ForegroundColor Green; ^
Write-Host '  ALL FIXES APPLIED!' -ForegroundColor Green; ^
Write-Host '  Restart your PC to fully take effect.' -ForegroundColor Yellow; ^
Write-Host '========================================'; ^
Write-Host ''; ^
Write-Host 'Running ping test...' -ForegroundColor Cyan; ^
Test-Connection -ComputerName 1.1.1.1 -Count 4 | ForEach-Object { Write-Host ('  1.1.1.1  -> ' + $_.ResponseTime + 'ms') }; ^
Test-Connection -ComputerName 8.8.8.8 -Count 4 | ForEach-Object { Write-Host ('  8.8.8.8  -> ' + $_.ResponseTime + 'ms') }; ^
Write-Host ''; ^
pause ^
}"
