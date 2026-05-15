---
name: church-gap-closure
description: Close Repo Church gaps, contradictions, and drift with explicit remediation tasks. Use when the user mentions gap closure, planning drift, bible misalignment, unresolved assumptions, failed gates, remediation planning, or contradictory docs/code.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Gap Closure

Use this skill whenever a gate finds missing evidence, drift, contradiction, or under-specified work.

## Gap Types

- missing requirement,
- weak acceptance criterion,
- stale or unverified market claim,
- architecture conflict,
- design doctrine conflict,
- dependency conflict,
- implementation drift,
- missing test or observability,
- unclear ownership,
- user signoff needed.

## Procedure

1. Load current blockers: `church ledger list gaps --root <repo> --format markdown`.
2. Capture new gaps before fixing them with `church ledger add gaps ...`.
3. Identify source evidence on both sides of the conflict.
4. Classify severity: `critical`, `high`, `medium`, `low`.
5. Decide resolution: fix now, defer with owner, supersede, or escalate for user decision.
6. Add closure proof by replacing the ledger item with `--force`, a satisfied status, `--proof`, and a recheck command when deferring.
7. Run `church ledger check gaps --root <repo>`.
8. Re-run the relevant lifecycle gate with `church lifecycle advance <workflow> ... --evidence <closure-artifact>`.

## Output

```markdown
## Closure Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Gap Ledger
| ID | Type | Severity | Evidence | Impact | Resolution | Owner | Proof | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Remediation Plan
| ID | Source gap | Severity | Owner | Acceptance test | Evidence required | Action | Automatable? | Recheck command | Blocks? | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Gate To Re-run
Gate:
Command or artifact:
```

## Rules

Do not silently rewrite doctrine. If the right answer changes Bible direction, create a Bible refresh item or ask for user signoff.
