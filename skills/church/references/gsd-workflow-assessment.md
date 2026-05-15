# GSD Workflow Automation Assessment

This assessment maps the local GSD workflow library into Repo Church automation boundaries. The goal is not to clone GSD. It is to preserve the gated phase-chaining strengths while moving deterministic state, routing, ledgers, handoffs, and artifact checks into `church`.

## Decision Questionnaire

Use these true/false questions before deciding whether a workflow belongs in the CLI, the agent, or both.

### Automation-Positive Questions

If most answers are true, automate the workflow or the relevant sub-steps:

1. Is the input schema known before runtime?
2. Can every required input be provided by flags, stdin, existing files, or state keys?
3. Is the output mostly structured data, an artifact path, a report, or a gate status?
4. Can success/failure be determined with deterministic checks?
5. Is the operation idempotent or safely repeatable?
6. Would two competent agents produce the same result if given the same files?
7. Is the workflow mostly state lookup, state mutation, indexing, counting, validating, rendering, or routing?
8. Can failures be reported with an actionable command example?
9. Would automation reduce token use or context loss without hiding important uncertainty?
10. Can destructive or progression-changing behavior be protected by `--dry-run`, `--force`, `--yes`, or explicit gate outcomes?

### Reasoning-Required Questions

If any of these are true, keep the workflow agent-led or user-led, while using the CLI for supporting mechanics:

1. Does the workflow require market, product, architecture, UX, security, or release judgment?
2. Is the best answer sensitive to ambiguous user intent or subjective quality?
3. Would a shallow template produce plausible but low-quality output?
4. Does the workflow create or approve strategy, requirements, phase scope, specs, UX, security posture, or launch risk?
5. Does the workflow require forming and testing hypotheses?
6. Does it need current external research or source credibility assessment?
7. Does it require comparing conflicting evidence and deciding precedence?
8. Does it require user acceptance, mutual signoff, or business risk acceptance?
9. Could automation make the result look more certain than the evidence supports?
10. Would two competent agents reasonably disagree on the best answer?

### Classification

| Result | Rule |
| --- | --- |
| **Automate** | Automation-positive mostly true, reasoning-required all false or low-impact. |
| **Hybrid** | Mechanics are deterministic, but outcome quality depends on interpretation. CLI stores/checks; agent decides. |
| **Reasoning-led** | Any high-impact reasoning-required question is true. CLI only loads context, tracks ledgers, and records gates. |
| **Do not automate** | Automation would hide uncertainty, fabricate confidence, bypass user signoff, or degrade quality. |

### Default Bias

When uncertain, automate evidence collection and state handling, not the decision itself.

## GSD Workflow Map

