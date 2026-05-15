# Agents

Specialist profiles are lazy-loaded by commands when their evidence or review is needed. They are contracts, not always-on context.

## When To Use Specialists

Use a specialist when the active gate needs focused judgment:

- moat or market clarity,
- Bible synthesis or doctrine audit,
- brownfield implementation mapping,
- phase anchor or spec quality,
- gap closure,
- UAT,
- ship readiness,
- security, UI, AI eval, or debugging review.

## Specialist Map

| Area | Agents |
| --- | --- |
| Bible and doctrine | [church-bible-scribe](../agents/church-bible-scribe.md), [church-doc-scribe](../agents/church-doc-scribe.md), [church-doctrine-auditor](../agents/church-doctrine-auditor.md) |
| Moat and strategy | [church-moat-scout](../agents/church-moat-scout.md) |
| Codebase and runtime | [church-codebase-cartographer](../agents/church-codebase-cartographer.md), [church-code-examiner](../agents/church-code-examiner.md), [church-runtime-guardian](../agents/church-runtime-guardian.md) |
| Planning and specs | [church-anchor-architect](../agents/church-anchor-architect.md), [church-spec-canonist](../agents/church-spec-canonist.md), [church-gap-steward](../agents/church-gap-steward.md) |
| Workstreams and handoff | [church-workstream-deacon](../agents/church-workstream-deacon.md), [church-workspace-steward](../agents/church-workspace-steward.md), [church-thread-steward](../agents/church-thread-steward.md) |
| Verification and ship | [church-uat-fellow](../agents/church-uat-fellow.md), [church-ship-steward](../agents/church-ship-steward.md) |
| Specialized review | [church-security-examiner](../agents/church-security-examiner.md), [church-ui-examiner](../agents/church-ui-examiner.md), [church-ai-eval-planner](../agents/church-ai-eval-planner.md), [church-debug-examiner](../agents/church-debug-examiner.md) |
| Operations | [church-git-steward](../agents/church-git-steward.md), [church-triage-steward](../agents/church-triage-steward.md), [church-archive-steward](../agents/church-archive-steward.md), [church-profile-counselor](../agents/church-profile-counselor.md), [church-sketch-curator](../agents/church-sketch-curator.md) |

## Quality Bar

Every profile should state:

- required inputs,
- work it performs,
- output shape,
- quality bar.

The package tests enforce these sections for every agent profile.

## Related Docs

- [Commands](commands.md)
- [Skills](skills.md)
- [Stage Command Map](../skills/church/references/stage-command-map.md)
