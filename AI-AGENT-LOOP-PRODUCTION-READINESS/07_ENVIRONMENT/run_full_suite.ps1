# Work 102 — hash-gated full-suite evidence runner
# Exit 0 = PASS on hash-matched source; 1 = tests ran & failed (valid evidence); 2 = drift/env failure (NOT a valid run).
param(
  [string]$Workspace = (Get-Location).Path,
  [string]$HashFile,
  [string]$EvidenceDir
)
$ErrorActionPreference = 'Stop'
if (-not $HashFile) { $HashFile = Join-Path $PSScriptRoot 'expected_candidate_hashes.json' }
$expected = (Get-Content $HashFile -Raw | ConvertFrom-Json).files
$venv = Join-Path $Workspace '.venv-work102/Scripts/python.exe'
if (-not (Test-Path $venv)) { throw 'Missing .venv-work102. Run setup_env.ps1 first.' }
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
if (-not $EvidenceDir) { $EvidenceDir = Join-Path $Workspace ('AI-AGENT-LOOP-PRODUCTION-READINESS/06_EVIDENCE/AUTHORIZED_RUN_' + $stamp) }
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

$hashStatus = @()
$drift = $false
foreach ($p in $expected.PSObject.Properties) {
  $full = Join-Path $Workspace $p.Name
  if (-not (Test-Path $full)) { $hashStatus += [pscustomobject]@{file=$p.Name; status='NOT_VERIFIED'; actual=$null}; $drift = $true; continue }
  $actual = (Get-FileHash $full -Algorithm SHA256).Hash.ToLower()
  $st = if ($actual -eq $p.Value) { 'MATCH' } else { $drift = $true; 'DRIFT' }
  $hashStatus += [pscustomobject]@{file=$p.Name; status=$st; actual=$actual}
}
$hashStatus | ConvertTo-Json -Depth 3 | Set-Content (Join-Path $EvidenceDir 'HASH_CHECK.json')
$hashStatus | Format-Table file, status -AutoSize
if ($drift) { Write-Host 'HASH DRIFT: refusing to run. Re-record candidate hashes via journal first.'; exit 2 }

Set-Location $Workspace
$pyArgs = '-m','pytest','05_TEST','-v','--junitxml=' + (Join-Path $EvidenceDir 'junit.xml')
& $venv @pyArgs *> (Join-Path $EvidenceDir 'pytest_raw_output.txt')
$code = $LASTEXITCODE
$manifest = [pscustomobject]@{
  run_id = 'AUTHORIZED_RUN_' + $stamp
  claim_scope = 'SANDBOX_CANDIDATE_HASH_BOUND'
  candidate = 'work102-patch-v2-adopted-20261024'
  command = ($pyArgs -join ' ')
  cwd = $Workspace
  python_version = (& $venv --version)
  pytest_version = ((& $venv -m pytest --version) -join ' ')
  exit_code = $code
  hash_file = $HashFile
  hash_status = 'ALL_MATCH'
  artifacts = @('HASH_CHECK.json','junit.xml','pytest_raw_output.txt','RUN_MANIFEST.json')
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $EvidenceDir 'RUN_MANIFEST.json')
Write-Host ("RUN COMPLETE exit=" + $code + " evidence=" + $EvidenceDir)
exit $code
