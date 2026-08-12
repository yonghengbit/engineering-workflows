# Paired Forward Evaluation

This directory measures the marginal routing and evidence-discipline effect of
`engineering-workflow`; it does not claim end-to-end software correctness.

Run the same prompts with the same model in two fresh contexts:

- baseline: do not load or invoke a custom skill;
- treatment: explicitly load the repository's `engineering-workflow`.

Keep the rubric hidden from both runs. Save one JSON object per case in JSONL, preserving the raw
model output. Score both with:

```powershell
python tests/evals/score_run.py tests/evals/results/<run>.jsonl
```

The score covers routing, process proportionality, authorization, transitions, evidence, and
subagent discipline. `holdout-protocol.md` freezes the rubric hash before a separate prompt set is
run; do not tune the rubric after seeing those outputs. The earlier baseline/treatment pair is
exploratory because the scorer was normalized after collection.

Record model, reasoning effort, date, prompt set, and limitations alongside published results. Do
not generalize this score to implementation pass rate, latency, cost, or other models. Regex scoring
is deterministic but wording-sensitive; preserve raw outputs and failed checks.
