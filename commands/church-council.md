---
name: church-council
description: Show Repo Church status, available workflows, reasoning boundaries, blocker ledgers, and recommended next command.
---

# church:council

Use as the command-center/status view.

## Progressive Loading

1. `church`
2. `church-gap-closure` only when blockers need triage
3. `church-optimizer` only when status exposes redundant or slow workflow steps

Agents:

- `church-gap-steward` when ledgers are blocked
- `church-doc-scribe` when a status handoff must be written

## CLI Pattern

```bash
church registry list --format markdown
church registry reasoning --format markdown
church context load --root <repo> --format markdown --include-history
church ledger check gaps --root <repo> --allow-open
church ledger check uat --root <repo> --allow-open
```

## Output

```markdown
## Council Status
Active workflow:
Gate:
Outcome:
Recommended next command:

## Blockers
| Kind | Count | Highest severity |
| --- | --- | --- |
```
