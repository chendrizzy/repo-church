# Repo Church Stage Command Map

Repo Church uses themed but practical command names. The names should help humans remember the lifecycle without obscuring the engineering function.

## Core Loop

| Order | Command | Primary purpose | GSD counterpart | Main skill(s) | Specialist agents |
| --- | --- | --- | --- | --- | --- |
| 1 | `church:gather` | Init/resume, context load, moat/Bible inventory, next route | `gsd-new-project`, `gsd-progress`, `gsd-resume-work` | `church`, `church-intake`, `church-moat`, `repo-bible` | `church-moat-scout`, `church-bible-scribe`, `church-anchor-architect` |
| 2 | `church:discern` | Assumption hardening, source checks, ambiguity closure | `gsd-discuss-phase`, `gsd-spike`, `gsd-import` | `church-harden`, `church-gap-closure` | `church-moat-scout`, `church-doctrine-auditor`, `church-gap-steward` |
| 3 | `church:canonize` | Parent anchor, spec gate, traceability, specialist review routing | `gsd-plan-phase`, `gsd-spec-phase`, `gsd-review` | `church-anchor`, `church-spec-gate` | `church-anchor-architect`, `church-spec-canonist`, `church-doctrine-auditor` |
| 4 | `church:commission` | Execution handoff, safe parallelism, validation/rollback path | `gsd-execute-phase`, `gsd-pause-work`, `gsd-workstreams` | `church-handoff` | `church-workstream-deacon`, `church-gap-steward` |
| 5 | `church:fellowship` | Peer review, collaborative UAT, mutual signoff | `gsd-verify-work`, `gsd-audit-uat`, `gsd-validate-phase` | `church-uat`, `church-gap-closure` | `church-uat-fellow`, `church-code-examiner`, domain examiners |
| 6 | `church:bless` | Ship/merge gate, release risk, rollback, Bible drift | `gsd-ship`, `gsd-complete-milestone` | `church-ship` | `church-ship-steward`, `church-doctrine-auditor` |
| 7 | `church:renew` | Bible refresh, learnings, next cycle setup | `gsd-docs-update`, `gsd-extract-learnings`, `gsd-new-milestone` | `repo-bible`, `church-anchor`, `church-moat` | `church-bible-scribe`, `church-doc-scribe`, `church-moat-scout` |

## Canonical Lifecycle Terms

Use this table when recording state. Do not invent alternate stage, gate, or workflow names in handoffs or gate records.

| Human command | Reference stage | CLI workflow key | Gate | Required artifact(s) | Allowed next CLI keys |
| --- | --- | --- | --- | --- | --- |
| `church:gather` | Bible Intake / Project Init | `init` | `intake` | `state`, `moat_json`, `moat_md` | `moat`, `bible`, `survey` |
| `church:gather` / `church-moat` | Moat Definition | `moat` | `moat` | `moat_json`, `moat_md` | `bible`, `survey`, `harden`, `anchor` |
| `repo-bible` | Bible Generation | `bible` | `bible` | `bible_packet` | `survey`, `harden`, `anchor` |
| `church:survey` | Codebase Survey | `survey` | `survey` | `bible_inventory` | `harden`, `anchor`, `gap-closure` |
| `church:discern` | Research Hardening | `harden` | `evidence` | `assumption_ledger` | `anchor`, `gap-closure` |
| `church:canonize` | Phase Anchoring | `anchor` | `anchor` | `phase_anchor` | `spec-gate`, `gap-closure` |
| `church:canonize` | Spec Gate | `spec-gate` | `spec` | `spec_gate` | `gap-closure`, `handoff` |
| `church:confess` / `church:atonement` | Gap Closure | `gap-closure` | `closure` | `gap_ledger` | `spec-gate`, `handoff` |
| `church:commission` | Execution Handoff | `handoff` | `handoff` | `handoff` | `uat` |
| `church:fellowship` | Collaborative UAT | `uat` | `verification` | `uat_ledger` | `ship`, `gap-closure` |
| `church:bless` | Ship Gate | `ship` | `ship` | `ship_gate` | `refresh` |
| `church:renew` | Bible Refresh | `refresh` | `refresh` | `refresh_record` | `moat`, `anchor`, `init` |

