# Medium Development

Use for non-trivial analysis and several implementation steps within a clear architectural boundary.

## Artifacts

Maintain:

```text
PLAN.md
HANDOFF.md
```

Do not create `DESIGN.md` unless reclassified to LARGE.

## PLAN.md

Keep it concise and execution-oriented:

```markdown
# Task

## Goal
## Context
## Plan
- [ ] 1. ...
- [ ] 2. ...
## Constraints
## Verification
```

Record only the current behavior, key path, and constraints needed to execute. Do not use the plan as
an investigation diary.

## Workflow

1. Explore the relevant code and real call path.
2. Create or update `PLAN.md`.
3. Perform the post-plan re-evaluation defined in `development/workflow.md`.
4. Execute in meaningful stages and update plan state.
5. Add or update tests.
6. Run stage-local and overall relevant verification.
7. Inspect the complete diff.
8. Update `HANDOFF.md`.

## HANDOFF.md

Use a current-state snapshot:

```markdown
# Handoff

## Objective
## Current Status
## Changes
## Key Findings
## Decisions
## Verification
## Remaining Work
## Important Files
```

Reclassify to LARGE when architecture tradeoffs, cross-module contract redesign, public API or data
layout changes, concurrency or scheduling semantics, distributed protocols, resource lifetime, or
backend compatibility require a coherent design decision.
