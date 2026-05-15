#!/usr/bin/env python3
"""Repo Church deterministic lifecycle helper CLI.

This CLI intentionally owns the mechanical workflow state, artifact routing,
moat templates, ledgers, and handoff/context rendering so agents spend their
tokens on judgment-heavy work instead of re-deriving lifecycle state.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import pathlib
import subprocess
import sys
from typing import Any


SCHEMA_VERSION = "church-state/v1"
MOAT_SCHEMA_VERSION = "church-moat/v1"
LEDGER_SCHEMA_VERSION = "church-ledger/v1"

DEFAULT_CHURCH_ROOT = ".church"
DEFAULT_BIBLE_DIR = ".church/bible"
DEFAULT_MOAT_DIR = ".church/moat"
DEFAULT_LEDGER_DIR = ".church/ledgers"
DEFAULT_RUNTIME_DIR = ".church/runtime"

GATE_OUTCOMES = ["PASS", "PASS_WITH_RISK", "HOLD", "BLOCK"]
PASSING_OUTCOMES = {"PASS", "PASS_WITH_RISK"}
UNKNOWN_OWNER_VALUES = {"", "unassigned", "unknown", "tbd", "todo", "none"}

WORKFLOW_REGISTRY: dict[str, dict[str, Any]] = {
    "init": {
        "default_stage": "project-init",
        "gate": "intake",
        "skill": "church",
        "required_artifacts": ["state", "moat_json", "moat_md"],
        "next": ["moat", "bible", "survey"],
        "automation": ["state-create", "moat-template", "artifact-registry"],
    },
    "moat": {
        "default_stage": "moat-definition",
        "gate": "moat",
        "skill": "church-moat",
        "required_artifacts": ["moat_json", "moat_md"],
        "next": ["bible", "survey", "harden", "anchor"],
        "automation": ["moat-template", "moat-score", "moat-render"],
    },
    "bible": {
        "default_stage": "bible-generation",
        "gate": "bible",
        "skill": "repo-bible",
        "required_artifacts": ["bible_packet"],
        "next": ["survey", "harden", "anchor"],
        "automation": ["delegate-repo-bible-cli"],
    },
    "survey": {
        "default_stage": "codebase-survey",
        "gate": "survey",
        "skill": "church",
        "required_artifacts": ["bible_inventory"],
        "next": ["harden", "anchor", "gap-closure"],
        "automation": ["context-load", "delegate-repo-bible-cli", "ledger-track"],
    },
    "harden": {
        "default_stage": "research-hardening",
        "gate": "evidence",
        "skill": "church-harden",
        "required_artifacts": ["assumption_ledger"],
        "next": ["anchor", "gap-closure"],
        "automation": ["ledger-track", "context-load"],
    },
    "anchor": {
        "default_stage": "phase-anchor",
        "gate": "anchor",
        "skill": "church-anchor",
        "required_artifacts": ["phase_anchor"],
        "next": ["spec-gate", "gap-closure"],
        "automation": ["state-advance", "artifact-registry"],
    },
    "spec-gate": {
        "default_stage": "spec-gate",
        "gate": "spec",
        "skill": "church-spec-gate",
        "required_artifacts": ["spec_gate"],
        "next": ["gap-closure", "handoff"],
        "automation": ["artifact-registry", "ledger-track"],
    },
    "gap-closure": {
        "default_stage": "gap-closure",
        "gate": "closure",
        "skill": "church-gap-closure",
        "required_artifacts": ["gap_ledger"],
        "next": ["spec-gate", "handoff"],
        "automation": ["ledger-track", "ledger-check"],
    },
    "handoff": {
        "default_stage": "execution-handoff",
        "gate": "handoff",
        "skill": "church-handoff",
        "required_artifacts": ["handoff"],
        "next": ["uat"],
        "automation": ["handoff-render", "context-load"],
    },
    "uat": {
        "default_stage": "collaborative-uat",
        "gate": "verification",
        "skill": "church-uat",
        "required_artifacts": ["uat_ledger"],
        "next": ["ship", "gap-closure"],
        "automation": ["ledger-track", "signoff-state"],
    },
    "ship": {
        "default_stage": "ship-gate",
        "gate": "ship",
        "skill": "church-ship",
        "required_artifacts": ["ship_gate"],
        "next": ["refresh"],
        "automation": ["gate-record", "signoff-state"],
    },
    "refresh": {
        "default_stage": "bible-refresh",
        "gate": "refresh",
        "skill": "repo-bible",
        "required_artifacts": ["refresh_record"],
        "next": ["moat", "anchor", "init"],
        "automation": ["delegate-repo-bible-cli", "state-advance"],
    },
    "hooks": {
        "default_stage": "runtime-hooks",
        "gate": "runtime",
        "skill": "church",
        "required_artifacts": ["hook_plan"],
        "next": ["init", "harden", "ship"],
        "automation": ["runtime-detect", "hook-plan", "fallback-render"],
    },
    "workspace": {
        "default_stage": "workspace-management",
        "gate": "workspace",
        "skill": "church",
        "required_artifacts": ["workspace_registry"],
        "next": ["init", "handoff", "refresh"],
        "automation": ["workspace-registry", "state-set"],
    },
    "thread": {
        "default_stage": "thread-management",
        "gate": "thread",
        "skill": "church-handoff",
        "required_artifacts": ["thread_registry"],
        "next": ["handoff", "refresh", "init"],
        "automation": ["thread-registry", "context-load", "handoff-link"],
    },
    "inbox": {
        "default_stage": "inbox-triage",
        "gate": "triage",
        "skill": "church-gap-closure",
        "required_artifacts": ["inbox_registry"],
        "next": ["harden", "gap-closure", "anchor"],
        "automation": ["inbox-registry", "ledger-routing"],
    },
    "profile": {
        "default_stage": "profile-capture",
        "gate": "consent",
        "skill": "church",
        "required_artifacts": ["profile_artifact"],
        "next": ["harden", "anchor", "uat"],
        "automation": ["consent-state", "profile-artifact"],
    },
    "sketch": {
        "default_stage": "sketch-capture",
        "gate": "design-artifact",
        "skill": "church-uat",
        "required_artifacts": ["sketch_registry"],
        "next": ["spec-gate", "uat", "refresh"],
        "automation": ["artifact-registry", "signoff-routing"],
    },
    "branch": {
        "default_stage": "branch-planning",
        "gate": "branch",
        "skill": "church-ship",
        "required_artifacts": ["branch_plan"],
        "next": ["ship", "refresh"],
        "automation": ["git-inspect", "branch-plan"],
    },
    "undo": {
        "default_stage": "undo-planning",
        "gate": "rollback",
        "skill": "church-ship",
        "required_artifacts": ["undo_plan"],
        "next": ["gap-closure", "ship", "refresh"],
        "automation": ["git-inspect", "rollback-plan"],
    },
    "archive": {
        "default_stage": "archive-planning",
        "gate": "archive",
        "skill": "church",
        "required_artifacts": ["archive_plan"],
        "next": ["refresh", "init"],
        "automation": ["artifact-inventory", "archive-plan"],
    },
}

STATE_KEY_REGISTRY: dict[str, dict[str, str]] = {
    "schema_version": {"type": "string", "purpose": "State schema version."},
    "repo_root": {"type": "path", "purpose": "Absolute repository root captured at init."},
    "church_root": {"type": "path", "purpose": "Repo Church artifact root, usually .church."},
    "bible_dir": {"type": "path", "purpose": "Durable Repo Bible packet directory."},
    "moat_dir": {"type": "path", "purpose": "Moat JSON and Markdown artifact directory."},
    "ledger_dir": {"type": "path", "purpose": "Structured lifecycle ledgers."},
    "active.workflow": {"type": "enum", "purpose": "Current workflow key from registry."},
    "active.stage": {"type": "string", "purpose": "Current lifecycle stage label."},
    "active.gate": {"type": "string", "purpose": "Current gate family."},
    "active.outcome": {"type": "enum", "purpose": "Current gate outcome."},
    "active.phase": {"type": "string|null", "purpose": "Current phase, if known."},
    "active.milestone": {"type": "string|null", "purpose": "Current milestone, if known."},
    "artifacts.<name>": {"type": "path", "purpose": "Named relative artifact path."},
    "signoff.agent": {"type": "boolean", "purpose": "Agent verification signoff."},
    "signoff.user": {"type": "boolean", "purpose": "User verification signoff."},
    "signoff.mutual_required": {"type": "boolean", "purpose": "Whether both signoffs are required."},
    "active.workspace": {"type": "string|null", "purpose": "Current Repo Church workspace, if any."},
    "active.thread": {"type": "string|null", "purpose": "Current Repo Church thread/handoff record, if any."},
}

REASONING_BOUNDARIES: dict[str, dict[str, Any]] = {
    "init": {
        "cli_owned": ["state creation", "artifact paths", "default moat scaffold", "optional Bible scaffold"],
        "agent_owned": ["greenfield vs brownfield implications", "project intent synthesis", "initial moat language"],
        "do_not_fully_automate": ["market positioning", "product strategy"],
    },
    "moat": {
        "cli_owned": ["moat JSON template", "dotted key updates", "import/export", "Markdown render", "coverage scoring"],
        "agent_owned": ["competitive research", "defensibility judgment", "elevator-pitch clarity", "Bible integration strategy"],
        "do_not_fully_automate": ["claiming durable advantage", "accepting unsupported moat claims"],
    },
    "bible": {
        "cli_owned": ["inventory", "scaffold", "source extraction", "validation", "claim scan", "HTML intake/render"],
        "agent_owned": ["doctrine synthesis", "market interpretation", "requirement design", "conflict resolution"],
        "do_not_fully_automate": ["strategic principles", "success requirements", "architecture doctrine"],
    },
    "survey": {
        "cli_owned": ["context load", "Bible inventory", "local artifact paths", "ledger storage"],
        "agent_owned": ["architecture interpretation", "interface risk", "implementation drift", "graph/map evidence quality"],
        "do_not_fully_automate": ["treating inventory as architecture judgment"],
    },
    "harden": {
        "cli_owned": ["assumption ledger storage", "source reports", "claim scans", "blocker checks"],
        "agent_owned": ["evidence quality judgment", "research interpretation", "risk impact"],
        "do_not_fully_automate": ["deciding that a hypothesis is safe enough for planning"],
    },
    "anchor": {
        "cli_owned": ["phase state", "artifact registration", "handoff context"],
        "agent_owned": ["phase slicing", "acceptance criteria quality", "dependency sequencing"],
        "do_not_fully_automate": ["parent phase scope approval"],
    },
    "spec-gate": {
        "cli_owned": ["Bible validation", "gap ledger records", "gate state"],
        "agent_owned": ["spec viability", "architecture tradeoffs", "execution risk"],
        "do_not_fully_automate": ["approving under-specified implementation plans"],
    },
    "gap-closure": {
        "cli_owned": ["gap ledger add/list/check", "status persistence", "proof links"],
        "agent_owned": ["root-cause interpretation", "remediation quality", "defer vs block decisions"],
        "do_not_fully_automate": ["silently downgrading unresolved blockers"],
    },
    "handoff": {
        "cli_owned": ["compact context rendering", "artifact listing", "history summary"],
        "agent_owned": ["first moves", "critical path", "parallel stream judgment"],
        "do_not_fully_automate": ["scope freeze when requirements conflict"],
    },
    "uat": {
        "cli_owned": ["UAT ledger storage", "signoff state", "HTML criteria render"],
        "agent_owned": ["workflow interpretation", "subjective UX quality", "failure severity"],
        "do_not_fully_automate": ["user acceptance", "brand/design approval"],
    },
    "ship": {
        "cli_owned": ["gate state", "ledger checks", "artifact links"],
        "agent_owned": ["release risk", "rollback adequacy", "Bible drift judgment"],
        "do_not_fully_automate": ["shipping with unresolved critical risk"],
    },
    "refresh": {
        "cli_owned": ["Bible CLI delegation", "state update"],
        "agent_owned": ["what doctrine changed", "whether strategy shifted", "market source interpretation"],
        "do_not_fully_automate": ["rewriting project direction"],
    },
    "hooks": {
        "cli_owned": ["runtime detection", "hook plan rendering", "fallback command generation", "hook scaffold artifact"],
        "agent_owned": ["which hooks are worth enabling", "risk mitigation for runtime-specific behavior"],
        "do_not_fully_automate": ["installing destructive hooks without explicit review"],
    },
    "workspace": {
        "cli_owned": ["workspace registry", "active workspace state", "status persistence"],
        "agent_owned": ["work partitioning rationale", "dependency and ownership judgment"],
        "do_not_fully_automate": ["creating conflicting workspaces without integration plan"],
    },
    "thread": {
        "cli_owned": ["thread registry", "handoff links", "resume hints"],
        "agent_owned": ["handoff quality", "what context matters for continuation"],
        "do_not_fully_automate": ["assuming stale thread context is current"],
    },
    "inbox": {
        "cli_owned": ["inbox item storage", "status counts", "ledger routing hints"],
        "agent_owned": ["priority, scope, and doctrine impact"],
        "do_not_fully_automate": ["silently converting ideas into approved scope"],
    },
    "profile": {
        "cli_owned": ["consent state", "profile artifact storage", "export"],
        "agent_owned": ["behavioral interpretation", "personalization ethics", "usefulness of profile signals"],
        "do_not_fully_automate": ["profiling without explicit consent"],
    },
    "sketch": {
        "cli_owned": ["design artifact registry", "signoff requirement state", "artifact links"],
        "agent_owned": ["creative direction", "design quality", "doctrine fit"],
        "do_not_fully_automate": ["approving subjective design without user acceptance"],
    },
    "branch": {
        "cli_owned": ["git status inspection", "clean branch plan rendering", "exclude/include classification"],
        "agent_owned": ["review scope judgment", "whether plan should be executed"],
        "do_not_fully_automate": ["rewriting branches without explicit confirmation"],
    },
    "undo": {
        "cli_owned": ["git status/log inspection", "rollback plan rendering", "risk warnings"],
        "agent_owned": ["root-cause and rollback suitability judgment"],
        "do_not_fully_automate": ["destructive restore/revert without explicit confirmation"],
    },
    "archive": {
        "cli_owned": ["artifact inventory", "archive plan rendering", "dry-run output"],
        "agent_owned": ["whether artifacts are safe to archive", "retention policy judgment"],
        "do_not_fully_automate": ["moving or deleting lifecycle evidence without review"],
    },
}

LEDGER_KINDS: dict[str, dict[str, Any]] = {
    "assumptions": {
        "required_fields": ["id", "status", "summary", "evidence", "owner"],
        "blocking_statuses": ["hypothesis", "stale", "contradicted", "blocked", "open"],
    },
    "gaps": {
        "required_fields": ["id", "status", "summary", "severity", "evidence", "owner"],
        "blocking_statuses": ["open", "blocked", "contradicted"],
    },
    "uat": {
        "required_fields": ["id", "status", "summary", "evidence", "owner"],
        "blocking_statuses": ["fail", "blocked", "open"],
    },
    "risks": {
        "required_fields": ["id", "status", "summary", "severity", "owner"],
        "blocking_statuses": ["open", "blocked"],
    },
}


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def repo_root(path: str | pathlib.Path) -> pathlib.Path:
    return pathlib.Path(path).expanduser().resolve()


def church_root(root: pathlib.Path) -> pathlib.Path:
    return root / DEFAULT_CHURCH_ROOT


def state_path(root: pathlib.Path) -> pathlib.Path:
    return church_root(root) / "state.json"


def moat_dir(root: pathlib.Path) -> pathlib.Path:
    return root / DEFAULT_MOAT_DIR


def ledger_dir(root: pathlib.Path) -> pathlib.Path:
    return root / DEFAULT_LEDGER_DIR


def ledger_path(root: pathlib.Path, kind: str) -> pathlib.Path:
    return ledger_dir(root) / f"{kind}.json"


def runtime_dir(root: pathlib.Path) -> pathlib.Path:
    return root / DEFAULT_RUNTIME_DIR


def registry_path(root: pathlib.Path, kind: str) -> pathlib.Path:
    return runtime_dir(root) / f"{kind}.json"


def load_json(path: pathlib.Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return dict(default or {})
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: invalid JSON at {path}: {exc}") from exc


def write_json(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        raise SystemExit("Error: --stdin was set but stdin was empty.\nExample: cat moat.json | church moat import --root . --stdin")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: stdin is not valid JSON: {exc}") from exc


def get_path(data: dict[str, Any], dotted: str) -> Any:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(dotted)
        cur = cur[part]
    return cur


def set_path(data: dict[str, Any], dotted: str, value: Any) -> None:
    cur = data
    parts = dotted.split(".")
    for part in parts[:-1]:
        existing = cur.setdefault(part, {})
        if not isinstance(existing, dict):
            raise SystemExit(f"Error: cannot set {dotted}; {part} is not an object.")
        cur = existing
    cur[parts[-1]] = value


def validate_state_set(key: str, value: Any) -> None:
    mutable_keys = {
        "active.workflow",
        "active.stage",
        "active.gate",
        "active.outcome",
        "active.phase",
        "active.milestone",
        "active.workspace",
        "active.thread",
        "signoff.agent",
        "signoff.user",
        "signoff.mutual_required",
    }
    if key.startswith("artifacts."):
        if missing_quality_value(key, value):
            raise SystemExit("Error: artifact state values must be non-empty paths.")
        return
    if key not in mutable_keys:
        raise SystemExit(
            f"Error: refusing to set unknown or unsafe state key '{key}'.\n"
            "Use church registry keys for supported state fields."
        )
    if key == "active.workflow" and value not in WORKFLOW_REGISTRY:
        raise SystemExit(f"Error: active.workflow must be one of: {', '.join(sorted(WORKFLOW_REGISTRY))}")
    if key == "active.outcome" and value not in GATE_OUTCOMES:
        raise SystemExit(f"Error: active.outcome must be one of: {', '.join(GATE_OUTCOMES)}")
    if key == "active.gate":
        known_gates = {info["gate"] for info in WORKFLOW_REGISTRY.values()}
        if value not in known_gates:
            raise SystemExit(f"Error: active.gate must be one of: {', '.join(sorted(known_gates))}")
    if key.startswith("signoff.") and not isinstance(value, bool):
        raise SystemExit(f"Error: {key} must be true or false.")


def merge_dict(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def coerce_value(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    try:
        return json.loads(value)
    except Exception:
        return value


def missing_quality_value(field: str, value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return True
        if field == "owner" and stripped.lower() in UNKNOWN_OWNER_VALUES:
            return True
        return False
    if isinstance(value, (list, dict, tuple, set)):
        return not bool(value)
    return False


def parse_artifact_updates(artifact_args: list[str] | None) -> dict[str, str]:
    updates: dict[str, str] = {}
    for artifact in artifact_args or []:
        if "=" not in artifact:
            raise SystemExit(
                "Error: --artifact must use NAME=PATH.\n"
                "Example: church lifecycle advance handoff --artifact handoff=.church/handoff.md"
            )
        key, value = artifact.split("=", 1)
        if not key.strip() or not value.strip():
            raise SystemExit("Error: --artifact requires non-empty NAME=PATH.")
        updates[key] = value
    return updates


def relative_to_root(root: pathlib.Path, path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def emit_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def emit_markdown(data: Any, title: str = "Repo Church") -> None:
    print(render_markdown(data, title))


def render_markdown(data: Any, title: str = "Repo Church") -> str:
    lines = [f"# {title}", ""]

    def render_value(key: str, value: Any, depth: int = 0) -> None:
        indent = "  " * depth
        if isinstance(value, dict):
            lines.append(f"{indent}- {key}:")
            for child_key, child_value in value.items():
                render_value(str(child_key), child_value, depth + 1)
        elif isinstance(value, list):
            lines.append(f"{indent}- {key}:")
            if not value:
                lines.append(f"{indent}  - []")
            for item in value:
                if isinstance(item, (dict, list)):
                    lines.append(f"{indent}  -")
                    render_value("item", item, depth + 2)
                else:
                    lines.append(f"{indent}  - {item}")
        else:
            lines.append(f"{indent}- {key}: {value}")

    if isinstance(data, dict):
        for key, value in data.items():
            render_value(str(key), value)
    elif isinstance(data, list):
        for item in data:
            lines.append(f"- {item}")
    else:
        lines.append(str(data))
    lines.append("")
    return "\n".join(lines)


def emit(data: Any, fmt: str, title: str = "Repo Church") -> None:
    if fmt == "json":
        emit_json(data)
    else:
        emit_markdown(data, title)


def default_state(root: pathlib.Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "repo_root": str(root),
        "church_root": DEFAULT_CHURCH_ROOT,
        "bible_dir": DEFAULT_BIBLE_DIR,
        "moat_dir": DEFAULT_MOAT_DIR,
        "ledger_dir": DEFAULT_LEDGER_DIR,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "active": {
            "workflow": "init",
            "stage": WORKFLOW_REGISTRY["init"]["default_stage"],
            "gate": WORKFLOW_REGISTRY["init"]["gate"],
            "outcome": "HOLD",
            "phase": None,
            "milestone": None,
        },
        "artifacts": {
            "state": ".church/state.json",
            "moat_json": ".church/moat/moat.json",
            "moat_md": ".church/moat/moat.md",
            "bible_packet": ".church/bible/",
            "assumption_ledger": ".church/ledgers/assumptions.json",
            "gap_ledger": ".church/ledgers/gaps.json",
            "uat_ledger": ".church/ledgers/uat.json",
            "risk_ledger": ".church/ledgers/risks.json",
        },
        "signoff": {
            "agent": False,
            "user": False,
            "mutual_required": False,
        },
        "workflows": WORKFLOW_REGISTRY,
        "state_keys": STATE_KEY_REGISTRY,
        "history": [],
    }


def save_state(root: pathlib.Path, data: dict[str, Any]) -> None:
    data["updated_at"] = now_iso()
    write_json(state_path(root), data)


def ensure_state(root: pathlib.Path) -> dict[str, Any]:
    path = state_path(root)
    if path.exists():
        return load_json(path)
    data = default_state(root)
    save_state(root, data)
    return data


def bible_script() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[2] / "repo-bible" / "scripts" / "repo_bible.py"


def run_bible(args: list[str]) -> int:
    script = bible_script()
    if not script.exists():
        print(f"Error: missing repo-bible CLI: {script}", file=sys.stderr)
        return 1
    return subprocess.run([sys.executable, str(script), *args], check=False).returncode


def run_bible_capture(args: list[str]) -> subprocess.CompletedProcess[str]:
    script = bible_script()
    if not script.exists():
        raise SystemExit(f"Error: missing repo-bible CLI: {script}")
    return subprocess.run([sys.executable, str(script), *args], check=False, capture_output=True, text=True)


def moat_template(project_name: str) -> dict[str, Any]:
    return {
        "schema_version": MOAT_SCHEMA_VERSION,
        "project_name": project_name,
        "updated_at": now_iso(),
        "elevator_pitch": "",
        "third_party_summary": "",
        "one_sentence_moat": "",
        "market": {
            "category": "",
            "buyer": "",
            "user": "",
            "urgent_pain": "",
            "why_now": "",
        },
        "competition": {
            "direct": [],
            "adjacent": [],
            "status_quo": [],
            "substitutes": [],
        },
        "wedge": {
            "entry_point": "",
            "first_10_users": "",
            "switching_trigger": "",
            "time_to_value": "",
        },
        "leverage": {
            "primary_source": "",
            "secondary_sources": [],
            "what_compounds_with_use": "",
            "what_gets_harder_to_copy": "",
        },
        "sustainability": {
            "defensibility": "",
            "switching_costs": "",
            "distribution_advantage": "",
            "data_or_learning_loop": "",
            "ecosystem_lock_in": "",
            "trust_or_compliance": "",
        },
        "proof": {
            "local_evidence": [],
            "market_evidence": [],
            "customer_evidence": [],
            "missing_evidence": [],
        },
        "risks": [],
        "validation_tests": [],
        "scorecard": {
            "clarity": 0,
            "urgency": 0,
            "differentiation": 0,
            "durability": 0,
            "evidence": 0,
            "third_party_comprehension": 0,
        },
    }


def render_moat_md(moat: dict[str, Any]) -> str:
    scorecard = moat.get("scorecard", {})
    competition = moat.get("competition", {})
    proof = moat.get("proof", {})
    sustainability = moat.get("sustainability", {})
    leverage = moat.get("leverage", {})
    wedge = moat.get("wedge", {})
    market = moat.get("market", {})

    def bullets(items: Any) -> str:
        if not items:
            return "- Not yet defined"
        if isinstance(items, list):
            return "\n".join(f"- {item}" for item in items) if items else "- Not yet defined"
        return f"- {items}"

    lines = [
        "# Project Moat",
        "",
        f"Updated: {moat.get('updated_at', '')}",
        "",
        "## Elevator Pitch",
        moat.get("elevator_pitch") or "Not yet defined.",
        "",
        "## Third-Party Summary",
        moat.get("third_party_summary") or "Not yet defined.",
        "",
        "## One-Sentence Moat",
        moat.get("one_sentence_moat") or "Not yet defined.",
        "",
        "## Market",
        f"- Category: {market.get('category') or 'Not yet defined'}",
        f"- Buyer: {market.get('buyer') or 'Not yet defined'}",
        f"- User: {market.get('user') or 'Not yet defined'}",
        f"- Urgent pain: {market.get('urgent_pain') or 'Not yet defined'}",
        f"- Why now: {market.get('why_now') or 'Not yet defined'}",
        "",
        "## Competitive Set",
        "### Direct",
        bullets(competition.get("direct")),
        "",
        "### Adjacent",
        bullets(competition.get("adjacent")),
        "",
        "### Status Quo",
        bullets(competition.get("status_quo")),
        "",
        "### Substitutes",
        bullets(competition.get("substitutes")),
        "",
        "## Wedge",
        f"- Entry point: {wedge.get('entry_point') or 'Not yet defined'}",
        f"- First 10 users: {wedge.get('first_10_users') or 'Not yet defined'}",
        f"- Switching trigger: {wedge.get('switching_trigger') or 'Not yet defined'}",
        f"- Time to value: {wedge.get('time_to_value') or 'Not yet defined'}",
        "",
        "## Leverage",
        f"- Primary source: {leverage.get('primary_source') or 'Not yet defined'}",
        f"- Secondary sources: {', '.join(leverage.get('secondary_sources') or []) or 'Not yet defined'}",
        f"- What compounds with use: {leverage.get('what_compounds_with_use') or 'Not yet defined'}",
        f"- What gets harder to copy: {leverage.get('what_gets_harder_to_copy') or 'Not yet defined'}",
        "",
        "## Sustainability",
        f"- Defensibility: {sustainability.get('defensibility') or 'Not yet defined'}",
        f"- Switching costs: {sustainability.get('switching_costs') or 'Not yet defined'}",
        f"- Distribution advantage: {sustainability.get('distribution_advantage') or 'Not yet defined'}",
        f"- Data or learning loop: {sustainability.get('data_or_learning_loop') or 'Not yet defined'}",
        f"- Ecosystem lock-in: {sustainability.get('ecosystem_lock_in') or 'Not yet defined'}",
        f"- Trust or compliance: {sustainability.get('trust_or_compliance') or 'Not yet defined'}",
        "",
        "## Proof",
        "### Local Evidence",
        bullets(proof.get("local_evidence")),
        "",
        "### Market Evidence",
        bullets(proof.get("market_evidence")),
        "",
        "### Customer Evidence",
        bullets(proof.get("customer_evidence")),
        "",
        "### Missing Evidence",
        bullets(proof.get("missing_evidence")),
        "",
        "## Risks",
        bullets(moat.get("risks")),
        "",
        "## Validation Tests",
        bullets(moat.get("validation_tests")),
        "",
        "## Scorecard",
    ]
    for key in ["clarity", "urgency", "differentiation", "durability", "evidence", "third_party_comprehension"]:
        lines.append(f"- {key}: {scorecard.get(key, 0)}/4")
    lines.append("")
    return "\n".join(lines)


def score_moat(moat: dict[str, Any]) -> dict[str, Any]:
    required_paths = [
        "elevator_pitch",
        "third_party_summary",
        "one_sentence_moat",
        "market.category",
        "market.buyer",
        "market.urgent_pain",
        "market.why_now",
        "competition.direct",
        "competition.status_quo",
        "wedge.entry_point",
        "wedge.switching_trigger",
        "leverage.primary_source",
        "leverage.what_compounds_with_use",
        "leverage.what_gets_harder_to_copy",
        "sustainability.defensibility",
        "proof.market_evidence",
        "validation_tests",
    ]
    narrative_paths = {
        "elevator_pitch",
        "third_party_summary",
        "one_sentence_moat",
        "market.category",
        "market.buyer",
        "market.urgent_pain",
        "market.why_now",
        "wedge.entry_point",
        "wedge.switching_trigger",
        "leverage.primary_source",
        "leverage.what_compounds_with_use",
        "leverage.what_gets_harder_to_copy",
        "sustainability.defensibility",
    }
    source_list_paths = {"proof.market_evidence", "validation_tests"}
    missing: list[str] = []
    quality_issues: list[str] = []
    present = 0
    if moat.get("schema_version") != MOAT_SCHEMA_VERSION:
        quality_issues.append(f"schema_version must be {MOAT_SCHEMA_VERSION}")
    for dotted in required_paths:
        try:
            value = get_path(moat, dotted)
        except KeyError:
            missing.append(dotted)
            continue
        if not value:
            missing.append(dotted)
        elif dotted in narrative_paths and (not isinstance(value, str) or len(value.strip()) < 12):
            missing.append(dotted)
            quality_issues.append(f"{dotted} is too thin to evaluate")
        elif dotted in source_list_paths and (
            not isinstance(value, list)
            or not value
            or any(not isinstance(item, str) or len(item.strip()) < 12 for item in value)
        ):
            missing.append(dotted)
            quality_issues.append(f"{dotted} must include substantive evidence items")
        else:
            present += 1
    scorecard = moat.get("scorecard", {})
    if isinstance(scorecard, dict):
        for key in ["clarity", "urgency", "differentiation", "durability", "evidence", "third_party_comprehension"]:
            value = scorecard.get(key)
            if not isinstance(value, int) or value < 0 or value > 4:
                quality_issues.append(f"scorecard.{key} must be an integer from 0 to 4")
    else:
        quality_issues.append("scorecard must be an object")
    coverage = present / len(required_paths)
    if coverage >= 0.9:
        outcome = "PASS"
    elif coverage >= 0.7:
        outcome = "PASS_WITH_RISK"
    elif coverage >= 0.4:
        outcome = "HOLD"
    else:
        outcome = "BLOCK"
    if quality_issues and outcome in PASSING_OUTCOMES:
        outcome = "HOLD"
    return {
        "outcome": outcome,
        "coverage": round(coverage, 3),
        "present": present,
        "required": len(required_paths),
        "missing": missing,
        "quality_issues": quality_issues,
    }


def create_moat(root: pathlib.Path, project_name: str | None, force: bool = False) -> dict[str, str | bool]:
    target_dir = moat_dir(root)
    json_path = target_dir / "moat.json"
    md_path = target_dir / "moat.md"
    if json_path.exists() and not force:
        return {"moat_json": str(json_path), "moat_md": str(md_path), "exists": True}
    target_dir.mkdir(parents=True, exist_ok=True)
    moat = moat_template(project_name or root.name)
    write_json(json_path, moat)
    md_path.write_text(render_moat_md(moat), encoding="utf-8")
    return {"moat_json": str(json_path), "moat_md": str(md_path), "exists": False}


def load_moat(root: pathlib.Path, input_path: str | None = None) -> tuple[pathlib.Path, dict[str, Any]]:
    path = pathlib.Path(input_path).expanduser().resolve() if input_path else moat_dir(root) / "moat.json"
    if not path.exists():
        raise SystemExit(f"Error: moat file not found: {path}\nExample: church moat init --root {root}")
    return path, load_json(path)


def save_moat(root: pathlib.Path, moat: dict[str, Any], output_path: str | None = None) -> pathlib.Path:
    path = pathlib.Path(output_path).expanduser().resolve() if output_path else moat_dir(root) / "moat.json"
    moat["updated_at"] = now_iso()
    write_json(path, moat)
    return path


def empty_ledger(kind: str) -> dict[str, Any]:
    if kind not in LEDGER_KINDS:
        raise SystemExit(f"Error: unknown ledger kind '{kind}'. Choices: {', '.join(sorted(LEDGER_KINDS))}")
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "kind": kind,
        "updated_at": now_iso(),
        "items": [],
    }


def load_ledger(root: pathlib.Path, kind: str) -> dict[str, Any]:
    path = ledger_path(root, kind)
    if not path.exists():
        return empty_ledger(kind)
    return load_json(path)


def save_ledger(root: pathlib.Path, kind: str, data: dict[str, Any]) -> pathlib.Path:
    data["updated_at"] = now_iso()
    path = ledger_path(root, kind)
    write_json(path, data)
    return path


def empty_registry(kind: str) -> dict[str, Any]:
    return {
        "schema_version": f"church-{kind}/v1",
        "kind": kind,
        "updated_at": now_iso(),
        "items": [],
    }


def load_registry(root: pathlib.Path, kind: str) -> dict[str, Any]:
    path = registry_path(root, kind)
    if not path.exists():
        return empty_registry(kind)
    return load_json(path)


def save_registry(root: pathlib.Path, kind: str, data: dict[str, Any]) -> pathlib.Path:
    data["updated_at"] = now_iso()
    path = registry_path(root, kind)
    write_json(path, data)
    return path


def upsert_registry_item(root: pathlib.Path, kind: str, item_id: str, item: dict[str, Any], force: bool = False) -> tuple[pathlib.Path, dict[str, Any]]:
    data = load_registry(root, kind)
    existing = [entry for entry in data.get("items", []) if entry.get("id") == item_id or entry.get("name") == item_id]
    if existing and not force:
        raise SystemExit(f"Error: {kind} item '{item_id}' already exists. Use --force to replace it.")
    data["items"] = [entry for entry in data.get("items", []) if entry.get("id") != item_id and entry.get("name") != item_id]
    item.setdefault("id", item_id)
    item.setdefault("created_at", now_iso())
    item["updated_at"] = now_iso()
    data.setdefault("items", []).append(item)
    path = save_registry(root, kind, data)
    return path, item


def find_registry_item(data: dict[str, Any], item_id: str) -> dict[str, Any] | None:
    for item in data.get("items", []):
        if item.get("id") == item_id or item.get("name") == item_id:
            return item
    return None


def update_registry_item_status(root: pathlib.Path, kind: str, item_id: str, status: str) -> tuple[pathlib.Path, dict[str, Any]]:
    data = load_registry(root, kind)
    item = find_registry_item(data, item_id)
    if item is None:
        raise SystemExit(f"Error: {kind} item '{item_id}' not found.")
    item["status"] = status
    item["updated_at"] = now_iso()
    path = save_registry(root, kind, data)
    return path, item


def ledger_item_quality_issues(item: dict[str, Any], kind: str) -> list[str]:
    info = LEDGER_KINDS[kind]
    allowed_statuses = set(info["blocking_statuses"]) | {
        "in-progress",
        "satisfied",
        "deferred-with-owner",
        "superseded",
        "pass",
        "fail",
    }
    issues: list[str] = []
    status = str(item.get("status", "")).lower()
    severity = str(item.get("severity", "medium")).lower()
    if status and status not in allowed_statuses:
        issues.append(f"unknown status '{item.get('status')}'")
    if severity not in {"low", "medium", "high", "critical"}:
        issues.append(f"unknown severity '{item.get('severity')}'")
    for field in info["required_fields"]:
        if missing_quality_value(field, item.get(field)):
            issues.append(f"missing required field '{field}'")
    if status == "satisfied" and missing_quality_value("proof", item.get("proof")):
        issues.append("satisfied item lacks closure proof")
    if status == "deferred-with-owner":
        if missing_quality_value("owner", item.get("owner")):
            issues.append("deferred item lacks owner")
        if missing_quality_value("recheck", item.get("recheck")):
            issues.append("deferred item lacks recheck command or trigger")
    return issues


def ledger_check(data: dict[str, Any], kind: str) -> dict[str, Any]:
    info = LEDGER_KINDS[kind]
    blocking_statuses = set(info["blocking_statuses"])
    items = data.get("items", [])
    quality_issues = [
        {
            "id": item.get("id", ""),
            "severity": item.get("severity", "medium"),
            "status": item.get("status", ""),
            "issues": ledger_item_quality_issues(item, kind),
        }
        for item in items
        if ledger_item_quality_issues(item, kind)
    ]
    blocker_ids = {
        issue["id"]
        for issue in quality_issues
        if str(issue.get("severity", "medium")).lower() in {"critical", "high", "medium"}
    }
    blockers = []
    for item in items:
        severity = str(item.get("severity", "medium")).lower()
        status = str(item.get("status", "")).lower()
        if severity in {"critical", "high", "medium"} and (status in blocking_statuses or item.get("id") in blocker_ids):
            blockers.append(item)
    critical = [item for item in blockers if str(item.get("severity", "")).lower() == "critical"]
    if critical:
        outcome = "BLOCK"
    elif blockers:
        outcome = "HOLD"
    else:
        outcome = "PASS"
    return {
        "kind": kind,
        "outcome": outcome,
        "item_count": len(items),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "quality_issue_count": len(quality_issues),
        "quality_issues": quality_issues,
    }


def render_ledger_md(data: dict[str, Any]) -> str:
    kind = data.get("kind", "ledger")
    lines = [f"# {kind.title()} Ledger", "", f"Updated: {data.get('updated_at', '')}", ""]
    items = data.get("items", [])
    if not items:
        lines.append("No items.")
        lines.append("")
        return "\n".join(lines)
    lines.append("| ID | Status | Severity | Summary | Owner | Evidence | Proof | Recheck |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for item in items:
        lines.append(
            "| {id} | {status} | {severity} | {summary} | {owner} | {evidence} | {proof} | {recheck} |".format(
                id=item.get("id", ""),
                status=item.get("status", ""),
                severity=item.get("severity", ""),
                summary=str(item.get("summary", "")).replace("|", "\\|"),
                owner=item.get("owner", ""),
                evidence=str(item.get("evidence", "")).replace("|", "\\|"),
                proof=str(item.get("proof", "")).replace("|", "\\|"),
                recheck=str(item.get("recheck", "")).replace("|", "\\|"),
            )
        )
    lines.append("")
    return "\n".join(lines)


def context_payload(root: pathlib.Path, include_history: bool, max_history: int) -> dict[str, Any]:
    state = ensure_state(root)
    active = state.get("active", {})
    workflow_key = active.get("workflow")
    if workflow_key not in WORKFLOW_REGISTRY:
        raise SystemExit(
            f"Error: state has unknown active.workflow '{workflow_key}'.\n"
            "Repair with: church state set active.workflow <known-workflow>"
        )
    workflow = WORKFLOW_REGISTRY[workflow_key]
    moat_score = None
    moat_path = moat_dir(root) / "moat.json"
    if moat_path.exists():
        moat_score = score_moat(load_json(moat_path))
    ledgers = {}
    for kind in LEDGER_KINDS:
        data = load_ledger(root, kind)
        ledgers[kind] = ledger_check(data, kind)
    payload = {
        "state_path": str(state_path(root)),
        "active": active,
        "workflow": workflow,
        "required_artifacts": workflow.get("required_artifacts", []),
        "next_workflows": workflow.get("next", []),
        "artifacts": state.get("artifacts", {}),
        "signoff": state.get("signoff", {}),
        "moat_score": moat_score,
        "ledger_status": ledgers,
    }
    if include_history:
        payload["history"] = state.get("history", [])[-max_history:]
    return payload


def lifecycle_quality_check(
    root: pathlib.Path,
    data: dict[str, Any],
    workflow_key: str,
    outcome: str,
    artifact_updates: dict[str, str],
    evidence: str | None,
) -> dict[str, Any]:
    if outcome not in PASSING_OUTCOMES:
        return {"checked": False, "blockers": [], "warnings": [], "reason": "outcome is not passing"}

    artifacts = dict(data.get("artifacts", {}))
    artifacts.update(artifact_updates)
    blockers: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if missing_quality_value("evidence", evidence):
        blockers.append({
            "check": "gate-evidence",
            "message": "passing gate outcomes require --evidence with proof, artifact, or recheck source",
        })

    workflow = WORKFLOW_REGISTRY[workflow_key]
    for artifact in workflow.get("required_artifacts", []):
        value = artifacts.get(artifact)
        if missing_quality_value(artifact, value):
            blockers.append({
                "check": "required-artifact",
                "message": f"required artifact '{artifact}' is not registered",
            })
            continue
        artifact_path = pathlib.Path(str(value))
        if not artifact_path.is_absolute() and not (root / artifact_path).exists():
            warnings.append({
                "check": "artifact-existence",
                "message": f"registered artifact '{artifact}' does not exist at {value}",
            })

    current_workflow = data.get("active", {}).get("workflow")
    if workflow_key == "moat" or (current_workflow == "moat" and workflow_key != "moat"):
        moat_path = moat_dir(root) / "moat.json"
        if not moat_path.exists():
            blockers.append({"check": "moat-score", "message": "moat.json is missing"})
        else:
            score = score_moat(load_json(moat_path))
            if score["outcome"] not in PASSING_OUTCOMES:
                blockers.append({
                    "check": "moat-score",
                    "message": f"moat score is {score['outcome']} with coverage {score['coverage']}",
                })

    for kind in LEDGER_KINDS:
        result = ledger_check(load_ledger(root, kind), kind)
        if result["outcome"] not in PASSING_OUTCOMES:
            blockers.append({
                "check": f"{kind}-ledger",
                "message": f"{kind} ledger is {result['outcome']} with {result['blocker_count']} blockers",
            })

    signoff = data.get("signoff", {})
    if workflow_key in {"uat", "ship"} and signoff.get("mutual_required"):
        if not signoff.get("agent") or not signoff.get("user"):
            blockers.append({
                "check": "mutual-signoff",
                "message": "mutual signoff is required but agent/user signoff is incomplete",
            })

    return {"checked": True, "blockers": blockers, "warnings": warnings}


def format_quality_blockers(check: dict[str, Any]) -> str:
    lines = ["Error: passing gate outcome failed quality checks."]
    for issue in check.get("blockers", []):
        lines.append(f"- {issue['check']}: {issue['message']}")
    if check.get("warnings"):
        lines.append("Warnings:")
        for warning in check["warnings"]:
            lines.append(f"- {warning['check']}: {warning['message']}")
    lines.append(
        "Use HOLD/BLOCK, add missing evidence/artifacts, or pass "
        "--allow-quality-risk only for an explicitly accepted non-critical exception."
    )
    return "\n".join(lines)


def run_church_capture(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(pathlib.Path(__file__).resolve()), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def write_artifact(root: pathlib.Path, rel_path: str, text: str) -> pathlib.Path:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def seed_bible_from_evidence_root(root: pathlib.Path, evidence_root: pathlib.Path) -> None:
    source = evidence_root / DEFAULT_BIBLE_DIR
    target = root / DEFAULT_BIBLE_DIR
    if source == target or not source.exists():
        return
    target.mkdir(parents=True, exist_ok=True)
    for source_path in source.glob("*.md"):
        if source_path.name.startswith("_repo-bible-"):
            continue
        (target / source_path.name).write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def proof_moat(project_name: str, evidence_root: pathlib.Path) -> dict[str, Any]:
    moat = moat_template(project_name)
    moat.update({
        "elevator_pitch": (
            "Repo Church turns agentic repository work into a Bible-backed lifecycle with deterministic gates, "
            "evidence ledgers, specialist contracts, and ship-ready handoffs."
        ),
        "third_party_summary": (
            "Repo Church is a portable skills package and CLI that helps coding agents plan, verify, ship, "
            "and refresh repository work without losing traceability between sessions."
        ),
        "one_sentence_moat": (
            "Its moat is the compounding repo-local doctrine, deterministic lifecycle state, proof-bearing "
            "ledgers, and installable agent skill contracts that make quality gates executable."
        ),
    })
    moat["market"].update({
        "category": "agent workflow governance",
        "buyer": "agent-heavy repo owners and technical operators",
        "user": "coding agents, skill authors, and repo maintainers",
        "urgent_pain": "agent work can drift from requirements, skip proof, and become hard to resume or review",
        "why_now": "agentic coding adoption makes durable repo-local process and evidence more valuable than one-off prompts",
    })
    moat["competition"].update({
        "direct": ["ad hoc agent planning prompts", "repo-local workflow scripts"],
        "adjacent": ["task runners", "AI coding IDE rules", "project management checklists"],
        "status_quo": ["manual planning docs", "unstructured PR review", "session-specific handoffs"],
        "substitutes": ["plain README instructions", "single-agent memory files"],
    })
    moat["wedge"].update({
        "entry_point": "installable repo lifecycle skill package with deterministic CLI validation",
        "first_10_users": "builders who repeatedly use agents for multi-phase repository work",
        "switching_trigger": "a resumed session or PR needs proof that requirements, evidence, UAT, and ship gates were satisfied",
        "time_to_value": "first init plus context load produces state, moat, Bible scaffold, and next workflow in one session",
    })
    moat["leverage"].update({
        "primary_source": "repo-local lifecycle artifacts that compound across phases",
        "secondary_sources": ["deterministic CLI checks", "specialist profile contracts", "Bible packet templates", "Python regression tests"],
        "what_compounds_with_use": "requirements, ledgers, evidence, handoffs, validation reports, and refresh records become reusable context",
        "what_gets_harder_to_copy": "the interaction between portable skills, deterministic state, quality gates, and accumulated project doctrine",
    })
    moat["sustainability"].update({
        "defensibility": "trust from repeatable proof that gates reject unsupported progress",
        "switching_costs": "repo history, Bible requirements, ledgers, and handoffs become embedded in the project workflow",
        "distribution_advantage": "skills.sh-compatible package with staged commands and specialist profiles",
        "data_or_learning_loop": "each phase refreshes requirements, gaps, validation evidence, and next-phase anchors",
        "ecosystem_lock_in": "low vendor lock-in by design; lock-in comes from useful repo-local artifacts",
        "trust_or_compliance": "explicit evidence, owner, proof, and recheck fields support auditability",
    })
    moat["proof"].update({
        "local_evidence": [
            f"{evidence_root / 'README.md'} documents the installable lifecycle and core loop",
            f"{evidence_root / 'skills/church/scripts/church.py'} implements state, moat, ledger, context, lifecycle, and quality checks",
            f"{evidence_root / 'tests/test_church_cli.py'} verifies CLI behavior and failure-mode guardrails",
            f"{evidence_root / 'tests/test_church_plugin_assets.py'} verifies staged command and specialist profile assets",
        ],
        "market_evidence": [
            "Local repo evidence supports the agent workflow governance category; current external competitor research is a refresh task"
        ],
        "customer_evidence": [
            "The self-hosted meta lifecycle request requires Repo Church to prove it can govern itself end to end"
        ],
        "missing_evidence": [
            "Current dated competitor research for public positioning",
            "Third-party user adoption data beyond this local repository",
        ],
    })
    moat["risks"] = [
        "Ceremony without enforcement if lifecycle gates are not tested end to end",
        "Overclaiming market moat without current competitor research",
        "Context bloat if Bible artifacts are not paired with deterministic summaries",
    ]
    moat["validation_tests"] = [
        "church lifecycle prove reaches refresh PASS without --force or --allow-quality-risk",
        "tests/test_church_cli.py proves weak PASS records and proofless closure are rejected",
        "npx skills add ./ --list proves install surface exposes the intended skills",
    ]
    moat["scorecard"] = {
        "clarity": 4,
        "urgency": 4,
        "differentiation": 4,
        "durability": 4,
        "evidence": 4,
        "third_party_comprehension": 4,
    }
    return moat


def render_handoff(root: pathlib.Path, fmt: str = "markdown") -> str | dict[str, Any]:
    payload = context_payload(root, include_history=True, max_history=8)
    active = payload["active"]
    if fmt == "json":
        return payload
    lines = [
        "# Repo Church Handoff",
        "",
        f"- Workflow: {active.get('workflow')}",
        f"- Stage: {active.get('stage')}",
        f"- Gate: {active.get('gate')}",
        f"- Outcome: {active.get('outcome')}",
        f"- Phase: {active.get('phase')}",
        f"- Milestone: {active.get('milestone')}",
        "",
        "## Required Artifacts",
    ]
    for artifact in payload.get("required_artifacts", []):
        lines.append(f"- {artifact}: {payload.get('artifacts', {}).get(artifact, 'not registered')}")
    lines.extend(["", "## Next Workflows"])
    for workflow in payload.get("next_workflows", []):
        info = WORKFLOW_REGISTRY.get(workflow, {})
        lines.append(f"- {workflow}: {info.get('skill', 'unknown skill')}")
    lines.extend(["", "## Ledger Status"])
    for kind, status in payload.get("ledger_status", {}).items():
        lines.append(f"- {kind}: {status['outcome']} ({status['blocker_count']} blockers)")
    lines.extend(["", "## Next", "Use the active workflow, gate outcome, and ledger blockers to choose the next Repo Church skill."])
    lines.append("")
    return "\n".join(lines)


def cmd_init(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = ensure_state(root)
    data["history"].append({"event": "init", "at": now_iso(), "mode": args.mode})
    moat_result: dict[str, Any] | None = None
    if args.moat:
        moat_result = create_moat(root, args.project_name or root.name, force=False)
        data["artifacts"]["moat_json"] = relative_to_root(root, moat_dir(root) / "moat.json")
        data["artifacts"]["moat_md"] = relative_to_root(root, moat_dir(root) / "moat.md")
        data["active"].update({
            "workflow": "moat",
            "stage": WORKFLOW_REGISTRY["moat"]["default_stage"],
            "gate": WORKFLOW_REGISTRY["moat"]["gate"],
            "outcome": "HOLD",
        })
        data["history"].append({"event": "moat.init", "at": now_iso()})
    scaffold_result = None
    if args.scaffold_bible:
        result = run_bible_capture(["scaffold", "--root", str(root)])
        scaffold_result = {
            "command": "church bible scaffold",
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
        if result.returncode != 0:
            emit({"state": str(state_path(root)), "mode": args.mode, "moat": moat_result, "bible_scaffold": scaffold_result}, args.format, "Repo Church Init")
            return result.returncode
    save_state(root, data)
    emit({"state": str(state_path(root)), "mode": args.mode, "moat": moat_result, "bible_scaffold": scaffold_result}, args.format, "Repo Church Init")
    return 0


def cmd_registry_list(args: argparse.Namespace) -> int:
    summary = [
        {
            "workflow": name,
            "stage": info["default_stage"],
            "gate": info["gate"],
            "skill": info["skill"],
            "next": info["next"],
        }
        for name, info in WORKFLOW_REGISTRY.items()
    ]
    emit(summary, args.format, "Repo Church Workflow Registry")
    return 0


def cmd_registry_show(args: argparse.Namespace) -> int:
    if args.workflow not in WORKFLOW_REGISTRY:
        print(f"Error: unknown workflow '{args.workflow}'. Example: church registry show moat", file=sys.stderr)
        return 1
    emit({args.workflow: WORKFLOW_REGISTRY[args.workflow]}, args.format, "Repo Church Workflow")
    return 0


def cmd_registry_keys(args: argparse.Namespace) -> int:
    emit(STATE_KEY_REGISTRY, args.format, "Repo Church State Keys")
    return 0


def cmd_registry_reasoning(args: argparse.Namespace) -> int:
    if args.workflow:
        emit({args.workflow: REASONING_BOUNDARIES[args.workflow]}, args.format, "Repo Church Reasoning Boundary")
    else:
        emit(REASONING_BOUNDARIES, args.format, "Repo Church Reasoning Boundaries")
    return 0


def cmd_state_show(args: argparse.Namespace) -> int:
    emit(ensure_state(repo_root(args.root)), args.format, "Repo Church State")
    return 0


def cmd_state_get(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = ensure_state(root)
    try:
        value = get_path(data, args.key)
    except KeyError:
        print(f"Error: missing key '{args.key}'. Example: church registry keys", file=sys.stderr)
        return 1
    emit(value, args.format, "Repo Church State Value")
    return 0


def cmd_state_set(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = ensure_state(root)
    value = coerce_value(args.value)
    validate_state_set(args.key, value)
    set_path(data, args.key, value)
    data["history"].append({"event": "state.set", "at": now_iso(), "key": args.key})
    save_state(root, data)
    emit({"updated": args.key, "state": str(state_path(root))}, args.format, "Repo Church State Update")
    return 0


def cmd_moat_init(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    result = create_moat(root, args.project_name or root.name, args.force)
    data = ensure_state(root)
    data["artifacts"]["moat_json"] = relative_to_root(root, moat_dir(root) / "moat.json")
    data["artifacts"]["moat_md"] = relative_to_root(root, moat_dir(root) / "moat.md")
    data["active"].update({
        "workflow": "moat",
        "stage": WORKFLOW_REGISTRY["moat"]["default_stage"],
        "gate": WORKFLOW_REGISTRY["moat"]["gate"],
        "outcome": "HOLD",
    })
    data["history"].append({"event": "moat.init", "at": now_iso()})
    save_state(root, data)
    emit(result, args.format, "Repo Church Moat Init")
    return 0


def cmd_moat_set(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    _, moat = load_moat(root, args.input)
    set_path(moat, args.key, coerce_value(args.value))
    path = save_moat(root, moat, args.output)
    emit({"updated": args.key, "moat_json": str(path)}, args.format, "Repo Church Moat Update")
    return 0


def cmd_moat_import(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    if not args.stdin and not args.input:
        print(
            "Error: moat import requires --stdin or --input <file>.\n"
            f"Example: cat moat.json | church moat import --root {root} --stdin --merge",
            file=sys.stderr,
        )
        return 1
    incoming = read_stdin_json() if args.stdin else load_json(pathlib.Path(args.input).expanduser().resolve())
    _, existing = load_moat(root) if (moat_dir(root) / "moat.json").exists() and args.merge else (None, {})
    moat = merge_dict(existing, incoming) if args.merge else incoming
    if "schema_version" not in moat:
        moat["schema_version"] = MOAT_SCHEMA_VERSION
    path = save_moat(root, moat)
    md_path = moat_dir(root) / "moat.md"
    md_path.write_text(render_moat_md(moat), encoding="utf-8")
    emit({"moat_json": str(path), "moat_md": str(md_path), "merged": args.merge}, args.format, "Repo Church Moat Import")
    return 0


def cmd_moat_export(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    _, moat = load_moat(root, args.input)
    if args.output:
        path = pathlib.Path(args.output).expanduser().resolve()
        if args.format == "json":
            write_json(path, moat)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render_moat_md(moat), encoding="utf-8")
        emit({"output": str(path)}, "json", "Repo Church Moat Export")
    else:
        if args.format == "json":
            emit_json(moat)
        else:
            print(render_moat_md(moat))
    return 0


def cmd_moat_render(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    _, moat = load_moat(root, args.input)
    md_path = pathlib.Path(args.output).expanduser().resolve() if args.output else moat_dir(root) / "moat.md"
    moat["updated_at"] = now_iso()
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_moat_md(moat), encoding="utf-8")
    emit({"moat_md": str(md_path)}, args.format, "Repo Church Moat Render")
    return 0


def cmd_moat_check(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    _, moat = load_moat(root, args.input)
    result = score_moat(moat)
    data = ensure_state(root)
    data["active"].update({"workflow": "moat", "gate": "moat", "outcome": result["outcome"]})
    data["history"].append({"event": "moat.check", "at": now_iso(), "outcome": result["outcome"]})
    save_state(root, data)
    emit(result, args.format, "Repo Church Moat Check")
    return 0 if args.allow_incomplete or result["outcome"] in PASSING_OUTCOMES else 1


def cmd_lifecycle_list(args: argparse.Namespace) -> int:
    return cmd_registry_list(args)


def cmd_lifecycle_show(args: argparse.Namespace) -> int:
    return cmd_registry_show(args)


def cmd_lifecycle_status(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    emit(context_payload(root, args.include_history, args.max_history), args.format, "Repo Church Lifecycle Status")
    return 0


def cmd_lifecycle_advance(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = ensure_state(root)
    current = data.get("active", {}).get("workflow", "init")
    artifact_updates = parse_artifact_updates(args.artifact)
    allowed = set(WORKFLOW_REGISTRY.get(current, {}).get("next", []))
    if args.workflow != current and args.workflow not in allowed and not args.force:
        print(
            f"Error: cannot advance from '{current}' to '{args.workflow}' without --force.\n"
            f"Allowed next workflows: {', '.join(sorted(allowed)) or '(none)'}\n"
            f"Example: church lifecycle advance {next(iter(allowed), args.workflow)} --root {root}",
            file=sys.stderr,
        )
        return 1
    info = WORKFLOW_REGISTRY[args.workflow]
    proposed_active = dict(data["active"])
    proposed_active.update({
        "workflow": args.workflow,
        "stage": args.stage or info["default_stage"],
        "gate": args.gate or info["gate"],
        "outcome": args.outcome,
    })
    if args.phase is not None:
        proposed_active["phase"] = args.phase
    if args.milestone is not None:
        proposed_active["milestone"] = args.milestone
    quality_check = lifecycle_quality_check(root, data, args.workflow, args.outcome, artifact_updates, args.evidence)
    if args.dry_run:
        emit({
            "dry_run": True,
            "active": proposed_active,
            "would_register_artifacts": artifact_updates,
            "quality_check": quality_check,
        }, args.format, "Repo Church Lifecycle Advance Preview")
        return 0
    if quality_check.get("blockers") and not args.allow_quality_risk:
        print(format_quality_blockers(quality_check), file=sys.stderr)
        return 1
    data["active"].update({
        "workflow": args.workflow,
        "stage": args.stage or info["default_stage"],
        "gate": args.gate or info["gate"],
        "outcome": args.outcome,
    })
    if args.phase is not None:
        data["active"]["phase"] = args.phase
    if args.milestone is not None:
        data["active"]["milestone"] = args.milestone
    for key, value in artifact_updates.items():
        data["artifacts"][key] = value
    event = {"event": "lifecycle.advance", "at": now_iso(), "workflow": args.workflow, "outcome": args.outcome}
    if args.evidence:
        event["evidence"] = args.evidence
    if args.force:
        event["forced"] = True
    if args.allow_quality_risk:
        event["quality_risk_accepted"] = True
        event["quality_check"] = quality_check
    data["history"].append(event)
    save_state(root, data)
    emit({"active": data["active"], "state": str(state_path(root)), "quality_check": quality_check}, args.format, "Repo Church Lifecycle Advance")
    return 0


def cmd_lifecycle_handoff(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    result = render_handoff(root, args.format)
    if args.output:
        path = pathlib.Path(args.output).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(result, indent=2, sort_keys=True) + "\n" if args.format == "json" else str(result)
        path.write_text(text, encoding="utf-8")
        data = ensure_state(root)
        data["artifacts"]["handoff"] = relative_to_root(root, path)
        data["history"].append({"event": "lifecycle.handoff", "at": now_iso(), "output": relative_to_root(root, path)})
        save_state(root, data)
        emit({"handoff": str(path)}, "json", "Repo Church Handoff")
    else:
        if args.format == "json":
            emit_json(result)
        else:
            print(result)
    return 0


def cmd_lifecycle_prove(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    evidence_root = repo_root(args.self_package or args.root)
    project_name = args.project_name or root.name
    proof_dir = root / DEFAULT_CHURCH_ROOT / "proof"
    proof_dir.mkdir(parents=True, exist_ok=True)
    commands: list[dict[str, Any]] = []

    def run_step(label: str, argv: list[str], allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
        result = run_church_capture(argv)
        commands.append({
            "label": label,
            "argv": ["church", *argv],
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        })
        if result.returncode != 0 and not allow_failure:
            raise SystemExit(f"Error: lifecycle prove failed at {label}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result

    def run_external_step(
        label: str,
        argv: list[str],
        cwd: pathlib.Path,
        allow_failure: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            argv,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "CHURCH_PYTHON": sys.executable, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        commands.append({
            "label": label,
            "argv": argv,
            "cwd": str(cwd),
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        })
        if result.returncode != 0 and not allow_failure:
            raise SystemExit(f"Error: lifecycle prove failed at {label}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result

    run_step("init", ["init", "--root", str(root), "--mode", args.mode, "--project-name", project_name, "--scaffold-bible", "--format", "json"])
    seed_bible_from_evidence_root(root, evidence_root)

    moat_path = moat_dir(root) / "moat.json"
    if not moat_path.exists() or score_moat(load_json(moat_path))["outcome"] not in PASSING_OUTCOMES:
        moat = proof_moat(project_name, evidence_root)
        save_moat(root, moat)
        (moat_dir(root) / "moat.md").write_text(render_moat_md(moat), encoding="utf-8")
    run_step("moat-render", ["moat", "render", "--root", str(root), "--format", "json"])
    run_step("moat-check", ["moat", "check", "--root", str(root), "--format", "json"])
    run_step("advance-moat", ["lifecycle", "advance", "moat", "--root", str(root), "--outcome", "PASS", "--evidence", ".church/moat/moat.md", "--format", "json"])

    bible_dir = root / DEFAULT_BIBLE_DIR
    report_paths = {
        "inventory": bible_dir / "_repo-bible-inventory.md",
        "sources": bible_dir / "_repo-bible-sources.md",
        "claim_scan": bible_dir / "_repo-bible-claim-scan.md",
        "validation": bible_dir / "_repo-bible-validation.md",
    }
    evidence_excludes = [
        "--exclude", ".church",
        "--exclude", ".church/**",
    ]
    bible_commands = [
        ("bible-inventory", ["bible", "inventory", "--root", str(evidence_root), *evidence_excludes, "--format", "markdown", "--output", str(report_paths["inventory"])]),
        ("bible-sources", ["bible", "sources", "--root", str(root), "--follow-local-md", "--format", "markdown", "--output", str(report_paths["sources"])]),
        ("bible-claim-scan", ["bible", "claim-scan", "--root", str(evidence_root), "--path", str(evidence_root), *evidence_excludes, "--required", "Repo Church", "--format", "markdown", "--output", str(report_paths["claim_scan"])]),
        ("bible-validate", ["bible", "validate", "--root", str(root), "--follow-local-md", "--format", "markdown", "--output", str(report_paths["validation"])]),
        ("bible-render-html", ["bible", "render-html", "--root", str(root), "--output", str(bible_dir / "html")]),
    ]
    for label, argv in bible_commands:
        run_step(label, argv)
    validation_json = run_step("bible-validate-json", [
        "bible", "validate",
        "--root", str(root),
        "--follow-local-md",
        "--format", "json",
        "--output", "-",
    ])
    validation_data = json.loads(validation_json.stdout)
    if validation_data.get("error_count") or validation_data.get("warning_count"):
        raise SystemExit(
            "Error: lifecycle prove requires clean Bible validation "
            f"(errors={validation_data.get('error_count')}, warnings={validation_data.get('warning_count')})."
        )
    run_step("advance-bible", ["lifecycle", "advance", "bible", "--root", str(root), "--outcome", "PASS", "--evidence", ".church/bible/_repo-bible-validation.md", "--artifact", "bible_packet=.church/bible/", "--format", "json"])

    survey_path = write_artifact(root, ".church/survey/codebase-survey.md", f"""# Codebase Survey

