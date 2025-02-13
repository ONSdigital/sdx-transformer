SHELL := bash
.ONESHELL:


.PHONY: test
test:
	# poetry install \
# 	&& poetry run flake8 . --count --statistics \
 	pytest -v --cov-report term-missing --disable-warnings --cov=app tests/
