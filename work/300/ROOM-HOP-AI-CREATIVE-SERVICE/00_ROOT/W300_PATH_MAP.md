# W300 PATH MAP — CANONICAL SOURCE AND SANDBOX MIRROR
Date: 2026-11-19
Status: ACTIVE — identity/path reconciliation

## Identity mapping
| Concept | Current value | Meaning |
|---|---|---|
| Work ID | `300` | Stable Work identifier; do not change/reuse |
| Sandbox runtime folder | `300/TRAO-DOI-VA-GIOI-THIEU/` | Legacy runtime folder name; metadata rename is not available through current Sandbox tools |
| Current product identity | `AI-IMAGE-AND-PHOTO-STUDIO` | Current product identity recorded in manifest |
| GitHub repository | `hqtt2026-thevinhvtqni/room-meeting-ai` | Canonical repository |
| GitHub branch | `main` | Canonical branch |
| GitHub Work root | `work/300/ROOM-HOP-AI-CREATIVE-SERVICE/` | Canonical Work document/code root |
| Display/product name | `300 - AI Image & Photo Studio` | User-facing product name |

## Canonical documents on GitHub main
- Manifest: `00_ROOT/DOC-001_WORK-MANIFEST.md`
- Document register: `00_ROOT/DOC-002_DOCUMENT-REGISTER.md`
- Decision log: `00_ROOT/DOC-003_DECISION-LOG.md`
- Official minutes: `00_ROOT/DOC-034_BIEN-BAN_HOP-WORK-300-MINUTES.md`
- Official journal: `00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-300-EXECUTION-JOURNAL.md`
- Review packet: `03_ARCHITECT/REVIEW_PACKET_PILOT_01.md`
- AI handoff: `03_ARCHITECT/AI_REVIEW_HANDOFF.md`
- Roadmap: `04_PLAN/IMPLEMENTATION_ROADMAP.md`

## Sandbox mirror / working evidence
Sandbox Work ID `300` currently exposes root folder `TRAO-DOI-VA-GIOI-THIEU/`.
- Cla review: `TRAO-DOI-VA-GIOI-THIEU/03_ARCHITECTURE/CLA_REVIEW_PILOT_01.md`
- Sandbox journal: `TRAO-DOI-VA-GIOI-THIEU/06_EVIDENCE/WORK_JOURNAL.md`
- Other discovery/design files remain in the same legacy runtime tree.

## Synchronization rules
1. GitHub main paths above are the canonical records for approved Work documentation.
2. Sandbox is a working/evidence mirror, not a second canonical governance source.
3. A Sandbox-only review artifact is not considered synchronized until copied to GitHub and read back.
4. Keep the legacy Sandbox folder name for traceability until the runtime supports a safe metadata rename. Do not create a second Work ID.
5. Keep the old dashboard source in place and mark LEGACY / NOT VERIFIED. It is excluded from current build scope; do not move/delete without impact assessment and explicit authorization.
6. Do not claim full mirror parity until all relevant files are compared.

## Known drift
- Three identifiers are visible across systems: Work ID `300`, Sandbox folder `TRAO-DOI-VA-GIOI-THIEU`, GitHub root `ROOM-HOP-AI-CREATIVE-SERVICE`, and product identity `AI-IMAGE-AND-PHOTO-STUDIO`.
- The Sandbox and GitHub folder structures are not identical.
- This map resolves navigation and authority, not runtime folder metadata or complete file parity.
