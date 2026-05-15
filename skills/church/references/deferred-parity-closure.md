# Deferred Parity Closure

Generated: 2026-05-14

This reference records the corrective pass that converted the previously deferred GSD parity rows into concrete Repo Church assets. The governing rule is semantic parity first, with automation bounded by evidence, consent, and review gates.

## Closure Matrix

| GSD capability family | Repo Church command | CLI command group | Specialist profile | Automation stance |
| --- | --- | --- | --- | --- |
| Runtime hooks and proactive guardrails | `church:guard` | `church hooks plan/check/scaffold` | `church-runtime-guardian` | CLI detects runtime signals, renders hook plans, and creates portable scaffold artifacts. Runtime-specific installation stays review-gated. |
| Workspace lifecycle | `church:workspace` | `church workspace list/create/status/switch/complete` | `church-workspace-steward` | CLI owns workspace registry and active workspace state. Agents judge partitioning, ownership, and integration risk. |
| Thread continuation | `church:thread` | `church thread list/create/status/resume/complete` | `church-thread-steward` | CLI stores continuation metadata and resume hints. Agents must reload current context before trusting stale thread state. |
| Inbox and backlog triage | `church:inbox` | `church inbox add/list/check` | `church-triage-steward` | CLI captures items and blocker counts. Agents decide priority, doctrine impact, and scope admission. |
| Behavioral profile signals | `church:profile` | `church profile init/set/export/check` | `church-profile-counselor` | CLI enforces consent and stores signals. Interpretation remains reasoning-led and ethically bounded. |
| Creative sketch/design exploration | `church:sketch` | `church sketch register/list/check` | `church-sketch-curator` | CLI records artifacts and signoff requirements. Creative direction and design acceptance remain agent/user-led. |
| PR branch filtering and review scope | `church:branch` | `church branch plan` | `church-git-steward` | CLI inspects git state and emits a dry-run plan. Branch mutation requires explicit review. |
| Guarded undo and rollback | `church:rewind` | `church undo plan` | `church-git-steward` | CLI renders rollback options and risk warnings. Destructive commands are never auto-executed. |
| Cleanup and archive planning | `church:archive` | `church archive plan` | `church-archive-steward` | CLI inventories candidate artifacts and emits a dry-run archive plan. Evidence movement/deletion remains review-gated. |

## Reasoning-Heavy Items

The remaining reasoning-heavy workflows are not omitted; they are implemented as command/profile assets with deterministic preflight support:

| Workflow | Why reasoning remains necessary | CLI-owned surface | Required human/agent judgment |
| --- | --- | --- | --- |
| `church:profile` | Behavioral signals can be sensitive, stale, or overfit to a narrow sample. | Consent flag, profile artifact, signal updates, export/check. | Whether signals are valid, useful, ethical, and appropriate for routing decisions. |
| `church:sketch` | Creative artifacts require subjective design judgment and project-doctrine fit. | Artifact registry, summary, source path, signoff blocker state. | Whether the design direction should influence specs, UI doctrine, or UAT. |
| `church:guard` | Runtime hooks can enforce useful guardrails but may disrupt agent portability or local developer flow. | Runtime detection, hook plan, scaffold artifact, portable fallback commands. | Which runtime adapters to enable and what failure modes require mitigation. |
| `church:branch` / `church:rewind` / `church:archive` | Git and cleanup operations can be destructive or externally visible. | Dry-run plans, current git evidence, command suggestions, risk warnings. | Whether to execute the plan, narrow scope, or ask for explicit user confirmation. |

## Parity Test Contract

This closure is guarded by tests that require:

- all command files to exist with frontmatter, staged labels, CLI references, and output sections,
- all specialist profiles to exist with required input, work, output, and quality-bar sections,
- operational stage labels to appear in `stage-command-map.md`,
- counterpart closure docs to include the converted GSD capability families,
- CLI E2E coverage for the new command groups and safety gates,
- stale backlog and scope-downgrade classifications to stay out of the final comparison and closure references.
