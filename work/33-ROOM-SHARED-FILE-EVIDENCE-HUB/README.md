# Work 33 — ROOM-SHARED-FILE-EVIDENCE-HUB

**Status:** ACTIVE — documentation initialized; implementation and live verification not yet done.  
**Owner / authority:** Vinh.  
**Workstream:** ROOM-HOP shared file storage, retrieval, and evidence.

## Objective
Establish a shared file area that authorized ROOM-HOP AI agents can use to store and retrieve the same real file, with verifiable content and an auditable evidence trail.

## Current known issue
A prior Sandbox report stated that `sandbox_list` could enumerate files while `sandbox_read` returned `{}` for `WORK.md`. This is an unverified report in this GitHub work record, not a confirmed root cause. Reading content is therefore BLOCKED until reproduced and traced.

## Scope
- Survey existing relevant tools and implementations in Work 24, Work 28, and Work 30.
- Trace the current read path and identify the cause of the empty `sandbox_read` result.
- Define shared storage, read/write contracts, access controls, and evidence requirements.
- Validate with a real test file and content comparison by Xu, Vi, An, and Ka.

## Guardrails
- Do not change the live PC or running services during initial READ/TRACE.
- Do not write to GitHub outside this Work 33 branch as part of this initialization.
- Do not report PASS without observable evidence.
- Do not treat file listing as proof that file content can be read.
- Any integration into the main architecture requires Vinh's approval.

## Work documents
- [Plan](PLAN.md)
- [Acceptance criteria](ACCEPTANCE.md)
- [Work log](WORK_LOG.md)
- [Manifest](MANIFEST.md)
