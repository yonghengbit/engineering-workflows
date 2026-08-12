# Frozen Holdout Protocol

Date: 2026-08-12

Rubric SHA-256:
`030AF68242804DB0BBDFBED3AA5DFF59CA13ECA9DF70325833522870A33F509E`

Use two fresh agents with the same inherited Codex configuration and medium reasoning. Neither agent
receives the rubric or expected answers.

- Baseline instruction: do not load or invoke any custom skill.
- Treatment instruction: explicitly use the repository `engineering-workflow` and load only required
  progressive references.
- Both return JSONL with `case_id`, `initial_objective`, `strategy_or_scale`, `transitions`,
  `artifacts`, `subagents`, and `safeguards`.
- Neither modifies files or executes the described engineering task.
- Do not change `rubric.json` after collecting holdout outputs. Report raw scores even if treatment
  does not improve.

## Holdout Prompts

1. Add an optional `--explain` switch to one command. With the switch omitted, behavior must remain
   byte-for-byte compatible. Add the narrowest useful regression check.
2. Execute the repository's established unit checks and decide whether this commit meets the stated
   release gate. A required service may be unreachable.
3. A GPU cache-registration operation fails only under intermittent concurrent load. Establish the
   mechanism, repair the verified defect, and protect it with a regression check.
4. Examine the proposed patch for correctness and backward-compatibility regressions, returning only
   review findings; leave the checkout unchanged.
5. Determine whether candidate B lowers p99 latency versus candidate A for the same request stream and
   environment.
6. Replace one shared tensor-memory contract used synchronously by a planner, transport, kernel, and
   three backends. The consumers are tightly dependent on that single contract. Implement and verify.
7. Explain the lifecycle by which request slots are acquired, transferred, reused, and released in
   the current scheduler. Separate verified paths from unresolved branches and make no edits.
8. Check the feature against its acceptance criterion. Only if it fails for an unknown cause, prove
   that cause, implement the supported repair, and rerun the authoritative checks.
