---
name: church-moat
description: Identify and define a project's competitive moat with strategic market research, elevator-pitch clarity, sustainability scoring, and Repo Bible integration. Use during greenfield or brownfield project init, market positioning, competitive leverage analysis, defensibility review, or whenever the user asks what makes the project hard to copy.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Moat

This skill defines the project's competitive leverage in a form the owner can pitch and a third party can understand quickly.

## Default Timing

Run this during initial Repo Church project init for both greenfield and brownfield projects. The moat should feed into the Repo Bible's positioning, success requirements, roadmap, architecture doctrine, GTM, and validation report.

## CLI First

Use the deterministic CLI when available:

```bash
skills/church/scripts/church init --root <repo> --mode greenfield
skills/church/scripts/church moat init --root <repo>
skills/church/scripts/church moat set --root <repo> elevator_pitch "..."
skills/church/scripts/church moat import --root <repo> --stdin --merge
skills/church/scripts/church moat export --root <repo> --format markdown
skills/church/scripts/church moat check --root <repo>
skills/church/scripts/church moat render --root <repo>
```

The CLI writes:

- `.church/state.json`
- `.church/moat/moat.json`
- `.church/moat/moat.md`

The CLI creates, stores, renders, and scores the moat. The agent still owns market research quality, wording clarity, and defensibility judgment.

## Research Framework

Read `church/references/moat-framework.md` when you need the full rubric.

At minimum, define:

- elevator pitch,
- one-sentence moat,
- third-party summary,
- urgent market pain,
- direct competitors,
- adjacent competitors,
- status quo,
- entry wedge,
- primary leverage source,
- what compounds with use,
- what gets harder to copy,
- proof,
- missing evidence,
- validation tests.

## Output

```markdown
## Moat Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Elevator Pitch

## One-Sentence Moat

## Third-Party Summary

## Competitive Leverage
| Dimension | Answer | Evidence | Risk |
| --- | --- | --- | --- |

## Sustainability Scorecard
| Dimension | Score 0-4 | Evidence | Next validation |
| --- | --- | --- | --- |

## Bible Integration
| Bible artifact | Required update |
| --- | --- |

## Validation Tasks
| Task | Automatable? | Proves |
| --- | --- | --- |
```

## Gate Standard

Return `PASS` only when the moat is clear enough for a non-expert to repeat, backed by current market evidence, and connected to concrete roadmap or GTM choices. Return `HOLD` when the moat is plausible but insufficiently proven. Return `BLOCK` when the proposed moat is generic, easy to copy, or contradicted by market evidence.
