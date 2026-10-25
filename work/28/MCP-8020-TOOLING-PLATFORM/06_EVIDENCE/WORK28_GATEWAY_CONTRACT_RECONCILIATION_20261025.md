# Work 28 gateway contract reconciliation

Date: 2026-10-25
Reviewer: Xu (AI-01)
Scope: static source review only; no runtime validation.

## Finding
The execution gateway interface is inconsistent with the strict execution contract. The gateway currently accepts script/command and args and emits RUN_COMMAND. The strict contract requires entry_path and expected_source_sha256, permits RUN_SCRIPT or RUN_TESTS, and rejects inline code and arbitrary command arguments.

The service currently returns NOT_IMPLEMENTED for tools whose catalog status is NOT_IMPLEMENTED before provider dispatch. Keep that status and fail-closed behavior unchanged.

## Required next steps
1. Align gateway inputs and requests to the strict hash-bound contract.
2. Add tests for request shape, path/hash/operation validation, Work authorization, and rejection before submission.
3. Verify lifecycle authorization for status, result, cancellation, artifacts, evidence, and handoff.
4. Obtain CI run evidence, then validate against the authorized canonical runtime and perform end-to-end tests.
5. Only after all gates pass may a separately reviewed change bind the gateway and change catalog status.

## Status
Static mismatch confirmed. Runtime not wired. Tests not run in this session. No PASS claimed.