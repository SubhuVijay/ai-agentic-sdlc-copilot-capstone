import json
import subprocess
import sys
import unittest

from hook_loader import hook_script, load_hook

guard_shell = load_hook("guard_shell")


def run_hook(payload: dict) -> dict:
    completed = subprocess.run(
        [sys.executable, str(hook_script("guard_shell"))],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr)
    return json.loads(completed.stdout)


class GuardShellTests(unittest.TestCase):
    def test_ordinary_git_commands_are_allowed(self):
        for command in (
            "git status",
            "git push -u origin HEAD",
            "git push origin feature-flag",
            "git clean -n",
            "git reset HEAD",
        ):
            with self.subTest(command=command):
                self.assertEqual(guard_shell.decide(command)["permissionDecision"], "allow")

    def test_secret_reads_are_denied(self):
        for command in (
            "cat .env",
            "Get-Content .env.local",
            "type .env",
            "Get-Content config/jira.local.json",
            "printenv",
            "Get-ChildItem Env:",
        ):
            with self.subTest(command=command):
                self.assertEqual(guard_shell.decide(command)["permissionDecision"], "deny")

    def test_env_example_read_is_allowed(self):
        self.assertEqual(guard_shell.decide("cat .env.example")["permissionDecision"], "allow")
        self.assertEqual(
            guard_shell.decide("Get-Content .env.sample")["permissionDecision"], "allow"
        )
        self.assertEqual(
            guard_shell.decide("Get-Content config/jira.example.json")["permissionDecision"],
            "allow",
        )

    def test_destructive_git_asks_for_confirmation(self):
        for command in (
            "git push --force",
            "git push --force-with-lease",
            "git push origin main -f",
            "git reset --hard",
            "git clean -fd",
            "git clean --force",
        ):
            with self.subTest(command=command):
                self.assertEqual(guard_shell.decide(command)["permissionDecision"], "ask")

    def test_decision_is_mirrored_for_vs_code(self):
        decision = guard_shell.decide("cat .env")
        specific = decision["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "PreToolUse")
        self.assertEqual(specific["permissionDecision"], "deny")

    def test_cli_payload_with_tool_args_string(self):
        output = run_hook(
            {"toolName": "powershell", "toolArgs": json.dumps({"command": "Get-Content .env"})}
        )
        self.assertEqual(output["permissionDecision"], "deny")

    def test_vs_code_payload_with_tool_input_object(self):
        output = run_hook(
            {"tool_name": "run_in_terminal", "tool_input": {"command": "git status"}}
        )
        self.assertEqual(output["permissionDecision"], "allow")

    def test_malformed_input_fails_open(self):
        completed = subprocess.run(
            [sys.executable, str(hook_script("guard_shell"))],
            input="not json",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["permissionDecision"], "allow")


if __name__ == "__main__":
    unittest.main()
