<div align="center">

<img src="assets/engineering-workflows-logo.svg" width="240" alt="Engineering Workflows logo">

# Engineering Workflows

**One entrypoint. Six workflows. Evidence-driven engineering.**

A goal-first workflow for AI coding agents that chooses the right amount of engineering process,
loads only what it needs, and treats verification as part of the result—not an afterthought.

[简体中文](README.md) | **English**

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-111827?style=flat-square)](https://agentskills.io)
[![Workflows](https://img.shields.io/badge/workflows-6-6366F1?style=flat-square)](#six-workflows-one-interface)
[![Progressive Loading](https://img.shields.io/badge/context-progressive_loading-0EA5E9?style=flat-square)](#why-this-exists)
[![Explicit First](https://img.shields.io/badge/invocation-explicit_first-8B5CF6?style=flat-square)](#one-minute-usage)
[![Holdout](https://img.shields.io/badge/holdout-43%2F48_%2889.6%25%29-10B981?style=flat-square)](#measured-scope)

[Why it exists](#why-this-exists) ·
[Install](#one-minute-installation) ·
[Use](#one-minute-usage) ·
[Architecture](docs/architecture.md) ·
[Full guide](docs/usage.md)

</div>

---

## Why this exists

Engineering tasks do not all need the same ceremony. A one-line fix should not pay the process cost of
a cross-subsystem redesign, while a performance claim or unknown crash should not be accepted without
controlled evidence.

Engineering Workflows gives a compatible coding agent one entrypoint and lets the current objective
determine the method:

| Principle | What it means |
|---|---|
| **Goal-first routing** | Describe the result you want; the framework selects the primary engineering intent. |
| **Proportional process** | SMALL work stays light; larger or higher-risk work earns planning, artifacts, or subagents only when useful. |
| **Evidence-driven completion** | Tests, benchmarks, root-cause proof, and review findings are treated as evidence with explicit PASS / FAIL / BLOCKED semantics. |

### Six workflows, one interface

| Intent | Primary question |
|---|---|
| **Development** | What software behavior should be intentionally changed? |
| **Testing** | Does the system satisfy explicit required criteria? |
| **Debugging** | What causes this unexpected behavior? |
| **Performance** | How fast is it, why, and under what controlled conditions? |
| **Investigation** | How does the existing system actually work? |
| **Review** | What problems or risks exist in this existing change or design? |

Invoke one skill using the host's syntax:

```text
Codex CLI / IDE  $engineering-workflow
ChatGPT          @engineering-workflow
Claude Code      /engineering-workflow
```

The framework handles routing, workflow-specific strategy, verification depth, optional artifacts,
and objective transitions.

---

## What it is

A portable Agent Skill for mixed, high-risk, and evidence-sensitive engineering work. It routes the
current result to the right method and applies only as much process as the task needs.

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
needed, one scale/strategy reference—not the whole library. Routine low-risk work can use the host
agent directly and pays no selected-skill body cost.

The core skill uses the open Agent Skills format: a `SKILL.md` entrypoint plus progressively loaded
references. `agents/openai.yaml` is an optional OpenAI integration for UI metadata and invocation
policy; non-OpenAI hosts can ignore it.

## Why Use It

- prove an unknown cause before repairing it;
- keep implementation verification inside Development instead of multiplying workflows;
- never count unavailable validation as PASS;
- require controlled, repeated evidence before performance claims;
- keep review read-only unless fixes are explicitly requested;
- avoid plans, handoffs, and subagents when they do not improve reliability.

## One-minute Installation

Codex repository scope:

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/engineering-workflow <repo>/.agents/skills/
```

Claude Code repository scope:

```bash
mkdir -p <repo>/.claude/skills
cp -r skills/engineering-workflow <repo>/.claude/skills/
```

Install only `engineering-workflow`; the six workflows are internal progressive references, not
separate skills. User-scope paths and other compatible hosts are covered in the
[full installation guide](docs/usage.md#2-安装).

## One-minute Usage

```text
$engineering-workflow

LMCache's REGISTER_KV_CACHE fails with a HIP error on DCU.
Find the root cause, fix it, and add a regression test.
```

The framework starts with Debugging, transitions to Development after root-cause proof, then uses
Testing for regression verification.

The skill is explicit-first. OpenAI hosts enforce this through `agents/openai.yaml`; other hosts use
their own invocation policy, so explicit selection is the portable behavior.

## Measured Scope

On a frozen eight-case holdout, the same inherited Codex configuration scored 35/48 (72.9%) without
the skill body and 43/48 (89.6%) with it: eight additional routing and evidence-discipline checks.
This is not a claim of general coding superiority. See `tests/evals/` for the frozen rubric hash, raw
JSONL, scorer, exploratory run, and limitations; the host did not expose a verifiable public model
slug.

A new three-way planning comparison covers the native agent, Engineering Workflows, and Superpowers
v6.1.1. On the same frozen 48-check rubric, this project scored **39/48 (81.2%)** versus Superpowers at
36/48 (75.0%), with 57.3% less loaded-input proxy and 52.4% less combined input/output proxy. The
native agent was cheapest but scored 30/48 (62.5%). These are single-run, planning-only character
proxies—not billed tokens or coding success rates. See the [full comparative report](tests/evals/comparative/report.md)
and raw JSONL.

![Three-way planning quality comparison](assets/benchmark-planning-quality.svg)

![Three-way token proxy comparison](assets/benchmark-token-proxy.svg)

## Layout

```text
engineering-workflows/
├── AGENTS.md
├── README.md
├── README.en.md
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

- [Full usage guide (Chinese)](docs/usage.md)
- [Architecture](docs/architecture.md)
- [Workflow author contract](docs/workflow-contract.md)
- [Roadmap](docs/roadmap.md)

Repository-specific build, test, style, and platform rules still belong in the target repository's
host instruction files, such as `AGENTS.md` or `CLAUDE.md`; this skill provides task-execution
methodology.
