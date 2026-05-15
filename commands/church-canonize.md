---
name: church-canonize
description: Canonize a phase: tighten parent anchors, spec gates, requirement traceability, Bible alignment, and measurable acceptance before implementation.
---

# church:canonize

Use this for the strict planning/spec gate. This is the church counterpart to phase planning, spec clarification, plan review, and convergence loops.

## Progressive Loading

1. `church`
2. `church-anchor`
3. `church-spec-gate`
4. `church-gap-closure` only for blockers
5. Domain skill only when needed: `church-moat`, `repo-bible`, UI/AI/security agents

Agents:

- `church-anchor-architect`
- `church-doctrine-auditor`
- `church-spec-canonist`
- `church-codebase-cartographer` when implementation reality is unclear
- `church-ai-eval-planner` when AI behavior is involved
- `church-ui-examiner` when user-facing UI is involved
- `church-security-examiner` when auth/data/security is touched

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church lifecycle show anchor --format markdown
church lifecycle show spec-gate --format markdown
church ledger check assumptions --root <repo> --allow-open --format json
church bible validate --root <repo> --follow-local-md --format json --output -
church registry reasoning spec-gate --format markdown
```

## Quantified Gate

`Canon Gate` may pass only when:

- 100% of in-scope requirements trace to Bible IDs or approved doctrine-change requests,
- 0 critical or high open assumption/gap blockers,
- every acceptance criterion has a test, UAT row, or explicit user-signoff path,
- phase scope includes objective, non-goals, dependencies, interfaces, risks, rollback, observability, and validation,
- brownfield plans account for current implementation interfaces and drift,
- AI/UI/security phases have the matching specialist review or a recorded non-applicability rationale.

Record:

```bash
church lifecycle advance anchor --root <repo> --outcome PASS|HOLD|BLOCK --phase "<phase>"
church lifecycle advance spec-gate --root <repo> --outcome PASS|HOLD|BLOCK --artifact spec_gate=<path>
```

## Output

```markdown
## Canon Verdict
Outcome:
Phase:
Spec approved: yes|no

## Traceability Matrix
| Requirement | Spec section | Acceptance proof | Bible source |
| --- | --- | --- | --- |

## Blocking Defects
| ID | Severity | Fix | Owner | Recheck |
| --- | --- | --- | --- | --- |
```
