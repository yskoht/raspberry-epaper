
.PHONY: format
format:
	poetry run black .
	poetry run isort .

.PHONY: lint
lint:
	poetry run flake8 --ignore=E501 raspberry_epaper

