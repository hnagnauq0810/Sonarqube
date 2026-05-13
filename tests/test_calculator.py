import pytest

from sonarqube_code_quality.calculator import divide, percentage


def test_divide_returns_result() -> None:
    assert divide(10, 2) == 5


def test_divide_rejects_zero_denominator() -> None:
    with pytest.raises(ValueError, match="denominator"):
        divide(10, 0)


def test_percentage_returns_rounded_value() -> None:
    assert percentage(1, 3) == 33.33


def test_percentage_returns_zero_when_total_is_zero() -> None:
    assert percentage(10, 0) == 0.0
