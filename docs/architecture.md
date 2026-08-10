# Architecture

## 1. Why the Framework Has Two Axes

Engineering tasks have at least two independent properties:

```text
Task Type  = what is the immediate engineering objective?
Task Scale = how much structure does this objective require?
```

Treating these as one dimension causes process mismatch.

Examples:

- a one-command regression check is Testing, but tiny;
- a cross-platform validation campaign is also Testing, but large;
- a crash investigation may end in a two-line fix, but its primary workflow is Debugging until root cause is established;
- a 30-line scheduler change can still be Large Development if it changes scheduling semantics.

Therefore the framework first selects **primary intent**, then lets the selected workflow choose its own scale or strategy.

## 2. Layers

```text
Layer 0: Repository Rules
AGENTS.md / AGENTS.override.md
        │
        ▼
Layer 1: Primary Intent
Development / Testing / Debugging /
Performance / Investigation / Review
        │
        ▼
Layer 2: Workflow Strategy
Examples:
Development -> SMALL / MEDIUM / LARGE / VERY_LARGE
Testing     -> QUICK / STRUCTURED / VALIDATION (planned)
        │
        ▼
Layer 3: Execution Artifacts
PLAN, DESIGN, TEST_PLAN, DEBUG notes, benchmark results, etc.
        │
        ▼
Layer 4: Verification and Transition
Complete current workflow or transition to another one
```

## 3. Primary Workflows

### Development

Goal: change software behavior intentionally.

Current implementation: `skills/adaptive-development/`.

### Testing

Goal: determine whether behavior satisfies explicit criteria.

The workflow should optimize for test objective, matrix, baseline, environment, reproducibility, pass/fail criteria, and reporting.

### Debugging

Goal: identify and prove the root cause of an unexpected symptom.

The workflow should be evidence- and hypothesis-driven. Code modification is downstream of root-cause confirmation, not the initial objective.

### Performance

Goal: measure, explain, or improve performance under controlled conditions.

The workflow should emphasize baseline, controlled variables, metrics, warmup, repetitions, environment, raw results, and statistical interpretation.

### Investigation

Goal: understand an implementation, call path, architecture, behavior, or technical question.

The workflow should distinguish verified facts, inference, hypotheses, and open questions.

### Review

Goal: evaluate an existing change or design.

The workflow should prioritize findings by severity and avoid silently turning review into implementation unless requested.

## 4. Workflow Chaining

A task can change primary intent during execution.

Transitions should happen when the objective changes, not simply because another activity is present.

Common chains:

```text
Testing -> Debugging -> Development -> Testing
```

```text
Performance -> Investigation -> Development -> Performance
```

```text
Review -> Development -> Testing
```

A transition should preserve relevant evidence and constraints, but the new workflow should own the next phase.

## 5. Why the Router Comes Last

The router only has value when it can route to stable workflows.

Implementing it too early tends to create:

- duplicated rules;
- ambiguous ownership;
- over-routing;
- a monolithic skill that becomes difficult to evolve.

For now, users may invoke a workflow explicitly or rely on Codex skill matching.

Once at least Testing and Debugging are stable, the `engineering-router` can be implemented with real routing targets.
