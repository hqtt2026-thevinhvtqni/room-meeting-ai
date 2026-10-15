# Work 28 — Lệnh thi công Co / kiểm soát Ka / nghiệm thu Xu

Date: 2026-10-16
Scope: Work 28 only. Preserve existing tools. Do not modify Work 13.
Branch: \`work/28-mcp-tooling-platform\`

## Task orders published

1. **Co — implement and integrate**: [Issue #12](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/12)
   - Finish Runtime (3), Sandbox (4), GitHub (6) tools and wire registration into the existing MCP :8020 server.
   - Use existing trusted providers; Runtime through Core :8000; no duplicate runtime/server.
   - Add tests, prove live \`tools/list\`, run real smoke tests where possible, and record evidence.
2. **Ka CSA — independent control/reconciliation**: [Issue #13](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/13)
   - Compare implementation against Work 28 architecture/contracts/security and test plan.
   - Verify live registration separately from source code; inspect negative tests, authorization, path containment, default-branch protections and evidence.
   - Publish \`KA_TOOLSET_V1_CONTROL_REVIEW.md\` with findings and GO/NO-GO.
3. **Xu — end-to-end coordination and acceptance**: [Issue #14](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/14)
   - Track Co's implementation and Ka's independent verdict.
   - Accept only with real evidence for registration, existing-tool regression, tests, security and live MCP behavior.
   - Keep Work 28 ACTIVE / NOT LOCKED and do not merge to main while any mandatory gate is BLOCKED.

## Shared acceptance contract

- Existing tools remain intact.
- New tools: 3 Runtime + 4 Sandbox + 6 GitHub = 13.
- Tool source, registration helper, live MCP registration and successful E2E are distinct evidence levels; do not conflate them.
- Runtime must not execute arbitrary caller-provided shell/Python and must rely on Core's trusted principal and WorkContext.
- Sandbox must enforce Work-relative paths, bounded I/O and verified readback for writes.
- GitHub must use authenticated provider, protect default branches, require expected blob SHA for updates and return verifiable commit SHA.
- Capture revision SHA, exact commands, exit codes, test inventory, raw logs, tool-list snapshot and readback evidence.
- Do not modify Work 13 or widen scope unless a mandatory dependency is proven and recorded.

## Dispatch truth

The three GitHub task issues have been created. This records task orders; it does **not** prove that Co or Ka received an inbox notification, accepted the tasks, or started work. Do not claim dispatch acknowledgement until verified through the authorized ROOM-HOP task inbox/dispatch mechanism.

## Current state at time of order

- DONE: adapter source and initial tests added on Work 28 branch.
- BLOCKED / pending Co: wiring into the actual MCP :8020 startup and providers; live \`tools/list\` evidence.
- BLOCKED / pending Ka: independent control review of the integrated revision.
- BLOCKED / pending Xu: final E2E acceptance after implementation and review evidence.
- Work 28 remains ACTIVE / NOT LOCKED.
