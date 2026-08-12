# Testing Workflow

Determine whether software satisfies explicit correctness, compatibility, or acceptance criteria.
Reproducing a planned failure remains Testing; transition only when diagnosis or repair becomes the
deliverable.

## Define the Contract

State a falsifiable objective, system/change under test, PASS/FAIL/BLOCKED criteria, environment, and
baseline. Inspect existing tests and the real behavior boundary before inventing checks. Absence of
visible errors is not PASS unless the intended cases and expected signals were verified.

## Select and Load One Strategy

| Strategy | Use when | Artifacts |
|---|---|---|
| QUICK | a few direct checks; clear criteria/environment | none |
| STRUCTURED | bounded matrix, new regression/integration design, durable record | `TEST_PLAN.md`, `TEST_REPORT.md` |
| VALIDATION | broad release/compatibility surface or per-case audit evidence | `VALIDATION_PLAN.md`, `results/`, `VALIDATION_REPORT.md` |

Do not choose VALIDATION because a command is merely slow. Load exactly one:

```text
QUICK      -> references/testing/quick.md
STRUCTURED -> references/testing/structured.md
VALIDATION -> references/testing/validation.md
```

Re-evaluate after inspecting coverage, after a plan, when the matrix/environment expands, when a
failure changes the objective, and before the conclusion. Preserve evidence when upgrading; downgrade
only when early inspection proves the task simpler.

## Execute

- Record reproducible commands/procedures and relevant sanitized environment.
- Confirm intended cases ran and map each conclusion to a criterion.
- Separate product failure, harness failure, and unavailable infrastructure.
- Preserve first useful failure evidence before changing conditions.
- Avoid purposeless reruns; preserve raw results for VALIDATION.
- Inspect test-code and artifact diffs.

```text
PASS     all required criteria satisfied
FAIL     valid evidence contradicts a required criterion
BLOCKED  required evidence unavailable
MIXED    separable criteria have different outcomes
```

Never count BLOCKED as PASS. On a valid failure, preserve command, environment, expected/observed
results, and gating impact. Transition to Debugging for root-cause proof or Development for a known
change, then return for independent regression verification when needed.

Parallelize only isolated cases with clear ownership and separately captured results. Serialize
shared devices, mutable fixtures, rate-limited services, and order-dependent setup.

## Exit

Complete when every required case has a terminal state, evidence maps to criteria, and required
reports are current. Report strategy, objective, result, evidence, coverage, blocked/untested cases,
and next action.
