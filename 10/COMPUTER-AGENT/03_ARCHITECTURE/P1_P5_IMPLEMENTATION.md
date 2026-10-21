# P1–P5 IMPLEMENTATION

P1 — PlaywrightBrowserAdapter: real Chromium lifecycle and browser actions.
P2 — AgentRuntime: all declared actions, deterministic ordering, evidence, bounded execution boundary.
P3 — verification: explicit post-condition checks; failure changes PASS to FAIL.
P4 — Dashboard: calls /health and /agent/execute; displays runtime result/evidence.
P5 — release: executable test suite + runtime smoke test + evidence manifest.

Important: the ROOM-HOP Sandbox can write source text but cannot itself launch the user's local Chromium process. Therefore P3/P5 PASS must be recorded only from an actual host execution.
