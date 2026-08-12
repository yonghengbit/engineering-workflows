# Review Workflow

Evaluate an existing change or design for concrete correctness, compatibility, security,
maintainability, test, performance, and resource risks. Do not silently implement fixes.

## Establish Scope

1. Identify the exact diff, commits, design, or files under review.
2. Determine intended behavior from the request and repository evidence.
3. Inspect repository and git state without overwriting user work.
4. Identify relevant callers, consumers, tests, and compatibility boundaries.

Use the narrowest evidence-backed scope when the target is ambiguous. Read-only commands and focused
tests may validate a finding without changing workflow ownership.

## Review in Risk Order

```text
intent and scope
 -> changed behavior and invariants
 -> callers / consumers / interfaces
 -> failure, cleanup, and rollback paths
 -> data, state, concurrency, and security effects
 -> compatibility and migration
 -> tests and observability
 -> performance / resource risks
 -> maintainability where it affects future correctness
```

Trace changed values across boundaries and inspect surrounding code. Consider negative paths,
partial failure, retries, repeated calls, empty inputs, boundary values, and relevant configuration
branches. Do not prioritize formatting owned by automated tools.

## Validate Findings

Before reporting a finding:

- identify the changed line or tight range that introduced or exposed it;
- verify surrounding path and preconditions;
- describe a concrete trigger and impact;
- check whether existing guards or tests prevent it;
- distinguish demonstrated defects from uncertainty needing investigation.

Do not report speculation as fact.

## Prioritize

```text
BLOCKER  unsafe to merge or deploy; catastrophic or security-critical impact is credible
MAJOR    material correctness, compatibility, data, availability, or regression defect
MINOR    bounded defect or robustness gap worth fixing
NIT      optional polish; omit unless exhaustive style feedback is requested
```

Severity reflects impact and likelihood, not edit size.

## Write Actionable Findings

```text
[SEVERITY] Short title
Location: file and tight line range
Trigger: concrete condition
Impact: what breaks or becomes unsafe
Evidence: relevant call path, contract, or test result
Recommendation: smallest direction that resolves the issue
```

Evaluate tests against changed behavior and important failure paths. A missing test is a finding only
when it leaves material behavior unprotected. Distinguish environment blockage from product failure.

## Dynamic Subagents and Completion

Use task-specific subagents only for independent review surfaces with low overlap and explicit scope.
The main agent deduplicates findings, reconciles severity, and owns the final review. Do not create a
fixed reviewer taxonomy.

Lead the response with findings ordered by severity, then open questions or assumptions, followed by
a brief scope and test summary. If no actionable findings exist, say so and state residual risks or
untested areas. Return to the top-level policy when selected fixes, root-cause proof, validation, or
measurement becomes the primary objective.
