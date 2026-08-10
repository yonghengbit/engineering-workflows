# Proposal: engineering-router

## Status

Do not implement yet.

The router should be promoted only after the target workflows are stable.

## Primary Intent

Choose the workflow that matches the user's current engineering objective and coordinate explicit workflow transitions.

## Proposed Routing

```text
intentional behavior change -> adaptive-development
verification / pass-fail     -> adaptive-testing
unexpected behavior/root cause -> systematic-debugging
measurement/performance      -> performance-benchmark
understanding existing code  -> code-investigation
evaluate an existing change  -> code-review
```

## Mixed Tasks

Choose the current primary objective.

Example:

```text
"Test this kernel and fix it if it fails."

start -> adaptive-testing
failure -> systematic-debugging
root cause -> adaptive-development
fix -> adaptive-testing
```

Do not launch every potentially relevant workflow at once.

## Router Must Stay Thin

The router may:

- classify primary intent;
- choose a workflow;
- carry minimal transition context.

It must not:

- duplicate child workflow procedures;
- copy child scale models;
- own detailed artifacts;
- turn every task into a multi-agent orchestration.

## Open Design Questions

Before implementation, validate:

- whether explicit router invocation is better than relying on skill descriptions for most cases;
- how Codex should load the chosen child workflow;
- how much context should be carried across transitions;
- how mixed Development + Performance requests should be sequenced.
