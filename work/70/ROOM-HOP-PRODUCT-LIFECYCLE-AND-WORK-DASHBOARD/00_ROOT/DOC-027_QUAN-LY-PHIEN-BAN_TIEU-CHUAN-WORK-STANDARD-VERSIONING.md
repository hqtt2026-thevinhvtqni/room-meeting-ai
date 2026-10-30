# WORK STANDARD VERSIONING
- **STT / Document ID:** DOC-027
- **Priority:** P3
- **Read order:** 34
- **Depends on:** DOC-001; DOC-033
- **Status:** ACTIVE
- **Version / Updated:** 1.2 / 2026-10-30

- Standard ID: ROOM-HOP-WORK-MASTER
- Current baseline: 1.2
- Effective date: 2026-10-30
- Change authority: Vinh
- Maintainer: Xu (AI-01)

## Version history
- **1.0:** Initial Work lifecycle structure, phases, gates and Dashboard baseline.
- **1.1:** Clarified exact top-level Work structure, nine fixed 05_BUILD child directories, Work Package/evidence registers and storage/export design boundaries.
- **1.2:** Adopted four coordinated Work records (Biên bản, Kế hoạch, Bản vẽ/Mô hình when needed, Nhật ký thi công); defined Work root as canonical owner and 05_BUILD as mapping/engineering coordination only; added stable artifact mapping requirements, anti-duplicate rules and controlled legacy migration.

Every instantiated Work records the standard version used. Template changes are versioned and documented. Existing Works are not silently upgraded when the master template changes. Breaking changes require migration notes, compatibility assessment and explicit rollout decision.
