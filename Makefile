.PHONY: init lint test audit-certs scan-orphans iam-hygiene full-dossier clean

init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

lint:
	ruff check src/ tests/
	mypy src/

test:
	pytest tests/ -v --tb=short

audit-certs:
	python -m src.operator.cli audit-certs

scan-orphans:
	python -m src.operator.cli scan-orphans

iam-hygiene:
	python -m src.operator.cli iam-hygiene

full-dossier:
	python -m src.operator.cli full-dossier --output-file=CLOUD_ASSET_LIFECYCLE_REPORT.json

clean:
	rm -rf .pytest_cache .mypy_cache dist/ build/ CLOUD_ASSET_LIFECYCLE_REPORT.json
