---
title: Success Requirements
generated: YYYY-MM-DD
status: controlling checklist
---

# Success Requirements

## Lifecycle Gates

| Lifecycle | Minimum gates before promotion |
|---|---|
| Development | [Gate] |
| Private beta | [Gate] |
| Public beta | [Gate] |
| GA release | [Gate] |
| Growth | [Gate] |

## Requirements Checklist

| ID | Category | Lifecycle | Requirement | Quantified gate | Automatable task | Evidence | Validation artifact |
|---|---|---|---|---|---|---|---|
| S-01 | Strategy | Development | [Requirement] | [Metric/threshold] | [Task] | [Source/artifact] | [File/report] |

Minimum quality:

- Keep stable IDs (`S-01`, `S-02`, ...); every roadmap phase and spec should cite them.
- Replace every bracketed placeholder before treating the packet as usable.
- Each lifecycle stage needs at least one measurable requirement or an explicit non-applicability note.
- Evidence must be a concrete source, local artifact, command output, or dated user decision.
- Validation artifacts should name the file, report, command, screenshot, or UAT row that proves the gate.

Example row:

| ID | Category | Lifecycle | Requirement | Quantified gate | Automatable task | Evidence | Validation artifact |
|---|---|---|---|---|---|---|---|
| S-02 | Reliability | Private beta | Import 100 representative tasks without silent data loss | `import_audit` reports 0 lost required fields across reference dataset | Run deterministic import audit | `data/reference-tasks.json`, import audit output | `.church/validation/import-audit.md` |
