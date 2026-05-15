---
name: church-fellowship
description: Run collaborative verification: peer review, UAT ledger checks, mutual signoff, and user-visible acceptance before phase progression.
---

# church:fellowship

Use this after implementation and before ship. It formalizes peer-reviewed and collaborative verification.

## Progressive Loading

1. `church`
2. `church-uat`
3. `church-gap-closure` for failures
4. `church-ship` only after UAT is green

Agents:

- `church-uat-fellow`
- `church-code-examiner`
- `church-ui-examiner` for UI work
- `church-security-examiner` for security-sensitive work
- `church-ai-eval-planner` for AI behavior

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church ledger init uat --root <repo>
church bible render-html --root <repo>
church ledger check gaps --root <repo> --allow-open --format json
church registry reasoning uat --format markdown
```

## Quantified Gate

`Fellowship Gate` may pass only when:

- 100% of must-pass user stories have UAT rows,
- 0 critical/high UAT failures remain open,
- objective checks are recorded with command and result,
- subjective product/UX/brand decisions have user signoff when required,
- `signoff.agent=true`,
- `signoff.user=true` when `signoff.mutual_required=true`.

Record:

```bash
church ledger add uat --root <repo> --id UAT-001 --summary "..." --status pass|fail --evidence "..." --owner agent
church state set signoff.agent true --root <repo>
church state set signoff.user true --root <repo>
church lifecycle advance uat --root <repo> --outcome PASS|HOLD|BLOCK
```

## Output

```markdown
## Fellowship Verdict
Outcome:
Mutual signoff required: yes|no
Agent signoff:
User signoff:

## UAT Matrix
| ID | Story | Result | Evidence | Signoff |
| --- | --- | --- | --- | --- |
```
