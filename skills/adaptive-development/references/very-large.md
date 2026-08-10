# Very Large Development Workflow

Use for multi-phase, multi-subsystem, multi-repository, long-running, or naturally multi-agent projects.

## Characteristics

Typical signals:

- several independently meaningful technical phases;
- multiple major subsystems;
- possible multiple repositories;
- explicit dependency graph between phases;
- multiple workstreams can progress independently;
- migration, rollout, or long-lived compatibility is significant;
- a single working context or single plan is insufficient to preserve state reliably.

## Required Artifacts

Use:

```text
DESIGN.md
ROADMAP.md

plans/
  01-<phase>.md
  02-<phase>.md
  ...

handoffs/
  01-<phase>.md
  02-<phase>.md
  ...
```

Do not maintain one giant `PLAN.md`.

## DESIGN.md

Describe system-level design:

- overall objective;
- current architecture;
- target architecture;
- core interfaces and contracts;
- data/control flow;
- subsystem boundaries;
- global constraints;
- compatibility/migration strategy;
- key technical decisions;
- global risks;
- global verification strategy.

Keep phase execution details out of this document.

## ROADMAP.md

`ROADMAP.md` is the project control plane.

Recommended structure:

```markdown
# Roadmap

## Goal

## Global Constraints

## Phases

- [ ] Phase 1: ...
- [ ] Phase 2: ...
- [ ] Phase 3: ...

## Dependencies

- Phase 2 depends on Phase 1.
- Phase 4 depends on Phase 2 and Phase 3.

## Current Critical Path

## Global Verification

## Completion Criteria
```

## Per-Phase Plan

Each phase has `plans/<phase>.md`:

```markdown
# Phase: <name>

## Goal

## Scope

## Inputs / Dependencies

## Constraints

## Plan

- [ ] ...

## Verification

## Exit Criteria
```

Every phase must have explicit exit criteria.

## Per-Phase Handoff

Each active or completed phase has `handoffs/<phase>.md`:

```markdown
# Handoff: <phase>

## Objective

## Status

## Changes

## Key Findings

## Decisions

## Verification

## Remaining Work

## Important Files
```

## Workflow

1. Explore enough architecture to establish system boundaries.
2. Create/update `DESIGN.md`.
3. Create/update `ROADMAP.md`.
4. Split work into phases with explicit dependencies and exit criteria.
5. Create phase plans only for active/near-term phases; do not pre-write excessive detail for distant phases.
6. Perform the post-roadmap re-evaluation defined in `SKILL.md`.
7. Execute independent phases in parallel only when the multi-agent policy permits it.
8. Execute contract-defining dependent phases sequentially.
9. Maintain phase handoffs as source-of-continuation state.
10. Re-evaluate at major phase boundaries.
11. Integrate and run system-level verification.
12. Reconcile documentation with final implementation and git diff.

## Multi-Agent Rules

Parallelize only when:

- ownership boundaries are explicit;
- dependencies are weak or already resolved;
- edit conflicts are unlikely;
- each workstream has clear inputs and outputs;
- each workstream can be independently verified.

Good parallel work:

```text
Agent A -> isolated backend implementation
Agent B -> test/benchmark infrastructure
Agent C -> compatibility investigation
```

Bad parallel work:

```text
Agent A -> redesign shared core interface
Agent B -> implement consumer against the old interface
```

If one workstream defines a contract required by another, make the dependency explicit and serialize them.

## Source-of-Truth Order

When artifacts disagree:

```text
current code / git diff
    -> DESIGN.md
    -> ROADMAP.md
    -> phase plan
    -> phase handoff
```

Fix stale documentation when discovered.

## Completion

A phase is complete only when its exit criteria are satisfied or explicitly waived with reason.

The project is complete only when:

- all required phases are complete;
- integration verification passes;
- compatibility/migration paths are verified;
- performance validation is complete when relevant;
- temporary experimental code is removed;
- documentation matches the final implementation.
