---
name: church-atonement
description: Debug or remediate failures with a structured diagnosis, risk ledger, gap closure, and recheck path.
---

# church:atonement

Use for bugs, failed gates, broken tests, regressions, or post-mortem analysis.

## Progressive Loading

1. `church`
2. `church-gap-closure`
3. Domain skill/agent based on failure type

Agents:

- `church-debug-examiner`
- `church-code-examiner`
- `church-security-examiner` when security is implicated

## CLI Pattern

```bash
church context load --root <repo> --format markdown --include-history
church ledger init risks --root <repo>
church ledger add risks --root <repo> --id RISK-001 --summary "..." --severity high --status open --owner agent
church ledger add gaps --root <repo> --id BUG-001 --summary "..." --severity high --status open --evidence "..." --owner agent
```

## Output

```markdown
## Atonement Verdict
Root cause:
Fix path:
Recheck command:

## Ledger Updates
| ID | Kind | Severity | Status |
| --- | --- | --- | --- |
```
