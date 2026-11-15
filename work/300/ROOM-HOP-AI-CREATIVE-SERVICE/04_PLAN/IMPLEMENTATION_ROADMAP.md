# W300 — IMPLEMENTATION ROADMAP / KẾ HOẠCH TRIỂN KHAI

## Phase 01_DISCOVER — current
1. Confirm scope and public-access direction — DONE by Vinh.
2. Inspect ROOM-HOP gateway/runtime/storage capabilities — BLOCKED pending stable Sandbox/MCP 8030 access.
3. Collect independent architecture reviews from Ka, Cla, Kha, Go and QE — PENDING.
4. Reconcile review opinions into final DOC-034 — PENDING.
5. Obtain Vinh approval of final architecture — PENDING.

## Phase 02_DESIGN
1. Finalize public MCP contract and tool schemas.
2. Define authentication/onboarding, tenant isolation and authorization.
3. Define asynchronous job lifecycle, idempotency, retries, cancellation and job ownership.
4. Define provider adapter interface for image/video.
5. Define storage, asset delivery, retention and deletion policy.
6. Define cost ledger, quotas, abuse protection and customer tiers.
7. Define quality checks, moderation, audit and operational monitoring.

## Phase 03_BUILD — gated
1. Build isolated public gateway only after architecture/security approval.
2. Implement image pipeline and verify against acceptance criteria.
3. Implement video pipeline and verify asynchronous lifecycle.
4. Connect storage/delivery and customer project/job persistence.
5. Integrate auth, quota/cost controls and audit.
6. Keep internal ROOM-HOP Core, Runtime, Sandbox and Build MCP inaccessible from customer routes.

## Phase 04_VERIFY
- Contract tests, unit/integration tests, tenant isolation tests, security tests, abuse/cost tests, failure/retry/idempotency tests, image/video output quality tests, independent QE.
- Each test result must be recorded in DOC-035 with method, evidence and PASS/FAIL/BLOCKED.

## Phase 05_RELEASE
- Public release only after gates G0–G8, operational readiness and Vinh's explicit release approval.

## Current gates
- G0 Scope: USER-CONFIRMED.
- G1 Architecture: PENDING.
- G2 Security: PENDING.
- G3 MCP contract: PENDING.
- G4 Image pipeline: NOT BUILT.
- G5 Video pipeline: NOT BUILT.
- G6 QE: NOT RUN.
- G7 Operations/cost: NOT READY.
- G8 Public release: NOT APPROVED.

## UI prototype
The Lovable UI snapshot is a demo-only front-end shell. It may be refined independently as a visual prototype, but it does not close any production gate above.
