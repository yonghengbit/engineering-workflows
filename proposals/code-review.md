# Proposal: code-review

## Primary Intent

Evaluate an existing change or design for correctness, compatibility, maintainability, test coverage, and relevant performance or safety risks.

## Non-Goal

Do not silently turn review into implementation. Modify code only when explicitly requested or when the workflow is transitioned to Development.

## Review Order

```text
intent
 -> diff
 -> correctness
 -> interfaces/compatibility
 -> failure paths
 -> tests
 -> performance/resource risks
 -> findings
```

## Findings

Prefer severity-oriented results such as:

```text
BLOCKER
MAJOR
MINOR
NIT
```

or:

```text
Must Fix
Should Fix
Optional
```

Each finding should point to concrete evidence and impact.

## Expected Transitions

```text
requested fixes -> adaptive-development
uncertain defect -> systematic-debugging
missing validation -> adaptive-testing
```
