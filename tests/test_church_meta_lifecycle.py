#!/usr/bin/env python3
"""Meta lifecycle proof test for Repo Church.

Run from the repository root:

    python3 tests/test_church_meta_lifecycle.py
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = PACKAGE_ROOT / "skills" / "church" / "scripts" / "church"


class ChurchMetaLifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="church-meta-lifecycle-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [str(CLI), *args],
            text=True,
            capture_output=True,
            env={**os.environ, "CHURCH_PYTHON": sys.executable, "PYTHONDONTWRITEBYTECODE": "1", **(env or {})},
        )
        if result.returncode != 0:
            self.fail(f"Command failed: church {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result

    def test_lifecycle_prove_reaches_refresh_with_required_evidence(self) -> None:
        result = self.run_cli(
            "lifecycle", "prove",
            "--root", str(self.tmp),
            "--self-package", str(PACKAGE_ROOT),
            "--project-name", "Repo Church",
            "--format", "json",
        )
        payload = json.loads(result.stdout)
        proof_path = pathlib.Path(payload["proof"])
        self.assertTrue(proof_path.exists())

        proof = json.loads(proof_path.read_text())
        self.assertEqual(proof["root"], ".")
        self.assertFalse(pathlib.PurePath(proof["evidence_root"]).is_absolute())
        self.assertEqual(proof["final_status"]["active"]["workflow"], "refresh")
        self.assertEqual(proof["final_status"]["active"]["outcome"], "PASS")
        self.assertEqual(
            proof["repo_bible_commands"],
            ["inventory", "sources", "claim-scan", "validate", "render-html"],
        )

        blocked_flags = {"--force", "--allow-quality-risk"}
        for command in proof["commands"]:
            self.assertEqual(command["exit_code"], 0, command)
            self.assertTrue(blocked_flags.isdisjoint(command["argv"]), command["argv"])
            for arg in command["argv"]:
                self.assertNotIn(str(self.tmp), arg)
            if "cwd" in command:
                self.assertFalse(pathlib.PurePath(command["cwd"]).is_absolute())
        validation_command = next(command for command in proof["commands"] if command["label"] == "bible-validate-json")
        validation = json.loads(validation_command["stdout"])
        self.assertEqual(validation["error_count"], 0)
        self.assertEqual(validation["warning_count"], 0)
        labels = {command["label"] for command in proof["commands"]}
        for required_label in [
            "ship-package-validator",
            "ship-cli-tests",
            "ship-plugin-assets",
            "ship-install-smoke",
        ]:
            self.assertIn(required_label, labels)

        pass_events = [
            item["workflow"]
            for item in proof["final_status"]["history"]
            if item.get("event") == "lifecycle.advance" and item.get("outcome") == "PASS"
        ]
        expected = [
            "moat", "bible", "survey", "harden", "anchor", "spec-gate",
            "gap-closure", "handoff", "uat", "ship", "refresh",
        ]
        cursor = 0
        for workflow in pass_events:
            if cursor < len(expected) and workflow == expected[cursor]:
                cursor += 1
        self.assertEqual(cursor, len(expected), pass_events)

        required_artifacts = [
            ".church/moat/moat.md",
            ".church/bible/_repo-bible-validation.md",
            ".church/survey/codebase-survey.md",
            ".church/ledgers/assumptions.json",
            ".church/anchors/meta-lifecycle-anchor.md",
            ".church/specs/meta-lifecycle-spec.md",
            ".church/ledgers/gaps.json",
            ".church/handoff/meta-lifecycle-handoff.md",
            ".church/ledgers/uat.json",
            ".church/ship/meta-ship-gate.md",
            ".church/refresh/meta-refresh-record.md",
        ]
        for rel_path in required_artifacts:
            self.assertTrue((self.tmp / rel_path).exists(), rel_path)

    def test_lifecycle_prove_skip_ship_checks_records_skips(self) -> None:
        result = self.run_cli(
            "lifecycle", "prove",
            "--root", str(self.tmp),
            "--self-package", str(PACKAGE_ROOT),
            "--project-name", "Repo Church",
            "--skip-ship-checks",
            "--format", "json",
        )
        proof = json.loads(pathlib.Path(json.loads(result.stdout)["proof"]).read_text())
        skipped = {entry["label"]: entry for entry in proof["commands"] if entry.get("skipped")}
        for label in [
            "ship-package-validator",
            "ship-cli-tests",
            "ship-plugin-assets",
            "ship-install-smoke",
        ]:
            self.assertIn(label, skipped)
            self.assertEqual(skipped[label]["stdout"], "Skipped due to --skip-ship-checks.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
