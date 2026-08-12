# Large Development

Use for cross-module, architecture-sensitive, high-risk, or compatibility-sensitive changes.

## Artifacts

Maintain `DESIGN.md` when the task contains a material design or compatibility decision. Maintain
`PLAN.md` when execution has multiple dependent phases or needs reviewable checkpoints. Maintain
`HANDOFF.md` only for continuation across tasks, sessions, or agents. A LARGE label alone does not
justify empty files.

```markdown
# Design
## Problem and Current Architecture
## Constraints and Boundaries
## Alternatives and Decision
## Compatibility and Risks
## Verification Strategy
```

```markdown
# Task
## Goal and Design Reference
## Phases and Dependencies
## Verification
```

## Workflow

1. Trace architecture, producer/consumer contracts, and compatibility boundaries.
2. Compare plausible approaches and persist the decision when it must survive the current context.
3. Plan coherent phases and re-evaluate scale.
4. Implement dependent contract work sequentially; verify each meaningful phase.
5. Run overall correctness, compatibility, and relevant performance checks.
6. Inspect the complete diff and preserve continuation state only when needed.

Label temporary compatibility paths and their intended lifetime. Record untested environments or
backends. Use subagents only for real independent workstreams; LARGE alone is not a reason.

Reclassify to VERY_LARGE when several independently deliverable subsystems, repositories, migration
or rollout phases need separate plans and one roadmap must coordinate them.
