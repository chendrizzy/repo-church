# Repo Church Documentation Index

This index is the user-facing entry point for Repo Church after the README. It gives new users a guided path first, then links to the distributed source references when they need implementation detail.

## Recommended Learning Path

1. [Getting Started](getting-started.md)
   Install the package, run a first project intake, and choose the right workflow for your goal.

2. [Concepts](concepts.md)
   Learn the Repo Bible, lifecycle stages, gates, ledgers, moat, UAT, and refresh model.

3. [Lifecycle](lifecycle.md)
   Walk through the complete staged loop and understand when a stage should repeat.

4. [Commands](commands.md)
   Use the core staged commands and optional operational shortcuts.

5. [CLI and Tooling](cli-and-tooling.md)
   Understand what the deterministic CLI owns and where agent judgment remains required.

6. [Skills](skills.md)
   Pick the umbrella skill or child skill that matches the current work.

7. [Agents](agents.md)
   See which specialist profiles commands can load for focused review or execution support.

8. [Package Authoring](package-authoring.md)
   Validate, extend, and keep the skill package portable across compatible agents.

9. [Reference Index](reference-index.md)
   Jump into source-level reference docs, command assets, agent contracts, Repo Bible workflows, and templates.

## Choose Your First Interaction

| Goal | Start With | Then Read |
| --- | --- | --- |
| Try Repo Church on an existing project | [Getting Started](getting-started.md) | [Lifecycle](lifecycle.md), [Commands](commands.md) |
| Generate or improve a Repo Bible | [Getting Started](getting-started.md) | [Skills](skills.md), [Reference Index](reference-index.md) |
| Plan a phase from existing doctrine | [Lifecycle](lifecycle.md) | [Commands](commands.md), [Concepts](concepts.md) |
| Harden assumptions before planning | [Concepts](concepts.md) | [Commands](commands.md), [Reference Index](reference-index.md) |
| Prepare execution handoff or UAT | [Lifecycle](lifecycle.md) | [Commands](commands.md), [Agents](agents.md) |
| Extend this package | [Package Authoring](package-authoring.md) | [Reference Index](reference-index.md) |

## Documentation Map

| User-Facing Page | Source References |
| --- | --- |
| [Getting Started](getting-started.md) | [church/SKILL.md](../skills/church/SKILL.md), [repo-bible/SKILL.md](../skills/repo-bible/SKILL.md) |
| [Concepts](concepts.md) | [Lifecycle Model](../skills/church/references/lifecycle-model.md), [Gate Taxonomy](../skills/church/references/gate-taxonomy.md), [Verification Protocol](../skills/church/references/verification-protocol.md) |
| [Lifecycle](lifecycle.md) | [Stage Command Map](../skills/church/references/stage-command-map.md), [Lifecycle Model](../skills/church/references/lifecycle-model.md), [Parallelism Guide](../skills/church/references/parallelism-guide.md) |
| [Commands](commands.md) | [commands/](../commands), [Stage Command Map](../skills/church/references/stage-command-map.md) |
| [CLI and Tooling](cli-and-tooling.md) | [CLI Automation Map](../skills/church/references/cli-automation-map.md), [CLI Architecture](../skills/church/references/cli-architecture.md), [Tooling Workbench](../skills/church/references/tooling-workbench.md) |
| [Skills](skills.md) | [skills/](../skills), [church/SKILL.md](../skills/church/SKILL.md), [repo-bible/SKILL.md](../skills/repo-bible/SKILL.md) |
| [Agents](agents.md) | [agents/](../agents), [Stage Command Map](../skills/church/references/stage-command-map.md) |
| [Package Authoring](package-authoring.md) | [AGENTS.md](../AGENTS.md), [validate-package.sh](../skills/church/scripts/validate-package.sh), [Plugin Asset Tests](../tests/test_church_plugin_assets.py) |
| [Reference Index](reference-index.md) | All distributed reference, workflow, template, command, and agent assets |

## Deep References

Use [Reference Index](reference-index.md) when you already know what you need and want the source asset directly.
