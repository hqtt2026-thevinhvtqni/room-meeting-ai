# Work 32 — one-shot, read-only PC runtime provenance diagnostic
# Run in PowerShell on the PC. No install, no file writes, no process changes.
# Excludes :8020, /mcp, POST, transcript APIs and environment dumps.
$ErrorActionPreference = 'Stop'
$TargetPid = 20468
$ExpectedAdapterBlob = '8cd73faca62057cbfbbd0ac03c07254c02e8df6c'
$BaseUrl = 'http://127.0.0.1:8787'
function Redact-CommandLine([string]$Value) {
 if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
 $v = [regex]::Replace($Value, '(?i)(--?(?:token|password|passwd|secret|api[-_]?key|authorization)\s+)(\S+)', '$1<REDACTED>')
 $v = [regex]::Replace($v, '(?i)((?:token|password|passwd|secret|api[-_]?key|authorization)=)([^&\s]+)', '$1<REDACTED>')
 return $v
}
function Get-ProcRecord([int]$Id) {
 if ($Id -le 0) { return $null }
 $p = Get-CimInstance Win32_Process -Filter "ProcessId = $Id" -ErrorAction SilentlyContinue
 if (-not $p) { return [ordered]@{pid=$Id;state='NOT_FOUND'} }
 $owner = $null
 try { $owner = Invoke-CimMethod -InputObject $p -MethodName GetOwner -ErrorAction Stop } catch {}
 return [ordered]@{pid=[int]$p.ProcessId;state='FOUND';parent_pid=[int]$p.ParentProcessId;creation_date=[string]$p.CreationDate;executable_path=[string]$p.ExecutablePath;command_line_redacted=(Redact-CommandLine ([string]$p.CommandLine));owner=if ($owner -and $owner.ReturnValue -eq 0) {"$($owner.Domain)\$($owner.User)"} else {'UNAVAILABLE'}}
}
function Get-HttpSummary([string]$Uri,[string]$Kind) {
 try {
  $r=Invoke-WebRequest -Uri $Uri -Method Get -UseBasicParsing -TimeoutSec 8
  $o=[ordered]@{url=$Uri;http_status=[int]$r.StatusCode}
  if ($Kind -eq 'health') {
   try {$j=$r.Content|ConvertFrom-Json; foreach($k in @('service','ok','browser_started')) {if($j.PSObject.Properties.Name -contains $k){$o[$k]=$j.$k}}} catch {$o['body_parse']='UNAVAILABLE'}
  } else {
   try {$j=$r.Content|ConvertFrom-Json; if($j.info){$o['title']=[string]$j.info.title;$o['version']=[string]$j.info.version};$o['paths']=@($j.paths.PSObject.Properties.Name)} catch {$o['body_parse']='UNAVAILABLE'}
  }
  return $o
 } catch {$status=$null;try{$status=[int]$_.Exception.Response.StatusCode}catch{};return [ordered]@{url=$Uri;http_status=$status;error=$_.Exception.GetType().Name}}
}
$result=[ordered]@{diagnostic='WORK32_PC_ONE_SHOT_READ_ONLY';timestamp=(Get-Date).ToString('o');target_pid=$TargetPid;expected_work32_adapter_git_blob=$ExpectedAdapterBlob;process_chain=@();cwd_status='NOT_CHECKED';cwd=$null;import_resolution_label='RECONSTRUCTED IMPORT RESOLUTION ONLY — NOT THE RUNNING PROCESS IN-MEMORY MODULE';import_origin=$null;python_version=$null;source_file_git_blob=$null;blob_matches_work32=$null;source_repository=$null;http=@();safety='No process changes; no environment output; no writes; no POST; no /mcp; no transcript access; no :8020.'}
$target=Get-ProcRecord $TargetPid
$result.process_chain += $target
$parentId=0
if($target -and $target.parent_pid){$parentId=[int]$target.parent_pid}
if($parentId -gt 0){$parent=Get-ProcRecord $parentId;$result.process_chain += $parent;if($parent -and $parent.parent_pid -and [int]$parent.parent_pid -gt 0){$result.process_chain += (Get-ProcRecord ([int]$parent.parent_pid))}}
$pythonExe=$null
if($target -and $target.state -eq 'FOUND'){$pythonExe=$target.executable_path}
if([string]::IsNullOrWhiteSpace($pythonExe) -or -not(Test-Path -LiteralPath $pythonExe -PathType Leaf)){
 $result.cwd_status='CWD_UNAVAILABLE_NO_VALID_PROCESS_EXECUTABLE'
} else {
 $cwdCode=@'
import json,sys
try:
 import psutil
 p=psutil.Process(int(sys.argv[1]))
 print(json.dumps({"cwd":p.cwd(),"create_time":p.create_time()}))
except Exception as e:
 print(json.dumps({"error":type(e).__name__,"detail":str(e)[:240]}))
'@
 $cwdRaw=$null
 try{$cwdRaw=& $pythonExe -c $cwdCode $TargetPid 2>$null}catch{}
 $cwdObj=$null
 if($cwdRaw){try{$cwdObj=($cwdRaw -join [Environment]::NewLine)|ConvertFrom-Json}catch{}}
 if($cwdObj -and $cwdObj.cwd){
  $result.cwd_status='AVAILABLE_VIA_EXISTING_PSUTIL';$result.cwd=[string]$cwdObj.cwd;$result.psutil_create_time=$cwdObj.create_time
  $resolveCode=@'
import importlib.util,json,sys,platform
s=importlib.util.find_spec("adapter")
print(json.dumps({"origin":(s.origin if s else None),"python_version":platform.python_version(),"executable":sys.executable}))
'@
  try {
   Push-Location -LiteralPath $result.cwd
   $resolveRaw=& $pythonExe -c $resolveCode 2>$null
   Pop-Location
   if($resolveRaw){$resolveObj=($resolveRaw -join [Environment]::NewLine)|ConvertFrom-Json;$result.import_origin=$resolveObj.origin;$result.python_version=$resolveObj.python_version;$result.resolution_executable=$resolveObj.executable}
  } catch {try{Pop-Location}catch{};$result.import_resolution_error=$_.Exception.GetType().Name}
  if($result.import_origin -and (Test-Path -LiteralPath $result.import_origin -PathType Leaf)){
   $sourceDir=Split-Path -Parent $result.import_origin
   try {
    $hash=(& git -C $sourceDir hash-object -- $result.import_origin 2>$null|Select-Object -First 1)
    if($LASTEXITCODE -eq 0 -and $hash){$result.source_file_git_blob=[string]$hash;$result.blob_matches_work32=([string]$hash -eq $ExpectedAdapterBlob)}
    $root=(& git -C $sourceDir rev-parse --show-toplevel 2>$null|Select-Object -First 1)
    if($LASTEXITCODE -eq 0 -and $root){$bn=(& git -C $root branch --show-current 2>$null|Select-Object -First 1);$head=(& git -C $root rev-parse HEAD 2>$null|Select-Object -First 1);$st=@(& git -C $root status --short 2>$null);$result.source_repository=[ordered]@{root=[string]$root;branch=[string]$bn;head=[string]$head;working_tree_entry_count=$st.Count;working_tree_status_first_20=@($st|Select-Object -First 20)}}else{$result.source_repository='GIT_METADATA_NOT_FOUND_FOR_RESOLVED_FILE'}
   } catch {$result.git_inspection_error=$_.Exception.GetType().Name}
  }
 } else {$result.cwd_status='CWD_UNAVAILABLE_PSUTIL_MISSING_OR_ACCESS_DENIED';if($cwdObj -and $cwdObj.error){$result.cwd_detail=[string]$cwdObj.error}}
}
$result.http += (Get-HttpSummary "$BaseUrl/health" 'health')
$result.http += (Get-HttpSummary "$BaseUrl/openapi.json" 'openapi')
$result|ConvertTo-Json -Depth 8
