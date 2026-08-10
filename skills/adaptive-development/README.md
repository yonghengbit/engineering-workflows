# adaptive-development

A Codex skill that automatically chooses one of four software-development workflows:

```text
SMALL
MEDIUM
LARGE
VERY_LARGE
```

The classification uses four dimensions:

```text
Scope + Uncertainty + Risk + Parallelism
```

It also performs controlled re-evaluation:

1. after initial code exploration;
2. after planning/design;
3. at major phase boundaries;
4. before final verification;
5. immediately when material complexity changes are discovered.

## Structure

```text
adaptive-development/
├── SKILL.md
└── references/
    ├── small.md
    ├── medium.md
    ├── large.md
    └── very-large.md
```

`SKILL.md` is the only router. It loads exactly one scale-specific reference.

## Install

For a repository-scoped skill, copy the folder to:

```text
<repo>/.agents/skills/adaptive-development/
```

For a user-wide local skill, copy it to:

```text
$HOME/.agents/skills/adaptive-development/
```

## Invoke

Explicitly:

```text
$adaptive-development

Goal: implement <your requirement>.
```

Or phrase the task normally and allow Codex to match the skill from its description.

## Expected repository documents

This skill does not replace project-level `AGENTS.md`.

Depending on task scale it may create or maintain:

```text
SMALL
  no task-management documents

MEDIUM
  PLAN.md
  HANDOFF.md

LARGE
  DESIGN.md
  PLAN.md
  HANDOFF.md

VERY_LARGE
  DESIGN.md
  ROADMAP.md
  plans/*
  handoffs/*
```

Use the skill as workflow logic; keep project-specific engineering conventions in `AGENTS.md`.
