# W122 — Owner Decision Register
**ID:** ODR-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Decision authority:** Vinh — Product Owner
**Coordinator:** Xu / AI-01
**Status:** FOR OWNER REVIEW — NO DECISIONS RECORDED
**Related:** G2 Decision Pack; SEC-W122-001; AUTH-STATE-W122-001; Synthetic T001–T024

> This register prepares decisions; it does not record approval. All recommendations remain proposals until the Owner explicitly decides and the canonical Biên bản is updated.

| ID | Decision required | Xu recommendation / safe default | Options to consider | Status |
|---|---|---|---|---|
| ODR-01 | First pilot mailbox model | One owner-designated personal mailbox; single tenant boundary for pilot | Single owner mailbox / delegated or shared mailbox | OPEN |
| ODR-02 | Initial provider | Gmail first behind provider-neutral adapter | Gmail first / multi-provider from R1 | OPEN |
| ODR-03 | R2 access | Gmail read-only; narrowest approved scope; no Gmail-native drafts or send | Metadata only / readonly body scope subject to Google review | OPEN |
| ODR-04 | Draft behavior | R3 W122-local drafts only; no Gmail Compose scope by default | Local-only / Gmail-native draft after separate review | OPEN |
| ODR-05 | Attachments | Exclude content and extraction from R1/R2; retain only minimum metadata if needed | Exclude / metadata-only / later safe-type extraction | OPEN |
| ODR-06 | Retention and deletion | Minimize data; do not persist raw bodies/attachments beyond bounded processing until explicit retention policy | Short retention / configurable retention / owner-managed deletion | OPEN |
| ODR-07 | Notifications | Dashboard alert with minimal metadata; no body preview by default | Dashboard only / email notification / both with content controls | OPEN |
| ODR-08 | Human approval | Verified mailbox owner approves all external side effects; AI cannot approve its own output | Owner only / named delegated human approvers | OPEN |
| ODR-09 | Auto-send | None in initial product; default DENY | None / future allow-listed low-risk categories after separate R4 gate | OPEN |
| ODR-10 | Cost ceiling | No paid service or recurring commitment before budget approval | Zero-cost prototype / owner-defined monthly ceiling | OPEN |
| ODR-11 | Data/model processing | Provider-neutral model adapter; no body sent to external model until data-processing/privacy review | Local/private model / approved external model / metadata-only | OPEN |
| ODR-12 | Anh Đức handover | Separate tenant onboarding, explicit consent, role setup, revoke and support runbook | Single-user handover / managed multi-user tenant | OPEN |

## Gate dependencies
G2 cannot close until required decisions are explicitly accepted, rejected or deferred with owner and due condition. G3 cannot begin until G2 is approved and integration/security/test contracts are evidenced. No decision in this register grants OAuth, mailbox access, code execution or send permission.

## Decision recording format
For each item record: decision ID; ACCEPT / REJECT / DEFER; exact selected option; rationale; scope; effective date; owner; dependencies; evidence; canonical Biên bản reference. Silence, “OK tiếp”, or review of this draft is not approval.

## Current truth
All ODR-01 through ODR-12 are OPEN. No owner decision has been inferred. G2 NOT APPROVED; G3 BUILD NOT AUTHORIZED; Gmail OAuth/mailbox NOT CONNECTED; send NOT AUTHORIZED. W120/W121 untouched.
