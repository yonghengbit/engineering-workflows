# Comparative Planning Benchmark v1

Frozen: 2026-08-13

Rubric SHA-256:
`BF77080CF79DC4719EAC94271F36FC205418CBE454897F52369366CE6DC85471`

## Conditions

Run each condition in a fresh agent context with the same inherited model configuration and no
access to `rubric.json`.

1. `native`: use no custom skill.
2. `engineering-workflow`: explicitly use `skills/engineering-workflow/SKILL.md` and load only the
   references required by each request.
3. `superpowers`: use `skills/using-superpowers/SKILL.md` from obra/superpowers v6.1.1 and any
   sub-skills it requires for each request.

Do not execute the described tasks or modify a checkout. Return one compact JSON object per prompt
with exactly these fields:

```json
{
  "case_id": "C1",
  "objective": "...",
  "approach": "...",
  "transitions": ["..."],
  "artifacts": ["..."],
  "agents": "...",
  "evidence": ["..."],
  "stop_conditions": ["..."],
  "loaded_files": ["relative/path/actually/read"]
}
```

Use `loaded_files: []` for the native condition. Paths for a skill condition must be relative to its
provided skill root and list only files actually read. Do not include repository instructions,
prompts, tool output, or model internals in that list.

## Prompts

### C1 — Small backward-compatible change

Add an optional `--explain` switch to one command. With the switch omitted, behavior must remain
byte-for-byte compatible. Add the narrowest useful regression check.

### C2 — Release gate with unavailable infrastructure

Execute the repository's established unit checks and decide whether this commit meets the stated
release gate. A required service may be unreachable. Do not change product code.

### C3 — Intermittent concurrent failure

A GPU cache-registration operation fails only under intermittent concurrent load. Establish the
mechanism, repair the verified defect, and protect it with a regression check.

### C4 — Read-only review

Examine the proposed patch for correctness and backward-compatibility regressions, returning only
review findings; leave the checkout unchanged.

### C5 — Controlled performance comparison

Determine whether candidate B lowers p99 latency versus candidate A for the same request stream and
environment.

### C6 — Shared contract replacement

Replace one shared tensor-memory contract used synchronously by a planner, transport, kernel, and
three backends. The consumers are tightly dependent on that single contract. Implement and verify.

### C7 — Evidence-labelled investigation

Explain the lifecycle by which request slots are acquired, transferred, reused, and released in the
current scheduler. Separate verified paths from unresolved branches and make no edits.

### C8 — Conditional diagnosis and repair

Check the feature against its acceptance criterion. Only if it fails for an unknown cause, prove
that cause, implement the supported repair, and rerun the authoritative checks.

## Integrity Rules

- Freeze and record the SHA-256 of `rubric.json` before dispatching agents.
- Do not tune prompts, patterns, or thresholds after seeing outputs.
- Preserve every raw output, including malformed or low-scoring output.
- Use identical prompts, schema, and inherited model configuration across conditions.
- Treat regex scores as wording-sensitive planning checks, not implementation success.
- Treat cost numbers as character-based proxies, not billed or exact model tokens.
- Do not generalize one harness run to all agents, repositories, models, or task distributions.
