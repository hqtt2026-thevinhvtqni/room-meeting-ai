# AI E2E BUILD PROCESS v0.1 — ARCHITECTURE SPECIFICATION

- Work ID: 05
- Work Name: GOOGLE-WORKSPACE-DOCS-DRIVE
- Status: VALIDATED PROTOTYPE / READY FOR REAL-WORK RUN (reported validation; underlying run artifacts remain subject to E2E read-back)
- Date: 2026-09-29
- Scope: Generic AI E2E Build Process for ROOM-HOP Works
- Runner binding: NONE in v0.1; Manus is planned as a later E2E Runner
- AI Team implementation: OUT OF SCOPE for v0.1

## 1. PURPOSE

Define a reusable process that can take a human Goal and drive a Work from Goal to a verifiable terminal state.

The process is independent of any specific AI provider, model, or AI-team topology.

Core principle:

```
GOAL
 ↓
PLAN
 ↓
TASK GRAPH
 ↓
RESEARCH / PROPOSALS
 ↓
SYNTHESIS
 ↓
EVIDENCE GATE
 ↓
DECISION GATE
 ↓
BUILD
 ↓
TEST
 ↓
QE / VALIDATION
 ↓
FIX / RECOVERY
 ↓
VERIFY
 ↓
RELEASE
 ↓
DOCUMENT
 ↓
DONE
```

## 2. SCOPE BOUNDARY

### IN SCOPE
- Goal intake
- Work creation/context
- Task decomposition
- Task dependencies
- Role/capability requirements
- Research and proposal collection
- Synthesis
- Evidence requirements
- Decision and gate transitions
- Build/test/QE lifecycle
- Failure and recovery
- Human/Vinh Gate
- Audit trail
- Completion criteria
- Mapping to ROOM-HOP runtime concepts

### OUT OF SCOPE
- Selecting a specific AI provider
- AI registry/discovery
- Model routing
- Automatic AI calling protocol
- Multi-AI team topology
- AI pricing/quota routing
- Manus-specific implementation
- Google Docs/Drive implementation itself

These are later execution-layer concerns.

## 3. DESIGN PRINCIPLES

1. Goal before implementation.
2. Architecture before code.
3. Evidence before claim.
4. Independent proposal before synthesis where alternatives matter.
5. Task ownership is explicit.
6. Dependencies are explicit.
7. No blind overwrite.
8. No blind retry.
9. No infinite retry loop.
10. AI cannot cross VINH GATE without human decision.
11. A role is a capability requirement, not a permanent identity.
12. A Work is not DONE merely because an AI says DONE.
13. Every important transition leaves an artifact/evidence trail.
14. The process must remain executable by one AI or by a future AI team.
15. Runner and process are separate layers.

## 4. CORE ENTITIES

### 4.1 Work

A Work is the top-level execution container.

Minimum fields:
- work_id
- work_name
- goal
- status
- created_at
- updated_at
- current_stage
- current_gate
- task_ids
- artifact_ids

### 4.2 Task

A Task is the smallest independently trackable unit of work.

Minimum fields:
- task_id
- work_id
- title
- objective
- required_role
- owner
- input_refs
- dependency_refs
- output_requirements
- status
- evidence_refs
- created_at
- updated_at

### 4.3 Artifact

An Artifact is a durable output of a stage/task.

Minimum fields:
- artifact_id
- task_id/work_id
- type
- owner
- timestamp
- input_refs
- content/location
- status
- evidence_refs
- next_refs

### 4.4 Evidence

Evidence is an observable basis for a claim or transition.

Acceptable examples:
- test output
- command + result
- API response
- file content
- revision/version
- log
- screenshot where appropriate
- checksum/hash where appropriate
- timestamped runtime result

### 4.5 Decision

A Decision records a choice and its basis.

Minimum fields:
- decision_id
- issue
- options
- selected option or NEED_DECISION
- evidence_refs
- rationale
- authority
- timestamp

## 5. WORK STATE MACHINE

Primary states:

```
NEW
 ↓
PLANNING
 ↓
TASKING
 ↓
RESEARCH
 ↓
SYNTHESIS
 ↓
EVIDENCE_REVIEW
 ↓
DECISION_REVIEW
 ↓
BUILD
 ↓
TEST
 ↓
QE
 ↓
RECOVERY (when required)
 ↓
VERIFY
 ↓
RELEASE
 ↓
DOCUMENT
 ↓
DONE
```

