# DOC-104 — Work32 PR49 Source Mirror Manifest

- **Document Number:** DOC-104
- **Priority:** P0 — source provenance before remediation
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Source branch:** `work/32-main-integration-20261109`
- **Source HEAD at fetch:** `f0a8e55bc16ed27b6c43fa51164bc9e8f74253ef`
- **Method:** GitHub file fetch by exact branch ref; SHA values are returned Git blob SHAs.
- **Destination:** Work32 Sandbox `06_EVIDENCE/SOURCE_MIRROR_PR49_20261109/`

| Source path | Git blob SHA |
|---|---|
| core/meeting_service.py | 0b80a81663c1be328c41878a6762d16d95378aab |
| core/context_loader.py | 0f686e594d248dfd93287271e8ac4d483feb5ef2 |
| core/identity_resolution.py | 207c0ea74e3c77929c1723b0e66beba4ccf36201 |
| core/secretary.py | 1e3a2eb2228b4c778429f1e3dad78cacaacf04d9 |
| core/agent_registry.py | 7e4b98e68fa1a208ebd5788d9235d9c222e402a3 |
| core/principal_registry.py | 1eda0c80f413c1405415f92e0e2ff3b82a43b5ef |
| core/meeting_manager.py | 64f075f4c22ed08bb82e97d97878beed45678212 |
| core/paste_rate_limiter.py | db95a2f910bb755bcbca7ea873c022fb1bb30853 |
| room_hop_mcp/adapter/server.py | b740f72b95ea3a6e0a7e1d19a3ef3275b9899815 |
| room_hop_mcp/adapter/http_server.py | f17d752f6badf2b600f78906e63982d18f70e859 |
| room_hop_mcp/browser_agent_adapter/adapter.py | 9f937fc98aec1a2847199046bf0af076db932349 |

## Verification
All 11 files were independently read back from Sandbox and compared to GitHub content from the exact branch. Result: **11/11 byte-for-byte equal**. This is source mirror integrity evidence, not runtime verification.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Record:** Read-only source mirror completed and byte-for-byte verified.

## NHẬT KÝ
- **W32-LOG-20261109-93**
- Retrieved 11 Core/adapter source files from PR #49 exact branch head and recorded blob SHAs.
- Sandbox readback comparison: 11/11 PASS.
- No source code was modified.
