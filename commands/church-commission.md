---
name: church-commission
description: Commission implementation work with frozen scope, execution handoff, workstream map, validation commands, and rollback notes.
---

# church:commission

Use this after `church:canonize` and before implementation execution. It creates the execution handoff and workstream split.

## Progressive Loading

1. `church`
2. `church-handoff`
3. `church-gap-closure` only if blockers are open

Agents:

- `church-workstream-deacon` for parallelization boundaries
- `church-code-examiner` only if implementation risk is already visible
- `church-gap-steward` when open blockers remain

## CLI Preflight

```bash
church context load --root <repo> --format markdown --include-history
church ledger check gaps --root <repo> --allow-open --format json
church lifecycle status --root <repo> --format json
church registry reasoning handoff --format markdown
```

## Gate

`Commission Gate` may pass only when:

- scope and non-goals are frozen,
- first three moves are unambiguous,
- safe parallel streams are separated from critical-path work,
- validation and rollback commands are named,
- unresolved blockers have owner, severity, and deferral rationale.

Render and register:

```bash
church lifecycle handoff --root <repo> --output <path> --format markdown
church lifecycle advance handoff --root <repo> --outcome PASS|PASS_WITH_RISK|HOLD --artifact handoff=<path>
```

## Output

```markdown
## Commission Verdict
Outcome:

## Workstreams
| Stream | Owner | Start condition | Validation |
| --- | --- | --- | --- |

## Frozen Handoff
Path:
Open risks:
```
