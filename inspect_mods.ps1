$modsPath = "$env:USERPROFILE\Documents\Teardown\mods"
$folders = Get-ChildItem -Path $modsPath -Directory

foreach ($f in $folders) {
    Write-Host "=========================================="
    Write-Host "MOD FOLDER: "$f.Name
    Get-ChildItem -Path $f.FullName | Select-Object Name
}
