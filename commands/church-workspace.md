---
name: church-workspace
description: Manage portable Repo Church workspace records for concurrent work without relying on one agent runtime.
---

# church:workspace

Use for workspace CRUD and active workspace routing.

## Progressive Loading

1. `church`
2. `church-handoff` when a workspace needs continuation context

Agents:

- `church-workspace-steward`
- `church-workstream-deacon` when workspace split affects execution

## CLI Pattern

```bash
church workspace create <name> --root <repo> --summary "..." --owner agent
church workspace list --root <repo> --format json
church workspace status <name> --root <repo> --format json
church workspace switch <name> --root <repo>
church workspace complete <name> --root <repo>
```

## Gate

`Workspace Gate` passes when:

- active workspace state is explicit,
- workspaces have owner, path, and summary,
- parallel workspaces have integration checkpoints,
- workspace changes do not bypass phase gates.

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Workspace Verdict
Outcome:
Active workspace:

## Workspaces
| Name | Status | Owner | Path | Integration concern |
| --- | --- | --- | --- | --- |
```
