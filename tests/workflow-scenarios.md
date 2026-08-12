# Workflow Scenarios

Use these prompts for manual or agent-based forward tests of the canonical
`$engineering-workflow`. Give an evaluator the Prompt column without the Expected column. Check
routing, progressive loading, strategy, artifacts, transition timing, subagent decisions, and exit
criteria.

## Core Routing Scenarios

| Prompt | Expected |
|---|---|
| Add one optional CLI flag. | Development -> SMALL; no task artifacts |
| Run the existing unit tests and tell me whether they pass. | Testing -> QUICK; PASS/FAIL/BLOCKED evidence |
| REGISTER_KV_CACHE crashes; find the root cause and fix it. | Debugging -> Development -> Testing |
| Trace how Scheduler allocates and frees KV blocks. | Investigation; no artifact unless multi-session |
| Review this PR and report correctness problems. | Review; severity-ordered findings; no implementation |
| Compare baseline and new kernel throughput. | Performance -> COMPARISON |
| This kernel is slow. Find the bottleneck, optimize it, and verify the gain. | Performance -> optional Investigation -> Development -> Performance |
| Test this feature; if it fails, diagnose and fix it. | Testing -> Debugging -> Development -> Testing |

## Workflow-specific Strategy Scenarios

| Prompt | Expected |
|---|---|
| Add a loader mode inside the existing loader module, including configuration and tests. | Development -> MEDIUM; in-task plan, persisted only if checkpoints or continuation require it |
| Change a cache layout across scheduler, connector, GPU kernel, and two runtime backends. | Development -> at least LARGE; design and compatibility verification; handoff only if continuation is needed |
| Port a caching subsystem through independently deliverable backend, kernel, integration, and rollout phases. | Development -> VERY_LARGE; roadmap and phase artifacts |
| Verify authentication across two databases and three token modes. | Testing -> STRUCTURED |
| Validate a release across operating systems, database versions, and sync/async drivers with per-case evidence. | Testing -> VALIDATION |
| A deterministic parser crash points to one local bounds check; prove the cause. | Debugging -> DIRECT unless contrary evidence appears |
| Stale data appears intermittently when failover and cache promotion overlap. | Debugging -> SYSTEMATIC; `DEBUG.md` |
| Run the established latency threshold check in the pinned environment. | Performance -> CHECK |
| Explain throughput scaling across concurrency and payload size. | Performance -> CHARACTERIZATION |

## Mixed-task Scenarios

| Prompt | Expected |
|---|---|
| Review this PR, reproduce serious findings, fix confirmed issues, and verify supported configurations. | Review -> optional Debugging -> Development -> Testing |
| Explain request-ID propagation, then add propagation across async jobs. | Investigation -> Development |
| Add a new backend and benchmark it against the existing backend. | Development owns implementation and its verification; transition to Performance only when an independent performance conclusion becomes primary |
| Diagnose this flaky test, fix the cause, and rerun the affected matrix. | Debugging -> Development -> Testing |

## Failure Cases

| Failure case | Prompt / condition | Must not happen |
|---|---|---|
| Keyword trap | `Implement the feature and add tests.` | Select Testing merely because `tests` appears; this starts as Development |
| Supporting activity trap | Development must read callers and run unit tests. | Transition to Investigation or Testing without a new primary deliverable |
| Large-task agent trap | A LARGE change is tightly coupled around one new shared interface. | Create multiple agents solely because the scale is LARGE |
| Benchmark verification trap | Implement a known optimization and run a regression benchmark before finishing. | Transition to Performance merely because Development performs benchmark verification |
| Eager-loading trap | Any single-intent request. | Load all six workflow files or every Development/Testing strategy |
| Artifact ceremony trap | `Add one optional CLI flag.` | Create `PLAN.md`, `DESIGN.md`, `ROADMAP.md`, or `HANDOFF.md` |
| Debug patch-first trap | Unknown intermittent crash with no reliable reproduction. | Implement a speculative production fix before root-cause evidence |
| Review mutation trap | `Review this PR and report problems.` | Modify code without an explicit fix request or transition |
| Blocked-as-pass trap | Required validation environment is unavailable. | Count BLOCKED as PASS or omit it from the conclusion |
| Router-agent trap | Any mixed request. | Spawn a router agent or fixed debugging/testing agent taxonomy |
| Implicit-cost trap | A routine low-risk engineering request without explicit invocation. | Auto-load the broad skill body despite `allow_implicit_invocation: false` |

## Acceptance Signals

- Exactly one primary workflow owns the current phase.
- Only its `workflow.md` is loaded initially.
- Development or Testing loads at most one selected strategy reference.
- Supporting activities stay inside the owning workflow.
- Transitions occur only after the primary deliverable changes.
- Artifacts and subagents are proportional to actual task structure.
- Final claims map to current code, git diff, or captured runtime evidence.
