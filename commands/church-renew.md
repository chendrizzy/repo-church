---
name: church-renew
description: Refresh the Bible, lessons, roadmap implications, and next cycle state after a phase, milestone, or strategic change.
---

# church:renew

Use after ship, milestone completion, or a material strategy/architecture/market change.

## Progressive Loading

1. `church`
2. `repo-bible`
3. `church-anchor` only if roadmap/phase order changes
4. `church-moat` if competitive leverage changed

Agents:

- `church-bible-scribe`
- `church-doctrine-auditor`
- `church-moat-scout`

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church bible validate --root <repo> --follow-local-md --format json --output -
church bible sources --root <repo> --follow-local-md --format json --output -
church bible render-html --root <repo>
church registry reasoning refresh --format markdown
```

## Gate

`Renewal Gate` passes when:

- doctrine drift has been captured or explicitly rejected,
- learnings are reflected in the next anchor or Bible refresh item,
- moat/market changes have been rechecked when relevant,
- next workflow is selected.

Record:

```bash
church lifecycle advance refresh --root <repo> --outcome PASS|PASS_WITH_RISK|HOLD|BLOCK --evidence "<refresh-record>"
```

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Renewal Verdict
Outcome:
Next cycle:

## Bible Updates
| Artifact | Change | Evidence |
| --- | --- | --- |
```
