<required_reading>
Read these files now:

1. `references/research-protocol.md`
2. `references/quality-gates.md`
3. `references/cli-offload.md`
</required_reading>

<process>
1. **Identify refresh trigger.**
   - New market data, competitor change, roadmap shift, implementation drift, design pivot, launch stage, funding/customer learning, or user-requested rebaseline.

2. **Snapshot current state.**
   - Run `scripts/repo-bible inventory --root <repo> --format json` (default writes `<bible-dir>/_repo-bible-inventory.json`; override with `--output`).
   - Run `scripts/repo-bible validate --root <repo> --format json` (default writes `<bible-dir>/_repo-bible-validation.json`; override with `--output`).
   - Record current Bible packet files and modified local project artifacts.
   - Do not overwrite prior research without preserving date/context.

3. **Refresh only unstable facts.**
   - Browse for pricing, docs, launch status, policies, standards, market share, product capabilities, security advisories, and competitor claims.
   - Prefer official/current sources.

4. **Diff against current Bible.**
   - Which requirements become stricter?
   - Which roadmap phases change?
   - Which assumptions are invalidated?
   - Which threats become less relevant?
   - Which visual/product claims become unsafe?

5. **Patch artifacts.**
   - Update market watchlist and source addenda.
   - Update success requirements if gates changed.
   - Update roadmap and architecture maps if scope/status changed.
   - Update design/persona/GTM doctrine when buyer or positioning evidence changed.
   - Add remediation rows for newly discovered drift.

6. **Validate and report.**
   - Rerun `scripts/repo-bible validate --root <repo>` (or pass `--path <packet-dir>` when not using defaults).
   - Regenerate `scripts/repo-bible render-html --root <repo>` if HTML review assets are part of the packet (defaults to `<bible-dir>/html`).
   - Run integrity checks.
   - Update validation report with date, trigger, sources, changed artifacts, and unresolved questions.
</process>

<success_criteria>
Refresh is complete when:

- New evidence is captured with date and source.
- Changed assumptions are mapped to requirements and roadmap impact.
- Artifacts are updated or explicitly left unchanged with rationale.
- Validation report reflects the refresh.
</success_criteria>
