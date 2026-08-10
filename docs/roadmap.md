# Roadmap

The framework should grow from concrete workflows upward, not from a generic router downward.

## Phase 1 — Development

Status: **implemented**

```text
skills/adaptive-development/
```

Capabilities:

- four-scale development classification;
- controlled re-evaluation;
- scale-specific planning artifacts;
- Very Large phase decomposition;
- optional multi-agent boundaries.

## Phase 2 — Testing and Debugging

Status: **next**

Implement:

```text
adaptive-testing
systematic-debugging
```

Why first:

These two workflows complete the normal correctness loop around Development:

```text
Development -> Testing
Testing failure -> Debugging
Debugging root cause -> Development
Development fix -> Testing
```

### adaptive-testing target

Likely strategies:

```text
QUICK
STRUCTURED
VALIDATION
```

Expected artifacts:

```text
QUICK:
  none

STRUCTURED:
  TEST_PLAN.md
  TEST_REPORT.md

VALIDATION:
  VALIDATION_PLAN.md
  results/*
  VALIDATION_REPORT.md
```

### systematic-debugging target

Core loop:

```text
Symptom
 -> Reproduce
 -> Evidence
 -> Hypotheses
 -> Minimal discriminating experiment
 -> Root cause
 -> Fix handoff
 -> Regression verification
```

Use a persistent `DEBUG.md` only for non-trivial investigations.

## Phase 3 — Performance

Status: planned

Implement:

```text
performance-benchmark
```

Key properties:

- explicit hypothesis;
- stable baseline;
- controlled variables;
- environment capture;
- warmup and repetitions;
- correctness before speed;
- raw results preserved;
- conclusion tied to measured evidence.

## Phase 4 — Investigation and Review

Status: planned

Implement:

```text
code-investigation
code-review
```

These workflows are useful, but they do not need to block the core Development/Testing/Debugging loop.

## Phase 5 — Engineering Router

Status: intentionally deferred

Implement only after the underlying workflows have been validated on real tasks.

Responsibilities:

```text
identify primary intent
 -> choose one workflow
 -> coordinate explicit transitions
```

The router must remain thin and must not duplicate child workflow rules.

## Promotion Criteria

A proposal can move from `proposals/` to `skills/` when:

- its primary intent is unambiguous;
- its non-goals are explicit;
- artifact rules are stable;
- it has a usable re-evaluation model;
- workflow transitions are defined;
- it has been tested against representative real tasks.
