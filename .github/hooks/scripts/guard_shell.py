#!/usr/bin/env python3
"""preToolUse hook: gate destructive git and secret dumps in terminal tools."""

import re

from hook_io import first_string, permission, run, tool_args

READ_VERBS = re.compile(
    r"\b(type|cat|more|less|head|tail|gc|Get-Content|Select-String)\b",
    re.IGNORECASE,
)
DUMP_ENV = re.compile(
    r"\bprintenv\b|Get-ChildItem\s+Env:|gci\s+Env:|ls\s+Env:",
    re.IGNORECASE,
)
GIT_PUSH = re.compile(r"\bgit(\.exe)?\s+(-C\s+\S+\s+)?push\b", re.IGNORECASE)
GIT_RESET_HARD = re.compile(
    r"\bgit(\.exe)?\s+(-C\s+\S+\s+)?reset\s+--hard\b",
    re.IGNORECASE,
)
GIT_CLEAN_FORCE = re.compile(
    r"\bgit(\.exe)?\s+(-C\s+\S+\s+)?clean\b[^\n]*(\s-\w*f\w*|\s--force\b)",
    re.IGNORECASE,
)
FORCE_FLAG = re.compile(
    r"(?<![\w-])(--force-with-lease|--force)(?![\w-])|\s-\w*f\w*"
)


def reads_dotenv(command: str) -> bool:
    if READ_VERBS.search(command) is None:
        return False
    scrubbed = re.sub(r"\.env\.(example|sample)\b", "", command, flags=re.IGNORECASE)
    return re.search(r"\.env\b", scrubbed, re.IGNORECASE) is not None


def reads_jira_local_config(command: str) -> bool:
    if READ_VERBS.search(command) is None:
        return False
    return re.search(r"jira\.local\.json\b", command, re.IGNORECASE) is not None


def is_force_push(command: str) -> bool:
    match = GIT_PUSH.search(command)
    if match is None:
        return False
    return FORCE_FLAG.search(command[match.end() :]) is not None


def decide(command: str) -> dict:
    if reads_dotenv(command) or reads_jira_local_config(command) or DUMP_ENV.search(command) is not None:
        return permission(
            "deny",
            "Blocked a command that would print secrets or environment values. "
            ".env.example and config/jira.example.json are safe to read.",
        )
    if is_force_push(command) or GIT_RESET_HARD.search(command) or GIT_CLEAN_FORCE.search(command):
        return permission(
            "ask",
            "This command can rewrite history or delete files. Confirm before continuing.",
        )
    return permission("allow")


def handle(payload: dict) -> dict:
    return decide(first_string(tool_args(payload), ("command", "cmd", "script")))


if __name__ == "__main__":
    run(handle)
