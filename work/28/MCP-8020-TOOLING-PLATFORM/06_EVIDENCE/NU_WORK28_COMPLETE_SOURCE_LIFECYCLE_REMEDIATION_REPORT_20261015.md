# Nu — Work 28 source lifecycle remediation report
Date: 2026-10-15 (+07)
Work: MCP-8020-TOOLING-PLATFORM
Scope: **Sandbox-only**. Collector on PC, PC access/modification, source transfer/import, live changes and release are prohibited.
Current disposition: **IMPLEMENTED / STATIC REVIEW IN PROGRESS / NOT EXECUTED**

## Current canonical version matrix
| Artifact | Current version/state | Purpose |
|---|---|---|
| `04_CODE/pc_readonly_source_collector.py` | `pc-readonly-collector/0.4.0` | Read-only allowlisted collection draft; incremental metadata bounds, shared manifest cap, owned cleanup |
| `04_CODE/source_snapshot_contract.py` | `CONTRACT_VERSION 0.1.1` | Strict manifest schema, hard caps, collision key, metadata/path policy |
| `04_CODE/source_snapshot_import_verifier.py` | `source-snapshot-verifier/0.3.0` | In-memory-only archive verification; explicit ZIP creator/type policy |
| `05_TEST/test_source_snapshot_contract.py` | updated | Contract regressions including KAST-01/KAST-03 |
| `05_TEST/test_source_snapshot_import_verifier.py` | updated | Archive/hash/collision/type regressions |
| `05_TEST/test_kast_followup.py` | new | KAST follow-up: DOS/Unix ZIP policy, shared cap, incremental bounds |

Historical pre-remediation version statements are retained in prior audit records and are not authoritative for the current package.

## KAST-01 — path collision
**Disposition: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.**
- `casefold_path_key()` uses NFC/NFKC normalization plus `casefold()`.
- Contract rejects included-file collisions for Windows-like case-insensitive destinations.
- Verifier checks manifest and ZIP collision keys and exact path-set equality.
- Tests: contract case collision and verifier collision coverage.
- Residual: Unicode/Windows equivalence remains to be exercised on the approved target runner.

## KAST-02 — ZIP member type policy
**Disposition: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.**
Policy in `validate_zip_member_type()`:
- Accepted creator platforms: `create_system` 3 (Unix) or 0 (DOS/FAT) only.
- Unix creator: mode must be present and regular; symlink, FIFO, character/block device, socket and other special modes reject.
- DOS creator: Unix mode must be zero/absent; normal/read-only/hidden/system/archive DOS attributes are allowed.
- DOS directory, device, volume and reparse-like attributes reject.
- Other creator platforms or mixed/ambiguous mode metadata reject.
- Directory name/flag, encryption and unsupported compression remain rejected.
- Tests: normal DOS mode=0 acceptance; DOS mode ambiguity, reparse-like attribute, unknown creator and Unix special modes rejection; existing symlink-mode test retained.
- Residual: this is still an in-memory verifier, not an extraction proof.

## KAST-03 — manifest size before parse and drift
**Disposition: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.**
- Single source of truth: `HARD_MAX_MANIFEST_BYTES` from `source_snapshot_contract.py`.
- Collector imports and uses that constant before manifest write.
- Verifier uses the same constant before decode/JSON parse.
- Follow-up test asserts contract/verifier constant identity.
- Oversized-manifest regression remains present.

## KAST-04 — incremental metadata bounds and owned cleanup
**Disposition: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.**
- `append_excluded()` enforces item length and count before each append.
- `parse_status()` enforces status item length/count during construction.
- Output directory must not pre-exist; collector sets ownership only after successful `mkdir()`.
- Failure cleanup removes only known archive/manifest paths and then removes the owned directory if empty.
- Follow-up tests cover immediate count and item-length rejection through the pure helper.
- Remaining failure-injection/Windows filesystem behavior requires approved isolated execution.

## Other lifecycle findings
- **F1 Windows race safety:** BLOCKED. Path checks, component checks, no-follow where supported and descriptor comparisons do not prove atomic safety against hostile concurrent replacement on Windows.
- **F3 provenance/receipt:** BLOCKED. Local manifest remains `UNAUTHENTICATED_LOCAL_OBSERVATION`; receipt validation is shape/hash/Work binding only, not signature, issuer or nonce-replay authentication.
- **F7 lifecycle:** DESIGN-READY / NOT VERIFIED. No extraction/import transaction is implemented.
- **F8 Git isolation:** DESIGN-READY / NOT VERIFIED. Fixed argv, `shell=False`, timeout, bounded output, `--no-optional-locks`, `core.fsmonitor=false` and sanitized environment are present; no approved harness has executed them.

## Evidence and test status
Canonical command:
`python -m unittest discover -s 05_TEST -t . -v`

- Approved runner: **not available/verified**.
- Test execution: **NOT RUN**.
- Exit code, stdout/stderr, test count and runner revision: **NOT AVAILABLE**.
- Artifact SHA-256: **NOT COMPUTED**; MCP surface has no approved artifact-hash operation.
- Source writes: completed through MCP and read back.
- Collector on PC: not run.
- Source transfer/import: not performed.
- E2E-Automatic: not started.

## Changed artifact readback
The following writes returned `status=ok` and were read back through MCP 8020:
- `04_CODE/pc_readonly_source_collector.py`
- `04_CODE/source_snapshot_contract.py`
- `04_CODE/source_snapshot_import_verifier.py`
- `05_TEST/test_source_snapshot_contract.py`
- `05_TEST/test_source_snapshot_import_verifier.py`
- `05_TEST/test_kast_followup.py`
- this report

Readback proves persistence and static inspection only; it is not a test PASS.

## Gate decision
```text
KAST-01: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED
KAST-02: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED
KAST-03: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED
KAST-04: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED
F1: BLOCKED
F3: BLOCKED
APPROVED RUNNER: BLOCKED
COLLECTOR RUN: NO-GO
SOURCE SNAPSHOT: NOT IMPORTED
E2E-AUTOMATIC: BLOCKED
RELEASE: NO-GO
```

## Historical evidence references
- `06_EVIDENCE/KA_INDEPENDENT_STATIC_REVIEW_KAST01_04_20261015.md`
- `06_EVIDENCE/KA_NU_FOLLOWUP_KAST01_04_STATIC_REVIEW_20261015.md`
- `06_EVIDENCE/NU_STATIC_REVIEW_SOURCE_TRANSFER_20261015_0834.md`
- `06_EVIDENCE/NU_FINDING_REMEDIATION_F1_F3_F7_F8_20261015_0840.md`
