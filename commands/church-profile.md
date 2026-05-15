---
name: church-profile
description: Capture consented profile signals for workflow personalization while keeping interpretation agent-led and auditable.
---

# church:profile

Use for GSD profile-user parity when personalization, collaboration preferences, or operator patterns should inform future workflow routing.

## Progressive Loading

1. `church`
2. `church-harden` only when profile claims affect high-impact decisions

Agents:

- `church-profile-counselor`
- `church-doctrine-auditor` when profile use affects product doctrine

## CLI Pattern

```bash
church profile init --root <repo> --subject user --purpose "workflow personalization" --consent
church profile set communication.preference concise --root <repo> "true"
church profile check --root <repo> --format json
church profile export --root <repo> --format markdown
```

## Gate

`Profile Gate` may pass only when:

- consent is explicit,
- profile signals are used as routing hints, not facts about product quality,
- material personalization assumptions can be corrected or removed,
- no behavioral inference is made without user-visible evidence.

## Output

```markdown
## Profile Verdict
Outcome:
Consent:
Reasoning-heavy: yes

## Signals
| Signal | Evidence | Use | Risk |
| --- | --- | --- | --- |
```
