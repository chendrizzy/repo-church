<purpose>
This reference defines validation standards for a high-quality project Bible.
</purpose>

<coverage_gates>
The Bible is incomplete if any of these are absent:

- Market landscape and competitive watchlist.
- Threats, gaps, opportunities, pitfalls.
- Core objectives and success requirements.
- Constitutional principles with evidence and application rules.
- Architecture, infrastructure, systems, and design doctrine.
- Specs/PRD/roadmap and phase gates.
- UX non-negotiables and must-pass workflows.
- Target personas, PMF rationale, acquisition strategy.
- GTM plan from pre-launch through growth.
- Reusable visual maps/graphs/blueprints.
- Alignment audit and remediation plan.
- Validation report.
</coverage_gates>

<strictness_gates>
Every major claim should be one of:

- Verified by local artifact.
- Verified by current external source.
- Historical pattern with source and applicability rationale.
- Hypothesis with validation task and failure criteria.

If it is none of these, remove or rewrite it.
</strictness_gates>

<measurability_gates>
Requirements must avoid vague verbs such as "improve", "optimize", "support", "be good", or "ensure" unless paired with:

- Metric.
- Threshold.
- Time/lifecycle stage.
- Test or verification method.
- Responsible phase/owner when known.
</measurability_gates>

<workflow_gates>
UX workflows must be written as enforceable paths:

- If user/persona does X, system must Y.
- If system cannot Y, it must Z.
- Include success, failure, permission, latency, recovery, and audit expectations.
</workflow_gates>

<validation_checks>
Run applicable checks:

- Markdown fence balance.
- Trailing whitespace.
- Required artifact/section scan.
- Local link/path existence where feasible.
- Source URL presence for current market claims.
- Requirement ID count and category coverage.
- Roadmap-to-requirement mapping.
- Architecture component status coverage.
- Design doctrine coverage if UI exists.
- `git diff --check` for tracked edited files.
</validation_checks>

<completion_standard>
Do not mark the work complete until:

- Coverage gates pass or caveats are explicitly documented.
- High-severity conflicts are captured.
- Remediation plan exists for every unresolved drift.
- Validation report states checks run and known caveats.
- Final response names created/updated artifacts and validation result.
</completion_standard>

