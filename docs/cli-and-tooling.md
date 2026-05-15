# CLI and Tooling

Repo Church is CLI-first where work is deterministic and agent-driven where judgment matters.

## What The CLI Owns

The CLI should handle reproducible mechanics:

- project initialization,
- workflow registry lookup,
- state storage,
- moat artifact storage and completeness checks,
- lifecycle status and handoff rendering,
- ledger serialization,
- context loading,
- workspace and thread records,
- inbox, profile, sketch, hook, branch, undo, and archive planning,
- Bible CLI delegation.

Source reference: [CLI Automation Map](../skills/church/references/cli-automation-map.md).

## What The Agent Owns

The agent or user should still own:

- product strategy,
- market and moat interpretation,
- architecture tradeoffs,
- spec quality,
- UX and brand judgment,
- security review,
- debugging hypotheses,
- risk acceptance,
- user acceptance.

The CLI can make these decisions easier to inspect. It should not pretend to make them automatically.

## Common Commands

From this package root:

```bash
skills/church/scripts/church init --root <repo> --mode brownfield
skills/church/scripts/church registry list --format json
skills/church/scripts/church registry reasoning --format markdown
skills/church/scripts/church lifecycle status --root <repo> --format json
skills/church/scripts/church lifecycle handoff --root <repo> --format markdown
skills/church/scripts/church context load --root <repo> --format markdown --include-history
skills/church/scripts/church bible inventory --root <repo> --format markdown
```

## Full Command Groups

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

## HTML Workbench

Use the HTML workbench when dense human input or review would be awkward in chat:

- large vision intake,
- Bible packet review,
- UAT criteria review,
- stakeholder scan,
- artifact navigation.

Source references:

- [Tooling Workbench](../skills/church/references/tooling-workbench.md)
- [Repo Bible CLI Offload](../skills/repo-bible/references/cli-offload.md)

## Architecture References

- [CLI Architecture](../skills/church/references/cli-architecture.md)
- [CLI Automation Map](../skills/church/references/cli-automation-map.md)
- [GSD Workflow Assessment](../skills/church/references/gsd-workflow-assessment.md)
