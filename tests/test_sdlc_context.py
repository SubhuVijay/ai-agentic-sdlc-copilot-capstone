import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from hook_loader import hook_script, load_hook

sdlc_context = load_hook("sdlc_context")


class GateReportTests(unittest.TestCase):
    def test_missing_gates_point_at_requirements(self):
        with tempfile.TemporaryDirectory() as directory:
            report = sdlc_context.gate_report(Path(directory))
        self.assertIn("Step 1 — Requirements: missing", report)
        self.assertIn("Next gate: Step 1 — Requirements", report)
        self.assertIn("docs/user-story.md", report)
        self.assertIn("Orchestrator:", report)
        self.assertIn(".github/agents/", report)

    def test_next_gate_is_the_first_missing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            report = sdlc_context.gate_report(root)
        self.assertIn("Step 1 — Requirements: present", report)
        self.assertIn("Next gate: Step 2 — Architecture", report)

    def test_completed_planning_gates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (
                "requirements.md",
                "architecture.md",
                "design-review.md",
                "impl-plan.md",
            ):
                (root / name).write_text("# done\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "user-story.md").write_text("# story\n", encoding="utf-8")
            report = sdlc_context.gate_report(root)
        self.assertIn("Planning gates are present", report)
        self.assertIn("Story input: present", report)

    def test_cli_emits_additional_context_in_both_shapes(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, str(hook_script("sdlc_context"))],
                input=json.dumps({"timestamp": 0, "cwd": directory, "source": "new"}),
                text=True,
                capture_output=True,
                encoding="utf-8",
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertIn("Step 1 — Requirements", payload["additionalContext"])
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("Step 1 — Requirements", payload["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
