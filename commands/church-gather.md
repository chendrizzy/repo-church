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

## Routing Rubric

| Signal | Threshold | Outcome | Next command | Required ledger item |
| --- | --- | --- | --- | --- |
| Bible packet missing or mostly placeholders | No usable requirements/roadmap/validation artifacts | `HOLD` | `repo-bible` / `church bible scaffold` | Gap for missing Bible source |
| Moat score is `BLOCK` or generic | Missing leverage, proof, or validation tests | `HOLD` | `church-moat` | Gap for weak moat evidence |
| Brownfield code can change scope or interfaces | Existing modules, data flows, or tests are unclear | `HOLD` | `church:survey` | Gap for implementation reality |
| External claim affects planning | Claim is stale, volatile, or unsupported | `HOLD` | `church:discern` | Assumption with confidence label |
| Critical/high blockers exist | Any open critical/high gap, risk, or UAT blocker | `BLOCK` | `church:atonement` or `church-gap-closure` | Closure item with owner and recheck |
| Requirements, moat, evidence, and blockers are usable | No critical routing unknowns | `PASS` or `PASS_WITH_RISK` | `church:canonize` or next registry key | Risk item for accepted non-critical risk |

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

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
