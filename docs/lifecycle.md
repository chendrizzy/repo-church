# Lifecycle

Repo Church uses a staged loop so work can move from doctrine to execution without losing evidence, assumptions, or signoff obligations.

## The Core Loop

| Order | Stage | Command | Output |
| --- | --- | --- | --- |
| 1 | Gather | `church:gather` | Context, Bible inventory, moat status, next route |
| 2 | Discern | `church:discern` | Assumption and evidence verdict |
| 3 | Canonize | `church:canonize` | Phase anchor and spec gate verdict |
| 4 | Commission | `church:commission` | Frozen execution handoff |
| 5 | Fellowship | `church:fellowship` | Review, UAT, and signoff record |
| 6 | Bless | `church:bless` | Ship or merge readiness verdict |
| 7 | Renew | `church:renew` | Bible refresh items and next cycle setup |

The source command map is [Stage Command Map](../skills/church/references/stage-command-map.md).

## Stage Details

### Gather

Use this to initialize or resume. It loads state, inventories the Bible, checks the moat, and decides the next workflow.

Advance when project state, Bible status, moat status, and next route are known.

### Discern

Use this before planning when assumptions, claims, competitors, platform facts, dependencies, or implementation risks are unstable.

Advance when high-impact unknowns have evidence, confidence labels, or explicit closure tasks.

### Canonize

Use this to turn the Bible and roadmap into a parent phase anchor and executable spec.

Advance when requirements trace to Bible IDs or approved doctrine-change requests, acceptance criteria are measurable, and validation is defined.

### Commission

Use this to freeze scope and prepare execution.

Advance when workstreams, owners, commands, validation, rollback, and open risks are clear enough for another agent to continue.

### Fellowship

Use this for review and UAT.

Advance when objective checks pass and any required user signoff is recorded.

### Bless

Use this for release or merge readiness.

Advance when tests, docs, migrations, observability, rollback, unresolved risks, and Bible alignment are verified.

### Renew

Use this after completion or when implementation changes doctrine.

Advance when Bible drift, roadmap updates, and next-cycle anchors are captured.

## Loop Rules

| If This Happens | Loop To |
| --- | --- |
| Moat changes strategy | Bible refresh or phase anchoring |
| Survey finds implementation drift | Discern or gap closure |
| Spec gate fails | Gap closure, then canonize again |
| UAT fails | Gap closure, then handoff or UAT |
| Ship gate finds doctrine drift | Renew |
| Refresh changes roadmap order | Gather or canonize |

## Parallel Work

Parallel work is allowed only when streams have clear ownership, disjoint write scope, and a reintegration gate. Use [Parallelism Guide](../skills/church/references/parallelism-guide.md) for the detailed rules.

## Related Docs

- [Concepts](concepts.md)
- [Commands](commands.md)
- [CLI and Tooling](cli-and-tooling.md)
- [Lifecycle Model](../skills/church/references/lifecycle-model.md)
