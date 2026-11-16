# DISCOVER BRIEF — ROOM MEDIA HUB
- Work: 117
- Status: DRAFT
- Product Owner: Vinh
- Coordinator: Xu

## Problem
Images and videos created, uploaded or referenced across ROOM-HOP can become scattered across chats, Work folders, AI outputs and external drives. Users and agents need a governed shared place to find and use media without copying large binaries into GitHub or bypassing Core permissions.

## Confirmed product intent
- Hybrid internal + Cloud storage.
- One shared Room-wide library.
- Images and videos are first-class media assets.
- Work-level associations and permission-controlled reuse are required.

## Stakeholders and users
- Vinh / Room Owner.
- ROOM-HOP AI agents and authorized human collaborators.
- Work owners and media producers (including video-generation workflows).
- Platform/security/operations and QE.

## Candidate use cases
1. Upload an image/video and retain original bytes.
2. Browse a gallery with thumbnails and metadata.
3. Play supported video formats without downloading the original.
4. Search by filename, type, date, creator, tags and linked Work.
5. Create albums/collections and share a controlled reference.
6. Attach a media asset to a Work, task, meeting or evidence record.
7. Generate thumbnails/proxies and record processing status.
8. Verify integrity, inspect versions and recover from local/cloud failure.
9. Soft-delete, restore and perform approved permanent purge.
10. Record who accessed, changed, shared or deleted an asset.

## Discovery boundaries
- W33 is a candidate storage foundation; do not assume its current CLI is production-ready or authorized for multi-user use.
- W26 and W29 are integration candidates; no existing media API or production endpoint is assumed.
- W116 is an external resource catalog, not the media store.
- Core authorization contract and cloud provider remain UNKNOWN until inspected/decided.

## Initial quality attributes
- Integrity: content hash verification and no silent corruption.
- Security: authenticated, authorized, least-privilege access; no public-by-default assets.
- Privacy: explicit retention, deletion, data classification and audit.
- Availability: internal access during cloud outage for locally available content, subject to final sync model.
- Durability: verified replica and restore procedure, not merely a "cloud connected" indicator.
- Performance: bounded upload, preview and playback with measurable targets to be defined.
- Portability: provider adapter and export path avoid hard vendor lock-in.
- Operability: health, capacity, replication lag, failed jobs and restore evidence visible.

## Unknowns requiring consultation
See canonical minutes and architecture consultation brief. No assumptions in this brief are runtime facts.
