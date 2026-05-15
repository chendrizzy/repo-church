# Meta Refresh Record

The Bible, moat, lifecycle state, ledgers, proof artifact, rendered HTML, and tests now encode the self-hosted lifecycle requirement.

## Refreshed Artifacts

- `.church/bible/*.md`
- `.church/bible/_repo-bible-*.md`
- `.church/bible/html/`
- `.church/moat/moat.md`
- `.church/ledgers/*.json`
- `.church/proof/lifecycle-proof.json`
- `.church/state.json`

## Recheck

Run `church lifecycle prove --root . --self-package . --project-name "Repo Church" --format json`, then rerun the validation commands in `.church/ship/meta-ship-gate.md`.
