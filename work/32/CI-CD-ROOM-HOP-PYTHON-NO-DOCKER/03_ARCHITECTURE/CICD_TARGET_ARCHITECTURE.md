# CI/CD Target Architecture — Python, No Docker

GitHub Actions is proposed as the CI coordinator using a hosted Python runner; Docker is not required. Initially enable validation only after approval; CD/deployment is a separate future phase.

Flow: scoped branch/PR → record source SHA and environment → run deterministic gates → retain logs/evidence → reviewer checks diff and risks → Vinh decides integration. No AI auto-merge, push or deploy.

Gates: G0 source/scope; G1 static syntax/compile; G2 unit tests; G3 safe integration tests; G4 dependency/security checks; G5 E2E when reproducible prerequisites exist; G6 evidence traceability; G7 human approval.

Status semantics: PASS = executed with evidence and passed; FAIL = executed and failed; BLOCKED = prerequisite/evidence unavailable; NOT RUN = not executed. Proposed repair loop: at most 3 attempts, then stop and request human review. No live-service mutation or deployment in this phase.