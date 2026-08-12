---
name: engineering-workflow
description: Route software engineering tasks to Development, Testing, Debugging, Performance, Investigation, or Review, then apply only the selected workflow and necessary process depth. Use for implementation, validation, diagnosis, benchmarking, code understanding, change review, and mixed engineering tasks that may transition between those objectives.
---

# Engineering Workflow

Use one lightweight routing policy, then let one workflow own execution until the primary objective
changes. The router is policy for the current main agent—not an agent, executor, artifact owner, or
multi-agent orchestrator.

## 1. Apply Repository Constraints

Follow applicable `AGENTS.md` and `AGENTS.override.md`. Inspect repository and git state when relevant.
Repository rules constrain execution; they do not determine task type.

## 2. Route the Current Deliverable

Choose the result the user wants now, using repository context rather than keywords:

| Intent | Owning question | Load |
|---|---|---|
| Debugging | What causes this unexpected behavior? | `references/debugging/workflow.md` |
| Performance | How fast is it, why, and under what conditions? | `references/performance/workflow.md` |
| Investigation | How does the existing system work? | `references/investigation/workflow.md` |
| Review | What risks exist in this change or design? | `references/review/workflow.md` |
| Testing | Does behavior satisfy explicit criteria? | `references/testing/workflow.md` |
| Development | What behavior should be intentionally changed? | `references/development/workflow.md` |

For genuinely mixed wording, prefer: unknown failure -> Debugging; performance question ->
Performance; understanding -> Investigation; evaluation of an existing change -> Review; explicit
pass/fail -> Testing; intentional change -> Development. This precedence is a tie-breaker, not keyword
matching. “Implement and add tests” starts as Development; “run tests and report” starts as Testing.

## 3. Load Progressively

1. Load exactly one workflow file from the table.
2. Stop routing while it owns the task.
3. Let it choose strategy, artifacts, verification, and execution shape.
4. Only then load one selected strategy reference when applicable:
   - Development: `references/development/small.md`, `references/development/medium.md`,
     `references/development/large.md`, or `references/development/very-large.md`;
   - Testing: `references/testing/quick.md`, `references/testing/structured.md`, or
     `references/testing/validation.md`.
5. Load a destination workflow only after a real objective transition.

Never preload all workflows or strategies.

## 4. Sequence Mixed Tasks

```text
unknown crash; fix and verify
Debugging -> Development -> Testing

test; diagnose and fix only if it fails
Testing -> Debugging -> Development -> Testing

find bottleneck; optimize; prove gain
Performance -> optional Investigation -> Development -> Performance

review then fix confirmed findings
Review -> Development -> Testing
```

Each arrow is conditional. Reading code, running tests, checking correctness, collecting a local
measurement, or adding diagnostic instrumentation remains supporting activity inside the current
workflow. Transition only when the primary deliverable changes.

## 5. Transition Compactly

Reuse current context or an existing artifact; do not create a transition document by default.

```text
From / To:
Current Objective:
Verified Findings / Evidence:
Constraints:
Changed Files:
Known Reproduction / Procedure:
Required Next Action:
Verification Needed:
```

Carry only what the destination needs and stop applying the previous workflow.

## 6. Common Rules

- Use the smallest process that can produce trustworthy evidence.
- The router creates no artifacts; the selected workflow owns proportional artifacts.
- Preserve user work, avoid unrelated changes, and state unverified assumptions.
- Report blocked verification and inspect the final diff after modifications.
- Prefer current code and git diff for implementation, actual output for runtime behavior, and the
  selected workflow's designated artifacts for workflow state. Correct stale documentation.

## 7. Subagents

The routing phase must not create subagents. A selected workflow may use task-derived subagents only
with clear ownership, weak dependencies, low edit-conflict risk, explicit inputs and outputs, and
independent verification. LARGE does not imply multi-agent work; keep shared-contract work sequential.

## 8. Ambiguity

Choose a reasonable reversible route from context. Ask one concise question only when two routes
would authorize materially different actions or deliverables. Do not infer permission to implement
from a request to explain, diagnose, test, benchmark, or review.
