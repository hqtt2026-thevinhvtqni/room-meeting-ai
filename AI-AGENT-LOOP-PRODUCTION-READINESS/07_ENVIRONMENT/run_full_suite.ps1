# Work 102 — hash-gated full-suite evidence runner
# Exit 0 = tests pass on hash-matched candidate; 1 = tests fail (valid evidence); 2 = hash/environment mismatch (not a valid test run).
param(
  [Parameter(Mandatory=$true)][string]$Workspace,
  [string]$HashFile,
  [string]$EvidenceDir
)
$ErrorActionPreference = 'Stop'
$workspaceFull = (Resolve-Path $Workspace).Path
if (-not $HashFile) { $HashFile = Join-Path $PSScriptRoot 'expected_candidate_hashes.json' }
$HashFile = (Resolve-Path $HashFile).Path
$expectedDoc = Get-Content $HashFile -Raw | ConvertFrom-Json
$expected = $expectedDoc.files
$venv = Join-Path $workspaceFull '.venv-work102/Scripts/python.exe'
if (-not (Test-Path $venv)) { Write-Error 'Missing .venv-work102; run setup_env.ps1 first.'; exit 2 }
$pyVersion = (& $venv --version 2>&1 | Out-String).Trim()
$pytestVersion = (& $venv -m pytest --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $pyVersion -ne 'Python 3.12.14' -or $pytestVersion -notmatch 'pytest 8\.3\.5(?:\s|$)') {
  Write-Error "Environment mismatch: python='$pyVersion'; pytest='$pytestVersion'. Refusing to run."
  exit 2
}
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
if (-not $EvidenceDir) { $EvidenceDir = Join-Path $workspaceFull ('06_EVIDENCE/AUTHORIZED_RUN_' + $stamp) }
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
$EvidenceDir = (Resolve-Path $EvidenceDir).Path

$hashStatus = @()
$drift = $false
foreach ($p in $expected.PSObject.Properties) {
  $full = Join-Path $workspaceFull $p.Name
  if (-not (Test-Path $full -PathType Leaf)) {
    $hashStatus += [pscustomobject]@{file=$p.Name; expected=$p.Value; status='NOT_VERIFIED'; actual=$null}
    $drift = $true
    continue
  }
  $actual = (Get-FileHash $full -Algorithm SHA256).Hash.ToLowerInvariant()
  $st = if ($actual -eq ([string]$p.Value).ToLowerInvariant()) { 'MATCH' } else { $drift = $true; 'DRIFT' }
  $hashStatus += [pscustomobject]@{file=$p.Name; expected=$p.Value; status=$st; actual=$actual}
}
$hashPath = Join-Path $EvidenceDir 'HASH_CHECK.json'
$hashStatus | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 $hashPath
if ($drift) {
  Write-Host 'HASH DRIFT/NOT_VERIFIED: refusing to run.'
  exit 2
}

$oldLocation = Get-Location
try {
  Set-Location $workspaceFull
  $junitPath = Join-Path $EvidenceDir 'junit.xml'
  $stdoutPath = Join-Path $EvidenceDir 'pytest_stdout.txt'
  $stderrPath = Join-Path $EvidenceDir 'pytest_stderr.txt'
  $pytestArgs = @('-m','pytest','05_TEST','-v',"--junitxml=$junitPath")
  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = $venv
  $startInfo.Arguments = ($pytestArgs | ForEach-Object { if ($_ -match '\s') { '"' + $_.Replace('"','\\"') + '"' } else { $_ } }) -join ' '
  $startInfo.WorkingDirectory = $workspaceFull
  $startInfo.UseShellExecute = $false
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true
  $proc = New-Object System.Diagnostics.Process
  $proc.StartInfo = $startInfo
  $null = $proc.Start()
  $stdoutTask = $proc.StandardOutput.ReadToEndAsync()
  $stderrTask = $proc.StandardError.ReadToEndAsync()
  $proc.WaitForExit()
  $stdout = $stdoutTask.Result
  $stderr = $stderrTask.Result
  Set-Content -Encoding utf8 -Path $stdoutPath -Value $stdout
  Set-Content -Encoding utf8 -Path $stderrPath -Value $stderr
  $code = $proc.ExitCode
}
catch {
  $stdout = ''
  $stderr = $_ | Out-String
  Set-Content -Encoding utf8 -Path (Join-Path $EvidenceDir 'pytest_stdout.txt') -Value $stdout
  Set-Content -Encoding utf8 -Path (Join-Path $EvidenceDir 'pytest_stderr.txt') -Value $stderr
  $code = 2
}
finally {
  Set-Location $oldLocation
}
$manifest = [pscustomobject]@{
  run_id = 'AUTHORIZED_RUN_' + $stamp
  claim_scope = 'AUTHORIZED_LOCAL_CANDIDATE_HASH_BOUND'
  candidate = $expectedDoc.candidate
  command = "$venv -m pytest 05_TEST -v --junitxml=$((Join-Path $EvidenceDir 'junit.xml'))"
  cwd = $workspaceFull
  python_version = $pyVersion
  pytest_version = $pytestVersion
  exit_code = $code
  hash_file = $HashFile
  hash_status = 'ALL_MATCH'
  per_file_hashes = $hashStatus
  artifacts = @('HASH_CHECK.json','junit.xml','pytest_stdout.txt','pytest_stderr.txt','RUN_MANIFEST.json')
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 (Join-Path $EvidenceDir 'RUN_MANIFEST.json')
Write-Host "RUN COMPLETE exit=$code evidence=$EvidenceDir"
exit $code
