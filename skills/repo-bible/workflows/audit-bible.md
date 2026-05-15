<required_reading>
Read these files now:

1. `references/bible-method.md`
2. `references/quality-gates.md`
3. `references/cli-offload.md`
</required_reading>

<process>
1. **Locate the Bible packet.**
   - Use user-provided paths first.
   - **Default canonical path:** `<repo>/.church/bible/`. Also consider legacy `.planning/commandments/` when using `--legacy-planning-bible` or during migration.
   - Otherwise search for `bible`, `commandments`, `doctrine`, `strategy`, `roadmap`, `requirements`, `market`, `design`, and `architecture` artifacts.

2. **Check artifact coverage.**
   - Run `scripts/repo-bible validate --root <repo>` (or `--path <packet-dir>` when not using defaults) first.
   - Use its errors, warnings, missing artifact terms, requirement IDs, and source counts as the audit baseline.
   - Market landscape and watchlist.
   - Success requirements.
   - Principles/constitution.
   - Architecture/infrastructure/system map.
   - Design/brand doctrine.
   - Specs/PRD/roadmap.
   - UX workflows and must-pass cases.
   - Persona/PMF/acquisition/GTM.
   - Visual maps.
   - Validation report.

3. **Score each artifact.**
   - `PASS`: actionable, evidence-backed, measurable, current.
   - `PARTIAL`: useful but missing measurable gates, sources, owners, or lifecycle coverage.
   - `FAIL`: absent, stale, generic, contradicted by code/research, or unverifiable.

4. **Audit against local reality.**
   - Run `scripts/repo-bible inventory --root <repo> --format markdown` before reading broad docs.
   - Compare claims to current implementation, tests, docs, roadmap, and known blockers.
   - Identify stale copy, fake proof, untracked migrations/assets, inconsistent states, and unsupported claims.

5. **Audit against current market reality.**
   - Run `scripts/repo-bible sources --root <repo> --path <packet-dir>` to see what is already sourced.
   - Browse for unstable or current competitive facts.
   - Flag new threats or changed assumptions.

6. **Produce audit output.**
   - Findings first, ordered by severity.
   - Include file/line references when local files are involved.
   - Add remediation rows with owner/phase/gate when known.
   - If the packet is hard to review in Markdown, run `scripts/repo-bible render-html --root <repo>` (writes HTML under `<bible-dir>/html` by default).
   - Update the Bible only if the user asked for fixes, not just review.
</process>

<success_criteria>
Audit is complete when:

- Every Bible domain has PASS/PARTIAL/FAIL status.
- High-severity contradictions are grounded in local evidence or current sources.
- Remediation actions are concrete, measurable, and phaseable.
- Any remaining caveats are explicit.
</success_criteria>
