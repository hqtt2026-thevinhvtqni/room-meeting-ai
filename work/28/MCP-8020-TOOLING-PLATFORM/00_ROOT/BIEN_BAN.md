# WORK 28 — BIÊN BẢN / OFFICIAL MINUTES REGISTER

**Document status:** Canonical register  
**Work:** 28 — MCP Tooling Platform  
**Repository branch:** `work/28-mcp-tooling-platform`  
**Authority:** Vinh  
**Coordinator:** Xu

This is the single official minutes register for Work 28. Record decisions and instructions here. Technical reports, AI handoffs, test logs and review notes remain supporting evidence and must not be treated as parallel official minutes.

## BB-W28-20261103-001 — Governance reset and delivery direction

- **Date:** 2026-11-03
- **Source:** Vinh's instruction in the current ChatGPT conversation.
- **Decision:** Xu is to guide and coordinate the complete Work 28 scope; implementation and completion are to proceed on GitHub with maximum safe automation; Vinh should not be required to attend every small step or remain at the PC.
- **Team:** exactly Xu, Vi, Ka and An.
  - Xu — coordinator, architecture and technical decision owner.
  - Vi — implementation lead.
  - Ka — independent architecture/security review.
  - An — independent QA and verification.
  - Co — excluded from Work 28; no participation.
- **Source of truth:** GitHub branch `work/28-mcp-tooling-platform` for code and controlled documents; GitHub Actions for CI evidence.
- **Architecture:** Core :8000 remains the only authorization/application authority. MCP Build/Verification :8030 remains the supported build lane. Historical MCP :8020 listener is quarantined and DO NOT USE; Runtime MCP must be rebuilt as a separate target. Execution Host :8031 remains the approved execution boundary.
- **Safety state:** Work status ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
- **Required behavior:** no unsupported PASS claims; preserve old evidence; one official minutes register and one Work-wide journal; record decisions, blockers, evidence and handoffs.
- **Important limitation:** this record establishes governance and assignments. It does not prove that Vi, Ka or An have acknowledged or executed a task. Their actual work must be evidenced in GitHub artifacts and CI/review records.

## Minutes maintenance rule

Append new numbered entries. Do not rewrite historical entries to make later outcomes appear earlier. Correct errors with a dated addendum that preserves the original record.
