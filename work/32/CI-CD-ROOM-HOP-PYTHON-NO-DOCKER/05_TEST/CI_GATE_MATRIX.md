# CI Gate Matrix

| Gate | Purpose | Evidence | Disposition |
|---|---|---|---|
| G0 | Source, branch, commit, changed paths | SHA and path list | FAIL/BLOCKED |
| G1 | Syntax, compile/import, static checks | Exact command, exit code, log | FAIL if command fails |
| G2 | Isolated unit tests | Command, counts, log | FAIL on assertion failure |
| G3 | Integration contracts | Environment, logs, cleanup | BLOCKED if unsafe/unavailable |
| G4 | Dependencies/security/secrets | Tool version, findings, exit code | FAIL/BLOCKED with reason |
| G5 | E2E when feasible | Run ID, artifacts, cleanup | BLOCKED if prerequisites missing |
| G6 | Evidence traceability | Artifact links and source SHA | FAIL if required evidence missing |
| G7 | Human approval | Reviewer and Vinh decision | NOT RUN until authorized |

A workflow file existing does not mean any gate passed. CD is not enabled in this phase.