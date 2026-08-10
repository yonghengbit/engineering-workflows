---
name: adaptive-development
description: Automatically classify software implementation tasks as small, medium, large, or very-large and apply the corresponding development workflow. Use for feature development, bug fixes, refactoring, backend integration, performance work, compatibility work, and other requests that require modifying a codebase. Do not use for pure code explanation, general Q&A, or review-only tasks that do not request implementation.
---

# Adaptive Development

Use this skill as the single entry point for non-trivial software implementation work.

The skill has two responsibilities:

1. classify the task by engineering complexity;
2. load and execute exactly one scale-specific workflow.

Do not estimate scale primarily from lines of code, number of files, or expected duration. Prefer cognitive complexity, architectural impact, risk, and decomposability.

Always use the lightest workflow that safely fits the task.

## 1. Repository Instructions First

Before implementation:

1. Follow all applicable `AGENTS.md` / `AGENTS.override.md` instructions already loaded by Codex.
2. Inspect the current repository and git state.
3. Locate the requested behavior and enough of its real call path to avoid classifying only from the user's wording.
4. Treat current code and git diff as the implementation source of truth.
5. User instructions override this workflow when they explicitly request a particular process, except where that would create a clear correctness or safety problem.

Do not perform a large investigation merely to classify the task. Perform enough exploration to identify the real scope and risk.

## 2. Classification Dimensions

Score four dimensions from 0 to 3.

### Scope

- `0 — Local`: one localized implementation area.
- `1 — Module`: several related files in one module or tightly coupled component.
- `2 — Cross-module`: multiple modules or important producer/consumer boundaries.
- `3 — Cross-system`: multiple subsystems, repositories, services, backends, or independent workstreams.

### Uncertainty

- `0 — Clear`: implementation and call path are already obvious.
- `1 — Investigation`: requires non-trivial call-chain or behavior analysis.
- `2 — Design`: multiple plausible implementation approaches exist.
- `3 — Architectural`: requires architecture exploration, prototyping, or major unresolved design decisions.

### Risk

- `0 — Low`: localized behavior with straightforward verification.
- `1 — Moderate`: existing behavior or compatibility must be preserved carefully.
- `2 — High`: materially touches important internal interfaces, public APIs, persistent formats, memory/data layout, performance-critical paths, concurrency, scheduling, resource lifetime, or backend compatibility.
- `3 — Critical`: materially touches incompatible migration, distributed protocol, security boundaries, broad persistence migration, rollout architecture, or several high-risk mechanisms together.

### Parallelism

- `0 — Atomic`: one coherent implementation flow.
- `1 — Phased`: several sequential implementation stages.
- `2 — Decomposable`: independent workstreams could reasonably be assigned separately.
- `3 — Program-scale`: multiple independently deliverable phases, repositories, or agents can progress concurrently.

## 3. Initial Classification

Calculate:

```text
complexity = scope + uncertainty + risk + parallelism
```

Initial mapping:

```text
0-2   -> SMALL
3-5   -> MEDIUM
6-8   -> LARGE
9-12  -> VERY_LARGE
```

This score is guidance. Architectural judgment and the minimum-level rules below take precedence.

## 4. Minimum-Level Rules

Classify at least as `LARGE` when the requested change materially changes one or more of:

- public API contracts;
- important cross-module producer/consumer contracts;
- persistent data formats;
- memory layout consumed across module boundaries;
- concurrency semantics;
- scheduling semantics;
- distributed communication protocols;
- allocator or resource-lifetime semantics;
- security-sensitive boundaries;
- compatibility across important runtime backends.

Do not escalate merely because these mechanisms appear somewhere in the call chain. The requested change must materially affect them.

Classify as `VERY_LARGE` when both are true:

1. the task spans multiple major subsystems or repositories;
2. it naturally decomposes into multiple independently verifiable workstreams or rollout phases.

Also consider `VERY_LARGE` when a single coherent `PLAN.md` can no longer represent the work effectively.

## 5. Select One Workflow

Load exactly one reference after classification:

```text
SMALL      -> references/small.md
MEDIUM     -> references/medium.md
LARGE      -> references/large.md
VERY_LARGE -> references/very-large.md
```

Do not load all four references by default.

Apply the common rules in this file plus the selected reference.

## 6. Reclassification Policy

Classification is provisional.

Do not rescore after every edit. Re-evaluate at fixed checkpoints and whenever material complexity changes are discovered.

### Checkpoint 1 — After Initial Exploration

This is the primary classification checkpoint.

After locating the relevant implementation and understanding the real call path, verify:

- actual module scope;
- producer/consumer boundaries;
- hidden compatibility requirements;
- interface changes;
- data-layout changes;
- concurrency or scheduling impact;
- protocol or persistence impact.

If the initial class is wrong, reclassify before significant implementation begins.

### Checkpoint 2 — After Planning or Design

For `MEDIUM`:

```text
exploration -> PLAN.md -> re-evaluate -> implementation
```

For `LARGE`:

```text
exploration -> DESIGN.md -> PLAN.md -> re-evaluate -> implementation
```

For `VERY_LARGE`:

```text
exploration -> DESIGN.md -> ROADMAP.md -> phase plans -> re-evaluate -> implementation
```

Check whether planning revealed:

- additional independent workstreams;
- major architectural choices;
- migration requirements;
- new subsystem dependencies;
- insufficient planning structure.

If a single plan no longer represents the task clearly, consider upgrading to `VERY_LARGE`.

### Checkpoint 3 — Major Phase Boundaries

After a meaningful implementation phase, perform a lightweight check:

