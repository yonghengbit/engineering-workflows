# Medium Development Workflow

Use when the task requires non-trivial analysis and multiple implementation steps, but the architectural boundary is still clear.

## Characteristics

Typical signals:

- several related files or components;
- a non-trivial call chain must be understood;
- work stays mainly inside one module or one primary subsystem;
- several sequential implementation steps are required;
- existing behavior or compatibility needs deliberate preservation;
- no major architecture decision is required.

## Required Artifacts

Maintain:

```text
PLAN.md
HANDOFF.md
```

Do not create `DESIGN.md` unless the task is reclassified to `LARGE`.

## PLAN.md

Keep it concise and execution-oriented:

```markdown
# Task

## Goal

What must be true when the task is complete.

## Context

Only the background needed to execute the task:
- current behavior;
- key call path;
- known constraints.

## Plan

- [ ] 1. ...
- [ ] 2. ...
- [ ] 3. ...

## Constraints

Task-specific boundaries.

## Verification

- unit:
- integration:
- benchmark/manual:
```

`PLAN.md` answers "what will be done next." It is not an investigation diary.

## Workflow

1. Explore the relevant code and confirm the real call path.
2. Create or update `PLAN.md`.
3. Perform the post-plan re-evaluation defined in `SKILL.md`.
4. Execute the plan in meaningful stages.
5. Update plan checkboxes when stage state changes.
6. Add or update tests.
7. Run local verification after meaningful stages when practical.
8. Run overall relevant verification.
9. Inspect the complete diff.
10. Update `HANDOFF.md`.

## HANDOFF.md

Use this shape:

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

The handoff is a current-state snapshot for continuation, not a chronological log.

## Escalation Signals

Reclassify to `LARGE` when implementation materially requires:

- architectural tradeoffs;
- cross-module contract redesign;
- public API changes;
- data-layout changes across boundaries;
- concurrency or scheduling semantic changes;
- distributed protocol changes;
- backend compatibility design;
- a design artifact to keep assumptions coherent.
