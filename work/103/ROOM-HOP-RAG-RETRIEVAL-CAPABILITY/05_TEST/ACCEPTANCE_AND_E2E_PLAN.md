# Work 103 — Verification and E2E Acceptance Plan

## Local/unit gates
- [ ] Syntax compile of 04_CODE/rag_retrieval.py
- [ ] Run unittest/pytest for 05_TEST/test_rag_retrieval.py
- [ ] Verify deterministic ranking over a labeled query set.
- [ ] Measure precision@k, recall@k, no-answer accuracy, and response latency.
- [ ] Add malformed document, path traversal, Unicode/Vietnamese, large-file, duplicate and deletion/reindex tests.

## Integration gates
- [ ] Read Work 28 manifest/contracts and live MCP tool inventory.
- [ ] Trace the actual Core service and approved repository abstraction; do not wire MCP to storage directly.
- [ ] Add Core-owned service/API contract using existing project conventions.
- [ ] Add MCP schema + adapter only after Core contract is stable.
- [ ] Test source allowlisting and identity/authorization behavior.
- [ ] Live E2E: MCP :8020 -> Core :8000 -> retrieval service -> canonical source -> returned citation -> source readback.
- [ ] Negative E2E: unapproved scope denied, empty query rejected, no evidence abstains, injected document commands are not followed, secrets are not indexed.
- [ ] Record raw command, exit code, timestamp, environment, test report, and source/commit identity.

## Release gate
No DONE/PASS claim until all required gates have evidence. Sandbox artifact creation/readback is not a substitute for executed tests or live integration.
