# Repo Church Lifecycle Model

Repo Church is a phase-chained lifecycle for work that must stay aligned with a durable project Bible.

## Stages

| Stage | Input | Output | Gate |
| --- | --- | --- | --- |
| Bible Intake | `.church/bible/` packet or equivalent project doctrine | Intake anchors and thin roadmap slice | Intake gate |
| Moat Definition | Market context, competitive set, owner vision, Bible draft | Moat JSON/Markdown, elevator pitch, scorecard, Bible integration tasks | Moat gate |
| Codebase Survey | Brownfield code, inventory, graph/map artifacts, architecture doctrine | Implementation map, interface risks, drift items | Survey gate |
| Research Hardening | Claims, assumptions, competitors, unstable facts | Confidence ledger | Evidence gate |
| Phase Anchoring | Roadmap and Bible requirements | Parent phase contract | Anchor gate |
| Spec Gate | Parent anchor and implementation target | Executable spec | Spec gate |
| Gap Closure | Audits, drift, contradictions, missing info | Closure ledger and remediation tasks | Closure gate |
| Execution Handoff | Approved spec and closure ledger | Frozen work package | Handoff gate |
| Collaborative UAT | Built feature and success criteria | UAT matrix and signoff record | Verification gate |
| Ship Gate | Diff, tests, docs, risk | Release decision | Ship gate |
| Refresh | Learnings and implementation changes | Bible or roadmap updates | Refresh gate |

## Bible Intake

The intake pass should be intentionally thin. Its job is not to produce a full implementation plan. It extracts the minimum set of anchors needed to know what must be researched before planning.

Required anchors:

- user and buyer,
- problem and desired outcome,
- non-goals,
- core success metrics,
- hard constraints,
- relevant requirement IDs,
- architecture and design doctrine,
- UX must-pass workflows,
- market threats or timing constraints.

## Moat Definition

The moat pass should run by default during greenfield and brownfield init. It names the competitive leverage that should shape the Bible, roadmap, architecture, and GTM.

Required outputs:

- elevator pitch,
- one-sentence moat,
- third-party summary,
- competitive set,
- entry wedge,
- primary leverage source,
- what compounds with use,
- what gets harder to copy,
- sustainability scorecard,
- proof and missing evidence,
- validation tasks,
- Bible integration tasks.

The moat must be easy for the owner to pitch and easier for a third party to understand. If it cannot be stated simply, the gate should hold.

## Codebase Survey

The survey pass is required when current implementation reality can change scope, architecture, dependencies, or validation. It is optional for truly greenfield work.

Required outputs:

- relevant modules and interfaces,
- data flows and external integrations,
- test and observability surfaces,
- ownership boundaries,
- implementation drift against Bible architecture/design doctrine,
- graph or map artifact usefulness,
- assumption or gap ledger entries for uncertain or blocking findings.

Inventory is only evidence. The survey gate holds when the agent cannot explain how the current codebase changes the next planning decision.

## Research Hardening

Assumptions should be treated as inventory, not narrative. A good hardening pass makes uncertainty visible and decides whether the next planning step is allowed.

Use current external sources for unstable market, pricing, platform, legal, standards, competitor, or provider claims. Use local repo evidence for implementation state. Use user statements as product intent, not as market proof.

## Phase Anchoring

A parent phase anchor is a contract for all child plans. It should be strong enough that two agents can independently produce compatible specs.

Minimum anchor content:

- phase objective,
- in scope and out of scope,
- Bible requirement IDs,
- measurable acceptance criteria,
- user stories and must-pass journeys,
- architecture and interface contracts,
- data and migration constraints,
- design doctrine,
- observability and rollback,
- risks and assumptions,
- dependency order,
- required validation and signoff mode.

## Spec Gate

Specs must be executable and falsifiable. Reject specs that describe intent without binding it to files, interfaces, tests, or verification artifacts.

Every spec should include:

- requirement traceability,
- file/module ownership,
- API/data contracts,
- edge cases,
- failure modes,
- implementation sequence,
- test plan,
- user validation plan,
- post-phase refresh obligations.

## Gap Closure

Gap closure is a separate stage because many lifecycle failures come from silently smoothing over contradictions. Capture the problem first, then resolve it.

Gap categories:

- missing requirement,
- weak acceptance criterion,
- stale or unverified market claim,
- architecture conflict,
- design doctrine conflict,
- phase dependency conflict,
- implementation drift,
- missing test or observability,
- unclear ownership,
- user signoff needed.

## Collaborative UAT

UAT is not only a final checklist. It is a phase-progression gate. For high-risk work, the agent must validate objective checks and the user must validate subjective, strategic, brand, or workflow fit.

## Refresh

Any execution that changes product doctrine, architecture doctrine, market positioning, success metrics, or phase order should create a Bible refresh item. Do not let implementation become undocumented strategy.
