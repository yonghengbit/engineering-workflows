# Development Workflow

Own intentional software behavior change. Trace the real path, classify complexity, load one scale
reference, implement, and verify. Reading code, writing tests, and checking a benchmark may support
Development without changing ownership.

## Classify Complexity

Score each dimension 0–3:

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Scope | local | module | cross-module | cross-system/workstreams |
| Uncertainty | clear | investigation | design choices | architectural |
| Risk | low | compatibility-sensitive | important contract/layout/concurrency/backend | migration/protocol/security/rollout |
| Parallelism | atomic | sequential phases | independently decomposable | program-scale |

```text
sum 0-2  -> SMALL
sum 3-5  -> MEDIUM
sum 6-8  -> LARGE
sum 9-12 -> VERY_LARGE
```

Use architectural judgment over file count, line count, or duration.

Classify at least LARGE when the requested change materially alters a public or important
producer/consumer contract, persistent format, cross-boundary memory layout, concurrency or
scheduling semantics, distributed protocol, resource lifetime, security boundary, or important
backend compatibility. Mere presence in the call path does not trigger this rule.

Use VERY_LARGE when multiple major subsystems or repositories also form independently verifiable
workstreams or rollout phases, or one `PLAN.md` can no longer represent the work.

## Load One Scale

After enough exploration to verify scope, load exactly one:

```text
SMALL      -> references/development/small.md
MEDIUM     -> references/development/medium.md
LARGE      -> references/development/large.md
VERY_LARGE -> references/development/very-large.md
```

## Re-evaluate Sparingly

Re-evaluate after initial exploration, after planning/design, at meaningful phase boundaries, before
final verification, and on material discoveries such as new contracts, layout, concurrency,
scheduling, lifetime, protocol, migration, backend, or independent-workstream impact. Do not rescore
after each file or command.

Upgrade without discarding useful work:

```text
SMALL -> MEDIUM       add Medium artifacts
MEDIUM -> LARGE       add/update DESIGN.md and revise PLAN.md
LARGE -> VERY_LARGE   preserve DESIGN.md; add ROADMAP.md and phase plans/handoffs
```

Downgrade only when early evidence proves the task materially simpler; avoid oscillation after
implementation progresses.

## Execute

- Trace real callers and consumers.
- Prefer the smallest correct change and existing abstractions.
- Preserve compatibility unless intentionally changed; avoid unrelated refactors and silent fallbacks.
- Remove temporary diagnostics and add tests proportional to behavior.
- Run the strongest practical verification, record blockers, and inspect the final diff.
- Keep required artifacts aligned with implementation.

Use subagents only for actual independent paths, backends, tests, benchmark infrastructure, or phase
preparation with low conflict and explicit outputs. Keep contract-defining work sequential.

## Exit

Complete when requested behavior is implemented, verification ran or is explicitly blocked, the diff
contains no unintended work, and artifacts are current. Report scale, reason, changes, verification,
and remaining issues; return to top-level routing only if the deliverable changes.
