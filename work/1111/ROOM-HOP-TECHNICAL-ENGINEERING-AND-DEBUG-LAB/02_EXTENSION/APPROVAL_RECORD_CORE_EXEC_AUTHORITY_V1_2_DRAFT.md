# APPROVAL RECORD — CORE EXECUTION AUTHORITY V1.2

- Work: 1111 — ROOM-HOP TECHNICAL ENGINEERING AND DEBUG LAB
- Prepared by: Co — Coder, under Cla (AI-03, CTO / Code-Debug Lead)
- Reconciled by: Xu — ROOM coordinator
- Decision owner: Anh Vinh
- Decision basis: explicit owner decisions already given on 2026-10-25 and follow-up instruction on 2026-10-26; reaffirmed by the owner on 2026-11-10 that this approval must not be requested repeatedly.
- Status: **APPROVED — PRIOR OWNER DECISION RECONCILED**
- This record supersedes the stale PENDING labels in the earlier draft. It records an existing approval; it does not invent a new approval date or expand scope.

## 1. Existing owner decision — authoritative history

On 2026-10-25, Anh Vinh explicitly opened Gate 2 and authorized Co to implement Core only under the following V1.2 contract:

- DR-1: port-independent, Core-enrolled service identity.
- DR-2: a separate short-lived grant token, with server-side validation.
- DR-3: Core-managed append-only durable store.
- DR-4: separate mount/process/port, remaining within Core authority.

On 2026-10-26, after MCP became available, Anh Vinh explicitly instructed Xu to continue. This is continuation of the same authorization, not a new approval checkpoint.

The 2026-11-08 instruction “ok tiếp cho hoàn thành đi CO, khong báo, ko chờ , cần PC báo lại” is consistent with the prior authorization and the user's end-to-end delegation preference. It must not be reinterpreted as a reason to ask the owner to re-approve DR-1..DR-4.

## 2. Owner decisions — reconciled

| Decision | Approved contract | Owner decision |
|---|---|---|
| DR-1 — Caller identity | Core-enrolled service identity; identity-based and port-independent. Deployment credential is injected through the approved environment/secret mechanism, never hardcoded. | **APPROVED — 2026-10-25** |
| DR-2 — Grant token | Separate, short-lived execution grant. Server validates the grant and its binding to caller, Work, purpose, status and expiry at each protected request. Token must not be exposed in logs/evidence. | **APPROVED — 2026-10-25** |
| DR-3 — Durable store | Core-managed append-only durable records for grant/run/evidence/handoff; preserve immutable history and allow lookup by record ID, with links to grant, source revision/hash, result and evidence. | **APPROVED — 2026-10-25** |
| DR-4 — Deployment separation | Additive separate mount/process/port within Core authority; not a second Core, not an independent execution route, and no authority outside the approved contract. | **APPROVED — 2026-10-25** |

## 3. Gate disposition

1. **Gate 1 — Contract approval: PASS / APPROVED.** DR-1..DR-4 are approved by the prior explicit owner decision recorded above.
2. **Gate 2 — Core implementation: OPEN / AUTHORIZED.** Co may implement and test the Core scope against the approved V1.2 contract, within the exact authorized repository/branch/task scope and all existing security controls.
3. **Gate 3 — W13 runtime alignment: NOT OPEN.** Requires separate verified runtime authorization and evidence that the exact hardened W13 source/build is active.
4. **Gate 4 — Security tests and live E2E: NOT OPEN.** Requires Gate 3 and separately authorized, task-scoped runtime probes. Source/unit/CI tests do not substitute for live evidence.
5. **Gate 5 — Wiring/publishing: NOT OPEN.** Requires Gates 1–4 to pass with exact-revision evidence and separate authorization for the relevant operation.

## 4. Implementation obligations and limits

- Implement only the approved DR-1..DR-4 contract; no arbitrary shell execution, direct MCP-to-W13 bypass, caller-supplied `authorized=true`, or authority outside Core.
- Bind grants and durable run records to the exact source revision/hash. A run record must not accept a source hash different from the revision bound to its grant.
- Bind protected operations to the exact Work and task/assignment authorization where the governing task contract requires it. Do not weaken DOC-117 or treat this approval as a substitute for task-scoped authorization.
- Fail closed for missing, stale, mismatched, expired, revoked, replayed or unverifiable authority.
- Durable audit/record failure must not be reported as successful protected execution.
- Do not read or disclose secret values. Use only the approved secret injection mechanism.
- No permission is granted here to operate PC/runner, restart services, access secrets, invoke live `/execute`, merge PR #48, modify `main`, deploy or release. Those remain separate gates/authorizations under DOC-117 and the relevant Work task.
- Preserve dirty working trees and unrelated changes. Do not reset, clean, stash, overwrite or discard unrelated work.

## 5. Operating instruction — no repeated approval loop

- Co must resume the authorized Core task without asking Anh Vinh to confirm DR-1..DR-4 again.
- Xu is responsible for reconciling prior owner decisions into the canonical approval record before escalating a decision.
- Agent progress is journal-first. No routine step-by-step chat polling or repeated approval prompts.
- Escalate only a genuinely new owner-reserved decision or an exact missing authority that cannot be resolved from canonical records. Continue all safe, authorized work while a separate gate is blocked.

## 6. Record integrity

- Decision owner: Anh Vinh
- Original approval date: 2026-10-25 (UTC+7)
- Follow-up continuation: 2026-10-26 (UTC+7)
- Reconciliation recorded: 2026-11-10 (UTC+7)
- Signature basis: prior explicit owner instructions preserved in conversation history and reconciled into this canonical Work record by Xu.
- This reconciliation does not claim that implementation, tests, CI, runtime, E2E or release have passed.

---
**Disposition:** DR-1..DR-4 APPROVED; Gate 1 PASS; Gate 2 OPEN/AUTHORIZED. Gates 3–5 remain closed pending their own prerequisites and authorization.
