# Skills

Repo Church is packaged as composable skills. Start with the umbrella skills, then load child skills only when their stage is relevant.

## Umbrella Skills

| Skill | Purpose | Source |
| --- | --- | --- |
| `repo-bible` | Generate, audit, and refresh the durable Repo Bible packet. | [SKILL.md](../skills/repo-bible/SKILL.md) |
| `church` | Route and orchestrate the lifecycle around the Repo Bible. | [SKILL.md](../skills/church/SKILL.md) |

Use `repo-bible` when the doctrine packet itself is the work. Use `church` when the project needs lifecycle routing, gates, ledgers, handoff, UAT, or ship readiness.

## Lifecycle Skills

| Skill | Purpose | Source |
| --- | --- | --- |
| `church-moat` | Define the competitive moat and integrate it into the Bible. | [SKILL.md](../skills/church-moat/SKILL.md) |
| `church-intake` | Convert Bible outputs into intake anchors and a thin roadmap slice. | [SKILL.md](../skills/church-intake/SKILL.md) |
| `church-harden` | Research and confidence-gate assumptions before planning. | [SKILL.md](../skills/church-harden/SKILL.md) |
| `church-anchor` | Strengthen parent phase anchors before specs or execution. | [SKILL.md](../skills/church-anchor/SKILL.md) |
| `church-spec-gate` | Review specs for measurable, traceable acceptance. | [SKILL.md](../skills/church-spec-gate/SKILL.md) |
| `church-gap-closure` | Turn gaps, drift, and contradictions into closure work. | [SKILL.md](../skills/church-gap-closure/SKILL.md) |
| `church-handoff` | Freeze phase scope and produce an execution handoff. | [SKILL.md](../skills/church-handoff/SKILL.md) |
| `church-uat` | Run collaborative user acceptance testing against Bible criteria. | [SKILL.md](../skills/church-uat/SKILL.md) |
| `church-ship` | Gate merge or release readiness with evidence, rollback, and Bible alignment. | [SKILL.md](../skills/church-ship/SKILL.md) |
| `church-optimizer` | Reduce lifecycle redundancy and improve safe parallelism. | [SKILL.md](../skills/church-optimizer/SKILL.md) |

## Loading Pattern

1. Start with `church` for routing.
2. Load `repo-bible` only when Bible generation, audit, or refresh is needed.
3. Load one child skill for the active gate.
4. Load specialist agents only when their evidence or review is required.

## Related Docs

- [Commands](commands.md)
- [Agents](agents.md)
- [Reference Index](reference-index.md)
