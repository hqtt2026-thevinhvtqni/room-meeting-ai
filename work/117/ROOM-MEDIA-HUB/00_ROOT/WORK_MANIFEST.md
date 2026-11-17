# WORK MANIFEST — WORK 117
- Work ID: 117
- Work Name: ROOM-MEDIA-HUB
- Vietnamese Name: TRUNG TÂM LƯU TRỮ VÀ QUẢN LÝ ẢNH / VIDEO ROOM-HOP
- Product Name: ROOM MEDIA HUB
- Status: ACTIVE — DISCOVER / ARCHITECTURE CONSULTATION PREPARATION; STRUCTURE NORMALIZATION IN PROGRESS
- Authority: Vinh
- Executive Coordinator: Xu / AI-01
- Canonical repository target: hqtt2026-thevinhvtqni/room-meeting-ai
- Canonical branch target: main
- Canonical path target: work/117/ROOM-MEDIA-HUB/
- Sandbox path: 117/ROOM-MEDIA-HUB/
- Confirmed product direction: Hybrid internal + Cloud storage; shared Room-wide media library.
- Purpose: Provide one governed, searchable, previewable and auditable media library for ROOM-HOP, with Work associations and permission-controlled access.
- Architecture boundary: W117 owns media experience, media metadata/catalog, media-specific processing and storage orchestration. Work 33 remains the candidate canonical binary/file storage foundation; no competing raw-file store is to be created without an approved ADR.
- Non-goals for this planning baseline: implementation, provider selection, production credentials, public exposure, automatic deletion, AI training on stored media, and Git LFS/media binaries in GitHub.
- Lifecycle: follow Work 70 / DOC-033 documentation rules and DOC-075 architecture process. No BUILD until requirements, consultation, architecture review and Vinh's required gate decisions are complete.
- Current truth: W117 planning workspace created; existing Work 33, 26, 29 and 116 reviewed at document level. Runtime integration and source parity are NOT VERIFIED.

## Canonical Sandbox structure — aligned to Work 70
- 00_ROOT/ — canonical Work records
- 01_DISCOVER/; 02_DEFINE/; 03_ARCHITECT/; 04_PLAN/ — lifecycle phases
- 05_BUILD/ — 00_ROOT/, 01_ORIGINAL/, 02_EXTENSION/, 03_ARCHITECTURE/, 04_CODE/, 05_TEST/, 06_EVIDENCE/ (staging only), 07_RELEASE/, 10_AI_DEBUG_HANDOFF/
- 06_VERIFY/; 07_ACCEPT/; 08_RELEASE/; 09_OPERATE/ — lifecycle phases
- EVIDENCE/ — canonical cross-phase evidence repository
- DASHBOARD/ — Work-level dashboard entry/overview
- Dashboard working package canonical path: 05_BUILD/04_CODE/dashboard/ (read-only Dashboard authorization only)
- Legacy paths identified for retirement after parity/readback: root 01_ORIGINAL/, 02_EXTENSION/, 03_ARCHITECTURE/, 04_CODE/, 05_TEST/, 06_EVIDENCE/, 07_RELEASE/. Root 03_ARCHITECT/ remains canonical and is NOT a duplicate.
- Normalization control: copies are verified before legacy files are deleted; no destructive directory operation is assumed available.
