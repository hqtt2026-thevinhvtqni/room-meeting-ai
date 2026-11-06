# DOC-005 — IMPLEMENTATION ROADMAP / KẾ HOẠCH TRIỂN KHAI

## Phase 0 — Intake and discovery
- Verify Work Entry Gate G0/G1 against Work 70.
- Identify event sources, consumers, Core authority contracts and current dispatch capabilities.
- Inventory existing schedulers, webhook listeners, queue/storage services to avoid duplicate infrastructure.
- Deliver: discovery evidence, dependency map, risks and decisions.

## Phase 1 — Define
- Approve trigger taxonomy, schema, lifecycle and acceptance criteria.
- Define permission matrix, human approval classes, retry/dedupe/replay semantics.
- Define SLO, retention, privacy and operational ownership.
- Deliver: approved requirements and decision log.

## Phase 2 — Architect
- Produce deployment, data, API, security, failure and observability designs.
- Validate Core identity/authorization/audit integration and AI dispatch transport.
- Complete threat model and ADRs.
- Deliver: reviewed architecture and contracts.

## Phase 3 — Build
WP-76-01 Registry + schema/versioning.
WP-76-02 Event gateway + authentication/normalization.
WP-76-03 Scheduler + time trigger.
WP-76-04 Condition evaluator + typed expression.
WP-76-05 Policy adapter + approval workflow.
WP-76-06 Orchestrator + dedupe/cooldown/retry.
WP-76-07 AI dispatcher adapter (only verified transport).
WP-76-08 Audit/evidence store.
WP-76-09 Read-only dashboard and operational controls.

## Phase 4 — Verify
- Unit, contract, integration, security, fault-injection, load and mobile/desktop UI tests.
- Test duplicate/replayed/late/out-of-order events; timezone boundaries; queue outage; audit outage; revoked identity; policy DENY; kill switch.
- Independent QE and evidence review.

## Phase 5 — Accept, release and operate
- Vinh acceptance after evidence review.
- Staged rollout: dry-run → shadow → limited allow-listed actions → controlled production.
- Runbooks, alerting, rollback, backup/restore, on-call and periodic access review.

## Gate discipline
No phase advances solely because documents exist. Each predecessor gate requires criteria, owner decision and verifiable evidence. Build is not authorized by this roadmap alone.
