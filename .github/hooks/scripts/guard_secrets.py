#!/usr/bin/env python3
"""preToolUse hook: block file tools that target secret or credential files."""

from pathlib import Path

from hook_io import first_string, permission, run, tool_args

ALLOWED_ENV_NAMES = {".env.example", ".env.sample"}
KEY_NAMES = {
    "credentials.json",
    "jira.local.json",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
    "id_ecdsa",
}
KEY_SUFFIXES = (".pem", ".p12", ".pfx", ".key")
PATH_KEYS = ("path", "filePath", "file_path", "filename", "uri")


def is_sensitive(file_path: str) -> bool:
    path = Path(file_path)
    name = path.name.lower()
    if name in ALLOWED_ENV_NAMES:
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    if name in KEY_NAMES or name.endswith(KEY_SUFFIXES):
        return True
    return ".ssh" in {part.lower() for part in path.parts}


def decide(file_path: str) -> dict:
    if file_path and is_sensitive(file_path):
        return permission("deny", "Blocked access to a secret or credential file.")
    return permission("allow")


def handle(payload: dict) -> dict:
    return decide(first_string(tool_args(payload), PATH_KEYS))


if __name__ == "__main__":
    run(handle)
