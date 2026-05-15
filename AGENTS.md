# AGENTS.md

This repository contains an agent-agnostic skill package following the skills.sh style.

## Skill Authoring Rules

- Keep each skill in `skills/<skill-name>/SKILL.md`.
- Keep staged slash-command assets in `commands/<command-name>.md`.
- Keep lazy-loaded specialist profiles in `agents/<agent-name>.md`.
- Make `name` match the parent directory exactly.
- Use lowercase kebab-case names only.
- Put trigger language in `description`; do not rely on title-only descriptions.
- Keep `SKILL.md` concise and move detailed checklists into `references/` inside the same skill directory.
- Prefer deterministic scripts for validation and repetitive checks.
- Keep package source portable across agents. Do not require Cursor, Codex, Claude, or a single vendor unless a skill explicitly declares that compatibility.

## Repo Church Rules

- `repo-bible` owns Bible generation, audits, and refreshes.
- `church` owns lifecycle routing, gates, and artifact handoffs.
- `commands/` owns the staged invocation surface; commands must name progressive skill loading, CLI preflight, gates, specialist agents, and output shape.
- `agents/` owns specialist profile contracts; profiles must state required inputs, work, output, and quality bar.
- Child skills must be usable independently, but should use the same gate names and output sections as the umbrella skill.
- Every phase plan should trace to Bible requirement IDs, architecture/design doctrine, success metrics, and verification evidence.
- Every blocker should become a closure item with owner, evidence, acceptance test, and recheck command.

## Validation

Run before publishing or installing broadly:

```bash
bash skills/church/scripts/validate-package.sh .
```
