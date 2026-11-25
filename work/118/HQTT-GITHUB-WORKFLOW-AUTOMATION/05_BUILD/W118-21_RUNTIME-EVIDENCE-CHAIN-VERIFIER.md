# W118-21 — Runtime Evidence Chain Verifier

- **Work:** W118 — HQTT GitHub Workflow Automation
- **State:** IMPLEMENTED ON FEATURE BRANCH — CI PENDING
- **Code:** `scripts/w118/evidence_chain.py`
- **Tests:** `tests/w118/test_evidence_chain.py`
- **JSON Schema:** `schemas/w118/evidence-chain.schema.json` (W118 normalized envelope only; not W70's schema).

## 1. Purpose

Validate a normalized evidence bundle across the five W118 lifecycle stages:
1. Core Task snapshot read
2. W102 Assignment/ACK
3. W14 execution
4. W33 evidence ingestion
5. W70 evidence register read-back

This is a W118-side evidence consistency checker. It does not create or replace any of the five systems, their APIs, or the W70 Evidence Register schema.

## 2. Checks performed

- Exactly five receipts in the required order.
- Same Work ID, Core Task ID, correlation ID and full source Git SHA across every stage.
- Unique receipt IDs and a strict previous-receipt chain.
- Stage-specific outcome values; a generic `PASS` string is not accepted as a receipt outcome.
- Issuer principal, authority reference and attestation reference are present.
- ISO-8601 timestamps include a timezone and are chronological.
- W33 ingested artifact SHA-256 matches W14 execution artifact SHA-256.
- W70 read-back artifact SHA-256 matches W33 ingested artifact SHA-256.

The receipt envelope is an internal W118 normalization format. Each service owner must map its real, approved receipt schema into this envelope; W118 does not assert that these field names exist in external APIs.

## 3. Run

```bash
python scripts/w118/evidence_chain.py --bundle path/to/normalized-evidence-chain.json
```

A structurally complete bundle returns `STRUCTURALLY_COMPLETE_UNAUTHENTICATED`. Any missing or inconsistent receipt returns `BLOCKED`.

## 4. Non-claims and security boundary

The verifier does not cryptographically authenticate issuers, authority references or attestation references. It does not contact endpoints, load secrets, execute Work, write W33, or read W70. It always returns:
- `runtime_e2e_pass: false`
- `authenticity_verified: false`
- `acceptance_granted: false`

Therefore, structural completeness is not Runtime E2E PASS. A future cryptographic attestation verifier and authoritative service read-back remain required before the chain can be accepted.
