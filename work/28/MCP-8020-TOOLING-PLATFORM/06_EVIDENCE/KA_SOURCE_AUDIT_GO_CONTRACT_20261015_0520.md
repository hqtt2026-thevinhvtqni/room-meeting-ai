# KA — Independent Source Audit of GO Checkpoint 2026-10-15 05:18
## Decision
BUILD CONTINUES. Contract v1.2.0 is NOT ACCEPTED yet. Source was read directly from Work 28 sandbox. Tests have NOT been executed. This audit does not authorize runtime, registry, PC, GitHub, sync, merge, or release changes.

## Confirmed source changes
- `04_CODE/tool_contracts.py` declares CONTRACT_VERSION 1.2.0.
- `05_TEST/test_tool_contracts.py` contains expanded tests for execution fields, run IDs, counters, path validation, summary mutation and exception mapping.
- Source reads succeeded for both files.
- The reported checkpoint evidence path `06_EVIDENCE/GO_BUILD_CHECKPOINT_CONTRACT_HARDENING_20261015_0518.md` could NOT be read at that exact path (FileNotFoundError). Locate/create the evidence file at the canonical path and verify readback.

## Blocking source findings — fix before claiming this slice complete
### KA-AUDIT-28-01 — to_dict likely fails with MappingProxyType (BLOCKER)
`ToolResult.to_dict()` calls `dataclasses.asdict(self)` before its custom `test_summary` conversion. `asdict` deep-copies non-dataclass values; `MappingProxyType` is not deepcopy/pickle-compatible in normal Python and is expected to raise TypeError. Add a regression test constructing a valid EXECUTION/RUN_TESTS PASS result and asserting `to_dict()` returns a serializable dict. Implement explicit safe serialization or another immutable representation that supports serialization. Do not merely remove the immutability guarantee.
### KA-AUDIT-28-02 — summary is not deeply immutable (BLOCKER for N05 claim)
`MappingProxyType(dict(self.test_summary))` only freezes the outer mapping. Nested lists/dicts/sets remain mutable through references stored inside it. Recursively copy/freeze allowed values or validate that only scalar JSON-compatible values are accepted. Add a nested-mutation regression test.
### KA-AUDIT-28-03 — error mapping test label is broader than implementation
`PermissionError` and `FileNotFoundError` are both mapped to NOT_FOUND. This may be intentional to reduce existence oracle leakage, but tests must document the security tradeoff; adapter-level behavior must not expose the hidden cause elsewhere. Do not claim this closes server-side authorization.
### KA-AUDIT-28-04 — verify test import/runner path
The test uses `importlib.import_module("04_CODE.tool_contracts")`. Confirm this works under the declared root command in the actual project layout when an approved runner becomes available. Not executed in this checkpoint.
### KA-AUDIT-28-05 — source digest still missing
SHA-256 is not dependent on running tests. Use an approved hash facility on the exact two files; record paths, hashes, and timestamp. If the sandbox cannot hash, report that specific platform limitation, not “no Python runner”.
### KA-AUDIT-28-06 — request/schema/auth interface is not authorization
Any interface stubs must fail closed and explicitly distinguish validated request shape from authenticated principal, authorized WorkContext, and filesystem/runtime enforcement. No fake PASS or implied enforcement.

## Required next checkpoint
1. Fix KA-AUDIT-28-01 and 02 with regression tests.
2. Add tests for `to_dict()` and nested data mutation.
3. Read back both changed source files and the evidence report.
4. Record actual SHA-256 values if the approved platform supports hashing.
5. Report tests executed = 0 unless actual runner output exists; do not claim PASS.
6. Keep N07/N08, trusted principal/WorkContext, OS isolation, MCP tools/list, live E2E, and release gates BLOCKED/NO-GO until independent evidence closes them.

## Current acceptance
CONTRACT SOURCE REVIEW: BLOCKED (at least two concrete regressions require correction).
TEST EXECUTION: BLOCKED / NOT RUN.
LIVE E2E: BLOCKED / NOT RUN.
RELEASE: NO-GO.
— Ka, CSA / Work 28 Coordinator (review directive, not a cryptographic signature)
