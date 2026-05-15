---
name: church-spec-gate
description: Review specs and implementation plans against Repo Church gates. Use when the user asks for spec review, plan hardening, PRD acceptance, implementation plan viability, requirement traceability, or stricter pre-execution approval.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Spec Gate

Use this skill before execution. The goal is to prevent under-specified plans from producing inefficient, brittle, or misaligned code.

## Inputs

- Parent phase anchor.
- Proposed spec, PRD, or implementation plan.
- Bible requirements, architecture doctrine, design doctrine, and UX workflows.
- Assumption ledger.

## Required Spec Coverage

- requirement IDs and source doctrine,
- explicit non-goals,
- affected modules/files/services,
- API/data/interface contracts,
- dependency ordering,
- error states and edge cases,
- performance/scalability expectations,
- observability and rollback,
- test plan,
- UAT/user-story validation,
- AI integration phase needs, if any,
- post-phase Bible refresh obligations.

## Procedure

1. Load context: `church context load --root <repo> --format markdown`.
2. Compare the spec against the parent anchor.
3. Verify every acceptance criterion is measurable.
4. Run or reuse `church bible validate --root <repo> --follow-local-md` when the spec references Bible or planning markdown.
5. Check implementation sequence and dependency order.
6. Check whether execution can be parallelized safely.
7. Emit missing work as closure items with `church ledger add gaps ...`.
8. Record the gate with `church lifecycle advance spec-gate --root <repo> --outcome PASS|PASS_WITH_RISK|HOLD|BLOCK --evidence <spec-or-review-artifact>`.

## Output

```markdown
## Spec Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Coverage Matrix
| Area | Required? | Present? | Evidence | Gap |
| --- | --- | --- | --- | --- |

## Execution Risk
| Risk | Cause | Impact | Mitigation |
| --- | --- | --- | --- |

## Required Revisions
| ID | Source gap | Severity | Revision | Owner | Acceptance test | Evidence required | Recheck command | Blocks? | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Tooling Used
Validation report:
Skipped tools and why:
```

## Acceptance Threshold

The spec may pass only if a capable executor can start without inventing product direction, architecture contracts, or verification criteria.
