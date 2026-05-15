---
name: church-bless
description: Bless a release or phase completion: ship gate, risk review, rollback, Bible drift check, and final progression decision.
---

# church:bless

Use this as the final ship/merge readiness gate.

## Progressive Loading

1. `church`
2. `church-ship`
3. `church-gap-closure` only if blockers remain
4. `repo-bible` if doctrine drift must be refreshed

Agents:

- `church-ship-steward`
- `church-doctrine-auditor`
- `church-security-examiner` for high-risk changes

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church ledger check gaps --root <repo> --allow-open --format json
church ledger check uat --root <repo> --allow-open --format json
church lifecycle status --root <repo> --format json
church bible validate --root <repo> --follow-local-md --format json --output -
church registry reasoning ship --format markdown
```

## Gate

`Blessing Gate` may pass only when:

- no critical or high unresolved gap/UAT blocker remains,
- release risk and rollback are documented,
- tests and objective checks are current,
- Bible drift is either absent, refreshed, or logged as a refresh blocker,
- mutual signoff requirements are satisfied.

Record:

```bash
church lifecycle advance ship --root <repo> --outcome PASS|PASS_WITH_RISK|HOLD|BLOCK
```

## Output

```markdown
## Blessing Verdict
SHIP_READY: yes|no
Outcome:

## Required Before Merge
| Action | Owner | Blocks? |
| --- | --- | --- |
```
