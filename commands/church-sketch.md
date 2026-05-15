---
name: church-sketch
description: Register creative sketch and design artifacts with doctrine links, signoff requirements, and acceptance routing.
---

# church:sketch

Use for GSD sketch parity when design exploration, rough UI concepts, diagrams, or visual artifacts need lifecycle tracking.

## Progressive Loading

1. `church`
2. `church-uat` when user acceptance is required
3. `repo-bible` when design doctrine changes

Agents:

- `church-sketch-curator`
- `church-ui-examiner`

## CLI Pattern

```bash
church sketch register --root <repo> --id SKETCH-001 --path design.png --summary "..." --requires-user-signoff
church sketch list --root <repo> --format json
church sketch check --root <repo> --allow-open --format json
```

## Gate

`Sketch Gate` passes when:

- the artifact is registered with source path and intended decision,
- user signoff is tracked for subjective design choices,
- accepted sketches feed `church:canonize` or `church:fellowship`,
- rejected sketches are superseded rather than silently forgotten.

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Sketch Verdict
Outcome:
User signoff required:

## Artifacts
| ID | Path | Status | Decision |
| --- | --- | --- | --- |
```
