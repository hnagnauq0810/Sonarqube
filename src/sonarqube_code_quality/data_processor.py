"""Clean implementation used after fixing SonarQube issues."""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessedData:
    """Summary returned after parsing comma-separated text."""

    total_items: int
    unique_items: int
    normalized_items: list[str]


def process_csv_items(data: str | None) -> ProcessedData:
    """Parse a comma-separated string into a normalized summary.

    The intentionally broken version of this function is documented in
    examples/issues_before.py. This version fixes the original issues by adding
    input validation, type hints, deterministic normalization, and test coverage.
    """
    if data is None:
        return ProcessedData(total_items=0, unique_items=0, normalized_items=[])

    if not isinstance(data, str):
        raise TypeError("data must be a string or None")

    normalized_items = [item.strip().lower() for item in data.split(",") if item.strip()]
    return ProcessedData(
        total_items=len(normalized_items),
        unique_items=len(set(normalized_items)),
        normalized_items=normalized_items,
    )


def get_required_secret(environment_variable: str) -> str:
    """Read a required secret from the environment.

    This avoids hardcoded credentials and gives a clear error when the secret is
    missing.
    """
    secret = os.getenv(environment_variable)
    if not secret or not secret.strip():
        raise RuntimeError(f"{environment_variable} is not configured")
    return secret


def run_safely(operation: Callable[[], None]) -> bool:
    """Run an operation and report whether it succeeded.

    Only expected operational exceptions are caught. Unexpected exceptions are
    allowed to propagate so they are visible during debugging and testing.
    """
    try:
        operation()
    except (RuntimeError, ValueError) as exc:
        logger.warning("Operation failed: %s", exc)
        return False

    return True
