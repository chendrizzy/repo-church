---
title: Alignment Audit
generated: 2026-05-15
status: audit reference
---

# Alignment Audit

## Summary

Repo Church already has the core architecture for self-governance: lifecycle skill, deterministic CLI, command surface, specialist agents, Bible CLI, tests, package validator, and install smoke path. The current meta run found that production readiness depends on turning that architecture into a repeatable full-lifecycle proof and ensuring the moat is supported by local evidence.

## Findings

| ID | Type | Severity | Evidence | Impact | Resolution |
|---|---|---|---|---|---|
| AA-01 | Missing proof | High | No dedicated test previously advanced all lifecycle keys from moat through refresh. | Framework could claim E2E readiness without executable proof. | Add `tests/test_church_meta_lifecycle.py`. |
| AA-02 | Meta-Bible placeholders | High | Scaffolded `.church/bible/*.md` contained bracket placeholders. | Agents could plan from vague doctrine. | Replace with requirement-traced meta-Bible. |
| AA-03 | Moat evidence gap | High | Initial `.church/moat/moat.json` scored `BLOCK`. | No hard moat support. | Import completed moat with local evidence and validation tests. |
| AA-04 | External market caveat | Medium | No live competitor research performed in this meta run. | Market positioning should not overclaim. | Keep claims local-evidence-backed; schedule P03 market refresh. |

## Closure Items

| Gap | Owner | Acceptance test | Evidence required | Recheck |
|---|---|---|---|---|
| AA-01 | agent | Meta lifecycle test passes. | Test output and validation report. | `python3 tests/test_church_meta_lifecycle.py` |
| AA-02 | agent | Bible validate reports no required artifact terms missing. | `_repo-bible-validation.md`. | `church bible validate --root . --follow-local-md` |
| AA-03 | agent | `church moat check` returns `PASS`. | `.church/moat/moat.md`. | `church moat check --root .` |
| AA-04 | future owner | Market claims cite current sources. | Updated market watchlist. | P03 refresh gate |
