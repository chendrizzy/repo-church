---
name: church-guard
description: Plan, check, and scaffold runtime hook coverage with agent-agnostic fallbacks and explicit review gates.
---

# church:guard

Use for hook-like workflow enforcement: pre-progress checks, pre-ship checks, context freshness, ledger blockers, or runtime adapter planning.

## Progressive Loading

1. `church`
2. `church-gap-closure` only if hook checks expose blockers

Agents:

- `church-runtime-guardian`
- `church-gap-steward` when fallback checks fail

## CLI Pattern

```bash
church hooks plan --root <repo> --runtime auto --event pre-progress --format json
church hooks check --root <repo> --runtime auto --event pre-progress --format json
church hooks scaffold --root <repo> --runtime auto --event pre-progress --format json
```

## Gate

`Guard Gate` passes when:

- runtime-specific hooks are represented as reviewed adapter plans,
- portable fallback commands exist for unsupported runtimes,
- destructive or externally visible hook behavior requires explicit review,
- hook failures become gap/risk ledger items instead of silent bypasses.

## Output

```markdown
## Guard Verdict
Outcome:
Runtime:
Fallback available: yes|no

## Hook Plan
| Event | Runtime | Adapter status | Fallback |
| --- | --- | --- | --- |
```