Evidence root: `{evidence_root}`

## Findings

- Lifecycle registry, CLI, commands, agents, Repo Bible CLI, tests, and package manifest are present.
- Inventory report is registered as `.church/bible/_repo-bible-inventory.md`.
- Full lifecycle proof must exercise every canonical workflow without `--force`.
""")
    run_step("advance-survey", ["lifecycle", "advance", "survey", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, survey_path), "--artifact", "bible_inventory=.church/bible/_repo-bible-inventory.md", "--format", "json"])

    run_step("ledger-init-assumptions", ["ledger", "init", "assumptions", "--root", str(root), "--format", "json"])
    run_step("ledger-add-assumption", [
        "ledger", "add", "assumptions", "--root", str(root),
        "--id", "A-META-001",
        "--summary", "Full lifecycle proof is the hard evidence needed for self-hosting readiness",
        "--status", "satisfied",
        "--evidence", ".church/proof/lifecycle-proof.json",
        "--owner", "agent",
        "--proof", "lifecycle prove reaches refresh PASS",
        "--acceptance-test", "tests/test_church_meta_lifecycle.py",
        "--recheck", "church lifecycle prove --root <repo>",
        "--extra", "confidence=verified-local",
        "--replace",
        "--format", "json",
    ])
    run_step("advance-harden", ["lifecycle", "advance", "harden", "--root", str(root), "--outcome", "PASS", "--evidence", ".church/ledgers/assumptions.json", "--artifact", "assumption_ledger=.church/ledgers/assumptions.json", "--format", "json"])

    anchor_path = write_artifact(root, ".church/anchors/meta-lifecycle-anchor.md", """# Meta Lifecycle Anchor

