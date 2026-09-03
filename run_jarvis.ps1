$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

# Kích hoạt virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Qt platform plugins của PySide6
$qtPlatform = Join-Path $PSScriptRoot ".venv\Lib\site-packages\PySide6\plugins\platforms"

if (-not (Test-Path "$qtPlatform\qwindows.dll")) {
    Write-Host "ERROR: qwindows.dll not found:"
    Write-Host $qtPlatform
    exit 1
}

# Ép Qt dùng đúng Windows platform plugin
$env:QT_QPA_PLATFORM_PLUGIN_PATH = $qtPlatform

# Xóa Qt plugin path cũ nếu có
Remove-Item Env:QT_PLUGIN_PATH -ErrorAction SilentlyContinue

Write-Host "JARVIS Qt platform: $qtPlatform"
Write-Host "Starting JARVIS..."

python ".\main.py"