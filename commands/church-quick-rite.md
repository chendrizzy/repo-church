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
church inbox add --root <repo> --id QUICK-<n> --kind backlog --severity low --summary "<task>" --route church:quick-rite
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

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Quick Rite
Task:
Risk: low

## Quick Eligibility
| Exclusion | Checked? | Evidence |
| --- | --- | --- |
| Strategy/Bible impact | yes|no | |
| Auth/security/privacy/payments | yes|no | |
| Architecture contract | yes|no | |
| User-facing UX | yes|no | |

## Work Summary
| Files changed | Validation command | Result | Full lifecycle needed? |
| --- | --- | --- | --- |

Escalate to `church:gather` if any exclusion is uncertain.
```
