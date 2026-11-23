# WP0 Provenance Verification — CI-Independent Digest Check

Date: 2026-10-29 (UTC)
Branch: `work/28/wp0-evidence-handoff-20261029`
Verifier: Vibe (implementing agent), at Xu's direction
Method: GitHub Actions workflow `.github/workflows/work28-wp0-capture-digest.yml`
Run: Work 28 WP0 Capture Digest #1 — completed successfully (9s), on commit `f37abfd`

## Purpose

Close the WP0 capture provenance discrepancy (declared hash vs committed blob)
using a verification channel that does not depend on any text-fetch
normalization. The digests were computed **inside the CI runner** on the exact
committed bytes of the working tree after `actions/checkout`.

## CI-computed digest (authoritative)

- file: `WP0_MCP8030_tools_list_capture_20261029.txt`
- byte_count: **5022**
- sha256: **C214E1E5D4447EF6A16675C93C392E24D1AE4FA1E487A15724776508F63268C0**
- git_blob_sha1: **7c16429d1732ffa75cdb520c94113d198cbfc602**

Source: `WP0_CAPTURE_DIGEST_CI_20261029.md` (committed by the workflow itself,
commit `a248355`).

## Comparison with declarations

| Item | Declared (Xu, commit 5790df6) | CI-computed | Verdict |
|---|---|---|---|
| byte_count | 5022 | 5022 | MATCH |
| sha256 | C214E1E5...F63268C0 | C214E1E5...F63268C0 | MATCH |
| git_blob_sha1 | 7c16429d...8cbfc602 | 7c16429d...8cbfc602 | MATCH |

## Conclusion

1. The discrepancy detected earlier (declared 5025 bytes vs committed blob) was
   fully explained and resolved by Xu's correction in commit `5790df6`.
2. Xu's declared SHA-256 `C214E1E5...` is CONFIRMED by an independent
   in-runner computation over the exact committed bytes.
3. The earlier reconstruction attempts via text-fetch channels (open_url)
   produced mismatching digests because of channel-side normalization; those
   attempts are recorded as method failures, not as evidence against the
   committed file.
4. **Provenance gate item 1 (independent hash/byte-count verification without
   text normalization): CLOSED — VERIFIED.**

## Limits of this verification

- Verifies the committed blob's integrity and the declared digest, NOT the
  semantic correctness of the capture itself, NOT handler execution, and NOT
  runtime integration (WP2 remains BLOCKED).
- The deployed service source (`room-hop-build v1.28.1`) provenance gap
  remains OPEN.

## Status after this check

- Work 28: `ACTIVE / INTEGRATION BLOCKED / NOT RELEASED`
- Execution gate: `CLOSED`
- WP0 provenance (hash/bytes): `VERIFIED (CI)`
- WP2 runtime integration: `BLOCKED`
