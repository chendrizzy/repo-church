# Parallelism Guide

Repo Church should reduce lifecycle runtime without reducing rigor.

## Safe Parallelism

Run in parallel when streams have separate evidence sources or separate write surfaces:

- market research vs codebase mapping,
- architecture audit vs UI doctrine audit,
- assumption validation vs test inventory,
- implementation of disjoint modules,
- UAT script drafting vs objective test execution,
- release notes vs rollback documentation.

## Unsafe Parallelism

Do not parallelize when one stream depends on the output of another:

- deep planning before assumption hardening,
- specs before parent phase anchor approval,
- implementation before spec gate,
- user signoff before agent verification evidence exists,
- merge readiness before UAT blockers are classified.

## Token Reduction Rules

- Prefer inventory scripts and indexes before loading large docs.
- Read only files needed for the current gate.
- Use evidence tables with paths and line numbers instead of pasting long excerpts.
- Reuse prior ledgers if the file hash/date/context remains valid.
- Close or supersede stale gaps instead of carrying duplicate entries.
- Keep child skills self-contained but point to the umbrella lifecycle for deeper context.

## Parallel Work Map

```markdown
| Stream | Type | Owner | Inputs | Output | Can start now? | Blocked by |
| --- | --- | --- | --- | --- | --- | --- |
```

## Critical Path Rule

The active agent should keep the blocker on the critical path local. Delegate or parallelize sidecar work that does not block the immediate next decision.
