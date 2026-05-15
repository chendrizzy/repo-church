# Repo Church Agent Skills

[![skills.sh](https://skills.sh/b/chendrizzy/repo-church)](https://skills.sh/chendrizzy/repo-church)

Repo Church is an agent-agnostic skill package for Bible-grounded repository planning, phase chaining, gap closure, and collaborative verification.

It helps agents and humans turn a durable Repo Bible into executable work: first clarify the product doctrine, then validate assumptions, plan phases, hand off execution, verify outcomes, and refresh the source of truth.

## Start Here

If you are new to Repo Church, follow the docs in this order:

1. [Docs Index](docs/INDEX.md) - the full learning path and reference map.
2. [Getting Started](docs/getting-started.md) - install the package and run the first workflow.
3. [Concepts](docs/concepts.md) - learn the Bible, lifecycle, gates, ledgers, and signoff model.
4. [Lifecycle](docs/lifecycle.md) - see how the staged loop works from intake to refresh.

The README is intentionally short. The detailed command, skill, agent, CLI, validation, and reference docs live under [docs/](docs/INDEX.md).

## Install


**Package source repo:** If you are working inside a clone of this repository, do not run `npx skills add . --all` from the package root—it replaces `skills/` with symlinks into `.agents/skills/`. Refresh global installs from outside the repo: `npx skills add chendrizzy/repo-church --all -g`.

Global install from GitHub (skills.sh leaderboard uses install telemetry from this path):

```bash
npx skills add chendrizzy/repo-church --all -g
```

Equivalent full URL:

```bash
npx skills add https://github.com/chendrizzy/repo-church --all -g
```

From a parent checkout that contains this package:

```bash
npx skills add ./agent-skills/repo-church --all
```

From this package root:

```bash
npx skills add . --all
```

Install only the core lifecycle skill:

```bash
npx skills add . --skill church
```

Install the Bible generator and lifecycle router together:

```bash
npx skills add . --skill repo-bible --skill church
```

## First Run

Use `church:gather` when you want the framework to inspect a project and choose the next gate. Under the hood, the command starts with deterministic context loading:

```bash
skills/church/scripts/church init --root <repo> --mode brownfield --project-name "<name>"
skills/church/scripts/church context load --root <repo> --format markdown --include-history
skills/church/scripts/church bible inventory --root <repo> --format markdown
skills/church/scripts/church moat check --root <repo> --allow-incomplete --format json
```

For a small low-risk task, use `church:quick-rite`. For anything that changes strategy, architecture, security, UX, phase scope, or Bible doctrine, use the staged lifecycle.

## Core Loop

```text
church:gather
  -> church:discern
  -> church:canonize
  -> church:commission
  -> church:fellowship
  -> church:bless
  -> church:renew
  -> repeat
```

| Stage | Purpose |
| --- | --- |
| `church:gather` | Load context, initialize state, inventory Bible artifacts, define or check the moat, and choose the next route. |
| `church:discern` | Harden assumptions, source claims, and close ambiguity before planning. |
| `church:canonize` | Create or review anchors and specs with requirement traceability. |
| `church:commission` | Freeze scope, split safe workstreams, and prepare execution handoff. |
| `church:fellowship` | Review, run UAT, and record mutual signoff where needed. |
| `church:bless` | Gate merge or release readiness against evidence, rollback, and Bible alignment. |
| `church:renew` | Refresh the Bible, capture learnings, and set up the next cycle. |

See [Lifecycle](docs/lifecycle.md) and [Commands](docs/commands.md) for the complete operator path.

## Why It Works

Repo Church is useful when ordinary agent planning is too easy to drift, overfit to stale context, or skip verification. It makes the work harder to fake by requiring:

- a durable Repo Bible as the strategic source of truth,
- CLI-first inventory and validation before broad synthesis,
- confidence labels for assumptions and claims,
- phase anchors that trace to requirements and doctrine,
- gap ledgers with owners and closure proof,
- execution handoffs with validation and rollback,
- collaborative UAT for subjective or high-risk work,
- refresh loops when implementation changes doctrine.

The goal is not ceremony. The goal is to make the next agent or human able to continue without re-deriving the project.

## Documentation

Use [docs/INDEX.md](docs/INDEX.md) as the documentation home.

Key pages:

- [Getting Started](docs/getting-started.md)
- [Concepts](docs/concepts.md)
- [Lifecycle](docs/lifecycle.md)
- [Commands](docs/commands.md)
- [CLI and Tooling](docs/cli-and-tooling.md)
- [Skills](docs/skills.md)
- [Agents](docs/agents.md)
- [Package Authoring](docs/package-authoring.md)
- [Reference Index](docs/reference-index.md)

## Validate

From this package root:

```bash
bash skills/church/scripts/validate-package.sh .
python3 tests/test_church_plugin_assets.py
python3 tests/test_church_cli.py
```

From a parent checkout:

```bash
bash agent-skills/repo-church/skills/church/scripts/validate-package.sh agent-skills/repo-church
python3 agent-skills/repo-church/tests/test_church_plugin_assets.py
python3 agent-skills/repo-church/tests/test_church_cli.py
```

- validate-package.sh checks repo-local skills/, commands/, and agents/ at the package root—not ~/.agents/skills/ after a global install.

The validator checks skill, command, and agent frontmatter; naming rules; required agent sections; and the eval file. The Python tests cover staged assets, package namespace rules, and CLI behavior.
