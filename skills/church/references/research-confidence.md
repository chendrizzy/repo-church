# Research Confidence Protocol

Repo Church assumes that vague confidence creates bad plans. Classify claims before planning.

## Confidence Labels

| Label | Definition | Planning Use |
| --- | --- | --- |
| `verified-local` | Proven by current repo files, tests, logs, screenshots, or generated artifacts. | Safe for implementation planning. |
| `verified-current` | Supported by current primary external sources. | Safe if cited and date-sensitive. |
| `supported-secondary` | Supported by reputable secondary analysis, but not primary. | Usable with risk note. |
| `user-intent` | Stated by the user as desired direction. | Treat as product intent, not market proof. |
| `hypothesis` | Plausible but not proven. | Requires validation task before high-cost work. |
| `stale` | Previously true but plausibly outdated. | Refresh before planning. |
| `contradicted` | Conflicts with current evidence. | Blocks until resolved. |

## Minimum Research Requirements

Research is required when a claim is about:

- current competitors, pricing, features, roadmap, or acquisition channels,
- platform policies, APIs, standards, SDKs, or agent runtime behavior,
- market demand, buyer willingness, or GTM channels,
- infrastructure costs or scalability,
- security, privacy, legal, or compliance requirements,
- any assumption that would change phase order if false.

## Evidence Quality Order

1. Current primary source, official docs, code, or API output.
2. Current local repo evidence.
3. Current direct product observation.
4. Reputable secondary source.
5. User statement.
6. Model inference.

Use model inference only as a hypothesis.

## Assumption Ledger

Use `confidence` for evidence strength and `status` for workflow state. For example, a claim can be `confidence=hypothesis` and `status=open`; do not store `hypothesis` as the only status because closure checks need both dimensions.

```markdown
| ID | Claim | Confidence | Evidence | Impact if wrong | Required validation | Status | Owner | Recheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## Acceptance Threshold

High-impact assumptions must be `verified-local`, `verified-current`, or explicitly deferred with owner and mitigation. A high-impact `hypothesis`, `stale`, or `contradicted` claim should produce `HOLD` or `BLOCK`.
