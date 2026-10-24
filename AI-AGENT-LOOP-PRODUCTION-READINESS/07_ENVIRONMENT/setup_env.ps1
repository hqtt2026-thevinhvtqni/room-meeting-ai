# Work 102 — authorized execution environment setup
# Creates .venv-work102 with pinned tool versions. Runner tooling only; no source changes.
param(
  [string]$Workspace = (Get-Location).Path
)
$ErrorActionPreference = 'Stop'
$py = Get-Command python -ErrorAction Stop
& $py --version
if (-not (& $py --version) -match '3\.12') { Write-Warning 'Python 3.12.x recommended (reference bundle used 3.12.14).' }
& $py -m venv (Join-Path $Workspace '.venv-work102')
$pyExe = Join-Path $Workspace '.venv-work102/Scripts/python.exe'
& $pyExe -m pip install --upgrade pip
& $pyExe -m pip install 'pytest==8.3.5'
& $pyExe --version
& $pyExe -m pytest --version
Write-Host 'ENV READY: .venv-work102 (pytest 8.3.5 pinned)'
