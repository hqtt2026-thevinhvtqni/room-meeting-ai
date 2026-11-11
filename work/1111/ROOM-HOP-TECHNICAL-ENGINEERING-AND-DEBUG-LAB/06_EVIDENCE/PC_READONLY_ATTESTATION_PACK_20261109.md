# PC READ-ONLY ATTESTATION PACK — W1111 C07

- Prepared by: Co — Coder under Cla (CTO)
- Date: 2026-11-09 (UTC+7)
- Target PC repository: `D:\ROOM-HOP-CLEAN\room-meeting-ai`
- Mode: READ ONLY. Do not restart/stop processes, call /execute, write files on PC, change environment, stage/commit/push, or print secret values.
- This document is a handoff package only; Co did not execute these commands on the PC.

## 1. PowerShell collection script

Run in PowerShell 7 or Windows PowerShell 5.1 from any directory. It prints process identity with secret-like command-line arguments redacted, attempts a read-only x64 PEB working-directory query, hashes four W13 files, reports Git branch/HEAD/working tree, and reports only whether secret-like environment variables exist.

```powershell
$ErrorActionPreference = 'Stop'
$repoRoot = 'D:\ROOM-HOP-CLEAN\room-meeting-ai'
$pids = @(14280, 16484) | Select-Object -Unique

'=== PROCESS IDENTITY ==='
foreach ($targetPid in $pids) {
    $p = Get-CimInstance Win32_Process -Filter "ProcessId = $targetPid" -ErrorAction SilentlyContinue
    if (-not $p) {
        [pscustomobject]@{ ProcessId=$targetPid; Present=$false }
        continue
    }
    $safeCommandLine = [string]$p.CommandLine
    $safeCommandLine = [regex]::Replace(
        $safeCommandLine,
        '(?i)((?:--)?(?:token|secret|password|api[-_]?key|credential)(?:=|\s+))(?:"[^"]*"|\S+)',
        '$1<REDACTED>'
    )
    [pscustomobject]@{
        ProcessId = $p.ProcessId
        ParentProcessId = $p.ParentProcessId
        ExecutablePath = $p.ExecutablePath
        CommandLineRedacted = $safeCommandLine
        CreationDate = $p.CreationDate
    } | Format-List

    # Read the target process current directory from its x64 PEB.
    # This uses PROCESS_QUERY_INFORMATION + PROCESS_VM_READ only.
    if ([IntPtr]::Size -eq 8) {
        Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class W1111ReadOnlyPeb {
  [StructLayout(LayoutKind.Sequential)]
  public struct PROCESS_BASIC_INFORMATION {
    public IntPtr Reserved1;
    public IntPtr PebBaseAddress;
    public IntPtr Reserved2_0;
    public IntPtr Reserved2_1;
    public UIntPtr UniqueProcessId;
    public UIntPtr InheritedFromUniqueProcessId;
  }
  [DllImport("kernel32.dll", SetLastError=true)]
  public static extern IntPtr OpenProcess(uint access, bool inherit, uint pid);
  [DllImport("kernel32.dll", SetLastError=true)]
  public static extern bool ReadProcessMemory(IntPtr process, IntPtr address, byte[] buffer, UIntPtr size, out UIntPtr read);
  [DllImport("kernel32.dll", SetLastError=true)]
  public static extern bool CloseHandle(IntPtr handle);
  [DllImport("ntdll.dll")]
  public static extern int NtQueryInformationProcess(IntPtr process, int infoClass, ref PROCESS_BASIC_INFORMATION info, int length, out int returned);
}
'@ -ErrorAction SilentlyContinue
        $h = [W1111ReadOnlyPeb]::OpenProcess(0x0410, $false, [uint32]$targetPid)
        try {
            if ($h -eq [IntPtr]::Zero) { throw "OpenProcess failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
            $bi = [W1111ReadOnlyPeb+PROCESS_BASIC_INFORMATION]::new()
            $ret = 0
            $nt = [W1111ReadOnlyPeb]::NtQueryInformationProcess($h, 0, [ref]$bi, [Runtime.InteropServices.Marshal]::SizeOf($bi), [ref]$ret)
            if ($nt -ne 0) { throw "NtQueryInformationProcess NTSTATUS=$nt" }
            $ptrSize = 8
            $ppBuf = New-Object byte[] 8
            $read = [UIntPtr]::Zero
            if (-not [W1111ReadOnlyPeb]::ReadProcessMemory($h, [IntPtr]::Add($bi.PebBaseAddress, 0x20), $ppBuf, [UIntPtr]8, [ref]$read)) { throw 'ReadProcessMemory PEB.ProcessParameters failed' }
            $pp = [BitConverter]::ToInt64($ppBuf, 0)
            $curBuf = New-Object byte[] 16
            if (-not [W1111ReadOnlyPeb]::ReadProcessMemory($h, [IntPtr]::Add([IntPtr]$pp, 0x38), $curBuf, [UIntPtr]16, [ref]$read)) { throw 'ReadProcessMemory CurrentDirectory failed' }
            $len = [BitConverter]::ToUInt16($curBuf, 0)
            $bufPtr = [BitConverter]::ToInt64($curBuf, 8)
            $pathBuf = New-Object byte[] $len
            if ($len -gt 0 -and -not [W1111ReadOnlyPeb]::ReadProcessMemory($h, [IntPtr]$bufPtr, $pathBuf, [UIntPtr]$len, [ref]$read)) { throw 'ReadProcessMemory directory buffer failed' }
            [pscustomobject]@{ ProcessId=$targetPid; WorkingDirectory=[Text.Encoding]::Unicode.GetString($pathBuf) } | Format-List
        } catch {
            [pscustomobject]@{ ProcessId=$targetPid; WorkingDirectory='UNAVAILABLE'; Reason=$_.Exception.Message } | Format-List
        } finally {
            if ($h -ne [IntPtr]::Zero) { [void][W1111ReadOnlyPeb]::CloseHandle($h) }
        }
    } else {
        [pscustomobject]@{ ProcessId=$targetPid; WorkingDirectory='UNAVAILABLE: run 64-bit PowerShell for x64 PEB query' } | Format-List
    }
}

'=== W13 SOURCE FILE SHA256 ==='
$w13 = Join-Path $repoRoot '.ai-workspace\sessions\AI-BUILD-GATEWAY-V1\workspace\13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE\execution_host'
$files = @('server.py','host.py','w12_adapter.py','wee_bridge.py')
foreach ($name in $files) {
    $path = Join-Path $w13 $name
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        Get-FileHash -Algorithm SHA256 -LiteralPath $path | Select-Object @{n='File';e={$name}},Hash,Path | Format-List
    } else {
        [pscustomobject]@{ File=$name; Hash='MISSING'; Path=$path } | Format-List
    }
}

'=== GIT BRANCH / HEAD / WORKTREE ==='
git -C $repoRoot branch --show-current
git -C $repoRoot rev-parse HEAD
git -C $repoRoot status --short

'=== SECRET-LIKE ENVIRONMENT VARIABLE PRESENCE ONLY ==='
$secretNames = @(Get-ChildItem Env: | Where-Object { $_.Name -match '(?i)(TOKEN|SECRET|CREDENTIAL|AUTH|API.?KEY|PRIVATE.?KEY)' })
[pscustomobject]@{
    SecretLikeEnvironmentVariablePresent = ($secretNames.Count -gt 0)
    SecretLikeEnvironmentVariableCount = $secretNames.Count
} | Format-List
```

