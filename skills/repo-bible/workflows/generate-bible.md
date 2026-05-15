<required_reading>
Read these files now:

1. `references/bible-method.md`
2. `references/research-protocol.md`
3. `references/quality-gates.md`
4. `references/cli-offload.md`
</required_reading>

<process>
1. **Establish scope and output path.**
   - Infer the project root from the current workspace unless the user names a path.
   - **Default:** write the Bible packet under **`<repo>/.church/bible/`** (Repo Church umbrella). Override only with explicit user preference, `--church-root`, `--bible-dir`, or `CHURCH_ROOT`.
   - Preserve existing docs; edit over create when a canonical artifact already exists.
   - If the user's vision is under-specified, run `scripts/repo-bible intake-html --root <repo>` (writes `vision-intake.html` under the resolved bible dir; optionally `--prefill <prior-export.json|md>`) and ask the user to complete/export it before doing a long interview.

2. **Inventory local evidence.**
   - First run `scripts/repo-bible inventory --root <repo> --format markdown` (writes `_repo-bible-inventory.md` under the resolved bible dir unless `--output -`).
   - Use the generated inventory to decide which files need LLM inspection.
   - Search for planning, research, specs, PRDs, roadmaps, architecture maps, design docs, brand docs, UX docs, tests, analytics, package files, schemas, and implementation status.
   - Record what exists, what is missing, what is stale, and what conflicts.
   - Include implementation reality: current components, planned components, known drift, technical debt, test coverage, and operational constraints.

3. **Refresh current market evidence.**
   - Research direct competitors, adjacent substitutes, platform incumbents, standards/protocol changes, pricing, ecosystem policies, security research, and buyer behavior.
   - Use primary sources when possible: official docs, pricing pages, changelogs, technical specs, filings, published research, public benchmarks, and credible industry reports.
   - Capture source URLs and dates. Label inference separately from verified facts.

4. **Derive the project constitution.**
   - Define canonical positioning and anti-positioning.
   - Define principles and philosophies only when they are supported by local or market evidence.
   - For each principle, explain why it matters to this project and how to apply it in practice.

5. **Derive stringent success requirements.**
   - Create requirement IDs by category.
   - Each requirement must include: requirement statement, quantifiable gate, automatable task, evidence artifact, lifecycle stage, and owner/phase when known.
   - Cover development, private beta, public beta, launch/GA, and growth.

6. **Build or update the Bible packet.**
   - For a new packet, run `scripts/repo-bible scaffold --root <repo>` (defaults to **`<repo>/.church/bible/`**) or `scripts/repo-bible scaffold --root <repo> --output <packet-dir>` to choose an explicit directory.
   - Use the templates that match the user's requested scope.
   - Recommended packet:
     - `README.md`
     - `success-requirements.md`
     - `market-landscape.md` or `market-watchlist.md`
     - `principles-doctrine.md`
     - `architecture-map.md`
     - `design-doctrine.md`
     - `ux-workflows.md`
     - `persona-gtm.md`
     - `roadmap.md`
     - `alignment-audit.md`
     - `validation-report.md`

7. **Map architecture and roadmap.**
   - Mark components as existing, partial, planned, external, risk, or deprecated.
   - Attach milestone/phase/status where available.
   - Identify AI/eval phases, security-sensitive phases, design phases, and GTM phases.
   - Add Mermaid diagrams when they improve reuse or clarity.

8. **Audit alignment and remediate drift.**
   - Compare current roadmap, architecture, implementation, docs, UX, brand, and GTM against the new requirements.
   - Capture conflicts before fixing.
   - Add remediation rows with severity, evidence, phase/source, action, and validation gate.

9. **Validate.**
   - Run `scripts/repo-bible validate --root <repo>` (defaults `--path` to **`<repo>/.church/bible/`**) for deterministic packet checks. Add `--requirement-prefixes` when IDs must match a controlled prefix set; add `--follow-local-md` / `--link-depth` when linked research docs should be included (output reports `link_traversal.mode`).
   - Run `scripts/repo-bible sources --root <repo>` to extract source URLs when useful (same follow flags as validate; defaults to the bible dir).
   - Run `scripts/repo-bible render-html --root <repo>` (defaults `--path` to the bible dir and `--output` to **`<bible-dir>/html`**) when a human-browsable packet would improve review.
   - Optionally run `scripts/repo-bible claim-scan --root <repo>` (defaults `--path` to the bible dir) with the same walk filters / `--follow-local-md` when linked markdown should be included in banned/required phrase scans. Pass `--path <repo>` to scan the full repository.
   - Run document integrity checks relevant to the repo: markdown fences, trailing whitespace, broken local links when feasible, required section scan, and git diff hygiene.
   - Verify every user-requested domain has an artifact.
   - Write a validation report with checks run, passed/failed status, known caveats, and next actions.

10. **Report outcome.**
    - Summarize created/updated artifacts.
    - Mention validation commands and caveats.
    - Do not claim market success is guaranteed; say which gates now govern the path to success.
</process>

<success_criteria>
Generation is complete when:

- The packet covers market, principles, requirements, architecture, design, UX, roadmap, personas, GTM, visual maps, remediation, and validation.
- Requirements are measurable and include actionable tasks.
- Current market research is source-backed.
- Existing/planned components are mapped with status and phase when known.
- Conflicts and false assumptions are captured before resolution.
- Validation report exists.
</success_criteria>
