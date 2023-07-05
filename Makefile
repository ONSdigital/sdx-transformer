
.PHONY: build
build: ## Install pipfile dependencies
	python3 -m venv venv
	. venv/bin/activate
	python3 --version
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: start
start: build ## Start program
	python run.py

.PHONY: dev_dependencies
dev_dependencies: build
	pip install -r test-requirements.txt

.PHONY: lint
lint: dev_dependencies
	flake8 . --count --statistics

.PHONY: test
test: lint
	pytest -v --cov-report term-missing --disable-warnings --cov=app tests/
