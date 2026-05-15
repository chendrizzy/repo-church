---
name: church-gather
description: Start or resume Repo Church project intake: initialize state, define or refresh the moat, inventory Bible artifacts, and choose the next gate.
---

# church:gather

Use this as the first staged command for greenfield or brownfield work. It replaces ad hoc project bootstrap, initial context recovery, and broad document rereads.

## Progressive Loading

Load only in this order:

1. `church`
2. `church-intake`
3. `church-moat` only when the moat is missing, stale, or weak
4. `repo-bible` only when Bible artifacts need generation, audit, or refresh

Dispatch agents only if their evidence is needed:

- `church-moat-scout` for market/moat research
- `church-bible-scribe` for Bible synthesis gaps
- `church-codebase-cartographer` for brownfield implementation reality
- `church-anchor-architect` when the next phase is unclear

## CLI Preflight

```bash
church init --root <repo> --mode greenfield|brownfield --project-name "<name>"
church context load --root <repo> --format markdown --include-history
church registry reasoning init --format markdown
church bible inventory --root <repo> --format markdown
church moat check --root <repo> --allow-incomplete --format json
```

## Gate

`Intake Gate` may pass only when:

- project root and `.church/state.json` exist,
- moat artifacts exist or a `church-moat` gap is recorded,
- Bible inventory is available,
- brownfield implementation reality is surveyed or explicitly unnecessary,
- next workflow is selected from `church registry list`,
- no critical unknown blocks basic routing.

## Output

```markdown
## Gather Verdict
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Next command:
Reason:

## Evidence Loaded
- State:
- Moat:
- Bible inventory:

## Required Follow-Up
| Item | Owner | Command | Blocks? |
| --- | --- | --- | --- |
```
