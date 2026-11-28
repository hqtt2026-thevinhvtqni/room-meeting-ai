# WORK 05 — SANDBOX AUTONOMOUS BUILD RULE v0.1

Status: ACTIVE
Scope: Work 05 / Sandbox execution
Authority: Vinh
Date: 2026-10-05

## 1. Purpose

Work 05 Sandbox is an autonomous AI BUILD ZONE.

The objective is not to require Vinh to pre-approve implementation details. The objective is to prove that an AI Runner can receive a Goal and independently turn it into a working product with test, QE, recovery, verification, and evidence.

## 2. AI autonomy

Within the Sandbox boundary, the AI Runner MAY independently:

- research and compare approaches;
- choose implementation technologies;
- design architecture and internal data models;
- create and modify source code;
- install required dependencies;
- create local/mock services and test environments;
- run builds and tests;
- diagnose failures;
- repair defects;
- perform bounded retries/recovery;
- run QE and final verification;
- document decisions and evidence;
- release the resulting Work artifact when acceptance criteria are met.

Implementation decisions do not require a separate Vinh approval merely because they are architectural or technical choices inside the Sandbox.

## 3. Product-first completion

The primary completion criterion is:

WORKING PRODUCT + E2E EVIDENCE.

DONE requires, as applicable:

- requested functionality implemented;
- product/service actually runnable;
- tests executed;
- QE/validation completed;
- failures classified and recovered or explicitly blocked;
- evidence preserved;
- final result reported truthfully.

A recommendation is not completion. A design document is not completion. A successful mock is not automatically completion of a real external integration.

## 4. ROOM-HOP boundary

Autonomy ends at the ROOM-HOP system boundary.

AI must not:

- create or replace a second Core;
- bypass Core :8000 as the ROOM-HOP source of truth;
- bypass MCP/interface boundaries where those boundaries are required;
- modify ROOM-HOP governance or security boundaries without authorization;
- claim external execution that did not actually occur;
- expose or fabricate credentials/secrets.

Sandbox autonomy is deliberately compatible with ROOM-HOP governance.

## 5. External dependency handling

If an external dependency is unavailable, the AI Runner MUST:

1. continue all work that can be completed safely inside the Sandbox;
2. build mocks/stubs/adapters where useful;
3. test the product boundary that can be tested;
4. preserve evidence;
5. identify the exact external dependency that remains;
6. stop only when further progress genuinely requires crossing an unavailable boundary.

The absence of a credential, service, account, or production environment is an ENVIRONMENT BLOCKER, not a reason to ask Vinh to approve ordinary implementation choices.

## 6. Vinh Gate

Vinh Gate is reserved for decisions that actually require Vinh's authority, including:

- changing ROOM-HOP core principles/boundaries;
- destructive or irreversible actions outside the Sandbox;
- access/security authorization that the AI does not possess;
- business/policy decisions that cannot be inferred from the Goal;
- material unresolved conflicts where no evidence-based safe choice exists.

Vinh Gate is NOT a general implementation approval gate.

## 7. Runner behavior

The Runner should continue from the latest valid checkpoint.

It must NOT restart the entire Work merely because a later phase is blocked.

Expected recovery loop:

FAIL → CLASSIFY → PRESERVE EVIDENCE → DIAGNOSE → REPAIR → BOUNDED RETRY → VERIFY → CONTINUE / BLOCK

## 8. Success criterion for Work 05

Work 05 is successful when the reusable AI E2E process has demonstrated that an AI Runner can autonomously build and validate a real Work product inside the Sandbox while preserving the ROOM-HOP boundary.

