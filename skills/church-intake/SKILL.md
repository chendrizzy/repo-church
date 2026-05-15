---
name: church-intake
description: Run Repo Church Bible intake and thin roadmap slicing. Use when the user asks for church intake, bible intake, roadmap from repo-bible, phase discovery, next milestone framing, or a lightweight planning entry point before research hardening.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Intake

Use this skill after a Repo Bible exists or during initial project init. If no state exists, run the CLI first.

## Inputs

- Repo root.
- Bible packet path, usually `.church/bible/`.
- Current planning files, if any.
- User's current objective.

## Procedure

1. Initialize or load deterministic state:
   - `church init --root <repo> --mode greenfield|brownfield`
   - `church context load --root <repo> --format markdown`
2. Run or reuse Repo Bible CLI inventory:
   - `church bible inventory --root <repo> --format markdown`
3. If vision capture is broad or under-specified, use the HTML workbench: `church bible intake-html --root <repo>` or `church bible intake-html --root <repo> --prefill <prior-export>`.
4. Locate Bible files: packet index, success requirements, roadmap, architecture map, design doctrine, UX workflows, market watchlist, validation report.
5. Extract intake anchors:
   - problem,
   - target user/buyer,
   - non-goals,
   - success metrics,
   - hard constraints,
   - relevant requirement IDs,
   - UX must-pass workflows,
   - market threats,
   - architecture/design constraints.
6. Produce a thin roadmap slice: next milestone, 3 to 5 outcomes, dependencies, and missing evidence.
7. Record route if clear: `church lifecycle advance <workflow> --root <repo> --outcome HOLD|PASS`.
8. Do not deep-plan implementation yet. Route unknowns to `church-harden`.

## Output

```markdown
## Intake Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Intake Anchors
| Anchor | Evidence | Impact |
| --- | --- | --- |

## Thin Roadmap Slice
Milestone:
Outcomes:
Dependencies:
Must-not-start-until:

## Route Next
Recommended next skill:
Reason:

## Tooling Used
CLI:
HTML workbench:
Skipped tools and why:
```

## Blockers

Return `HOLD` when the Bible path is missing or the core user/outcome/constraints cannot be found. Return `BLOCK` when the Bible contradicts active planning state.
