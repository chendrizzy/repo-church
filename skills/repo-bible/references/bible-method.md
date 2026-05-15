<purpose>
This reference defines what a project Bible must contain and how to reason about it.
</purpose>

<definition>
A project Bible is a governing packet, not a slide deck. It should let a future agent or team member answer:

- What are we building and why now?
- Who must care, and why will they switch or adopt?
- What market forces threaten or enable us?
- What principles govern decisions?
- What measurable gates define success?
- What systems, architecture, UI, UX, GTM, and operations must exist?
- What current implementation or plan conflicts with the desired direction?
- How will we validate, refresh, and enforce this over time?
</definition>

<minimum_artifacts>
Recommended artifacts:

1. `README.md`: packet index, canonical positioning, non-negotiable gates.
2. `success-requirements.md`: measurable requirement checklist with automatable tasks.
3. `market-watchlist.md`: landscape, threats, opportunities, gaps, watch cadence.
4. `principles-doctrine.md`: constitution, philosophies, rationale, practical application.
5. `architecture-map.md`: existing/planned components, phase/status, dependencies, risks.
6. `design-doctrine.md`: brand, UI, visual system, accessibility, copy, UX posture.
7. `ux-workflows.md`: must-pass user journeys and if-X-then-Y cases.
8. `persona-gtm.md`: target personas, PMF logic, acquisition plays, GTM plan.
9. `roadmap.md`: optimized phase plan, specs/PRD implications, gates, owners.
10. `alignment-audit.md`: gaps, drift, conflicts, remediation.
11. `validation-report.md`: checks run, evidence coverage, caveats.
</minimum_artifacts>

<requirement_shape>
Every success requirement should include:

- ID.
- Category.
- Lifecycle stage.
- Requirement.
- Quantified gate.
- Automatable task.
- Evidence/source.
- Owner/phase if known.
- Validation artifact.
</requirement_shape>

<principles_shape>
Every constitutional principle should include:

- Principle name.
- Why it applies to this project.
- Evidence or historical pattern.
- Practical rules.
- Anti-patterns.
- Metrics that prove adherence.
</principles_shape>

<roadmap_shape>
Roadmap phases should include:

- Phase name and objective.
- Requirement IDs satisfied.
- Required specs/PRD/ADR.
- Existing components reused.
- New components planned.
- AI/eval/security/design/GTM flags.
- Exit criteria.
- Remediation dependencies.
</roadmap_shape>

<visualization_guidance>
Use visuals when they reduce ambiguity:

- Mermaid architecture graph for systems/components.
- Sequence diagram for UX or runtime flows.
- Matrix for competitors, threats, requirements, phases, or personas.
- Timeline for launch/GTM.
- Venn-style map for positioning.
- Funnel or flywheel for acquisition/growth.

Keep diagrams source-backed and reusable. Avoid decorative visuals.
</visualization_guidance>

<anti_patterns>
- Generic principles that could apply to any startup.
- Vanity metrics as success gates.
- "Guarantee success" claims without validation paths.
- Competitor summaries without implications.
- Roadmaps that add features without deletion/remediation.
- Design doctrine that ignores current implementation.
- GTM plans not tied to persona and channel evidence.
- Requirements without measurable gates.
</anti_patterns>

