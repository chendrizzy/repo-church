---
name: church-inbox
description: Capture and triage inbox or backlog items into typed Repo Church records before routing them to ledgers or gates.
---

# church:inbox

Use for GSD inbox/review-backlog parity when incoming ideas, questions, risks, or backlog items need durable triage.

## Progressive Loading

1. `church`
2. `church-gap-closure` for blocking inbox items
3. `church-anchor` when triage changes phase scope

Agents:

- `church-triage-steward`
- `church-gap-steward` when items block gates

## CLI Pattern

```bash
church inbox add --root <repo> --id INBOX-001 --kind idea --summary "..." --route anchor
church inbox list --root <repo> --format json
church inbox check --root <repo> --allow-open --format json
```

## Gate

`Inbox Gate` passes when:

- every incoming item has kind, owner, status, and route,
- critical/high inbox items block until triaged,
- ideas are not silently converted into approved scope.

## Output

```markdown
## Inbox Verdict
Outcome:
Open items:

## Triage
| ID | Kind | Severity | Route | Blocks? |
| --- | --- | --- | --- | --- |
```
