# SonarQube Issue Fix Documentation

This document provides the before/after comparison required by the assignment.

## Intentional issues

The intentionally problematic code is stored in:

```text
examples/issues_before.py
```

To create a failing SonarQube run for screenshots, temporarily copy it into the analyzed source folder:

```bash
cp examples/issues_before.py src/sonarqube_code_quality/issues_before.py
pytest --cov=src --cov-report=xml
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="<YOUR_TOKEN>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

After taking the failing Quality Gate screenshot, remove the copied file:

```bash
rm src/sonarqube_code_quality/issues_before.py
pytest --cov=src --cov-report=xml
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="<YOUR_TOKEN>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

## Before/after table

| Issue Type | Before | After | Severity |
|---|---|---|---|
| Bug | `data.split(",")` was called without validating whether `data` was `None`. | `process_csv_items` accepts `str | None` and returns an empty result for `None`. | Major |
| Security Hotspot | Password was hardcoded as `"admin123"`. | `get_required_secret` reads secrets from environment variables. | Critical |
| Code Smell | A bare `except:` caught every exception. | `run_safely` catches only expected `RuntimeError` and `ValueError`. | Major |
| Code Smell | The exception handler used `pass`, silently hiding failures. | Failures are logged and the function returns a clear boolean status. | Major |
| Maintainability | The function had no type hints or clear return model. | Type hints and a `ProcessedData` dataclass make behavior explicit. | Minor |
| Code Smell | Unused variable `debug_mode` remained in the function. | Removed unused variables. | Minor |
| Code Smell | Duplicate loops repeated the same cleanup logic. | A single list comprehension performs deterministic normalization. | Minor |

## Final clean implementation

The final fixed implementation is in:

```text
src/sonarqube_code_quality/data_processor.py
```

This version is covered by tests in:

```text
tests/test_data_processor.py
```
