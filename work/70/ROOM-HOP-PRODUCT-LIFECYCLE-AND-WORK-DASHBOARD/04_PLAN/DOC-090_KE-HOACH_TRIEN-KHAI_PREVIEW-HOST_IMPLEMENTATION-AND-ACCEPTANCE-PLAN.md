# DOC-090 — KẾ HOẠCH TRIỂN KHAI VÀ NGHIỆM THU PREVIEW HOST
# PREVIEW HOST IMPLEMENTATION AND ACCEPTANCE PLAN

- Document ID: DOC-090
- Priority: P1 — highest priority in Work 70
- Parent architecture: DOC-089
- Pilot: Work 70
- Status: ACTIVE / IMPLEMENTATION IN PROGRESS — NOT DEPLOYED
- Date: 2026-11-07

## 1. Priority override

Preview Host is the first delivery priority of Work 70 until a usable, verified PC + Android preview exists. Other dashboard polish tasks are sequenced behind this capability except fixes required to render safely and accurately.

## 2. Work packages

### WP-PREVIEW-01 — Secure static host
- Python standard-library HTTP server.
- Registry-driven route resolution; no arbitrary path-to-filesystem mapping.
- GET/HEAD only; directory listing disabled.
- path traversal and symlink escape protection.
- static extension allowlist, security headers, no-cache JSON.
- health endpoint separate from Work status.
- default loopback binding.

### WP-PREVIEW-02 — Work registry and pilot
- explicit registry schema and Work 70 entry.
- execution and product/capability routes.
- no assumption that the product/capability projection is the independent Product Dashboard.
- source revision/freshness metadata shown honestly.

### WP-PREVIEW-03 — Windows operations
- start, stop, status and health-check PowerShell scripts.
- configurable port (default proposal 8060; check collision).
- process PID file and bounded logs.
- startup fails closed on invalid registry or missing dashboard root.

### WP-PREVIEW-04 — Private mobile access
- keep app bound to loopback.
- expose only through private HTTPS (preferred Tailscale Serve).
- verify Tailscale availability, login, serve configuration and tailnet ACLs on PC.
- verify Android phone is on the same authorized tailnet.
- do not use public port forwarding or public unauthenticated hosting.

### WP-PREVIEW-05 — Verification and onboarding
- unit/security tests for routing, traversal, methods, MIME, unknown/disabled Work, missing assets, malformed registry.
- browser E2E on PC and Android.
- register a second Work only after Work 70 pilot is stable.
- independent QE and formal acceptance.

## 3. Required evidence matrix

| ID | Test | Expected | Current |
|---|---|---|---|
| PH-01 | registry parses and validates | PASS | NOT RUN |
| PH-02 | Work 70 execution route | actual HTML + JSON | NOT RUN |
| PH-03 | Work 70 product route | actual HTML + JSON | NOT RUN |
| PH-04 | unknown Work | 404 | NOT RUN |
| PH-05 | disabled Work | 404/503 | NOT RUN |
| PH-06 | traversal / encoded traversal | denied | NOT RUN |
| PH-07 | symlink escape | denied | NOT RUN |
| PH-08 | POST/PUT/PATCH/DELETE | 405 | NOT RUN |
| PH-09 | extension allowlist | denied outside allowlist | NOT RUN |
| PH-10 | stale/unknown source metadata | visible, never upgraded | NOT RUN |
| PH-11 | PC browser | renders and fetches JSON | NOT RUN |
| PH-12 | Android browser via private HTTPS | renders and fetches JSON | NOT RUN |
| PH-13 | no public exposure | confirmed private only | NOT RUN |
| PH-14 | restart/stop/health | deterministic | NOT RUN |
| PH-15 | second Work isolation | no cross-read | NOT RUN |

## 4. Ownership and execution boundary

- Xu / AI-01: coordinate, architecture, acceptance matrix, evidence/journal, decision gates.
- Ka / AI-02: independent architecture/security review of DOC-089 and host boundary.
- Code owner: implement source and scripts after review; no unverified assignment is claimed.
- Qw / AI-05: independent QE after implementation and frozen test inputs.
- Vinh: final decision on network exposure, acceptance and release.

MCP 8030 can create/read/write Sandbox artifacts only. It cannot run the host, access the user's PC process table, configure Tailscale, or produce a verified preview URL. Those deployment actions require the user's PC environment or an explicitly connected execution host.

## 5. Release gates

- G1 Design: DOC-089 reviewed.
- G2 Build: host + registry + scripts + tests present.
- G3 Local verification: all security/unit tests pass.
- G4 Browser: PC and Android E2E pass.
- G5 Private access: HTTPS and tailnet access verified, no public exposure.
- G6 Independent QE: Qw report and no unresolved P1/P2 blockers.
- G7 Acceptance: Vinh approval.
- G8 Release: operational URL and runbook recorded.

No gate is inferred from file creation or self-reported checks.

## 6. Current blocker

The actual Work 70 dashboard artifacts are in the Sandbox namespace. The Preview Host must run in an environment that can read the same files. The present MCP 8030 Sandbox API does not expose a serving/runtime operation. A verified PC-hosted URL therefore cannot be created from Sandbox file operations alone. Build the host package and run it on the designated PC; then verify the private route.

## 7. Immediate next step

Build WP-PREVIEW-01 through WP-PREVIEW-03 in Work 70 Sandbox, read back every artifact, and prepare a single PC bootstrap procedure to transfer/sync the artifacts into the repository. Do not mark deployed until the user PC has actually run it and produced verifiable health/browser evidence.
