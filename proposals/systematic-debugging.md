# Proposal: systematic-debugging

## Primary Intent

Identify and prove the root cause of unexpected behavior.

## Core Principle

Do not patch first and explain later.

Prefer:

```text
Symptom
 -> Reproduce
 -> Evidence
 -> Hypotheses
 -> Rank hypotheses
 -> Minimal discriminating experiment
 -> Root cause
 -> Fix
 -> Regression verification
```

## Artifacts

For simple, obvious issues: no persistent artifact.

For non-trivial investigations: optionally maintain `DEBUG.md`:

```markdown
# Debug

## Symptom
## Expected Behavior
## Reproduction
## Evidence
## Hypotheses
## Experiments
## Root Cause
## Fix
## Verification
```

## Rules

- Separate observation from inference.
- Prefer experiments that distinguish between competing hypotheses.
- Avoid broad code changes before root cause is supported.
- Temporary instrumentation should be minimal and removed unless intentionally retained.

## Expected Transitions

```text
root cause confirmed + code change needed
    -> adaptive-development

fix completed
    -> adaptive-testing

performance-only root cause
    -> performance-benchmark or investigation as appropriate
```
