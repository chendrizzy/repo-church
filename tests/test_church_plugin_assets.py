#!/usr/bin/env python3
"""Static package tests for Repo Church plugin commands and agent profiles.

Run from the repository root:

    python3 agent-skills/repo-church/tests/test_church_plugin_assets.py
"""

from __future__ import annotations

import json
import pathlib
import re
import unittest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
COMMANDS_ROOT = PACKAGE_ROOT / "commands"
AGENTS_ROOT = PACKAGE_ROOT / "agents"
SKILLS_ROOT = PACKAGE_ROOT / "skills"

EXPECTED_COMMANDS = [
    "church-gather",
    "church-discern",
    "church-canonize",
    "church-commission",
    "church-fellowship",
    "church-bless",
    "church-renew",
    "church-survey",
    "church-guard",
    "church-workspace",
    "church-thread",
    "church-inbox",
    "church-profile",
    "church-sketch",
    "church-branch",
    "church-rewind",
    "church-archive",
    "church-confess",
    "church-atonement",
    "church-quick-rite",
    "church-council",
]

CORE_STAGE_LABELS = [
    "church:gather",
    "church:discern",
    "church:canonize",
    "church:commission",
    "church:fellowship",
    "church:bless",
    "church:renew",
]

EXPECTED_AGENTS = [
    "church-ai-eval-planner",
    "church-anchor-architect",
    "church-bible-scribe",
    "church-archive-steward",
    "church-codebase-cartographer",
    "church-code-examiner",
    "church-debug-examiner",
    "church-doc-scribe",
    "church-doctrine-auditor",
    "church-gap-steward",
    "church-git-steward",
    "church-moat-scout",
    "church-profile-counselor",
    "church-runtime-guardian",
    "church-security-examiner",
    "church-ship-steward",
    "church-sketch-curator",
    "church-spec-canonist",
    "church-thread-steward",
    "church-triage-steward",
    "church-uat-fellow",
    "church-ui-examiner",
    "church-workstream-deacon",
    "church-workspace-steward",
]


