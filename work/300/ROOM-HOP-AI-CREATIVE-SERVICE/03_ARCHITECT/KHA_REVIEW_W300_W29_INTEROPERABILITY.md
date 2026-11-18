# KHA / AI-04 — INDEPENDENT REVIEW ADDENDUM (W300 ↔ W29)

- Received: 2026-11-19 06:28 +07:00
- Source basis: user-forwarded Kha report; Kha states review limited to W300 REVIEW_PACKET_PILOT_01.md and W117 EXISTING_WORK_TECHNICAL_AUDIT.md.
- Review mode: static document review only; no source-code inspection, ROOM participation, BUILD, provider call or API call claimed.
- Verdict: **APPROVE WITH CONDITIONS** for future interoperability design only; not architecture/build approval.

## 1. FLUX.2 klein 4B deferral
Kha assesses that deferring FLUX.2 klein 4B does not prevent future W300-to-W29 interoperability. W29 should consume a normalized image artifact and metadata contract, not depend on which image-generation model produced it. Model choice remains an internal W300 adapter concern.

## 2. Proposed minimal output contract (design proposal, not frozen)
Mandatory candidate fields:
- `contract_version`: version of the interchange contract.
- `asset_id`: stable unique identifier (UUID recommended; UUID v4 is a proposal, not a proven W29 requirement).
- `artifact_uri`: storage-neutral locator resolvable by an authorized consumer; do not prescribe a local absolute path or public URL before storage/security design.
- `media_type`: MIME type such as image/png or image/jpeg; file extension alone is insufficient.
- `width_px`, `height_px`: verified dimensions from decoded output bytes.
- `created_at`: ISO 8601 timestamp with timezone.

Recommended integrity/provenance fields:
- `sha256`, `byte_size`, `source_rights_ref` / consent reference, `origin_task`, `provider`, `model_id`, `model_version`, `prompt_ref` (not necessarily raw prompt), `seed` when supported, `qc_status` and `metadata_policy`.

Optional future fields may include tags, color profile, orientation, alpha-channel flag, crop/safe-area hints and intended aspect ratio. These must not be required for basic W29 ingestion unless W29 evidence proves otherwise.

## 3. Independence / loose coupling
W300 exports a versioned artifact package and does not call W29 internals. W29 independently reads/imports it. Keep storage implementation behind an opaque artifact URI and authorization mechanism. Do not require a shared mutable database or shared internal functions. Contract evolution must be additive where possible and versioned; consumers reject unsupported major versions with explicit errors.

## 4. Evidence gaps in W117
The supplied W117 audit is not the original W29 source tree. Before integration, inspect W29's actual input DTO/schema and import path, validation/error behavior, max file/byte/pixel limits and batch/bandwidth constraints. Also verify auth/access control, storage ownership/lifecycle, accepted formats/color profiles/orientation and whether W29 preserves or transforms the source asset. Kha explicitly does not claim these points are verified.

## 5. Conditions
1. Keep FLUX.2 klein 4B deferred from Pilot 01.
2. Record the above as a proposal only; do not freeze the contract until W29 source and owner-approved interface requirements are inspected.
3. Do not make W300 dependent on W29, or implement video/image-to-video in W300.
4. Before cross-Work integration, complete a direct W29 source audit for the evidence gaps above.

## 6. Evidence boundary
This report records the content supplied by Vinh as Kha's review. The two named GitHub documents were the stated basis; Xu has not independently verified Kha's browsing process or the full W29 source tree in this entry.
