---
name: church-harden
description: Harden assumptions with local evidence and current research before planning. Use for church harden, assumption validation, research hardening, evidence gate, market-confidence checks, stale claim review, or GSD-style pre-plan risk tightening.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Research Hardening

This skill prevents weak assumptions from becoming implementation plans.

## Inputs

- Intake anchors or proposed phase/spec.
- Bible market watchlist, success requirements, roadmap, and validation report.
- Local implementation evidence when relevant.

## Procedure

1. Load context: `church context load --root <repo> --format markdown`.
2. Initialize the assumption ledger if needed: `church ledger init assumptions --root <repo>`.
3. Run Repo Bible source extraction and claim scanning:
   - `church bible sources --root <repo> --follow-local-md --format json`
   - `church bible claim-scan --root <repo> --path <repo> --banned <phrases> --required <phrases>`
4. List critical claims and classify each as `verified-local`, `verified-current`, `supported-secondary`, `user-intent`, `hypothesis`, `stale`, or `contradicted`.
5. Record each material assumption with `church ledger add assumptions --root <repo> --id A-... --status <status> --summary <claim> --evidence <source> --owner <owner>`.
6. Run `church ledger check assumptions --root <repo>` before planning.
7. Research high-impact or unstable claims using current primary sources where possible.
8. Route `hypothesis`, `stale`, or `contradicted` high-impact claims to gap closure before planning.

## Output

```markdown
## Evidence Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Assumption Ledger
| ID | Claim | Confidence | Evidence | Impact if wrong | Required validation | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Research Notes
- Source:
- Finding:
- Planning impact:

## Planning Permission
Can proceed: yes|no
Conditions:

## Tooling Used
Sources report:
Claim scan:
Skipped tools and why:
```

## Acceptance Threshold

High-impact assumptions must be verified or explicitly deferred with owner, mitigation, and a recheck point. Do not allow implementation planning to rest on unlabeled inference.
