# Starts the Ollama server with models stored on D:.
# The Ollama tray app ignores OLLAMA_MODELS and downloads to C:, so we stop it
# and run the server directly instead.

$ErrorActionPreference = "Stop"
$ollamaExe = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
$modelsDir = "D:\ollama\models"

Get-Process | Where-Object { $_.ProcessName -like "ollama*" } | Stop-Process -Force -Confirm:$false
Start-Sleep -Seconds 2

New-Item -ItemType Directory -Force $modelsDir | Out-Null
$env:OLLAMA_MODELS = $modelsDir
Start-Process -FilePath $ollamaExe -ArgumentList "serve" -WindowStyle Hidden

for ($i = 0; $i -lt 30; $i++) {
    try {
        $v = (Invoke-RestMethod "http://127.0.0.1:11434/api/version").version
        Write-Output "Ollama $v running. Models folder: $modelsDir"
        exit 0
    } catch {
        Start-Sleep -Seconds 1
    }
}
Write-Output "Ollama did not start within 30 seconds."
exit 1
