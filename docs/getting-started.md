# Getting Started

This guide gets a new user from install to a useful first Repo Church interaction.

## 1. Install The Package

From a parent checkout that contains this package:

```bash
npx skills add ./agent-skills/repo-church --all
```

From this package root:

```bash
npx skills add . --all
```

For the smallest useful install:

```bash
npx skills add . --skill repo-bible --skill church
```

`repo-bible` creates and maintains the durable doctrine packet. `church` routes the planning, hardening, handoff, UAT, ship, and refresh lifecycle around it.

## 2. Pick Your Project Mode

| Project Situation | Mode | First Command |
| --- | --- | --- |
| Existing code or docs can affect the plan | `brownfield` | `church:gather` |
| New project with little implementation reality | `greenfield` | `church:gather` |
| Small low-risk change | quick path | `church:quick-rite` |
| Bible-only generation, audit, or refresh | Bible workflow | `repo-bible` |

Use the full staged lifecycle when the work affects strategy, architecture, security, privacy, payments, UX, phase scope, or doctrine.

## 3. Run A First Intake

From this package root, the bundled CLI can inspect another repository:

```bash
skills/church/scripts/church init --root <repo> --mode brownfield --project-name "<name>"
skills/church/scripts/church context load --root <repo> --format markdown --include-history
skills/church/scripts/church bible inventory --root <repo> --format markdown
skills/church/scripts/church moat check --root <repo> --allow-incomplete --format json
```

If the target project does not have a Bible packet yet, generate or scaffold it with `repo-bible` or `church bible ...`.

```bash
skills/church/scripts/church bible scaffold --root <repo>
skills/church/scripts/church bible inventory --root <repo> --format markdown
```

## 4. Let The Result Route You

After the intake, Repo Church should produce a gate verdict and next command. Common routes:

| Finding | Next Step |
| --- | --- |
| Bible is missing or weak | Generate, audit, or refresh the Repo Bible. |
| Moat is missing or hard to explain | Run moat definition before deep planning. |
| Current code may change scope | Run `church:survey`. |
| High-impact assumptions are unverified | Run `church:discern`. |
| Parent phase is ready for planning | Run `church:canonize`. |
| Scope is approved and execution can start | Run `church:commission`. |

## 5. Verify Value Quickly

A useful first session should give you at least one of these outcomes:

- a clearer project moat,
- a Bible inventory and missing-artifact list,
- a confidence-labeled assumption ledger,
- a stronger phase anchor,
- a spec gate with concrete defects,
- an execution handoff the next agent can use,
- a UAT or ship verdict with evidence.

If you do not get one of those, the framework has not produced enough leverage yet. Continue with the next gate rather than jumping straight to implementation.

## Related Docs

- [Concepts](concepts.md)
- [Lifecycle](lifecycle.md)
- [Commands](commands.md)
- [Reference Index](reference-index.md)
