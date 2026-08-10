# Large Development Workflow

Use for cross-module, high-risk, architecture-sensitive, or compatibility-sensitive development.

## Characteristics

Typical signals:

- multiple core modules or producer/consumer boundaries;
- more than one plausible technical approach;
- important interface or internal contract changes;
- data structure or memory-layout changes;
- concurrency, scheduling, caching, communication, or resource-management semantics;
- performance-critical paths;
- multiple backend/platform compatibility requirements;
- systematic regression verification is needed.

## Required Artifacts

Maintain:

```text
DESIGN.md
PLAN.md
HANDOFF.md
```

## DESIGN.md

`DESIGN.md` answers "why this solution."

Recommended structure:

```markdown
# Design

## Problem

What problem must be solved.

## Current Architecture

Current behavior, critical call path, and relevant boundaries.

## Constraints

Compatibility, performance, API, platform, and task-specific constraints.

## Proposed Design

The chosen design.

## Alternatives Considered

### Option A
- advantages:
- disadvantages:

### Option B
- advantages:
- disadvantages:

## Decision

What was selected and why.

## Compatibility

Impact on:
- APIs/contracts;
- configuration;
- backends/platforms;
- data/layout;
- behavior.

## Risks

Known failure modes or uncertainty.

## Verification Strategy

How correctness, compatibility, and performance will be checked.
```

Do not use `DESIGN.md` as an execution log.

## PLAN.md

Create the plan from the accepted design.

Example:

```markdown
# Task

## Goal

## Design Reference

See `DESIGN.md`.

## Plan

- [ ] Phase 1: core contract/data-structure changes
- [ ] Phase 2: producer path
- [ ] Phase 3: consumer path
- [ ] Phase 4: compatibility path
- [ ] Phase 5: tests
- [ ] Phase 6: benchmark/regression validation

## Verification
```

Do not reopen architecture choices in `PLAN.md` unless new evidence invalidates the design.

## Workflow

1. Explore current architecture and the real call path.
2. Identify compatibility and risk boundaries.
3. Create or update `DESIGN.md`.
4. Compare plausible approaches and record the decision.
5. Create or update `PLAN.md`.
6. Perform the post-design/plan re-evaluation defined in `SKILL.md`.
7. Implement in coherent phases.
8. Perform lightweight re-evaluation at phase boundaries.
9. Run phase-local verification where practical.
10. Run overall correctness and compatibility tests.
11. Run benchmark/regression checks when performance is relevant.
12. Inspect the complete diff.
13. Update `HANDOFF.md`.

## Implementation Rules

- Design before broad implementation.
- Keep one coherent set of architectural assumptions.
- Explicitly label temporary workarounds.
- Do not let a fallback silently become the primary design.
- Define compatibility paths and their intended lifetime.
- For performance work, preserve a baseline and compare against it when practical.
- Record environments/backends that could not be tested.

## Escalation Signals

Reclassify to `VERY_LARGE` when:

- the task becomes multiple independently deliverable phases;
- several subsystems can be developed and verified separately;
- work spans multiple repositories;
- migration or rollout is a major workstream;
- several agents could progress independently with low conflict;
- a single `PLAN.md` no longer represents the project clearly.