Phase: P01 Self-Hosted Lifecycle Proof

Objective: prove Repo Church can govern itself through every canonical lifecycle gate with evidence-backed state transitions.

Requirements: SR-01, SR-02, SR-03, SR-04, SR-05.

Acceptance: full lifecycle proof reaches `refresh/PASS`; tests and package validation pass; generated proof artifact records every stage.
""")
    run_step("advance-anchor", ["lifecycle", "advance", "anchor", "--root", str(root), "--outcome", "PASS", "--phase", "P01", "--evidence", relative_to_root(root, anchor_path), "--artifact", "phase_anchor=.church/anchors/meta-lifecycle-anchor.md", "--format", "json"])

    spec_path = write_artifact(root, ".church/specs/meta-lifecycle-spec.md", """# Meta Lifecycle Spec

## Scope

Add deterministic proof that Repo Church can run its own lifecycle from moat through refresh without bypass flags.

## Requirements

| Requirement | Implementation | Verification |
|---|---|---|
| SR-01 | `church lifecycle prove` and `tests/test_church_meta_lifecycle.py` | Test reaches `refresh/PASS` |
| SR-02 | Existing quality checks stay active during proof | No `--force` or `--allow-quality-risk` in proof steps |
| SR-03 | Moat imports local evidence and validation tests | `church moat check` returns PASS |
| SR-05 | Proof registers required artifacts | Proof JSON lists stages and artifact paths |
""")
    run_step("advance-spec", ["lifecycle", "advance", "spec-gate", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, spec_path), "--artifact", "spec_gate=.church/specs/meta-lifecycle-spec.md", "--format", "json"])

    run_step("ledger-init-gaps", ["ledger", "init", "gaps", "--root", str(root), "--format", "json"])
    run_step("ledger-add-gap", [
        "ledger", "add", "gaps", "--root", str(root),
        "--id", "GAP-META-001",
        "--summary", "Full lifecycle proof was absent before this meta run",
        "--status", "satisfied",
        "--severity", "high",
        "--evidence", ".church/bible/alignment-audit.md",
        "--owner", "agent",
        "--proof", "lifecycle prove command and regression test close the proof gap",
        "--acceptance-test", "tests/test_church_meta_lifecycle.py",
        "--recheck", "python3 tests/test_church_meta_lifecycle.py",
        "--replace",
        "--format", "json",
    ])
    gap_path = write_artifact(root, ".church/gaps/meta-gap-closure.md", "# Meta Gap Closure\n\nGAP-META-001 is closed by the lifecycle proof command and regression test.\n")
    run_step("advance-gap", ["lifecycle", "advance", "gap-closure", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, gap_path), "--artifact", "gap_ledger=.church/ledgers/gaps.json", "--format", "json"])

    handoff_path = write_artifact(root, ".church/handoff/meta-lifecycle-handoff.md", "# Meta Lifecycle Handoff\n\nScope is frozen to P01: prove full self-hosted lifecycle and validate the package. Next executor should run the validation commands in `.church/bible/validation-report.md`.\n")
    run_step("advance-handoff", ["lifecycle", "advance", "handoff", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, handoff_path), "--artifact", "handoff=.church/handoff/meta-lifecycle-handoff.md", "--format", "json"])

    run_step("ledger-init-uat", ["ledger", "init", "uat", "--root", str(root), "--format", "json"])
    run_step("ledger-add-uat", [
        "ledger", "add", "uat", "--root", str(root),
        "--id", "UAT-META-001",
        "--summary", "Full lifecycle proof reaches refresh PASS",
        "--status", "satisfied",
        "--evidence", ".church/proof/lifecycle-proof.json",
        "--owner", "agent",
        "--proof", "proof artifact records every canonical stage",
        "--acceptance-test", "tests/test_church_meta_lifecycle.py",
        "--recheck", "church lifecycle prove --root <repo>",
        "--extra", "result=pass",
        "--replace",
        "--format", "json",
    ])
    run_step("signoff-agent", ["state", "set", "signoff.agent", "true", "--root", str(root), "--format", "json"])
    uat_path = write_artifact(root, ".church/uat/meta-uat.md", """# Meta UAT

