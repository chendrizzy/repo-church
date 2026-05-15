<purpose>
This reference explains how to reduce token consumption by using the bundled repo-bible CLI before asking the LLM to synthesize.
</purpose>

<tool>
The bundled CLI is:

```bash
scripts/repo-bible <command> [options]
```

If the wrapper is not executable in the current environment, run:

```bash
python scripts/repo_bible.py <command> [options]
```

**Path defaults:** all generated reports and scaffolds resolve under **`<repo>/.church/bible/`** unless you pass `--church-root`, `--bible-dir`, or set `CHURCH_ROOT`. Use **`--legacy-planning-bible`** to read/write **`<repo>/.planning/commandments/`** during migration.
</tool>

<commands>
| Command | Token-saving purpose |
|---|---|
| `inventory --root <repo>` | Finds candidate planning/research/design/spec docs, source/test counts, package/schema files, git branch, and git status. Use before reading many files. Skips generated paths by default (see walk filters). |
| `scaffold --root <repo>` | Copies Bible packet templates into **`<repo>/.church/bible/`** (override with `--output <dir>`). |
| `validate --root <repo>` | Checks fences, trailing whitespace, local markdown links, missing artifact terms, URLs, and requirement IDs. Default `--path` is the resolved bible dir. Optional `--requirement-prefixes S,E,C,...` rejects unknown IDs. JSON/markdown output includes `link_traversal` (`packet_local_only` vs `expanded`). |
| `sources --root <repo>` | Extracts source URLs from markdown under the bible dir by default. With `--follow-local-md`, unions URLs from linked local `.md`/`.mdx` up to `--link-depth`. |
| `claim-scan --root <repo> --banned <phrases> --required <phrases>` | Finds stale or unsafe positioning claims and missing required language. Default `--path` is the bible dir; pass `--path <repo>` to scan the whole tree. Skips hits inside balanced ASCII `"quotes"` or inline `` `ticks` `` by default (`--no-quote-allowlist` disables). Optional `--claim-config` JSON with `allow_substrings` skips banned hits on lines containing any listed substring (case-insensitive). With `--follow-local-md`, scans the same markdown link closure as `sources`/`validate`. JSON output includes `quote_skipped_hits`, `config_skipped_hits`, and `link_traversal`. |
| `intake-html --root <repo>` | Creates `vision-intake.html` under the bible dir by default. Optional `--prefill` with a prior JSON export or Markdown (`## section` / `### prompt` / body, same shape as the export) seeds textareas and embeds `<script type="application/json" id="repo-bible-prefill">` so a first visit can populate `localStorage` when empty. |
| `render-html --root <repo>` | Renders packet Markdown into **`<bible-dir>/html`** by default so humans can inspect and navigate without loading source docs into the LLM. |

**Walk filters (default on; disable with `--no-default-excludes`):** path segments matching `_repo-bible-*`, segments ending with `-html`, and spill files such as `_inventory.md`, `_validation.md`, `_sources.md`, `vision-intake.html`, `_claim-scan.md`, and `*claim*scan*.md`. Add more with repeatable `--exclude GLOB` (matched with `fnmatch` against paths relative to the walked directory).
</commands>

<recommended_flow>
For generation (from repository root; outputs land in `.church/bible/`):

```bash
scripts/repo-bible inventory --root .
scripts/repo-bible scaffold --root .
scripts/repo-bible intake-html --root .
scripts/repo-bible intake-html --root . --prefill .church/bible/prior-intake.json
```

For validation:

```bash
scripts/repo-bible validate --root .
scripts/repo-bible validate --root . --requirement-prefixes S,E,C,P,T,D,U,O --follow-local-md --link-depth 3
scripts/repo-bible sources --root .
scripts/repo-bible sources --root . --follow-local-md --format json
scripts/repo-bible render-html --root .
```

For claim drift (example scans repo root, reports still default under `.church/bible/`):

```bash
scripts/repo-bible claim-scan --root . --path . \
  --banned "best tools for any task|only marketplace|AI magic" \
  --required "quote|trust|attribution" \
  --claim-config .church/bible/claim-config.json
```
</recommended_flow>

<llm_boundary>
Use the CLI for:

- Counting files, lines, requirement IDs, URLs, and docs.
- Finding candidate evidence files.
- Copying templates.
- Generating structured HTML intake forms.
- Rendering packet Markdown to local HTML.
- Markdown/link/whitespace checks.
- Repetitive phrase scans.

Use the LLM for:

- Judging strategic implications.
- Interpreting market research.
- Resolving contradictions.
- Writing project-specific principles.
- Designing requirements and roadmap tradeoffs.
- Explaining caveats and recommendations.
</llm_boundary>
