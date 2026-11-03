# Release Policy Draft — Not Active

Work 32 is in survey/design only. No production release or deployment is authorized.

Future release requirements: Vinh approval; exact reviewed commit; required gates PASS or explicit approved BLOCKED disposition; reviewer checks diff, dependencies, permissions, secrets and artifacts; separately documented deployment target; tested rollback/recovery; post-release evidence.

Prohibited now: auto-deploy, auto-merge, AI-controlled commit/push, PC or live-service changes during survey, and treating a green workflow as sufficient without reviewing evidence.

## CI evidence and CD gate update — 2026-11-04

CI and Auto E2E are operational on the Work branch. Exact-code run `41719444619` passed 157 bounded unit tests and 38 Auto E2E tests (one warning). Workflow artifacts are retained for 14 days and action dependencies are pinned to audited commit SHAs.

The deployment policy remains inactive. Before any CD execution, the release owner must identify and attest the staging/VPS target, document the service/runtime and deployment path, configure a protected environment with human approval, establish least-privilege deployment credentials and host trust, define health checks, and demonstrate rollback. Do not fabricate a host, deploy command, secret, health endpoint, or successful deployment result. No production deployment is authorized by the CI pass.
