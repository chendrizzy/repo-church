---
name: church-optimizer
description: Optimize Repo Church or GSD-like lifecycle workflows for less redundancy, lower token use, and safer parallelism. Use when the user asks to reduce workflow time, reduce token consumption, improve phase parallelism, simplify gates, or tune lifecycle efficiency without weakening reliability.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church Workflow Optimizer

Use this skill to tune a lifecycle without lowering gate quality.

## Inputs

- Current lifecycle steps.
- Recent handoffs, plans, audits, and UAT outputs.
- Pain points: repeated reads, confusing flags, slow steps, duplicate artifacts, or missed gaps.

## Procedure

1. Inspect current automation map: `church registry list --format json`.
2. Load current context: `church context load --root <repo> --format markdown --include-history`.
3. Map each lifecycle step to its unique decision value.
4. Replace repeated broad reading with CLI reports where possible: inventory, validate, sources, claim-scan, context load, ledgers, handoff.
5. Replace dense markdown-only review with HTML workbench or rendered packet review when a human must inspect many criteria.
6. Identify duplicate artifact reads and redundant summaries.
7. Separate critical-path decisions from sidecar research or verification.
8. Recommend parallel streams only where dependencies allow.
9. Rename confusing flags or states using Repo Church vocabulary.
10. Preserve any step that catches high-severity failure modes.

## Output

```markdown
## Optimization Verdict
Outcome: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:

## Redundancy Map
| Step | Duplicates | Keep/merge/remove | Rationale |
| --- | --- | --- | --- |

## Parallelism Plan
| Stream | Starts after | Output | Risk |
| --- | --- | --- | --- |

## Naming Cleanup
| Current term | Proposed term | Why |
| --- | --- | --- |

## Reliability Guardrails
| Guardrail | Failure mode prevented |
| --- | --- |

## Tooling Substitutions
| Current manual step | CLI/HTML substitute | Reliability impact | Token/time impact |
| --- | --- | --- | --- |
```

## Rule

Do not remove a workflow step solely because it is slow. Remove or merge it only when another step already produces equivalent evidence with equal or better reliability.
