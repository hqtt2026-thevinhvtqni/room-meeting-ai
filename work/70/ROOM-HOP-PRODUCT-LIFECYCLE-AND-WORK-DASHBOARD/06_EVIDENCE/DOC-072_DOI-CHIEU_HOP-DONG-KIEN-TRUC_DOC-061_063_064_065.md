# DOC-072 — ĐỐI CHIẾU HỢP ĐỒNG KIẾN TRÚC DOC-061 / DOC-063 / DOC-064 / DOC-065

- **Document ID:** DOC-072
- **Priority:** P0
- **Read order:** 72
- **Date:** 2026-11-02
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- **Status:** RECONCILIATION COMPLETE — DESIGN ONLY / NOT APPROVED / NOT IMPLEMENTED
- **Depends on:** DOC-004; DOC-005; DOC-010; DOC-011; DOC-035; DOC-054; DOC-057; DOC-061; DOC-063; DOC-064; DOC-065; DOC-066; DOC-071
- **Source baseline:** GitHub `hqtt2026-thevinhvtqni/room-meeting-ai`, branch `main`; source-code baseline for DOC-071 remains `9ab3b80a979c1952f0b2b45a168e8ea94d73d424`. Document blobs were fetched from current main during this reconciliation.
- **Execution boundary:** Documentation/source reconciliation only. No code, Core, API, database, permission, provider, adapter, runtime or branch mutation.

## 1. Purpose

Đối chiếu bốn lớp tài liệu để tránh:
- biến target architecture thành implementation fact;
- tạo nhiều nguồn authority hoặc nhiều Execution Host;
- dùng identity/dispatch receipt thay cho authorization;
- dùng delivery/ACK/progress/review thay cho Work/Gate transition;
- nhầm logical contract với API route hoặc storage đã tồn tại;
- mở BUILD khi G0/G1/G4 chưa đạt.

## 2. Source documents and current disposition

| Document | Scope | Current disposition | Does not prove |
|---|---|---|---|
| DOC-061 | Runtime/lifecycle/Core authority contract, state domains, Dashboard projection, logical Work command | DRAFT — source reconciliation complete / contract approval pending | Work API, deployed runtime, persistence, authorization enforcement, implementation approval |
| DOC-063 | Work Entry authorization, deny-to-recovery, server-side trust, audit, recovery/protected data separation, commit-time validity | DRAFT — design only / not approved / not implemented | Actual Core auth middleware, grant service, transaction boundary, recovery store, runtime enforcement |
| DOC-064 | Target Hybrid AI Dispatch architecture, adapter modes, session continuity, trust boundaries, lifecycle and rollout | DRAFT — target architecture / implementation not authorized | Native connector availability, private-session access, automated dispatch, live registry |
| DOC-065 | Provider-neutral logical assignment/dispatch/ACK/progress/result/review/event contract | DRAFT — contract proposal | API routes, database schema, live assignment, actual delivery or verified ACK |
| DOC-066 | Implementation and test plan for dispatch | DRAFT — planned / implementation not authorized / tests not run | Any dispatch execution, ACK, runtime test or permission grant |
| DOC-071 | Read-only Core runtime/persistence/owner trace | Source trace complete within inspected scope | Exhaustive proof that no external service/owner exists |

## 3. Layered target model — consistent interpretation

### 3.1 Core authority and Work lifecycle (DOC-061)

- Core is the intended authoritative boundary for authenticated principal, Work/WP state, version, authorization, persistence, audit and canonical evidence metadata — only after actual Core contracts are located and verified.
- Lifecycle Engine is a domain evaluator, not an authentication provider, permission issuer, authoritative store or bypass around Core.
- Dashboard is a read-only projection. A local snapshot must remain explicitly labeled; it cannot be presented as Core live.
- DOC-061 logical command/result fields are proposals, not approved route names or DTOs.

### 3.2 Work Entry authorization and deny recovery (DOC-063)

