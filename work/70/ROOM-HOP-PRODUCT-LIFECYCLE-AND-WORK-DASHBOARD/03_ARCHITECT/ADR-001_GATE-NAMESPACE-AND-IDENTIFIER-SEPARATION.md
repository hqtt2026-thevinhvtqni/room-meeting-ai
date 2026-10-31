# ADR-001 — Gate Namespace and Identifier Separation
- Work: 70
- Status: PROPOSAL ONLY — NOT APPROVED / NOT IMPLEMENTED
- Owner: Xu / AI-01
- Authority: Vinh

## Problem
DOC-004 uses G0-G9 for lifecycle phase exits. DOC-057 independently uses G0-G5 for participant Work Entry. DOC-054 uses G0-G4 for technical integration. The same short identifier therefore names different controls.

## Proposed identifiers
- Lifecycle gates: LC-G0 through LC-G9 (DOC-004).
- Work Entry gates: WE-G0 through WE-G5 (DOC-057).
- Integration gates: INT-G0 through INT-G4 (DOC-054).

## Compatibility
Keep existing definitions and order unchanged. Treat bare G0..G9 as legacy aliases only within the source document where they are defined. New records, APIs, events, evidence, logs and Dashboard views must use the namespaced identifier. Do not silently reinterpret historical records.

## Migration
1. Approve this ADR.
2. Update DOC-004, DOC-057 and DOC-054 consistently.
3. Update DOC-001 current phase pointer and all cross-references.
4. Update DOC-042, DOC-044, phase playbooks, schemas and tests.
5. Add a validator that rejects ambiguous bare gate IDs in new machine-readable records.
6. Preserve historical IDs and provide explicit alias mapping.
7. Verify links, register, Sandbox/GitHub exact readback and regression tests.

## Non-goals
No gate criteria, decision authority, state machine or release policy changes in this proposal.

## Decision required
Vinh to approve, reject or request changes. Until then, current documents remain authoritative and no technical implementation may assume these proposed IDs.
