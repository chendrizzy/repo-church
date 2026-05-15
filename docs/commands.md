# Commands

Repo Church commands are staged entry points. They load the right skill, run CLI preflight where possible, and produce a predictable output shape.

## Core Staged Commands

| Command | Use When | Source Asset |
| --- | --- | --- |
| `church:gather` | Start or resume lifecycle work. | [command](../commands/church-gather.md) |
| `church:discern` | Harden assumptions, sources, and ambiguity. | [command](../commands/church-discern.md) |
| `church:canonize` | Tighten anchors, specs, traceability, and acceptance. | [command](../commands/church-canonize.md) |
| `church:commission` | Freeze scope and prepare execution handoff. | [command](../commands/church-commission.md) |
| `church:fellowship` | Run peer review, UAT, and mutual signoff. | [command](../commands/church-fellowship.md) |
| `church:bless` | Gate merge or release readiness. | [command](../commands/church-bless.md) |
| `church:renew` | Refresh Bible doctrine and set up the next cycle. | [command](../commands/church-renew.md) |

## Optional Operational Commands

| Command | Use When | Source Asset |
| --- | --- | --- |
| `church:survey` | Brownfield code, architecture, interfaces, or drift may affect planning. | [command](../commands/church-survey.md) |
| `church:guard` | Runtime hooks or portable guardrail scaffolds are needed. | [command](../commands/church-guard.md) |
| `church:workspace` | Workstream or workspace state needs tracking. | [command](../commands/church-workspace.md) |
| `church:thread` | Continuation records or resume hints are needed. | [command](../commands/church-thread.md) |
| `church:inbox` | Backlog, risk, or requirement capture needs triage. | [command](../commands/church-inbox.md) |
| `church:profile` | Consented workflow personalization should be recorded. | [command](../commands/church-profile.md) |
| `church:sketch` | Design artifacts or creative signoff need routing. | [command](../commands/church-sketch.md) |
| `church:branch` | PR-safe branch scope needs planning. | [command](../commands/church-branch.md) |
| `church:rewind` | Undo, restore, or rollback needs a guarded plan. | [command](../commands/church-rewind.md) |
| `church:archive` | Artifact cleanup or archiving needs a dry-run plan. | [command](../commands/church-archive.md) |
| `church:confess` | Ad hoc gaps, risks, requirements, or phase ideas need capture. | [command](../commands/church-confess.md) |
| `church:atonement` | Debugging, diagnosis, remediation, and recheck are needed. | [command](../commands/church-atonement.md) |
| `church:quick-rite` | A small low-risk task does not need the full cycle. | [command](../commands/church-quick-rite.md) |
| `church:council` | A command-center or status view is needed. | [command](../commands/church-council.md) |

## Command Selection

| Situation | Command |
| --- | --- |
| New project or stale context | `church:gather` |
| Planning feels premature | `church:discern` |
| Spec quality is uncertain | `church:canonize` |
| Execution can start but needs clean scope | `church:commission` |
| Feature exists and needs acceptance | `church:fellowship` |
| Work is ready to merge or release | `church:bless` |
| Product doctrine changed | `church:renew` |
| Task is truly tiny and low risk | `church:quick-rite` |

## Source References

- [Stage Command Map](../skills/church/references/stage-command-map.md)
- [Lifecycle Model](../skills/church/references/lifecycle-model.md)
- [CLI Automation Map](../skills/church/references/cli-automation-map.md)
