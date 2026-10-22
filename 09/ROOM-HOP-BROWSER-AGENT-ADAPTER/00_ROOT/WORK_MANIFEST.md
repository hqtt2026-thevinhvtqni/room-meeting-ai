# WORK MANIFEST — Work 09

- **Work ID:** 09
- **Name:** ROOM-HOP Browser Agent Adapter
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Canonical path:** `09/ROOM-HOP-BROWSER-AGENT-ADAPTER/`
- **Related Work:** Work 09.1 — Browser Workflow Engine (separate; do not merge into Work 09)
- **Structure:** `00_ROOT` through `07_RELEASE`
- **Source of work:** Work 09 Sandbox; original source must be preserved under `01_ORIGINAL`
- **Runtime boundary:** Browser adapter/provider remains separate from ROOM-HOP Core and MCP; do not deploy Core into Sandbox
- **Release status:** NOT VERIFIED by this manifest

## Standardization rules

1. Keep Work 09 under the numbered root alongside other Works.
2. Preserve source provenance and existing evidence; do not fabricate test results.
3. Exclude `.venv/`, `__pycache__/`, `.pyc`, credentials, and transient logs from Git.
4. Separate source synchronization from runtime/E2E verification.
5. Do not mark release PASS until tests and end-to-end evidence have been reviewed.
