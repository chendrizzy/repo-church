---
name: church-rewind
description: Plan guarded undo or rollback operations with git evidence, risk warnings, and explicit execution review.
---

# church:rewind

Use for GSD undo parity when a rollback, revert, or local restore needs planning.

## Progressive Loading

1. `church`
2. `church-gap-closure`
3. `church-ship` when release rollback is involved

Agents:

- `church-git-steward`
- `church-debug-examiner` when rollback follows a bug

## CLI Pattern

```bash
church undo plan --root <repo> --ref HEAD --format json
church undo plan --root <repo> --ref <commit> --path backend/src/file.ts --format markdown
```

## Gate

`Rewind Gate` passes when:

- dirty state and recent commits are visible,
- restore versus revert is chosen intentionally,
- destructive commands are not run without explicit review,
- rollback risk is recorded in a gap/risk ledger when unresolved.

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Rewind Verdict
Outcome:
Ref:
Execution reviewed: yes|no

## Rollback Plan
| Command | Purpose | Risk |
| --- | --- | --- |
```