- Authorization is evaluated server-side from trusted principal and authoritative Work/WP/assignment/scope/gate/source revision.
- Caller-supplied `authorized=true`, actor/role, gate result or identity text is never sufficient.
- Recovery/Work Entry evidence scope is separate from Protected Product mutation scope. Permission to submit remediation evidence does not grant protected write.
- Authorization must still be valid at commit time; stale assignment, revocation, source revision or gate/WP version change must prevent mutation.
- Audit and protected mutation must be atomic or use an explicitly approved durable outbox/reconciliation protocol. No storage/transaction technology is selected by this design.
- These are design requirements only. DOC-071 has not identified an implementation of this Work-scoped boundary.

### 3.3 Hybrid dispatch control plane (DOC-064)

- Dispatch Orchestrator manages assignment readiness, dependency, capability evidence, idempotency and adapter selection; it is not a second lifecycle authority.
- Adapter Gateway performs transport/handoff only. It cannot approve acceptance, Work Gate or release.
- `SESSION_HANDOFF` produces a handoff packet; packet creation is not dispatch delivery. User submission requires separate receipt.
- `ROOM_MEETING_RELAY` is limited to verified Meeting context and does not prove access to private AI conversations.
- Native connector and API modes remain unavailable until capability, identity, target/session and cost/security requirements are verified.
- Core Work/Assignment/Evidence Registry remains conditional on an approved, real Core contract.

### 3.4 Logical dispatch contract (DOC-065)

- Assignment, dispatch attempt, transport status, ACK, progress, result, review and Work/Gate state are separate records/domains.
- `DELIVERED` requires provider/adapter delivery evidence; HTTP acceptance alone is insufficient unless the connector semantics prove delivery.
- `ACKNOWLEDGED` requires verified connector identity or a clearly labeled manual receipt; a typed AI ID is not identity proof.
- Result submission moves to review, not directly to DONE. Independent review and authorized closure are required.
- The sample JSON `status: READY` is illustrative only; it is not a live assignment and must not be copied into authoritative state.
- Contract route names are intentionally omitted pending Core owner mapping.

## 4. Contract dependency order

1. DOC-061 establishes state/authority/runtime boundaries and requires Core owner mapping.
2. DOC-063 refines the authorization enforcement point and adds recovery/protected-scope separation plus commit-time validity.
3. DOC-064 defines the dispatch architecture that must consume the verified authorization and assignment contracts; it cannot create an alternate authority.
4. DOC-065 defines logical payloads/events for DOC-064; it does not instantiate API routes or storage.
5. DOC-066 can plan implementation/test sequencing only after the source contract, owner, permission and gate prerequisites are satisfied.
6. DOC-071 is current bounded source evidence for the Core gap; it takes precedence over any target-design assumption when describing present implementation.

No contradiction requires changing DOC-004 or DOC-005. If any draft proposes a conflicting state name, route, gate alias or authority rule, the active canonical documents remain controlling until Vinh approves a formal decision.

## 5. Gate namespace and authority guard

- Lifecycle gates G0–G9 remain governed by DOC-004.
- Integration gates in DOC-054 retain their own document context.
- Work Entry criteria in DOC-057 retain their own policy context.
- DOC-060 namespace separation remains proposal-only. Do not silently alias the several G0/G4 labels or activate a new namespace.
- In DOC-063, reference to G4 as PLAN→BUILD is interpreted under DOC-004, not as permission from an Integration or Work Entry gate.
- G0/G1 remain NOT_READY; Lifecycle G4 remains NOT_READY / NOT PASS. No WP is authorized for BUILD by these drafts.

## 6. Runtime and implementation findings carried forward

