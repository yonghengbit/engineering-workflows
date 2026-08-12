# Development Workflow

Own intentional software behavior change. Trace the real path, select one scale, implement the
smallest coherent change, and verify it. Code reading, tests, and supporting benchmarks remain
Development activities unless the requested result changes.

## Select Scale

Choose from verified scope, uncertainty, risk, and coordination needs—not line count or duration:

| Scale | Use when |
|---|---|
| SMALL | Local, clear, low-risk change with direct verification |
| MEDIUM | Several steps inside a stable architectural boundary |
| LARGE | Cross-module contract, architecture, compatibility, concurrency, layout, lifetime, security, backend, or migration risk |
| VERY_LARGE | Several independently deliverable subsystems, repositories, or rollout phases need a program-level roadmap |

Use the higher scale when one material boundary dominates. Do not inflate scale because many files
merely participate in one simple call path.

Load exactly one:

```text
SMALL      -> references/development/small.md
MEDIUM     -> references/development/medium.md
LARGE      -> references/development/large.md
VERY_LARGE -> references/development/very-large.md
```

## Re-evaluate Only on New Evidence

Recheck after initial exploration, after a durable design or plan, at meaningful phase boundaries,
before final verification, or when a new contract, layout, concurrency, protocol, migration,
security, compatibility, or independent-workstream impact appears. Do not rescore every command.
Preserve useful work when scale changes and avoid oscillation after implementation begins.

## Execute

- Trace real callers, consumers, failure paths, and compatibility boundaries.
- Prefer existing abstractions and the smallest correct change; avoid unrelated refactors and silent
  fallbacks.
- Add tests proportional to changed behavior and remove temporary diagnostics.
- Run the strongest practical verification, record blockers, and inspect the final diff.
- Create durable artifacts only when the selected scale reference requires them for decisions,
  coordination, or continuation.

Use subagents only for actual independent paths or phases with low edit conflict and independent
verification. Keep shared-contract decisions sequential.

## Exit

Complete when requested behavior is implemented, relevant verification ran or is explicitly
blocked, the diff contains no unintended work, and any necessary continuation state is current.
Report scale and reason, changes, evidence, and remaining risk. Return to routing only when the
requested deliverable changes.
