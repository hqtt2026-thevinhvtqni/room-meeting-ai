

## Architecture Addendum — Native Desktop Adapter Evaluation (2026-11-23)

### Decision status
DOCUMENTED DESIGN CANDIDATE ONLY. This addendum evaluates agent-desktop as a possible native Desktop Adapter. It does not select the dependency, authorize installation, or authorize implementation.

### Unified Computer Agent boundary
W10 remains the single Computer Agent / Computer Provider boundary. It may expose multiple adapter types behind the same governed runtime:

- **Browser Adapter (existing):** Playwright / Chromium page automation. Remains the path for web-page DOM and browser workflows.
- **Desktop Adapter (proposed):** native desktop application automation through an OS accessibility tree. agent-desktop is one candidate backend; not yet integrated or selected.

The proposed flow is: caller → approved ROOM-HOP authorization route → W10 Agent API → Agent Runtime/policy → selected adapter → fresh observation → post-condition verification → evidence.

### Candidate backend: agent-desktop
The upstream project is a CLI/C library, not an AI agent. It exposes native accessibility snapshots as JSON with element refs and supports macOS AX, Windows UI Automation and Linux AT-SPI. It can expose its commands as MCP tools over stdio. It does not replace Browser Adapter and does not provide an LLM. A successful action is not proof of a changed UI; W10 must obtain a fresh observation and verify the post-condition.

Official technical assessment and test plan: ../06_EVIDENCE/W10_AGENT_DESKTOP_TECHNICAL_ASSESSMENT_20261123.md.

### Mandatory boundaries
1. The existing ACTION_CONTRACT.md, WORKFLOW_CONTRACT.md and SAFETY_POLICY.md remain LOCKED and unchanged. Do not silently map desktop-specific operations into the browser contract.
2. A separate Desktop capability/action contract and threat model must be reviewed before any implementation.
3. W10 API remains loopback-only; no direct remote exposure and no Core authorization bypass.
4. W24 owns PC Source Bridge/Core authorization/authenticated PC transport; W112 owns cross-Work contracts; W14 owns canonical autonomous E2E execution/delivery; W113 owns shared Dashboard ingress :3000. W10 standalone UI remains :3010.
5. Any agent-desktop CLI/library invocation must be wrapped by W10 policy and ProcessSupervisor. No unrestricted shell or direct unrestricted MCP access for remote agents.
6. Every state-changing operation requires a fresh observation and explicit post-condition verification. Unsupported accessibility surfaces fail closed; no silent coordinate fallback.
7. Desktop snapshots, clipboard, screenshots and traces are sensitive data; local/private evidence and redaction are the default.

### Implementation sequence — gated
D0: upstream/license/security/platform review and dependency pinning proposal.
D1: Desktop capability contract + threat model + Owner authorization.
D2: Windows interactive-host pilot, read-only snapshot first.
D3: narrowly allow-listed actions and ref freshness/post-condition tests.
D4: W10 wrapper, process containment, audit/evidence and security tests.
D5: Browser Adapter regression, cross-platform feasibility and comparative benchmark.
D6: Owner review; only then decide integration or reject candidate.

No D0–D6 runtime implementation has been performed by this addendum. No source code or LOCKED contract changed.
