# CLI And HTML Workbench Philosophy

Repo Church inherits the Repo Bible rule: use deterministic tooling to reduce noise before asking the agent to synthesize.

## CLI First

Use CLI reports for repeatable facts:

- file and artifact inventory,
- source URL extraction,
- requirement ID checks,
- markdown/link hygiene,
- banned or required claim scans,
- rendered HTML packets,
- generated intake forms.

Use `church` as the root lifecycle CLI when available:

```bash
skills/church/scripts/church init --root <repo> --mode brownfield
skills/church/scripts/church moat check --root <repo>
skills/church/scripts/church lifecycle status --root <repo>
skills/church/scripts/church bible inventory --root <repo>
```

The root CLI owns state and lifecycle tracking. Its `bible` command delegates to the bundled Repo Bible CLI.

When the bundled `repo-bible` skill is installed with this package, the direct Bible script lives at:

```bash
skills/repo-bible/scripts/repo-bible
```

If the shell wrapper is unavailable, use:

```bash
python3 skills/repo-bible/scripts/repo_bible.py <command> [options]
```

When a skill has been installed into an agent-specific directory, locate the sibling `repo-bible` skill and run the same commands from that directory.

## Recommended Commands

From a package checkout:

```bash
skills/repo-bible/scripts/repo-bible inventory --root <repo> --format markdown
skills/repo-bible/scripts/repo-bible validate --root <repo>
skills/repo-bible/scripts/repo-bible sources --root <repo> --follow-local-md --format json
skills/repo-bible/scripts/repo-bible claim-scan --root <repo> --path <repo> --banned "guarantee success|AI magic"
skills/repo-bible/scripts/repo-bible render-html --root <repo>
```

From inside `skills/repo-bible/`:

```bash
scripts/repo-bible inventory --root <repo> --format markdown
scripts/repo-bible intake-html --root <repo>
scripts/repo-bible render-html --root <repo>
```

## HTML Workbench

Use HTML when a dense packet needs human input or review:

- `intake-html` creates a structured vision capture form.
- `intake-html --prefill <json-or-md>` turns prior notes into editable fields.
- `render-html` creates a navigable Bible packet for review and signoff.

HTML is not a replacement for durable Markdown. Treat it as a workbench layer that improves capture, review speed, and user collaboration. Export or incorporate the results into the canonical Bible artifacts.

## Agent Boundary

Use tooling for mechanical checks and compression. Use the agent for:

- strategic interpretation,
- resolving contradictions,
- phase sequencing,
- design and architecture judgment,
- deciding what evidence changes the plan.

## Skip Criteria

It is acceptable to skip a tool when:

- the package is not installed with `repo-bible`,
- the repo is tiny and the relevant files are already known,
- the task is a single narrow question,
- running the tool would be slower than reading one obvious artifact.

When skipping, state the reason briefly in the gate output.
