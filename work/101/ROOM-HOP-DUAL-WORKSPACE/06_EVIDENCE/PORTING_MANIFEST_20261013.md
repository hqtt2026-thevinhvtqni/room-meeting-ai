# Work 101 Initial Porting Manifest

Date: 2026-10-13
Source: Sandbox Work ID 101
Destination: GitHub branch `work/101-room-hop-dual-workspace`, Work root `work/101/ROOM-HOP-DUAL-WORKSPACE/`

## Ported or reconciled
- Work requirements and context/target identity.
- Canonical folder contract, architecture, sync rules and Dashboard Preview ADR.
- Pure policy module and its unit tests (security path cases include single-backslash paths).
- Dashboard contract schema, canonical static Dashboard and separate static Preview.
- Branch/target evidence and build log.

## Deliberately excluded
- `desktop.ini` and other OS metadata.
- Secrets, credentials, runtime databases, logs, caches, temporary files and generated artifacts.
- Any Work 101 files at repository root.
- Any runtime adapter or direct Core/MCP/GitHub write implementation not proven by existing contracts.

## Verification limits
Files are being read back from GitHub after creation. This manifest does not claim source/destination digest parity, test execution, browser runtime, two-way sync or E2E PASS. Sync remains DRY_RUN; merge/release disabled.