Terminal/exception states:
- BLOCKED
- NEED_DECISION
- FAILED
- PARTIAL

Rules:
- A state transition requires its entry conditions.
- A failed transition does not silently advance the Work.
- RECOVERY returns only to a defined prior state after a repair plan.
- DONE is terminal for the current Work version unless a new change request creates a new execution cycle.

## 6. TASK GRAPH

Tasks form a directed dependency graph.

Example:

```
T01 Goal clarification
 ↓
T02 Research
 ├── T03 Proposal A
 ├── T04 Proposal B
 └── T05 Evidence
      ↓
T06 Synthesis
      ↓
T07 Decision
      ↓
T08 Build
      ↓
T09 Test
      ↓
T10 QE
```

Rules:
- A task cannot start while a required dependency is unresolved.
- Parallel tasks are allowed only when dependencies permit.
- Shared outputs are references, not silent copies.
- A task must not modify another task's owned artifact without an explicit handoff/change request.
- Overlap is recorded as dependency, conflict, or shared concern; it is not resolved by silent overwrite.

## 7. ROLE / CAPABILITY CONTRACT

v0.1 defines roles as capabilities:

- Orchestrator: controls Work/task state and transitions.
- Researcher: gathers independent research and evidence.
- Architect: produces architecture options and trade-offs.
- Synthesizer: consolidates proposals and evidence.
- Builder: implements approved scope.
- Tester: executes defined tests.
- QE: independently validates implementation/result.
- Evidence: normalizes and links evidence.
- Recovery: executes repair/retry/recovery plan.
- Release: checks release readiness.
- Documentation: records final durable state.

Important:
- Role != AI identity.
- One AI may perform multiple roles.
- Multiple AIs may perform the same role.
- The concrete AI assignment mechanism is outside this specification.

## 8. ARTIFACT CONTRACT

Canonical stage artifacts:

```
01_INPUT
02_PLAN
03_TASK_GRAPH
04_RESEARCH
05_PROPOSALS
06_SYNTHESIS
07_EVIDENCE
08_DECISION
09_BUILD
10_TEST
11_QE
12_FIX
13_RELEASE
14_FINAL
```

Every important artifact should contain:

```
STATUS
OWNER / AGENT
TIMESTAMP
INPUT
ACTION
RESULT
EVIDENCE
NEXT
```

Artifact rules:
- Preserve prior evidence.
- Do not silently delete historical conclusions.
- Revisions must be traceable.
- A corrected artifact should identify the reason for correction.
- Final artifacts must reference the evidence that supports their claims.

## 9. GATE ENGINE

### AUTO GATE
Continue when the action is already authorized by policy and dependencies/evidence are satisfied.

### EVIDENCE GATE
Required before a claim or stage transition that depends on observable proof.

Minimum:
- claim
- evidence
- evidence location
- verification result

### CONFLICT GATE
Triggered when material proposals/results disagree.

Required:
1. identify disagreement;
2. preserve both inputs;
3. compare assumptions;
4. compare evidence;
5. determine whether more testing is needed;
6. synthesize or escalate.

### VINH GATE
Mandatory human decision point for:
- architecture authority;
- business/policy choices;
- destructive or irreversible actions;
- security boundaries;
- changes to ROOM-HOP principles;
- unresolved material conflicts;
- decisions explicitly reserved to Vinh.

No AI may silently bypass this gate.

## 10. EVIDENCE CONTRACT

A claim is considered supported only when the evidence is:
- observable;
- traceable to the claim;
- associated with a timestamp/context where relevant;
- sufficient for the requested decision.

Evidence states:
- MISSING
- COLLECTED
- VERIFIED
- CONFLICTING
- INVALID
- SUPERSEDED

Important distinction:
- Research source is not automatically runtime evidence.
- A proposal is not proof.
- A successful command/test result is evidence only for what it actually tested.

## 11. FAILURE / RECOVERY ENGINE

Canonical flow:

```
FAIL
 ↓
CLASSIFY
 ↓
PRESERVE ERROR + EVIDENCE
 ↓
DIAGNOSE
 ↓
REPAIR PLAN
 ↓
RETRY (LIMITED)
 ↓
VERIFY
 ├── PASS → CONTINUE
 └── FAIL → ESCALATE / VINH GATE / BLOCKED
```

