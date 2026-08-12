# Medium Development

Use for several implementation steps inside a stable architectural boundary.

## Artifacts

Plan in the current task by default. Maintain `PLAN.md` only when the work cannot be executed reliably
in one context, needs checkpoints, or must be reviewed independently. Maintain `HANDOFF.md` only when
another task, session, or agent needs continuation state. Do not create `DESIGN.md` unless reclassified.

When durable files are justified, keep them compact:

```markdown
# Task
## Goal
## Context and Constraints
## Plan
## Verification
```

```markdown
# Handoff
## Objective and Status
## Changes and Decisions
## Verification
## Remaining Work
## Important Files
```

## Workflow

1. Trace the relevant path and confirm the architectural boundary.
2. State a concise execution plan; persist it only when the artifact criteria apply.
3. Re-evaluate scale after planning.
4. Implement coherent steps with focused tests and local checks.
5. Run overall relevant verification and inspect the complete diff.
6. Write or update continuation state only when a handoff is actually needed.

Reclassify to LARGE when implementation requires a coherent decision about architecture, public or
cross-module contracts, layout, concurrency, scheduling, protocol, lifetime, security, migration, or
backend compatibility.
