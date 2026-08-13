# Comparative Planning Benchmark v1 — Results

Date: 2026-08-13

Rubric SHA-256:
`BF77080CF79DC4719EAC94271F36FC205418CBE454897F52369366CE6DC85471`

## Result

| Condition | Planning checks | Loaded-input proxy | Output proxy | Combined proxy |
|---|---:|---:|---:|---:|
| Native agent | 30/48 (62.5%) | 0 | 2,751 | 2,751 |
| Engineering Workflows | **39/48 (81.2%)** | **6,552** | **2,851** | **9,403** |
| Superpowers v6.1.1 | 36/48 (75.0%) | 15,338 | 4,428 | 19,766 |

![Planning quality comparison](../../../assets/benchmark-planning-quality.svg)

![Token proxy comparison](../../../assets/benchmark-token-proxy.svg)

In this single frozen run, Engineering Workflows passed three more planning checks than Superpowers
(+6.2 percentage points) while using 57.3% less loaded-input proxy, 35.6% less output proxy, and
52.4% less combined proxy. It was the only skill condition above 80%.

The native agent was cheapest and already strong on several cases. Engineering Workflows added nine
checks (+18.7 percentage points) but also added 6,652 combined proxy tokens. The evidence therefore
supports a narrower claim: use the workflow when routing, authorization boundaries, or evidence
discipline justify added context; do not invoke it for every routine task.

## What Was Tested

Eight planning-only requests covered:

- a backward-compatible small CLI change;
- a release gate with unavailable infrastructure;
- an intermittent concurrent GPU failure;
- a read-only compatibility review;
- a controlled p99 comparison;
- a tightly coupled shared-contract migration;
- a read-only scheduler lifecycle investigation;
- a test → conditional diagnosis → repair → retest chain.

Three fresh subagents inherited the same host configuration. The native condition loaded no custom
skill. Engineering Workflows loaded its router plus only selected workflow/strategy references.
Superpowers started with `using-superpowers` and followed its required applicable sub-skills. Agents
returned the exact files they read, and the scorer counted each unique loaded file once across the
eight-case run.

The competitor was pinned to [obra/superpowers v6.1.1](https://github.com/obra/superpowers/tree/v6.1.1)
at commit `d884ae04edebef577e82ff7c4e143debd0bbec99`. Source manifests preserve normalized character
counts and SHA-256 hashes for every loaded file.

## Reproduce

```powershell
python tests/evals/comparative/score_comparison.py `
  tests/evals/comparative/results/native-inherited-agent-2026-08-13.jsonl

python tests/evals/comparative/score_comparison.py `
  tests/evals/comparative/results/engineering-workflow-inherited-agent-2026-08-13.jsonl `
  --source-manifest tests/evals/comparative/manifests/engineering-workflow.json

python tests/evals/comparative/score_comparison.py `
  tests/evals/comparative/results/superpowers-v6.1.1-inherited-agent-2026-08-13.jsonl `
  --source-manifest tests/evals/comparative/manifests/superpowers-v6.1.1.json
```

## Limitations

- The tasks tested planning, not executable coding success, latency, or defect rate.
- The host exposed no verifiable public model slug, exact reasoning setting, or billed token usage.
- `ceil(characters / 4)` is deterministic but is only a token proxy.
- Regex scoring is wording-sensitive. For example, semantically relevant text in a different output
  field may miss a check, and the native run used `agents: []`, which did not match textual
  no-agent patterns.
- Each condition ran once. Sampling variance and cross-model behavior remain unknown.
- The rubric reflects this project's priorities: proportional process, authorization boundaries,
  controlled evidence, and avoiding unnecessary artifacts or parallelism.
- Superpowers intentionally optimizes for mandatory design/TDD discipline. Its additional context
  and artifacts can be valuable on tasks where maximum ceremony is preferred.

These results justify further executable, repeated, and cross-model evaluation. They do not justify
claims that Engineering Workflows can plan every task, always saves tokens, or is universally better.
