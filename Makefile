lint:
	poetry run flake8 page_loader

install:
	poetry install

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

build:
	poetry build

publish:
	poetry publish --dry-run

test:
	poetry run pytest
