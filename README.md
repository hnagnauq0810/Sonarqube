# SonarQube Code Quality Assignment

This repository implements the **Continuous Code Quality with SonarQube** assignment.

It includes:

- A Python 3.11+ project with tests.
- `sonar-project.properties`.
- Local SonarQube analysis with Docker.
- GitHub Actions workflow for SonarQube scanning.
- Quality Gate enforcement.
- Before/after documentation for at least 5 fixed code issues.
- A separate Vietnamese guide: [`HUONG_DAN_THUC_HIEN.md`](HUONG_DAN_THUC_HIEN.md).

## Project structure

```text
sonarqube-code-quality/
├── .github/workflows/sonarqube.yml
├── docs/
│   └── ISSUE_FIXES.md
├── examples/
│   └── issues_before.py
├── src/
│   └── sonarqube_code_quality/
│       ├── __init__.py
│       ├── calculator.py
│       └── data_processor.py
├── tests/
│   ├── test_calculator.py
│   └── test_data_processor.py
├── pyproject.toml
├── sonar-project.properties
├── README.md
└── HUONG_DAN_THUC_HIEN.md
```

## Prerequisites

Install:

- Docker
- Python 3.11+
- Git
- VS Code or PyCharm with SonarLint, optional bonus

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run tests and coverage

```bash
pytest --cov=src --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml
```

Expected result:

- Tests pass.
- `coverage.xml` is created.
- Coverage is above 80%.

## Run lint and format checks

```bash
black --check src tests
ruff check src tests
```

To auto-format:

```bash
black src tests
ruff check src tests --fix
```

## Start SonarQube locally

Run:

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  sonarqube:2026.1-community
```

Check logs:

```bash
docker logs -f sonarqube
```

Open:

```text
http://localhost:9000
```

Default credentials:

```text
Username: admin
Password: admin
```

After login:

1. Change the admin password.
2. Create a project manually.
3. Use project key: `sonarqube-code-quality`.
4. Generate a project analysis token.
5. Store the token securely.

## SonarQube project configuration

The project uses this file:

```text
sonar-project.properties
```

Important settings:

```properties
sonar.projectKey=sonarqube-code-quality
sonar.projectName=SonarQube Code Quality
sonar.sources=src
sonar.tests=tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
```

## Run local SonarQube analysis

First generate coverage:

```bash
pytest --cov=src --cov-report=xml --cov-report=term-missing
```

Then run scanner.

For macOS/Windows Docker Desktop:

```bash
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="<YOUR_TOKEN>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

For Linux:

```bash
docker run --rm \
  --network host \
  -e SONAR_HOST_URL="http://localhost:9000" \
  -e SONAR_TOKEN="<YOUR_TOKEN>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

## GitHub Actions integration

Workflow file:

```text
.github/workflows/sonarqube.yml
```

It does the following:

1. Runs on push to `main`.
2. Runs on pull requests targeting `main`.
3. Installs Python dependencies.
4. Runs Black and Ruff.
5. Runs tests with coverage.
6. Uploads coverage/test artifacts.
7. Executes SonarQube scan.
8. Waits for Quality Gate result.
9. Fails the workflow if Quality Gate fails.

### Required GitHub secrets

Go to:

```text
GitHub repository -> Settings -> Secrets and variables -> Actions
```

Create:

| Secret | Value |
|---|---|
| `SONAR_TOKEN` | Token generated in SonarQube |
| `SONAR_HOST_URL` | Example: `http://localhost:9000` for self-hosted runner |

### Important note about local SonarQube and GitHub Actions

If SonarQube is running on your laptop at `localhost:9000`, GitHub-hosted runners cannot access it.

Use one of these options:

1. Recommended for this assignment: install a GitHub self-hosted runner on your machine.
2. Expose SonarQube using a secure tunnel such as ngrok or Cloudflare Tunnel.
3. Use SonarCloud instead of local SonarQube, if your instructor accepts it.

This project uses:

```yaml
runs-on: self-hosted
```

because it is designed for local SonarQube.

## Quality Gate

Create a custom Quality Gate in SonarQube with these conditions:

| Condition | Required value |
|---|---|
| New Bugs | `= 0` |
| New Vulnerabilities | `= 0` |
| New Code Coverage | `>= 80%` |
| New Duplicated Lines | `<= 3%` |

Apply this Quality Gate to the project.

## How to create a failing Quality Gate screenshot

The final source code is clean. To demonstrate a failing gate:

```bash
cp examples/issues_before.py src/sonarqube_code_quality/issues_before.py
pytest --cov=src --cov-report=xml --cov-report=term-missing
```

Run SonarQube scanner again.

Take a screenshot of the failed Quality Gate.

Then restore the project:

```bash
rm src/sonarqube_code_quality/issues_before.py
pytest --cov=src --cov-report=xml --cov-report=term-missing
```

Run SonarQube scanner again and take a passing Quality Gate screenshot.

## Fixed issues documentation

See:

```text
docs/ISSUE_FIXES.md
```

Summary:

| Issue Type | Before | After | Severity |
|---|---|---|---|
| Bug | Called `.split()` without validating `None`. | Added validation for `str | None`. | Major |
| Security Hotspot | Hardcoded password. | Read secret from environment variable. | Critical |
| Code Smell | Bare `except:`. | Catch specific exceptions. | Major |
| Code Smell | Silent `pass` in exception handler. | Log failure and return status. | Major |
| Maintainability | No type hints or return model. | Added type hints and dataclass. | Minor |

## SonarLint bonus

For the bonus:

1. Install SonarLint in VS Code or PyCharm.
2. Connect SonarLint to your SonarQube server.
3. Bind the IDE project to `sonarqube-code-quality`.
4. Take a screenshot showing SonarLint connected and analyzing the project.

## Submission checklist

Submit:

- GitHub repository URL.
- Source code with `sonar-project.properties`.
- `.github/workflows/sonarqube.yml`.
- Screenshot of SonarQube dashboard.
- Screenshot of successful project analysis.
- Screenshot of Quality Gate pass.
- Screenshot of Quality Gate fail.
- Screenshot of GitHub Actions workflow.
- Documentation of fixed issues: `docs/ISSUE_FIXES.md`.
- README and `HUONG_DAN_THUC_HIEN.md`.
- Optional bonus screenshot: SonarLint connected to SonarQube.
