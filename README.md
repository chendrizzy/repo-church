# Repo Church Agent Skills

Repo Church is an agent-agnostic skill package for bible-grounded repository planning, phase chaining, gap closure, and collaborative verification.

It builds around `repo-bible` as the durable vision and requirements source, then adds stricter lifecycle gates inspired by mature GSD-style phase workflows:

- explicit artifact consumption before planning or execution,
- CLI-first inventory, validation, source extraction, and claim scanning,
- HTML workbench capture and review before long-form synthesis,
- research-backed assumption confidence,
- stronger parent phase anchors and spec acceptance thresholds,
- gap ledgers with closure proofs,
- parallelizable lifecycle passes,
- collaborative UAT and mutual signoff gates,
- default moat identification during greenfield or brownfield init,
- ship checks that trace back to the Repo Bible.

## Install

From this repository:

```bash
npx skills add ./agent-skills/repo-church --all
```

Install only the umbrella skill:

```bash
npx skills add ./agent-skills/repo-church --skill church
```

Install the Bible generator and church workflow together:

```bash
npx skills add ./agent-skills/repo-church --skill repo-bible --skill church
```

## Skills

| Skill | Purpose |
| --- | --- |
| `repo-bible` | Generate, audit, and refresh the durable Repo Bible packet. |
| `church` | Route and orchestrate the full church lifecycle. |
| `church-moat` | Identify the project's competitive moat and integrate it into the Bible. |
| `church-intake` | Convert Bible outputs into intake anchors and a thin roadmap slice. |
| `church-harden` | Research and confidence-gate assumptions before planning. |
| `church-anchor` | Strengthen parent phase anchors before specs or execution. |
| `church-spec-gate` | Review specs for measurable, traceable acceptance. |
| `church-gap-closure` | Turn gaps, drift, and contradictions into closure work. |
| `church-handoff` | Freeze phase scope and produce an execution handoff. |
| `church-uat` | Run collaborative user acceptance testing against Bible criteria. |
| `church-ship` | Gate merge/release readiness with evidence, rollback, and Bible alignment. |
| `church-optimizer` | Reduce lifecycle redundancy and improve safe parallelism. |

## Commands

Core staged commands:

| Command | Purpose |
| --- | --- |
| `church:gather` | Init/resume, context load, moat/Bible inventory, next route. |
| `church:discern` | Assumption hardening, source checks, ambiguity closure. |
| `church:canonize` | Parent anchor, spec gate, traceability, specialist review routing. |
| `church:commission` | Execution handoff, safe parallelism, validation/rollback path. |
| `church:fellowship` | Peer review, collaborative UAT, mutual signoff. |
| `church:bless` | Ship/merge gate, release risk, rollback, Bible drift. |
| `church:renew` | Bible refresh, learnings, next cycle setup. |

Operational shortcuts:

| Command | Purpose |
| --- | --- |
| `church:survey` | Map brownfield code, architecture, interfaces, and drift before planning. |
| `church:guard` | Plan/check/scaffold runtime hooks with portable fallbacks. |
| `church:workspace` | Manage workspace records and active workspace state. |
| `church:thread` | Manage thread continuation records and resume hints. |
| `church:inbox` | Capture and triage inbox/backlog items. |
| `church:profile` | Capture consented profile signals for workflow personalization. |
| `church:sketch` | Register creative/design artifacts and signoff requirements. |
| `church:branch` | Plan PR-safe branch scope without mutating git state. |
| `church:rewind` | Plan guarded undo/rollback operations. |
| `church:archive` | Plan artifact cleanup/archive operations. |
| `church:confess` | Capture ad hoc gaps, risks, requirements, or phase ideas. |
| `church:atonement` | Debug, diagnose, remediate, and recheck failures. |
| `church:quick-rite` | Small low-risk tasks without full cycle overhead. |
| `church:council` | Command-center/status view. |

