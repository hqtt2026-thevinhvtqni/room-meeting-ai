# WORK 10 — TEST PLAN

## P0 Contract
- [ ] /health returns service identity
- [ ] unsupported action is rejected
- [ ] type and click remain separate action types
- [ ] no fake PASS when browser adapter is disconnected

## P1 Browser
- [ ] start/close lifecycle
- [ ] navigate
- [ ] observe
- [ ] click
- [ ] type
- [ ] key_press
- [ ] wait
- [ ] extract
- [ ] screenshot

## P2 Agent Loop
- [ ] action sequence executes in order
- [ ] failure stops the sequence
- [ ] evidence is recorded
- [ ] post-condition is verified

## P3 Integrated E2E
Scenario: open a real page -> inspect -> identify target -> click -> type -> submit -> observe -> verify result.

PASS requires runtime evidence and post-condition verification.
