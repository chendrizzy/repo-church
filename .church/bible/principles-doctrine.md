---
title: Principles Doctrine
generated: 2026-05-15
status: operating constitution
---

# Principles Doctrine

| ID | Principle | Practical rule | Evidence |
|---|---|---|---|
| PR-01 | Evidence before certainty | A gate cannot pass without proof, artifacts, or a recheckable source. | `lifecycle_quality_check`, `gate-taxonomy.md` |
| PR-02 | CLI owns mechanics; agents own judgment | Automate state, ledgers, reports, and validation; do not automate strategy approval. | `skills/church/SKILL.md`, `cli-automation-map.md` |
| PR-03 | Traceability beats ceremony | Every phase, spec, UAT row, and ship decision cites requirement IDs or a doctrine-change request. | `success-requirements.md`, `stage-command-map.md` |
| PR-04 | Closure requires proof | `satisfied` means evidence plus proof, not a hopeful status label. | `ledger_item_quality_issues` |
| PR-05 | Portability is a product constraint | Commands and scripts must not depend on one agent runtime. | `AGENTS.md`, `skills/church/scripts/church` |

## Decision Rules

- Prefer a `HOLD` over a speculative `PASS` when evidence is thin.
- Convert every blocker into a ledger item with owner, acceptance test, and recheck command.
- Keep public namespace surfaces stable unless validation proves a hard cutover is safer.
- Treat every Bible update as a source-of-truth change that needs validation and refresh notes.