See `skills/church/references/stage-command-map.md` for the command-to-GSD mapping, `skills/church/references/counterpart-gap-closure.md` for the closed counterpart gaps, and `skills/church/references/deferred-parity-closure.md` for the corrective pass that converted the previously deferred parity rows into assets.

## Agents

Specialist profiles are lazy-loaded by commands as needed:

`church-moat-scout`, `church-bible-scribe`, `church-codebase-cartographer`, `church-runtime-guardian`, `church-workspace-steward`, `church-thread-steward`, `church-triage-steward`, `church-profile-counselor`, `church-sketch-curator`, `church-git-steward`, `church-archive-steward`, `church-anchor-architect`, `church-spec-canonist`, `church-doctrine-auditor`, `church-gap-steward`, `church-workstream-deacon`, `church-uat-fellow`, `church-ship-steward`, `church-code-examiner`, `church-security-examiner`, `church-ui-examiner`, `church-ai-eval-planner`, `church-debug-examiner`, and `church-doc-scribe`.

## Tooling Philosophy

Repo Church inherits the Repo Bible workflow preference for deterministic tooling before agent synthesis:

- Use `church` as the root lifecycle CLI and command namespace.
- Run CLI inventory before reading many files.
- Generate HTML intake/workbench views when dense user input or human review is needed.
- Render Markdown packets to HTML for navigable review instead of forcing agents to hold every artifact in context.
- Use validation, source extraction, and claim scans to produce compact evidence reports.
- Let agents interpret tradeoffs and resolve contradictions after the tooling has reduced noise.

The bundled `church` skill includes `scripts/church` for lifecycle state, moat, handoff, and Bible delegation. The bundled `repo-bible` skill includes `scripts/repo-bible` and `scripts/repo_bible.py` for Bible-specific operations.

## CLI Shape

Preferred root commands:

```bash
agent-skills/repo-church/skills/church/scripts/church init --root . --mode brownfield
agent-skills/repo-church/skills/church/scripts/church moat check --root .
agent-skills/repo-church/skills/church/scripts/church lifecycle status --root .
agent-skills/repo-church/skills/church/scripts/church lifecycle handoff --root .
agent-skills/repo-church/skills/church/scripts/church bible inventory --root .
```

`church bible ...` delegates to the nested Repo Bible CLI. Keep the standalone `repo-bible` command as a compatibility shim and internal module boundary.

The full deterministic command surface is:

```bash
church init
church registry list|show|keys|reasoning
church state show|get|set
church moat init|set|import|export|render|check
church lifecycle list|show|status|advance|handoff
church ledger init|add|list|check
church context load
church workspace list|create|status|switch|complete
church thread list|create|status|resume|complete
church inbox add|list|check
church profile init|set|export|check
church sketch register|list|check
church hooks plan|check|scaffold
church branch plan
church undo plan
church archive plan
church bible ...
```

## Package Shape

This package follows the skills.sh agent skill shape:

```text
repo-church/
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
  evals/
    evals.json
```

Every skill directory contains a `SKILL.md` with `name` and `description` frontmatter. Skill names match their directory names, use lowercase kebab-case, and include trigger language in the description.

## Validate

```bash
bash agent-skills/repo-church/skills/church/scripts/validate-package.sh agent-skills/repo-church
python3 agent-skills/repo-church/tests/test_church_plugin_assets.py
python3 agent-skills/repo-church/tests/test_church_cli.py
```

The validator checks skill frontmatter, command and agent discovery assets, kebab-case names, name-to-file alignment, local reference paths, and the eval file.

## Design Notes

Repo Church deliberately avoids tying the package to one agent runtime. Cursor, Codex, Claude Code, Cline, OpenCode, Devin, and other skills.sh-compatible agents should be able to install the same skill package. Project-local wrappers may still exist under `.agents/skills/`, `.claude/skills/`, or another agent directory, but this source package should remain portable.

The framework also avoids promising that a checklist can guarantee market success. It translates "guarantee success" into measurable gates that eliminate preventable failure modes, maximize probability, and force unknowns into visible validation work.
