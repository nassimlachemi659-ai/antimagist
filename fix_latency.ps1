# ============================================================
# fix_latency.ps1 - Network Latency & Ping Optimizer
# Run this as Administrator for full effect!
# Right-click -> "Run with PowerShell" -> Accept UAC prompt
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Network Latency Fix Script" -ForegroundColor Cyan
Write-Host "  Run as ADMINISTRATOR for full effect!" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# --- 1. TCP Min RTO (Retransmit Timeout) - Gaming critical ---
Write-Host "[1/6] Setting TCP Min RTO to 100ms (was 300ms)..." -ForegroundColor Green
netsh int tcp set supplemental template=internet MinRto=100
Write-Host "      Lower RTO = faster packet recovery during gaming`n"

# --- 2. Enable ECN (Explicit Congestion Notification) ---
Write-Host "[2/6] Enabling ECN (Explicit Congestion Notification)..." -ForegroundColor Green
netsh int tcp set global ecncapability=enabled
Write-Host "      ECN lets routers signal congestion without dropping packets`n"

# --- 3. Disable Nagle's Algorithm ---
Write-Host "[3/6] Disabling Nagle's Algorithm..." -ForegroundColor Green
$path = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
$adapters = Get-ChildItem $path
$fixed = 0
foreach ($adapter in $adapters) {
    $ip = Get-ItemProperty -Path $adapter.PSPath -Name "DhcpIPAddress" -ErrorAction SilentlyContinue
    if ($ip -and $ip.DhcpIPAddress -and $ip.DhcpIPAddress -ne "0.0.0.0") {
        Set-ItemProperty -Path $adapter.PSPath -Name "TcpAckFrequency" -Value 1 -Type DWord -Force
        Set-ItemProperty -Path $adapter.PSPath -Name "TCPNoDelay"      -Value 1 -Type DWord -Force
        Write-Host "      Fixed adapter: $($ip.DhcpIPAddress)" -ForegroundColor Gray
        $fixed++
    }
}
if ($fixed -eq 0) { Write-Host "      No DHCP adapters found, skipping." -ForegroundColor Yellow }
Write-Host "      Nagle buffers small packets = more latency in games`n"

# --- 4. Disable Delivery Optimization P2P sharing (upload bandwidth hog) ---
Write-Host "[4/6] Disabling Windows Delivery Optimization P2P sharing..." -ForegroundColor Green
$doPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization"
if (!(Test-Path $doPath)) { New-Item -Path $doPath -Force | Out-Null }
Set-ItemProperty -Path $doPath -Name "DODownloadMode" -Value 0 -Type DWord -Force
Write-Host "      This stops Windows from using YOUR connection to seed updates to others`n"

# --- 5. Disable Auto-Tuning (optional, set to restricted for gaming) ---
Write-Host "[5/6] Setting TCP Receive Window Auto-Tuning to 'highlyrestricted'..." -ForegroundColor Green
netsh int tcp set global autotuninglevel=highlyrestricted
Write-Host "      Reduces buffer bloat which causes high ping variance (jitter)`n"

# NOTE: Switch back to 'normal' if download speeds drop:
# netsh int tcp set global autotuninglevel=normal

# --- 6. Flush DNS Cache ---
Write-Host "[6/6] Flushing DNS cache..." -ForegroundColor Green
ipconfig /flushdns | Out-Null
Write-Host "      Clears stale DNS entries that can slow connection setup`n"

# --- Verify Changes ---
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verification - Current TCP Settings:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
netsh int tcp show global
Write-Host ""
netsh int tcp show supplemental

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  All optimizations applied!" -ForegroundColor Green
Write-Host "  Restart your PC for Nagle changes to take full effect." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# --- Run a quick ping test to verify improvement ---
Write-Host "`n=== Quick Ping Test ===" -ForegroundColor Cyan
Write-Host "Cloudflare (1.1.1.1):"
Test-Connection -ComputerName 1.1.1.1 -Count 4 | Select-Object ResponseTime | Format-Table -AutoSize
Write-Host "Google (8.8.8.8):"
Test-Connection -ComputerName 8.8.8.8 -Count 4 | Select-Object ResponseTime | Format-Table -AutoSize

Read-Host "`nPress Enter to exit"