Failure classes:
- INPUT
- CONFIGURATION
- AUTHENTICATION
- AUTHORIZATION
- TOOL
- RUNTIME
- DATA
- CONCURRENCY
- EXTERNAL_SERVICE
- LOGIC
- TEST
- ENVIRONMENT
- UNKNOWN

Retry rule:
Every retry must add information or change the recovery action. Repeating the same failed action without new information is prohibited.

## 12. COMPLETION CONTRACT

Work may be DONE only when:
- Goal acceptance criteria are satisfied;
- required tasks are complete;
- required implementation is complete, if applicable;
- required tests have run;
- QE/validation is complete where required;
- evidence is stored and traceable;
- residual issues are classified;
- documentation is updated;
- no unresolved VINH GATE remains.

Allowed non-DONE outcomes:
- PASS
- BLOCKED
- NEED_DECISION
- FAILED
- RECOVERY
- PARTIAL

## 13. HUMAN / VINH INTERACTION

The process should minimize unnecessary questions.

AI should ask Vinh only when:
- required authority is missing;
- documented decisions conflict;
- the action crosses VINH GATE;
- business/policy intent is ambiguous in a way that changes the result;
- an irreversible/destructive action requires approval.

Otherwise AI continues automatically under established policy.

## 14. AUDIT TRAIL

Every material transition should be traceable:

```
timestamp
work_id
task_id
stage
actor/agent
action
input_refs
result
evidence_refs
next_state
```

The audit trail is append-oriented conceptually: historical facts are preserved even when the current state changes.

## 15. ROOM-HOP MAPPING

The process does not create a second system of truth.

Target mapping:

```
AI / Runner
   ↓
MCP 8020
   ↓
Core 8000 — SINGLE TRUTH
   ↓
Workspace / Adapter / External Systems
```

Implications:
- Work/task state belongs to the authoritative ROOM-HOP runtime layer when runtime implementation begins.
- Sandbox is the AI working environment.
- Sandbox must not gain extra governance/permission gates beyond necessary technical filesystem/path safety.
- External services remain adapters/integrations, not Core 2.

## 16. SINGLE-AI AND FUTURE-TEAM COMPATIBILITY

The process is intentionally neutral to execution topology.

### Single AI
One Runner can execute multiple roles sequentially.

### Future AI Team
Multiple agents can execute tasks by capability.

The process contract remains unchanged.

Therefore v0.1 does not encode:
- a fixed number of AIs;
- fixed AI identities;
- fixed provider/model;
- provider-specific calling APIs.

This separation is intentional.

## 17. MANUS RUNNER BOUNDARY

Manus is a planned first E2E Runner for a later phase.

Later phase objective:

```
Human Goal
 ↓
Manus
 ↓
AI E2E BUILD PROCESS v0.1
 ↓
Artifacts / Evidence / Gates
 ↓
DONE / BLOCKED / NEED_DECISION
```

The Manus phase must consume this process rather than redefine it.

Manus-specific:
- computer/tool use;
- AI/model calling;
- execution loop;
- task routing;
- runtime integration;
- provider limitations

are not part of this Work 05 architecture specification.

## 18. DRY-RUN ACCEPTANCE CRITERIA

Before declaring v0.1 ready for Manus execution, a dry-run must demonstrate:

1. Goal can be converted into a Work.
2. Work can be decomposed into tasks.
3. Dependencies prevent invalid task ordering.
4. Each stage creates a durable artifact.
5. Evidence is required at defined gates.
6. A conflict can be represented without losing either proposal.
7. A failure can enter Recovery without an infinite loop.
8. VINH GATE can stop the process.
9. A successful run can reach DONE.
10. An unsuccessful run ends in a defined non-DONE state.
11. The same process can be executed by one AI without changing the contract.
12. No provider-specific AI mechanism is required by the process itself.

## 19. STATUS

Architecture Specification v0.1 is:

**VALIDATED PROTOTYPE / READY FOR REAL-WORK RUN**

Validation history reported for this process:
- v0.1 Process Mechanics: PASS
- v0.2 Real Build: PASS
- v0.3 Failure & Recovery: PASS

These are reported milestone outcomes, not a substitute for inspecting each run's immutable artifacts. Next controlled step: execute one bounded real-work run with complete evidence and independent read-back. The generic process remains runner-neutral; Manus is a planned runner, not the process identity.

No production code is authorized by this specification alone.
