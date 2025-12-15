SHELL := bash
.ONESHELL:


PHONY: install
install: ## Install dependencies
	uv sync


.PHONY: test
test:
	uv run pytest -v --cov-report term-missing --disable-warnings --cov=app tests/


.PHONY: lint
lint:
	@echo "Running Ruff linter..."
	uv run --only-group lint ruff check --fix
