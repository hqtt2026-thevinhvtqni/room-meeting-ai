# W1111 C07 — CORE PEB CWD MINIMAL RELOAD
- Prepared by: Co — Technical Execution Assistant / Coder W1111
- Date/time: 2026-11-10 10:45 UTC+7
- Source recovered from existing Sandbox evidence: 06_EVIDENCE/PC_READONLY_ATTESTATION_PACK_20261109.md.
- Important naming correction: the existing successful PEB reader in that pack is the global static type W1111ReadOnlyPeb, not namespace/class W1111ReadOnly.PebReader. The earlier 10:36 failure referenced a type that was not loaded in the current session.
- The PEB reader uses OpenProcess access 0x0410 (query + VM read), NtQueryInformationProcess(ProcessBasicInformation), ReadProcessMemory and CloseHandle. x64 offsets: PEB.ProcessParameters 0x20; RTL_USER_PROCESS_PARAMETERS.CurrentDirectory 0x38; UNICODE_STRING length 0 and buffer pointer 8.
- The accompanying script below preserves the existing PEB layout and read sequence; it adds only a type-presence guard and labeled read-only output for PIDs 7940 and 1472.

## PC action required
- Run in 64-bit PowerShell. It does not restart/stop processes, call HTTP endpoints, write repository files, read secrets or mutate Git.
- Expected evidence: PID 7940 CWD and PID 1472 CWD, each with length and directory-exists check; any failure prints NOT_VERIFIED and an explicit error.

```powershell
# W1111 — minimal read-only PEB CWD probe for current Core/Host PIDs
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 8) { throw 'Run in 64-bit PowerShell; x64 PEB offsets are required.' }
if (-not ('W1111ReadOnlyPeb' -as [type])) {
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
'@
}
foreach ($targetPid in @(7940,1472)) {
  $h = [IntPtr]::Zero
  try {
    $h = [W1111ReadOnlyPeb]::OpenProcess(0x0410, $false, [uint32]$targetPid)
    if ($h -eq [IntPtr]::Zero) { throw "OpenProcess failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
    $bi = [W1111ReadOnlyPeb+PROCESS_BASIC_INFORMATION]::new()
    $ret = 0
    $nt = [W1111ReadOnlyPeb]::NtQueryInformationProcess($h, 0, [ref]$bi, [Runtime.InteropServices.Marshal]::SizeOf($bi), [ref]$ret)
    if ($nt -ne 0) { throw "NtQueryInformationProcess NTSTATUS=$nt" }
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
    $cwd = [Text.Encoding]::Unicode.GetString($pathBuf)
    [pscustomobject]@{ PID=$targetPid; PEB_CURRENT_DIRECTORY=$cwd; PEB_CWD_LENGTH=$cwd.Length; PEB_DIRECTORY_EXISTS=(Test-Path -LiteralPath $cwd -PathType Container) } | Format-List
  } catch {
    [pscustomobject]@{ PID=$targetPid; PEB_CURRENT_DIRECTORY='NOT_VERIFIED'; PEB_READ_ERROR=$_.Exception.Message } | Format-List
  } finally {
    if ($h -ne [IntPtr]::Zero) { [void][W1111ReadOnlyPeb]::CloseHandle($h) }
  }
}
```

## Interpretation
- Empty output or a failed type load is NOT evidence of an empty Core CWD.
- Keep PID 1472 prior VERIFIED result unless a new measurement contradicts it.
- CWD does not prove imported module path; exact module provenance remains a separate gate.