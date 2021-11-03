
.PHONY: format
format:
	poetry run black .
	poetry run isort .

