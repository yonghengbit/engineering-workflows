# Small Development

Use for localized, clear, low-risk changes with a direct call path and straightforward verification.

## Artifacts

Create no `PLAN.md`, `DESIGN.md`, `HANDOFF.md`, or `ROADMAP.md` unless reclassified.

## Workflow

1. Confirm the implementation location and direct callers or consumers.
2. Confirm expected behavior and impact boundary.
3. Implement the smallest correct change.
4. Add or update necessary tests.
5. Run directly relevant verification.
6. Inspect the diff and remove temporary or unrelated work.
7. Report the change and evidence.

Do not create abstractions for ceremony. Reclassify immediately if exploration reveals material
contract, architecture, compatibility, concurrency, scheduling, persistence, protocol, or lifetime
risk.
