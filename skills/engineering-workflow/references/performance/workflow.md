# Performance Workflow

Produce a reproducible performance conclusion supported by controlled measurements.

## Define the Claim

Before measuring, record the question or hypothesis, baseline and candidate, independent and
controlled variables, metrics and units, target environment and workload, and any acceptance or
practical-significance threshold.

Do not run the easiest benchmark if it cannot answer the question. Correctness checks remain part of
Performance because invalid output makes speed measurements meaningless. Return to the top-level
policy when product implementation or a separate code-understanding deliverable becomes primary.

## Select an Experiment Strategy

### CHECK

Use for a known benchmark or threshold with a fixed environment, workload, metric, and procedure.
Artifacts are optional when command and result fit in the completion report.

### COMPARISON

Use to compare a baseline and one or more candidates under controlled conditions.

### CHARACTERIZATION

Use to explain scaling, bottlenecks, sensitivity, or interactions across workload or environment
dimensions.

For COMPARISON and CHARACTERIZATION maintain:

```text
BENCHMARK_PLAN.md
results/
BENCHMARK_REPORT.md
```

Select from the claim, not runtime. Re-evaluate if the question or matrix changes.

## Plan Non-trivial Experiments

```markdown
# Benchmark Plan

## Question / Hypothesis
## Baseline and Candidates
## Correctness Preconditions
## Environment
## Workload
## Metrics and Units
## Controlled Variables
## Experiment Matrix
## Warmup
## Repetitions and Ordering
## Evidence Capture
## Analysis Method
## Acceptance Criteria
```

Capture versions, hardware, runtime settings, concurrency, input identity, and resource limits to the
degree they may affect the conclusion. Do not record secrets.

## Establish Correctness and Baseline

1. Verify baseline and candidates produce acceptable results.
2. Confirm the benchmark measures the intended operation.
3. Run a smoke measurement to detect setup faults.
4. Capture baseline before changing conditions.
5. Identify startup, compilation, saturation, and cache effects.

Reject or label measurements from functionally invalid candidates.

## Execute Controlled Measurements

- Change only declared independent variables.
- Use appropriate warmup and enough repetitions to expose variance.
- Interleave or randomize order when drift can bias results.
- Reset state when cache, allocator, storage, or service history matters.
- Preserve per-trial values, failures, timeouts, and rejected-run reasons.
- Avoid concurrent workloads unless concurrency is part of the design.
- Apply equivalent tuning to baseline and candidate unless asymmetry is the subject.

Raw results are the measurement source of truth. Never hand-edit them to match a summary.

## Analyze and Report

Report variability, not only the best run. Separate statistical noise from practical significance,
identify confounders, and bound conclusions to tested environment, workload, configuration,
concurrency, and metric definitions. Do not infer causal mechanisms from correlation alone.

```markdown
# Benchmark Report

## Summary
## Question / Hypothesis
## Environment and Workload
## Correctness Check
## Results
## Variability and Analysis
## Confounders / Deviations
## Conclusion
## Raw Evidence
## Follow-up
```

## Dynamic Subagents and Re-evaluation

Use task-specific subagents only for isolated benchmark infrastructure, independent environments, or
analysis cross-checks with explicit result formats. Serialize shared hardware or stateful experiments.
The main agent owns controls and final interpretation.

Re-evaluate after smoke testing, baseline capture, unexpectedly high variance, correctness failure,
and before the final claim.

## Exit

Complete when correctness preconditions hold, required trials are terminal or explicitly blocked,
raw evidence is preserved, and the conclusion is no broader than the data. Return to the top-level
policy for optimization implementation, mechanism investigation, or follow-up validation.
