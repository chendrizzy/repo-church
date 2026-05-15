---
name: church-survey
description: Survey brownfield code, architecture, interfaces, and graph/map evidence before anchoring or major implementation work.
---

# church:survey

Use this when a brownfield project, unfamiliar subsystem, integration-heavy phase, or architecture-sensitive change needs a codebase map before planning.

## Progressive Loading

1. `church`
2. `repo-bible` for inventory and architecture-map updates
3. `church-harden` only when mapping exposes assumptions
4. `church-gap-closure` only when mapping exposes blockers

Agents:

- `church-codebase-cartographer`
- `church-doctrine-auditor` when implementation reality conflicts with Bible doctrine
- `church-gap-steward` when map findings block planning

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church bible inventory --root <repo> --format json --output -
church bible validate --root <repo> --follow-local-md --format json --output -
church registry reasoning bible --format markdown
```

Optional graph inputs may be consumed when a project already has them, but this command must not require a vendor-specific graph tool.

## Gate

`Survey Gate` may pass only when:

- relevant modules, interfaces, data flows, and test surfaces are identified,
- implementation reality is compared against Bible architecture/design doctrine,
- stale or missing architecture-map entries are logged for refresh,
- ambiguous ownership or integration boundaries become assumption/gap ledger items,
- graph or map artifacts are treated as evidence, not as final architectural judgment.

Record:

```bash
church ledger add assumptions --root <repo> --id MAP-001 --summary "..." --status verified-local --evidence "..." --owner agent
church ledger add gaps --root <repo> --id MAP-GAP-001 --summary "..." --severity medium --status open --evidence "..." --owner agent
```

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Survey Verdict
Outcome:
Planning allowed: yes|no

## Codebase Map
| Area | Evidence | Interfaces | Risks |
| --- | --- | --- | --- |

## Architecture Drift
| Bible artifact | Code evidence | Action |
| --- | --- | --- |
```
