"""Validation and selection for holds that have exceeded their pickup window."""

from __future__ import annotations

import logging
import re
from datetime import date
from typing import Iterable

DEFAULT_DAYS = 7
_POSITIVE_INTEGER = re.compile(r"[0-9]+\Z")
_LOGGER = logging.getLogger(__name__)


def validate_days(value: str | None) -> int:
    """Validate a supplied window value, or return the default when absent."""
    if value is None:
        return DEFAULT_DAYS
    if not _POSITIVE_INTEGER.fullmatch(value):
        raise ValueError("days must be a positive integer")
    days = int(value)
    if days <= 0:
        raise ValueError("days must be a positive integer")
    return days


def select_overdue(
    holds: Iterable[dict],
    days: int = DEFAULT_DAYS,
    today: date | None = None,
) -> list[dict]:
    """Return ready holds waiting strictly longer than ``days`` calendar days."""
    current_date = date.today() if today is None else today
    overdue: list[dict] = []
    for hold in holds:
        if hold.get("status") != "ready" or not hold.get("readySince"):
            continue
        ready_since = hold["readySince"]
        if not isinstance(ready_since, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", ready_since
        ):
            _LOGGER.warning("Excluding a hold with malformed readySince")
            continue
        try:
            ready_date = date.fromisoformat(ready_since)
        except ValueError:
            _LOGGER.warning("Excluding a hold with malformed readySince")
            continue

        waiting_days = (current_date - ready_date).days
        if waiting_days <= days:
            continue
        overdue.append({
            "id": hold["id"],
            "title": hold["title"],
            "patron": hold["patron"],
            "readySince": ready_since,
            "status": hold["status"],
            "phone": hold.get("phone") if hold.get("phone") is not None else "Not Found",
            "waitingDays": waiting_days,
        })
    return overdue