def parse_frontmatter(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise AssertionError(f"{path} missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise AssertionError(f"{path} missing closing frontmatter")

    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


class ChurchPluginAssetTest(unittest.TestCase):
    def test_manifest_exposes_command_and_agent_roots(self) -> None:
        manifest = json.loads((PACKAGE_ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "repo-church")
        self.assertEqual(manifest["commands"], "./commands")
        self.assertEqual(manifest["agents"], "./agents")

    def test_expected_staged_commands_exist_and_are_self_describing(self) -> None:
        stems = sorted(path.stem for path in COMMANDS_ROOT.glob("*.md"))
        self.assertEqual(stems, sorted(EXPECTED_COMMANDS))

        for stem in EXPECTED_COMMANDS:
            path = COMMANDS_ROOT / f"{stem}.md"
            text = path.read_text()
            metadata = parse_frontmatter(path)
            command_label = stem.replace("church-", "church:", 1)

            self.assertEqual(metadata.get("name"), stem)
            self.assertGreater(len(metadata.get("description", "")), 40)
            self.assertIn(f"# {command_label}", text)
            self.assertIn("church", text)
            self.assertIn("## Output", text)
            self.assertIn("common gate record", text)

            if command_label in CORE_STAGE_LABELS:
                self.assertIn("## Progressive Loading", text)
                self.assertIn("## CLI Preflight", text)
                self.assertRegex(text, r"church lifecycle|church context|church bible|church ledger")
            else:
                self.assertRegex(text, r"## CLI (Pattern|Preflight)")

    def test_stage_map_keeps_core_loop_in_order(self) -> None:
        stage_map = (SKILLS_ROOT / "church" / "references" / "stage-command-map.md").read_text()
        positions = [stage_map.index(f"`{label}`") for label in CORE_STAGE_LABELS]
        self.assertEqual(positions, sorted(positions))

        for label in CORE_STAGE_LABELS:
            self.assertIn("GSD counterpart", stage_map)
            self.assertIn(label, stage_map)

        for label in [
            "church:confess",
            "church:atonement",
            "church:quick-rite",
            "church:council",
            "church:guard",
            "church:workspace",
            "church:thread",
            "church:inbox",
            "church:profile",
            "church:sketch",
            "church:branch",
            "church:rewind",
            "church:archive",
        ]:
            self.assertIn(label, stage_map)
        self.assertIn("church:survey", stage_map)

    def test_expected_agent_profiles_exist_and_have_contract_sections(self) -> None:
        stems = sorted(path.stem for path in AGENTS_ROOT.glob("*.md"))
        self.assertEqual(stems, sorted(EXPECTED_AGENTS))

        combined_references = "\n".join(
            [
                (PACKAGE_ROOT / "README.md").read_text(),
                (SKILLS_ROOT / "church" / "references" / "stage-command-map.md").read_text(),
                "\n".join(path.read_text() for path in COMMANDS_ROOT.glob("*.md")),
            ]
        )

        for stem in EXPECTED_AGENTS:
            path = AGENTS_ROOT / f"{stem}.md"
            text = path.read_text()
            metadata = parse_frontmatter(path)

            self.assertEqual(metadata.get("name"), stem)
            self.assertGreater(len(metadata.get("description", "")), 40)
            self.assertIn("capabilities:", text)
            for section in ["## Required Inputs", "## Work", "## Output", "## Quality Bar"]:
                self.assertIn(section, text)
            self.assertIn("standard footer", text)
            self.assertIn(stem, combined_references)

    def test_commands_only_reference_existing_church_assets(self) -> None:
        known_assets = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        known_assets.update(path.stem for path in AGENTS_ROOT.glob("*.md"))

        token_pattern = re.compile(r"`((?:church-[a-z0-9-]+|repo-bible)(?:[^`\\s]*)?)`")
        for path in COMMANDS_ROOT.glob("*.md"):
            tokens = set(token_pattern.findall(path.read_text()))
            unknown = sorted(token for token in tokens if token not in known_assets)
            self.assertEqual(unknown, [], f"{path} references unknown repo assets")

    def test_counterpart_gap_closure_records_resolved_gsd_deltas(self) -> None:
        gap_doc = SKILLS_ROOT / "church" / "references" / "counterpart-gap-closure.md"
        text = gap_doc.read_text()

        for required in [
            "Stage-contained command layer",
            "Lazy-loaded specialist profiles",
            "Requirements and spec stringency",
            "Collaborative UAT and mutual signoff",
            "Bible leverage between phases",
            "Brownfield codebase mapping",
            "Runtime hooks",
            "Workspace and thread records",
            "Git branch and rollback planning",
            "Profile and sketch artifacts",
            "Agentic reasoning boundary",
            "Gap closure accountability",
        ]:
            self.assertIn(required, text)

        self.assertIn("validate-package.sh", text)
        self.assertIn("Plugin asset tests", text)

    def test_deferred_parity_closure_records_actual_assets(self) -> None:
        closure_doc = SKILLS_ROOT / "church" / "references" / "deferred-parity-closure.md"
        text = closure_doc.read_text()

        for required in [
            "church:guard",
            "church:workspace",
            "church:thread",
            "church:inbox",
            "church:profile",
            "church:sketch",
            "church:branch",
            "church:rewind",
            "church:archive",
            "church profile init/set/export/check",
            "church sketch register/list/check",
            "church hooks plan/check/scaffold",
        ]:
            self.assertIn(required, text)

        self.assertIn("Reasoning-Heavy Items", text)
        self.assertIn("semantic parity first", text)

    def test_gsd_workflow_assessment_has_no_unresolved_future_placeholders(self) -> None:
        assessment = SKILLS_ROOT / "church" / "references" / "gsd-workflow-assessment.md"
        text = assessment.read_text().lower()
        self.assertNotIn("future `", text)
        self.assertNotIn("| future ", text)
        self.assertNotIn("extension backlog", text)
        self.assertNotIn("non-core", text)

        final_report = SKILLS_ROOT / "church" / "references" / "final-optimization-gap-closure.md"
        gap_report = SKILLS_ROOT / "church" / "references" / "counterpart-gap-closure.md"
        deferred_closure = SKILLS_ROOT / "church" / "references" / "deferred-parity-closure.md"
        comparison = PACKAGE_ROOT.parent.parent / ".agents" / "skills" / "gsd-church_asset-comparison"
        for path in [final_report, gap_report, deferred_closure, comparison]:
            if path.exists():
                content = path.read_text().lower()
                self.assertNotIn("extension backlog", content)
                self.assertNotIn("non-core", content)

    def test_church_namespace_hard_cutover_has_no_legacy_cli_or_profile_references(self) -> None:
        legacy_name = "repo" + "-church"
        legacy_snake = "repo" + "_church"
        legacy_env = "REPO_" + "CHURCH_ROOT"
        legacy_cli = SKILLS_ROOT / "church" / "scripts" / legacy_name
        self.assertFalse(legacy_cli.exists(), f"{legacy_name} CLI alias should be removed for hard cutover")

        scan_roots = [
            PACKAGE_ROOT,
            PACKAGE_ROOT.parent.parent / ".agents" / "skills",
        ]
        allowed = [
            re.compile(r"agent-skills/" + re.escape(legacy_name)),
            re.compile(r'"name": "' + re.escape(legacy_name) + r'"'),
            re.compile(r'manifest\["name"\].*' + re.escape(legacy_name)),
            re.compile(r"^" + re.escape(legacy_name) + r"/$"),
        ]
        for root in scan_roots:
            if not root.exists():
                continue
            paths = [p for p in root.rglob("*") if p.is_file() and p.suffix in {".md", ".py", ".sh", ".json"}]
            for path in paths:
                if ".git" in path.parts:
                    continue
                for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                    if legacy_name not in line and legacy_snake not in line and legacy_env not in line:
                        continue
                    self.assertTrue(
                        any(pattern.search(line) for pattern in allowed),
                        f"legacy namespace reference at {path}:{lineno}: {line}",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
