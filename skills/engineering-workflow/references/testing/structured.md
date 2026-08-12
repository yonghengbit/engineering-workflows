# Structured Testing

Use for bounded test matrices, new regression design, integration checks, or multi-configuration
verification needing durable planning and reporting.

## Artifacts

Maintain:

```text
TEST_PLAN.md
TEST_REPORT.md
```

## TEST_PLAN.md

```markdown
# Test Plan

## Objective
## System / Change Under Test
## Environment
## Baseline
## Pass / Fail Criteria
## Matrix
| Case | Configuration | Procedure | Expected | Priority |
|---|---|---|---|---|
## Setup and Isolation
## Evidence to Capture
## Risks / Constraints
```

Keep every case traceable to the objective. Mark optional coverage explicitly.

## TEST_REPORT.md

```markdown
# Test Report

## Summary
## Environment
## Results
| Case | Result | Evidence | Notes |
|---|---|---|---|
## Failures
## Blocked / Untested
## Conclusion
## Follow-up
```

## Workflow

1. Inspect existing coverage and fixtures.
2. Define criteria and write the plan before interpreting results.
3. Re-evaluate strategy and matrix completeness.
4. Prepare isolated, reproducible setup.
5. Execute high-signal or gating cases first.
6. Preserve failure evidence and avoid contaminating later cases.
7. Add test code only when existing coverage cannot answer the objective.
8. Complete the report from actual evidence.
9. Inspect test-code and artifact diffs.

Reclassify to VALIDATION when a broad compatibility or release surface needs independently tracked
raw results.
