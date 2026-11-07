# DOC-089 — KIẾN TRÚC HỆ THỐNG PREVIEW HOST DÙNG CHUNG CHO MỌI WORK
# SHARED DASHBOARD PREVIEW HOST ARCHITECTURE

- Document ID: DOC-089
- Priority: P1 — HIGHEST BUILD PRIORITY
- Owner: Xu / AI-01 (coordination); implementation owner to be assigned by evidence
- Status: DESIGN BASELINE — NOT DEPLOYED / NOT ACCEPTED
- Date: 2026-11-07
- Authority: Vinh / Product Owner

## 1. Problem and decision

Work Dashboard HTML/JSON artifacts exist in Sandbox, but Sandbox MCP is a file-storage interface and does not host HTTP pages. File existence/readback is not a usable preview. A shared Preview Host is therefore a product capability, not a one-off workaround for Work 70.

**Decision:** build one shared, read-only static Preview Host that serves allowlisted Dashboard files for multiple Works through stable per-Work routes. Work 70 is the pilot; successful verification is required before onboarding other Works.

## 2. User outcome

- User can open a real browser URL on PC and Android phone.
- One host serves multiple Works; each Work has its own route.
- The host renders the actual HTML and sibling JSON files, not a chat mockup.
- A Work without a valid Dashboard is clearly reported as unavailable; no fabricated page/data.
- The same host can be reused by all future Works following the Work 70 standard.

## 3. Architecture

Browser (PC / Android)
  -> private HTTPS access layer (preferred: Tailscale Serve on the user's own tailnet)
  -> Preview Host (Python standard-library HTTP server, loopback bind by default)
  -> allowlisted Preview Registry
  -> each Work's Dashboard directory (static HTML/CSS/JS/JSON only)

The Preview Host is a static-file presenter. It is not Core, Workspace, Gateway, Agent Runtime, MCP, lifecycle authority, or a data collector.

### 3.1 Routing contract

- Landing: /
- Work landing: /work/{work_id}/
- Explicit dashboard view: /work/{work_id}/{view}/
- Static assets and sibling JSON are resolved only under that Work's registered dashboard root.
- Initial pilot routes:
  - /work/70/execution/
  - /work/70/product/
- Registry maps Work ID to a canonical dashboard directory and named entrypoints. Do not infer filesystem paths from arbitrary URL input.

### 3.2 Registry contract

Each enabled record contains:
- work_id (stable string)
- display_name
- dashboard_root (repository-relative, explicit allowlist)
- views (named view -> relative entry file)
- enabled (boolean)
- source_revision (commit SHA or immutable snapshot ID when available)
- freshness_status (FRESH / STALE / UNKNOWN)
- last_verified_at (timestamp or null)

Unknown or disabled Work IDs return 404/503, not a default dashboard. Missing entrypoints return a clear unavailable page and server-side diagnostic.

### 3.3 Security and isolation

- GET and HEAD only. POST, PUT, PATCH, DELETE and all other methods return 405.
- No directory listing.
- Resolve and validate every path against the registered dashboard root; reject traversal, encoded traversal, absolute paths and symlink escapes.
- Serve only a narrow static extension allowlist; no Python, environment, secrets, repository source, or arbitrary files.
- Default bind is 127.0.0.1. Do not expose 0.0.0.0/public internet by default.
- Remote PC/mobile access uses private HTTPS (preferred Tailscale Serve) and tailnet access controls. Never publish a public unauthenticated endpoint.
- No credentials in URLs, HTML, JavaScript, registry, or logs.
- No write routes and no direct Core mutation. Dashboard data remains a read-only projection.
- Security headers: nosniff, no-referrer, restrictive same-origin policy; disable caching for status JSON or use explicit no-cache.
- Errors must not reveal absolute filesystem paths or secrets.

### 3.4 Freshness and provenance

- Show Work ID, view, source revision/snapshot, generated time, freshness status and last verification.
- If source revision is unknown, label UNKNOWN; do not claim live/current.
- STALE stays visible; Preview Host must not silently convert stale data to fresh.
- Host health is distinct from Work status and Gate status.

## 4. Non-goals

- Not a replacement for Core API, Work Dashboard domain service, authentication/authorization, persistence, or product dashboard.
- Not a CI/CD deployer and not a GitHub writer.
- Not a data generator or mock-data provider.
- Not a lifecycle/Gate decision-maker.
- No dependency on MCP 8020. Preferred build/control path remains MCP 8030 for Sandbox work only.

## 5. Operational model

- One host process on the user's designated PC.
- One explicit registry controls which Work dashboards are served.
- Private HTTPS access layer exposes only the local host to authorized tailnet devices.
- Startup/stop scripts, health endpoint, structured logs and runbook are required.
- Port default proposal: 8060, subject to a local port-availability check before deployment; never assume it is free.
- The server must start in read-only mode and fail closed if registry validation fails.

## 6. Acceptance criteria

A. Real browser rendering:
- Actual Work 70 execution and product/capability HTML render from the host.
- Browser network requests load the correct sibling JSON, not stale hardcoded fallback.

B. Multi-Work:
- At least two registered test Works can be routed independently, with no cross-Work file access.
- Unknown Work returns 404; disabled Work is not served.

C. PC/mobile:
- Open and navigate on PC and Android over private HTTPS.
- Responsive layout and JSON fetch work on both.

D. Security:
- GET/HEAD succeed; write methods return 405.
- traversal, encoded traversal, symlink escape, unregistered Work and non-allowlisted extensions are denied.
- no public unauthenticated exposure.

E. Integrity:
- STALE/UNKNOWN provenance remains visible.
- Missing/malformed JSON produces an explicit error state, not fabricated success.
- Host availability is not represented as Work Gate PASS.

F. Operations:
- documented install/start/stop/health/recovery steps.
- restart and registry reload tested.
- logs contain no secrets.

## 7. Verification states

- Design baseline: RECORDED.
- Implementation: NOT STARTED.
- Local host run: NOT RUN.
- PC browser E2E: NOT RUN.
- Android browser E2E: NOT RUN.
- Private HTTPS: NOT RUN.
- Security tests: NOT RUN.
- Independent QE: NOT RUN.
- Acceptance / release: NOT AUTHORIZED.

## 8. Dependency and blocker

MCP 8030 exposes Sandbox file operations only; it does not host or render HTTP pages. The actual host must run in the user's PC/repository environment (or an explicitly approved server). ChatGPT cannot truthfully claim a live URL until that environment has started the host and the URL has been tested from PC and Android.

## 9. Next actions

1. Build a minimal secure static host and explicit registry under Work 70 05_BUILD.
2. Add a Work 70 pilot registry record.
3. Provide deterministic Windows start/stop/health scripts.
4. Validate server security and local browser rendering.
5. Configure private HTTPS on the PC and verify Android access.
6. Obtain independent QE, then onboard another Work as multi-Work proof.
7. Only after all evidence, mark DONE/ACCEPTED and publish operational URL.

---
Xu / AI-01 — design baseline. Vinh retains final acceptance authority.
