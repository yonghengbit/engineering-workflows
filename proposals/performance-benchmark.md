# Proposal: performance-benchmark

## Primary Intent

Measure, compare, explain, or validate system performance under controlled conditions.

## Required Discipline

Every meaningful performance claim should identify:

- hypothesis;
- baseline;
- changed variable;
- controlled variables;
- metrics;
- environment;
- warmup;
- repetition policy;
- raw results;
- interpretation.

Correctness must be established before comparing speed.

## Suggested Artifacts

For non-trivial work:

```text
BENCHMARK_PLAN.md
BENCHMARK_REPORT.md
results/
```

## Typical Flow

```text
Question
 -> Hypothesis
 -> Baseline
 -> Experimental controls
 -> Correctness check
 -> Warmup
 -> Repeated measurement
 -> Analyze variance
 -> Explain result
 -> Conclusion
```

## Expected Transitions

```text
unexpected result -> code-investigation or systematic-debugging
optimization needed -> adaptive-development
optimization completed -> performance-benchmark
```
