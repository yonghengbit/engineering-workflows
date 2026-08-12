# Architecture

## 1. Canonical Entry Point

The framework exposes one installable skill:

```text
skills/engineering-workflow/
```

The top-level `SKILL.md` is a routing policy used by the current Codex main agent. It is not a
separate router agent and does not execute child procedures itself.

```text
User Prompt + Repository Context + AGENTS.md constraints
    -> engineering-workflow
    -> Primary Intent routing
    -> one workflow reference
    -> workflow-specific strategy or scale
    -> execution + verification
    -> optional transition
```

This prevents seven peer skills from competing through implicit skill matching and lets users express
engineering goals without naming an activity type.

## 2. Repository Rules and Workflow Method

`AGENTS.md` owns repository-specific constraints: build commands, test conventions, editable paths,
style, platforms, and safety rules.

`engineering-workflow` owns task methodology: primary intent, process depth, artifacts, verification,
dynamic subagent decisions, and objective transitions.

Repository instructions constrain every workflow but do not route the task.

## 3. Primary Intent Routing

The router asks which result the user wants now:

| Intent | Owning question |
|---|---|
| Development | What software behavior should be intentionally changed? |
| Testing | Does the system satisfy explicit required criteria? |
| Debugging | What causes this unexpected behavior? |
| Performance | How fast is it, why, and under what controlled conditions? |
| Investigation | How does the existing system actually work? |
| Review | What problems or risks exist in this existing change or design? |

The routing policy uses unknown failure, performance, understanding, review, explicit verification,
then intentional change as precedence for genuinely mixed requests. This is a goal-based tie-breaker,
not keyword scoring.

Once selected, the router stops and loads exactly one reference:

```text
references/<intent>/workflow.md
```

## 4. Progressive Loading

The canonical skill does not load all procedures at startup.

```text
route Debugging
    -> load references/debugging/workflow.md only

route Development
    -> load references/development/workflow.md
    -> classify LARGE
    -> load references/development/large.md only
```

Testing uses the same two-stage pattern for QUICK, STRUCTURED, or VALIDATION. This keeps routing
context small while retaining detailed execution rules.

### Context budgets

Progressive loading only helps if each loaded layer stays concise. Structural tests therefore enforce
character budgets as a deterministic proxy for token cost:

- top-level `SKILL.md`: at most 5,000 characters;
- common SMALL Development path: at most 9,200 loaded characters;
- common QUICK Testing path: at most 8,500 loaded characters;
- each intent workflow has its own bounded size.

At roughly four English characters per token, the current SMALL Development path is about 2.2k
tokens and QUICK Testing about 2.0k tokens, excluding repository context and tool output. This proxy
is intentionally approximate; its purpose is preventing silent prompt growth, not predicting billing.

The design follows mature skill practices: the
[Anthropic skill creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
uses metadata → `SKILL.md` → on-demand resources; the
[OpenAI skill examples](https://github.com/openai/skills) emphasize reusable scoped resources; and
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/blob/main/docs/skill-anatomy.md)
explicitly recommends removing sections that do not change agent behavior. We keep the evidence and
systematic discipline seen in [obra/superpowers](https://github.com/obra/superpowers), without making
its full mandatory development chain the default for small tasks.

## 5. Task Type and Strategy Are Separate

```text
Development  -> SMALL / MEDIUM / LARGE / VERY_LARGE
Testing      -> QUICK / STRUCTURED / VALIDATION
Debugging    -> DIRECT / SYSTEMATIC
Performance  -> CHECK / COMPARISON / CHARACTERIZATION
Investigation-> proportional artifact only
Review       -> findings-first output
```

No common scale is forced onto every workflow. Strategy exists only when it materially changes
execution.

## 6. Supporting Activity and Transitions

Reading code, running tests, measuring a local baseline, or adding diagnostic instrumentation may be
supporting activity inside the current workflow. Ownership changes only when the primary deliverable
changes.

```text
Testing -> Debugging -> Development -> Testing
Performance -> optional Investigation -> Development -> Performance
Review -> Development -> Testing
Investigation -> Development
```

Transitions load the destination reference on demand and carry a compact payload containing current
objective, verified evidence, constraints, changed files, reproduction or procedure, next action, and
verification needs. A transition does not require a new Markdown artifact.

## 7. Proportional Artifacts

The router creates no artifacts. Each selected workflow decides:

| Workflow / Strategy | Artifacts |
|---|---|
| Development / SMALL | none |
| Development / MEDIUM | `PLAN.md`, `HANDOFF.md` |
| Development / LARGE | `DESIGN.md`, `PLAN.md`, `HANDOFF.md` |
| Development / VERY_LARGE | `DESIGN.md`, `ROADMAP.md`, `plans/*`, `handoffs/*` |
| Testing / QUICK | none |
| Testing / STRUCTURED | `TEST_PLAN.md`, `TEST_REPORT.md` |
| Testing / VALIDATION | `VALIDATION_PLAN.md`, `results/*`, `VALIDATION_REPORT.md` |
| Debugging / DIRECT | none |
| Debugging / SYSTEMATIC | `DEBUG.md` |
| Performance / non-trivial | `BENCHMARK_PLAN.md`, `results/*`, `BENCHMARK_REPORT.md` |
| Investigation / complex | `INVESTIGATION.md` |
| Review | findings in response |

## 8. Dynamic Subagents

Routing never creates agents. After selection, the workflow and current repository determine whether
independent work exists. Parallel work requires clear ownership, weak dependencies, low edit
conflict, explicit inputs and outputs, and independent verification.

Roles are derived from the task, such as two actual backend paths or an isolated test harness. The
framework maintains no fixed specialist taxonomy, and LARGE does not imply multi-agent execution.

## 9. Source of Truth

```text
implementation   current code + git diff
runtime behavior actual test / benchmark / runtime evidence
workflow state   designated workflow artifacts
```

Observed evidence overrides stale documentation; stale documentation should then be corrected.

## 10. Compatibility Decision

The repository is still first-version and has no documented external dependency on the old peer skill
names. The v2 migration therefore removes them instead of adding wrappers that would remain alternate
implicit entry points. If compatibility becomes necessary later, wrappers may only pin Primary Intent
and must delegate all procedure to this canonical skill.