| GSD workflow | Repo Church target | Automation stance | Reasoning boundary |
| --- | --- | --- | --- |
| `gsd-add-tests` | `ledger uat`, `lifecycle advance uat` | Hybrid | CLI stores UAT/test obligations; agent designs meaningful tests. |
| `gsd-ai-integration-phase` | `lifecycle advance anchor/spec-gate`, `ledger gaps` | Reasoning-led | Agent must design AI evals, failure modes, and guardrails; CLI records gates. |
| `gsd-audit-fix` | `ledger gaps`, `lifecycle handoff` | Hybrid | CLI tracks findings; agent decides fixes and validates behavior. |
| `gsd-audit-milestone` | `lifecycle status`, `context load`, `ledger check` | Hybrid | CLI checks state; agent judges original intent vs delivered value. |
| `gsd-audit-uat` | `ledger check uat/gaps` | Automate more | CLI should surface outstanding UAT; agent judges severity and user acceptance. |
| `gsd-autonomous` | `registry list`, `lifecycle advance`, `context load` | Hybrid | CLI can chain gates; agent must make each gate decision. |
| `gsd-capture` | `ledger add`, `state set` | Automate more | CLI stores captured items; agent classifies ambiguous ideas. |
| `gsd-cleanup` | `church:archive`, `church archive plan` | Automate more | Archive hygiene is deterministic; Repo Church keeps it dry-run and review-gated to preserve evidence. |
| `gsd-code-review` | `ledger gaps`, `lifecycle advance spec-gate/ship` | Reasoning-led | Review findings require code judgment. CLI records and gates. |
| `gsd-complete-milestone` | `lifecycle advance refresh`, `context load` | Hybrid | CLI can archive state; agent verifies milestone intent. |
| `gsd-config` | `state get/set`, `registry keys` | Automate more | Deterministic config belongs in CLI. |
| `gsd-debug` | `ledger risks/gaps`, `context load` | Reasoning-led | Debug hypotheses need reasoning; CLI preserves trace and state. |
| `gsd-discuss-phase` | `context load`, `moat`, `ledger assumptions` | Reasoning-led | Adaptive questioning and ambiguity reduction should stay agentic. |
| `gsd-docs-update` | `bible validate/render-html`, `ledger gaps` | Hybrid | CLI validates docs; agent writes accurate documentation. |
| `gsd-eval-review` | `ledger gaps/uat`, `lifecycle advance uat` | Reasoning-led | Eval coverage quality requires AI-system judgment. |
| `gsd-execute-phase` | `lifecycle status/advance`, `ledger check`, `handoff` | Hybrid | CLI orchestrates phase state; agent implements and adapts. |
| `gsd-explore` | `moat`, `ledger assumptions` | Reasoning-led | Exploration is intentionally creative and should not be reduced to routing. |
| `gsd-extract-learnings` | `church:renew`, `lifecycle handoff`, `ledger add gaps/risks` when learnings imply follow-up | Hybrid | CLI can capture structured learnings as artifacts/ledger items; agent extracts meaning. |
| `gsd-fast` | direct agent execution plus `state set` if needed | Hybrid | CLI overhead should be optional for trivial tasks. |
| `gsd-forensics` | `context load`, `ledger gaps/risks` | Reasoning-led | Diagnosis needs reasoning; CLI provides evidence snapshot. |
| `gsd-graphify` | `church:survey`, `bible inventory`, optional project-local graph artifacts | Hybrid | Repo Church consumes graph/map evidence when present but does not require a vendor-specific graph builder. |
| `gsd-health` | `registry`, `state show`, `ledger check`, `bible validate` | Automate more | Health checks are deterministic and should be CLI-first. |
| `gsd-help` | `--help`, `registry list` | Automate more | CLI help should be layered and copy-pasteable. |
| `gsd-import` | `bible sources/validate`, `ledger gaps` | Hybrid | CLI detects links/conflicts; agent resolves semantic conflicts. |
| `gsd-inbox` | `church:confess`, `ledger add gaps/risks/assumptions` | Hybrid | CLI stores incoming items in typed ledgers; agent triages priority and alignment. |
| `gsd-ingest-docs` | `bible inventory/scaffold/sources`, `ledger gaps` | Hybrid | CLI ingests structure; agent handles precedence and synthesis. |
| `gsd-manager` | `registry`, `lifecycle`, `state`, `context` | Automate more | Command center mechanics belong in CLI. |
| `gsd-map-codebase` | `church:survey`, `bible inventory`, `church-codebase-cartographer` | Hybrid | CLI inventories; the cartographer maps interfaces, drift, meaning, and risks. |
| `gsd-milestone-summary` | `context load`, `lifecycle handoff` | Hybrid | CLI gathers evidence; agent writes useful summary. |
| `gsd-mvp-phase` | `lifecycle advance anchor/spec-gate` | Reasoning-led | MVP slicing quality depends on product judgment. |
| `gsd-new-milestone` | `lifecycle advance init/moat/anchor` | Hybrid | CLI initializes state; agent chooses milestone goals. |
| `gsd-new-project` | `init`, `moat`, `bible scaffold/intake-html` | Hybrid | CLI scaffolds; agent captures vision and strategy. |
| `gsd-ns-context` | `context load`, `bible inventory`, `church:survey` when architecture graph context matters | Automate more | Namespace routing and context loading should be deterministic. |
| `gsd-ns-ideate` | `moat`, `ledger assumptions` | Reasoning-led | Ideation stays agentic. |
| `gsd-ns-manage` | `church:council`, `church:workspace`, `church:thread`, `state`, `registry`, `lifecycle` | Automate more | Management mechanics belong in CLI; workspace/thread state is portable repo-local data. |
| `gsd-ns-project` | `init`, `lifecycle`, `context` | Hybrid | CLI manages project state; agent judges project direction. |
| `gsd-ns-review` | `ledger gaps/uat/risks` | Hybrid | CLI aggregates reviews; agent judges findings. |
| `gsd-ns-workflow` | `lifecycle`, `context`, `handoff` | Automate more | Workflow state and progression should be CLI-first. |
| `gsd-pause-work` | `lifecycle handoff` | Automate more | Handoff rendering is deterministic; agent adds first moves. |
| `gsd-phase` | `church:confess`, `church:canonize`, `lifecycle advance` | Hybrid | CLI can store phase state; agent edits roadmap semantics through anchor/spec gates. |
| `gsd-plan-phase` | `lifecycle advance anchor/spec-gate`, `ledger assumptions/gaps` | Reasoning-led | Planning quality is harmed by full automation. |
| `gsd-plan-review-convergence` | `ledger gaps`, `lifecycle advance spec-gate` | Reasoning-led | Convergence requires review judgment; CLI tracks open concerns. |
| `gsd-pr-branch` | `church:branch`, `church branch plan` | Automate more | Branch filtering is deterministic but risky; Repo Church outputs a reviewed branch plan instead of mutating git silently. |
| `gsd-profile-user` | `church:profile`, `church profile`, `church-profile-counselor` | Reasoning-led | Behavioral profiling stays interpretive and consent-aware; CLI stores consented signals and blocks unconsented use. |
| `gsd-progress` | `lifecycle status/advance`, `context load` | Automate more | Progress routing should be deterministic with explicit gates. |
| `gsd-quick` | direct agent execution with optional `state set` | Hybrid | Avoid over-process; CLI optional. |
| `gsd-resume-work` | `context load`, `lifecycle handoff` | Automate more | Fresh context loading should be CLI-first. |
| `gsd-review` | `ledger gaps`, `lifecycle advance spec-gate` | Reasoning-led | Peer review content needs judgment; CLI records outcomes. |
| `gsd-review-backlog` | `church:confess`, `ledger add gaps/risks` | Hybrid | CLI stores backlog-like review items in typed ledgers; agent prioritizes. |
| `gsd-secure-phase` | `ledger risks/gaps`, `lifecycle advance ship` | Reasoning-led | Threat mitigation verification requires security judgment. |
| `gsd-settings` | `state get/set`, `registry keys` | Automate more | Settings should be deterministic. |
| `gsd-ship` | `ledger check`, `lifecycle advance ship`, `handoff` | Hybrid | CLI gates; agent judges release risk. |
| `gsd-sketch` | `church:sketch`, `church sketch`, `church-sketch-curator` | Reasoning-led | Design exploration is creative; Repo Church registers artifacts and routes acceptance/signoff through gates. |
| `gsd-spec-phase` | `lifecycle advance spec-gate`, `ledger assumptions` | Reasoning-led | Ambiguity scoring and spec clarity need reasoning. |
| `gsd-spike` | `ledger assumptions/risks`, `context load` | Reasoning-led | Spikes exist to learn; agent interpretation matters. |
| `gsd-stats` | `registry`, `state`, `ledger check`, `bible inventory` | Automate more | Metrics should be CLI-generated. |
| `gsd-thread` | `church:thread`, `church thread`, `context load`, `lifecycle handoff` | Automate more | Persistent thread bookkeeping is repo-local and portable; runtime IDs are optional metadata. |
| `gsd-ui-phase` | `lifecycle advance spec-gate`, `ledger uat/gaps` | Reasoning-led | Design contract quality needs visual/product judgment. |
| `gsd-ui-review` | `ledger gaps/uat`, `lifecycle advance uat` | Reasoning-led | Visual audit scoring needs judgment and screenshots. |
| `gsd-ultraplan-phase` | `lifecycle advance spec-gate`, `ledger gaps` | Hybrid | CLI can import/export plan artifacts; plan critique stays agentic. |
| `gsd-undo` | `church:rewind`, `church undo plan` | Automate more | Git rollback planning is CLI-driven with safeguards; execution remains explicitly reviewed. |
| `gsd-update` | plugin/package version command | Automate more | Version checks and changelog display are deterministic. |
| `gsd-validate-phase` | `ledger check`, `lifecycle advance uat/ship` | Hybrid | CLI finds missing gates; agent validates coverage quality. |
| `gsd-verify-work` | `ledger uat`, `state signoff.*`, `lifecycle advance uat` | Hybrid | CLI tracks UAT; user/agent acceptance remains collaborative. |
| `gsd-workspace` | `church:workspace`, `church workspace` | Automate more | Workspace CRUD is deterministic repo-local state and belongs in the CLI. |
| `gsd-workstreams` | `church:commission`, `church:workspace`, `church-workstream-deacon`, `lifecycle handoff` | Automate more | Workstream planning and workspace records are core lifecycle support. |

## Applied Repo Church Changes

- `church registry reasoning` exposes which parts stay agentic.
- `church context load` replaces repeated fresh-context inference.
- `church ledger` owns assumptions, gaps, UAT, and risk records.
- `church lifecycle handoff` owns deterministic handoff rendering.
- `church moat` owns moat persistence/rendering/scoring, while the skill owns market judgment.
- Skills now call CLI commands first, then reason over compact outputs.
