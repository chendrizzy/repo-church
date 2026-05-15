---
name: church-branch
description: Plan a PR-safe branch and review scope without mutating git state or hiding planning artifacts.
---

# church:branch

Use for GSD PR-branch parity when a clean review branch needs scoped staging guidance.

## Progressive Loading

1. `church`
2. `church-ship`

Agents:

- `church-git-steward`
- `church-ship-steward`

## CLI Pattern

```bash
church branch plan --root <repo> --target main --name church/final-parity --message "church parity assets"
```

## Gate

`Branch Gate` passes when:

- current branch and dirty files are inspected,
- excluded planning/runtime paths are explicit,
- generated commands are reviewed before execution,
- PR scope aligns with ship-gate evidence.

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Branch Verdict
Outcome:
Current branch:
Planned branch:

## Review Scope
| File | Include? | Reason |
| --- | --- | --- |
```
