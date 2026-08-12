# Engineering Workflows for Codex

A single Codex skill that routes an engineering goal to the right method and applies only as much
process as the task needs.

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
needed, one scale/strategy reference—not the whole library.

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
