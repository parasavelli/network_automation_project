# Makefile for network_automation_project

PYTHON := python3

help:
	@echo "make install       - install all requirements"
	@echo "make lint          - run formatting and lint checks"
	@echo "make test          - run unit tests with coverage"
	@echo "make run           - run CLI with local config"
	@echo "make docker-run    - run CLI inside Docker container"
	@echo "make check         - run full pre-commit and mypy checks"

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r requirements-dev.txt

lint:
	ruff check .
	isort . --check-only
	black . --check
	mypy .

test:
	pytest tests/ --cov=src --cov-report=term-missing

run:
	PYTHONPATH=. $(PYTHON) scripts/run_ssh_backup.py --devices-file=src/config/devices.yaml

docker-run:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running."; exit 1)
	docker build -t ssh-backup .
	docker run --rm \
		-v $$PWD/configs:/app/configs \
		--env-file .env \
		ssh-backup --devices-file=src/config/devices.yaml

check:
	pre-commit run --all-files --show-diff-on-failure
