# Engineering Workflows for Codex

A single opt-in Codex skill for mixed, high-risk, and evidence-sensitive engineering work. It routes
the current result to the right method and applies only as much process as the task needs.

```text
User goal + repository constraints
    -> engineering-workflow
    -> Primary Intent
    -> one selected workflow
    -> workflow-specific strategy
    -> execution and verification
    -> optional transition when the objective changes
```

The six primary intents are Development, Testing, Debugging, Performance, Investigation, and Review.
Users normally describe the outcome they want; they do not need to choose a workflow, scale, artifact,
or number of agents.

The skill uses progressive loading and tested context budgets: it loads one intent workflow and, when
needed, one scale/strategy reference—not the whole library. Routine low-risk work can use native
Codex directly and pays no selected-skill body cost.

## Why Use It

- prove an unknown cause before repairing it;
- keep implementation verification inside Development instead of multiplying workflows;
- never count unavailable validation as PASS;
- require controlled, repeated evidence before performance claims;
- keep review read-only unless fixes are explicitly requested;
- avoid plans, handoffs, and subagents when they do not improve reliability.

## One-minute Installation

Repository scope:

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/engineering-workflow <repo>/.agents/skills/
```

User scope:

```bash
mkdir -p "$HOME/.agents/skills"
cp -r skills/engineering-workflow "$HOME/.agents/skills/"
```

Install only `engineering-workflow`; the six workflows are internal progressive references, not
separate skills.

## One-minute Usage

```text
$engineering-workflow

LMCache 的 REGISTER_KV_CACHE 在 DCU 环境报 HIP error，
请找到根因，修复，并补充回归测试。
```

The framework starts with Debugging, transitions to Development after root-cause proof, then uses
Testing for regression verification.

The skill is explicit-invocation by default. This avoids broad automatic activation on routine edits
and makes its context cost a user choice.

## Measured Scope

On a frozen eight-case holdout, the same inherited Codex configuration scored 35/48 (72.9%) without
the skill body and 43/48 (89.6%) with it: eight additional routing and evidence-discipline checks.
This is not a claim of general coding superiority. See `tests/evals/` for the frozen rubric hash, raw
JSONL, scorer, exploratory run, and limitations; the host did not expose a verifiable public model
slug.

## Layout

```text
engineering-workflows/
├── AGENTS.md
├── README.md
├── docs/
│   ├── architecture.md
│   ├── roadmap.md
│   ├── usage.md
│   └── workflow-contract.md
├── skills/
│   └── engineering-workflow/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           ├── development/
│           ├── testing/
│           ├── debugging/
│           ├── performance/
│           ├── investigation/
│           └── review/
└── tests/
```

## Documentation

- [完整使用指南](docs/usage.md)
- [架构设计](docs/architecture.md)
- [Workflow 作者契约](docs/workflow-contract.md)
- [路线图](docs/roadmap.md)

Repository-specific build, test, style, and platform rules still belong in the target repository's
`AGENTS.md`; this skill provides task-execution methodology.
