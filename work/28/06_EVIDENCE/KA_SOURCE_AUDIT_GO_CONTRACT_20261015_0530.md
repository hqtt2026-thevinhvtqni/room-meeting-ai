# KA — Independent Re-audit of GO Contract v1.2.1 — 2026-10-15 05:30 UTC+07

## Decision
The two findings from audit 05:20 are addressed in source by inspection. Contract acceptance remains BLOCKED pending one JSON-validation hardening item and actual test execution. This is a source review, not a runtime/test PASS.

## Evidence inspected
Read directly from Work 28 sandbox:
- `MCP-8020-TOOLING-PLATFORM/04_CODE/tool_contracts.py`
- `MCP-8020-TOOLING-PLATFORM/05_TEST/test_tool_contracts.py`
- `06_EVIDENCE/GO_BUILD_CHECKPOINT_CONTRACT_HARDENING_20261015_0525.md`
- Sandbox listing confirms checkpoint 05:25 exists in root `06_EVIDENCE/`. Earlier lookup used the wrong prefixed path; corrected.

## Findings closed by source inspection
### KA-AUDIT-28-01 — to_dict / MappingProxyType
CLOSED AT SOURCE-REVIEW LEVEL. `to_dict()` no longer calls `dataclasses.asdict()`; it constructs fields explicitly and thaws `test_summary`. Regression test checks `json.dumps(payload)`. Test has not been executed.

### KA-AUDIT-28-02 — nested immutability
CLOSED AT SOURCE-REVIEW LEVEL for supported dict/list/tuple structures. `_deep_freeze()` recursively converts mappings to `MappingProxyType` and sequences to tuples; tests attempt nested mutation and verify original nested input mutation does not change the frozen copy. Test has not been executed.

### Evidence path
The 05:25 checkpoint exists at the root evidence path claimed by Go and was read successfully. It records 0 tests executed and no hash values.

## Remaining source issue
### KA-AUDIT-28-07 — JSON-compatible summary values are not fully validated (BLOCKER for strict JSON contract)
`_deep_freeze()` accepts any Mapping keys without checking they are strings and accepts all floats including NaN and positive/negative infinity. Those are not strict JSON values; after `_thaw()`, `json.dumps(..., allow_nan=False)` may fail, and non-string keys may serialize inconsistently or fail for some key types. Add tests for non-string nested keys and non-finite floats, then reject them (e.g. require string mapping keys and finite floats). Also consider whether the public `result: Any` field needs a documented serialization contract; `to_dict()` returns it without normalization. Do not silently describe all of `to_dict()` as universally JSON-safe unless its `result` field is constrained or deliberately documented as caller-owned.

## SHA-256 status
The connector provides text read/write/list actions but no hash action was discovered. I cannot truthfully claim SHA-256 values for the exact sandbox bytes through the currently exposed tools. This is a connector capability limitation, not a Python test-runner limitation. Use an approved external hash facility on the exact sandbox files when available; do not invent hashes.

## Acceptance status
- v1.2.1 source: IMPROVED; two prior audit findings closed by inspection.
- Contract source review: BLOCKED on KA-AUDIT-28-07.
- Unit tests: BLOCKED / NOT RUN (0 reported).
- Runtime identity / trusted principal / WorkContext / OS isolation: BLOCKED.
- Live MCP tools/list / live E2E: BLOCKED / NOT RUN.
- Release: NO-GO.

## Required next checkpoint for Go
1. Validate summary keys and finite float values; add regression tests.
2. Clarify serialization rules for `result: Any`.
3. Read back source, tests, and checkpoint.
4. Preserve actual test count = 0 until an approved runner produces real output.
5. Keep all runtime/security/live-E2E gates blocked until independently evidenced.

— Ka, CSA / Work 28 Coordinator (source review; not a cryptographic signature)
