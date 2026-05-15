---
name: church
description: Orchestrate Repo Church lifecycle workflows around a Repo Bible packet. Use when the user mentions church, repo-bible-driven planning, GSD-inspired phase gates, lifecycle hardening, assumption validation, gap closure, collaborative UAT, phase handoff, ship gate, or wants a stricter planning-to-verification workflow.
license: MIT
metadata:
  version: "0.1.0"
  package: church
---

# Repo Church

Repo Church is a portable lifecycle framework for turning a Repo Bible into executable, evidence-backed work. It keeps GSD's useful phase chaining and artifact handoff discipline, then tightens the loose spots: assumptions, gap closure, parent phase anchors, spec acceptance, parallelism, and collaborative verification.

## Use This For

- Building or operating a repo-wide planning lifecycle from a Repo Bible.
- Turning vision, research, and doctrine into phase anchors and specs.
- Hardening assumptions before implementation.
- Finding and closing drift between plans, code, design, and market evidence.
- Running post-phase UAT with agent and user signoff.
- Preparing release or merge readiness gates.

If the user only needs to generate, audit, or refresh the Bible packet itself, use `repo-bible` first.

## Core Vocabulary

Use this lifecycle vocabulary consistently:

| Term | Meaning |
| --- | --- |
| Bible | Durable `.church/bible/` packet containing doctrine, requirements, market watchlist, architecture/design doctrine, roadmap, UX workflows, GTM, and validation. |
| Anchor | A parent phase contract with objective, scope, non-goals, requirements, interfaces, risks, dependencies, and must-pass verification. |
| Gate | A decision checkpoint with acceptance criteria and evidence. Outcomes are `PASS`, `PASS_WITH_RISK`, `HOLD`, or `BLOCK`. |
| Ledger | A table of assumptions, gaps, drift, or risks with owner, evidence, status, and closure proof. |
| Handoff | A frozen execution brief that names consumed artifacts, scope, first moves, validation commands, and unresolved risk. |
| Mutual signoff | A high-risk verification mode where the agent and user both approve progression. |

Read `references/stage-command-map.md` for the staged command sequence, `references/counterpart-gap-closure.md` for the closed GSD-to-Repo-Church deltas, `references/deferred-parity-closure.md` for the corrective parity pass, `references/final-optimization-gap-closure.md` for the final looped closure report, `references/lifecycle-model.md` for the complete lifecycle, `references/gate-taxonomy.md` for gate semantics, `references/cli-automation-map.md` for what the CLI now owns, `references/gsd-workflow-assessment.md` for the GSD-derived automation boundaries, `references/cli-architecture.md` for the root CLI design, `references/tooling-workbench.md` for CLI/HTML workflow rules, `references/moat-framework.md` for competitive moat research, `references/research-confidence.md` for evidence thresholds, `references/parallelism-guide.md` for safe concurrency, and `references/verification-protocol.md` for UAT/signoff rules.

## CLI First

For lifecycle work, run deterministic commands before synthesizing:

```bash
church context load --root <repo> --format markdown
church registry list --format json
church registry reasoning --format markdown
church lifecycle status --root <repo> --format json
```

Use the skill for interpretation, not for manually reconstructing state that the CLI can load.

Do not automate away reasoning-heavy stages. Market/moat definition, spec quality, architecture decisions, debugging hypotheses, UI judgment, security review, and user acceptance must still be handled by an agent or user using the CLI outputs as evidence.

When deciding whether to move a new workflow into the CLI, apply the true/false questionnaire in `references/gsd-workflow-assessment.md`. Default to automating evidence collection and state handling, not the decision itself.

## Lifecycle

1. **Bible Intake**
   - Run `church init` for greenfield or brownfield project init when available.
   - Confirm the Bible packet exists or run `church bible ...` / `repo-bible`.
   - Run the Repo Bible inventory CLI before loading broad docs when the package has the script available.
   - Use `intake-html` for large vision capture or when the user wants autonomous field filling followed by human review.
   - Extract intake anchors: problem, target user, non-goals, success signals, hard constraints, doctrine IDs, UX must-pass workflows.
   - Output a thin roadmap slice only; do not deep-plan before assumptions are hardened.

2. **Moat Definition**
   - Define the project's competitive leverage during initial project init.
   - Produce an elevator pitch, one-sentence moat, third-party summary, competitive map, sustainability scorecard, proof, risks, and validation tasks.
   - Integrate moat implications into Bible positioning, success requirements, roadmap, architecture, and GTM.

