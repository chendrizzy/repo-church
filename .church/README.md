# Repo Church

Operator map for **Repo Church** outputs in this repository. All **Repo Bible** packet artifacts default under **`bible/`** here. Override locations with `repo_bible.py` `--church-root`, `--bible-dir`, or the `CHURCH_ROOT` environment variable when you intentionally use a non-standard layout.

## Directory layout

| Path | Purpose |
|------|---------|
| `bible/` | Markdown packet (requirements, roadmap, audits), `_repo-bible-*.md` tool reports, `vision-intake.html`, and optional `html/` rendered bundle for human review. |
| `runs/` | Local scratch and throwaway exports (typically gitignored). |
| `index.json` | Small manifest updated by `repo_bible.py scaffold` (paths relative to the repository root). |

## Quick commands (from repository root)

```bash
python path/to/repo_bible.py inventory --root .
python path/to/repo_bible.py scaffold --root .
python path/to/repo_bible.py validate --root .
python path/to/repo_bible.py render-html --root .
python path/to/repo_bible.py intake-html --root .
```

Use `--legacy-planning-bible` to read or write the older `.planning/commandments` packet during migration. See the **repo-bible** `SKILL.md` for full workflows.
