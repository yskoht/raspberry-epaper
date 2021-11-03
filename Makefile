PYTHON := python


.PHONY: format
format:
	poetry run black .
	poetry run isort .


.PHONY: lint
lint:
	poetry run flake8 --ignore=E501,W503 raspberry_epaper


.PHONY: build
build:
	poetry build


.PHONY: clean
clean:
	rm -rf ./dist


.PHONY: bump-version
bump-version:
	poetry version minor
	git add pyproject.toml
	git commit -m 'Bump version'


.PHONY: publish
publish: clean build
	poetry publish


.PHONY: setup
setup:
	poetry install


.PHONY: setup-poetry
setup-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -
