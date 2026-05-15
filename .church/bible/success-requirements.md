---
title: Success Requirements
generated: 2026-05-15
status: controlling checklist
---

# Success Requirements

## Lifecycle Gates

| Lifecycle | Minimum gates before promotion |
|---|---|
| Development | SR-01 E2E lifecycle test passes; SR-02 weak PASS probes fail as expected. |
| Private beta | SR-03 moat evidence cites local files, commands, and install smoke output. |
| Public beta | SR-04 command/agent outputs carry common traceability and closure fields. |
| GA release | SR-05 install surface, namespace guard, and package validation pass in CI-equivalent local runs. |
| Growth | Refresh loop updates Bible, roadmap, moat evidence, and validation report after each material change. |

## Requirements Checklist

| ID | Category | Lifecycle | Requirement | Quantified gate | Automatable task | Evidence | Validation artifact |
|---|---|---|---|---|---|---|---|
| SR-01 | Lifecycle | Development | Repo Church can run itself from `init` through `refresh` without manual state repair. | Full lifecycle test reaches active workflow `refresh` with `PASS`. | Add/run `tests/test_church_meta_lifecycle.py`. | `skills/church/scripts/church.py`, `.church/state.json`, lifecycle artifacts | `tests/test_church_meta_lifecycle.py`, `.church/validation/meta-lifecycle-e2e.md` |
| SR-02 | Gate integrity | Development | Passing outcomes require proof and cannot mask blockers. | Weak moat PASS, proofless closure, and forced ship-without-evidence all exit non-zero. | Run CLI failure-mode probes in tests. | `skills/church/scripts/church.py`, `tests/test_church_cli.py` | CLI test output |
| SR-03 | Moat proof | Private beta | Moat claims are backed by local implementation, docs, and validation evidence. | `church moat check` returns `PASS` and proof lists local evidence plus validation tests. | Import completed moat JSON and render Markdown. | `.church/moat/moat.json`, `.church/moat/moat.md`, `README.md`, tests | `.church/moat/moat.md`, `.church/validation/meta-ship-gate.md` |
| SR-04 | Output quality | Public beta | Command and specialist outputs require traceability, evidence quality, acceptance coverage, and closure/recheck fields. | All 21 command files mention common gate record; all 24 agent profiles mention standard footer. | `rg` count checks plus plugin asset tests. | `commands/*.md`, `agents/*.md`, `tests/test_church_plugin_assets.py` | `.church/validation/meta-uat.md` |
| SR-05 | Install surface | GA release | Public package surface remains portable and namespace-clean. | `validate-package.sh`, Python tests, and `npx skills add ./ --list` pass. | Run package validation and install smoke checks. | `AGENTS.md`, `.claude-plugin/plugin.json`, `tests/test_church_plugin_assets.py` | `.church/validation/meta-ship-gate.md` |
