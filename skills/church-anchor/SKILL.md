---
name: church-anchor
description: Strengthen Repo Church parent phase anchors before child specs or implementation. Use when the user asks to improve roadmap phases, tighten phase requirements, define parent phase anchors, sequence dependencies, or raise acceptance thresholds before planning.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Phase Anchor

A phase anchor is the parent contract for child plans. It should be strong enough for independent agents to create compatible specs without guessing.

## Inputs

- Bible roadmap and success requirements.
- Architecture map and design doctrine.
- Market watchlist and validation report.
- Existing phase plan or proposed milestone.

## Anchor Requirements

Each phase anchor must include:

- objective,
- in scope,
- out of scope,
- Bible requirement IDs,
- measurable acceptance criteria,
- user stories and must-pass journeys,
- architecture and interface contracts,
- data, migration, and operational constraints,
- design doctrine,
- dependency order,
- risks and assumptions,
- observability and rollback,
- required validation and signoff mode.

## Procedure

1. Load deterministic context: `church context load --root <repo> --format markdown`.
2. Inspect the workflow contract: `church lifecycle show anchor --format markdown`.
3. Read the proposed phase and relevant Bible artifacts.
4. Build a traceability table from Bible requirements to phase outcomes.
5. Identify missing details that would cause divergent implementation.
6. Record anchor gaps with `church ledger add gaps ...` when they block independent execution.
7. Advance only after judgment: `church lifecycle advance anchor --root <repo> --outcome PASS|PASS_WITH_RISK|HOLD|BLOCK --phase <phase> --evidence <anchor-artifact>`.

## Output

```markdown
## Anchor Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Phase Anchor
Phase:
Objective:
Scope:
Non-goals:
Requirements:
Interfaces:
Dependencies:
Verification:
Signoff mode:

## Traceability
| Requirement | Phase outcome | Acceptance metric | Evidence |
| --- | --- | --- | --- |

## Anchor Gaps
| Gap | Severity | Required fix | Owner | Recheck |
| --- | --- | --- | --- | --- |
```

## Blockers

Return `BLOCK` if the phase cannot be reconciled with Bible doctrine or if core acceptance criteria are not measurable.
