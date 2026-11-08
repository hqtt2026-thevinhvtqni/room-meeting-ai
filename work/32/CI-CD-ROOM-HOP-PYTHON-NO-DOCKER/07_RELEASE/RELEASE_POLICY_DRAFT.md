# Release Policy Draft — Not Active

Work 32 CI implementation and exact-SHA validation are operational on its feature branch. This policy remains NOT ACTIVE for release/deployment authorization. CI acceptance or artifact creation does not authorize merge, staging, production deployment or a RELEASED claim. No production release or deployment is authorized.

Future release requirements: Vinh approval; exact reviewed commit; required gates PASS or explicit approved BLOCKED disposition; reviewer checks diff, dependencies, permissions, secrets and artifacts; separately documented deployment target; tested rollback/recovery; post-release evidence.

Prohibited now: auto-deploy, auto-merge, AI-controlled commit/push, PC or live-service changes during survey, and treating a green workflow as sufficient without reviewing evidence.

## CI evidence and CD gate update — 2026-11-04

CI and Auto E2E are operational on the Work branch. Exact-code run `41719444619` passed 157 bounded unit tests and 38 Auto E2E tests (one warning). Workflow artifacts are retained for 14 days and action dependencies are pinned to audited commit SHAs.

The deployment policy remains inactive. Before any CD execution, the release owner must identify and attest the staging/VPS target, document the service/runtime and deployment path, configure a protected environment with human approval, establish least-privilege deployment credentials and host trust, define health checks, and demonstrate rollback. Do not fabricate a host, deploy command, secret, health endpoint, or successful deployment result. No production deployment is authorized by the CI pass.


## Status reconciliation — 2026-11-08

- Exact-SHA CI acceptance: PASS on Work32 feature branch; latest full validated implementation SHA at this checkpoint: `a216f38d734377d923b7860c5f45c2521f54a7e8` (Run #233 / `42460156145`, SUCCESS).
- Windows Browser Adapter + MCP Public V1 stdio handoff/readback: PASS; disposable fixture and exact process cleanup verified.
- Immutable source artifact and artifact-level test: PASS. The artifact remains a CI release candidate only.
- Main integration: BLOCKED; branch diverges from current main and requires independent review and a clean integration strategy.
- Dashboard→Core browser integration: BLOCKED / NOT RUN.
- CD/staging/production: BLOCKED / NOT RUN. No attested target, protected approval environment, deployment credentials, operational health check or tested rollback evidence.
- G7 RELEASE: NOT READY / NOT AUTHORIZED. Product Owner authority remains Vinh under DOC-050. This document remains a draft and does not create approval.
- Work 32 status: ACTIVE — NOT RELEASED.
