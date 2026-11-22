# WORK 10 — LATEST CANONICAL BRANCH HEAD CI — RUN 195

- Document ID: W10-GITHUB-ACTIONS-CI-EVIDENCE-20261122-RUN195
- Workflow: Work 10 Cross-Platform Verification
- Run ID: `44965933111`; Run #195
- Exact tested commit / current branch HEAD: `73b51f61b62d3b1664e8d9d0dd54e979eb5640b1`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44965933111
- Conclusion: SUCCESS — both matrix jobs completed successfully.

## Ubuntu 24.04
- Job ID: `137034838816`
- Total: **220 PASS / 0 FAIL / 2 expected SKIP**
- HTTP API: 52 PASS
- Dashboard live E2E: 7 PASS
- Windows launcher contract: 13 PASS
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14731777359`; size 42,956 bytes
- SHA-256: `7780d3fd99641dc62dbedbddd916bb2d2dd78b16548ed2f0bc91185984b6fc43`

## Windows Server 2022
- Job ID: `137034839060`
- Total: **226 PASS / 0 FAIL / 0 SKIP**
- HTTP API: 52 PASS
- Dashboard live E2E: 7 PASS
- Windows launcher contract: 13 PASS
- PowerShell AST syntax + local launcher start/stop smoke: PASS
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14731377088`; size 36,862 bytes
- SHA-256: `fdca1edd3851e41710de3c4b9d547fb2824e05e24a9f517fbd1bc1aef4e8eab3`

## Relationship to Run #180

Run #195 is the latest canonical branch HEAD CI after the final Work Manifest/Journal/inventory synchronization. It contains documentation/evidence-only changes after Run #180; accepted runtime source and tests are unchanged from the Run #180 code commit. Run #180 remains the latest full code regression and includes the latest launcher token-isolation and HTTP oversized-request test fixes.

## Disposition

- Latest canonical branch HEAD: CI PASS.
- Latest full code regression: Run #180 PASS.
- Current totals: Windows 226 PASS; Ubuntu 220 PASS + 2 expected SKIP.
- No main merge, deployment or release.
- Work 10 remains ACTIVE — NOT RELEASED pending Owner PC acceptance and remaining integration/security gates.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
