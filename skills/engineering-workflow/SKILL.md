---
name: engineering-workflow
description: Coordinate mixed, high-risk, or evidence-sensitive software engineering work across Development, Testing, Debugging, Performance, Investigation, and Review. Use explicitly when a task needs reliable routing, proportional process, or controlled transitions between objectives; use native Codex directly for routine low-risk work.
---

# Engineering Workflow

Route the current deliverable once, then let one workflow own execution until the requested result
changes. Treat this router as policy for the current agent, not as an executor or orchestrator.

## Apply Repository Constraints

Follow applicable `AGENTS.md` and `AGENTS.override.md`. Inspect repository and git state when relevant.
Repository rules constrain every route but do not select it.

## Route by Requested Result

| Intent | Current result | Load |
|---|---|---|
| Debugging | Prove what causes unexpected behavior | `references/debugging/workflow.md` |
| Performance | Produce a controlled performance conclusion | `references/performance/workflow.md` |
| Investigation | Explain how the existing system works | `references/investigation/workflow.md` |
| Review | Identify risks in an existing change or design | `references/review/workflow.md` |
| Testing | Decide whether explicit criteria pass | `references/testing/workflow.md` |
| Development | Intentionally change software behavior | `references/development/workflow.md` |

For mixed wording, use the earliest unresolved result: unknown failure before repair, measurement
before optimization, understanding before a requested change, review before selected fixes, explicit
pass/fail before conditional diagnosis, otherwise intentional change. This is an outcome rule, not
keyword matching. “Implement and add tests” starts as Development; “run tests and report” starts as
Testing.

## Load Progressively

1. Load exactly one workflow from the table and stop routing.
2. Let that workflow choose process, evidence, artifacts, and execution shape.
3. Load at most one selected strategy reference when required:
   - Development: `references/development/small.md`, `references/development/medium.md`,
     `references/development/large.md`, or `references/development/very-large.md`;
   - Testing: `references/testing/quick.md`, `references/testing/structured.md`, or
     `references/testing/validation.md`.
4. Load another workflow only after a real objective transition.

Never preload alternatives.

## Preserve Ownership

Reading code, running tests, checking correctness, collecting a supporting measurement, or adding
diagnostic instrumentation stays inside the owner. Transition only when the primary requested result
changes, for example:

```text
unknown failure -> proven cause -> requested repair -> independent regression result
Debugging       -> Development  -> Testing

failed check -> requested diagnosis -> requested repair -> rerun
Testing      -> Debugging           -> Development     -> Testing
```

Every arrow is conditional. A review does not authorize fixes; diagnosis, testing, benchmarking, and
explanation do not authorize production changes unless the request includes them.

## Transition Compactly

Reuse current evidence; do not create a transition document by default. Carry only the destination's
objective, verified evidence, constraints, changed files, reproduction or procedure, next action,
and verification need. Stop applying the previous procedure.

## Common Boundaries

- Use the smallest process that can support trustworthy claims.
- The router creates no artifacts or subagents.
- Preserve user work, report blocked evidence, and inspect the final diff after modifications.
- Prefer current code and diff for implementation, actual output for runtime behavior, and raw
  measurements for performance.
- A workflow may use task-derived subagents only for independent, low-conflict work with explicit
  inputs, outputs, and verification. Scale alone never requires them.
- Ask only when ambiguity would authorize materially different actions; otherwise choose a reversible
  route and state the assumption.
