---
name: church-quick-rite
description: Handle a small, low-risk task without invoking the full Repo Church cycle, while preserving optional state or ledger breadcrumbs.
---

# church:quick-rite

Use for trivial, low-risk changes where full phase ceremony would be wasteful.

## Progressive Loading

1. `church` only if state context matters
2. Specific implementation skill only if needed

Agent dispatch is normally unnecessary.

## CLI Pattern

```bash
church context load --root <repo> --format markdown
church state set active.workflow quick --root <repo>
```

## Guardrail

Do not use this command when the task affects:

- product strategy,
- auth/security/privacy/payments,
- architecture contracts,
- user-facing UX,
- phase scope,
- Bible doctrine.

## Output

```markdown
## Quick Rite
Task:
Risk: low
State update needed: yes|no
Validation:
```
