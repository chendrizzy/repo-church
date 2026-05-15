#!/usr/bin/env python3
"""End-to-end tests for the Repo Church CLI.

Run from the repository root:

    python3 agent-skills/repo-church/tests/test_church_cli.py
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


class ChurchCliE2ETest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="church-e2e-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args: str, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [str(CLI), *args],
            input=input_text,
            text=True,
            capture_output=True,
            env={**os.environ, "CHURCH_PYTHON": sys.executable, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if check and result.returncode != 0:
            self.fail(f"Command failed: church {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result

    def json_cli(self, *args: str, input_text: str | None = None, check: bool = True):
        result = self.run_cli(*args, input_text=input_text, check=check)
        return json.loads(result.stdout)

    def seed_complete_moat(self) -> dict:
        return {
            "schema_version": "church-moat/v1",
            "project_name": "Demo",
            "elevator_pitch": "Demo helps indie teams turn repo intent into governed agent workflows.",
            "third_party_summary": "Demo is a repo lifecycle tool that makes agent planning easier to verify.",
            "one_sentence_moat": "Its moat is the compounding project-specific workflow memory captured in deterministic gates.",
            "market": {
                "category": "agent workflow infrastructure",
                "buyer": "technical founders",
                "user": "coding agents and repo owners",
                "urgent_pain": "agent plans lose context and skip gates",
                "why_now": "agentic coding adoption is rising",
            },
            "competition": {
                "direct": ["GSD"],
                "adjacent": ["generic task runners"],
                "status_quo": ["manual planning docs"],
                "substitutes": ["ad hoc prompts"],
            },
            "wedge": {
                "entry_point": "repo initialization",
                "first_10_users": "solo builders with agent-heavy workflows",
                "switching_trigger": "planning drift",
                "time_to_value": "first init",
            },
            "leverage": {
                "primary_source": "deterministic lifecycle state",
                "secondary_sources": ["Bible packet", "CLI ledgers"],
                "what_compounds_with_use": "project-specific gates and evidence",
                "what_gets_harder_to_copy": "curated repo doctrine plus historical signoff data",
            },
            "sustainability": {
                "defensibility": "workflow memory and trust",
                "switching_costs": "phase history and ledgers",
                "distribution_advantage": "skills.sh-compatible package",
                "data_or_learning_loop": "gate outcomes improve future planning",
                "ecosystem_lock_in": "repo-local artifacts",
                "trust_or_compliance": "explicit evidence records",
            },
            "proof": {
                "local_evidence": ["CLI E2E tests"],
                "market_evidence": ["agent workflow demand"],
                "customer_evidence": ["repo owner pain"],
                "missing_evidence": [],
            },
            "risks": ["generic positioning"],
            "validation_tests": ["third party repeats the moat accurately"],
            "scorecard": {
                "clarity": 4,
                "urgency": 4,
                "differentiation": 4,
                "durability": 4,
                "evidence": 3,
                "third_party_comprehension": 4,
            },
        }

    def test_help_surfaces_all_command_groups(self) -> None:
        output = self.run_cli("--help").stdout
        for group in [
            "init", "registry", "state", "moat", "lifecycle", "ledger", "context",
            "workspace", "thread", "inbox", "profile", "sketch", "hooks", "branch", "undo", "archive", "bible",
        ]:
            self.assertIn(group, output)

        for group in [
            "registry", "state", "moat", "lifecycle", "ledger", "context",
            "workspace", "thread", "inbox", "profile", "sketch", "hooks", "branch", "undo", "archive", "bible",
        ]:
            result = self.run_cli(group, "--help")
            self.assertEqual(result.returncode, 0)

    def test_registry_state_context_and_lifecycle(self) -> None:
        init = self.json_cli("init", "--root", str(self.tmp), "--mode", "brownfield", "--project-name", "Demo", "--format", "json")
        self.assertTrue(pathlib.Path(init["state"]).exists())

        workflows = self.json_cli("registry", "list", "--format", "json")
        self.assertTrue(any(item["workflow"] == "moat" for item in workflows))
        workflow_names = {item["workflow"] for item in workflows}
        for item in workflows:
            for next_workflow in item["next"]:
                self.assertIn(next_workflow, workflow_names)
        self.assertEqual(self.json_cli("registry", "show", "moat", "--format", "json")["moat"]["skill"], "church-moat")
        self.assertEqual(self.json_cli("registry", "show", "survey", "--format", "json")["survey"]["gate"], "survey")
        self.assertIn("agent_owned", self.json_cli("registry", "reasoning", "moat", "--format", "json")["moat"])
        self.assertIn("agent_owned", self.json_cli("registry", "reasoning", "survey", "--format", "json")["survey"])
        self.assertIn("active.workflow", self.json_cli("registry", "keys", "--format", "json"))

        self.assertIn("active", self.json_cli("state", "show", "--root", str(self.tmp), "--format", "json"))
        self.assertEqual(self.json_cli("state", "get", "active.workflow", "--root", str(self.tmp), "--format", "json"), "moat")
        self.json_cli("state", "set", "active.phase", "phase-01", "--root", str(self.tmp), "--format", "json")
        self.assertEqual(self.json_cli("state", "get", "active.phase", "--root", str(self.tmp), "--format", "json"), "phase-01")

        self.assertTrue(any(item["workflow"] == "anchor" for item in self.json_cli("lifecycle", "list", "--format", "json")))
        self.assertEqual(self.json_cli("lifecycle", "show", "anchor", "--format", "json")["anchor"]["gate"], "anchor")
        status = self.json_cli("lifecycle", "status", "--root", str(self.tmp), "--include-history", "--format", "json")
        self.assertEqual(status["active"]["workflow"], "moat")
        self.assertIn("moat_json", status["artifacts"])
        self.json_cli(
            "moat", "import",
            "--root", str(self.tmp),
            "--stdin",
            "--merge",
            "--format", "json",
            input_text=json.dumps(self.seed_complete_moat()),
        )

        preview = self.json_cli("lifecycle", "advance", "bible", "--root", str(self.tmp), "--outcome", "PASS", "--dry-run", "--format", "json")
        self.assertTrue(preview["dry_run"])
        survey_preview = self.json_cli("lifecycle", "advance", "survey", "--root", str(self.tmp), "--outcome", "PASS", "--dry-run", "--format", "json")
        self.assertTrue(survey_preview["dry_run"])
        self.json_cli(
            "lifecycle", "advance", "bible",
            "--root", str(self.tmp),
            "--outcome", "PASS",
            "--evidence", "bible packet registered for test handoff",
            "--artifact", "bible_packet=.church/bible/",
            "--format", "json",
        )
        handoff_path = self.tmp / ".church" / "handoff.md"
        self.json_cli("lifecycle", "handoff", "--root", str(self.tmp), "--output", str(handoff_path), "--format", "markdown")
        self.assertIn("Repo Church Handoff", handoff_path.read_text())

        context = self.run_cli("context", "load", "--root", str(self.tmp), "--format", "markdown", "--include-history").stdout
        self.assertIn("Repo Church Context", context)
        self.assertIn("next_workflows", context)

    def test_moat_commands_and_flags(self) -> None:
        self.json_cli("init", "--root", str(self.tmp), "--mode", "greenfield", "--project-name", "Demo", "--format", "json")
        self.json_cli("moat", "init", "--root", str(self.tmp), "--project-name", "Demo", "--force", "--format", "json")
        incomplete = self.json_cli("moat", "check", "--root", str(self.tmp), "--allow-incomplete", "--format", "json")
        self.assertEqual(incomplete["outcome"], "BLOCK")
        weak_pass = self.run_cli("lifecycle", "advance", "moat", "--root", str(self.tmp), "--outcome", "PASS", "--format", "json", check=False)
        self.assertNotEqual(weak_pass.returncode, 0)
        self.assertIn("moat score is BLOCK", weak_pass.stderr)

        self.json_cli("moat", "set", "elevator_pitch", "Short pitch", "--root", str(self.tmp), "--format", "json")
        exported_md = self.run_cli("moat", "export", "--root", str(self.tmp), "--format", "markdown").stdout
        self.assertIn("Short pitch", exported_md)
        self.assertTrue(exported_md.startswith("# Project Moat"))

        bad_import = self.run_cli("moat", "import", "--root", str(self.tmp), "--format", "json", check=False)
        self.assertNotEqual(bad_import.returncode, 0)
        self.assertIn("requires --stdin or --input", bad_import.stderr)
        complete = json.dumps(self.seed_complete_moat())
        self.json_cli("moat", "import", "--root", str(self.tmp), "--stdin", "--merge", "--format", "json", input_text=complete)
        score = self.json_cli("moat", "check", "--root", str(self.tmp), "--format", "json")
        self.assertIn(score["outcome"], ["PASS", "PASS_WITH_RISK"])
        thin = self.seed_complete_moat()
        thin["schema_version"] = "not-church-moat"
        thin["elevator_pitch"] = "x"
        thin["proof"]["market_evidence"] = ["x"]
        thin["validation_tests"] = ["x"]
        thin_path = self.tmp / "thin-moat.json"
        thin_path.write_text(json.dumps(thin))
        thin_score = self.json_cli("moat", "check", "--root", str(self.tmp), "--input", str(thin_path), "--allow-incomplete", "--format", "json")
        self.assertNotEqual(thin_score["outcome"], "PASS")
        self.assertGreater(len(thin_score["quality_issues"]), 0)

        custom_md = self.tmp / "custom-moat.md"
        self.json_cli("moat", "render", "--root", str(self.tmp), "--output", str(custom_md), "--format", "json")
        self.assertIn("Project Moat", custom_md.read_text())

        custom_json = self.tmp / "exported-moat.json"
        self.json_cli("moat", "export", "--root", str(self.tmp), "--output", str(custom_json), "--format", "json")
        self.assertTrue(custom_json.exists())

    def test_ledger_commands_and_blocker_checks(self) -> None:
        self.json_cli("init", "--root", str(self.tmp), "--format", "json")
        self.json_cli("ledger", "init", "gaps", "--root", str(self.tmp), "--format", "json")
        self.assertTrue(self.json_cli("ledger", "init", "gaps", "--root", str(self.tmp), "--format", "json")["exists"])
        self.json_cli(
            "ledger", "add", "gaps",
            "--root", str(self.tmp),
            "--id", "GAP-1",
            "--summary", "Missing evidence",
            "--status", "open",
            "--severity", "high",
            "--evidence", ".church/moat/moat.md",
            "--owner", "agent",
            "--extra", "workflow=moat",
            "--format", "json",
        )
        blocked = self.json_cli("ledger", "check", "gaps", "--root", str(self.tmp), "--allow-open", "--format", "json")
        self.assertEqual(blocked["outcome"], "HOLD")

        listed = self.run_cli("ledger", "list", "gaps", "--root", str(self.tmp), "--format", "markdown").stdout
        self.assertIn("GAP-1", listed)

        self.json_cli(
            "ledger", "add", "gaps",
            "--root", str(self.tmp),
            "--id", "GAP-1",
            "--summary", "Evidence added",
            "--status", "satisfied",
            "--severity", "high",
            "--evidence", ".church/moat/moat.md",
            "--owner", "agent",
            "--proof", "test passed",
            "--force",
            "--format", "json",
        )
        passed = self.json_cli("ledger", "check", "gaps", "--root", str(self.tmp), "--format", "json")
        self.assertEqual(passed["outcome"], "PASS")
        self.json_cli(
            "ledger", "add", "gaps",
            "--root", str(self.tmp),
            "--id", "GAP-2",
            "--summary", "Closed without proof",
            "--status", "satisfied",
            "--severity", "high",
            "--evidence", ".church/moat/moat.md",
            "--owner", "agent",
            "--format", "json",
        )
        no_proof = self.run_cli("ledger", "check", "gaps", "--root", str(self.tmp), "--format", "json", check=False)
        self.assertNotEqual(no_proof.returncode, 0)
        self.assertGreater(json.loads(no_proof.stdout)["quality_issue_count"], 0)
        reset = self.json_cli("ledger", "init", "gaps", "--root", str(self.tmp), "--force", "--format", "json")
        self.assertIn("ledger", reset)

    def test_bible_delegation_subcommands(self) -> None:
        self.run_cli("bible", "--help")
        inventory = self.json_cli("bible", "inventory", "--root", str(self.tmp), "--format", "json", "--output", "-")
        self.assertEqual(inventory["root"], ".")

        self.run_cli("bible", "scaffold", "--root", str(self.tmp))
        self.assertTrue((self.tmp / ".church" / "bible").exists())

        validate = self.json_cli("bible", "validate", "--root", str(self.tmp), "--format", "json", "--output", "-")
        self.assertIn("error_count", validate)
        self.assertIn("results", validate)

        sources = self.json_cli("bible", "sources", "--root", str(self.tmp), "--format", "json", "--output", "-")
        self.assertIn("urls", sources)
        self.assertIn("link_traversal", sources)

        self.run_cli("bible", "claim-scan", "--root", str(self.tmp), "--path", str(self.tmp), "--banned", "AI magic", "--format", "json", "--output", "-", check=False)
        self.run_cli("bible", "intake-html", "--root", str(self.tmp))
        self.run_cli("bible", "render-html", "--root", str(self.tmp))
        self.assertTrue((self.tmp / ".church" / "bible" / "vision-intake.html").exists())
        self.assertTrue((self.tmp / ".church" / "bible" / "html").exists())

    def test_bible_inventory_excludes_matching_git_status_paths(self) -> None:
        subprocess.run(["git", "init"], cwd=self.tmp, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        legacy_name = "repo" + "-church"
        noisy_dir = self.tmp / legacy_name
        noisy_dir.mkdir()
        (noisy_dir / ".git").mkdir()
        (noisy_dir / "note.md").write_text("local nested checkout noise\n")

        inventory = self.json_cli(
            "bible", "inventory",
            "--root", str(self.tmp),
            "--format", "json",
            "--output", "-",
        )

        self.assertNotIn(legacy_name, "\n".join(inventory["git_status_short"]))

    def test_deferred_parity_cli_groups(self) -> None:
        self.json_cli("init", "--root", str(self.tmp), "--mode", "brownfield", "--project-name", "Demo", "--format", "json")

        workspace = self.json_cli("workspace", "create", "api", "--root", str(self.tmp), "--summary", "API work", "--owner", "agent", "--format", "json")
        self.assertEqual(workspace["workspace"]["name"], "api")
        self.assertEqual(self.json_cli("workspace", "status", "api", "--root", str(self.tmp), "--format", "json")["name"], "api")
        self.assertEqual(self.json_cli("workspace", "switch", "api", "--root", str(self.tmp), "--format", "json")["active_workspace"], "api")
        self.assertEqual(self.json_cli("workspace", "complete", "api", "--root", str(self.tmp), "--format", "json")["workspace"]["status"], "complete")

        thread = self.json_cli("thread", "create", "main", "--root", str(self.tmp), "--runtime", "codex", "--summary", "handoff", "--format", "json")
        self.assertEqual(thread["thread"]["runtime"], "codex")
        self.assertIn("next_command", self.json_cli("thread", "resume", "main", "--root", str(self.tmp), "--format", "json"))
        self.assertEqual(self.json_cli("thread", "complete", "main", "--root", str(self.tmp), "--format", "json")["thread"]["status"], "complete")

        inbox = self.json_cli("inbox", "add", "--root", str(self.tmp), "--id", "IN-1", "--kind", "backlog", "--summary", "Review item", "--severity", "low", "--format", "json")
        self.assertEqual(inbox["item"]["kind"], "backlog")
        self.assertEqual(self.json_cli("inbox", "check", "--root", str(self.tmp), "--allow-open", "--format", "json")["outcome"], "PASS")

        blocked_profile = self.json_cli("profile", "init", "--root", str(self.tmp), "--subject", "user", "--force", "--format", "json")
        self.assertFalse(blocked_profile["consent"])
        self.assertNotEqual(self.run_cli("profile", "check", "--root", str(self.tmp), "--format", "json", check=False).returncode, 0)
        consented_profile = self.json_cli("profile", "init", "--root", str(self.tmp), "--subject", "user", "--purpose", "workflow", "--consent", "--force", "--format", "json")
        self.assertTrue(consented_profile["consent"])
        self.json_cli("profile", "set", "communication.concise", "true", "--root", str(self.tmp), "--format", "json")
        self.assertEqual(self.json_cli("profile", "check", "--root", str(self.tmp), "--format", "json")["outcome"], "PASS")

        sketch = self.json_cli("sketch", "register", "--root", str(self.tmp), "--id", "SK-1", "--path", "design.png", "--summary", "Concept", "--requires-user-signoff", "--format", "json")
        self.assertTrue(sketch["sketch"]["requires_user_signoff"])
        self.assertEqual(self.json_cli("sketch", "check", "--root", str(self.tmp), "--allow-open", "--format", "json")["outcome"], "HOLD")

        hook_plan = self.json_cli("hooks", "plan", "--root", str(self.tmp), "--runtime", "generic", "--format", "json")
        self.assertEqual(hook_plan["detected"], ["generic"])
        hook_scaffold = self.json_cli("hooks", "scaffold", "--root", str(self.tmp), "--runtime", "generic", "--format", "json")
        self.assertTrue(pathlib.Path(hook_scaffold["hook_plan"]).exists())
        self.assertTrue(self.json_cli("hooks", "check", "--root", str(self.tmp), "--runtime", "generic", "--format", "json")["scaffold_exists"])

        branch = self.json_cli("branch", "plan", "--root", str(self.tmp), "--name", "church/test", "--format", "json")
        self.assertTrue(branch["requires_review"])
        undo = self.json_cli("undo", "plan", "--root", str(self.tmp), "--ref", "HEAD", "--format", "json")
        self.assertTrue(undo["requires_review"])
        archive = self.json_cli("archive", "plan", "--root", str(self.tmp), "--format", "json")
        self.assertTrue(archive["dry_run"])

    def test_init_scaffold_bible_flag(self) -> None:
        result = self.json_cli("init", "--root", str(self.tmp), "--mode", "brownfield", "--project-name", "Demo", "--scaffold-bible", "--format", "json")
        self.assertEqual(result["bible_scaffold"]["exit_code"], 0)
        self.assertTrue((self.tmp / ".church" / "bible" / "README.md").exists())

    def test_invalid_transitions_fail_fast_with_actionable_error(self) -> None:
        self.json_cli("init", "--root", str(self.tmp), "--format", "json")
        result = self.run_cli("lifecycle", "advance", "ship", "--root", str(self.tmp), "--outcome", "PASS", "--format", "json", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Allowed next workflows", result.stderr)
        forced = self.run_cli("lifecycle", "advance", "ship", "--root", str(self.tmp), "--outcome", "PASS", "--force", "--format", "json", check=False)
        self.assertNotEqual(forced.returncode, 0)
        self.assertIn("passing gate outcome failed quality checks", forced.stderr)
        invalid_state = self.run_cli("state", "set", "active.workflow", "bogus", "--root", str(self.tmp), "--format", "json", check=False)
        self.assertNotEqual(invalid_state.returncode, 0)
        self.assertIn("active.workflow must be one of", invalid_state.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
