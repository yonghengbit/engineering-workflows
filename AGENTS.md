# AGENTS.md

This repository is a workflow library, not an application.

## Editing Principles

- Keep `skills/` limited to workflows that are ready to be used by Codex.
- Keep incomplete or exploratory workflow designs under `proposals/`.
- Do not place a `SKILL.md` under `proposals/`.
- Prefer one clear responsibility per workflow.
- Do not duplicate detailed workflow rules in the future `engineering-router`.
- Keep repository/project-specific engineering conventions out of reusable workflow skills.
- Preserve backward compatibility for existing skill names and invocation behavior unless a change is intentional and documented.

## Architecture Rules

Use these layers:

```text
repository constraints
    -> primary-intent workflow
    -> workflow-specific scale/strategy
    -> execution
    -> verification
    -> optional workflow transition
```

Task type and task scale are separate concepts.

Examples:

- `Development` is a task type.
- `LARGE` is a development scale.
- `Testing` may use a different scale model.
- `Debugging` should be hypothesis-driven rather than reuse development scaling mechanically.

## Adding a New Workflow

Before creating `skills/<name>/SKILL.md`:

1. define its primary intent;
2. define what it explicitly does not own;
3. define entry and exit conditions;
4. define artifacts, if any;
5. define re-evaluation or escalation behavior;
6. define allowed workflow transitions;
7. test the workflow against several real tasks.

Use `docs/workflow-contract.md` as the common contract.

## Router Rule

The future `engineering-router` must stay thin.

It may:

- classify the primary intent;
- choose the appropriate workflow;
- coordinate a transition when the primary objective changes.

It must not:

- contain the detailed development/testing/debugging procedures;
- reproduce scale-specific rules from child workflows;
- turn every mixed task into a heavyweight multi-workflow process.

## Documentation

When implementation and documentation disagree, inspect the active skill and correct stale documentation.