## Operational Shortcuts

| Command | Primary purpose | GSD counterpart | Guardrail |
| --- | --- | --- | --- |
| `church:survey` | Brownfield codebase, architecture, interface, and graph/map evidence survey | `gsd-map-codebase`, `gsd-graphify`, `gsd-codebase-mapper`, `gsd-pattern-mapper`, `gsd-integration-checker` | Inventory is evidence only; architecture judgment stays agentic. |
| `church:guard` | Runtime hook planning, check scaffolds, and portable fallbacks | Runtime hooks, GSD health/progress guardrails | Hooks must have fallback commands and explicit review before install. |
| `church:workspace` | Workspace CRUD and active workspace state | `gsd-workspace`, `gsd-workstreams` | Workspaces cannot bypass lifecycle gates or integration checkpoints. |
| `church:thread` | Thread continuation records and resume hints | `gsd-thread`, `gsd-resume-work`, `gsd-pause-work` | Saved thread context must be refreshed before use. |
| `church:inbox` | Inbox/backlog capture and triage | `gsd-inbox`, `gsd-review-backlog`, `gsd-capture` | Triage is not approval; scope changes must pass gates. |
| `church:profile` | Consented personalization profile artifacts | `gsd-profile-user` | Behavioral signals require explicit consent and reversibility. |
| `church:sketch` | Creative/design artifact registration and signoff routing | `gsd-sketch`, UI planning/review agents | Sketches inform decisions; they do not approve design alone. |
| `church:branch` | PR-safe branch planning and review-scope isolation | `gsd-pr-branch` | Generates reviewable plans; execution requires explicit review. |
| `church:rewind` | Undo, restore, and rollback planning | `gsd-undo` | Destructive commands require current status evidence and review. |
| `church:archive` | Cleanup/archive dry-run planning | `gsd-cleanup` | Never delete lifecycle evidence by default. |
| `church:confess` | Capture ad hoc gaps, risks, requirements, or phase ideas | `gsd-capture`, `gsd-phase`, `gsd-review-backlog` | Must write to ledger; does not silently mutate scope. |
| `church:atonement` | Debug, diagnose, remediate, and recheck failures | `gsd-debug`, `gsd-forensics`, `gsd-audit-fix` | Requires evidence-backed root cause or explicit unknown. |
| `church:quick-rite` | Small low-risk tasks without full cycle overhead | `gsd-fast`, `gsd-quick` | Forbidden for strategy, security, architecture, UX, or phase-scope changes. |
| `church:council` | Command center/status view | `gsd-manager`, `gsd-health`, `gsd-stats` | CLI-first status; agent only interprets tradeoffs. |

## Specialist Dispatch Thresholds

Dispatch the specialist when the signal is present; record non-applicability when skipping.

| Signal | Required specialist | Skip only when |
| --- | --- | --- |
| User-facing UI, visual design, interaction states, or screenshots changed | `church-ui-examiner` | The change is text-only and has no layout or workflow impact. |
| Auth, data access, privacy, compliance, payments, destructive migrations, or secrets touched | `church-security-examiner` | A cited diff proves no sensitive surface changed. |
| AI behavior, evals, prompts, model routing, embeddings, or generated output quality changed | `church-ai-eval-planner` | The phase has no AI-facing behavior. |
| Brownfield architecture is unfamiliar or affects interfaces/data flow | `church-codebase-cartographer` | Current maps and file evidence are fresh enough for the decision. |
| Market, competitor, platform, pricing, or policy claims affect planning | `church-moat-scout` | Claims are already current-source-backed with dates. |
| Spec ambiguity could produce divergent implementations | `church-spec-canonist` | Acceptance criteria, files, tests, edge cases, and rollback are already explicit. |
| Release readiness or rollback is being judged | `church-ship-steward` | The change is documentation-only and no lifecycle state advances. |

## Naming Standard

- Use church/Bible terms only when they improve recall.
- Pair every themed name with a practical description.
- Avoid joke names for safety-critical workflows.
- Do not hide severity, blockers, or user-signoff requirements behind metaphor.
