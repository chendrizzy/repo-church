# Package Authoring

This page is for maintainers extending the Repo Church skill package.

## Package Shape

```text
.
  .claude-plugin/
    plugin.json
  commands/
    church-gather.md
    church-survey.md
    ...
  agents/
    church-moat-scout.md
    church-codebase-cartographer.md
    ...
  skills/
    church/
      SKILL.md
      references/
      scripts/
    church-moat/
      SKILL.md
    church-intake/
      SKILL.md
    repo-bible/
      SKILL.md
      scripts/
      references/
      templates/
      workflows/
  docs/
    INDEX.md
    getting-started.md
    ...
  evals/
    evals.json
```

## Authoring Rules

- Keep each skill in `skills/<skill-name>/SKILL.md`.
- Keep staged slash-command assets in `commands/<command-name>.md`.
- Keep lazy-loaded specialist profiles in `agents/<agent-name>.md`.
- Make `name` match the parent directory or file stem exactly.
- Use lowercase kebab-case names only.
- Put trigger language in `description`; do not rely on title-only descriptions.
- Keep `SKILL.md` concise and move detailed checklists into `references/` inside the same skill directory.
- Prefer deterministic scripts for validation and repetitive checks.
- Keep the package portable across compatible agent runtimes.

Source reference: [AGENTS.md](../AGENTS.md).

## Validation

From this package root:

```bash
bash skills/church/scripts/validate-package.sh .
python3 tests/test_church_plugin_assets.py
python3 tests/test_church_cli.py
```

The validator checks:

- skill frontmatter,
- command frontmatter,
- agent frontmatter,
- kebab-case names,
- name-to-file alignment,
- required agent sections,
- eval JSON shape.

The Python tests add regression coverage for staged commands, specialist profile contracts, CLI behavior, package namespace cutover, and expected lifecycle assets.

## Link Hygiene

Docs under `docs/` should link to source assets with paths relative to `docs/`, such as:

```markdown
[Lifecycle Model](../skills/church/references/lifecycle-model.md)
[church:gather](../commands/church-gather.md)
[church-bible-scribe](../agents/church-bible-scribe.md)
```

Keep user-facing docs under `docs/`. Keep machine-consumed skill references inside the skill directory that owns them.

## Portability

Repo Church deliberately avoids binding the package to one agent runtime. Runtime-specific wrappers can exist in consuming projects, but the package source should remain portable and installable as a skills.sh-style package.

## Related Docs

- [Reference Index](reference-index.md)
- [CLI and Tooling](cli-and-tooling.md)
- [Skills](skills.md)
