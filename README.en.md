<div align="center">

<img src="assets/engineering-workflows-logo.svg" width="240" alt="Engineering Workflows logo">

# Engineering Workflows

**One entrypoint. Six workflows. Teach your coding agent when to move fast—and when rigor is
non-negotiable.**

An engineering decision layer for Codex, Claude Code, and other Agent Skills-compatible tools. It
selects the right workflow, loads only the rules the current task needs, and finishes with evidence.

[简体中文](README.md) | **English**

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-111827?style=flat-square)](https://agentskills.io)
[![Workflows](https://img.shields.io/badge/workflows-6-6366F1?style=flat-square)](#how-it-works)
[![Planning](https://img.shields.io/badge/planning-39%2F48_%2881.2%25%29-10B981?style=flat-square)](#start-with-the-results)
[![Context](https://img.shields.io/badge/context-52.4%25_less_vs_Superpowers-0EA5E9?style=flat-square)](#start-with-the-results)

[Why](#coding-agents-have-capability-but-not-always-engineering-judgment) ·
[Evidence](#start-with-the-results) ·
[When to use it](#when-it-is-worth-using) ·
[Install](#one-minute-installation) ·
[Use](#one-minute-usage) ·
[Full guide](docs/usage.md)

</div>

---

## Coding agents have capability, but not always engineering judgment

A native agent can write code, yet it may not choose the right engineering process for each task:

- a small change can be over-planned, wasting context and time;
- an unknown crash can receive a speculative fix before its cause is proven;
- an unavailable test can be described ambiguously as successful validation;
- a performance claim can lack a baseline, repetition, or controlled variables;
- a read-only review can silently turn into unauthorized implementation.

Engineering Workflows does not replace an agent's coding ability. It supplies the missing decision
layer: identify the current objective, choose proportional process, and require evidence that matches
the conclusion.

> Keep small work light. Give risky work enough rigor. Say `BLOCKED` when verification is impossible
> instead of pretending the task is complete.

## Start with the results

The claims are backed by a frozen task set, rubric, raw outputs, source hashes, and a reproducible
scorer stored in this repository.

| Condition | Planning checks | Loaded-input proxy | Output proxy | Combined proxy |
|---|---:|---:|---:|---:|
| Native agent | 30/48 (62.5%) | **0** | **2,751** | **2,751** |
| **Engineering Workflows** | **39/48 (81.2%)** | 6,552 | 2,851 | **9,403** |
| Superpowers v6.1.1 | 36/48 (75.0%) | 15,338 | 4,428 | 19,766 |

![Three-way planning quality comparison](assets/benchmark-planning-quality.svg)

![Three-way token proxy comparison](assets/benchmark-token-proxy.svg)

Across this frozen set of eight planning-only cases, Engineering Workflows passed three more checks
than Superpowers while using **57.3% less loaded-input proxy** and **52.4% less combined proxy**.
The native agent remained cheapest, so the claim is not “a skill always saves tokens.” It is:
**when engineering discipline is warranted, get stronger planning with less workflow context.**

The token figures are `ceil(normalized characters / 4)`, not billed tokens. Each condition ran once,
and this benchmark does not measure real coding success. Read the [full report](tests/evals/comparative/report.md),
[frozen protocol](tests/evals/comparative/protocol.md), and [raw summary](tests/evals/comparative/results/summary.json).

## Why Engineering Workflows

| | Native agent | Engineering Workflows | Heavy multi-skill process |
|---|---|---|---|
| Process choice | Depends on the prompt and model habits | **Explicit routing by current objective** | Often forces a prescribed sequence |
| Context cost | Lowest | **One workflow plus an optional strategy, loaded on demand** | May load several skills in sequence |
| Small tasks | Fast, but discipline varies | **Stays light; no mandatory plan or subagent** | Can carry fixed ceremony cost |
| High-risk tasks | Users must supply constraints | **Explicit gates for causes, validation, and performance evidence** | Rigorous, but potentially heavier |
| Mixed objectives | Activities can blur together | **Transitions only when the primary deliverable changes** | Can become a multi-process chain |
| Completion semantics | Depends on agent wording | **Auditable PASS / FAIL / BLOCKED** | Depends on each skill's contract |

This is not a longer generic prompt and it does not force a plan for every request. The entrypoint only
routes. Detailed rules load progressively. Supporting activity does not cause unnecessary workflow
switches, and plans, artifacts, or subagents are used only when they improve reliability.

## When it is worth using

Explicitly invoke it for:

- unknown failures, concurrency problems, and evidence-poor debugging;
- cross-module development, migrations, and high-risk behavior changes;
- release gates, acceptance testing, and validation with potentially unavailable infrastructure;
- performance benchmarks, regression isolation, and reproducible optimization claims;
- read-only investigation or review, and mixed tasks whose primary objective may change.

Use the native agent directly for:

- low-risk routine changes with an obvious intent and validation path;
- explanation, rewriting, or simple mechanical operations.

That is why the project is **explicit-first**: workflow context is paid only when it has a reason to
improve the result.

## How it works

```text
User goal + repository constraints
    -> engineering-workflow router
    -> one primary intent
    -> one workflow
    -> scale / strategy loaded when needed
    -> execution and verification
    -> transition only when the primary objective changes
```

| Intent | Question it answers |
|---|---|
| **Development** | What software behavior should be intentionally changed? |
| **Testing** | Does the system satisfy explicit acceptance criteria? |
| **Debugging** | What causes the unexpected behavior? |
| **Performance** | How fast is it, why, and under what controlled conditions? |
| **Investigation** | How does the existing system actually work? |
| **Review** | What problems or risks exist in the current change or design? |

The core skill follows the open Agent Skills format: one `SKILL.md` entrypoint and progressively loaded
references. `agents/openai.yaml` is an optional OpenAI integration; other compatible hosts can ignore it.

## One-minute installation

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

Install only `engineering-workflow`. The six workflows are internal references, not six independent
skills. User-scope paths, Windows commands, and other compatible hosts are covered in the
[full installation guide](docs/usage.md#2-安装).

## One-minute usage

Invoke the skill using the host's syntax, then describe the result you want:

```text
Codex CLI / IDE  $engineering-workflow
ChatGPT          @engineering-workflow
Claude Code      /engineering-workflow
```

```text
$engineering-workflow

LMCache's REGISTER_KV_CACHE fails with a HIP error on DCU.
Find the root cause, fix it, and add a regression test.
```

The framework starts in Debugging and transitions to Development after the cause is proven. It moves
to Testing only if the primary deliverable becomes an independent acceptance conclusion. You describe
the outcome; the framework chooses the workflow, scale, artifacts, and agent count.

## Documentation and repository

- [Full usage guide (Chinese)](docs/usage.md)
- [Comparative benchmark and reproduction](tests/evals/comparative/README.md)
- [Architecture](docs/architecture.md)
- [Workflow author contract](docs/workflow-contract.md)
- [Roadmap](docs/roadmap.md)

Repository-specific build, test, style, and platform rules still belong in the target repository's
`AGENTS.md`, `CLAUDE.md`, or equivalent host instructions. This skill provides reusable execution
methodology only.
