from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
START = (ROOT / "05_TEST" / "START_WORK10_LOCAL.ps1").read_text(encoding="utf-8")
STOP = (ROOT / "05_TEST" / "STOP_WORK10_LOCAL.ps1").read_text(encoding="utf-8")
ACCEPTANCE = (ROOT / "05_TEST" / "RUN_WORK10_ACCEPTANCE.ps1").read_text(encoding="utf-8")


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"  PASS  {label}")


def main() -> None:
    check("launcher binds Agent API and Dashboard to loopback only",
          "127.0.0.1" in START and "3010" in START and "8787" in START)
    check("standalone Dashboard never starts a listener on shared port 3000",
          not re.search(r"http\.server\s+3000|TcpListener[^\n]*3000", START, re.IGNORECASE))
    check("writes and PowerShell remain disabled by default",
          "[string[]]$WritableRoots = @()" in START
          and "[string[]]$PowerShellRoots = @()" in START
          and "[switch]$EnableWrite" in START and "[switch]$EnablePowerShell" in START)
    check("write and PowerShell roots require explicit enable switches and stay inside read roots",
          "requires the explicit -EnableWrite" in START
          and "requires the explicit -EnablePowerShell" in START
          and "Test-PathWithinRoots" in START)
    check("default read access is restricted to the Work 10 root",
          "if (-not $AllowedRoots -or $AllowedRoots.Count -eq 0) { $AllowedRoots = @($WorkRoot) }" in START)
    check("launcher rejects drive-root and network-share-root grants",
          "GetPathRoot($canonical)" in START and "cannot be a drive or network-share root" in START)
    check("session record captures root permissions without storing the bearer token",
          "allowed_roots = $resolvedAllowedRoots" in START
          and "writable_roots = $resolvedWritableRoots" in START
          and "powershell_roots = $resolvedPowerShellRoots" in START
          and "write_enabled = [bool]$EnableWrite" in START
          and "powershell_enabled = [bool]$EnablePowerShell" in START)
    check("launcher refuses unknown processes occupying either local port",
          "Test-LoopbackPortAvailable" in START and "will not terminate an unknown process" in START)
    check("bearer token is copied to clipboard and not added to session record",
          "Set-Clipboard -Value $token" in START
          and not re.search(r"\btoken\s*=", START[START.find("$session ="):START.find("ConvertTo-Json")], re.IGNORECASE))
    check("launcher uses process-local environment, not persistent user environment",
          "SetEnvironmentVariable(" not in START and "$env:COMPUTER_AGENT_API_TOKEN = $null" in START)
    check("stop script refuses to stop while execution is busy",
          "execution_busy" in STOP and "Wait for completion" in STOP)
    check("stop script verifies command line and process start time before stopping",
          "Get-CimInstance Win32_Process" in STOP
          and "CommandLine" in STOP and "StartTime" in STOP)
    check("stop script removes only its session record after verified shutdown",
          "Remove-Item -LiteralPath $sessionPath" in STOP
          and "refusing to stop it" in STOP)
    check("non-interactive mode suppresses clipboard and browser launch",
          "[switch]$NoClipboard" in START and "[switch]$NoOpenBrowser" in START)
    api_start = START.find("$api = Start-Process")
    dashboard_start = START.find("$dashboard = Start-Process")
    token_clear = START.find("$env:COMPUTER_AGENT_API_TOKEN = $null", api_start)
    check("static Dashboard server does not inherit the Agent API bearer token",
          api_start >= 0 and token_clear > api_start and token_clear < dashboard_start)
    check("launcher failure cleans up the session record and secret variables",
          "Remove-Item -LiteralPath $sessionPath -Force" in START
          and "$token = $null" in START)
    check("one-command acceptance runner is gated to Windows 10 client",
          "Win32_OperatingSystem" in ACCEPTANCE and "Windows 10" in ACCEPTANCE and "ProductType -ne 1" in ACCEPTANCE)
    check("acceptance runner performs launcher smoke, full suite and real browser E2E",
          "START_WORK10_LOCAL.ps1" in ACCEPTANCE and "STOP_WORK10_LOCAL.ps1" in ACCEPTANCE
          and "05_TEST/run_all_tests.py" in ACCEPTANCE and "05_TEST/e2e_real_browser.py" in ACCEPTANCE)
    check("acceptance report captures source hashes and never writes secret values",
          "Get-FileHash" in ACCEPTANCE and "production_v8_hmac_env_present" in ACCEPTANCE and "production_v8_trust_validation = \"NOT_RUN\"" in ACCEPTANCE
          and "COMPUTER_AGENT_API_TOKEN =" not in ACCEPTANCE)
    check("acceptance report keeps release gate open after local test success",
          'release_gate = "OPEN"' in ACCEPTANCE and "HOST_TESTS_PASS" in ACCEPTANCE)
    check("acceptance runner always writes a report even after a test failure",
          "finally {" in ACCEPTANCE and "failure_reason" in ACCEPTANCE and "Set-Content -LiteralPath $reportPath" in ACCEPTANCE)
    check("launcher exposes no generic shell or inline PowerShell command",
          "Invoke-Expression" not in START and "powershell.exe -Command" not in START)
    print("Windows launcher contract: 22 checks passed")


if __name__ == "__main__":
    main()
