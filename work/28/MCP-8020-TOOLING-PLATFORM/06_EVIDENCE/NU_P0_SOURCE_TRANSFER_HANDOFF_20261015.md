# Nu Handoff — transfer canonical PC source to Work 28

Date: 2026-10-15
Priority: P0 / SOURCE-TRANSFER
Owner: Nu (collector/transfer implementation); Go (reproducibility); Cla (security veto); Ka (gate reconciliation); Vinh (final authority).

## Objective
Bring a verified, read-only snapshot of the actual PC working tree at D:\ROOM-HOP-CLEAN\room-meeting-ai into Work 28:
MCP-8020-TOOLING-PLATFORM/04_CODE/source_snapshot/

Do not modify source files, commit, push, restart MCP/Core, change the live registry, or substitute public GitHub main.

## Important capability boundary
The current MCP 8020 tool surface can write/read individual text files in a Work Sandbox but does not expose binary archive upload/import or arbitrary directory transfer. A PC-side ZIP by itself does NOT mean the source has been transferred into Work 28. Nu must not report transfer PASS until an authorized byte-transfer route exists and destination hashes are verified.

## Step A — review before running
1. Read and security-review 04_CODE/pc_readonly_source_collector.py; do not run the draft blindly.
2. Confirm the exact repo path and a new output directory outside the repository, for example D:\ROOM-HOP-SNAPSHOT\run-20261015-01.
3. Confirm the allowlist covers the implementation and tests needed for the MCP 8020 audit. Do not broaden it silently.
4. Do not include .env files, credentials/tokens, private keys/certificates, databases/runtime state, private-data logs, caches, generated output, or unrelated personal data.
5. Record the source tree's actual Git HEAD, branch, dirty/untracked status. The previously reported HEAD d7c90d9d31062d389810808e43dfdd19d7711b75 is only a prior reference and must be re-read from the PC tree.

## Step B — approved read-only collection
Only after Cla review and operator approval, run the collector in a controlled PC terminal with the exact repository and a fresh external output directory. It must use fixed read-only Git queries and must not modify the source tree. Capture the complete stdout, stderr, and exit code. If collector changes are needed, revise and review first.

Expected outputs:
- room-hop-source-snapshot.zip
- room-hop-source-snapshot.manifest.json
- collector stdout with source HEAD/branch/dirty, file count, total bytes, archive SHA-256, manifest SHA-256
- independent SHA-256 values computed on the resulting files.

## Step C — transfer route is a separate gate
Identify an authorized way to upload the ZIP bytes into Work 28. Acceptable routes must be explicitly supported by a tool/API or a user-uploaded attachment that Ka can actually read; do not invent endpoints, credentials, or tool names.
- If a real Work Sandbox archive import tool becomes available: transfer to a staging location, verify archive SHA-256 before extraction, reject absolute/traversal paths, symlinks/reparse points and duplicate paths, extract into 04_CODE/source_snapshot/, then recompute every file SHA-256 and compare to the manifest.
- If no import/upload route exists: STOP at SOURCE_TRANSFER_CAPABILITY_MISSING. Preserve the archive and manifest on PC and report the exact missing API/capability. Do not claim Work 28 contains the source.
- Do not try to paste binary ZIP bytes into sandbox_write or write base64 chunks as a fake import; no verified extraction/byte-integrity path exists that way.

## Step D — completion evidence
Only report SOURCE_SNAPSHOT_IMPORTED after all of the following:
1. Source archive and manifest were created from the actual PC tree.
2. Archive hash verified before extraction.
3. Import destination is exactly Work 28/04_CODE/source_snapshot/.
4. Manifest provenance and dirty/untracked state preserved.
5. All imported file sizes and SHA-256 values match the manifest.
6. An independent readback/inventory proves the actual files are present.
7. Raw logs, command, exit code, collector version, archive/manifest hashes, and verification result are saved under 06_EVIDENCE/.

## Current gate
- Collector draft exists in Sandbox but is NOT run and NOT yet security-approved.
- Current MCP surface has no archive upload/import tool.
- Source snapshot import: BLOCKED.
- Canonical source audit and live E2E-Automatic: BLOCKED until verified import.
- PC source modification: prohibited.
