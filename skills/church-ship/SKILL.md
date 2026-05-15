---
name: church-ship
description: Run a Repo Church ship or merge gate with tests, docs, rollback, risk, and Bible alignment. Use when the user asks for ship checklist, merge readiness, release gate, pre-merge review, or phase completion approval.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Ship Gate

Use this skill before merging, releasing, or marking a phase complete.

## Inputs

- Current diff or PR.
- Phase anchor, spec gate result, UAT result.
- Test/build/lint results.
- Bible alignment notes.

## Checklist

1. Scope matches approved phase.
2. Required tests/builds ran and results are captured.
3. Docs or user-facing notes are updated.
4. Migrations, flags, auth, privacy, security, or payments risks are called out.
5. Rollback path is clear.
6. Observability/logging is sufficient for changed behavior.
7. Repo Bible validation, source extraction, claim scan, or HTML render was run when packet artifacts changed materially.
8. Bible drift is either updated or logged for refresh.
9. Open gaps are non-blocking or explicitly accepted.

Use deterministic checks before final judgment:

```bash
church context load --root <repo> --format markdown
church ledger check gaps --root <repo> --allow-open
church ledger check uat --root <repo> --allow-open
church lifecycle status --root <repo> --format json
```

Record final decision:

```bash
church lifecycle advance ship --root <repo> --outcome PASS|PASS_WITH_RISK|HOLD|BLOCK
```

## Output

```markdown
## Ship Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
SHIP_READY: yes|no
Reason:

## Checklist
| Item | Status | Evidence |
| --- | --- | --- |

## Risk And Rollback
Risk:
Rollback:
Monitoring:

## Bible Alignment
Aligned: yes|no
Refresh needed:

## Required Before Merge
| Action | Owner | Blocks? |
| --- | --- | --- |

## Tooling Used
Bible validation:
Source/claim checks:
HTML render:
```

## Blockers

Return `BLOCK` for failing must-pass tests, unresolved critical UAT failures, unknown rollback on risky changes, or Bible contradictions that affect user-facing direction.
