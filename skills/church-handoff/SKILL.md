---
name: church-handoff
description: Produce a Repo Church phase handoff with frozen scope, consumed artifacts, validation commands, and next actions. Use for phase handoff, context handoff, resume brief, execution handoff, or preparing another agent to continue work.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Handoff

Use this skill when work is about to move from planning to execution, between agents, or across sessions.

## Inputs

- Approved phase anchor and spec gate result.
- Gap ledger and unresolved risks.
- Current branch and repo status.
- Validation commands and last known results.

## Procedure

1. Load state: `church context load --root <repo> --format markdown --include-history`.
2. Freeze in-scope and out-of-scope work.
3. List consumed artifacts with paths and why they matter.
4. Name unresolved gaps from `church ledger check gaps --root <repo> --allow-open`.
5. Define first three moves for the next executor.
6. Split safe parallel streams from critical path work.
7. Render deterministic handoff: `church lifecycle handoff --root <repo> --output <path> --format markdown`.
8. Register the handoff with `church lifecycle advance handoff --root <repo> --artifact handoff=<path>`.

## Output

```markdown
## Handoff Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Phase
Name:
Objective:
Branch:

## Frozen Scope
In scope:
Out of scope:

## Consumed Artifacts
| Artifact | Purpose |
| --- | --- |

## Next Three Moves
1.
2.
3.

## Parallel Streams
| Stream | Owner | Can start now? | Blocked by |
| --- | --- | --- | --- |

## Validation
Commands:
Last result:
Rollback:

## Open Risks
| Risk | Owner | Mitigation | Recheck |
| --- | --- | --- | --- |
```

## Blockers

Return `HOLD` if the next executor would need to infer scope, acceptance criteria, or critical context.
