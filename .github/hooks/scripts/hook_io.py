"""Shared stdin/stdout handling for GitHub Copilot hooks.

Copilot CLI and the coding agent send camelCase fields (toolName, toolArgs as a
JSON string). VS Code sends snake_case fields (tool_name, tool_input as an
object). Both shapes are accepted, and decisions are written in both shapes.
"""

import json
import sys
from typing import Callable, Iterable


def read_payload() -> dict:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def tool_args(payload: dict) -> dict:
    args = payload.get("toolArgs", payload.get("tool_input", {}))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return {}
    return args if isinstance(args, dict) else {}


def first_string(args: dict, keys: Iterable[str]) -> str:
    for key in keys:
        value = args.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def permission(decision: str, reason: str = "") -> dict:
    result = {"permissionDecision": decision}
    if reason:
        result["permissionDecisionReason"] = reason
    result["hookSpecificOutput"] = {"hookEventName": "PreToolUse", **result}
    return result


def session_context(text: str) -> dict:
    return {
        "additionalContext": text,
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text},
    }


def emit(output: dict) -> None:
    json.dump(output, sys.stdout)
    sys.stdout.write("\n")


def run(handler: Callable[[dict], dict]) -> None:
    try:
        emit(handler(read_payload()))
    except Exception:
        emit({})
