rule Suspicious_Scripting {
    meta:
        description = "Detects files trying to execute hidden shell commands"
        author = "Super Strong Antimalware"
        threat_level = "High"
    strings:
        $cmd = "cmd.exe /c" ascii wide nocase
        $ps = "powershell -enc" ascii wide nocase
        $wscript = "WScript.Shell" ascii wide nocase
    condition:
        any of them
}

rule EICAR_YARA_Test {
    meta:
        description = "Detects the standard EICAR test string anywhere in a file"
        author = "Super Strong Antimalware"
        threat_level = "Test"
    strings:
        $eicar = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    condition:
        $eicar
}

rule Suspicious_Web_Downloader {
    meta:
        description = "Detects scripts trying to quietly download files from the internet"
        threat_level = "Medium"
    strings:
        $http = "http://" ascii wide nocase
        $https = "https://" ascii wide nocase
        $download = "Net.WebClient).DownloadFile" ascii wide nocase
    condition:
        ($http or $https) and $download
}