- Did scope materially expand?
- Did an architectural assumption change?
- Did new high-risk behavior appear?
- Did new independent workstreams appear?
- Is the current workflow still sufficient?

If all answers are no, continue without full rescoring.

Do not re-evaluate after every file or small edit.

### Checkpoint 4 — Before Final Verification

Before full testing and final diff review, compare the actual implementation against the selected workflow:

- final change scope;
- actual affected contracts;
- compatibility surface;
- testing requirements;
- documentation requirements.

If the implementation grew beyond the workflow, add the minimum missing artifacts needed to accurately capture the design and current state.

### Event-Triggered Reclassification

Immediately re-evaluate, regardless of checkpoint, when discovering a material change such as:

- previously unknown cross-module dependencies;
- public or important internal interface redesign;
- producer/consumer contract changes;
- memory or persistent-data layout changes;
- concurrency semantic changes;
- scheduling semantic changes;
- resource-lifetime changes;
- distributed protocol changes;
- backend compatibility changes;
- migration or rollout requirements;
- multiple independently verifiable workstreams;
- a planning artifact that no longer represents the task clearly.

## 7. Escalation Procedure

### SMALL -> MEDIUM

Create the artifacts required by `references/medium.md`.

Preserve useful work already completed.

### MEDIUM -> LARGE

Do not keep expanding implementation under an undersized plan.

1. create or update `DESIGN.md`;
2. record the newly discovered architectural issue and the chosen decision;
3. revise `PLAN.md`;
4. continue using `references/large.md`.

### LARGE -> VERY_LARGE

1. preserve `DESIGN.md`;
2. create `ROADMAP.md`;
3. split the existing plan into phase-specific files under `plans/`;
4. create phase handoffs under `handoffs/` as work progresses;
5. continue using `references/very-large.md`.

Do not discard useful investigation or implementation during escalation.

## 8. Downgrade Procedure

Downgrade only when early exploration proves the task materially simpler than expected.

Do not delete useful artifacts solely to conform to a lower classification. Instead, stop maintaining artifacts that are no longer necessary.

Avoid repeated upgrade/downgrade oscillation. Once implementation has materially progressed, prefer keeping the current level unless it is clearly inadequate.

## 9. Common Implementation Rules

Regardless of scale:

- Understand existing behavior before modifying it.
- Trace real callers and consumers instead of inferring behavior from names.
- Prefer the smallest correct change.
- Reuse existing abstractions where appropriate.
- Avoid unrelated refactoring.
- Preserve compatibility unless the task explicitly changes it.
- Do not hide errors behind unsupported fallbacks.
- Avoid unexplained hardcoded values.
- Keep temporary debug instrumentation out of the final diff.
- Add tests proportional to the behavioral change.
- Run the strongest practical verification available.
- Record tests that could not be executed and why.
- Inspect the final git diff before completion.

## 10. Artifact Responsibilities

Each artifact has one purpose:

```text
AGENTS.md              = persistent repository rules and engineering conventions
DESIGN.md              = why the solution is designed this way
ROADMAP.md             = how a very large project is divided and coordinated
PLAN.md / plans/*      = what will be executed next
HANDOFF.md / handoffs/*= what the current implementation state is
```

Do not duplicate the same narrative across all artifacts.

Code and git diff remain the source of truth when documentation disagrees with implementation. Correct stale documentation when discovered.

## 11. Multi-Agent Policy

Do not use multiple agents merely because a task is `LARGE` or `VERY_LARGE`.

Parallelize only when workstreams have:

- clear ownership;
- weak dependencies;
- low edit-conflict probability;
- explicit inputs;
- explicit outputs;
- independent verification.

Good candidates include:

- independent codebase exploration;
- isolated backend implementation;
- test development;
- benchmark infrastructure;
- compatibility investigation.

Prefer sequential execution when one phase defines interfaces or contracts required by the next.

For `VERY_LARGE`, use `ROADMAP.md`, phase plans, and phase handoffs as coordination boundaries.

## 12. User Overrides

If the user explicitly says:

- "treat this as a small change";
- "use the large workflow";
- "do not create planning documents";

follow that preference where reasonable.

If the requested level is materially too small for correctness, state the discovered risk briefly and introduce only the minimum additional structure necessary.

Do not silently add large process overhead.

## 13. Completion Report

At completion, report concisely:

```text
Classification:
Why:
Changes:
Verification:
Remaining issues:
```

For `MEDIUM`, `LARGE`, and `VERY_LARGE`, ensure the relevant handoff state is current before finishing.

Do not produce a long development diary unless requested.

## 14. Classification Examples

### Example A — SMALL

Request:

> Add one optional CLI flag and pass it to an existing constructor.

Typical result:

```text
Scope       0
Uncertainty 0
Risk        0
Parallelism 0
=> SMALL
```

### Example B — MEDIUM

Request:

> Add another model loading mode using the existing loader architecture.

Requires registry changes, loader implementation, configuration, tests, and non-trivial call-chain inspection, but does not materially redesign loader contracts.

Typical result: `MEDIUM`.

### Example C — LARGE

Request:

> Support a new KV-cache layout across scheduler, connector, transfer context, and GPU kernel while preserving existing backends.

This materially affects cross-module contracts, memory layout, backend compatibility, and performance-sensitive code.

Minimum result: `LARGE`, even if the final diff is small.

### Example D — VERY_LARGE

Request:

> Port the complete caching subsystem to a new accelerator, including memory layout, transfer kernels, storage backend, multiprocessing integration, connector integration, tests, and benchmarks.

This contains multiple independently verifiable phases across several subsystems.

Result: `VERY_LARGE`.
