install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

test:
	pytest --cov=src --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml

lint:
	black --check src tests
	ruff check src tests

format:
	black src tests
	ruff check src tests --fix

sonarqube-up:
	docker run -d --name sonarqube -p 9000:9000 -v sonarqube_data:/opt/sonarqube/data sonarqube:2026.1-community

sonarqube-logs:
	docker logs -f sonarqube
