# Proposal: adaptive-testing

## Primary Intent

Determine whether a system or change satisfies explicit correctness, compatibility, or validation criteria.

## Non-Goals

- Root-cause analysis of failures belongs to `systematic-debugging`.
- Implementing fixes belongs to `adaptive-development`.
- Performance claims that require controlled benchmarking belong to `performance-benchmark`.

## Proposed Strategies

### QUICK

Use for a small number of direct checks or existing tests.

Artifacts: none.

Flow:

```text
objective -> environment check -> execute -> interpret -> PASS/FAIL/BLOCKED
```

### STRUCTURED

Use for a meaningful test matrix, new test design, cross-config checks, or regression work.

Artifacts:

```text
TEST_PLAN.md
TEST_REPORT.md
```

`TEST_PLAN.md` should capture objective, environment, matrix, baseline, pass criteria, and procedure.

`TEST_REPORT.md` should capture summary, results, failures, observations, conclusion, and follow-up.

### VALIDATION

Use for broad compatibility/correctness campaigns across models, platforms, configurations, or subsystems.

Artifacts:

```text
VALIDATION_PLAN.md
results/*
VALIDATION_REPORT.md
```

## Re-evaluation

Re-evaluate when the matrix expands materially, a failure requires root-cause investigation, or performance becomes a primary claim.

## Expected Transitions

```text
Testing failure -> systematic-debugging
Fix required    -> adaptive-development
Performance question -> performance-benchmark
```
