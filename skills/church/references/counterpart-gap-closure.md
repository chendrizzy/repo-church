# Counterpart Gap Closure

This note consolidates the negative GSD-to-Church deltas that were identified during framework comparison and records how the current package resolves them.

## Closed Gaps

| Gap | Prior church weakness | Resolution | Measurable improvement |
| --- | --- | --- | --- |
| Stage-contained command layer | Repo Church had invocable skills and CLI mechanics, but no plugin-root staged slash-command workflows comparable to GSD's command entrypoints. | Added `commands/` with seven core lifecycle stages and fourteen operational shortcuts. Each command names progressive skill loading, CLI preflight, gate criteria, specialist agents, and output shape. | Package validator and asset tests must find all expected command files, matching frontmatter, staged labels, CLI references, and required sections. |
| Lazy-loaded specialist profiles | GSD had specialized agents for review, planning, execution, UI, security, evals, debugging, runtime operations, git hygiene, and artifact stewardship; Repo Church relied mostly on skill prose. | Added `agents/` profiles for moat, Bible, survey, runtime guardrails, workspace/thread stewardship, triage, profile/sketch interpretation, git/archive planning, anchor, spec, doctrine, gap, workstream, UAT, ship, code, security, UI, AI eval, debug, and docs work. | Asset tests require all expected profiles, matching frontmatter, required sections, and at least one staged-command or reference mention. |
| Requirements and spec stringency | Early Repo Church gates were stricter than ad hoc prompting but not explicitly stage-command enforced. | `church:canonize` adds a quantified Canon Gate: full requirement traceability, zero critical/high blockers, acceptance proof paths, scope completeness, and specialist review routing. | Canon command content must retain quantified traceability and blocker rules. Spec-gate skills continue to record gaps through the CLI ledger. |
| Collaborative UAT and mutual signoff | UAT existed as a skill, but the command layer did not force a peer-review and user-signoff pass before ship. | `church:fellowship` adds the collaborative verification stage with UAT rows, objective evidence, agent signoff, and user signoff when mutual approval is required. | Fellowship command and verification protocol require UAT ledger records plus `signoff.agent` and conditional `signoff.user` state keys. |
| Bible leverage between phases | Bible validation and HTML tooling existed, but stage transitions did not consistently require Bible drift checks. | Gather, Canonize, Fellowship, Bless, and Renew commands call `church bible inventory`, `validate`, `render-html`, or source checks before progression. | Command tests require deterministic `church` CLI references; validator catches missing command assets. |
| Brownfield codebase mapping | GSD has dedicated mapper/graphify agents; Repo Church initially relied on Bible inventory without an explicit stage/profile for implementation reality. | Added `church:survey` and `church-codebase-cartographer` to map modules, interfaces, data flows, tests, graph/map evidence, and Bible drift before planning. | Asset tests require the survey command/profile and ensure unresolved `future` placeholders do not remain in the GSD workflow assessment. |
| Runtime hooks | Runtime-specific hooks previously lacked concrete package assets. | Added `church:guard`, `church-runtime-guardian`, and `church hooks plan/check/scaffold` so hooks are planned through portable fallback commands before runtime adapters. | CLI E2E covers hook plan/check/scaffold and asset tests require the command/profile. |
| Workspace and thread records | Workspace/thread CRUD was previously deferred as runtime-specific. | Added `church:workspace`, `church:thread`, `church-workspace-steward`, `church-thread-steward`, and CLI registries for workspaces/threads. | CLI E2E covers create/list/status/switch/resume/complete flows. |
| Inbox and backlog triage | Inbox/backlog coverage was collapsed into generic gap capture. | Added `church:inbox`, `church-triage-steward`, and `church inbox add/list/check`. | Inbox blockers are deterministically counted while scope approval remains gated. |
| Git branch and rollback planning | PR branch filtering and undo were deferred because they can be destructive. | Added `church:branch`, `church:rewind`, `church-git-steward`, and CLI dry-run planning commands for branch and rollback workflows. | Commands inspect git state and output reviewed command plans without mutating state. |
| Archive cleanup | Cleanup/archive previously lacked concrete package assets. | Added `church:archive`, `church-archive-steward`, and `church archive plan` for non-destructive archive planning. | Archive planning remains dry-run and preserves lifecycle evidence. |
| Profile and sketch artifacts | Behavioral profiling and creative sketching previously lacked concrete package assets. | Added `church:profile`, `church:sketch`, `church-profile-counselor`, `church-sketch-curator`, and CLI artifact registries with consent/signoff gates. | Profile check blocks without consent; sketch check holds on unresolved user-signoff items. |
| Agentic reasoning boundary | Some GSD processes are useful because they remain judgment-heavy; over-automating them would reduce quality. | Stage commands use CLI preflight for deterministic state and evidence, then route judgment to named specialists. `gsd-workflow-assessment.md` remains the automation boundary source. | Commands explicitly separate CLI preflight from agent outputs; specialist profiles require `Quality Bar` sections. |
| Naming clarity | GSD command names are direct but numerous; Repo Church needed a memorable theme without hiding engineering semantics. | Added practical church/Bible-themed labels: gather, discern, canonize, commission, fellowship, bless, renew, confess, atonement, quick-rite, council. | Stage map requires every themed command to pair with primary purpose, GSD counterpart, skills, and agents. |
| Gap closure accountability | Prior gap closure relied on the user or agent remembering to translate findings into trackable work. | Commands and specialist profiles route contradictions, blockers, failed UAT rows, and unresolved risks into `church ledger add/check` workflows. | Gap-steward profile and command preflights require ledger checks at planning, execution, UAT, and ship gates. |

## Safety Boundaries

- Repo Church preserves semantic parity with the GSD workflow surface. It may group related GSD assets under a smaller command family only when the counterpart remains traceable in the stage map, comparison artifact, CLI, and tests.
- Repo Church does not automate strategy, architecture, security, UX, launch, or acceptance decisions. It automates the evidence and state surfaces that make those decisions more reliable.
- Repo Church does not install runtime-specific hooks automatically. Hook assets produce reviewed plans, portable fallbacks, and scaffold files that package consumers can adapt to their runtime.

## Current Quality Bar

Before publishing or using Repo Church as a canonical workflow package:

1. `validate-package.sh` must pass with zero errors and zero warnings.
2. CLI E2E tests must pass across init, registry, state, moat, lifecycle, ledger, context, and Bible delegation.
3. Plugin asset tests must pass for command/profile completeness, naming, stage mapping, and manifest wiring.
4. Any later GSD-equivalent asset marked as missing must get a Repo Church command/profile/skill counterpart unless the user explicitly approves exclusion.
