# Investigation Workflow

Build an evidence-backed mental model of existing software and answer the user's question without
making modification or evaluation the primary objective.

## Define the Question and Boundary

1. Restate the question and what counts as an answer.
2. Identify repository, revision, configuration, and runtime path.
3. Choose the narrowest real entry point that exposes the behavior.
4. Inspect current code and git state before trusting documentation.

Do not turn orientation into a repository-wide survey. Focused read-only commands or tests may verify
facts without changing workflow ownership.

## Trace Real Boundaries

Start from a CLI/API boundary, event handler, public method, test, data producer, or persisted format:

```text
entry point
 -> dispatch / ownership
 -> state and data transformations
 -> producer-consumer boundaries
 -> side effects / lifecycle
 -> externally visible result
```

Inspect definitions and actual callers or consumers. Search tests and configuration for contracts
not obvious from names. Verify documentation against code.

## Label Knowledge

```text
Verified fact  directly supported by code, tests, output, or repository metadata
Inference      conclusion derived from verified facts
Hypothesis     plausible but unverified
Unknown        material question not answered by available evidence
```

Attach file and symbol references to important facts. State configuration-dependent branches. Do not
present comments, names, stale docs, or unexecuted test intent as observed runtime behavior.

## Proportional Artifact

Create no artifact for a bounded investigation. For large, multi-session, or handoff-sensitive work,
maintain:

```markdown
# Investigation

## Question
## Scope
## Entry Points
## Verified Findings
## Data / Control Flow
## Inferences
## Hypotheses
## Unknowns
## Answer
## Important Files
```

Keep it as a current evidence model, not a search log.

## Dynamic Subagents and Stop Condition

Use task-specific subagents only for independent subsystems or call paths with explicit questions and
evidence requirements. The main agent integrates findings and resolves contradictions. Reading code
alone is never a reason to transition into Investigation from another workflow.

Stop when the question is answered with sufficient evidence. If static evidence cannot answer it,
identify the smallest runtime observation needed. Return to the top-level policy when the requested
deliverable becomes implementation, root-cause proof, testing, measurement, or review.

Report the answer, verified path, evidence, inferences, unknowns or configuration branches, and any
next action.
