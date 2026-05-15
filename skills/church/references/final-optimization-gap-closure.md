# Final Optimization Gap Closure

Generated: 2026-05-14

Scope: final iterative review of the Repo Church framework against the GSD skill/workflow library, with emphasis on overlooked counterpart coverage, risky phrasing, inefficient or ambiguous processes, and verifiable gap closure.

## Review Standard

A review loop is clean only when all of these checks pass:

1. Package validation reports zero errors and zero warnings.
2. Plugin asset tests pass for command/profile completeness, manifest wiring, staged labels, GSD assessment hygiene, and reference consistency.
3. CLI E2E tests pass across init, registry, state, moat, lifecycle, ledger, context, and Bible delegation.
4. Manifest and eval JSON parse cleanly.
5. Stale comparison scans find no unresolved claims such as missing command/profile layers, unresolved `future` placeholders, legacy backlog labels, or scope-downgrade classifications.
6. `npx skills add ./agent-skills/repo-church --list` discovers the package.

## Gap Evaluations

| ID | Gap | Evidence | Evaluation | Closure Plan | Status |
| --- | --- | --- | --- | --- | --- |
| FOG-001 | Stale comparison artifact still claimed Repo Church lacked slash commands and specialist profiles. | `.agents/skills/gsd-church_asset-comparison` contained pre-remediation status text. | High clarity risk: later agents could trust stale comparison output and rebuild solved assets. | Replace the artifact with current coverage mapping and concrete assets for every deferred row. | Closed |
| FOG-002 | GSD map-codebase/graphify coverage was under-specified. | Prior comparison had blank rows; `gsd-workflow-assessment.md` referenced deferred map/graph commands. | High planning risk for brownfield work: implementation reality can invalidate anchors/specs. | Add `church:survey`, `church-codebase-cartographer`, registry `survey` gate, lifecycle docs, and tests. | Closed |
| FOG-003 | `church:survey` initially existed as a command but not as deterministic lifecycle state. | `church registry show survey` failed before registry update. | Medium consistency risk: a named gate without registry support weakens handoff and progression tracking. | Add `survey` to `WORKFLOW_REGISTRY`, reasoning boundaries, allowed transitions, and CLI E2E assertions. | Closed |
| FOG-004 | GSD-derived extension mechanics were described as deferred instead of actual feature coverage. | `gsd-workflow-assessment.md` had archive/graph/inbox/workspace/workstream/undo/thread entries without concrete counterpart assets. | High parity risk: omission classifications undercut the requirement for complete GSD counterpart coverage. | Add actual church command/profile/CLI coverage for hooks, workspace, thread, inbox, profile, sketch, branch, undo, and archive mechanics. Add tests blocking stale scope classifications. | Closed |
| FOG-005 | Command-center shortcut lacked progressive loading and specialist routing. | `church-council.md` only had CLI pattern/output sections. | Low usability risk: status command could expose blockers without routing triage. | Add progressive loading for `church-gap-closure` and `church-optimizer`, plus gap/doc specialists. | Closed |
| FOG-006 | Validation docs did not list the plugin asset regression suite. | README validate section omitted `test_church_plugin_assets.py`. | Low maintenance risk: contributors might run CLI tests only and miss command/profile regressions. | Add asset test command to README validation block. | Closed |

## Deferred Rows Converted To Assets

The following GSD capabilities are now represented by concrete Repo Church assets:

