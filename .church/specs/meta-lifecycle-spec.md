# Meta Lifecycle Spec

## Scope

Add deterministic proof that Repo Church can run its own lifecycle from moat through refresh without bypass flags.

## Requirements

| Requirement | Implementation | Verification |
|---|---|---|
| SR-01 | `church lifecycle prove` and `tests/test_church_meta_lifecycle.py` | Test reaches `refresh/PASS` |
| SR-02 | Existing quality checks stay active during proof | No `--force` or `--allow-quality-risk` in proof steps |
| SR-03 | Moat imports local evidence and validation tests | `church moat check` returns PASS |
| SR-05 | Proof registers required artifacts | Proof JSON lists stages and artifact paths |
