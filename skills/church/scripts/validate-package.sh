#!/bin/bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
echo "Validating Repo Church skills package at ${ROOT}" >&2

python3 - "$ROOT" <<'PY'
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
skills_dir = root / "skills"
commands_dir = root / "commands"
agents_dir = root / "agents"
errors = []
warnings = []
skills = []
commands = []
agents = []

name_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

if not skills_dir.is_dir():
    errors.append("missing skills/ directory")
else:
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.relative_to(root)} missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{skill_md.relative_to(root)} missing YAML frontmatter")
            continue
        try:
            _, fm, body = text.split("---", 2)
        except ValueError:
            errors.append(f"{skill_md.relative_to(root)} malformed frontmatter")
            continue
        fields = {}
        for line in fm.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
        name = fields.get("name")
        desc = fields.get("description")
        if not name:
            errors.append(f"{skill_md.relative_to(root)} missing name")
        elif name != skill_dir.name:
            errors.append(f"{skill_md.relative_to(root)} name '{name}' does not match directory '{skill_dir.name}'")
        elif not name_re.match(name):
            errors.append(f"{skill_md.relative_to(root)} name is not lowercase kebab-case")
        if not desc:
            errors.append(f"{skill_md.relative_to(root)} missing description")
        elif len(desc) < 80:
            warnings.append(f"{skill_md.relative_to(root)} description may be too short for reliable triggering")
        if "TODO" in text:
            warnings.append(f"{skill_md.relative_to(root)} contains TODO")
        skills.append({"name": name or skill_dir.name, "lines": len(text.splitlines())})

if commands_dir.is_dir():
    for command_md in sorted(commands_dir.glob("*.md")):
        text = command_md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{command_md.relative_to(root)} missing YAML frontmatter")
            continue
        try:
            _, fm, body = text.split("---", 2)
        except ValueError:
            errors.append(f"{command_md.relative_to(root)} malformed frontmatter")
            continue
        fields = {}
        for line in fm.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
        name = fields.get("name")
        desc = fields.get("description")
        if not name:
            errors.append(f"{command_md.relative_to(root)} missing name")
        elif name != command_md.stem:
            errors.append(f"{command_md.relative_to(root)} name '{name}' does not match file stem '{command_md.stem}'")
        elif not name_re.match(name):
            errors.append(f"{command_md.relative_to(root)} name is not lowercase kebab-case")
        if not desc:
            errors.append(f"{command_md.relative_to(root)} missing description")
        if "church" not in text:
            warnings.append(f"{command_md.relative_to(root)} does not reference church CLI")
        commands.append({"name": name or command_md.stem, "lines": len(text.splitlines())})

if agents_dir.is_dir():
    for agent_md in sorted(agents_dir.glob("*.md")):
        text = agent_md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{agent_md.relative_to(root)} missing YAML frontmatter")
            continue
        try:
            _, fm, body = text.split("---", 2)
        except ValueError:
            errors.append(f"{agent_md.relative_to(root)} malformed frontmatter")
            continue
        fields = {}
        for line in fm.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
        name = fields.get("name")
        desc = fields.get("description")
        if not name:
            errors.append(f"{agent_md.relative_to(root)} missing name")
        elif name != agent_md.stem:
            errors.append(f"{agent_md.relative_to(root)} name '{name}' does not match file stem '{agent_md.stem}'")
        elif not name_re.match(name):
            errors.append(f"{agent_md.relative_to(root)} name is not lowercase kebab-case")
        if not desc:
            errors.append(f"{agent_md.relative_to(root)} missing description")
        for required in ["## Required Inputs", "## Work", "## Output", "## Quality Bar"]:
            if required not in text:
                errors.append(f"{agent_md.relative_to(root)} missing {required}")
        agents.append({"name": name or agent_md.stem, "lines": len(text.splitlines())})

evals = root / "evals" / "evals.json"
if not evals.is_file():
    warnings.append("missing evals/evals.json")
else:
    try:
        data = json.loads(evals.read_text(encoding="utf-8"))
        if "evals" not in data or not isinstance(data["evals"], list):
            errors.append("evals/evals.json missing evals array")
    except Exception as exc:
        errors.append(f"evals/evals.json invalid JSON: {exc}")

result = {
    "ok": not errors,
    "skills": skills,
    "commands": commands,
    "agents": agents,
    "errors": errors,
    "warnings": warnings,
}
print(json.dumps(result, indent=2))
if errors:
    sys.exit(1)
PY
