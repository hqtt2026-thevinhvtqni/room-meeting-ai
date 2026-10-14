# Work 98 — DASH + PREVIEW Acceptance Specification
- TÊN: Xu
- CHỨC DANH: Work 98 product/technical lead
- NGÀY: 2026-10-13
- GIỜ-PHÚT: 15:02 UTC+7

## DASH — product dashboard
- Target: apps/dashboard-pc/ in future target tree; preserve current / dashboard until path migration is approved.
- Pages: overview, ONT inventory/detail, customer/acc lookup, alerts, tickets, technicians, diagnostic history and audit.
- Filters/search/pagination must work on typed records; loading/empty/error states required.
- Every metric displays provenance/data mode. Mock data must show visible DEMO label.
- Desktop-first responsive layout, keyboard focus and accessible labels.

## APP — shared technician/customer app
- One responsive app with separate role journeys.
- Role comes from authenticated acc identity, not a client-controlled query parameter or hidden nav item.
- Sensitive actions checked at trusted service/local-agent boundary.
- Customer cannot reach technician actions by changing deep link; tests assert denial, not merely redirect.
- Technician completion requires diagnosis/action/test result and customer-confirmation policy.

## PREVIEW — build review
- Product preview is distinct from a Work file-list preview.
- Header: Work 98, build ID, source revision, created time, data mode and test state.
- Tabs: DASH, APP Khách hàng, APP Kỹ thuật viên, E2E Journey, Build & Evidence.
- Preview opens actual generated build/dev target with deterministic fixture data.
- If no executable build artifact exists, show explicit BLOCKED and reason, not a fake PASS.
- Include desktop and narrow-mobile viewports, deep links and error states.
- Link each acceptance check to evidence.

## Acceptance checklist
- [ ] DASH loads from canonical source and labels mock/live state.
- [ ] Customer role cannot reach technician-only route/actions.
- [ ] Technician workflow can process ticket end-to-end.
- [ ] Customer can create and track own ticket.
- [ ] Deep links validate IDs and enforce authorization.
- [ ] Preview points to current source revision and real build artifact.
- [ ] Build/lint/E2E results are captured and repeatable.
- [ ] No runtime dependency on ROOM-HOP Core or MCP.