Agent signoff: yes.
User signoff: not required for this non-destructive proof command.
Result: PASS.

## Must-Pass Evidence

- `.church/proof/lifecycle-proof.json` records the canonical workflow sequence through `refresh/PASS`.
- `tests/test_church_meta_lifecycle.py` verifies the proof command on an isolated temporary root.
- Ledger checks for assumptions, gaps, risks, and UAT return PASS with zero blockers.
""")
    run_step("advance-uat", ["lifecycle", "advance", "uat", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, uat_path), "--artifact", "uat_ledger=.church/ledgers/uat.json", "--format", "json"])

    ship_path = write_artifact(root, ".church/ship/meta-ship-gate.md", """# Meta Ship Gate

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
""")
    run_external_step("ship-package-validator", ["bash", "skills/church/scripts/validate-package.sh", "."], evidence_root)
    run_external_step("ship-cli-tests", [sys.executable, "tests/test_church_cli.py"], evidence_root)
    run_external_step("ship-plugin-assets", [sys.executable, "tests/test_church_plugin_assets.py"], evidence_root)
    run_external_step("ship-install-smoke", ["npx", "skills", "add", "./", "--list"], evidence_root)
    run_step("advance-ship", ["lifecycle", "advance", "ship", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, ship_path), "--artifact", "ship_gate=.church/ship/meta-ship-gate.md", "--format", "json"])

    refresh_path = write_artifact(root, ".church/refresh/meta-refresh-record.md", """# Meta Refresh Record

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
""")
    run_step("advance-refresh", ["lifecycle", "advance", "refresh", "--root", str(root), "--outcome", "PASS", "--evidence", relative_to_root(root, refresh_path), "--artifact", "refresh_record=.church/refresh/meta-refresh-record.md", "--format", "json"])

    final_status = context_payload(root, include_history=True, max_history=32)
    proof = {
        "schema_version": "church-lifecycle-proof/v1",
        "root": str(root),
        "evidence_root": str(evidence_root),
        "project_name": project_name,
        "created_at": now_iso(),
        "commands": commands,
        "final_status": final_status,
        "repo_bible_commands": ["inventory", "sources", "claim-scan", "validate", "render-html"],
        "canonical_pass_workflows": [
            "moat", "bible", "survey", "harden", "anchor", "spec-gate",
            "gap-closure", "handoff", "uat", "ship", "refresh",
        ],
    }
    proof_path = proof_dir / "lifecycle-proof.json"
    write_json(proof_path, proof)
    emit({"proof": str(proof_path), "final_active": final_status["active"], "commands": len(commands)}, args.format, "Repo Church Lifecycle Proof")
    return 0


def cmd_ledger_init(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    path = ledger_path(root, args.kind)
    if path.exists() and not args.force:
        emit({"ledger": str(path), "exists": True, "reset": False}, args.format, "Repo Church Ledger Init")
        return 0
    data = empty_ledger(args.kind)
    path = save_ledger(root, args.kind, data)
    state = ensure_state(root)
    state["artifacts"][f"{args.kind.rstrip('s')}_ledger"] = relative_to_root(root, path)
    state["history"].append({"event": "ledger.init", "at": now_iso(), "kind": args.kind})
    save_state(root, state)
    emit({"ledger": str(path)}, args.format, "Repo Church Ledger Init")
    return 0


def cmd_ledger_add(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = load_ledger(root, args.kind)
    item = {
        "id": args.id,
        "status": args.status,
        "severity": args.severity,
        "summary": args.summary,
        "evidence": args.evidence,
        "owner": args.owner,
        "proof": args.proof,
        "acceptance_test": args.acceptance_test,
        "recheck": args.recheck,
        "blocks_progression": args.blocks_progression,
        "workflow": args.workflow,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    if args.extra:
        for pair in args.extra:
            if "=" not in pair:
                print("Error: --extra must use KEY=VALUE.\nExample: church ledger add gaps --extra file=PLAN.md", file=sys.stderr)
                return 1
            key, value = pair.split("=", 1)
            item[key] = coerce_value(value)
    existing_ids = {entry.get("id") for entry in data.get("items", [])}
    replace_existing = args.force or args.replace
    if item["id"] in existing_ids and not replace_existing:
        print(f"Error: ledger item '{item['id']}' already exists. Use --replace to refresh it or --force to replace it.", file=sys.stderr)
        return 1
    if item["id"] in existing_ids:
        data["items"] = [entry for entry in data["items"] if entry.get("id") != item["id"]]
    data.setdefault("items", []).append(item)
    path = save_ledger(root, args.kind, data)
    state = ensure_state(root)
    state["history"].append({"event": "ledger.add", "at": now_iso(), "kind": args.kind, "id": item["id"]})
    save_state(root, state)
    emit({"ledger": str(path), "item": item}, args.format, "Repo Church Ledger Add")
    return 0


def cmd_ledger_list(args: argparse.Namespace) -> int:
    data = load_ledger(repo_root(args.root), args.kind)
    if args.format == "markdown":
        print(render_ledger_md(data))
    else:
        emit_json(data)
    return 0


def cmd_ledger_check(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = load_ledger(root, args.kind)
    result = ledger_check(data, args.kind)
    emit(result, args.format, "Repo Church Ledger Check")
    return 0 if args.allow_open or result["outcome"] in PASSING_OUTCOMES else 1


def cmd_context_load(args: argparse.Namespace) -> int:
    payload = context_payload(repo_root(args.root), args.include_history, args.max_history)
    emit(payload, args.format, "Repo Church Context")
    return 0


def cmd_bible(args: argparse.Namespace) -> int:
    passthrough = ["--help"] if getattr(args, "bible_help", False) and not args.args else args.args or ["--help"]
    return run_bible(passthrough)


def cmd_workspace_list(args: argparse.Namespace) -> int:
    emit(load_registry(repo_root(args.root), "workspaces"), args.format, "Repo Church Workspaces")
    return 0


def cmd_workspace_create(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    item = {
        "name": args.name,
        "status": "active",
        "path": args.path or ".",
        "summary": args.summary or "",
        "owner": args.owner or "unassigned",
    }
    path, saved = upsert_registry_item(root, "workspaces", args.name, item, force=args.force)
    state = ensure_state(root)
    state.setdefault("active", {})["workspace"] = args.name
    state["artifacts"]["workspace_registry"] = relative_to_root(root, path)
    state["history"].append({"event": "workspace.create", "at": now_iso(), "name": args.name})
    save_state(root, state)
    emit({"registry": str(path), "workspace": saved}, args.format, "Repo Church Workspace Create")
    return 0


def cmd_workspace_status(args: argparse.Namespace) -> int:
    data = load_registry(repo_root(args.root), "workspaces")
    item = find_registry_item(data, args.name)
    if item is None:
        print(f"Error: workspace '{args.name}' not found.", file=sys.stderr)
        return 1
    emit(item, args.format, "Repo Church Workspace Status")
    return 0


def cmd_workspace_switch(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = load_registry(root, "workspaces")
    item = find_registry_item(data, args.name)
    if item is None:
        print(f"Error: workspace '{args.name}' not found.", file=sys.stderr)
        return 1
    state = ensure_state(root)
    state.setdefault("active", {})["workspace"] = args.name
    state["history"].append({"event": "workspace.switch", "at": now_iso(), "name": args.name})
    save_state(root, state)
    emit({"active_workspace": args.name, "workspace": item}, args.format, "Repo Church Workspace Switch")
    return 0


def cmd_workspace_complete(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    path, item = update_registry_item_status(root, "workspaces", args.name, "complete")
    state = ensure_state(root)
    state["history"].append({"event": "workspace.complete", "at": now_iso(), "name": args.name})
    save_state(root, state)
    emit({"registry": str(path), "workspace": item}, args.format, "Repo Church Workspace Complete")
    return 0


def cmd_thread_list(args: argparse.Namespace) -> int:
    emit(load_registry(repo_root(args.root), "threads"), args.format, "Repo Church Threads")
    return 0


def cmd_thread_create(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    item = {
        "name": args.name,
        "status": "active",
        "runtime": args.runtime or "unknown",
        "external_id": args.external_id or "",
        "summary": args.summary or "",
        "handoff": args.handoff or "",
    }
    path, saved = upsert_registry_item(root, "threads", args.name, item, force=args.force)
    state = ensure_state(root)
    state.setdefault("active", {})["thread"] = args.name
    state["artifacts"]["thread_registry"] = relative_to_root(root, path)
    state["history"].append({"event": "thread.create", "at": now_iso(), "name": args.name})
    save_state(root, state)
    emit({"registry": str(path), "thread": saved}, args.format, "Repo Church Thread Create")
    return 0


def cmd_thread_status(args: argparse.Namespace) -> int:
    data = load_registry(repo_root(args.root), "threads")
    item = find_registry_item(data, args.name)
    if item is None:
        print(f"Error: thread '{args.name}' not found.", file=sys.stderr)
        return 1
    emit(item, args.format, "Repo Church Thread Status")
    return 0


def cmd_thread_resume(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    data = load_registry(root, "threads")
    item = find_registry_item(data, args.name)
    if item is None:
        print(f"Error: thread '{args.name}' not found.", file=sys.stderr)
        return 1
    state = ensure_state(root)
    state.setdefault("active", {})["thread"] = args.name
    state["history"].append({"event": "thread.resume", "at": now_iso(), "name": args.name})
    save_state(root, state)
    emit({
        "thread": item,
        "next_command": f"church context load --root {root} --include-history --format markdown",
    }, args.format, "Repo Church Thread Resume")
    return 0


def cmd_thread_complete(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    path, item = update_registry_item_status(root, "threads", args.name, "complete")
    state = ensure_state(root)
    state["history"].append({"event": "thread.complete", "at": now_iso(), "name": args.name})
    save_state(root, state)
    emit({"registry": str(path), "thread": item}, args.format, "Repo Church Thread Complete")
    return 0


def cmd_inbox_add(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    item = {
        "id": args.id,
        "status": args.status,
        "kind": args.kind,
        "severity": args.severity,
        "summary": args.summary,
        "evidence": args.evidence or "",
        "owner": args.owner or "unassigned",
        "route": args.route or "",
    }
    path, saved = upsert_registry_item(root, "inbox", args.id, item, force=args.force)
    state = ensure_state(root)
    state["artifacts"]["inbox_registry"] = relative_to_root(root, path)
    state["history"].append({"event": "inbox.add", "at": now_iso(), "id": args.id, "kind": args.kind})
    save_state(root, state)
    emit({"registry": str(path), "item": saved}, args.format, "Repo Church Inbox Add")
    return 0


def cmd_inbox_list(args: argparse.Namespace) -> int:
    emit(load_registry(repo_root(args.root), "inbox"), args.format, "Repo Church Inbox")
    return 0


def cmd_inbox_check(args: argparse.Namespace) -> int:
    data = load_registry(repo_root(args.root), "inbox")
    open_items = [item for item in data.get("items", []) if str(item.get("status", "open")).lower() in {"open", "blocked", "untriaged"}]
    blockers = [item for item in open_items if str(item.get("severity", "medium")).lower() in {"critical", "high"}]
    result = {
        "outcome": "BLOCK" if any(str(item.get("severity", "")).lower() == "critical" for item in blockers) else ("HOLD" if blockers else "PASS"),
        "item_count": len(data.get("items", [])),
        "open_count": len(open_items),
        "blocker_count": len(blockers),
        "blockers": blockers,
    }
    emit(result, args.format, "Repo Church Inbox Check")
    return 0 if args.allow_open or result["outcome"] in PASSING_OUTCOMES else 1


def cmd_profile_init(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    profile = {
        "schema_version": "church-profile/v1",
        "subject": args.subject,
        "consent": bool(args.consent),
        "status": "active" if args.consent else "blocked",
        "purpose": args.purpose or "",
        "signals": {},
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    path = registry_path(root, "profile")
    if path.exists() and not args.force:
        print("Error: profile artifact already exists. Use --force to replace it.", file=sys.stderr)
        return 1
    write_json(path, profile)
    state = ensure_state(root)
    state["artifacts"]["profile_artifact"] = relative_to_root(root, path)
    state["history"].append({"event": "profile.init", "at": now_iso(), "subject": args.subject, "consent": bool(args.consent)})
    save_state(root, state)
    emit({"profile": str(path), "status": profile["status"], "consent": profile["consent"]}, args.format, "Repo Church Profile Init")
    return 0


def cmd_profile_set(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    path = registry_path(root, "profile")
    profile = load_json(path, default={"schema_version": "church-profile/v1", "signals": {}})
    if not profile.get("consent") and not args.force:
        print("Error: profile has no consent. Use profile init --consent or --force for non-behavioral project metadata.", file=sys.stderr)
        return 1
    set_path(profile.setdefault("signals", {}), args.key, coerce_value(args.value))
    profile["updated_at"] = now_iso()
    write_json(path, profile)
    emit({"profile": str(path), "updated": args.key}, args.format, "Repo Church Profile Set")
    return 0


def cmd_profile_export(args: argparse.Namespace) -> int:
    profile = load_json(registry_path(repo_root(args.root), "profile"))
    emit(profile, args.format, "Repo Church Profile")
    return 0


def cmd_profile_check(args: argparse.Namespace) -> int:
    profile = load_json(registry_path(repo_root(args.root), "profile"))
    result = {
        "outcome": "PASS" if profile.get("consent") else "BLOCK",
        "consent": bool(profile.get("consent")),
        "signal_count": len(profile.get("signals", {})),
        "status": profile.get("status", "unknown"),
    }
    emit(result, args.format, "Repo Church Profile Check")
    return 0 if args.allow_blocked or result["outcome"] in PASSING_OUTCOMES else 1


def cmd_sketch_register(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    item = {
        "id": args.id,
        "status": args.status,
        "path": args.path,
        "summary": args.summary,
        "requires_user_signoff": bool(args.requires_user_signoff),
        "evidence": args.evidence or "",
    }
    path, saved = upsert_registry_item(root, "sketches", args.id, item, force=args.force)
    state = ensure_state(root)
    state["artifacts"]["sketch_registry"] = relative_to_root(root, path)
    if args.requires_user_signoff:
        state.setdefault("signoff", {})["mutual_required"] = True
    state["history"].append({"event": "sketch.register", "at": now_iso(), "id": args.id})
    save_state(root, state)
    emit({"registry": str(path), "sketch": saved}, args.format, "Repo Church Sketch Register")
    return 0


def cmd_sketch_list(args: argparse.Namespace) -> int:
    emit(load_registry(repo_root(args.root), "sketches"), args.format, "Repo Church Sketches")
    return 0


def cmd_sketch_check(args: argparse.Namespace) -> int:
    data = load_registry(repo_root(args.root), "sketches")
    blockers = [
        item for item in data.get("items", [])
        if item.get("requires_user_signoff") and str(item.get("status", "open")).lower() not in {"accepted", "superseded"}
    ]
    result = {
        "outcome": "HOLD" if blockers else "PASS",
        "item_count": len(data.get("items", [])),
        "signoff_blockers": blockers,
    }
    emit(result, args.format, "Repo Church Sketch Check")
    return 0 if args.allow_open or result["outcome"] in PASSING_OUTCOMES else 1


def detect_runtime(root: pathlib.Path, runtime: str) -> list[str]:
    if runtime != "auto":
        return [runtime]
    candidates = []
    if (root / ".claude").exists() or (root / ".claude-plugin").exists():
        candidates.append("claude")
    if (root / ".codex").exists() or (root / "AGENTS.md").exists():
        candidates.append("codex")
    if (root / ".cursor").exists():
        candidates.append("cursor")
    return candidates or ["generic"]


def hook_plan(root: pathlib.Path, runtime: str, event: str) -> dict[str, Any]:
    runtimes = detect_runtime(root, runtime)
    return {
        "runtime": runtime,
        "detected": runtimes,
        "event": event,
        "portable_fallback": [
            "church context load --root <repo> --format markdown --include-history",
            "church ledger check gaps --root <repo> --allow-open --format json",
            "church lifecycle status --root <repo> --format json",
        ],
        "runtime_hooks": [
            {
                "runtime": item,
                "status": "adapter-required" if item != "generic" else "fallback-only",
                "risk_control": "dry-run first; require explicit install confirmation; preserve fallback commands",
            }
            for item in runtimes
        ],
    }


def cmd_hooks_plan(args: argparse.Namespace) -> int:
    emit(hook_plan(repo_root(args.root), args.runtime, args.event), args.format, "Repo Church Hooks Plan")
    return 0


def cmd_hooks_check(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    plan = hook_plan(root, args.runtime, args.event)
    scaffold = registry_path(root, "hooks")
    result = {
        "outcome": "PASS" if scaffold.exists() else "PASS_WITH_RISK",
        "scaffold_exists": scaffold.exists(),
        "plan": plan,
    }
    emit(result, args.format, "Repo Church Hooks Check")
    return 0


def cmd_hooks_scaffold(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    plan = hook_plan(root, args.runtime, args.event)
    plan["installed"] = False
    plan["review_required"] = True
    path = registry_path(root, "hooks")
    write_json(path, plan)
    state = ensure_state(root)
    state["artifacts"]["hook_plan"] = relative_to_root(root, path)
    state["history"].append({"event": "hooks.scaffold", "at": now_iso(), "runtime": args.runtime, "hook_event": args.event})
    save_state(root, state)
    emit({"hook_plan": str(path), "plan": plan}, args.format, "Repo Church Hooks Scaffold")
    return 0


def git_capture(root: pathlib.Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=str(root), check=False, capture_output=True, text=True)


def cmd_branch_plan(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    branch = git_capture(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    status = git_capture(root, ["status", "--short"])
    changed = [line.strip() for line in status.stdout.splitlines() if line.strip()]
    plan = {
        "current_branch": branch.stdout.strip() if branch.returncode == 0 else "unknown",
        "target": args.target,
        "new_branch": args.name,
        "exclude_paths": args.exclude or [".planning", ".church"],
        "changed_files": changed,
        "commands": [
            f"git switch -c {args.name}",
            "# Review changed files and stage only PR-safe paths.",
            "git status --short",
            "git add <approved files>",
            f"git commit -m \"{args.message}\"",
        ],
        "requires_review": True,
    }
    if args.output:
        write_json(pathlib.Path(args.output).expanduser().resolve(), plan)
    emit(plan, args.format, "Repo Church Branch Plan")
    return 0


def cmd_undo_plan(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    status = git_capture(root, ["status", "--short"])
    log = git_capture(root, ["log", "--oneline", "-5"])
    plan = {
        "ref": args.ref,
        "paths": args.path or [],
        "dirty_status": status.stdout.splitlines() if status.returncode == 0 else [],
        "recent_commits": log.stdout.splitlines() if log.returncode == 0 else [],
        "commands": [
            f"git show --stat {args.ref}",
            "git restore --staged <paths>",
            "git restore <paths>",
            f"git revert {args.ref}",
        ],
        "risk_control": "Choose restore for uncommitted local changes and revert for published commits. Never run without reviewing status.",
        "requires_review": True,
    }
    if args.output:
        write_json(pathlib.Path(args.output).expanduser().resolve(), plan)
    emit(plan, args.format, "Repo Church Undo Plan")
    return 0


def cmd_archive_plan(args: argparse.Namespace) -> int:
    root = repo_root(args.root)
    candidates = []
    for rel in args.path or [".planning/phases", ".church/runtime"]:
        candidate = root / rel
        if candidate.exists():
            candidates.append(relative_to_root(root, candidate))
    plan = {
        "archive_root": args.archive_root,
        "candidates": candidates,
        "commands": [f"mkdir -p {args.archive_root}", "mv <approved artifacts> <archive-root>/"],
        "dry_run": True,
        "requires_review": True,
    }
    if args.output:
        write_json(pathlib.Path(args.output).expanduser().resolve(), plan)
    emit(plan, args.format, "Repo Church Archive Plan")
    return 0


def add_format(parser: argparse.ArgumentParser, default: str = "json") -> None:
    parser.add_argument("--format", choices=["json", "markdown"], default=default, help=f"Output format (default: {default}).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Repo Church lifecycle helper CLI",
        epilog=(
            "Examples:\n"
            "  church init --root . --mode brownfield --project-name api-bank\n"
            "  church moat check --root . --allow-incomplete\n"
            "  church lifecycle advance anchor --root . --outcome PASS --evidence .church/anchors/phase-01.md --force\n"
            "  church context load --root . --format markdown\n"
            "  church bible inventory --root . --format json --output -"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize state, default moat artifacts, and optional Bible scaffold.")
    p_init.add_argument("--root", default=".")
    p_init.add_argument("--mode", choices=["greenfield", "brownfield"], default="brownfield")
    p_init.add_argument("--project-name")
    p_init.add_argument("--no-moat", action="store_false", dest="moat")
    p_init.add_argument("--scaffold-bible", action="store_true", help="Also run church bible scaffold --root <repo>.")
    add_format(p_init)
    p_init.set_defaults(func=cmd_init, moat=True)

    p_registry = sub.add_parser("registry", help="Inspect predefined workflow and state-key dictionaries.")
    registry_sub = p_registry.add_subparsers(dest="registry_command", required=True)
    p_registry_list = registry_sub.add_parser("list", help="List workflow registry entries.")
    add_format(p_registry_list)
    p_registry_list.set_defaults(func=cmd_registry_list)
    p_registry_show = registry_sub.add_parser("show", help="Show one workflow registry entry.")
    p_registry_show.add_argument("workflow", choices=sorted(WORKFLOW_REGISTRY))
    add_format(p_registry_show)
    p_registry_show.set_defaults(func=cmd_registry_show)
    p_registry_keys = registry_sub.add_parser("keys", help="List predefined state keys.")
    add_format(p_registry_keys)
    p_registry_keys.set_defaults(func=cmd_registry_keys)
    p_registry_reasoning = registry_sub.add_parser("reasoning", help="Show which workflow parts stay agentic.")
    p_registry_reasoning.add_argument("workflow", nargs="?", choices=sorted(WORKFLOW_REGISTRY))
    add_format(p_registry_reasoning)
    p_registry_reasoning.set_defaults(func=cmd_registry_reasoning)

    p_state = sub.add_parser("state", help="Read or mutate lifecycle state.")
    state_sub = p_state.add_subparsers(dest="state_command", required=True)
    p_state_show = state_sub.add_parser("show", help="Show full state.")
    p_state_show.add_argument("--root", default=".")
    add_format(p_state_show)
    p_state_show.set_defaults(func=cmd_state_show)
    p_state_get = state_sub.add_parser("get", help="Get one dotted state key.")
    p_state_get.add_argument("key")
    p_state_get.add_argument("--root", default=".")
    add_format(p_state_get)
    p_state_get.set_defaults(func=cmd_state_get)
    p_state_set = state_sub.add_parser("set", help="Set one dotted state key.")
    p_state_set.add_argument("key")
    p_state_set.add_argument("value")
    p_state_set.add_argument("--root", default=".")
    add_format(p_state_set)
    p_state_set.set_defaults(func=cmd_state_set)

    p_moat = sub.add_parser("moat", help="Create, update, render, export, and validate moat artifacts.")
    moat_sub = p_moat.add_subparsers(dest="moat_command", required=True)
    p_moat_init = moat_sub.add_parser("init", help="Create moat.json and moat.md.")
    p_moat_init.add_argument("--root", default=".")
    p_moat_init.add_argument("--project-name")
    p_moat_init.add_argument("--force", action="store_true")
    add_format(p_moat_init)
    p_moat_init.set_defaults(func=cmd_moat_init)
    p_moat_set = moat_sub.add_parser("set", help="Set one dotted moat key.")
    p_moat_set.add_argument("key")
    p_moat_set.add_argument("value")
    p_moat_set.add_argument("--root", default=".")
    p_moat_set.add_argument("--input")
    p_moat_set.add_argument("--output")
    add_format(p_moat_set)
    p_moat_set.set_defaults(func=cmd_moat_set)
    p_moat_import = moat_sub.add_parser("import", help="Import moat JSON from --input or stdin.")
    p_moat_import.add_argument("--root", default=".")
    p_moat_import.add_argument("--input")
    p_moat_import.add_argument("--stdin", action="store_true")
    p_moat_import.add_argument("--merge", action="store_true")
    add_format(p_moat_import)
    p_moat_import.set_defaults(func=cmd_moat_import)
    p_moat_export = moat_sub.add_parser("export", help="Export moat JSON or Markdown.")
    p_moat_export.add_argument("--root", default=".")
    p_moat_export.add_argument("--input")
    p_moat_export.add_argument("--output")
    add_format(p_moat_export)
    p_moat_export.set_defaults(func=cmd_moat_export)
    p_moat_render = moat_sub.add_parser("render", help="Render moat.json to moat.md.")
    p_moat_render.add_argument("--root", default=".")
    p_moat_render.add_argument("--input")
    p_moat_render.add_argument("--output")
    add_format(p_moat_render)
    p_moat_render.set_defaults(func=cmd_moat_render)
    p_moat_check = moat_sub.add_parser("check", help="Score moat completeness and update active moat gate.")
    p_moat_check.add_argument("--root", default=".")
    p_moat_check.add_argument("--input")
    p_moat_check.add_argument("--allow-incomplete", action="store_true", help="Return 0 even when moat is HOLD/BLOCK.")
    add_format(p_moat_check)
    p_moat_check.set_defaults(func=cmd_moat_check)

    p_lifecycle = sub.add_parser("lifecycle", help="Track phase progression state and handoffs.")
    lifecycle_sub = p_lifecycle.add_subparsers(dest="lifecycle_command", required=True)
    p_lifecycle_list = lifecycle_sub.add_parser("list", help="List lifecycle workflows.")
    add_format(p_lifecycle_list)
    p_lifecycle_list.set_defaults(func=cmd_lifecycle_list)
    p_lifecycle_show = lifecycle_sub.add_parser("show", help="Show one workflow.")
    p_lifecycle_show.add_argument("workflow", choices=sorted(WORKFLOW_REGISTRY))
    add_format(p_lifecycle_show)
    p_lifecycle_show.set_defaults(func=cmd_lifecycle_show)
    p_lifecycle_status = lifecycle_sub.add_parser("status", help="Show active lifecycle status.")
    p_lifecycle_status.add_argument("--root", default=".")
    p_lifecycle_status.add_argument("--include-history", action="store_true")
    p_lifecycle_status.add_argument("--max-history", type=int, default=8)
    add_format(p_lifecycle_status)
    p_lifecycle_status.set_defaults(func=cmd_lifecycle_status)
    p_lifecycle_advance = lifecycle_sub.add_parser("advance", help="Advance to a workflow with gate outcome.")
    p_lifecycle_advance.add_argument("workflow", choices=sorted(WORKFLOW_REGISTRY))
    p_lifecycle_advance.add_argument("--gate")
    p_lifecycle_advance.add_argument("--stage")
    p_lifecycle_advance.add_argument("--outcome", choices=GATE_OUTCOMES, default="HOLD")
    p_lifecycle_advance.add_argument("--phase")
    p_lifecycle_advance.add_argument("--milestone")
    p_lifecycle_advance.add_argument("--evidence")
    p_lifecycle_advance.add_argument("--artifact", action="append", help="Register artifact as NAME=PATH.")
    p_lifecycle_advance.add_argument("--force", action="store_true", help="Allow non-adjacent transition.")
    p_lifecycle_advance.add_argument(
        "--allow-quality-risk",
        action="store_true",
        help="Record a passing outcome despite quality-check blockers; use only for explicitly accepted non-critical exceptions.",
    )
    p_lifecycle_advance.add_argument("--dry-run", action="store_true", help="Preview transition without writing state.")
    p_lifecycle_advance.add_argument("--root", default=".")
    add_format(p_lifecycle_advance)
    p_lifecycle_advance.set_defaults(func=cmd_lifecycle_advance)
    p_lifecycle_handoff = lifecycle_sub.add_parser("handoff", help="Render compact handoff from current state.")
    p_lifecycle_handoff.add_argument("--root", default=".")
    p_lifecycle_handoff.add_argument("--output")
    add_format(p_lifecycle_handoff, default="markdown")
    p_lifecycle_handoff.set_defaults(func=cmd_lifecycle_handoff)
    p_lifecycle_prove = lifecycle_sub.add_parser(
        "prove",
        help="Run the canonical Repo Church lifecycle with evidence artifacts and emit a proof record.",
    )
    p_lifecycle_prove.add_argument("--root", default=".")
    p_lifecycle_prove.add_argument(
        "--self-package",
        help="Package root to inventory and claim-scan as evidence (defaults to --root).",
    )
    p_lifecycle_prove.add_argument("--project-name")
    p_lifecycle_prove.add_argument("--mode", choices=["greenfield", "brownfield"], default="brownfield")
    add_format(p_lifecycle_prove)
    p_lifecycle_prove.set_defaults(func=cmd_lifecycle_prove)

    p_ledger = sub.add_parser("ledger", help="Manage structured assumption/gap/UAT/risk ledgers.")
    ledger_sub = p_ledger.add_subparsers(dest="ledger_command", required=True)
    for command, help_text, func in [
        ("init", "Create or reset a ledger.", cmd_ledger_init),
        ("list", "List ledger items.", cmd_ledger_list),
        ("check", "Check ledger blockers.", cmd_ledger_check),
    ]:
        p = ledger_sub.add_parser(command, help=help_text)
        p.add_argument("kind", choices=sorted(LEDGER_KINDS))
        p.add_argument("--root", default=".")
        if command == "init":
            p.add_argument("--force", action="store_true", help="Reset an existing ledger.")
        if command == "check":
            p.add_argument("--allow-open", action="store_true", help="Return 0 even with open blockers.")
        add_format(p, default="markdown" if command == "list" else "json")
        p.set_defaults(func=func)
    p_ledger_add = ledger_sub.add_parser("add", help="Add or replace one ledger item.")
    p_ledger_add.add_argument("kind", choices=sorted(LEDGER_KINDS))
    p_ledger_add.add_argument("--id", required=True)
    p_ledger_add.add_argument("--summary", required=True)
    p_ledger_add.add_argument("--status", default="open")
    p_ledger_add.add_argument("--severity", default="medium")
    p_ledger_add.add_argument("--evidence", default="")
    p_ledger_add.add_argument("--owner", default="unassigned")
    p_ledger_add.add_argument("--proof", default="")
    p_ledger_add.add_argument("--acceptance-test", default="", help="Acceptance proof needed to close this item.")
    p_ledger_add.add_argument("--recheck", default="", help="Command or trigger used to recheck closure.")
    p_ledger_add.add_argument("--blocks-progression", action="store_true", help="Mark this item as blocking phase progression.")
    p_ledger_add.add_argument("--workflow")
    p_ledger_add.add_argument("--extra", action="append")
    p_ledger_add.add_argument("--replace", action="store_true", help="Refresh an existing item with the same ID.")
    p_ledger_add.add_argument("--force", action="store_true")
    p_ledger_add.add_argument("--root", default=".")
    add_format(p_ledger_add)
    p_ledger_add.set_defaults(func=cmd_ledger_add)

    p_context = sub.add_parser("context", help="Load compact fresh context from deterministic state.")
    context_sub = p_context.add_subparsers(dest="context_command", required=True)
    p_context_load = context_sub.add_parser("load", help="Load current state, artifacts, next workflows, ledgers, and moat score.")
    p_context_load.add_argument("--root", default=".")
    p_context_load.add_argument("--include-history", action="store_true")
    p_context_load.add_argument("--max-history", type=int, default=8)
    add_format(p_context_load, default="markdown")
    p_context_load.set_defaults(func=cmd_context_load)

    p_workspace = sub.add_parser("workspace", help="Manage portable Repo Church workspace records.")
    workspace_sub = p_workspace.add_subparsers(dest="workspace_command", required=True)
    p_workspace_list = workspace_sub.add_parser("list", help="List workspaces.")
    p_workspace_list.add_argument("--root", default=".")
    add_format(p_workspace_list)
    p_workspace_list.set_defaults(func=cmd_workspace_list)
    p_workspace_create = workspace_sub.add_parser("create", help="Create a workspace record and set it active.")
    p_workspace_create.add_argument("name")
    p_workspace_create.add_argument("--root", default=".")
    p_workspace_create.add_argument("--path")
    p_workspace_create.add_argument("--summary")
    p_workspace_create.add_argument("--owner")
    p_workspace_create.add_argument("--force", action="store_true")
    add_format(p_workspace_create)
    p_workspace_create.set_defaults(func=cmd_workspace_create)
    p_workspace_status = workspace_sub.add_parser("status", help="Show one workspace.")
    p_workspace_status.add_argument("name")
    p_workspace_status.add_argument("--root", default=".")
    add_format(p_workspace_status)
    p_workspace_status.set_defaults(func=cmd_workspace_status)
    p_workspace_switch = workspace_sub.add_parser("switch", help="Set active workspace.")
    p_workspace_switch.add_argument("name")
    p_workspace_switch.add_argument("--root", default=".")
    add_format(p_workspace_switch)
    p_workspace_switch.set_defaults(func=cmd_workspace_switch)
    p_workspace_complete = workspace_sub.add_parser("complete", help="Mark a workspace complete.")
    p_workspace_complete.add_argument("name")
    p_workspace_complete.add_argument("--root", default=".")
    add_format(p_workspace_complete)
    p_workspace_complete.set_defaults(func=cmd_workspace_complete)

    p_thread = sub.add_parser("thread", help="Manage portable thread and continuation records.")
    thread_sub = p_thread.add_subparsers(dest="thread_command", required=True)
    p_thread_list = thread_sub.add_parser("list", help="List thread records.")
    p_thread_list.add_argument("--root", default=".")
    add_format(p_thread_list)
    p_thread_list.set_defaults(func=cmd_thread_list)
    p_thread_create = thread_sub.add_parser("create", help="Create a thread continuation record.")
    p_thread_create.add_argument("name")
    p_thread_create.add_argument("--root", default=".")
    p_thread_create.add_argument("--runtime")
    p_thread_create.add_argument("--external-id")
    p_thread_create.add_argument("--summary")
    p_thread_create.add_argument("--handoff")
    p_thread_create.add_argument("--force", action="store_true")
    add_format(p_thread_create)
    p_thread_create.set_defaults(func=cmd_thread_create)
    p_thread_status = thread_sub.add_parser("status", help="Show one thread record.")
    p_thread_status.add_argument("name")
    p_thread_status.add_argument("--root", default=".")
    add_format(p_thread_status)
    p_thread_status.set_defaults(func=cmd_thread_status)
    p_thread_resume = thread_sub.add_parser("resume", help="Set thread active and print resume hint.")
    p_thread_resume.add_argument("name")
    p_thread_resume.add_argument("--root", default=".")
    add_format(p_thread_resume)
    p_thread_resume.set_defaults(func=cmd_thread_resume)
    p_thread_complete = thread_sub.add_parser("complete", help="Mark a thread complete.")
    p_thread_complete.add_argument("name")
    p_thread_complete.add_argument("--root", default=".")
    add_format(p_thread_complete)
    p_thread_complete.set_defaults(func=cmd_thread_complete)

    p_inbox = sub.add_parser("inbox", help="Capture and triage inbox/backlog items.")
    inbox_sub = p_inbox.add_subparsers(dest="inbox_command", required=True)
    p_inbox_add = inbox_sub.add_parser("add", help="Add an inbox/backlog item.")
    p_inbox_add.add_argument("--id", required=True)
    p_inbox_add.add_argument("--summary", required=True)
    p_inbox_add.add_argument("--kind", choices=["idea", "question", "gap", "risk", "backlog"], default="idea")
    p_inbox_add.add_argument("--status", default="open")
    p_inbox_add.add_argument("--severity", default="medium")
    p_inbox_add.add_argument("--evidence", default="")
    p_inbox_add.add_argument("--owner", default="unassigned")
    p_inbox_add.add_argument("--route", default="")
    p_inbox_add.add_argument("--force", action="store_true")
    p_inbox_add.add_argument("--root", default=".")
    add_format(p_inbox_add)
    p_inbox_add.set_defaults(func=cmd_inbox_add)
    p_inbox_list = inbox_sub.add_parser("list", help="List inbox/backlog items.")
    p_inbox_list.add_argument("--root", default=".")
    add_format(p_inbox_list)
    p_inbox_list.set_defaults(func=cmd_inbox_list)
    p_inbox_check = inbox_sub.add_parser("check", help="Check open inbox blockers.")
    p_inbox_check.add_argument("--root", default=".")
    p_inbox_check.add_argument("--allow-open", action="store_true")
    add_format(p_inbox_check)
    p_inbox_check.set_defaults(func=cmd_inbox_check)

    p_profile = sub.add_parser("profile", help="Manage consented profile artifacts for personalization.")
    profile_sub = p_profile.add_subparsers(dest="profile_command", required=True)
    p_profile_init = profile_sub.add_parser("init", help="Create a consented profile artifact.")
    p_profile_init.add_argument("--root", default=".")
    p_profile_init.add_argument("--subject", default="user")
    p_profile_init.add_argument("--purpose")
    p_profile_init.add_argument("--consent", action="store_true")
    p_profile_init.add_argument("--force", action="store_true")
    add_format(p_profile_init)
    p_profile_init.set_defaults(func=cmd_profile_init)
    p_profile_set = profile_sub.add_parser("set", help="Set one profile signal key.")
    p_profile_set.add_argument("key")
    p_profile_set.add_argument("value")
    p_profile_set.add_argument("--root", default=".")
    p_profile_set.add_argument("--force", action="store_true", help="Allow non-behavioral metadata without consent.")
    add_format(p_profile_set)
    p_profile_set.set_defaults(func=cmd_profile_set)
    p_profile_export = profile_sub.add_parser("export", help="Export profile artifact.")
    p_profile_export.add_argument("--root", default=".")
    add_format(p_profile_export)
    p_profile_export.set_defaults(func=cmd_profile_export)
    p_profile_check = profile_sub.add_parser("check", help="Check consent and profile readiness.")
    p_profile_check.add_argument("--root", default=".")
    p_profile_check.add_argument("--allow-blocked", action="store_true")
    add_format(p_profile_check)
    p_profile_check.set_defaults(func=cmd_profile_check)

    p_sketch = sub.add_parser("sketch", help="Register design/ideation artifacts and signoff requirements.")
    sketch_sub = p_sketch.add_subparsers(dest="sketch_command", required=True)
    p_sketch_register = sketch_sub.add_parser("register", help="Register a sketch or design artifact.")
    p_sketch_register.add_argument("--id", required=True)
    p_sketch_register.add_argument("--path", required=True)
    p_sketch_register.add_argument("--summary", required=True)
    p_sketch_register.add_argument("--status", default="open")
    p_sketch_register.add_argument("--evidence", default="")
    p_sketch_register.add_argument("--requires-user-signoff", action="store_true")
    p_sketch_register.add_argument("--force", action="store_true")
    p_sketch_register.add_argument("--root", default=".")
    add_format(p_sketch_register)
    p_sketch_register.set_defaults(func=cmd_sketch_register)
    p_sketch_list = sketch_sub.add_parser("list", help="List sketch artifacts.")
    p_sketch_list.add_argument("--root", default=".")
    add_format(p_sketch_list)
    p_sketch_list.set_defaults(func=cmd_sketch_list)
    p_sketch_check = sketch_sub.add_parser("check", help="Check design signoff blockers.")
    p_sketch_check.add_argument("--root", default=".")
    p_sketch_check.add_argument("--allow-open", action="store_true")
    add_format(p_sketch_check)
    p_sketch_check.set_defaults(func=cmd_sketch_check)

    p_hooks = sub.add_parser("hooks", help="Plan, check, and scaffold runtime hook fallbacks.")
    hooks_sub = p_hooks.add_subparsers(dest="hooks_command", required=True)
    for command, help_text, func in [
        ("plan", "Render a hook plan without writing files.", cmd_hooks_plan),
        ("check", "Check hook scaffold and fallback readiness.", cmd_hooks_check),
        ("scaffold", "Write a reviewed hook plan artifact.", cmd_hooks_scaffold),
    ]:
        p = hooks_sub.add_parser(command, help=help_text)
        p.add_argument("--root", default=".")
        p.add_argument("--runtime", choices=["auto", "claude", "codex", "cursor", "generic"], default="auto")
        p.add_argument("--event", default="pre-progress")
        add_format(p)
        p.set_defaults(func=func)

    p_branch = sub.add_parser("branch", help="Plan a PR-safe branch without mutating git state.")
    branch_sub = p_branch.add_subparsers(dest="branch_command", required=True)
    p_branch_plan = branch_sub.add_parser("plan", help="Plan a clean branch and review-safe staging path.")
    p_branch_plan.add_argument("--root", default=".")
    p_branch_plan.add_argument("--target", default="main")
    p_branch_plan.add_argument("--name", required=True)
    p_branch_plan.add_argument("--message", default="church scoped changes")
    p_branch_plan.add_argument("--exclude", action="append")
    p_branch_plan.add_argument("--output")
    add_format(p_branch_plan)
    p_branch_plan.set_defaults(func=cmd_branch_plan)

    p_undo = sub.add_parser("undo", help="Plan rollback/undo operations without mutating git state.")
    undo_sub = p_undo.add_subparsers(dest="undo_command", required=True)
    p_undo_plan = undo_sub.add_parser("plan", help="Render a rollback plan.")
    p_undo_plan.add_argument("--root", default=".")
    p_undo_plan.add_argument("--ref", default="HEAD")
    p_undo_plan.add_argument("--path", action="append")
    p_undo_plan.add_argument("--output")
    add_format(p_undo_plan)
    p_undo_plan.set_defaults(func=cmd_undo_plan)

    p_archive = sub.add_parser("archive", help="Plan artifact cleanup/archive operations.")
    archive_sub = p_archive.add_subparsers(dest="archive_command", required=True)
    p_archive_plan = archive_sub.add_parser("plan", help="Render a dry-run archive plan.")
    p_archive_plan.add_argument("--root", default=".")
    p_archive_plan.add_argument("--path", action="append")
    p_archive_plan.add_argument("--archive-root", default=".church/archive")
    p_archive_plan.add_argument("--output")
    add_format(p_archive_plan)
    p_archive_plan.set_defaults(func=cmd_archive_plan)

    p_bible = sub.add_parser("bible", help="Delegate to bundled repo-bible CLI.", add_help=False)
    p_bible.add_argument("-h", "--help", action="store_true", dest="bible_help")
    p_bible.add_argument("args", nargs=argparse.REMAINDER)
    p_bible.set_defaults(func=cmd_bible)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
