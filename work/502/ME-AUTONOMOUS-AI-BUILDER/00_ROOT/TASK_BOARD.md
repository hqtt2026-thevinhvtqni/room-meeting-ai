# TASK BOARD — WORK 502
- Version: 0.1
- Status: DESIGN / DISCOVERY
- BUILD authorization: NOT GRANTED

| Task ID | Work Package | Scope | Status | Dependency / Exit evidence |
|---|---|---|---|---|
| W502-WP01 | Discover ROOM-HOP contracts | Core identity/auth, Gateway, Agent Runtime, Sandbox/Execution Host, audit | IN_PROGRESS | Source-backed contract map |
| W502-WP02 | AutoGPT due diligence | Exact release, license, security, self-host requirements, API/MCP | IN_PROGRESS | Version-pinned review and risk report |
| W502-WP03 | Model integration | Work 501 registry/router/policy contracts | BLOCKED | Work 501 approved API and policy contract |
| W502-WP04 | MÊ architecture | Adapter, state machine, role contracts, data flow, trust boundaries | IN_PROGRESS | Approved architecture and ADRs |
| W502-WP05 | Security and safety | Tool allowlist, sandboxing, secrets, egress, prompt injection, budget limits | PLANNED | Threat model and security acceptance |
| W502-WP06 | UX and dashboards | One-prompt intake, task timeline, source/evidence, review dashboard | PLANNED | UX model and data contract |
| W502-WP07 | Test strategy | Unit/integration/browser/E2E/recovery and acceptance | PLANNED | QA plan and objective thresholds |
| W502-WP08 | Independent consultation | Cla, Ka, Qw, Vibe, Go, Qc, Kha and relevant owners | PLANNED | Actual response/ACK evidence; unverified identity remains UNVERIFIED |
| W502-WP09 | Lifecycle structure normalization | Resolve generated starter folder numbering against Work 70 | BLOCKED | Non-destructive migration map and readback |
| W502-WP10 | Build and pilot | Implement a bounded vertical slice after approval | NOT AUTHORIZED | Explicit Vinh BUILD approval |
| W502-WP11 | Release and handoff | Preview, production gates, docs, source and demo link | NOT AUTHORIZED | Acceptance + release approval |

## Operating limits
- Maximum 3 retries per unchanged repair approach.
- No infinite loops; timeouts, max steps, max concurrency and token/resource ceilings are mandatory.
- Paid provider, billing, cloud resource and public production deploy are denied until separately approved.
- Every task must have input/output contract, owner, dependency, acceptance criteria and evidence.