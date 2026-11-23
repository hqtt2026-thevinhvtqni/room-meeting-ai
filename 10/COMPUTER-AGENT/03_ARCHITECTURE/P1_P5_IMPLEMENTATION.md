

## Architecture extension proposal — Desktop capability track (2026-11-23)

This is a design-only track and does not change the existing P1–P5 browser implementation definitions.

- **D0 — Research:** verify upstream project, license, release/checksum, platform limits, security guidance and supported accessibility surfaces.
- **D1 — Contract:** define a separate Desktop Adapter capability contract, threat model, action allow-list, ref freshness rules, privacy rules and failure semantics. Keep the three existing LOCKED contracts unchanged.
- **D2 — Host pilot:** after explicit Owner authorization, run read-only snapshot tests on the designated interactive Windows host; capture exact OS/session/binary provenance.
- **D3 — Action verification:** test only non-destructive actions on a dedicated test application/account; refresh snapshot after each action and prove post-conditions.
- **D4 — W10 wrapper:** if the pilot passes and Owner separately authorizes implementation, wrap the dependency behind W10 Agent Runtime and ProcessSupervisor; prohibit unrestricted CLI/MCP/shell bypass.
- **D5 — Regression and benchmark:** preserve Browser Adapter E2E; compare token usage, latency, success/failure, retries and unsupported controls on identical workloads.
- **D6 — Owner decision:** integrate, defer or reject based on evidence. No release by implication.

Gate state on 2026-11-23: D0 DOCUMENTED from public upstream docs; D1–D6 NOT STARTED. Dependency install, runtime, tests and benchmark NOT RUN. This track is not a new Work and does not replace the existing P1–P5 track.
