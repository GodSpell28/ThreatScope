rule ThreatScopeMalware {
    meta:
        description = "Generic malware detection heuristic"
        author = "ThreatScope"
        date = "2026-06-27"
        reference = "https://github.com/GodSpell28/ThreatScope"
    strings:
        $mz = { 4D 5A }
        $url1 = "http://" nocase wide ascii
        $url2 = "https://" nocase wide ascii
        $reg1 = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run" nocase
    condition:
        $mz at 0 and (1 of ($url*)) and $reg1
}
