---
name: repo-bible
description: Generates, audits, and refreshes comprehensive repo Bible packets for products, platforms, and projects. Use when the user asks to create a strategic reference packet, commandments, operating doctrine, market-backed roadmap, product constitution, GTM plan, architecture/design doctrine, or reusable repo bible.
---

<objective>
Generate a repo Bible: a durable packet of reference assets that governs strategy, market positioning, requirements, roadmap, architecture, infrastructure, UX, design, customer personas, GTM, operating principles, and success gates for any repository, project, or product.

This skill is intentionally strict. It turns research, local evidence, competitive analysis, implementation reality, and product philosophy into verifiable artifacts that future agents and humans can use before planning or executing work.
</objective>

<church_layout>
**Repo Church** is the umbrella for machine- and operator-generated artifacts under `<repo>/.church/`:

| Path | Purpose |
|------|---------|
| `bible/` | **Repo Bible packet** — markdown doctrine/requirements, `_repo-bible-*.md` CLI tool reports, `vision-intake.html`, and `html/` (default output of `render-html`) for human review. |
| `runs/` | Local scratch exports (operators should keep this gitignored). |
| `README.md` | Operator map; created on first `scaffold` if missing. |
| `index.json` | Small manifest (`church_root`, `bible_dir` relative to repo root); refreshed by `scaffold`. |

Defaults resolve under **`<repo>/.church/bible/`** (override with `--church-root`, `--bible-dir`, or `CHURCH_ROOT`). One-time migration from `.planning/commandments/`: copy the tree into `.church/bible/`, or re-run generation with `--legacy-planning-bible` while reading old paths.

Use **`--output -`** on inventory, sources, validate, or claim-scan when you need stdout instead of the default report file under `bible/`.
</church_layout>

<quick_start>
If the user asks to create a Bible from scratch, read `workflows/generate-bible.md` and follow it.

If the user asks to review or improve an existing Bible, read `workflows/audit-bible.md`.

If the user asks to update a Bible for new market data, roadmap drift, or implementation changes, read `workflows/refresh-bible.md`.

Before loading large local docs, run the CLI helper where possible (paths default to **`<repo>/.church/bible/`**):

```bash
python scripts/repo_bible.py inventory --root <repo> --format markdown
```

For interactive vision capture or human review (defaults write under `.church/bible/`):

```bash
python scripts/repo_bible.py intake-html --root <repo>
python scripts/repo_bible.py intake-html --root <repo> --prefill <prior-export.json-or.md>
python scripts/repo_bible.py render-html --root <repo>
```

Walk hygiene defaults skip `_repo-bible-*`, `*-html` trees, and common spill files (`_inventory.md`, `_validation.md`, etc.); override with `--no-default-excludes` or add `--exclude GLOB`. Use `--follow-local-md` on `sources`, `validate`, and `claim-scan` to traverse linked markdown; use `--requirement-prefixes` on `validate` to enforce ID families.
</quick_start>

<essential_principles>
**Evidence before certainty.** Do not state that a requirement, market claim, or success path is proven unless local artifacts or current sources support it. If a claim is aspirational, label it as a hypothesis and attach a validation gate.

**No magic guarantees.** Translate "guarantee success" into enforceable gates that maximize probability and eliminate preventable failure modes. Avoid claiming unconditional market success.

**Local reality first.** Inspect the repo/product artifacts before inventing strategy. Current code, docs, tickets, designs, tests, analytics, and prior research constrain the Bible.

**Current market second.** Refresh unstable market facts with current sources. Competitors, platform policies, pricing, standards, integration surfaces, and buyer expectations change quickly.

**Actionability per requirement.** Every success requirement must include at least one concrete task, preferably automatable, that can close or verify the requirement.

**Phase-gated doctrine.** The Bible must become a working operating system: roadmap phases, architecture components, design choices, GTM work, and future plans cite the Bible's requirement IDs.

**Conflicts first, then fixes.** Capture false assumptions, drift, contradictions, weak claims, and misalignments before resolving them. Do not silently rewrite history.

**User-facing clarity.** Use maps, matrices, timelines, Venn-style diagrams, blueprints, and flows when they materially improve decision-making or can be reused in public/product surfaces.
</essential_principles>

<intake>
When needed, ask only the missing questions:

- What project/root path should the Bible govern?
- Is this a full first Bible, an audit, or a refresh?
- Should the output be project-local, repo-local, or a standalone document packet?
- Are there must-use research docs, strategy docs, designs, or prior planning artifacts?

If the user already provided enough context, do not ask. Proceed.
</intake>

<routing>
| User intent | Workflow |
|---|---|
| Create/build/generate a Bible, commandments packet, operating doctrine, strategic packet | `workflows/generate-bible.md` |
| Audit/review/check an existing Bible or planning packet | `workflows/audit-bible.md` |
| Refresh/update/iterate an existing Bible with new research, market changes, or implementation drift | `workflows/refresh-bible.md` |
| Unclear | Ask the smallest clarifying question, then route |

After reading the selected workflow, follow it exactly and load only the references/templates it requests.
</routing>

<reference_index>
**Method:** `references/bible-method.md`
**Research:** `references/research-protocol.md`
**Validation:** `references/quality-gates.md`
**CLI offload:** `references/cli-offload.md`
</reference_index>

<templates_index>
Use templates only when writing corresponding artifacts:

- `templates/packet-index.md`
- `templates/success-requirements.md`
- `templates/market-watchlist.md`
- `templates/principles-doctrine.md`
- `templates/architecture-map.md`
- `templates/design-doctrine.md`
- `templates/persona-gtm.md`
- `templates/ux-workflows.md`
- `templates/roadmap.md`
- `templates/alignment-audit.md`
- `templates/validation-report.md`
</templates_index>

<success_criteria>
The skill succeeds when the project has a Bible packet with:

- Current market landscape, threats, gaps, opportunities, and watchlist.
- Evidence-backed principles, philosophies, and practical guidelines.
- Measurable success requirements with automatable tasks.
- Roadmap, PRD/spec implications, phase gates, and remediation plans.
- Architecture, infrastructure, systems, and design doctrines.
- UX non-negotiables and must-pass workflows.
- Target personas, PMF rationale, acquisition strategy, and GTM plan.
- Visual maps/graphs/flowcharts where useful.
- Validation report proving artifact coverage and known caveats.
</success_criteria>
