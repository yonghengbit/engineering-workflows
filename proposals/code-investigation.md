# Proposal: code-investigation

## Primary Intent

Understand existing code, architecture, call paths, data flow, lifecycle, or technical behavior without making implementation the primary objective.

## Core Output Model

Distinguish:

```text
Verified fact
Inference
Hypothesis
Unknown / open question
```

## Typical Flow

```text
Question
 -> locate real entry point
 -> trace callers/consumers
 -> inspect state/data flow
 -> verify conclusions in code/tests
 -> build mental model
 -> conclusions + open questions
```

## Artifacts

Usually none.

For a large or multi-session investigation, use `INVESTIGATION.md`.

## Expected Transitions

```text
design/change requested -> adaptive-development
unexpected behavior discovered -> systematic-debugging
performance hypothesis discovered -> performance-benchmark
```
