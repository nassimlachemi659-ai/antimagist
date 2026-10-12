$drive = Get-PSDrive C
$used = [math]::round($drive.Used / 1GB, 2)
$free = [math]::round($drive.Free / 1GB, 2)
$total = [math]::round(($drive.Used + $drive.Free) / 1GB, 2)

Write-Host "=========================================="
Write-Host "C: Drive Total: $total GB | Used: $used GB | Free: $free GB"
Write-Host "=========================================="

# Check top folders in C:\
$rootFolders = Get-ChildItem C:\ -Directory -ErrorAction SilentlyContinue
foreach ($f in $rootFolders) {
    try {
        $size = (Get-ChildItem $f.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeGB = [math]::round($size / 1GB, 2)
        Write-Host "Folder: $($f.Name) -> $sizeGB GB"
    } catch {}
}

# Check user profile
Write-Host "--- User Profile Subfolders ($env:USERPROFILE) ---"
$userFolders = Get-ChildItem $env:USERPROFILE -Directory -ErrorAction SilentlyContinue
foreach ($f in $userFolders) {
    try {
        $size = (Get-ChildItem $f.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeGB = [math]::round($size / 1GB, 2)
        Write-Host "User Subfolder: $($f.Name) -> $sizeGB GB"
    } catch {}
}

# Check Temp sizes
$temp1 = (Get-ChildItem $env:TEMP -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$temp2 = (Get-ChildItem "C:\Windows\Temp" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
Write-Host "User Temp: $([math]::round($temp1/1MB, 2)) MB | Windows Temp: $([math]::round($temp2/1MB, 2)) MB"
