# GO BUILD CHECKPOINT — Contract Hardening v1.2.0
**Go — Builder / Implementer**  
**15/10/2026 05:18 UTC+07**

## A. Source changes made

### File: `MCP-8020-TOOLING-PLATFORM/04_CODE/tool_contracts.py`
- Bumped `CONTRACT_VERSION` **1.1.0 → 1.2.0**
- **N01**: `execution_operation` only allowed when `operation_kind=EXECUTION`; execution-only fields (`run_id`, `exit_code`, `source_sha256`, `test_summary`) rejected on non-EXECUTION results.
- **N03**: `exit_code` must be real `int` (reject `bool`/`float`); counters must be real `int` (reject `bool`).
- **N05**: `test_summary` is deep-copied and frozen with `MappingProxyType` so post-construction mutation is impossible.
- **N06**: Expanded `_PROTECTED_COMPONENTS` (`.env.local`, `.envrc`, `.git-credentials`, `.npmrc`, `.netrc`, `.pypirc`, `id_rsa`, `credentials`, `desktop.ini`…); reject literal backslash; reject additional Unicode separators (Zl/Zp, U+1680).
- **N04**: `result_from_exception` maps both `PermissionError` and `FileNotFoundError` to `NOT_FOUND` (no existence oracle).
- Added `validate_run_id()` enforcing `run-<32 hex>` shape.
- Explicit documentation that this module does **not** enforce server-side principal / WorkContext / isolation.

### File: `MCP-8020-TOOLING-PLATFORM/05_TEST/test_tool_contracts.py`
- Updated all tests for v1.2.0 contract.
- Added / strengthened tests for:
  - `test_contract_version_is_1_2_0`
  - `test_execution_operation_only_with_execution` (N01)
  - `test_execution_fields_rejected_on_non_execution` (N01)
  - `test_test_summary_is_immutable` (N05)
  - `test_execution_bool_exit_code_cannot_claim_pass` (N03)
  - `test_rejects_literal_backslash` (N06)
  - Expanded protected-name and Unicode separator rejection
  - `validate_run_id` shape checks
  - Updated `result_from_exception` expectations (N04)

## B. Tests added
- 6 new test methods + expanded existing ones covering N01, N03, N04, N05, N06.
- All previous 17 assertions preserved or strengthened (no weakening).

## C. Tests actually executed
**BLOCKED** — no approved Python runner available in the current roomhop connector surface.  
No `python_run` / local unittest execution was performed in this session.

## D. Tests not executed and why
Canonical command that **must** be run by an approved runner:
```bash
python -m unittest discover -s 05_TEST -t . -v
```
Expected (once runner available): all tests PASS, exit code 0, tests_run ≥ 20.

## E. Remaining runtime / security blockers
| Finding | Status after this change |
|---------|--------------------------|
| N01 forged PASS via wrong operation_kind | **Closed at contract level** |
| N02 self-attested test summary | Partially mitigated (immutable); full trust requires external collector |
| N03 loose counters / bool exit_code | **Closed** |
| N04 exception mapping / existence oracle | **Closed at contract level** |
| N05 mutable test_summary | **Closed** |
| N06 path validator gaps | **Improved**; full containment still requires filesystem adapter |
| N07 source hash only covers entry_path | **Still open** (server/adapter responsibility) |
| N08 alternate execution host reachable | **Still open** (PC/runtime responsibility) |
| Server-side principal / WorkContext | **Still open** — pure contract cannot enforce |
| OS isolation / process-tree cleanup | **Still open** |
| Live MCP tools/list + PID binding | **Still PARTIAL / BLOCKED** |

## Guardrails respected
- No python_run enabled
- No live registry mutation
- No PC / GitHub write
- No sync / merge / release
- No claim of live E2E PASS

## Next action
1. When approved runner becomes available → run the canonical unittest command and record exit code + counters.
2. Continue with next independent build slice: request schema + server-side authorization interface stubs (still pure / no runtime).
3. Cla to begin security engineering remediation in parallel.

---
Go — Builder / Implementer  
15/10/2026 05:18 UTC+07
