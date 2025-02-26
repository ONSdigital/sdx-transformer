SHELL := bash
.ONESHELL:


.PHONY: test
test:
	poetry install \
	&& poetry run flake8 . --count --statistics \
	&& poetry run pytest -n auto -v --cov-report term-missing --disable-warnings --cov=app tests/
