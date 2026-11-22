from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
START = (ROOT / "05_TEST" / "START_WORK10_LOCAL.ps1").read_text(encoding="utf-8")
STOP = (ROOT / "05_TEST" / "STOP_WORK10_LOCAL.ps1").read_text(encoding="utf-8")


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
          'COMPUTER_AGENT_HOST_WRITABLE_ROOTS = ""' in START
          and 'COMPUTER_AGENT_HOST_POWERSHELL_ROOTS = ""' in START)
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
    check("launcher failure cleans up the session record and secret variables",
          "Remove-Item -LiteralPath $sessionPath -Force" in START
          and "$token = $null" in START)
    check("launcher exposes no generic shell or inline PowerShell command",
          "Invoke-Expression" not in START and "powershell.exe -Command" not in START)
    print("Windows launcher contract: 12 checks passed")


if __name__ == "__main__":
    main()
