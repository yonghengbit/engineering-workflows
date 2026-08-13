# Comparative Planning Benchmark

This benchmark compares planning behavior and context cost for three conditions:

- `native`: no custom workflow skill;
- `engineering-workflow`: this repository's canonical skill;
- `superpowers`: obra/superpowers v6.1.1.

It measures planning and evidence discipline across eight synthetic but realistic engineering
requests. It does not execute code, measure implementation success, or expose provider billing
tokens. Context and output cost use a deterministic `ceil(UTF-8 characters / 4)` proxy so runs are
comparable without claiming tokenizer accuracy.

Read [`protocol.md`](protocol.md) before collecting results. Score one run with:

```powershell
python tests/evals/comparative/score_comparison.py `
  tests/evals/comparative/results/<run>.jsonl `
  --skill-root <skill-root>
```

For `native`, omit `--skill-root`. Preserve raw JSONL, source commit, model/harness description,
date, rubric hash, and limitations with every published comparison.

The frozen v1 results and bounded interpretation are in [`report.md`](report.md). Source manifests
allow cost reproduction without retaining the temporary competitor checkout.
