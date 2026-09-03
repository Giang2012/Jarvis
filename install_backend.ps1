$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "J.A.R.V.I.S backend installer"
Write-Host "Project: $ProjectRoot"

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backup = Join-Path $ProjectRoot ".jarvis_backup_backend_$stamp"
New-Item -ItemType Directory -Path $backup -Force | Out-Null

$files = @(
    "core\brain.py",
    "ai\reasoner.py",
    "ai\planner.py",
    "config\settings.py",
    "services\desktop_service.py",
    "services\screen_service.py",
    "services\screen_observer.py",
    "services\file_service.py",
    "services\media_service.py",
    "services\clipboard_service.py",
    "services\system_service.py",
    "skills\desktop.py",
    "skills\vision.py",
    "skills\files.py",
    "skills\media.py",
    "skills\clipboard.py"
)

foreach ($rel in $files) {
    $src = Join-Path $ProjectRoot $rel
    if (Test-Path $src) {
        $dest = Join-Path $backup $rel
        New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
        Copy-Item $src $dest -Force
    }
}

# The patch lives under .\patch\. Copy its tree over the project.
$patchRoot = Join-Path $ProjectRoot "patch"
if (-not (Test-Path $patchRoot)) {
    throw "Missing .\patch directory. Extract the ZIP first, keeping the patch folder."
}

foreach ($rel in $files) {
    $src = Join-Path $patchRoot $rel
    $dest = Join-Path $ProjectRoot $rel
    if (Test-Path $src) {
        New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
        Copy-Item $src $dest -Force
    }
}

# Append dependencies only if absent.
$req = Join-Path $ProjectRoot "requirements.txt"
if (Test-Path $req) {
    $content = Get-Content $req -Raw
    foreach ($dep in @("psutil", "pytesseract")) {
        if ($content -notmatch "(?im)^\s*$dep([<>=!~].*)?$") {
            Add-Content $req $dep
        }
    }
}

Write-Host ""
Write-Host "Backend installed."
Write-Host "Backup: $backup"
Write-Host ""
Write-Host "Next:"
Write-Host "  .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
Write-Host "  .\.venv\Scripts\python.exe -m compileall core ai services skills config"
Write-Host "  .\.venv\Scripts\python.exe smoke_test_backend.py"
