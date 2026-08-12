# Validation Testing

Use for broad compatibility, migration, release, or correctness campaigns across independently
executable environments, configurations, or subsystems.

## Artifacts

Maintain:

```text
VALIDATION_PLAN.md
results/
VALIDATION_REPORT.md
```

## Validation Plan

Define the claim and boundaries, required and optional dimensions, supported and excluded
environments, stable case identifiers, ownership, dependencies, acceptance rules, evidence format,
retry policy, stopping conditions, and completion criteria.

Use the same stable identifiers in the plan, raw results, and report.

## Raw Results

Store each case predictably, for example:

```text
results/<case-id>/<run-id>/
```

Preserve command or procedure, sanitized environment, status, and unedited relevant output. Do not
overwrite a materially different run. Link external evidence when repository rules designate another
result store.

## Validation Report

Summarize executed scope, version and environment boundaries, results by case ID, failures, blocked
cases, plan deviations, aggregate conclusion, and follow-up.

## Workflow

1. Inspect current coverage and define the validation boundary.
2. Create case identifiers and acceptance rules.
3. Re-evaluate completeness and feasibility.
4. Validate setup with a representative smoke case.
5. Execute isolated partitions in parallel only when safe.
6. Preserve per-case evidence immediately.
7. Stop or narrow downstream work when a gating failure invalidates it.
8. Build the report from raw results, not memory.
9. Verify every required case has a terminal status.
10. Inspect final artifacts and test-code diffs.