3. **Codebase Survey**
   - Run when brownfield implementation reality can affect scope, interfaces, dependencies, or validation.
   - Use `church:survey` / `church bible inventory` before architecture-sensitive anchoring.
   - Map modules, interfaces, data flows, integrations, tests, and drift against Bible doctrine.
   - Treat graph/map artifacts as evidence; keep architecture judgment agentic.

4. **Research Hardening**
   - Build an assumption ledger.
   - Label every critical claim `verified`, `current-source-backed`, `local-evidence-backed`, `hypothesis`, `stale`, or `contradicted`.
   - Research unstable or high-impact assumptions before phase planning.

5. **Phase Anchoring**
   - Strengthen the parent phase before child plans.
   - Require measurable outcomes, interface contracts, dependency order, architectural constraints, design doctrine, and verification responsibilities.
   - Reject anchors that cannot guide independent execution.

6. **Spec Gate**
   - Turn anchors into implementation specs with requirement IDs, acceptance tests, non-goals, risk controls, data/interface contracts, migration notes, and user-story must-pass checks.
   - Every spec must trace back to Bible requirement IDs or explicitly document a doctrine change request.
   - Prefer generated validation/source/claim reports as inputs over raw whole-repo reading.

7. **Gap Closure**
   - Capture contradictions, missing evidence, under-specified areas, and implementation drift before resolving them.
   - Close each gap with a remediation task and proof, or defer it with owner, deadline, and risk.

8. **Execution Handoff**
   - Freeze phase scope and consumed artifacts.
   - Name independent work streams and safe parallelism.
   - Include first actions, commands, validation gates, and rollback notes.

9. **Collaborative UAT**
   - Convert success requirements and user stories into a UAT matrix.
   - Render the Bible or phase packet to HTML when a human needs to scan criteria and sign off efficiently.
   - Run agent checks first, then user-path validation for subjective or product-critical flows.
   - Require mutual signoff for irreversible, brand-critical, data-risk, security-risk, or strategy-changing work.

10. **Ship Gate**
   - Verify tests, docs, migrations, observability, rollback, Bible alignment, and unresolved risk.
   - Output `SHIP_READY: yes|no` with evidence.

11. **Refresh**
   - If implementation changes doctrine, update the Bible or file a Bible drift item.
   - Run validation, source extraction, claim scan, and HTML render when packet contents change materially.
   - Feed learnings into the next anchor.

## Routing

| User intent | Load |
| --- | --- |
| Generate or audit the Bible packet | `repo-bible` |
| Initialize lifecycle state or default moat artifacts | `church`, CLI `church init` |
| Define competitive moat and defensibility | `church-moat` |
| Start from Bible and identify next phase | `church-intake` |
| Map brownfield codebase reality before planning | `church:survey`, `church-codebase-cartographer` |
| Validate assumptions or research confidence | `church-harden` |
| Improve roadmap parent phase anchors | `church-anchor` |
| Review PRD/spec/planning quality | `church-spec-gate` |
| Close drift, contradictions, or missing evidence | `church-gap-closure` |
| Prepare execution continuation | `church-handoff` |
| Run UAT and mutual signoff | `church-uat` |
| Release/merge readiness | `church-ship` |
| Reduce redundant lifecycle work or improve parallelism | `church-optimizer` |

## Default Output

Use this structure unless a child skill defines a narrower template:

```markdown
## Church Verdict
Gate: PASS | PASS_WITH_RISK | HOLD | BLOCK
Reason:
Required next action:

## Evidence Consumed
- [path or URL] - why it matters

## Findings
| ID | Type | Severity | Evidence | Impact | Resolution |
| --- | --- | --- | --- | --- | --- |

## Updated Lifecycle State
| Stage | Status | Evidence | Next |
| --- | --- | --- | --- |

## Parallel Work Map
| Stream | Can run now? | Blocked by | Owner |
| --- | --- | --- | --- |

## Handoff
- Frozen scope:
- Open gaps:
- Validation command:
- User signoff needed:
```

## Completion Standard

Repo Church work is complete only when:

- CLI and HTML workbench opportunities were used or explicitly skipped as unnecessary.
- Initial project moat is defined, scored, and integrated into the Bible or marked as a blocking gap.
- Required Bible artifacts were consumed or the absence is explicitly blocking.
- Every phase/spec/verification item traces to a requirement, doctrine, or documented change request.
- Assumptions are confidence-labeled and high-impact unknowns are researched.
- Gaps have closure tasks and proof requirements.
- Parallelizable work is separated from critical-path work.
- The next agent or human can continue without re-deriving the lifecycle state.