## 2. Known comparison anchors (do not treat as current values)

| Item | Previously observed value | Scope / limitation |
|---|---|---|
| PID 16484 | Python 3.12, `python.exe -m execution_host.server`, created 2026-11-08 11:39:57 | Historical user-provided process evidence; later output reports PID 14280, so do not conflate |
| PID 14280 | Python 3.12, `python -m execution_host.server`, created 2026-11-09 02:53:23 | Latest PID recorded in W1111; current presence must be rechecked |
| Previous health build_hash | `a3ab13f49fd10501588a6da26028b1c147ba7097836884ae39264af49e124012` | Health identity associated with PID 16484 only; not mapped to a reproducible source manifest |
| Prior W13 file hashes | Full values were captured in the 2026-11-08 journal entry for PID 16484 | Disk hashes do not prove the process imported those exact files |
| New PID 14280 source hashes | NOT PROVIDED in the recorded excerpt | Fill from the four SHA256 outputs above |
| Git branch / HEAD / dirty state | NOT RE-ATTESTED by this package | Fill from read-only Git output |

## 3. Required return evidence

Paste the complete output for:
1. Both process identity blocks (PID 14280 and PID 16484).
2. WorkingDirectory result or explicit UNAVAILABLE reason for each present PID.
3. Four full SHA256 results.
4. Git branch, full HEAD SHA and complete `git status --short`.
5. Secret-like environment presence/count only; never paste variable values.

## 4. Decision required from Anh Vinh — legacy host risk

The historical PID 16484 health evidence reported `allow_processes=true` and `127.0.0.1:8031`; the newer PID 14280 must be independently checked. The older host may lack the PR #48 Core-grant authorization boundary.

- [ ] KEEP RUNNING temporarily for read-only diagnosis only.
- [ ] TEMPORARILY PAUSE after an explicit owner decision and a separate controlled shutdown plan.
- [ ] OTHER: ______________________________________

Co does not stop or restart either process. This package makes no safety certification and no deployment recommendation decision on behalf of Anh Vinh.
