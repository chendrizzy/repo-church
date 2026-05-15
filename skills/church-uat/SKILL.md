---
name: church-uat
description: Run collaborative Repo Church UAT with stricter phase-progression gates and mutual signoff. Use when the user asks for user testing, collaborative verification, UAT, acceptance walkthrough, mutual approval, must-pass stories, or post-phase validation.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Collaborative UAT

This skill validates implemented work against Bible success requirements, UX workflows, and phase acceptance criteria.

## Inputs

- Built feature or completed phase.
- Success requirements and UX workflows.
- Phase anchor and spec acceptance criteria.
- Test/build results.

## Procedure

1. Initialize UAT ledger if needed: `church ledger init uat --root <repo>`.
2. Build a UAT matrix from requirements and user stories.
3. Render the Bible packet to HTML when criteria review or user signoff would benefit: `church bible render-html --root <repo>`.
4. Run objective checks first: tests, build, lint, screenshots, API calls, logs, migrations as relevant.
5. Record each UAT result with `church ledger add uat ...`.
6. Convert failures to gap-closure items with `church ledger add gaps ...`.
7. Record signoff state with `church state set signoff.agent true` and, when the user approves, `church state set signoff.user true`.
8. Require mutual signoff when strategic, subjective, brand, data, security, pricing, or roadmap decisions are involved.
9. Advance with `church lifecycle advance uat --root <repo> --outcome PASS|HOLD|BLOCK`.

## Output

```markdown
## Verification Gate
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## UAT Matrix
| Story/Requirement | Steps | Expected | Actual | Result | Evidence | Owner | Signoff |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Objective Checks
| Check | Command | Result | Evidence |
| --- | --- | --- | --- |

## Mutual Signoff
Required: yes|no
Agent signoff: yes|no
User signoff: yes|no|pending
Reason:

## Failures To Close
| Failure | Severity | Owner | Recheck |
| --- | --- | --- | --- |

## Tooling Used
HTML packet:
Objective commands:
Skipped tools and why:
```

## Progression Rule

Do not progress a phase with failed must-pass stories unless the user explicitly accepts the risk and the failure is recorded as deferred with owner and recheck.
