# Workflow Contract

This contract is for authors extending the canonical `engineering-workflow` skill. It does not require
every workflow to create the same artifacts.

## 1. Architectural Placement

Keep one installable `SKILL.md`. Put detailed primary-intent procedure under:

```text
skills/engineering-workflow/references/<intent>/workflow.md
```

Add strategy references only when a strategy materially changes execution. The top-level skill owns
routing, loading, transitions, and common principles; references own execution details.

## 2. Primary Intent

State the single question the workflow owns and route by current requested outcome, not keywords.
Define entry conditions and adjacent non-goals. Supporting activities inside another workflow do not
create ownership.

## 3. Strategy or Scale

Use workflow-specific distinctions:

```text
Development -> SMALL / MEDIUM / LARGE / VERY_LARGE
Testing     -> QUICK / STRUCTURED / VALIDATION
Debugging   -> DIRECT / SYSTEMATIC
```

Do not copy Development scaling into unrelated workflows. Define a strategy only when it changes
artifacts, execution, verification, or coordination.

## 4. Progressive Loading

The router loads exactly one `<intent>/workflow.md`. A selected workflow may then load exactly one
strategy reference. Do not require startup loading of unrelated intents or every strategy.

List selectable paths in the top-level `SKILL.md` so they remain directly discoverable.

## 5. Artifacts

Artifacts must have one purpose and be proportional to task complexity. Specify when each becomes
required and when it must not be created. Router-owned artifacts are forbidden.

Prefer no artifact for SMALL, QUICK, DIRECT, bounded Investigation, and normal Review. A workflow
transition alone never requires a new document.

## 6. Re-evaluation

Define a small number of fixed checkpoints plus event-triggered re-evaluation for material new
evidence. Avoid rescoring after every file, command, or small action. Preserve useful evidence when
upgrading strategy.

## 7. Dynamic Subagents

The router must not decide or create subagents. A selected workflow may use them only with clear
ownership, weak dependencies, low edit conflict, explicit inputs and outputs, and independent
verification. Derive roles from the task and repository; do not maintain a fixed specialist taxonomy.

## 8. Exit Conditions

Define what makes the current primary deliverable complete or blocked. Examples:

```text
Development requested behavior implemented and relevant verification complete
Testing     required cases have terminal states mapped to criteria
Debugging   root cause supported by discriminating evidence
Performance conclusion bounded to preserved measurements
Investigation question answered with evidence and unknowns identified
Review      actionable findings reported with scope and residual risk
```

## 9. Workflow Transitions

Transition only when the primary objective changes. Use the canonical payload:

```text
From:
To:

Current Objective:
Verified Findings / Evidence:
Constraints:
Changed Files:
Known Reproduction / Procedure:
Required Next Action:
Verification Needed:
```

Carry only what the destination needs. Load the destination workflow at transition time and stop
applying the previous procedure.

## 10. Source of Truth

```text
code behavior      current code + git diff
measured behavior  actual raw output + environment
workflow state     designated artifacts
```

Documentation does not override contradictory implementation or observation. Correct stale docs.

## 11. Promotion Checklist

Before adding or changing a workflow:

- primary intent, non-goals, entry, and exit are unambiguous;
- strategy distinctions are necessary;
- artifacts are proportional;
- re-evaluation and transitions are explicit;
- progressive paths exist and are referenced from the top-level skill;
- representative routing and failure scenarios pass;
- user and architecture documentation match the active skill.
