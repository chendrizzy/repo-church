---
title: Optimized Roadmap
generated: YYYY-MM-DD
status: roadmap reference
---

# Optimized Roadmap

| Phase | Objective | Requirement IDs | Existing components | New components | Required specs/ADRs | Exit gate |
|---|---|---|---|---|---|---|
| P00 | [Objective] | [IDs] | [Components] | [Components] | [Docs] | [Gate] |

Minimum quality:

- Replace every bracketed placeholder before using this as a planning source.
- Every phase must cite requirement IDs from Success Requirements or document a doctrine-change request.
- Every exit gate must be measurable and point to a validation artifact, test, UAT row, or signoff record.
- Mark AI, eval, security, data, migration, design, and GTM flags explicitly so specialist review is routed early.

Example row:

| Phase | Objective | Requirement IDs | Existing components | New components | Required specs/ADRs | Exit gate |
|---|---|---|---|---|---|---|
| P01 | Make the import path auditable end to end | S-02, A-03 | `src/importer`, `tests/fixtures` | `.church/validation/import-audit.md` | ADR-001 import guarantees, SPEC-P01 | 0 lost required fields in reference dataset and signed audit report |

## Phase Details

### P00: [Name]

- Goal:
- Tasks:
- AI/eval/security/design/GTM flags:
- Dependencies:
- Exit criteria:
