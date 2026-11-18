import json
import subprocess
import sys
import unittest

from hook_loader import hook_script, load_hook

guard_secrets = load_hook("guard_secrets")


class GuardSecretsTests(unittest.TestCase):
    def test_secret_files_are_denied(self):
        for path in (
            ".env",
            ".env.local",
            "config/.env.production",
            "credentials.json",
            "config/jira.local.json",
            "deploy/server.pem",
            "certs/client.pfx",
            "home/user/.ssh/config",
            "id_ed25519",
        ):
            with self.subTest(path=path):
                self.assertEqual(guard_secrets.decide(path)["permissionDecision"], "deny")

    def test_ordinary_and_example_files_are_allowed(self):
        for path in (
            ".env.example",
            ".env.sample",
            "README.md",
            "src/doc_sync/snapshot.py",
            "docs/user-story.md",
            "",
        ):
            with self.subTest(path=path):
                self.assertEqual(guard_secrets.decide(path)["permissionDecision"], "allow")

    def test_cli_and_vs_code_payloads(self):
        for payload, expected in (
            ({"toolName": "view", "toolArgs": json.dumps({"path": ".env"})}, "deny"),
            ({"tool_name": "read_file", "tool_input": {"filePath": "id_rsa"}}, "deny"),
            ({"tool_name": "read_file", "tool_input": {"filePath": "README.md"}}, "allow"),
            ({"tool_name": "run_in_terminal", "tool_input": {"command": "git status"}}, "allow"),
        ):
            with self.subTest(payload=payload):
                completed = subprocess.run(
                    [sys.executable, str(hook_script("guard_secrets"))],
                    input=json.dumps(payload),
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(json.loads(completed.stdout)["permissionDecision"], expected)


if __name__ == "__main__":
    unittest.main()
