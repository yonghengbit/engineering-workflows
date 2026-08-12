# Debugging Workflow

Identify and prove the root cause of unexpected software behavior. Do not patch first and explain
later; a small eventual fix may require a non-trivial investigation.

## Establish the Symptom

1. State observed and expected behavior separately.
2. Identify the earliest known bad boundary, environment, and relevant version.
3. Obtain the smallest reliable reproduction available.
4. Preserve original errors, logs, traces, inputs, and commands before changing conditions.

If reproduction is unavailable, state what evidence exists and what is missing. Do not invent a cause
from an unverified symptom description.

Minimal instrumentation, diagnostic assertions, or an experimental patch may distinguish
hypotheses. Do not let the experiment silently become the production fix. For "find and fix," prove
the cause here before returning to the top-level policy for Development and later Testing.

## Choose Investigation Weight

### DIRECT

Use when the symptom is reliably reproduced, evidence points to one local cause, and one focused
check can confirm or reject it. Create no persistent artifact.

### SYSTEMATIC

Use when reproduction is difficult, the path is non-trivial, several causes are plausible, state or
timing matters, or work spans meaningful experiments.

Maintain `DEBUG.md`:

```markdown
# Debug

## Symptom
## Expected Behavior
## Reproduction
## Environment
## Evidence
## Hypotheses
| Hypothesis | Supporting Evidence | Contradicting Evidence | Next Experiment |
|---|---|---|---|
## Experiments
## Root Cause
## Fix Handoff
## Regression Verification
```

Keep it as a current evidence model, not a chronological transcript. Mark disproven hypotheses and
never rewrite experimental results to fit a later theory.

## Build and Test Hypotheses

```text
Symptom
 -> Reproduce
 -> Locate failing boundary
 -> Gather evidence
 -> Generate competing hypotheses
 -> Rank by explanatory power and test cost
 -> Run the smallest discriminating experiment
 -> Update the evidence model
 -> Prove root cause
```

Before an experiment, state which hypotheses it distinguishes, expected observations, changed and
controlled variables, and evidence to capture. Prefer boundary checks, bisection, controlled
substitution, focused traces, and state inspection over broad logging or speculative refactors.

## Evidence Rules

Separate:

```text
Observation  directly captured behavior
Inference    conclusion supported by observations
Hypothesis   plausible explanation still needing a test
Unknown      missing information that may affect the conclusion
```

A root cause is supported only when it explains the symptom and evidence, identifies the mechanism
and failing boundary, survives a discriminating or counterfactual test, and is not contradicted by a
simpler remaining hypothesis. Stack proximity and disappearance after an unrelated change are not
sufficient.

## Re-evaluate and Use Subagents

Re-evaluate after initial reproduction, each discriminating experiment, a symptom change, and before
declaring root cause. Switch DIRECT to SYSTEMATIC when the first focused hypothesis fails, hidden
state or timing appears, the suspected cause crosses boundaries, or several experiments are needed.

Use task-specific subagents only for independent evidence collection or competing hypothesis checks
with isolated inputs and explicit outputs. Keep reproduction control and causal synthesis with the
main agent. Do not create fixed "debug agents."

## Exit

Debugging is complete when root cause is supported and the next action is explicit. If blocked,
report missing evidence, attempts, current hypotheses, and the smallest unblocking observation.
"Could not reproduce" is a state, not a cause.

Return to the top-level transition policy with symptom, reproduction, environment, decisive evidence,
root cause, required change, constraints, regression needs, and open questions.
