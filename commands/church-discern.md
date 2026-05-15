---
name: church-discern
description: Harden assumptions and ambiguity before phase planning using evidence ledgers, current research, and Bible/market source checks.
---

# church:discern

Use this after `church:gather` and before specs or execution. It replaces loose discussion with evidence-backed assumption hardening.

## Progressive Loading

1. `church`
2. `church-harden`
3. `church-gap-closure` only when blockers are found
4. `repo-bible` only for source extraction, validation, claim scans, or Bible refresh

Agents:

- `church-moat-scout` for external market assumptions
- `church-doctrine-auditor` for Bible conflicts
- `church-gap-steward` for closure planning

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church ledger init assumptions --root <repo>
church bible sources --root <repo> --follow-local-md --format json --output -
church bible claim-scan --root <repo> --path <repo> --format json --output -
church registry reasoning harden --format markdown
```

## Gate

`Evidence Gate` cannot pass with:

- high-impact assumptions still `hypothesis`, `stale`, or `contradicted`,
- market claims without current source evidence,
- Bible conflicts without a gap item,
- ambiguous user intent that changes phase scope.

Use:

```bash
church ledger add assumptions --root <repo> --id A-001 --summary "..." --status verified-current --evidence "..." --owner agent
church ledger check assumptions --root <repo>
church lifecycle advance harden --root <repo> --outcome PASS|HOLD|BLOCK
```

## Output

```markdown
## Discern Verdict
Outcome:
Planning allowed: yes|no

## Assumptions
| ID | Claim | Confidence | Evidence | Impact | Status |
| --- | --- | --- | --- | --- | --- |

## Blocking Questions
| Question | Why it matters | Owner | Recheck |
| --- | --- | --- | --- |
```
