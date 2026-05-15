---
name: church-archive
description: Plan artifact cleanup and archival without deleting lifecycle evidence or breaking future handoffs.
---

# church:archive

Use for GSD cleanup parity when completed phase, runtime, or generated artifacts need archive planning.

## Progressive Loading

1. `church`
2. `church-ship` when archiving follows release
3. `church-handoff` when archived material affects continuation

Agents:

- `church-archive-steward`
- `church-doc-scribe`

## CLI Pattern

```bash
church archive plan --root <repo> --archive-root .church/archive --format json
church archive plan --root <repo> --path .planning/phases --output .church/archive-plan.json
```

## Gate

`Archive Gate` passes when:

- archive candidates are listed before movement,
- retained evidence and handoff links remain valid,
- no artifact is deleted by default,
- cleanup decisions are reversible or explicitly accepted.

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Archive Verdict
Outcome:
Dry run:

## Candidates
| Path | Action | Risk |
| --- | --- | --- |
```
