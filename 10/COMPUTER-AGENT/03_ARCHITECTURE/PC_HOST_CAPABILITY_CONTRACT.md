# WORK 10 — PC HOST CAPABILITY CONTRACT

- Contract ID: W10-PC-HOST-CAPABILITY-1.0
- Status: PROPOSED / IMPLEMENTATION IN PROGRESS
- Owner: Work 10 — COMPUTER-AGENT
- Scope: File system, PowerShell script execution and pytest execution on the local PC host.
- Relationship: Separate from the LOCKED browser Action Contract. This document does not add action types or alter ACTION_CONTRACT.md, WORKFLOW_CONTRACT.md or SAFETY_POLICY.md.

## 1. Design boundary

All host operations are submitted to POST /agent/host/execute and run inside the same OS-contained worker process managed by ProcessSupervisor. They do not execute in the HTTP server process. The host API uses the same bearer token, exact Origin allow-list, 1 MiB request limit, exclusive execution lease, parent deadline and process-tree cleanup as browser workflows.

No generic shell, arbitrary command string, or powershell -Command operation is exposed.

**Privilege note:** host operations execute under the local agent service account. The API's path allow-lists constrain which paths the agent may directly select, but they are not an OS-level filesystem sandbox for code inside an approved pytest test or approved PowerShell script. Only configure trusted roots and trusted scripts/tests; use a dedicated low-privilege Windows account for stronger isolation.

## 2. Supported operations

| Operation | Required arguments | Safety boundary |
|---|---|---|
| list_directory | path | Read-only; resolved path must remain inside an allowlisted root; bounded entry count |
| read_file | path; optional encoding | Read-only; UTF-8 or base64; bounded file size; symlink target must remain inside root |
| write_file | path, content; optional encoding, overwrite | Requires explicit writable-root allow-list; bounded content; no overwrite unless overwrite=true; atomic write/read-back/hash |
| run_pytest | paths list; optional cwd | Fixed executable sys.executable -m pytest -q; paths/cwd must remain inside allowed roots; no arbitrary CLI flags or shell |
| run_powershell_script | script; optional string arguments list | Windows only; existing .ps1 must be inside explicit PowerShell script roots; invokes powershell.exe/pwsh -NoProfile -NonInteractive -File; no inline command |
| validate_acceptance_manifest | manifest_path, evidence_root, attestation_path | V8 JSON Schema + semantic category policy + exact state comparison + fixture/artifact SHA-256 + trusted host/source provenance + HMAC-signed attestation; requires pinned hashes and protected HMAC key |

## 3. Host configuration

All paths are operator-configured local paths; values are separated by the platform path separator (; on Windows, : on POSIX).

- COMPUTER_AGENT_HOST_ALLOWED_ROOTS: roots for list/read/pytest.
- COMPUTER_AGENT_HOST_WRITABLE_ROOTS: explicit roots for write_file. If absent, file writes are disabled.
- COMPUTER_AGENT_HOST_POWERSHELL_ROOTS: explicit roots for approved .ps1 scripts. If absent, PowerShell execution is disabled.
- COMPUTER_AGENT_HOST_MAX_FILE_BYTES: default 5 MiB, hard cap 20 MiB.
- COMPUTER_AGENT_HOST_MAX_OUTPUT_BYTES: default 1 MiB, hard cap 4 MiB.
- COMPUTER_AGENT_HOST_COMMAND_TIMEOUT_SECONDS: default 120 s, hard cap 300 s.

Default allowed root is the Work 10 root. Writable and PowerShell roots default to empty. An operator must deliberately configure them before those capabilities become available.

## 4. Execution and result semantics

- Host operation request includes an operation name and object arguments.
- Unknown operations and paths outside configured roots are BLOCKED before filesystem/process side effects.
- File writes are read back and SHA-256 hashed before PASS.
- Pytest/PowerShell run without shell=True; command is an argument vector, not a shell string. Pytest disables ambient plugin autoload, uses a generated empty config and confines conftest discovery to the selected allowed cwd.
- A completed command with nonzero exit code is FAIL.
- A command timeout or uncertain child state is BLOCKED; worker sets cleanup_pending, parent terminates the complete Job Object/process group and verifies containment empty before releasing the execution lease.
- Result includes operation, status, output summary, evidence, timestamps and state trace.

## 5. Prohibited behavior

- No arbitrary shell, cmd.exe /c, powershell -Command, Invoke-Expression, or dynamic script text.
- No writes outside explicit writable roots.
- No PowerShell script outside explicit script roots.
- No user-supplied executable path or arbitrary executable/argument vector.
- No bypass of authentication, Origin allow-list, execution lease or ProcessSupervisor.
- No claim of full PC access merely because a host operation passed on a hosted CI runner.

## 6. Acceptance tests

- Path traversal and symlink escape are BLOCKED.
- Read/list operate only within allowlisted roots.
- Write denied by default; allowed only inside writable roots; overwrite requires explicit flag; read-back hash matches.
- Pytest executes only allowlisted test paths and returns exact exit code/output.
- PowerShell script executes only on Windows and only from explicit .ps1 roots; nonzero exit and timeout semantics are correct.
- All host operations include ProcessSupervisor containment evidence.
- Windows host operations must pass on hosted Windows runner and then be validated on Owner's physical Windows 10 PC.
- Linux host operations remain under the LIMITED process-group test profile until cgroup-v2 is implemented.

KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead


## Implementation status update — 2026-11-22

PC Host Capability Contract v1.0 is implemented in host_operations.py and POST /agent/host/execute. GitHub Actions #49 passes on hosted Windows Server 2022 and Ubuntu 24.04. Windows covers PowerShell; both cover file operations and pytest. See 06_EVIDENCE/W10_HOST_CAPABILITIES_CI_EVIDENCE_20261122_RUN49.md.

Status: IMPLEMENTED — HOSTED CI PASS. Physical Windows 10 validation, operator-specific root configuration, low-privilege service account/ACL review and ROOM-HOP integration remain open. The allow-list is an API boundary, not an OS sandbox for approved pytest/PowerShell code; only trusted scripts and test roots may be configured.


## V8 acceptance validator trust configuration

The host capability API also exposes validate_acceptance_manifest. It rejects caller-authored consistency flags (not part of the V8 schema), recomputes expected/observed equality, checks category-specific allowed outcomes, disallows UNKNOWN lease/owner states on PASS, verifies fixture/artifact bytes and runner/source identity, and writes a separate HMAC-SHA256 attestation.

Required host configuration:
- COMPUTER_AGENT_VALIDATOR_SHA256 — pinned acceptance_validator.py SHA-256.
- COMPUTER_AGENT_VALIDATOR_SCHEMA_SHA256 — pinned V8 schema SHA-256.
- COMPUTER_AGENT_VALIDATOR_POLICY_SHA256 — pinned category policy SHA-256.
- COMPUTER_AGENT_VALIDATOR_HMAC_KEY — secret key of at least 32 bytes.
- COMPUTER_AGENT_VALIDATOR_KEY_ID — stable key identifier.
- COMPUTER_AGENT_SOURCE_COMMIT — expected source commit SHA (CI may use GITHUB_SHA).

If any pin/key is missing or mismatched, validator returns BLOCKED and emits no trusted PASS attestation. CI uses a clearly labelled test-only HMAC key; that key is not production trust material. The allow-listed pytest/PowerShell code runs with the host service account's privileges and is not an OS-level filesystem sandbox.
