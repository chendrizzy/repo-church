# Repo Church CLI Architecture

Repo Church should use one root CLI with command groups, not multiple competing top-level CLIs.

## Recommendation

Use:

```bash
church init
church moat ...
church bible ...
church lifecycle ...
```

Keep `repo-bible` as a compatibility shim and as an internal module boundary.

## Why Single Root CLI

- One lifecycle state store: `.church/state.json`.
- One workflow registry and key-value dictionary.
- One install surface for agents and humans.
- Easier automation and handoff.
- Fewer naming decisions during phase progression.
- Clearer future SDK shape.
- Better cross-workflow validation because Bible, moat, lifecycle, and ship gates share state.

## Why Keep Internal Separation

The Bible renderer and lifecycle tracker have different responsibilities:

- Bible tooling captures, renders, validates, and audits durable doctrine.
- Church tooling tracks workflows, gates, moat, phase state, handoffs, and signoff.

Separating internal modules keeps the code maintainable without forcing users to remember multiple CLIs.

## Compatibility Strategy

- `church bible <args>` delegates to the bundled Repo Bible CLI.
- Existing `repo-bible <args>` remains valid as a shim for older docs and users.
- New docs should prefer `church bible`.
- Skill names can remain `repo-bible` and `church-*` because skills are semantic entry points, not CLI namespaces.

## When Multi-CLI Is Justified

Use separate top-level CLIs only when at least one is true:

- separate release cadence and versioning are mandatory,
- dependencies are heavy or incompatible,
- security boundaries differ,
- one tool must be embedded in environments where the other cannot run,
- user personas are completely different,
- one command surface is stable legacy and must remain frozen.

Absent those constraints, separate top-level CLIs create unnecessary state fragmentation.
