# Concepts

Repo Church turns project doctrine into phase-gated work. The framework is designed for agent-heavy repositories where context drift, weak assumptions, or skipped verification can quietly degrade the outcome.

## Repo Bible

The Repo Bible is the durable source of truth for a project. It usually lives under `.church/bible/` in the target repository and contains strategy, requirements, market context, principles, roadmap, architecture and design doctrine, UX workflows, GTM, and validation evidence.

Use `repo-bible` when the Bible itself needs to be generated, audited, or refreshed. Use `church` when work needs to move through lifecycle gates using the Bible as input.

Source references:

- [repo-bible/SKILL.md](../skills/repo-bible/SKILL.md)
- [Bible Method](../skills/repo-bible/references/bible-method.md)
- [Quality Gates](../skills/repo-bible/references/quality-gates.md)

## Lifecycle

The lifecycle is a repeatable loop:

```text
gather -> discern -> canonize -> commission -> fellowship -> bless -> renew
```

Each stage consumes evidence, produces an artifact or verdict, and decides whether the work can advance.

Source references:

- [Lifecycle Model](../skills/church/references/lifecycle-model.md)
- [Stage Command Map](../skills/church/references/stage-command-map.md)

## Gates

A gate is a decision checkpoint. Gate outcomes are:

| Outcome | Meaning |
| --- | --- |
| `PASS` | Continue. Required evidence is present. |
| `PASS_WITH_RISK` | Continue, but carry an explicit risk. |
| `HOLD` | Pause and close a gap before advancing. |
| `BLOCK` | Stop. A required condition is missing or contradicted. |

Source reference: [Gate Taxonomy](../skills/church/references/gate-taxonomy.md).

## Ledgers

Ledgers keep uncertainty visible. They record assumptions, gaps, risks, UAT items, blockers, owners, evidence, status, and closure proof.

Use ledgers when a claim is not yet proven, an implementation detail contradicts doctrine, or a user signoff path is required.

Source references:

- [CLI Automation Map](../skills/church/references/cli-automation-map.md)
- [Research Confidence](../skills/church/references/research-confidence.md)

## Moat

The moat pass defines the competitive leverage that should shape the Bible, roadmap, architecture, and GTM. It is not a marketing slogan. It should be simple enough for the owner to pitch and for a third party to repeat.

Source reference: [Moat Framework](../skills/church/references/moat-framework.md).

## Collaborative UAT

UAT is a phase-progression gate, not only a final checklist. The agent validates objective evidence first. The user signs off on subjective, strategic, brand, or workflow fit when the risk calls for it.

Source reference: [Verification Protocol](../skills/church/references/verification-protocol.md).

## Refresh

When implementation changes doctrine, architecture, market positioning, success metrics, or phase order, Repo Church creates a refresh item. The Bible should not drift behind the product.

## Related Docs

- [Getting Started](getting-started.md)
- [Lifecycle](lifecycle.md)
- [Commands](commands.md)
