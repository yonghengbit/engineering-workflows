# Large Development

Use for cross-module, high-risk, architecture-sensitive, or compatibility-sensitive development.

## Artifacts

Maintain:

```text
DESIGN.md
PLAN.md
HANDOFF.md
```

## DESIGN.md

Capture why the solution is designed this way:

```markdown
# Design

## Problem
## Current Architecture
## Constraints
## Proposed Design
## Alternatives Considered
## Decision
## Compatibility
## Risks
## Verification Strategy
```

Cover critical call paths, producer/consumer boundaries, compatibility, data/layout, performance,
platform constraints, and meaningful alternatives. Do not use `DESIGN.md` as an execution log.

## PLAN.md

Create an execution plan from the accepted design:

```markdown
# Task

## Goal
## Design Reference
See `DESIGN.md`.
## Plan
- [ ] Phase 1: ...
- [ ] Phase 2: ...
## Verification
```

Do not reopen architecture choices unless new evidence invalidates the design.

## Workflow

1. Trace current architecture and compatibility boundaries.
2. Create or update `DESIGN.md` and compare plausible approaches.
3. Record the decision and create or update `PLAN.md`.
4. Perform the post-design/plan re-evaluation in `development/workflow.md`.
5. Implement coherent phases with local verification.
6. Re-evaluate lightly at phase boundaries.
7. Run overall correctness, compatibility, and relevant performance checks.
8. Inspect the complete diff and update `HANDOFF.md`.

Keep one coherent set of architectural assumptions. Label temporary workarounds, define compatibility
paths and their intended lifetime, preserve performance baselines when relevant, and record untested
environments or backends.

Use subagents only for actual independent workstreams; LARGE alone is not a reason.

Reclassify to VERY_LARGE when the task becomes several independently deliverable phases, spans
multiple repositories or major subsystems, includes migration or rollout as a major workstream, or a
single `PLAN.md` no longer represents it clearly.
