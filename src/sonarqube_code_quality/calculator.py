"""Small calculation helpers used by the sample project."""


def divide(numerator: float, denominator: float) -> float:
    """Return numerator divided by denominator.

    Raises:
        ValueError: If denominator is zero.
    """
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


def percentage(part: float, total: float) -> float:
    """Return the percentage value for part / total."""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)
