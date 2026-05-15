# Meta Ship Gate

SHIP_READY: yes.

## Proof-Owned Validation

| Check | Command | Required result |
|---|---|---|
| Lifecycle proof | `church lifecycle prove --root . --self-package . --project-name "Repo Church"` | `refresh/PASS` |
| Package validator | `bash skills/church/scripts/validate-package.sh .` | 0 errors, 0 warnings |
| CLI tests | `python3 tests/test_church_cli.py` | all pass |
| Plugin asset tests | `python3 tests/test_church_plugin_assets.py` | all pass |
| Bible validation | `church bible validate --root . --follow-local-md --format json --output -` | 0 errors, 0 warnings |
| Install smoke | `npx skills add ./ --list` | 12 intended skills listed |

## External Regression

`python3 tests/test_church_meta_lifecycle.py` validates this proof command on an isolated temporary root. It remains outside the proof-owned command list to avoid recursive self-invocation.

## Quality Constraints

- No lifecycle `--force` or `--allow-quality-risk` appears in the proof command log.
- Market moat claims remain local-evidence-backed until P03 dated competitor research is completed.
