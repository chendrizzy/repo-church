# CLI Automation Map

Repo Church uses the CLI for deterministic workflow mechanics and skills for judgment-heavy interpretation.

## Offloaded Workflows

| Workflow | CLI command | Skill still responsible for |
| --- | --- | --- |
| Project init | `church init` | Interpreting product intent and choosing greenfield/brownfield implications. |
| Workflow registry | `church registry list/show/keys` | Deciding which workflow should run next when tradeoffs exist. |
| State tracking | `church state show/get/set` | Explaining state changes and resolving contradictions. |
| Moat artifacts | `church moat init/set/import/export/render/check` | Market research, moat wording, defensibility interpretation. |
| Lifecycle progression | `church lifecycle list/show/status/advance/handoff` | Gate judgment, risk acceptance, phase sequencing rationale. |
| Fresh context loading | `church context load` | Synthesis and prioritization from the loaded state. |
| Assumption/gap/UAT/risk ledgers | `church ledger init/add/list/check` | Writing high-quality findings and deciding severity. |
| Bible tooling | `church bible ...` | Bible synthesis, doctrine updates, and market-backed claims. |
| Codebase survey mechanics | `church context load`, `church bible inventory`, `church lifecycle advance survey` | Architecture interpretation, interface-risk judgment, and implementation drift severity. |
| Runtime hook planning | `church hooks plan/check/scaffold` | Selecting which runtime adapters to enable and reviewing adapter risks. |
| Workspace and thread records | `church workspace ...`, `church thread ...` | Deciding work partitioning, stale-context risk, and continuation quality. |
| Inbox/backlog capture | `church inbox add/list/check` | Prioritization, scope approval, and doctrine impact. |
| Profile artifacts | `church profile init/set/export/check` | Behavioral interpretation, personalization ethics, and whether signals should affect work. |
| Sketch artifacts | `church sketch register/list/check` | Creative direction, design quality, and subjective acceptance. |
| Git hygiene planning | `church branch plan`, `church undo plan` | Whether to execute git operations and how to handle destructive risk. |
| Archive planning | `church archive plan` | Retention policy and whether artifacts are safe to move. |

## Automation Boundary

The CLI should own:

- idempotent artifact creation,
- state key storage,
- workflow dictionary lookup,
- gate status recording,
- ledger serialization,
- moat completeness scoring,
- context and handoff rendering,
- Bible CLI delegation,
- survey gate recording when brownfield codebase mapping affects planning.

The agent should own:

- research judgment,
- product strategy,
- market interpretation,
- architecture tradeoffs,
- spec quality assessment,
- UX and brand judgment,
- risk acceptance recommendations.

## Target Command Groups

```bash
church init
church registry list|show|keys
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

All commands are non-interactive, accept `--root`, and return structured output where practical.

## Reasoning Boundary Command

Use this before deciding whether to automate more:

```bash
church registry reasoning --format markdown
church registry reasoning moat --format json
```

The output states `cli_owned`, `agent_owned`, and `do_not_fully_automate` for each workflow.

## GSD Coverage

See `references/gsd-workflow-assessment.md` for the workflow-by-workflow assessment of the local GSD library and the true/false questionnaire used to classify each workflow. Apply that questionnaire when adding new Repo Church command groups: automate reproducible mechanics, preserve agent judgment where full automation would reduce planning, review, debugging, design, or UAT quality.
