---
name: church-thread
description: Manage portable thread and continuation records with handoff links, runtime identifiers, and resume hints.
---

# church:thread

Use for persistent thread bookkeeping, continuation records, or context handoff routing across agent sessions.

## Progressive Loading

1. `church`
2. `church-handoff`

Agents:

- `church-thread-steward`
- `church-doc-scribe` when a durable handoff needs writing

## CLI Pattern

```bash
church thread create <name> --root <repo> --runtime codex --summary "..." --handoff .church/handoff.md
church thread list --root <repo> --format json
church thread status <name> --root <repo> --format json
church thread resume <name> --root <repo> --format markdown
church thread complete <name> --root <repo>
```

## Gate

`Thread Gate` passes when:

- continuation records include runtime, summary, and handoff evidence,
- resume hints use deterministic context loading,
- stale thread context is not treated as current without revalidation.

## Output

Every output must include the common gate record fields from `skills/church/references/gate-taxonomy.md`: evidence, failed criteria, risk owner, required next action, recheck command or artifact, and agent/user signoff status. Keep stage-specific sections below that record.

```markdown
## Thread Verdict
Outcome:
Active thread:
Resume command:

## Continuation Records
| Name | Runtime | Status | Handoff |
| --- | --- | --- | --- |
```
