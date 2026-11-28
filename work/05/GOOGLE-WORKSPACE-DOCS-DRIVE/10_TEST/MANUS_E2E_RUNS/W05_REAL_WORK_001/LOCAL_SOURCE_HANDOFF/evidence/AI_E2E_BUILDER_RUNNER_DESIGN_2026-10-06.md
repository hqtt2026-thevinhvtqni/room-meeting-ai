# AI E2E Builder/Runner — General Design v0.1

Source lesson: Work 05 — Google Workspace Docs/Drive.

## Purpose

A reusable evidence-first lifecycle is:

`Input → Plan → Task Graph → Research → Decision Gate → Build → Run → Test → Evidence → Failure Detection → Bounded Recovery → Retest → QE → Release`.

Truthful verdicts are PASS, PARTIAL, BLOCKED, and NOT_RUN. Report text cannot upgrade BLOCKED or NOT_RUN to PASS.

## Core invariants

1. Existing Core/domain boundary remains authoritative; adapters are integrations.
2. No parallel architecture; attach to canonical project and existing UI/API boundaries.
3. Every PASS has command, timestamp, inputs, expected, actual, status, artifact path, and checksum where relevant.
4. Secrets are runtime-injected and never enter AI prompts, Room state, browser storage, logs, or source.
5. Mock/fake and real-provider suites have separate markers, commands, and reports.
6. Failures are preserved before bounded repair; focused retest is followed by full regression.
7. External mutations require explicit approved targets; no guessed target.
8. Canonical artifacts are verified by read-back from canonical storage.
9. Append-only records must reject accidental overwrites or require full-content compare-and-swap.

## Gate model

G01 authenticated provider; G02 explicit safe target; G03 lazy client/dependency readiness; G04 create/read/update; G05 revision conflict; G06 idempotent replay; G07 external-edit reconciliation; G08 failure recovery; G09 real browser boundary; G10 canonical evidence/read-back.

## Work 05 lessons

A local green suite is not external-provider evidence. Provider-shaped fakes are not Google runtime success. Changes/watch requires a real change-feed acceptance path. OAuth metadata must be separate from encrypted credentials. UI tests must attach to the existing Room route, not create a new frontend. Failure logs need append semantics. Phase checksums are snapshots. Canonical persistence requires canonical read-back.

## Required runner package

`01_INPUT.md`, `02_PLAN.md`, `03_TASK_GRAPH.md`, `04_RESEARCH.md`, `05_DECISIONS.md`, `06_BUILD.md`, `07_TEST.md`, `08_FAILURES.md`, `09_RECOVERY.md`, `10_QE.md`, `11_RELEASE.md`, `12_FINAL.md`, plus source/tests/evidence/checksum directories.

Real external and browser modes fail closed when credentials, safe target IDs, UI base URL, or authorization state are absent.
