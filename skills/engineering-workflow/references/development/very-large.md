# Very Large Development

Use for multi-phase, multi-subsystem, multi-repository, or independently deliverable programs whose
state cannot be represented reliably by one plan.

## Artifacts

Use:

```text
DESIGN.md
ROADMAP.md
plans/
  01-<phase>.md
  02-<phase>.md
handoffs/
  01-<phase>.md
  02-<phase>.md
```

Do not maintain one giant `PLAN.md`.

## DESIGN.md

Describe the system-level objective, current and target architecture, core contracts, data/control
flow, subsystem boundaries, global constraints, compatibility or migration strategy, decisions,
risks, and global verification. Keep phase execution detail out.

## ROADMAP.md

Use the roadmap as the project control plane:

```markdown
# Roadmap

## Goal
## Global Constraints
## Phases
- [ ] Phase 1: ...
- [ ] Phase 2: ...
## Dependencies
## Current Critical Path
## Global Verification
## Completion Criteria
```

## Phase Plans

Create plans only for active or near-term phases:

```markdown
# Phase: <name>

## Goal
## Scope
## Inputs / Dependencies
## Constraints
## Plan
## Verification
## Exit Criteria
```

Every phase needs explicit exit criteria.

## Phase Handoffs

Maintain continuation state for active or completed phases:

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
2. Create or update `DESIGN.md` and `ROADMAP.md`.
3. Split work into phases with dependencies and exit criteria.
4. Create detail only for active or near-term phases.
5. Perform the post-roadmap re-evaluation in `development/workflow.md`.
6. Serialize contract-defining dependent phases.
7. Run independent phases in parallel only when ownership, inputs, outputs, and verification are
   explicit and edit conflicts are unlikely.
8. Maintain phase handoffs and re-evaluate at phase boundaries.
9. Integrate and run system-level verification.
10. Reconcile documentation with implementation and final diff.

The main agent owns integration and cross-phase consistency. Derive any subagent roles from the
actual phase boundaries; do not use a fixed agent taxonomy.

## Completion

A phase is complete only when its exit criteria are met or explicitly waived with reason. The project
is complete only when all required phases, integration verification, compatibility or migration,
relevant performance validation, cleanup, and documentation reconciliation are complete.
