# Workflow Contract

Every workflow in this project should define the same small set of boundaries.

This is a design contract for workflow authors. It is not a requirement that every skill create the same files.

## 1. Primary Intent

State the single question the workflow owns.

Examples:

```text
Development:
"What software behavior should be changed?"

Testing:
"Does the system satisfy these criteria?"

Debugging:
"What causes this unexpected behavior?"

Performance:
"How fast is it, why, and under what controlled conditions?"
```

## 2. Entry Conditions

Define when the workflow should be selected.

Do not select only from keywords. Prefer the user's current objective.

## 3. Non-Goals

Explicitly state adjacent work that belongs to another workflow.

Example:

Debugging may create minimal instrumentation, but broad implementation after root-cause confirmation belongs to Development.

## 4. Strategy / Scale

A workflow may define its own internal scale model.

Do not force `SMALL/MEDIUM/LARGE/VERY_LARGE` onto every workflow merely because Development uses it.

Possible examples:

```text
Development -> SMALL / MEDIUM / LARGE / VERY_LARGE
Testing     -> QUICK / STRUCTURED / VALIDATION
Debugging   -> DIRECT / SYSTEMATIC (possible)
```

Use only distinctions that materially change execution.

## 5. Artifacts

Artifacts must have a single purpose and should only exist when useful.

Examples:

```text
Development:
PLAN.md
DESIGN.md
HANDOFF.md

Testing:
TEST_PLAN.md
TEST_REPORT.md

Performance:
BENCHMARK_PLAN.md
BENCHMARK_REPORT.md
raw-results/
```

Do not create documents for ceremony.

## 6. Re-evaluation

Define when assumptions or classification must be reconsidered.

Prefer:

- a small number of fixed checkpoints;
- event-triggered re-evaluation when material new evidence appears.

Avoid rescoring after every small action.

## 7. Exit Conditions

A workflow should define what counts as completion.

Examples:

```text
Debugging:
root cause supported by evidence.

Testing:
planned cases executed or explicitly blocked;
results mapped to pass criteria.

Development:
requested behavior implemented;
relevant verification completed.
```

## 8. Workflow Transitions

Define legitimate next workflows.

A transition should include only the context the next workflow needs.

Suggested handoff payload:

```text
Objective:
Evidence / Findings:
Constraints:
Changed Files, if any:
Known Reproduction:
Required Next Action:
Verification Needed:
```

Do not force a new persistent document for every transition; use existing artifacts when they already contain the required state.

## 9. Source of Truth

For code behavior:

```text
current code / git diff
```

For measured behavior:

```text
raw test or benchmark output + environment
```

For workflow state:

```text
the workflow's designated plan/report/handoff artifact
```

Documentation must not override contradictory observed evidence.