| GSD area | Repo Church asset | Automation boundary |
| --- | --- | --- |
| Runtime hooks | `church:guard`, `church-runtime-guardian`, `church hooks plan/check/scaffold` | CLI produces reviewed hook plans and portable fallbacks; runtime adapters require explicit review. |
| Workspace and thread CRUD | `church:workspace`, `church:thread`, workspace/thread CLI registries | CLI stores portable state; agents judge partitioning, stale context, and continuation quality. |
| Inbox and backlog | `church:inbox`, `church-triage-steward`, `church inbox add/list/check` | CLI records and counts blockers; agents decide priority/scope. |
| Behavioral user profiling | `church:profile`, `church-profile-counselor`, `church profile init/set/export/check` | CLI enforces consent and storage; interpretation remains agent-led. |
| Creative sketching surface | `church:sketch`, `church-sketch-curator`, `church sketch register/list/check` | CLI tracks artifacts and signoff blockers; creative judgment remains agent/user-led. |
| PR branch filtering, undo, cleanup | `church:branch`, `church:rewind`, `church:archive`, git/archive planning CLIs | CLI renders dry-run plans and risk warnings; execution requires explicit review. |

This closes coverage by replacing prior omissions with concrete assets while preserving review gates for risky operations.

## Loop Results

| Loop | Findings | Remediation | Verification |
| --- | --- | --- | --- |
| 1 | FOG-001, FOG-002, FOG-004, FOG-005, FOG-006 | Added survey command/profile, updated comparison and assessment docs, tightened council, added tests/docs. | Initial targeted tests passed after patch. |
| 2 | FOG-003 | Added `survey` registry workflow, reasoning boundary, allowed transitions, and CLI assertions. | Targeted registry/CLI checks passed. |
| 3 | None | No change. | Clean loop 1 passed. |
| 4 | None | No change. | Clean loop 2 passed. |
| 5 | None | No change. | Clean loop 3 passed. |

## Consecutive Clean Loop Evidence

Each clean loop ran:

```bash
bash agent-skills/repo-church/skills/church/scripts/validate-package.sh agent-skills/repo-church
python3 agent-skills/repo-church/tests/test_church_plugin_assets.py
python3 agent-skills/repo-church/tests/test_church_cli.py
python3 -m json.tool agent-skills/repo-church/.claude-plugin/plugin.json
python3 -m json.tool agent-skills/repo-church/evals/evals.json
rg <stale-gap-patterns> agent-skills/repo-church .agents/skills/gsd-church_asset-comparison
npx skills add ./agent-skills/repo-church --list
```

Result: three consecutive clean loops returned no identified gap-closure opportunities.

## Corrective Parity Pass Evidence

After the deferred-row scope correction, the package was rechecked with:

```bash
python3 -m py_compile agent-skills/repo-church/skills/church/scripts/church.py
bash agent-skills/repo-church/skills/church/scripts/validate-package.sh agent-skills/repo-church
python3 agent-skills/repo-church/tests/test_church_plugin_assets.py
python3 agent-skills/repo-church/tests/test_church_cli.py
python3 -m json.tool agent-skills/repo-church/.claude-plugin/plugin.json
python3 -m json.tool agent-skills/repo-church/evals/evals.json
rg <stale-scope-patterns> agent-skills/repo-church/skills/church/references agent-skills/repo-church/README.md .agents/skills/gsd-church_asset-comparison
npx skills add ./agent-skills/repo-church --list
```

Result: all checks passed. The stale-scope scan returned no matches outside regression-test assertions.

## Namespace Hard Cutover Evidence

The public framework namespace was migrated to `church` after parity closure:

- primary CLI is `skills/church/scripts/church`,
- no legacy CLI alias remains under `skills/church/scripts/`,
- framework skills install as `church`, `church-*`, and `repo-bible`,
- specialist profiles use `church-*`,
- the legacy long namespace remains only as package/plugin identity or package path text,
- the asset regression suite includes a hard-cutover guard for stale CLI/profile references.

## Current Closure Verdict

Outcome: `PASS`

Repo Church now has:

- 12 skills,
- 21 staged command assets,
- 24 specialist profiles,
- deterministic lifecycle registry coverage including `survey` and operational parity workflows,
- GSD workflow assessment without unresolved deferral placeholders,
- up-to-date GSD-to-Church comparison,
- asset tests and CLI E2E tests guarding the framework skeleton.

The framework is ready to be applied to API Bank planning and implementation work, with previously deferred GSD parity rows represented by actual Repo Church assets.
