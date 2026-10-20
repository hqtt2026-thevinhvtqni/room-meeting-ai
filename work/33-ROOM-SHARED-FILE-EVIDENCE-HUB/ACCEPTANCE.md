# Work 33 — Acceptance Criteria

No criterion is PASS until its evidence is recorded and reviewable.

| ID | Criterion | Required evidence | Initial status |
|---|---|---|---|
| W33-AC-01 | Relevant Work 24/28/30 tools and contracts are identified | Paths, tool schemas, and source references | PENDING |
| W33-AC-02 | Empty `sandbox_read` response is reproduced or disproved | Raw request/response and timestamp | BLOCKED |
| W33-AC-03 | Root cause is traced to a specific layer | Call chain and source-backed explanation | PENDING |
| W33-AC-04 | Shared-file contract is documented | API/tool contract and access policy | PENDING |
| W33-AC-05 | A real test file can be stored and retrieved | Exact write/read responses and content comparison | PENDING |
| W33-AC-06 | Content integrity is verified | SHA-256 before and after read | PENDING |
| W33-AC-07 | Xu, Vi, An, and Ka can read the same authorized file | Per-agent identity, result, and timestamp | PENDING |
| W33-AC-08 | Negative cases are tested | Missing file, denied access, invalid path, empty file, and binary handling as applicable | PENDING |
| W33-AC-09 | Evidence and handoff are complete | Work log, artifacts, test results, and commit SHA | PENDING |

## Status semantics
- **DONE:** The stated task or artifact has been completed.
- **PASS:** Acceptance criteria are met with inspectable evidence.
- **BLOCKED:** Progress depends on an unresolved issue or unavailable prerequisite.
- **PENDING:** Not yet executed or not yet assessed.
- **DECISION:** Requires an explicit decision or approval from Vinh.

A directory listing alone is not evidence that file content is readable. A successful write response alone is not evidence that stored content can be retrieved correctly.
