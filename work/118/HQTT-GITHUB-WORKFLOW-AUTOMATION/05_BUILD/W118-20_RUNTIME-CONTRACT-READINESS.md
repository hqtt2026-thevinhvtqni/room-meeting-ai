# W118-20 — Runtime Contract Readiness

- **Work:** W118 — HQTT GitHub Workflow Automation
- **State:** IMPLEMENTED ON FEATURE BRANCH — CI PENDING
- **Purpose:** Validate owner-supplied integration contracts before any live runtime preflight.
- **Code:** `scripts/w118/runtime_contract.py`
- **Tests:** `tests/w118/test_runtime_contract.py`

## 1. Scope and authority

The validator is a static, fail-closed intake gate. It does not:
- discover or guess Core/W102/W14/W33/W70 endpoints;
- contact services, load credentials, dispatch work or mutate runtime state;
- grant authority or treat a proposed contract as approved;
- claim Runtime PASS, Evidence verification, Work acceptance or release.

A valid result is only `READY_FOR_RUNTIME_PREFLIGHT`. It means the submitted contract bundle is structurally complete and marked approved by its accountable owners. Service availability, principal authentication, authorization, real execution, W33 receipt and W70 read-back remain separate gates.

## 2. Required canonical components

| Component ID | Required operations |
|---|---|
| `core_task_authority` | `read_task` |
| `w102_assignment_ack` | `authorize_assignment`, `acknowledge_assignment` |
| `w14_execution_host` | `execute_work` |
| `w33_evidence_ingress` | `ingest_evidence` |
| `w70_evidence_register` | `register_evidence`, `read_evidence` |

Operation names are W118 integration roles, not assertions about deployed endpoint paths or methods. Each accountable owner must supply the exact method, service-relative path, request/response schema references and side-effect classification.

## 3. Owner-supplied contract fields

Each component entry must contain:
- `owner`, `contract_id`, `contract_version`, `source_revision`, `contract_ref`;
- `approved: true` (a proposal or unapproved document remains BLOCKED);
- `base_url` (HTTPS outside loopback development);
- `auth.mode` from `BEARER_REF`, `MTLS`, `SIGNED_REQUEST`, `WORKLOAD_IDENTITY`;
- `auth.credential_ref` pointing to a secret manager entry. Never put raw tokens, passwords, keys or authorization headers in this file;
- all required `operations`, each with `method`, `path`, `request_schema_ref`, `response_schema_ref`, and `side_effect`;
- `evidence.correlation_id_field` and `evidence.receipt_id_field`, defined by the owner.

The contract must preserve one correlation ID across Core → W102 → W14 → W33 → W70 and expose a receipt identifier at each evidence boundary. Exact field names are owner-defined, not inferred by W118.

## 4. Run locally or in CI

```bash
python scripts/w118/runtime_contract.py --contract path/to/owner-approved-runtime-contract.json
```

Exit code:
- `0`: `READY_FOR_RUNTIME_PREFLIGHT` only.
- `2`: `BLOCKED`; inspect the machine-readable `errors` and `missing_components`.

The report always includes:
- `runtime_execution_performed: false`
- `runtime_pass: false`
- `authority_granted: false`

The validator has no HTTP client and makes no network calls. Unit tests use in-memory fixtures only and do not constitute service integration evidence.

## 5. Security and negative cases

The test suite covers missing dependencies, unapproved contracts, missing operations/schema references, plaintext external endpoints, credential leakage, missing secret references, path traversal, unknown components and malformed input. All failures return BLOCKED.

## 6. Next integration gates

1. Each owner supplies an approved, revision-pinned contract bundle and safe non-secret credential reference.
2. Ka independently reviews contract provenance and security fields.
3. W118 adds a separately authorized, read-only preflight adapter only after endpoint/auth semantics are owner-approved.
4. W14 execution remains a separately controlled mutation gate; no execution is attempted during preflight.
5. W33 returns an authenticated ingestion receipt; W70 performs authoritative read-back and integrity verification.
6. A controlled end-to-end run uses one correlation ID and records positive and negative outcomes. Only then can Runtime Auto E2E be assessed.

**Current limitation:** no owner-approved runtime bundle is present in this commit. The five dependent runtime gates remain BLOCKED / NOT VERIFIED.
