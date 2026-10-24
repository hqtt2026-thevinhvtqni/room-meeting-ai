# Work 102 — pinned candidate test environment setup
# Creates only .venv-work102 under the supplied workspace; does not modify candidate source.
param(
  [Parameter(Mandatory=$true)][string]$Workspace
)
$ErrorActionPreference = 'Stop'
$workspaceFull = (Resolve-Path $Workspace).Path
$pyCommand = Get-Command python -ErrorAction Stop
$baseVersion = (& $pyCommand.Source --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $baseVersion -ne 'Python 3.12.14') {
  throw "Required Python 3.12.14 exactly; found '$baseVersion'. No environment created."
}
$venvDir = Join-Path $workspaceFull '.venv-work102'
if (Test-Path $venvDir) {
  throw "Refusing to overwrite existing venv: $venvDir. Remove it manually only after preserving any needed evidence."
}
& $pyCommand.Source -m venv $venvDir
if ($LASTEXITCODE -ne 0) { throw 'python -m venv failed.' }
$pyExe = Join-Path $venvDir 'Scripts/python.exe'
& $pyExe -m pip install 'pytest==8.3.5'
if ($LASTEXITCODE -ne 0) { throw 'Installing pinned pytest failed.' }
$pyVersion = (& $pyExe --version 2>&1 | Out-String).Trim()
$pytestVersion = (& $pyExe -m pytest --version 2>&1 | Out-String).Trim()
if ($pyVersion -ne 'Python 3.12.14') { throw "Venv Python version mismatch: $pyVersion" }
if ($pytestVersion -notmatch 'pytest 8\.3\.5(?:\s|$)') { throw "Pinned pytest version mismatch: $pytestVersion" }
Write-Host "ENV READY: $venvDir"
Write-Host $pyVersion
Write-Host $pytestVersion