DOC-071 and the latest DOC-061 source addenda establish a bounded source picture:
- Core entrypoints inspected compose Meeting/Identity capabilities; no Work/WP/Assignment/Evidence API was found in the inspected adapters/services.
- `create_http_app()` exists as a factory, but its runtime wiring is NOT VERIFIED.
- Meeting YAML/file persistence is not a Work persistence contract.
- Agent/Principal registries and Identity Resolution do not implement Work authorization.
- Work 28 `:8031` trace remains in DOC-061; this reconciliation does not repeat or broaden it.
- No accountable Core owner has been identified from the inspected repository metadata/search surface. This does not prove no maintainer exists outside that surface.

## 7. Required architecture decisions — not taken here

| Decision | Required authority/evidence | Current state |
|---|---|---|
| Name Core owner and service boundary | Accountable Core maintainer confirmation | BLOCKED |
| Select one authoritative Lifecycle/ExecutionHost path | Architecture authority + source/test evidence | OPEN |
| Confirm Work registry, Assignment and Evidence APIs | Core owner source path, revision, tests and runtime proof | NOT VERIFIED |
| Approve Work-scoped auth and commit-time enforcement | Core owner + security/architecture approval | NOT VERIFIED |
| Approve recovery/protected data separation and audit strategy | Core owner storage/transaction contract | NOT VERIFIED |
| Approve adapter/provider/session capabilities | Capability test + identity/target/session evidence | NOT VERIFIED |
| Approve routes/DTO/schema versions | Core owner contract review | NOT APPROVED |
| Approve G4 and per-WP DoR | Authority under DOC-004 and Product Owner | NOT READY |

## 8. Reconciliation defects and corrections

1. DOC-011 v1.7 had a stale sentence saying the WP register was absent from Sandbox. It was restored and exact-synced on 2026-11-02. DOC-011 is updated to v1.8 to reflect that current fact.
2. DOC-061 contains dated historical source baselines and corrections. Read the latest dated addenda together; do not treat the first-page branch counts or older Core snapshots as current.
3. DOC-063 P0.3/P0.4 addendum is additive design requirements, not implementation evidence.
4. DOC-064/065 are target architecture/logical contract, not proof that the user’s existing AI conversations can be directly reached by ROOM-HOP.
5. DOC-066 is verified as a Sandbox artifact and synchronized to main, but remains DRAFT; no dispatch/ACK/test was executed.

## 9. Next controlled sequence

1. Keep Core owner identification as the critical blocker; request the accountable maintainer to provide source baseline, runtime entrypoint, Work service/API, auth boundary, persistence/audit contract and tests.
2. Require Vi to produce source-path/symbol/test evidence only if a new source baseline or Core-owner handoff becomes available; do not repeat DOC-061 `:8031` audit without new evidence.
3. Ask Ka to review this reconciliation against DOC-061 and DOC-063 P0.3/P0.4; review is not approval.
4. Keep DOC-064/065/066 at design/test-plan status until owner/API/auth prerequisites are proven.
5. Continue read-only lifecycle/controller test design; do not create a third Execution Host or modify Core.
6. Revisit branch integration only with an explicit diff inventory and recovery plan; no merge/rebase/cherry-pick while divergent.

## 10. Final status

- Architecture reconciliation: **DONE — DOCUMENT/SOURCE RECONCILIATION ONLY**.
- Core owner: **NOT IDENTIFIED**.
- Core Work API/auth/persistence/evidence: **NOT VERIFIED**.
- DOC-061/063/064/065: **DRAFT / NOT APPROVED / NOT IMPLEMENTED**.
- DOC-066: **DRAFT / TESTS NOT RUN**.
- G0/G1: **NOT_READY**.
- G4 / BUILD: **NOT_READY / NOT PASS / NOT AUTHORIZED**.
- Runtime QE: **NOT RUN**.
- Work 70: **NOT ACCEPTED / NOT RELEASED**.

**Conclusion:** The four documents are compatible when read as layered target contracts, but none proves implementation. DOC-071 remains the current bounded statement of actual Core capability. Core owner, verified Work-scoped contracts and G4 remain prerequisites; no code or runtime work is authorized by this reconciliation.
