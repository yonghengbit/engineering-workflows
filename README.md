# Engineering Workflows for Codex

A small workflow framework for engineering tasks.

The project separates two different decisions:

1. **What kind of engineering task is this?**
2. **How much process does that task actually need?**

The first implemented workflow is `adaptive-development`, which classifies development work as:

```text
SMALL
MEDIUM
LARGE
VERY_LARGE
```

Development complexity is evaluated using:

```text
Scope + Uncertainty + Risk + Parallelism
```

and is re-evaluated after exploration, after planning/design, at major phase boundaries, before final verification, and when material complexity changes are discovered.

## Architecture

```text
User Task
   │
   ▼
Repository constraints
AGENTS.md / AGENTS.override.md
   │
   ▼
Primary Intent
   │
   ├── Development  ──> adaptive-development
   ├── Testing      ──> adaptive-testing          [planned]
   ├── Debugging    ──> systematic-debugging     [planned]
   ├── Performance  ──> performance-benchmark    [planned]
   ├── Investigation──> code-investigation       [planned]
   └── Review       ──> code-review              [planned]
                           │
                           ▼
                    workflow-specific process
```

The eventual `engineering-router` will only choose the primary workflow and coordinate transitions. It should not duplicate the detailed rules of the individual workflows.

## Current Status

```text
skills/
└── adaptive-development/       READY

proposals/
├── adaptive-testing.md         DESIGN ONLY
├── systematic-debugging.md     DESIGN ONLY
├── performance-benchmark.md    DESIGN ONLY
├── code-investigation.md       DESIGN ONLY
├── code-review.md              DESIGN ONLY
└── engineering-router.md       DESIGN ONLY
```

Only directories under `skills/` are intended to be installed as Codex skills.

Files under `proposals/` are intentionally not executable skills. They define boundaries and expected artifacts so that future skills can be implemented without prematurely fixing unstable behavior.

## Project Layout

```text
engineering-workflows/
├── README.md
├── AGENTS.md
├── skills/
│   └── adaptive-development/
│       ├── SKILL.md
│       ├── README.md
│       └── references/
│           ├── small.md
│           ├── medium.md
│           ├── large.md
│           └── very-large.md
├── docs/
│   ├── architecture.md
│   ├── workflow-contract.md
│   └── roadmap.md
└── proposals/
    ├── adaptive-testing.md
    ├── systematic-debugging.md
    ├── performance-benchmark.md
    ├── code-investigation.md
    ├── code-review.md
    └── engineering-router.md
```

## Core Principle: Primary Intent First

Classify a task by its **current primary objective**, not by whether code may eventually be changed.

Examples:

```text
"Implement a new scheduler option."
=> Development

"Verify this kernel for BF16 and FP16."
=> Testing

"vLLM crashes during REGISTER_KV_CACHE; find and fix it."
=> Debugging

"Compare native vLLM and LMCache TTFT/throughput."
=> Performance

"Trace how Scheduler allocates KV blocks."
=> Investigation

"Review this PR for correctness and compatibility."
=> Review
```

A task may transition between workflows when its objective changes.

Example:

```text
Testing
  │
  └── failure discovered
          ▼
      Debugging
          │
          └── root cause confirmed
                  ▼
              Development
                  │
                  └── fix completed
                          ▼
                       Testing
```

This is **workflow chaining**. It is preferable to making one giant skill responsible for every engineering activity.

## Installation

Install only the skills you want Codex to discover.

Repository scoped:

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/adaptive-development <repo>/.agents/skills/
```

User scoped:

```bash
mkdir -p "$HOME/.agents/skills"
cp -r skills/adaptive-development "$HOME/.agents/skills/"
```

Do not copy `proposals/` into `.agents/skills/`.

## Usage Today

Explicit invocation:

```text
$adaptive-development

Goal:
Implement <requirement>.
```

Or use normal development language and allow Codex to match the skill.

Project-specific engineering rules still belong in the target repository's `AGENTS.md`. This project defines reusable workflows; it does not replace repository-specific instructions.

## Evolution Rule

A new workflow moves through:

```text
idea
  -> proposals/<workflow>.md
  -> workflow boundary stabilizes
  -> implement SKILL.md + references
  -> validate on real tasks
  -> move to skills/<workflow>/
  -> optionally teach engineering-router about it
```

Do not implement the top-level router before the underlying workflows are stable enough to route to.
