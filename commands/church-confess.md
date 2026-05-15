---
name: church-confess
description: Add an ad hoc requirement, phase idea, gap, risk, or confession into the correct Repo Church ledger without disrupting the active gate.
---

# church:confess

Use for ad hoc changes that should not be silently folded into the plan.

## Progressive Loading

1. `church`
2. `church-gap-closure` when the item blocks planning or execution
3. `church-anchor` when the item changes phase scope

Agent:

- `church-gap-steward`

## CLI Pattern

```bash
church context load --root <repo> --format markdown
church ledger add gaps --root <repo> --id GAP-001 --summary "..." --severity medium --status open --evidence "..." --owner "<owner>"
church ledger check gaps --root <repo> --allow-open
```

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Confession Recorded
Ledger:
ID:
Blocks active gate: yes|no
Recommended next command:
```
