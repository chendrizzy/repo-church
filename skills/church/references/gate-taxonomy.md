# Gate Taxonomy

Repo Church uses explicit gate outcomes so phase status is not confused with artifact existence.

## Outcomes

| Outcome | Meaning | Allowed next step |
| --- | --- | --- |
| `PASS` | All required evidence and acceptance checks are satisfied. | Continue. |
| `PASS_WITH_RISK` | Work may continue, but a known risk is documented with owner, trigger, and mitigation. | Continue only if risk is non-critical. |
| `HOLD` | Missing information or user input prevents a reliable decision, but no confirmed defect exists. | Pause progression until resolved. |
| `BLOCK` | A contradiction, failed check, or critical missing requirement makes progression unsafe. | Do not proceed; open closure work. |

## Status Values

Use these statuses in ledgers. Keep lifecycle outcome, ledger status, research confidence, and UAT result as separate fields; do not overload `status` with confidence labels or test results.

- `open`
- `in-progress`
- `satisfied`
- `deferred-with-owner`
- `superseded`
- `contradicted`
- `blocked`

Avoid vague states such as "done-ish", "probably", "needs review", or "TBD" without an owner and next action.

## Ledger Closure Quality

A ledger item is not closed just because its status says `satisfied`. Closure requires:

- owner is assigned and not `unassigned`,
- evidence points to the source problem or validation artifact,
- proof explains what changed or passed,
- recheck command or trigger is present for deferred items,
- acceptance test is named for anything that blocks progression.

Unknown statuses, unknown severities, missing required fields, and `satisfied` items without proof should be treated as unresolved by CLI checks.

## Gate Families

| Gate | Blocks When |
| --- | --- |
| Intake gate | Bible path is missing, core user/outcome/constraints cannot be identified, or roadmap slice has no requirement IDs. |
| Moat gate | Competitive leverage is generic, unclear, unsupported, or disconnected from Bible/roadmap/GTM decisions. |
| Evidence gate | High-impact assumptions are unverified, stale, or contradicted. |
| Anchor gate | Parent phase lacks objective, scope, interfaces, measurable acceptance, dependency order, or signoff mode. |
| Spec gate | Spec lacks traceability, file/module ownership, test plan, edge cases, or user-story validation. |
| Closure gate | Gaps have no owner, proof, or recheck path. |
| Handoff gate | Next executor cannot proceed without re-reading broad context or guessing scope. |
| Verification gate | Must-pass workflows fail, objective checks are absent, or mutual signoff is required but missing. |
| Ship gate | Tests/docs/risk/rollback/Bible alignment are incomplete. |

## Mutual Signoff Triggers

Require both agent and user approval before phase progression when work affects:

- user-facing product direction,
- brand or design doctrine,
- pricing, monetization, or GTM,
- data migrations or destructive operations,
- auth, security, privacy, or compliance,
- irreversible infrastructure,
- roadmap order or phase scope,
- ambiguous subjective UX quality.

## Gate Record Format

Every staged command output must include this common record before stage-specific sections. A `PASS` or `PASS_WITH_RISK` should also be recorded with `church lifecycle advance ... --evidence <proof-or-artifact>` so the state file can reject evidence-free passing outcomes.

```markdown
Gate:
Outcome:
Evidence:
Evidence type: verified-local | verified-current | supported-secondary | user-intent | hypothesis | stale | contradicted
Confidence:
Inference vs direct support:
Failed criteria:
Risk owner:
Required next action:
Recheck command or artifact:
User signoff required: yes|no
Agent signoff: yes|no
User signoff: yes|no|pending
```
