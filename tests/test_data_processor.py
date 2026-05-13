import pytest

from sonarqube_code_quality.data_processor import (
    ProcessedData,
    get_required_secret,
    process_csv_items,
    run_safely,
)


def test_process_csv_items_normalizes_and_counts_values() -> None:
    result = process_csv_items(" Apple, banana, apple, , ORANGE ")

    assert result == ProcessedData(
        total_items=4,
        unique_items=3,
        normalized_items=["apple", "banana", "apple", "orange"],
    )


def test_process_csv_items_handles_none() -> None:
    assert process_csv_items(None) == ProcessedData(
        total_items=0,
        unique_items=0,
        normalized_items=[],
    )


def test_process_csv_items_rejects_invalid_type() -> None:
    with pytest.raises(TypeError, match="string or None"):
        process_csv_items(123)  # type: ignore[arg-type]


def test_get_required_secret_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_SECRET", "safe-secret-from-env")

    assert get_required_secret("APP_SECRET") == "safe-secret-from-env"


def test_get_required_secret_fails_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("APP_SECRET", raising=False)

    with pytest.raises(RuntimeError, match="APP_SECRET"):
        get_required_secret("APP_SECRET")


def test_run_safely_returns_true_for_successful_operation() -> None:
    called = False

    def operation() -> None:
        nonlocal called
        called = True

    assert run_safely(operation) is True
    assert called is True


def test_run_safely_handles_expected_runtime_errors() -> None:
    def operation() -> None:
        raise RuntimeError("temporary failure")

    assert run_safely(operation) is False


def test_run_safely_does_not_hide_unexpected_errors() -> None:
    def operation() -> None:
        raise TypeError("programming error")

    with pytest.raises(TypeError, match="programming error"):
        run_safely(operation)
