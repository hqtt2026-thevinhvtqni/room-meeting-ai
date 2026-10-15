# Work 28 — WP2 isolated slice report
Date: 2026-10-15 (+07)
Status: SOURCE REVIEW DONE; LOCAL SNAPSHOT TEST PASS; APPROVED RUNNER BLOCKED; LIVE E2E BLOCKED; RELEASE NO-GO

## Scope and guardrails
- Read Work 28 manifest, original requirement, latest status reconciliation, next execution assignment, contract audit, tool-gap decision, current contract source, current test source and test plan through MCP 8020 Sandbox.
- No PC/GitHub write, listener restart, live MCP registry mutation, deployment, merge, release or `python_run` enablement was performed.
- The test run below used a temporary local copy reconstructed from MCP readback. It is **LOCAL SNAPSHOT TEST** only and is not an approved runner, not canonical PC evidence, and not live MCP-to-Core E2E evidence.

## Changed files
- No Work 28 source/test file was changed in this slice. The existing readback already contains contract v1.3.0 and the expanded regression suite.
- Added this evidence report only.

## Source review findings
1. `04_CODE/tool_contracts.py` declares CONTRACT_VERSION `1.3.0` and explicitly states it is pure contract/shape validation, not authentication, authorization, filesystem containment, execution, evidence storage or runtime attestation.
2. `TrustedPrincipal` and `WorkContext` are fail-closed data-shape contracts, but object construction cannot prove transport authenticity or Core authorization. The adapter/Core must derive them from trusted server-side context.
3. Path validation rejects traversal, absolute/drive/UNC paths, ADS syntax, control/format/confusable characters, Windows reserved names, option-like components and protected metadata names. This remains lexical validation only; symlink/TOCTOU/filesystem containment is still an adapter/runtime gate.
4. Write and append payloads are bounded by UTF-8 byte count. Read/list limits are bounded request parameters only; actual streaming read/list enforcement is absent from this pure module and remains BLOCKED pending adapter implementation and tests.
5. Execution PASS validation requires explicit execution operation, run ID, exit code 0, evidence reference, source SHA-256 and a valid RUN_TESTS counter set. This is shape validation and does not establish that evidence or runtime results are authentic.

## Local snapshot test evidence
- Exact command: `python3 -m unittest discover -s 05_TEST -t .`
- Temporary working directory: `/tmp/work28-check`
- Interpreter: Python 3.12.3
- Result: **31 tests run, OK, exit code 0**
- Failures: 0
- Errors: 0
- Skipped: 0
- Source snapshot SHA-256:
  - `04_CODE/tool_contracts.py`: `00578cd7a0c65a9cbc4b97b873f5bf0dc6b08709138a6ee620fe482dbe111582`
  - `05_TEST/test_tool_contracts.py`: `d177ae0af5cea1e54790de09ee42c56a6e9a52a7ec03d137629458cb76a8cb81`
- Provenance: files reconstructed from successful MCP `sandbox_read` responses at 2026-10-15 07:40 (+07); no Git revision was available for the temporary copy.

## Gate separation
| Evidence class | Result | Meaning |
|---|---|---|
| SOURCE REVIEW | DONE | Current contract/test source was read and reviewed through MCP 8020. |
| LOCAL SNAPSHOT TEST | PASS | 31 regression tests pass on the temporary readback copy. |
| APPROVED RUNNER | BLOCKED | No approved canonical runner or PC runtime identity was available in this session. |
| LIVE MCP `tools/list` binding | PARTIAL/BLOCKED | Historical supplied evidence reports 18 tools, but same-endpoint before/after plus exact loaded revision is not independently captured here. |
| MCP → Core → authorized capability → evidence readback | BLOCKED | No live authorization trace, protected evidence proof or runtime execution evidence. |
| Release / closure | NO-GO | Work remains ACTIVE / NOT LOCKED. |

## Remaining blockers and actionable handoff
1. Run the same canonical command in the approved runner from the real Work 28 root and capture interpreter, working directory, source revision, both source hashes, raw stdout/stderr, exit code and counters.
2. Implement/test adapter-enforced bounded read and bounded list iteration; prove exact-limit and over-limit behavior without unbounded materialization.
3. Identify and evidence the active Core authorization route and trusted principal/WorkContext derivation for every protected Sandbox operation.
4. Capture raw live `tools/list` from the PC :8020 endpoint and bind it to listener PID, entrypoint, loaded revision and source hashes.
5. Keep execution, `python_run`, registry mutation, deployment, sync, merge and release blocked until security review and live E2E gates pass.

## Decision
The isolated contract/test slice is complete at the evidence level available in this Sandbox: **local snapshot tests PASS**. This does not complete Work 28 acceptance. Work 28 stays **ACTIVE / NOT LOCKED**, live E2E **BLOCKED**, release **NO-GO**.
