# Small Development Workflow

Use for localized, clear, low-risk changes.

## Characteristics

Typical signals:

- one localized implementation area;
- direct call path is clear;
- no architecture decision is required;
- no material public/cross-module contract change;
- no material change to data layout, concurrency, scheduling, persistence, protocol, or resource lifetime;
- verification is straightforward.

File count is not the deciding factor. Cognitive complexity takes precedence.

## Required Artifacts

Do not create:

- `PLAN.md`
- `DESIGN.md`
- `HANDOFF.md`
- `ROADMAP.md`

unless the task is reclassified.

## Workflow

1. Confirm the real implementation location and direct callers/consumers.
2. Confirm the expected behavior and impact boundary.
3. Implement the smallest correct change.
4. Add or update necessary tests.
5. Run directly relevant verification.
6. Inspect git diff.
7. Remove temporary debug code and unrelated edits.
8. Report the change and verification result.

## Constraints

- Do not create abstractions merely for style.
- Do not perform unrelated cleanup.
- Do not skip verification because the change is small.
- If exploration reveals materially larger scope or risk, reclassify immediately.
