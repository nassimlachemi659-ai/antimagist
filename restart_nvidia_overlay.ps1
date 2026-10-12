Write-Host "Restarting NVIDIA Overlay capture services..."
Get-Process -Name "NVIDIA Overlay", "nvcontainer" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "NVIDIA Overlay services reset successfully!"
